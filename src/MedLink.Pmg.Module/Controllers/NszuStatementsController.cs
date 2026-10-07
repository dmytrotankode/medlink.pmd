using MedLink.Pmg.Module.Data;
using MedLink.Pmg.Module.Models;
using MedLink.Pmg.Module.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace MedLink.Pmg.Module.Controllers;

/// <summary>Звіти НСЗУ: імпорт (OpenXML SAX), перегляд 45 колонок, 2-Way звірка, зведення</summary>
[ApiController]
[Route("api/v1/nszu/statements")]
public class NszuStatementsController : ControllerBase
{
    private readonly PmgDbContext _db;
    private readonly INszuStatementXlsxProcessor _processor;
    private readonly ReconciliationService _reconciliation;
    private readonly MedLinkDemoDataService _demo;
    private readonly AnalyticsService _analytics;
    private readonly IConfiguration _cfg;
    private readonly IHostEnvironment _env;

    public NszuStatementsController(PmgDbContext db, INszuStatementXlsxProcessor processor, ReconciliationService reconciliation, MedLinkDemoDataService demo, AnalyticsService analytics, IConfiguration cfg, IHostEnvironment env)
    { _db = db; _processor = processor; _reconciliation = reconciliation; _demo = demo; _analytics = analytics; _cfg = cfg; _env = env; }

    /// <summary>Список імпортованих звітів (історія)</summary>
    [HttpGet]
    public async Task<IActionResult> List([FromQuery] Guid? organizationId, [FromQuery] int take = 50)
    {
        var q = _db.Statements.AsNoTracking().Where(s => s.RecordState == 2);
        if (organizationId.HasValue) q = q.Where(s => s.OrganizationId == organizationId);
        var list = await q.OrderByDescending(s => s.ImportedAt).Take(take).ToListAsync();
        var orgs = await _db.LegalEntities.AsNoTracking().ToDictionaryAsync(o => o.Id, o => o);
        return Ok(list.Select(s => new { statement = s, organization = orgs.GetValueOrDefault(s.OrganizationId) }));
    }

    [HttpGet("history")]
    public Task<IActionResult> History([FromQuery] int take = 20) => List(null, take);

    [HttpGet("{id:guid}")]
    public async Task<IActionResult> Get(Guid id)
    {
        var s = await _db.Statements.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        if (s == null) return NotFound(new { error = "Звіт не знайдено" });
        var org = await _db.LegalEntities.AsNoTracking().FirstOrDefaultAsync(o => o.Id == s.OrganizationId);
        return Ok(new { statement = s, organization = org });
    }

    /// <summary>Завантаження та потоковий парсинг файлу звіту (.xlsx, multipart/form-data: file, organizationId?, isMountain?, generateDemo?, reconcile?)</summary>
    [HttpPost("upload")]
    [RequestSizeLimit(512L * 1024 * 1024)]
    [RequestFormLimits(MultipartBodyLengthLimit = 512L * 1024 * 1024)]
    public async Task<IActionResult> Upload([FromForm] IFormFile? file, [FromForm] Guid? organizationId, [FromForm] bool isMountain = false, [FromForm] bool generateDemo = true, [FromForm] bool reconcile = true, [FromForm] string? fileName = null, CancellationToken ct = default)
    {
        Stream stream; string name; long size;
        if (file != null && file.Length > 0)
        {
            var uploads = DatabaseSeeder.ResolvePath(_env.ContentRootPath, _cfg["Pmg:UploadsPath"] ?? "App_Data/uploads");
            Directory.CreateDirectory(uploads);
            var saved = Path.Combine(uploads, $"{DateTime.UtcNow:yyyyMMdd_HHmmss}_{Path.GetFileName(file.FileName)}");
            await using (var fs = System.IO.File.Create(saved)) await file.CopyToAsync(fs, ct);
            stream = System.IO.File.OpenRead(saved); name = file.FileName; size = file.Length;
        }
        else if (!string.IsNullOrEmpty(fileName))
        {
            var path = ResolveSample(fileName);
            if (path == null) return BadRequest(new { error = $"Файл {fileName} не знайдено у каталозі зразків" });
            stream = System.IO.File.OpenRead(path); name = Path.GetFileName(path); size = new FileInfo(path).Length;
        }
        else return BadRequest(new { error = "Файл звіту НСЗУ не надано (поле form-data «file» або «fileName» зразка)" });

        try
        {
            StatementImportResult result;
            await using (stream) result = await _processor.ProcessAsync(stream, name, size, organizationId, isMountain, null, ct);
            object? demo = null, rec = null;
            if (generateDemo && _cfg.GetValue("Pmg:GenerateMedLinkDemoEntities", true)) demo = await _demo.EnsureDemoEntitiesAsync(result.StatementId, ct);
            if (reconcile) rec = await _reconciliation.ReconcileAsync(result.StatementId, ct);
            result.Reconciliation = rec;
            return Ok(new { result, demoEntities = demo, message = $"Звіт «{name}» проаналізовано: {result.TotalRecords} ЕМЗ, відхилено {result.RejectedRecords}, втрачено {PmgTariffCalculatorService.Money(result.LostRevenueUah)}" });
        }
        catch (InvalidDataException ex) { return BadRequest(new { error = ex.Message }); }
    }

