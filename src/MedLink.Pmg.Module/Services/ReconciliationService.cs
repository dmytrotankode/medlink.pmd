using System.Text.Json;
using MedLink.Pmg.Module.Data;
using MedLink.Pmg.Module.Models;
using Microsoft.EntityFrameworkCore;

namespace MedLink.Pmg.Module.Services;

public class ReconciliationResult
{
    public Guid StatementId { get; set; }
    public string Status { get; set; } = "COMPLETED";
    public DateTime ReconciledAt { get; set; } = DateTime.UtcNow;
    public int TotalChecked { get; set; }
    public int MatchedPaidCount { get; set; }
    public int DiscrepancyRejectedCount { get; set; }
    public int MissingInMisCount { get; set; }
    public int MissingInNhsuCount { get; set; }
    public decimal MissingInNhsuAmountUah { get; set; }
    public decimal LostRevenueUah { get; set; }
    public decimal PotentialRecoveryUah { get; set; }
    public int DiscrepanciesCreated { get; set; }
    public string Message { get; set; } = string.Empty;
}

/// <summary>
/// Двостороння (2-Way) звірка звіту НСЗУ з ЕМЗ МІС «Медлінк» за Encounter.EhealthId:
///   звіт → МІС: кожен рядок шукається у mis_encounter.ehealth_id (MatchedPaid / DiscrepancyRejected / MissingInMis);
///   МІС → звіт: підписані ЕМЗ закладу за період, відсутні у звіті → прихована дефектура (MissingInNhsu).
/// Для кожної розбіжності формується рекомендація асистента (RecommendationEngine).
/// </summary>
public class ReconciliationService
{
    private readonly PmgDbContext _db;
    private readonly RecommendationEngine _recommender;
    private readonly ILogger<ReconciliationService> _log;
    private static readonly JsonSerializerOptions JsonOpts = new() { Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping };

    public ReconciliationService(PmgDbContext db, RecommendationEngine recommender, ILogger<ReconciliationService> log) { _db = db; _recommender = recommender; _log = log; }

