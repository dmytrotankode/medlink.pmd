using System.Text.Json;
using MedLink.Pmg.Module.Data;
using MedLink.Pmg.Module.Models;
using Microsoft.EntityFrameworkCore;

namespace MedLink.Pmg.Module.Services;

/// <summary>
/// АРМ лікаря: пре-білінг та Anti-Defektura перевірка ЕМЗ до підписання КЕП.
/// Повертає тариф, дерево розрахунку, знахідки правил FR-*/PK-* та оцінку ризику дефектури.
/// </summary>
public class PrebillingService
{
    private readonly PmgDbContext _db;
    private readonly IPmgTariffCalculatorService _calc;
    private readonly ITariffCatalogProvider _catalog;
    private static readonly JsonSerializerOptions JsonOpts = new() { Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping };

    public PrebillingService(PmgDbContext db, IPmgTariffCalculatorService calc, ITariffCatalogProvider catalog) { _db = db; _calc = calc; _catalog = catalog; }

    public async Task<PrebillingResponse> EvaluateAsync(PrebillingRequest req, CancellationToken ct = default)
    {
        var cat = await _catalog.GetAsync(ct);
        var icd = PmgTariffCalculatorService.NormalizeIcd(req.PrimaryIcd10Code ?? req.IcdCode);
        var services = new List<string>();
        if (!string.IsNullOrWhiteSpace(req.ServiceCode)) services.Add(req.ServiceCode.Trim());
        foreach (var s in req.Services ?? new()) if (!string.IsNullOrWhiteSpace(s) && !services.Contains(s.Trim())) services.Add(s.Trim());
        foreach (var s in req.CompanionServices ?? new()) if (!string.IsNullOrWhiteSpace(s) && !services.Contains(s.Trim())) services.Add(s.Trim());

        // Якщо передано EncounterId — підтягнути дані ЕМЗ та лікаря
        MisEncounter? enc = null; OrgEmployee? emp = null;
        if (req.EncounterId.HasValue)
        {
            enc = await _db.Encounters.AsNoTracking().FirstOrDefaultAsync(e => e.Id == req.EncounterId, ct);
            if (enc != null)
            {
                if (string.IsNullOrEmpty(icd)) icd = PmgTariffCalculatorService.NormalizeIcd(enc.PrimaryIcd10Code);
                if (services.Count == 0 && !string.IsNullOrEmpty(enc.InterventionsJson)) services = JsonSerializer.Deserialize<List<string>>(enc.InterventionsJson) ?? new();
                req.PackageNumber ??= enc.PackageNumber; req.PatientAge ??= enc.PatientAge; req.Priority ??= enc.Priority; req.EmployeeId ??= enc.EmployeeId; req.PatientGender ??= enc.PatientGender;
            }
        }
        if (req.EmployeeId.HasValue) emp = await _db.Employees.AsNoTracking().FirstOrDefaultAsync(e => e.Id == req.EmployeeId, ct);
        var position = (req.DoctorPosition ?? emp?.PositionCode ?? "").Trim().ToUpperInvariant();

        var findings = new List<Finding>();
        var rules = await _db.RuleConfigs.AsNoTracking().Where(r => r.IsActive).ToDictionaryAsync(r => r.RuleCode, r => r, ct);
        Finding F(string code, int sev, string msg, string? errorCode = null, string? suggestion = null)
        {
            rules.TryGetValue(code, out var rc);
            var f = new Finding { RuleCode = code, Severity = sev, Message = msg, NormativeReference = rc?.NormativeReference, ErrorCode = errorCode, Suggestion = suggestion };
            findings.Add(f); return f;
        }

        // Визначення пакету: явно, або за ДСГ (3/4/47), або Пакет 9 за послугами
        var pkg = PmgTariffCalculatorService.NormalizePackage(req.PackageNumber);
        var candidates = _calc.ResolveDsgCandidates(cat, string.IsNullOrEmpty(pkg) || pkg is "3" or "4" or "47" ? (string.IsNullOrEmpty(pkg) ? null : pkg) : null, icd, services);
        if (string.IsNullOrEmpty(pkg))
        {
            if (candidates.Count > 0) pkg = candidates[0].PackageNumber;
            else if (_calc.ResolveOutpatientClass(cat, services, icd, null) != null) pkg = "9";
        }

        // Мультихірургія: ≥2 хірургічних послуг з переліку ДСГ, або явний прапорець
        bool multi = req.HasMultiSurgery ?? false;
        if (!multi && services.Count >= 2 && pkg is "3" or "47")
        {
            var surgical = services.Count(s => cat.DsgIdsByService.ContainsKey(s));
            multi = surgical >= 2;
        }

        var calc = _calc.Calculate(new TariffRequest
        {
            PackageNumber = pkg, PrimaryIcd10Code = icd, ServiceCodes = services, Priority = req.Priority ?? req.AdmissionType, PatientAge = req.PatientAge,
            IsMountain = req.IsMountain, HasMultiSurgery = multi, LengthOfStayDays = req.LengthOfStayDays, RehabGroup = req.RehabGroup,
        }, cat);

        // ---- Правила валідації ----
        if (string.IsNullOrEmpty(icd)) F("FR-02", 2, "Не вказано основний діагноз МКХ-10 — ЕМЗ не буде віднесено до жодного пакету (0 ₴).", "ERR_PRIMARY_DIAG_07", "Оберіть основний діагноз.");
        else if (!cat.Icd10Names.ContainsKey(icd) && !cat.DsgIdsByDiag.ContainsKey(icd)) F("FR-03", 1, $"Код МКХ-10 {icd} відсутній у переліках ДСГ/класів ПМГ-2026 — перевірте кодування.", null, null);

        if (pkg is "3" or "47" && !services.Any(s => cat.DsgIdsByService.ContainsKey(s)))
            F("FR-04", 2, $"Для хірургічного пакету {pkg} відсутній код операції АКПІ — НСЗУ відхилить випадок (0 ₴).", "ERR_SURG_NO_OP_05", candidates.FirstOrDefault(c => c.SvcCount > 0) is { } c0 ? $"Додайте інтервенцію з переліку ДСГ {c0.DsgCode}." : "Додайте код операції.");
        if (pkg is "3" or "4" or "47" && !calc.Resolved)
            F("FR-02", 2, $"Діагноз {icd} не входить до переліку діагнозів ДСГ пакету {pkg} або не збігається з інтервенцією — ризик «Не відповідає жодному пакету/послузі».", "ERR_NO_PKG_02", "Перевірте пакет/діагноз або додайте обов'язкову інтервенцію.");
        if (pkg == "9" && !calc.Resolved)
            F("FR-02", 1, "Амбулаторний клас не визначено за кодами послуг — застосовано коефіцієнт 1.00 (155 ₴).", null, "Додайте код консультації/процедури АКПІ.");

        // FR-05 — посада лікаря (MedProfit + позиції класів Пакету 9)
        var posCheck = CheckDoctorPosition(cat, position, services, calc.ClassNumber);
        if (posCheck.applicable)
        {
            if (!posCheck.valid) F("FR-05", 2, $"Посада лікаря {position} не входить до дозволених для послуги {posCheck.service} ({posCheck.allowed}). Ризик дефектури ERR_DOC_SPEC_04: 0 ₴!", "ERR_DOC_SPEC_04", $"Призначте виконавця з посадою {posCheck.allowed}.");
            else F("FR-05", 0, $"Посада лікаря {position} відповідає вимогам послуги {posCheck.service}.", null, null);
        }
        else if (string.IsNullOrEmpty(position)) F("FR-05", 1, "Посаду виконавця не вказано — перевірка Anti-Defektura неможлива.", null, "Вкажіть лікаря-виконавця.");

        // FR-06 — вік/стать за клінічними нормами довідника послуг
        foreach (var s in services)
        {
            var norm = await _db.ServiceCatalog.AsNoTracking().FirstOrDefaultAsync(x => x.ServiceCode == s, ct);
            if (norm == null) continue;
            if (req.PatientAge.HasValue && (req.PatientAge < norm.AgeMin || req.PatientAge > norm.AgeMax))
                F("FR-06", 1, $"Вік пацієнта {req.PatientAge} поза нормою послуги {s} ({norm.AgeMin}–{norm.AgeMax}).", "ERR_AGE_03");
            if (!string.IsNullOrEmpty(req.PatientGender) && norm.GenderRestriction != "ALL" && !req.PatientGender.StartsWith(norm.GenderRestriction, StringComparison.OrdinalIgnoreCase))
                F("FR-06", 1, $"Стать пацієнта не відповідає обмеженню послуги {s} ({norm.GenderRestriction}).", "ERR_AGE_03");
            if (req.LengthOfStayDays.HasValue && pkg is "3" or "4" && req.LengthOfStayDays < norm.MinStayDays)
                F("PK-01A", 1, $"Тривалість перебування {req.LengthOfStayDays} дн. менша за норму {norm.MinStayDays} дн. для {s} — ризик «Необґрунтована тривалість лікування».", "ERR_STAY_TOO_SHORT_06", "Розгляньте Пакет 47 (хірургія одного дня).");
        }
        if (calc.PlannedCoef != 1m) F("PK-02", 0, $"Планова госпіталізація — застосовано коефіцієнт {calc.PlannedCoef}.");
        if (calc.MountainCoef != 1m) F("PK-04", 0, $"Гірський коефіцієнт {calc.MountainCoef} застосовано.");
        if (calc.MultiSurgeryCoef != 1m) F("PK-05", 0, $"Мультихірургія: застосовано коефіцієнт {calc.MultiSurgeryCoef} (+30 %).");
        if (calc.AgeCoef != 1m) F("PK-06", 0, $"Неонатальний коефіцієнт {calc.AgeCoef} застосовано.");
        if (pkg is "53" or "54") F("RD-01", calc.Resolved ? 0 : 2, calc.Resolved ? $"Група реабілітації {calc.DsgCode} визначена за діагнозом." : "Групу реабілітації не визначено — обов'язкове кодування діагнозу першопричини та МКФ.", calc.Resolved ? null : "ERR_REHAB_IND_08");
        if (calc.Resolved && calc.Tariff > 0) F("PK-12", 0, $"Розрахунок: {calc.Formula}");

        var maxSev = findings.Count == 0 ? 0 : findings.Max(f => f.Severity);
        var resp = new PrebillingResponse
        {
            IsValid = maxSev < 2, Status = maxSev == 2 ? "REJECTED_DEFEKTURA" : maxSev == 1 ? "WARNING" : "APPROVED",
            PackageNumber = pkg, DsgCode = calc.DsgCode, DsgName = calc.DsgName, ClassNumber = calc.ClassNumber, WeightCoef = calc.WeightCoef, BaseRate = calc.BaseRate,
            Tariff = maxSev == 2 ? 0m : calc.Tariff, FullTariff = calc.FullTariff, Formula = calc.Formula, MultisurgeryApplied = calc.MultiSurgeryCoef != 1m,
            CalculationSteps = calc.Steps, Findings = findings,
            AntiDefekturaCheck = new
            {
                isValid = maxSev < 2, status = maxSev == 2 ? "REJECTED_DEFEKTURA" : "APPROVED",
                doctorPositionStatus = !posCheck.applicable ? "NOT_CHECKED" : posCheck.valid ? "VALID" : "INVALID_SPECIALIZATION",
                doctorPosition = position, allowedPositions = posCheck.allowed,
                expectedTariffIfRejected = 0m, potentialTariff = calc.Tariff,
                errorWarning = findings.FirstOrDefault(f => f.Severity == 2)?.Message,
            },
            DsgCandidates = candidates.Take(5).Select(c => (object)new { c.DsgCode, c.Name, c.PackageNumber, c.WeightCoef, c.ShareTariff, c.SvcCount }).ToList(),
        };

        if (req.Persist || req.EncounterId.HasValue)
        {
            var ar = new DsgAnalysisResult
            {
                EncounterId = req.EncounterId, OrganizationId = req.OrganizationId ?? enc?.LegalEntityId ?? Guid.Empty, PackageNumber = pkg, DsgGroupCode = calc.DsgCode,
                Status = maxSev, Tariff = calc.FullTariff, EstimatedPayment = resp.Tariff, WeightCoef = calc.WeightCoef,
                CalculationJson = JsonSerializer.Serialize(new { calc.Model, calc.Formula, calc.Steps, calc.Notes }, JsonOpts), FindingsJson = JsonSerializer.Serialize(findings, JsonOpts),
                PrimaryIcd10Code = icd, EmployeeId = req.EmployeeId, DepartmentId = enc?.DepartmentId, Trigger = 1, Caption = $"Пре-білінг {icd} {calc.DsgCode} {resp.Status}",
                DictionaryVersionsJson = JsonSerializer.Serialize(new { catalogLoadedAt = cat.LoadedAt, tariffSetting = cat.Settings.Caption }),
            };
            _db.AnalysisResults.Add(ar);
            await _db.SaveChangesAsync(ct);
            resp.AnalysisResultId = ar.Id;
        }
        return resp;
    }

    public static (bool applicable, bool valid, string? service, string? allowed) CheckDoctorPosition(TariffCatalog cat, string position, List<string> services, string? classNumber)
    {
        if (string.IsNullOrEmpty(position)) return (false, true, null, null);
        foreach (var s in services)
        {
            if (cat.DoctorPositionsByService.TryGetValue(s, out var rule) && !string.IsNullOrWhiteSpace(rule.PositionRequirements))
            {
                var allowed = rule.PositionRequirements.Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries).Select(x => x.ToUpperInvariant()).ToList();
                return (true, allowed.Contains(position), s, string.Join(", ", allowed));
            }
        }
        if (!string.IsNullOrEmpty(classNumber) && cat.ClassByNumber.TryGetValue(classNumber, out var cls) && cat.PositionsByClassId.TryGetValue(cls.Id, out var set) && set.Count > 0)
            return (true, set.Contains(position), $"клас {classNumber}", string.Join(", ", set.OrderBy(x => x)));
        return (false, true, null, null);
    }
}