    /// <summary>Імпорт одного з вбудованих реальних звітів (зразків) за назвою</summary>
    [HttpPost("process-sample")]
    public Task<IActionResult> ProcessSample([FromQuery] string fileName, [FromQuery] bool isMountain = false, CancellationToken ct = default)
        => Upload(null, null, isMountain, true, true, fileName, ct);

    [HttpGet("samples")]
    public IActionResult Samples()
    {
        var names = _cfg.GetSection("Pmg:SampleReports").Get<string[]>() ?? Array.Empty<string>();
        return Ok(names.Select(n => { var p = ResolveSample(n); return new { fileName = n, exists = p != null, sizeBytes = p != null ? new FileInfo(p).Length : 0 }; }));
    }

    private string? ResolveSample(string fileName)
    {
        var root = DatabaseSeeder.ResolvePath(_env.ContentRootPath, _cfg["Pmg:SampleReportsPath"] ?? "../..");
        foreach (var dir in new[] { root, Path.Combine(root, "medlink_pmg_bundle", "sample_reports"), DatabaseSeeder.ResolvePath(_env.ContentRootPath, _cfg["Pmg:UploadsPath"] ?? "App_Data/uploads") })
        {
            var p = Path.Combine(dir, Path.GetFileName(fileName));
            if (System.IO.File.Exists(p)) return p;
        }
        return null;
    }

    /// <summary>Рядки звіту (аудит 45 колонок) з фільтрами та пагінацією</summary>
    [HttpGet("{id:guid}/lines")]
    public async Task<IActionResult> Lines(Guid id, [FromQuery] string? status, [FromQuery] string? package, [FromQuery] string? search, [FromQuery] string? errorCategory, [FromQuery] int? matchStatus, [FromQuery] string? doctor, [FromQuery] string? emzType, [FromQuery] int page = 1, [FromQuery] int pageSize = 50, [FromQuery] string? sort = "lineNumber", [FromQuery] bool desc = false)
    {
        var q = _analytics.AuditQuery(id, status, package, search, errorCategory, matchStatus, doctor, emzType);
        var total = await q.CountAsync();
        q = sort switch
        {
            "tariff" => desc ? q.OrderByDescending(l => l.MisAmount) : q.OrderBy(l => l.MisAmount),
            "lost" => desc ? q.OrderByDescending(l => l.LostRevenue) : q.OrderBy(l => l.LostRevenue),
            "doctor" => desc ? q.OrderByDescending(l => l.PractitionerName) : q.OrderBy(l => l.PractitionerName),
            "date" => desc ? q.OrderByDescending(l => l.PeriodStart) : q.OrderBy(l => l.PeriodStart),
            _ => desc ? q.OrderByDescending(l => l.LineNumber) : q.OrderBy(l => l.LineNumber),
        };
        pageSize = Math.Clamp(pageSize, 1, 1000);
        var items = await q.Skip((page - 1) * pageSize).Take(pageSize).ToListAsync();
        return Ok(new { statementId = id, total, page, pageSize, items });
    }

