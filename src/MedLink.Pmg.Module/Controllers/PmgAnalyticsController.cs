using System.Text.Json;
using MedLink.Pmg.Module.Data;
using MedLink.Pmg.Module.Models;
using MedLink.Pmg.Module.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace MedLink.Pmg.Module.Controllers;

/// <summary>Аналітика ПМГ: аудит-грід, звіт за лікарями, журнал розбіжностей (Lost Revenue), асистент виправлення, черга ресинхронізації</summary>
[ApiController]
[Route("api/v1/pmg/analytics")]
public class PmgAnalyticsController : ControllerBase
{
    private readonly PmgDbContext _db;
    private readonly AnalyticsService _analytics;
    private readonly CorrectionService _correction;
    private readonly RecommendationEngine _recommender;

    public PmgAnalyticsController(PmgDbContext db, AnalyticsService analytics, CorrectionService correction, RecommendationEngine recommender)
    { _db = db; _analytics = analytics; _correction = correction; _recommender = recommender; }

    /// <summary>Пагінована таблиця 45 колонок із розрахованими тарифами</summary>
    [HttpGet("audit-grid")]
    public async Task<IActionResult> AuditGrid([FromQuery] Guid statementId, [FromQuery] string? status, [FromQuery] string? package, [FromQuery] string? search, [FromQuery] int page = 1, [FromQuery] int pageSize = 50)
    {
        var q = _analytics.AuditQuery(statementId, status, package, search, null, null, null, null);
        var total = await q.CountAsync();
        var items = await q.OrderBy(l => l.LineNumber).Skip((page - 1) * pageSize).Take(Math.Clamp(pageSize, 1, 500)).ToListAsync();
        return Ok(new
        {
            totalItems = total, page, pageSize,
            items = items.Select(l => new
            {
                id = l.Id, lineNumber = l.LineNumber, emzId = l.EncounterEhealthId, emzType = l.EmzType, date = l.PeriodStart, docName = l.PractitionerName, docPosition = l.PractitionerPosition,
                package = l.PackageNumber, packageName = l.PackageName, diagMain = l.PrimaryIcd10Code, diagText = l.PrimaryDiagnosis, services = l.Interventions, dsgCode = l.DsgCode, weightCoef = l.WeightCoef,
                calculatedTariff = l.MisAmount, lostRevenue = l.LostRevenue, recoverable = l.RecoverableAmount, included = l.IncludedInReport, errorComment = l.ErrorComment, errorCode = l.ErrorCode, errorCategory = l.ErrorCategory,
                matchStatus = l.MatchStatus, matchStatusName = ((MatchStatus)l.MatchStatus).ToString(), matchedEncounterId = l.MatchedEncounterId,
                colValues45 = string.IsNullOrEmpty(l.RawPayloadJson) ? null : JsonSerializer.Deserialize<string?[]>(l.RawPayloadJson),
            }),
            columnTitles = NszuStatementsController.ColumnTitles,
        });
    }

    [HttpGet("doctors-summary")]
    public async Task<IActionResult> DoctorsSummary([FromQuery] Guid statementId, CancellationToken ct) => Ok(await _analytics.DoctorsSummaryAsync(statementId, ct));

    [HttpGet("summary")]
    public async Task<IActionResult> Summary([FromQuery] Guid statementId, CancellationToken ct)
    {
        try { return Ok(await _analytics.SummaryAsync(statementId, ct)); } catch (KeyNotFoundException) { return NotFound(); }
    }