    public async Task<ReconciliationResult> ReconcileAsync(Guid statementId, CancellationToken ct = default)
    {
        var st = await _db.Statements.FirstOrDefaultAsync(s => s.Id == statementId, ct) ?? throw new KeyNotFoundException($"Statement {statementId} not found");
        var res = new ReconciliationResult { StatementId = statementId };

        // попередні розбіжності цього звіту (крім уже виправлених) — перебудовуємо
        var old = await _db.Discrepancies.Where(d => d.StatementId == statementId && d.Status == "New").ToListAsync(ct);
        _db.Discrepancies.RemoveRange(old);
        await _db.SaveChangesAsync(ct);
        var keep = await _db.Discrepancies.Where(d => d.StatementId == statementId).Select(d => d.StatementLineId).ToListAsync(ct);
        var keepSet = new HashSet<Guid?>(keep);

        var lines = await _db.StatementLines.Where(l => l.StatementId == statementId).ToListAsync(ct);
        var ehIds = lines.Where(l => l.EncounterEhealthId != null).Select(l => l.EncounterEhealthId!.Value).Distinct().ToList();
        var encounters = new Dictionary<Guid, MisEncounter>();
        foreach (var chunk in ehIds.Chunk(800))
        {
            var found = await _db.Encounters.AsNoTracking().Where(e => e.EhealthId != null && chunk.Contains(e.EhealthId.Value) && e.RecordState == 2).ToListAsync(ct);
            foreach (var e in found) encounters[e.EhealthId!.Value] = e;
        }

        var newDiscrepancies = new List<NszuEncounterDiscrepancy>();
        foreach (var l in lines)
        {
            res.TotalChecked++;
            MisEncounter? enc = null;
            if (l.EncounterEhealthId != null) encounters.TryGetValue(l.EncounterEhealthId.Value, out enc);
            if (enc != null)
            {
                l.MatchedEncounterId = enc.Id; l.MatchedEmployeeId = enc.EmployeeId; l.MatchedDepartmentId = enc.DepartmentId; l.MatchedPatientId = enc.PatientId;
            }
            else { l.MatchedEncounterId = null; }

            if (l.IncludedInReport == NszuInclusion.Rejected)
            {
                l.MatchStatus = enc != null ? (int)MatchStatus.DiscrepancyRejected : (int)MatchStatus.MissingInMis;
                if (enc != null) res.DiscrepancyRejectedCount++; else res.MissingInMisCount++;
                res.LostRevenueUah += l.LostRevenue; res.PotentialRecoveryUah += l.RecoverableAmount;
                if (!keepSet.Contains(l.Id))
                {
                    var rec = _recommender.Build(l, enc);
                    newDiscrepancies.Add(new NszuEncounterDiscrepancy
                    {
                        StatementId = statementId, StatementLineId = l.Id, EncounterId = enc?.Id, EncounterEhealthId = l.EncounterEhealthId,
                        EmployeeId = enc?.EmployeeId, DepartmentId = enc?.DepartmentId, PatientId = enc?.PatientId,
                        DiscrepancyType = enc != null ? "Rejected" : "MissingInMis", ErrorCode = l.ErrorCode, ErrorCategory = l.ErrorCategory,
                        NszuComment = l.ErrorComment, NszuDetails = JoinDetails(l), PackageNumber = l.PackageNumber, DsgCode = l.DsgCode, PrimaryIcd10Code = l.PrimaryIcd10Code,
                        LostAmount = l.LostRevenue, RecoverableAmount = l.RecoverableAmount, RecommendationJson = JsonSerializer.Serialize(rec, JsonOpts),
                        Caption = $"{l.ErrorComment} — {l.PractitionerName}",
                    });
                }
            }
            else
            {
                l.MatchStatus = enc != null ? (int)MatchStatus.MatchedPaid : (int)MatchStatus.MissingInMis;
                if (enc != null) res.MatchedPaidCount++; else res.MissingInMisCount++;
            }
        }

        // МІС → звіт: прихована дефектура
        var reported = new HashSet<Guid>(ehIds);
        var misOnly = await _db.Encounters.AsNoTracking()
            .Where(e => e.LegalEntityId == st.OrganizationId && e.RecordState == 2 && e.IsSigned && e.EhealthId != null && e.DateStart >= st.PeriodFrom && e.DateStart <= st.PeriodTo)
            .ToListAsync(ct);
        var hiddenExisting = new HashSet<Guid?>(await _db.Discrepancies.Where(d => d.StatementId == statementId && d.DiscrepancyType == "HiddenDefektura").Select(d => d.EncounterId).ToListAsync(ct));
        var calc = await _db.TariffSettings.AsNoTracking().OrderByDescending(t => t.ValidFrom).FirstOrDefaultAsync(ct) ?? new DsgTariffSetting();
        foreach (var e in misOnly)
        {
            if (reported.Contains(e.EhealthId!.Value)) continue;
            res.MissingInNhsuCount++;
            var amount = await EstimateEncounterTariffAsync(e, ct);
            res.MissingInNhsuAmountUah += amount;
            if (hiddenExisting.Contains(e.Id)) continue;
            var rec = _recommender.BuildHidden(e, amount);
            newDiscrepancies.Add(new NszuEncounterDiscrepancy
            {
                StatementId = statementId, EncounterId = e.Id, EncounterEhealthId = e.EhealthId, EmployeeId = e.EmployeeId, DepartmentId = e.DepartmentId, PatientId = e.PatientId,
                DiscrepancyType = "HiddenDefektura", ErrorCode = "HIDDEN_DEFEKTURA", ErrorCategory = "Прихована дефектура (відсутній у звіті НСЗУ)",
                NszuComment = "ЕМЗ підписано та відправлено в ЕСОЗ, але не потрапив до звіту НСЗУ за період",
                PackageNumber = e.PackageNumber, PrimaryIcd10Code = e.PrimaryIcd10Code, LostAmount = amount, RecoverableAmount = Math.Round(amount * 0.9m, 2),
                RecommendationJson = JsonSerializer.Serialize(rec, JsonOpts), Caption = $"Прихована дефектура — {e.Caption}",
            });
        }

        _db.Discrepancies.AddRange(newDiscrepancies);
        res.DiscrepanciesCreated = newDiscrepancies.Count;
        st.ReconciledAt = DateTime.UtcNow; st.Status = "Reconciled";
        st.MatchedPaidCount = res.MatchedPaidCount; st.DiscrepancyCount = res.DiscrepancyRejectedCount; st.MissingInMisCount = res.MissingInMisCount;
        st.MissingInNhsuCount = res.MissingInNhsuCount; st.MissingInNhsuAmount = res.MissingInNhsuAmountUah;
        await _db.SaveChangesAsync(ct);
        _db.ChangeTracker.Clear();

        res.LostRevenueUah = Math.Round(res.LostRevenueUah, 2); res.PotentialRecoveryUah = Math.Round(res.PotentialRecoveryUah, 2); res.MissingInNhsuAmountUah = Math.Round(res.MissingInNhsuAmountUah, 2);
        res.Message = $"2-Way звірку виконано: {res.MatchedPaidCount} ЕМЗ підтверджено, {res.DiscrepancyRejectedCount} відхилених знайдено в МІС, {res.MissingInMisCount} відсутні в МІС, " +
                      $"{res.MissingInNhsuCount} випадків прихованої дефектури на {PmgTariffCalculatorService.Money(res.MissingInNhsuAmountUah)}.";
        _log.LogInformation("{Msg}", res.Message);
        return res;
    }