    [HttpGet("{id:guid}/lines/{lineId:guid}")]
    public async Task<IActionResult> Line(Guid id, Guid lineId)
    {
        var l = await _db.StatementLines.AsNoTracking().FirstOrDefaultAsync(x => x.Id == lineId && x.StatementId == id);
        if (l == null) return NotFound();
        var enc = l.MatchedEncounterId != null ? await _db.Encounters.AsNoTracking().FirstOrDefaultAsync(e => e.Id == l.MatchedEncounterId) : null;
        var disc = await _db.Discrepancies.AsNoTracking().FirstOrDefaultAsync(d => d.StatementLineId == lineId);
        return Ok(new { line = l, columns = ColumnTitles, encounter = enc, discrepancy = disc });
    }

    public static readonly string[] ColumnTitles =
    {
        "Звітний рік", "Звітний місяць", "Тип ЕМЗ", "ID ЕМЗ", "Внесено до ЕСОЗ", "Посада медичного працівника (виконавця)", "Медичний працівник (виконавець)", "Місце надання послуг", "Тип направлення",
        "Код ЄДРПОУ закладу, де видано направлення", "Посада лікаря, який видав направлення", "ID епізоду", "Тип епізоду", "Дата та час початку епізоду / госпіталізації", "Дата та час початку періоду / забору",
        "Дата та час кінця періоду / виписки", "Тривалість лікування, днів", "Основний діагноз", "Статус достовірності основного діагнозу", "Клінічний статус основного діагнозу", "Додаткові / супутні діагнози",
        "Спростовані та помилкові додаткові діагнози", "Перелік інтервенцій (послуги / діагностика)", "Клас взаємодії", "Пріоритет", "Тип взаємодії", "Підстава звернення в стаціонар", "Результат лікування (виписки)",
        "Унікальний код пацієнта", "Наявність декларації", "Стать пацієнта", "Вік пацієнта", "Додаткова інформація з ЕМЗ", "АДСГ", "Пакет послуг", "Номер послуги", "Включення до статистики", "Включення до звіту",
        "Коментар щодо виявлених помилок", "Деталі виявлених помилок (JSON)", "Деталі невідповідностей (верифікація)", "Деталі помилок / конфліктів при групуванні", "Деталі перегляду НСЗУ", "Додаткові коментарі / зауваження", "Дата перегляду НСЗУ",
    };

    /// <summary>Запуск 2-Way звірки з ЕМЗ МІС «Медлінк» (повторний запуск перебудовує нові розбіжності)</summary>
    [HttpPost("{id:guid}/reconcile")]
    public async Task<IActionResult> Reconcile(Guid id, [FromQuery] bool generateDemo = false, CancellationToken ct = default)
    {
        if (!await _db.Statements.AnyAsync(s => s.Id == id, ct)) return NotFound(new { error = "Звіт не знайдено" });
        object? demo = generateDemo ? await _demo.EnsureDemoEntitiesAsync(id, ct) : null;
        var res = await _reconciliation.ReconcileAsync(id, ct);
        return Ok(new { res.StatementId, res.Status, res.ReconciledAt, res.TotalChecked, res.MatchedPaidCount, res.DiscrepancyRejectedCount, res.MissingInMisCount, res.MissingInNhsuCount, res.MissingInNhsuAmountUah, res.LostRevenueUah, res.PotentialRecoveryUah, res.DiscrepanciesCreated, res.Message, demoEntities = demo });
    }

    [HttpGet("{id:guid}/summary")]
    public async Task<IActionResult> Summary(Guid id, CancellationToken ct)
    {
        try { return Ok(await _analytics.SummaryAsync(id, ct)); }
        catch (KeyNotFoundException) { return NotFound(); }
    }

    [HttpGet("{id:guid}/doctors-summary")]
    public async Task<IActionResult> Doctors(Guid id, CancellationToken ct) => Ok(await _analytics.DoctorsSummaryAsync(id, ct));

