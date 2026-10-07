using MedLink.Pmg.Module.Data;
using MedLink.Pmg.Module.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace MedLink.Pmg.Module.Controllers;

/// <summary>Службові: стан системи, довідкова інформація про стенд, ролі та процеси</summary>
[ApiController]
[Route("api/v1/system")]
public class SystemController : ControllerBase
{
    private readonly PmgDbContext _db;
    private readonly ITariffCatalogProvider _catalog;
    private readonly IConfiguration _cfg;
    public SystemController(PmgDbContext db, ITariffCatalogProvider catalog, IConfiguration cfg) { _db = db; _catalog = catalog; _cfg = cfg; }

    [HttpGet("health")]
    public async Task<IActionResult> Health() => Ok(new { status = "ok", utc = DateTime.UtcNow, database = _db.Database.GetDbConnection().DataSource, canConnect = await _db.Database.CanConnectAsync() });

    [HttpGet("info")]
    public async Task<IActionResult> Info()
    {
        var cat = await _catalog.GetAsync();
        return Ok(new
        {
            product = "MedLink PMG-2026 Analytics (автономний стенд)", version = "4.0.0", stack = ".NET 8 / EF Core 8 (SQLite → PostgreSQL) / Quasar 1.15.3 + Vue 2", authorization = "none (стенд)",
            tariffSettings = cat.Settings, packageRules = cat.PackageRules.Count, catalogLoadedAt = cat.LoadedAt,
            roles = Roles, processes = Processes,
        });
    }

    [HttpPost("catalog/reload")]
    public async Task<IActionResult> Reload() { _catalog.Invalidate(); var c = await _catalog.GetAsync(); return Ok(new { reloaded = true, c.LoadedAt }); }

    /// <summary>Повне скидання стенду: видалення звітів, ЕМЗ, розбіжностей (довідники лишаються)</summary>
    [HttpPost("reset-transactional-data")]
    public async Task<IActionResult> Reset([FromQuery] bool confirm = false)
    {
        if (!confirm) return BadRequest(new { error = "Передайте confirm=true" });
        await _db.ResyncQueue.ExecuteDeleteAsync(); await _db.Discrepancies.ExecuteDeleteAsync(); await _db.AnalysisResults.ExecuteDeleteAsync();
        await _db.StatementLines.ExecuteDeleteAsync(); await _db.StatementPatients.ExecuteDeleteAsync(); await _db.StatementReportRows.ExecuteDeleteAsync(); await _db.Statements.ExecuteDeleteAsync();
        await _db.Encounters.ExecuteDeleteAsync(); await _db.Patients.ExecuteDeleteAsync(); await _db.Employees.ExecuteDeleteAsync(); await _db.Departments.ExecuteDeleteAsync(); await _db.LegalEntities.ExecuteDeleteAsync();
        return Ok(new { reset = true });
    }

    public static readonly object[] Roles =
    {
        new { code = "Doctor", name = "Лікар (стаціонар / амбулаторія)", processes = new[] { "P1", "P5", "P7" }, screens = new[] { "АРМ лікаря: картка ЕМЗ", "Пре-білінг та Anti-Defektura", "Комбінатор послуг", "Мої розбіжності" } },
        new { code = "Economist", name = "Економіст / монітор ПМГ", processes = new[] { "P2", "P3", "P4", "P5", "P6" }, screens = new[] { "Імпорт звіту НСЗУ", "Аудит 45 колонок", "2-Way звірка", "Журнал розбіжностей", "Черга переподання" } },
        new { code = "ChiefPhysician", name = "Начмед / головний лікар", processes = new[] { "P3", "P4", "P6" }, screens = new[] { "Дашборд закладу", "Звіт за лікарями та відділеннями", "Рейтинг дефектури" } },
        new { code = "Admin", name = "Адміністратор МІС", processes = new[] { "P8" }, screens = new[] { "Довідники ПМГ", "Налаштування тарифів", "Правила валідації", "Сутності Медлінка" } },
    };

    public static readonly object[] Processes =
    {
        new { code = "P1", name = "Пре-білінг та онлайн-контроль у картці лікаря", roles = new[] { "Doctor" }, api = new[] { "POST /api/v1/medlink/encounters", "POST /api/v1/pmg/prebilling/evaluate", "POST /api/v1/medlink/encounters/{id}/status (Signed)" } },
        new { code = "P2", name = "Імпорт та потоковий парсинг звіту НСЗУ (4 аркуші, 45 колонок)", roles = new[] { "Economist" }, api = new[] { "POST /api/v1/nszu/statements/upload", "GET /api/v1/nszu/statements/{id}" } },
        new { code = "P3", name = "Автономний розрахунок тарифів ПМГ-2026 та аудит 45 колонок", roles = new[] { "Economist", "ChiefPhysician" }, api = new[] { "GET /api/v1/nszu/statements/{id}/lines", "GET /api/v1/pmg/analytics/audit-grid", "GET /api/v1/nszu/statements/{id}/summary" } },
        new { code = "P4", name = "2-Way звірка з ЕМЗ Медлінка та прихована дефектура", roles = new[] { "Economist" }, api = new[] { "POST /api/v1/nszu/statements/{id}/reconcile", "GET /api/v1/pmg/analytics/discrepancies" } },
        new { code = "P5", name = "Асистент виправлення, коригування ЕМЗ в 1 клік, черга переподання в ЕСОЗ", roles = new[] { "Economist", "Doctor" }, api = new[] { "POST /api/v1/pmg/analytics/apply-correction", "POST /api/v1/pmg/analytics/discrepancies/{id}/status", "POST /api/v1/pmg/analytics/resync-queue/{id}/status" } },
        new { code = "P6", name = "Звіт за лікарями та відділеннями (аркуш «Звіт»)", roles = new[] { "ChiefPhysician", "Economist" }, api = new[] { "GET /api/v1/nszu/statements/{id}/doctors-summary" } },
        new { code = "P7", name = "Матриця комбінацій, мультихірургія 1.30, бібліотека еталонів myAddLib", roles = new[] { "Doctor" }, api = new[] { "POST /api/v1/pmg/combinations/validate", "POST /api/v1/pmg/combinations/library-save" } },
        new { code = "P8", name = "Адміністрування довідників, тарифів, правил та сутностей Медлінка", roles = new[] { "Admin" }, api = new[] { "GET/PUT /api/v1/pmg/dictionaries/tariff-settings", "CRUD /api/v1/pmg/dictionaries/package-rules", "CRUD /api/v1/medlink/*" } },
    };
}
