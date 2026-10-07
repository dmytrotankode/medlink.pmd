using System.Text.Json;
using MedLink.Pmg.Module.Data;
using MedLink.Pmg.Module.Models;
using Microsoft.EntityFrameworkCore;

namespace MedLink.Pmg.Module.Services;

/// <summary>
/// Життєві цикли (статусні моделі) сутностей модуля та правила переходів.
/// Ролі: Doctor (лікар), Economist (економіст / монітор ПМГ), ChiefPhysician (начмед / головний лікар), Admin (адміністратор МІС).
/// </summary>
public static class Workflows
{
    public static readonly Dictionary<string, string[]> Encounter = new()
    {
        ["Draft"] = new[] { "Signed", "Deleted" },
        ["Signed"] = new[] { "Submitted", "Draft" },
        ["Submitted"] = new[] { "Accepted", "Rejected", "Corrected" },
        ["Accepted"] = new[] { "Corrected" },
        ["Rejected"] = new[] { "Corrected", "Draft" },
        ["Corrected"] = new[] { "Resubmitted", "Signed" },
        ["Resubmitted"] = new[] { "Accepted", "Rejected" },
    };
    public static readonly Dictionary<string, string[]> Discrepancy = new()
    {
        ["New"] = new[] { "InProgress", "Corrected", "Dismissed" },
        ["InProgress"] = new[] { "Corrected", "Dismissed", "New" },
        ["Corrected"] = new[] { "Resubmitted", "InProgress" },
        ["Resubmitted"] = new[] { "Closed", "InProgress" },
        ["Dismissed"] = new[] { "New" },
        ["Closed"] = Array.Empty<string>(),
    };
    public static readonly Dictionary<string, string[]> Statement = new()
    {
        ["Uploaded"] = new[] { "Parsing", "Failed" },
        ["Parsing"] = new[] { "Tariffed", "Failed" },
        ["Tariffed"] = new[] { "Reconciled" },
        ["Reconciled"] = new[] { "Reconciled", "Archived" },
        ["Failed"] = new[] { "Uploaded" },
        ["Archived"] = new[] { "Reconciled" },
    };
    public static readonly Dictionary<string, string[]> Resync = new()
    {
        ["Queued"] = new[] { "SignedKep", "Cancelled" },
        ["SignedKep"] = new[] { "Sent", "Failed" },
        ["Sent"] = new[] { "Accepted", "Failed" },
        ["Failed"] = new[] { "Queued", "Cancelled" },
        ["Accepted"] = Array.Empty<string>(),
        ["Cancelled"] = new[] { "Queued" },
    };

    /// <summary>Хто може виконувати перехід (інформаційно, без авторизації у стенді)</summary>
    public static readonly Dictionary<string, string[]> RolesForTransition = new()
    {
        ["Encounter:Signed"] = new[] { "Doctor" }, ["Encounter:Submitted"] = new[] { "Doctor", "Admin" }, ["Encounter:Corrected"] = new[] { "Doctor", "Economist" },
        ["Encounter:Resubmitted"] = new[] { "Doctor" }, ["Discrepancy:InProgress"] = new[] { "Economist", "ChiefPhysician" }, ["Discrepancy:Corrected"] = new[] { "Doctor", "Economist" },
        ["Discrepancy:Resubmitted"] = new[] { "Doctor" }, ["Discrepancy:Dismissed"] = new[] { "Economist", "ChiefPhysician" }, ["Discrepancy:Closed"] = new[] { "Economist" },
        ["Resync:SignedKep"] = new[] { "Doctor" }, ["Resync:Sent"] = new[] { "System" }, ["Resync:Accepted"] = new[] { "System" },
    };

    public static bool CanTransition(Dictionary<string, string[]> wf, string from, string to)
        => wf.TryGetValue(from, out var allowed) && allowed.Contains(to);
}

/// <summary>Застосування коригувань до ЕМЗ Медлінка (виправлення в 1 клік) та постановка в чергу ресинхронізації з ЕСОЗ</summary>
public class CorrectionService
{
    private readonly PmgDbContext _db;
    private readonly IPmgTariffCalculatorService _calc;
    private readonly ITariffCatalogProvider _catalog;
    private readonly ILogger<CorrectionService> _log;
    private static readonly JsonSerializerOptions JsonOpts = new() { Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping };

    public CorrectionService(PmgDbContext db, IPmgTariffCalculatorService calc, ITariffCatalogProvider catalog, ILogger<CorrectionService> log) { _db = db; _calc = calc; _catalog = catalog; _log = log; }