    [HttpGet("{id:guid}/errors-summary")]
    public async Task<IActionResult> Errors(Guid id, CancellationToken ct) => Ok(await _analytics.ErrorsSummaryAsync(id, ct));

    [HttpGet("{id:guid}/patients")]
    public async Task<IActionResult> Patients(Guid id, [FromQuery] string? package, [FromQuery] string? search, [FromQuery] int page = 1, [FromQuery] int pageSize = 50)
    {
        var q = _db.StatementPatients.AsNoTracking().Where(p => p.StatementId == id);
        if (!string.IsNullOrEmpty(package)) q = q.Where(p => p.PackageNumber == package);
        if (!string.IsNullOrEmpty(search)) q = q.Where(p => (p.PatientIdHash != null && p.PatientIdHash.StartsWith(search)) || (p.ServiceNumber != null && p.ServiceNumber.Contains(search)) || (p.ServiceStatus != null && p.ServiceStatus.Contains(search)));
        var total = await q.CountAsync();
        var items = await q.OrderBy(p => p.PatientIdHash).Skip((page - 1) * pageSize).Take(Math.Clamp(pageSize, 1, 500)).ToListAsync();
        var byPkg = await _db.StatementPatients.AsNoTracking().Where(p => p.StatementId == id).GroupBy(p => new { p.PackageNumber, p.ServiceNumber, p.IncludedInStats })
            .Select(g => new { g.Key.PackageNumber, g.Key.ServiceNumber, g.Key.IncludedInStats, count = g.Count() }).OrderByDescending(x => x.count).ToListAsync();
        return Ok(new { total, page, pageSize, items, byService = byPkg });
    }

    [HttpGet("{id:guid}/report-rows")]
    public async Task<IActionResult> ReportRows(Guid id) => Ok(await _db.StatementReportRows.AsNoTracking().Where(r => r.StatementId == id).OrderBy(r => r.CreatedOn).ToListAsync());

    /// <summary>Видалення звіту разом з рядками, розбіжностями та результатами (каскадно)</summary>
    [HttpDelete("{id:guid}")]
    public async Task<IActionResult> Delete(Guid id, [FromQuery] bool hard = true)
    {
        var s = await _db.Statements.FirstOrDefaultAsync(x => x.Id == id);
        if (s == null) return NotFound();
        if (!hard) { s.RecordState = 4; s.Status = "Archived"; s.ModifiedOn = DateTime.UtcNow; await _db.SaveChangesAsync(); return Ok(new { archived = true }); }
        await _db.Discrepancies.Where(d => d.StatementId == id).ExecuteDeleteAsync();
        await _db.StatementPatients.Where(d => d.StatementId == id).ExecuteDeleteAsync();
        await _db.StatementReportRows.Where(d => d.StatementId == id).ExecuteDeleteAsync();
        await _db.AnalysisResults.Where(a => a.StatementLineId != null && _db.StatementLines.Any(l => l.Id == a.StatementLineId && l.StatementId == id)).ExecuteDeleteAsync();
        await _db.StatementLines.Where(d => d.StatementId == id).ExecuteDeleteAsync();
        _db.Statements.Remove(s);
        await _db.SaveChangesAsync();
        return Ok(new { deleted = true });
    }

    /// <summary>Зміна статусу звіту (Reconciled → Archived тощо)</summary>
    [HttpPost("{id:guid}/status")]
    public async Task<IActionResult> SetStatus(Guid id, [FromBody] StatusChange body)
    {
        var s = await _db.Statements.FirstOrDefaultAsync(x => x.Id == id);
        if (s == null) return NotFound();
        if (!Workflows.CanTransition(Workflows.Statement, s.Status, body.Status)) return BadRequest(new { error = $"Перехід {s.Status} → {body.Status} не дозволено", allowed = Workflows.Statement.GetValueOrDefault(s.Status) });
        s.Status = body.Status; s.ModifiedOn = DateTime.UtcNow;
        await _db.SaveChangesAsync();
        return Ok(s);
    }
}

public class StatusChange { public string Status { get; set; } = string.Empty; public string? Note { get; set; } public Guid? UserId { get; set; } public string? Role { get; set; } }