    /// <summary>Зведення по всіх звітах закладів (дашборд керівника)</summary>
    [HttpGet("overview")]
    public async Task<IActionResult> Overview()
    {
        var statements = await _db.Statements.AsNoTracking().Where(s => s.RecordState == 2).OrderByDescending(s => s.PeriodFrom).ToListAsync();
        var orgs = await _db.LegalEntities.AsNoTracking().ToDictionaryAsync(o => o.Id, o => o);
        var open = await _db.Discrepancies.AsNoTracking().Where(d => d.Status == "New" || d.Status == "InProgress").GroupBy(d => d.StatementId).Select(g => new { g.Key, count = g.Count(), recoverable = g.Sum(x => x.RecoverableAmount) }).ToDictionaryAsync(x => x.Key, x => x);
        var queue = await _db.ResyncQueue.AsNoTracking().GroupBy(q => q.Status).Select(g => new { status = g.Key, count = g.Count() }).ToListAsync();
        return Ok(new
        {
            totals = new
            {
                statements = statements.Count, records = statements.Sum(s => s.TotalRecords), rejected = statements.Sum(s => s.RejectedRecords),
                accrued = statements.Sum(s => s.DirectPayAmount + s.GlobalBudgetAmount), lost = statements.Sum(s => s.LostRevenueAmount), recoverable = statements.Sum(s => s.RecoverableAmount), hidden = statements.Sum(s => s.MissingInNhsuAmount),
                encounters = await _db.Encounters.CountAsync(e => e.RecordState == 2), employees = await _db.Employees.CountAsync(e => e.RecordState == 2), patients = await _db.Patients.CountAsync(p => p.RecordState == 2),
            },
            statements = statements.Select(s => new { statement = s, organization = orgs.GetValueOrDefault(s.OrganizationId), openDiscrepancies = open.GetValueOrDefault(s.Id)?.count ?? 0, openRecoverable = open.GetValueOrDefault(s.Id)?.recoverable ?? 0 }),
            resyncQueue = queue,
        });
    }

    // ---------------------------------------------------------------- discrepancies

    [HttpGet("discrepancies")]
    public async Task<IActionResult> Discrepancies([FromQuery] Guid? statementId, [FromQuery] string? status, [FromQuery] string? type, [FromQuery] string? category, [FromQuery] string? search, [FromQuery] Guid? employeeId, [FromQuery] int page = 1, [FromQuery] int pageSize = 50)
    {
        var q = _db.Discrepancies.AsNoTracking().Where(d => d.RecordState == 2);
        if (statementId.HasValue) q = q.Where(d => d.StatementId == statementId);
        if (!string.IsNullOrEmpty(status) && status != "all") q = q.Where(d => d.Status == status);
        if (!string.IsNullOrEmpty(type) && type != "all") q = q.Where(d => d.DiscrepancyType == type);
        if (!string.IsNullOrEmpty(category) && category != "all") q = q.Where(d => d.ErrorCategory == category);
        if (employeeId.HasValue) q = q.Where(d => d.EmployeeId == employeeId);
        if (!string.IsNullOrEmpty(search)) q = q.Where(d => (d.NszuComment != null && d.NszuComment.Contains(search)) || (d.PrimaryIcd10Code != null && d.PrimaryIcd10Code.StartsWith(search)) || (d.Caption != null && d.Caption.Contains(search)));
        var total = await q.CountAsync();
        var items = await q.OrderByDescending(d => d.LostAmount).Skip((page - 1) * pageSize).Take(Math.Clamp(pageSize, 1, 500)).ToListAsync();
        var empIds = items.Where(i => i.EmployeeId != null).Select(i => i.EmployeeId!.Value).Distinct().ToList();
        var emps = await _db.Employees.AsNoTracking().Where(e => empIds.Contains(e.Id)).ToDictionaryAsync(e => e.Id, e => e);
        var lineIds = items.Where(i => i.StatementLineId != null).Select(i => i.StatementLineId!.Value).ToList();
        var lines = await _db.StatementLines.AsNoTracking().Where(l => lineIds.Contains(l.Id)).Select(l => new { l.Id, l.PractitionerName, l.PractitionerPosition, l.PrimaryDiagnosis, l.Interventions, l.PeriodStart, l.EmzType, l.PatientAge, l.PatientGender }).ToDictionaryAsync(l => l.Id, l => l);
        var categories = await _db.Discrepancies.AsNoTracking().Where(d => d.RecordState == 2 && (!statementId.HasValue || d.StatementId == statementId)).GroupBy(d => d.ErrorCategory).Select(g => new { category = g.Key ?? "—", count = g.Count(), lost = g.Sum(x => x.LostAmount) }).OrderByDescending(x => x.count).ToListAsync();
        return Ok(new
        {
            total, page, pageSize, categories,
            items = items.Select(d => new
            {
                discrepancy = d, employee = d.EmployeeId != null ? emps.GetValueOrDefault(d.EmployeeId.Value) : null, line = d.StatementLineId != null ? lines.GetValueOrDefault(d.StatementLineId.Value) : null,
                recommendation = string.IsNullOrEmpty(d.RecommendationJson) ? (JsonElement?)null : JsonSerializer.Deserialize<JsonElement>(d.RecommendationJson),
                allowedTransitions = Workflows.Discrepancy.GetValueOrDefault(d.Status) ?? Array.Empty<string>(),
            }),
        });
    }