    /// <summary>Оцінка тарифу ЕМЗ МІС (для прихованої дефектури) через тарифний движок</summary>
    private async Task<decimal> EstimateEncounterTariffAsync(MisEncounter e, CancellationToken ct)
    {
        var calcSvc = _recommender.Calculator;
        var cat = await _recommender.Catalog.GetAsync(ct);
        var services = string.IsNullOrEmpty(e.InterventionsJson) ? new List<string>() : JsonSerializer.Deserialize<List<string>>(e.InterventionsJson) ?? new();
        var c = calcSvc.Calculate(new TariffRequest { PackageNumber = e.PackageNumber, PrimaryIcd10Code = e.PrimaryIcd10Code, ServiceCodes = services, ServiceNumber = e.ServiceNumber, Priority = e.Priority, PatientAge = e.PatientAge }, cat);
        return c.Tariff;
    }

    private static string? JoinDetails(NszuStatementLine l)
    {
        var parts = new List<string>();
        void Add(string label, string? v) { if (!string.IsNullOrWhiteSpace(v) && v != "-") parts.Add($"{label}: {v}"); }
        Add("Деталі помилок (40)", l.CompletenessDetailsJson); Add("Невідповідності (41)", l.VerificationDetails); Add("Конфлікти групування (42)", l.GroupingConflictDetails);
        Add("Перегляд НСЗУ (43)", l.NszuReviewDetails); Add("Зауваження (44)", l.AdditionalRemarks);
        return parts.Count == 0 ? null : string.Join("\n", parts);
    }
}

/// <summary>Генерація рекомендацій асистента виправлення для відхилених ЕМЗ (на основі словника помилок, ДСГ та матриці послуг)</summary>
public class RecommendationEngine
{
    public IPmgTariffCalculatorService Calculator { get; }
    public ITariffCatalogProvider Catalog { get; }
    private readonly NszuErrorClassifier _classifier;

    public RecommendationEngine(IPmgTariffCalculatorService calculator, ITariffCatalogProvider catalog, NszuErrorClassifier classifier)
    { Calculator = calculator; Catalog = catalog; _classifier = classifier; }