    public async Task<object> ApplyAsync(ApplyCorrectionRequest req, CancellationToken ct = default)
    {
        var d = await _db.Discrepancies.FirstOrDefaultAsync(x => x.Id == req.DiscrepancyId, ct) ?? throw new KeyNotFoundException("Розбіжність не знайдено");
        var encId = req.EncounterId ?? d.EncounterId;
        var enc = encId.HasValue ? await _db.Encounters.FirstOrDefaultAsync(e => e.Id == encId, ct) : null;
        var before = enc == null ? null : new { enc.PrimaryIcd10Code, enc.InterventionsJson, enc.PackageNumber, enc.EmployeeId, enc.DateStart, enc.DateEnd, enc.EpisodeId, enc.Status };

        Recommendation? rec = null;
        if (!string.IsNullOrEmpty(d.RecommendationJson)) rec = JsonSerializer.Deserialize<Recommendation>(d.RecommendationJson, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
        if (req.AcceptRecommendation && rec != null)
        {
            if (!string.IsNullOrEmpty(rec.SuggestedServiceCode)) (req.AddServices ??= new()).Add(rec.SuggestedServiceCode);
            if (!string.IsNullOrEmpty(rec.SuggestedIcdCode)) req.NewPrimaryIcd10Code ??= rec.SuggestedIcdCode;
            if (!string.IsNullOrEmpty(rec.SuggestedPackageNumber)) req.NewPackageNumber ??= rec.SuggestedPackageNumber;
        }

        var changes = new List<string>();
        if (enc != null)
        {
            var services = string.IsNullOrEmpty(enc.InterventionsJson) ? new List<string>() : JsonSerializer.Deserialize<List<string>>(enc.InterventionsJson) ?? new();
            foreach (var s in req.AddServices ?? new()) if (!services.Contains(s)) { services.Add(s); changes.Add($"+ АКПІ {s}"); }
            foreach (var s in req.RemoveServices ?? new()) if (services.Remove(s)) changes.Add($"− АКПІ {s}");
            enc.InterventionsJson = JsonSerializer.Serialize(services);
            if (!string.IsNullOrEmpty(req.NewPrimaryIcd10Code) && req.NewPrimaryIcd10Code != enc.PrimaryIcd10Code) { changes.Add($"Діагноз {enc.PrimaryIcd10Code} → {req.NewPrimaryIcd10Code}"); enc.PrimaryIcd10Code = PmgTariffCalculatorService.NormalizeIcd(req.NewPrimaryIcd10Code); }
            if (!string.IsNullOrEmpty(req.NewPackageNumber) && req.NewPackageNumber != enc.PackageNumber) { changes.Add($"Пакет {enc.PackageNumber} → {req.NewPackageNumber}"); enc.PackageNumber = req.NewPackageNumber; }
            if (req.NewEmployeeId.HasValue && req.NewEmployeeId != enc.EmployeeId) { changes.Add("Змінено лікаря-виконавця"); enc.EmployeeId = req.NewEmployeeId; }
            if (req.NewDateStart.HasValue) { changes.Add($"Початок → {req.NewDateStart:yyyy-MM-dd HH:mm}"); enc.DateStart = req.NewDateStart; }
            if (req.NewDateEnd.HasValue) { changes.Add($"Кінець → {req.NewDateEnd:yyyy-MM-dd HH:mm}"); enc.DateEnd = req.NewDateEnd; }
            if (req.NewEpisodeId.HasValue) { changes.Add("Прив'язано до епізоду"); enc.EpisodeId = req.NewEpisodeId; }
            enc.CodingCorrected = true; enc.CorrectedAt = DateTime.UtcNow; enc.CorrectionNote = req.Note ?? rec?.Title; enc.Status = "Corrected"; enc.ModifiedOn = DateTime.UtcNow; enc.ModifiedBy = req.CorrectedBy ?? Guid.Empty;
        }

        // перерахунок очікуваного тарифу після виправлення
        decimal expected = rec?.ExpectedRevenue ?? d.RecoverableAmount;
        if (enc != null)
        {
            var cat = await _catalog.GetAsync(ct);
            var services = JsonSerializer.Deserialize<List<string>>(enc.InterventionsJson ?? "[]") ?? new();
            var calc = _calc.Calculate(new TariffRequest { PackageNumber = enc.PackageNumber, PrimaryIcd10Code = enc.PrimaryIcd10Code, ServiceCodes = services, Priority = enc.Priority, PatientAge = enc.PatientAge, ServiceNumber = enc.ServiceNumber }, cat);
            if (calc.Resolved && calc.Tariff > 0) expected = calc.Tariff;
        }

        d.Status = "Corrected"; d.CorrectedAt = DateTime.UtcNow; d.CorrectedBy = req.CorrectedBy; d.ModifiedOn = DateTime.UtcNow;
        d.RecoverableAmount = expected;
        d.CorrectionJson = JsonSerializer.Serialize(new { before, changes, note = req.Note, expectedRevenue = expected, acceptedRecommendation = req.AcceptRecommendation }, JsonOpts);

        EheResyncQueue? q = null;
        if (req.EnqueueResync && enc != null)
        {
            q = new EheResyncQueue { EncounterId = enc.Id, DiscrepancyId = d.Id, Reason = rec?.Title ?? "Коригування кодування ЕМЗ за результатами аудиту НСЗУ", Status = "Queued", Caption = $"Resync {enc.EhealthId}", PayloadJson = JsonSerializer.Serialize(new { enc.EhealthId, enc.PrimaryIcd10Code, enc.InterventionsJson, enc.PackageNumber }, JsonOpts) };
            _db.ResyncQueue.Add(q);
        }
        await _db.SaveChangesAsync(ct);
        _log.LogInformation("Correction applied to discrepancy {Id}: {Changes}", d.Id, string.Join("; ", changes));
        return new { success = true, discrepancyId = d.Id, encounterId = enc?.Id, status = d.Status, changes, expectedRevenueUah = expected, resyncQueueId = q?.Id, message = enc == null ? "Розбіжність позначено виправленою (ЕМЗ поза МІС)" : "Взаємодію успішно скориговано в Медлінку та поставлено в чергу переподання в ЕСОЗ" };
    }
}