    [HttpGet("discrepancies/{id:guid}")]
    public async Task<IActionResult> Discrepancy(Guid id)
    {
        var d = await _db.Discrepancies.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        if (d == null) return NotFound();
        var line = d.StatementLineId != null ? await _db.StatementLines.AsNoTracking().FirstOrDefaultAsync(l => l.Id == d.StatementLineId) : null;
        var enc = d.EncounterId != null ? await _db.Encounters.AsNoTracking().FirstOrDefaultAsync(e => e.Id == d.EncounterId) : null;
        var emp = d.EmployeeId != null ? await _db.Employees.AsNoTracking().FirstOrDefaultAsync(e => e.Id == d.EmployeeId) : null;
        var dept = d.DepartmentId != null ? await _db.Departments.AsNoTracking().FirstOrDefaultAsync(e => e.Id == d.DepartmentId) : null;
        var pat = d.PatientId != null ? await _db.Patients.AsNoTracking().FirstOrDefaultAsync(e => e.Id == d.PatientId) : null;
        var error = d.ErrorCode != null ? await _db.ErrorDictionary.AsNoTracking().FirstOrDefaultAsync(e => e.ErrorCode == d.ErrorCode) : null;
        var official = d.NszuComment != null ? await _db.ErrorDescriptions.AsNoTracking().FirstOrDefaultAsync(e => e.CommentText == d.NszuComment) : null;
        var queue = await _db.ResyncQueue.AsNoTracking().Where(q => q.DiscrepancyId == id).OrderByDescending(q => q.CreatedOn).ToListAsync();
        return Ok(new
        {
            discrepancy = d, line, encounter = enc, employee = emp, department = dept, patient = pat, errorDictionary = error, officialDescription = official, resyncQueue = queue,
            recommendation = string.IsNullOrEmpty(d.RecommendationJson) ? (JsonElement?)null : JsonSerializer.Deserialize<JsonElement>(d.RecommendationJson),
            correction = string.IsNullOrEmpty(d.CorrectionJson) ? (JsonElement?)null : JsonSerializer.Deserialize<JsonElement>(d.CorrectionJson),
            allowedTransitions = Workflows.Discrepancy.GetValueOrDefault(d.Status) ?? Array.Empty<string>(),
        });
    }

    /// <summary>Перегенерувати рекомендацію асистента для розбіжності</summary>
    [HttpPost("discrepancies/{id:guid}/recommend")]
    public async Task<IActionResult> Recommend(Guid id)
    {
        var d = await _db.Discrepancies.FirstOrDefaultAsync(x => x.Id == id);
        if (d == null) return NotFound();
        var line = d.StatementLineId != null ? await _db.StatementLines.AsNoTracking().FirstOrDefaultAsync(l => l.Id == d.StatementLineId) : null;
        var enc = d.EncounterId != null ? await _db.Encounters.AsNoTracking().FirstOrDefaultAsync(e => e.Id == d.EncounterId) : null;
        Recommendation rec = line != null ? _recommender.Build(line, enc) : enc != null ? _recommender.BuildHidden(enc, d.LostAmount) : new Recommendation { Title = "Недостатньо даних" };
        d.RecommendationJson = JsonSerializer.Serialize(rec); d.ModifiedOn = DateTime.UtcNow;
        await _db.SaveChangesAsync();
        return Ok(rec);
    }