    public Recommendation Build(NszuStatementLine l, MisEncounter? enc)
    {
        var cat = Catalog.GetAsync().GetAwaiter().GetResult();
        var cls = _classifier.Classify(l.ErrorComment);
        var services = string.IsNullOrEmpty(l.InterventionCodesJson) ? new List<string>() : JsonSerializer.Deserialize<List<string>>(l.InterventionCodesJson) ?? new();
        var icd = l.PrimaryIcd10Code;
        var rec = new Recommendation { Action = string.IsNullOrEmpty(cls.Action) ? "ManualReview" : cls.Action, Confidence = 0.6m, ExpectedRevenue = l.LostRevenue };
        cat.ErrorsByCode.TryGetValue(l.ErrorCode ?? "", out var dict);
        rec.NormativeReference = dict?.NormativeReference;

        switch (rec.Action)
        {
            case "AddProcedure":
            {
                // Підібрати ДСГ стаціонару за діагнозом та запропонувати обов'язкову інтервенцію
                var pkgForDsg = l.PackageNumber is "3" or "4" or "47" ? l.PackageNumber : null;
                var candidates = Calculator.ResolveDsgCandidates(cat, pkgForDsg, icd, Array.Empty<string>())
                    .Where(d => d.SvcCount > 0).OrderByDescending(d => d.WeightCoef).Take(3).ToList();
                var best = candidates.FirstOrDefault();
                if (best != null)
                {
                    var svcCode = FirstServiceOfDsg(cat, best);
                    var tariff = Calculator.CalculateHospitalTariff(best.PackageNumber, best.WeightCoef, l.Priority, false, false, l.PatientAge, cat.Settings);
                    rec.Title = $"Додати код АКПІ {svcCode} для віднесення до ДСГ {best.DsgCode}";
                    rec.Explanation = $"Діагноз {icd} входить до переліку ДСГ {best.DsgCode} «{best.Name}» (пакет {best.PackageNumber}), але у ЕМЗ відсутня обов'язкова інтервенція. " +
                                      $"Після додавання коду послуги очікуваний тариф {PmgTariffCalculatorService.Money(tariff.Tariff)}.";
                    rec.SuggestedServiceCode = svcCode; rec.SuggestedServiceName = svcCode != null && cat.AchiNames.TryGetValue(svcCode, out var n) ? n : null;
                    rec.SuggestedPackageNumber = best.PackageNumber; rec.TargetDsg = best.DsgCode; rec.ExpectedRevenue = tariff.Tariff; rec.Confidence = 0.8m;
                    rec.Steps = new() { "Відкрити ЕМЗ у Медлінку", $"Додати інтервенцію АКПІ {svcCode}", "Перевірити посаду виконавця (Anti-Defektura)", "Підписати КЕП та переподати в ЕСОЗ" };
                }
                else if (l.PackageNumber == "9" || string.IsNullOrEmpty(l.PackageNumber))
                {
                    var cls9 = Calculator.ResolveOutpatientClass(cat, services, icd, null);
                    rec.Action = cls9 != null ? "ReclassifyPackage" : "FixDiagnosis";
                    rec.Title = cls9 != null ? $"Переподати як амбулаторну послугу класу {cls9.ClassNumber}" : "Уточнити діагноз та код послуги для віднесення до пакету";
                    rec.Explanation = cls9 != null
                        ? $"Інтервенції ЕМЗ відповідають класу {cls9.ClassName} Пакету 9 (тариф {PmgTariffCalculatorService.Money(Math.Round(cat.Settings.OutpatientBaseRate * cls9.Coefficient, 2))}). Перевірте посаду лікаря та наявність направлення."
                        : "НСЗУ не змогла віднести ЕМЗ до жодного пакету: перевірте код послуги АКПІ, посаду виконавця, тип взаємодії та наявність електронного направлення.";
                    rec.SuggestedPackageNumber = cls9 != null ? "9" : null; rec.TargetDsg = cls9?.ClassNumber; rec.Confidence = cls9 != null ? 0.7m : 0.4m;
                    if (cls9 != null) rec.ExpectedRevenue = Math.Round(cat.Settings.OutpatientBaseRate * cls9.Coefficient, 2);
                }
                else goto default;
                break;
            }
            case "LinkEpisode":
                rec.Title = "Прив'язати взаємодію до клінічного епізоду лікування";
                rec.Explanation = "Запис сформовано для МВТН без відкритого епізоду або з некоректним типом звернення. Створіть/оберіть епізод лікування з відповідним діагнозом, вкажіть тип взаємодії та переподайте ЕМЗ.";
                rec.Steps = new() { "Відкрити ЕМЗ у Медлінку", "Обрати або створити епізод лікування", "Встановити коректний тип взаємодії", "Переподати в ЕСОЗ" };
                rec.Confidence = 0.75m; break;
            case "AdjustDates":
                rec.Title = "Скоригувати часові межі послуги (перекриття з іншим ЕМЗ)";
                rec.Explanation = "Послуга перетинається з іншою послугою цього пацієнта (деталі у колонці 40). Перевірте дати/час початку та завершення або об'єднайте з госпіталізацією.";
                rec.Steps = new() { "Переглянути парні ЕМЗ з колонки 40", "Виправити дати/час", "Переподати в ЕСОЗ" };
                rec.Confidence = 0.55m; break;
            case "ReclassifyPackage":
                rec.Title = l.PackageNumber is "3" or "4" ? "Рекласифікувати у хірургію одного дня (Пакет 47)" : "Переподати ЕМЗ під відповідний пакет";
                rec.Explanation = "Тривалість лікування не відповідає умовам закупівлі пакету. За наявності хірургічного втручання випадок може бути оплачений за Пакетом 47 (частка 0.60) замість повної втрати.";
                rec.SuggestedPackageNumber = l.PackageNumber is "3" or "4" ? "47" : l.PackageNumber;
                rec.Confidence = 0.5m; break;
            case "FixDiagnosis":
                rec.Title = "Уточнити основний діагноз / тип епізоду";
                rec.Explanation = "Тип епізоду або основний діагноз не є оплачуваним для цього пакету. Перегляньте кодування МКХ-10 та тип епізоду у Медлінку.";
                rec.Confidence = 0.5m; break;
            case "AddIcfCoding":
                rec.Title = "Додати кодування функціональних обмежень (МКФ) та діагноз першопричини";
                rec.Explanation = "Для реабілітаційних пакетів 53/54 обов'язкові: діагноз першопричини, функціональні обмеження (МКФ), індивідуальний план та мінімальна тривалість циклу.";
                rec.Confidence = 0.7m; break;
            case "ChangeDoctor":
                rec.Title = "Призначити виконавця з посадою, дозволеною для послуги";
                rec.Explanation = "Посада лікаря-виконавця не відповідає вимогам послуги (MedProfit Anti-Defektura). Оберіть лікаря з дозволеною посадою та переподайте ЕМЗ.";
                rec.Confidence = 0.8m; break;
            case "RemoveDuplicate":
                rec.Title = "Технічний запис — виправлення не потребує";
                rec.Explanation = "Дублікат або запис «entered in error» не оплачується; переконайтеся, що основний ЕМЗ зарахований.";
                rec.ExpectedRevenue = 0; rec.Confidence = 0.95m; break;
            default:
                rec.Action = "ManualReview";
                rec.Title = string.IsNullOrEmpty(cls.Title) ? "Потребує ручного аналізу економістом" : cls.Title;
                rec.Explanation = dict?.RemediationAdvice ?? "Перегляньте коментар НСЗУ та деталі помилок (колонки 39–44) і прийміть рішення щодо переподання.";
                rec.Confidence = 0.35m; break;
        }
        if (enc == null) rec.Steps.Insert(0, "ЕМЗ не знайдено в МІС «Медлінк» (внесено в іншій системі) — виправлення виконується у системі-джерелі");
        return rec;
    }

    public Recommendation BuildHidden(MisEncounter e, decimal amount) => new()
    {
        Action = "Resubmit", Title = "Перевірити статус ЕМЗ в ЕСОЗ та переподати",
        Explanation = $"ЕМЗ {e.EhealthId} підписано у Медлінку ({e.SignedAt:yyyy-MM-dd}), але НСЗУ не включила його до звіту за період. Перевірте статус відправки в ЕСОЗ, цілісність епізоду та повторно відправте запис.",
        ExpectedRevenue = amount, Confidence = 0.65m, Steps = new() { "Перевірити журнал відправок в ЕСОЗ", "Переконатися, що епізод закрито", "Переподати ЕМЗ до 10-го числа наступного місяця" },
    };

    private static string? FirstServiceOfDsg(TariffCatalog cat, PmgDsg dsg)
    {
        foreach (var kv in cat.DsgIdsByService)
            if (kv.Value.Contains(dsg.Id)) return kv.Key;
        return null;
    }
}