    /// <summary>Зміна статусу розбіжності за workflow (New → InProgress → Corrected → Resubmitted → Closed / Dismissed)</summary>
    [HttpPost("discrepancies/{id:guid}/status")]
    public async Task<IActionResult> DiscrepancyStatus(Guid id, [FromBody] StatusChange body)
    {
        var d = await _db.Discrepancies.FirstOrDefaultAsync(x => x.Id == id);
        if (d == null) return NotFound();
        if (!Workflows.CanTransition(Workflows.Discrepancy, d.Status, body.Status))
            return BadRequest(new { error = $"Перехід {d.Status} → {body.Status} не дозволено", allowed = Workflows.Discrepancy.GetValueOrDefault(d.Status) });
        d.Status = body.Status; d.ModifiedOn = DateTime.UtcNow; d.ModifiedBy = body.UserId ?? Guid.Empty;
        if (body.Status == "Resubmitted" && d.EncounterId != null)
        {
            var enc = await _db.Encounters.FirstOrDefaultAsync(e => e.Id == d.EncounterId);
            if (enc != null && Workflows.CanTransition(Workflows.Encounter, enc.Status, "Resubmitted")) { enc.Status = "Resubmitted"; enc.ModifiedOn = DateTime.UtcNow; }
        }
        await _db.SaveChangesAsync();
        return Ok(new { d.Id, d.Status, allowed = Workflows.Discrepancy.GetValueOrDefault(d.Status) });
    }

    [HttpDelete("discrepancies/{id:guid}")]
    public async Task<IActionResult> DeleteDiscrepancy(Guid id)
    {
        var d = await _db.Discrepancies.FirstOrDefaultAsync(x => x.Id == id);
        if (d == null) return NotFound();
        d.RecordState = 4; d.Status = "Dismissed"; d.ModifiedOn = DateTime.UtcNow;
        await _db.SaveChangesAsync();
        return Ok(new { deleted = true });
    }

    /// <summary>Виправлення в 1 клік: застосувати рекомендацію / ручні зміни до ЕМЗ Медлінка і поставити в чергу переподання</summary>
    [HttpPost("apply-correction")]
    public async Task<IActionResult> ApplyCorrection([FromBody] ApplyCorrectionRequest req, CancellationToken ct)
    {
        try { return Ok(await _correction.ApplyAsync(req, ct)); }
        catch (KeyNotFoundException ex) { return NotFound(new { error = ex.Message }); }
    }

    /// <summary>Пакетне застосування рекомендацій до всіх нових розбіжностей звіту з довірою ≥ minConfidence</summary>
    [HttpPost("apply-corrections/batch")]
    public async Task<IActionResult> ApplyBatch([FromQuery] Guid statementId, [FromQuery] decimal minConfidence = 0.7m, [FromQuery] int limit = 200, CancellationToken ct = default)
    {
        var items = await _db.Discrepancies.AsNoTracking().Where(d => d.StatementId == statementId && d.Status == "New" && d.EncounterId != null && d.RecommendationJson != null).Take(limit).ToListAsync(ct);
        int applied = 0; decimal expected = 0;
        foreach (var d in items)
        {
            var rec = JsonSerializer.Deserialize<Recommendation>(d.RecommendationJson!, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
            if (rec == null || rec.Confidence < minConfidence || rec.Action is "ManualReview" or "RemoveDuplicate") continue;
            var r = await _correction.ApplyAsync(new ApplyCorrectionRequest { DiscrepancyId = d.Id, AcceptRecommendation = true, Note = "Пакетне застосування рекомендації асистента" }, ct);
            applied++; expected += rec.ExpectedRevenue;
        }
        return Ok(new { statementId, candidates = items.Count, applied, expectedRevenueUah = Math.Round(expected, 2) });
    }

    // ---------------------------------------------------------------- analysis results & resync queue

    [HttpGet("analysis-results")]
    public async Task<IActionResult> AnalysisResults([FromQuery] Guid? encounterId, [FromQuery] Guid? employeeId, [FromQuery] int take = 100)
    {
        var q = _db.AnalysisResults.AsNoTracking().AsQueryable();
        if (encounterId.HasValue) q = q.Where(a => a.EncounterId == encounterId);
        if (employeeId.HasValue) q = q.Where(a => a.EmployeeId == employeeId);
        return Ok(await q.OrderByDescending(a => a.AnalyzedAt).Take(take).ToListAsync());
    }

    [HttpGet("resync-queue")]
    public async Task<IActionResult> ResyncQueue([FromQuery] string? status, [FromQuery] int take = 200)
    {
        var q = _db.ResyncQueue.AsNoTracking().Where(x => x.RecordState == 2);
        if (!string.IsNullOrEmpty(status) && status != "all") q = q.Where(x => x.Status == status);
        var items = await q.OrderByDescending(x => x.CreatedOn).Take(take).ToListAsync();
        var encIds = items.Select(i => i.EncounterId).Distinct().ToList();
        var encs = await _db.Encounters.AsNoTracking().Where(e => encIds.Contains(e.Id)).ToDictionaryAsync(e => e.Id, e => e);
        return Ok(items.Select(i => new { item = i, encounter = encs.GetValueOrDefault(i.EncounterId), allowedTransitions = Workflows.Resync.GetValueOrDefault(i.Status) ?? Array.Empty<string>() }));
    }

    /// <summary>Перехід статусу елемента черги (Queued → SignedKep → Sent → Accepted / Failed). Емуляція КЕП та відправки в ЕСОЗ.</summary>
    [HttpPost("resync-queue/{id:guid}/status")]
    public async Task<IActionResult> ResyncStatus(Guid id, [FromBody] StatusChange body)
    {
        var q = await _db.ResyncQueue.FirstOrDefaultAsync(x => x.Id == id);
        if (q == null) return NotFound();
        if (!Workflows.CanTransition(Workflows.Resync, q.Status, body.Status)) return BadRequest(new { error = $"Перехід {q.Status} → {body.Status} не дозволено", allowed = Workflows.Resync.GetValueOrDefault(q.Status) });
        q.Status = body.Status; q.ModifiedOn = DateTime.UtcNow;
        if (body.Status == "Sent") { q.SentAt = DateTime.UtcNow; q.Attempts++; }
        if (body.Status == "Failed") q.LastError = body.Note;
        var enc = await _db.Encounters.FirstOrDefaultAsync(e => e.Id == q.EncounterId);
        if (enc != null)
        {
            if (body.Status == "Sent" && Workflows.CanTransition(Workflows.Encounter, enc.Status, "Resubmitted")) enc.Status = "Resubmitted";
            if (body.Status == "Accepted" && Workflows.CanTransition(Workflows.Encounter, enc.Status, "Accepted")) enc.Status = "Accepted";
            if (body.Status == "SignedKep") { enc.IsSigned = true; enc.SignedAt = DateTime.UtcNow; }
        }
        if (body.Status == "Accepted" && q.DiscrepancyId != null)
        {
            var d = await _db.Discrepancies.FirstOrDefaultAsync(x => x.Id == q.DiscrepancyId);
            if (d != null && Workflows.CanTransition(Workflows.Discrepancy, d.Status, "Resubmitted")) d.Status = "Resubmitted";
        }
        await _db.SaveChangesAsync();
        return Ok(new { q.Id, q.Status, encounterStatus = enc?.Status, allowed = Workflows.Resync.GetValueOrDefault(q.Status) });
    }

    [HttpDelete("resync-queue/{id:guid}")]
    public async Task<IActionResult> DeleteQueue(Guid id)
    {
        var q = await _db.ResyncQueue.FirstOrDefaultAsync(x => x.Id == id);
        if (q == null) return NotFound();
        _db.ResyncQueue.Remove(q); await _db.SaveChangesAsync();
        return Ok(new { deleted = true });
    }

    /// <summary>Матриця життєвих циклів та ролей (для UI та документації)</summary>
    [HttpGet("workflows")]
    public IActionResult WorkflowsInfo() => Ok(new { encounter = Workflows.Encounter, discrepancy = Workflows.Discrepancy, statement = Workflows.Statement, resync = Workflows.Resync, rolesForTransition = Workflows.RolesForTransition });
}
