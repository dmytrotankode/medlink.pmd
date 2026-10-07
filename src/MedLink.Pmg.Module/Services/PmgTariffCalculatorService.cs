using System.Globalization;
using System.Text.RegularExpressions;
using MedLink.Pmg.Module.Data;
using MedLink.Pmg.Module.Models;
using Microsoft.EntityFrameworkCore;

namespace MedLink.Pmg.Module.Services;

/// <summary>Кешований зріз довідників для швидкої тарифікації десятків тисяч рядків без запитів до БД</summary>
public class TariffCatalog
{
    public DsgTariffSetting Settings { get; init; } = new();
    public Dictionary<string, DsgPackageTariffRule> PackageRules { get; init; } = new();
    public Dictionary<int, PmgDsg> DsgById { get; init; } = new();
    /// <summary>(package, dsg_code) → DSG</summary>
    public Dictionary<string, PmgDsg> DsgByPkgCode { get; init; } = new(StringComparer.OrdinalIgnoreCase);
    /// <summary>dsg_code → усі ДСГ з таким кодом (у різних пакетах)</summary>
    public Dictionary<string, List<PmgDsg>> DsgByCode { get; init; } = new(StringComparer.OrdinalIgnoreCase);
    /// <summary>diag_code → множина dsg_id</summary>
    public Dictionary<string, HashSet<int>> DsgIdsByDiag { get; init; } = new(StringComparer.OrdinalIgnoreCase);
    /// <summary>service_code → множина dsg_id</summary>
    public Dictionary<string, HashSet<int>> DsgIdsByService { get; init; } = new(StringComparer.OrdinalIgnoreCase);
    public Dictionary<int, PmgPackage9Class> ClassById { get; init; } = new();
    public Dictionary<string, PmgPackage9Class> ClassByNumber { get; init; } = new(StringComparer.OrdinalIgnoreCase);
    public Dictionary<string, HashSet<int>> ClassIdsByService { get; init; } = new(StringComparer.OrdinalIgnoreCase);
    public Dictionary<string, HashSet<int>> ClassIdsByDiag { get; init; } = new(StringComparer.OrdinalIgnoreCase);
    public Dictionary<int, HashSet<string>> PositionsByClassId { get; init; } = new();
    public Dictionary<string, PmgRehabGroup> RehabGroups { get; init; } = new(StringComparer.OrdinalIgnoreCase);
    public Dictionary<string, List<PmgRehabDiagnosis>> RehabByDiag { get; init; } = new(StringComparer.OrdinalIgnoreCase);
    public Dictionary<string, PmgPackage> Packages { get; init; } = new();
    public Dictionary<string, PmgNhsuErrorDictionary> ErrorsByCode { get; init; } = new(StringComparer.OrdinalIgnoreCase);
    public Dictionary<string, string> Icd10Names { get; init; } = new(StringComparer.OrdinalIgnoreCase);
    public Dictionary<string, string> AchiNames { get; init; } = new(StringComparer.OrdinalIgnoreCase);
    public Dictionary<string, PmgServiceDoctorPosition> DoctorPositionsByService { get; init; } = new(StringComparer.OrdinalIgnoreCase);
    public DateTime LoadedAt { get; init; } = DateTime.UtcNow;
}

public interface ITariffCatalogProvider
{
    Task<TariffCatalog> GetAsync(CancellationToken ct = default);
    void Invalidate();
}

/// <summary>Singleton-кеш довідників (перезавантажується після зміни налаштувань тарифів)</summary>
public class TariffCatalogProvider : ITariffCatalogProvider
{
    private readonly IServiceScopeFactory _scopes;
    private readonly ILogger<TariffCatalogProvider> _log;
    private TariffCatalog? _catalog;
    private readonly SemaphoreSlim _lock = new(1, 1);

    public TariffCatalogProvider(IServiceScopeFactory scopes, ILogger<TariffCatalogProvider> log) { _scopes = scopes; _log = log; }

    public void Invalidate() => _catalog = null;

    public async Task<TariffCatalog> GetAsync(CancellationToken ct = default)
    {
        if (_catalog != null) return _catalog;
        await _lock.WaitAsync(ct);
        try
        {
            if (_catalog != null) return _catalog;
            using var scope = _scopes.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<PmgDbContext>();
            var sw = System.Diagnostics.Stopwatch.StartNew();
            var cat = new TariffCatalog
            {
                Settings = await db.TariffSettings.AsNoTracking().Where(s => s.IsActive).OrderByDescending(s => s.ValidFrom).FirstOrDefaultAsync(ct) ?? new DsgTariffSetting(),
                PackageRules = await db.PackageTariffRules.AsNoTracking().Where(r => r.IsActive).ToDictionaryAsync(r => r.PackageNumber, r => r, ct),
                Packages = await db.Packages.AsNoTracking().ToDictionaryAsync(p => p.PackageId, p => p, ct),
                ErrorsByCode = await db.ErrorDictionary.AsNoTracking().ToDictionaryAsync(e => e.ErrorCode, e => e, StringComparer.OrdinalIgnoreCase, ct),
                RehabGroups = await db.RehabGroups.AsNoTracking().ToDictionaryAsync(g => g.Code, g => g, StringComparer.OrdinalIgnoreCase, ct),
            };
            foreach (var d in await db.Dsg.AsNoTracking().ToListAsync(ct))
            {
                cat.DsgById[d.Id] = d;
                cat.DsgByPkgCode[$"{d.PackageNumber}|{d.DsgCode}"] = d;
                if (!cat.DsgByCode.TryGetValue(d.DsgCode, out var l)) cat.DsgByCode[d.DsgCode] = l = new();
                l.Add(d);
            }
            foreach (var x in await db.DsgDiagnoses.AsNoTracking().Select(x => new { x.DiagCode, x.DsgId }).ToListAsync(ct))
            {
                if (!cat.DsgIdsByDiag.TryGetValue(x.DiagCode, out var s)) cat.DsgIdsByDiag[x.DiagCode] = s = new();
                s.Add(x.DsgId);
            }
            foreach (var x in await db.DsgServices.AsNoTracking().Select(x => new { x.ServiceCode, x.DsgId }).ToListAsync(ct))
            {
                if (!cat.DsgIdsByService.TryGetValue(x.ServiceCode, out var s)) cat.DsgIdsByService[x.ServiceCode] = s = new();
                s.Add(x.DsgId);
            }
            foreach (var c in await db.Package9Classes.AsNoTracking().ToListAsync(ct))
            {
                cat.ClassById[c.Id] = c;
                cat.ClassByNumber[c.ClassNumber] = c;
            }
            foreach (var x in await db.Package9ClassServices.AsNoTracking().ToListAsync(ct))
            {
                if (!cat.ClassIdsByService.TryGetValue(x.ServiceCode, out var s)) cat.ClassIdsByService[x.ServiceCode] = s = new();
                s.Add(x.ClassId);
            }
            foreach (var x in await db.Package9ClassDiagnoses.AsNoTracking().ToListAsync(ct))
            {
                if (!cat.ClassIdsByDiag.TryGetValue(x.DiagCode, out var s)) cat.ClassIdsByDiag[x.DiagCode] = s = new();
                s.Add(x.ClassId);
            }
            foreach (var x in await db.Package9ClassPositions.AsNoTracking().ToListAsync(ct))
            {
                if (!cat.PositionsByClassId.TryGetValue(x.ClassId, out var s)) cat.PositionsByClassId[x.ClassId] = s = new(StringComparer.OrdinalIgnoreCase);
                s.Add(x.PositionCode);
            }
            foreach (var x in await db.RehabDiagnoses.AsNoTracking().ToListAsync(ct))
            {
                if (!cat.RehabByDiag.TryGetValue(x.DiagCode, out var s)) cat.RehabByDiag[x.DiagCode] = s = new();
                s.Add(x);
            }
            foreach (var x in await db.Icd10.AsNoTracking().ToListAsync(ct)) cat.Icd10Names[x.Code] = x.Name;
            foreach (var x in await db.Achi.AsNoTracking().ToListAsync(ct)) cat.AchiNames[x.Code] = x.Name;
            foreach (var x in await db.ServiceDoctorPositions.AsNoTracking().ToListAsync(ct)) cat.DoctorPositionsByService[x.ServiceCode] = x;
            _catalog = cat;
            _log.LogInformation("Tariff catalog loaded in {Ms} ms: DSG {Dsg}, diag links {Dl}, svc links {Sl}, classes {Cl}", sw.ElapsedMilliseconds, cat.DsgById.Count, cat.DsgIdsByDiag.Count, cat.DsgIdsByService.Count, cat.ClassById.Count);
            return cat;
        }
        finally { _lock.Release(); }
    }
}

public interface IPmgTariffCalculatorService
{
    Task<TariffCalculation> CalculateAsync(TariffRequest req, CancellationToken ct = default);
    TariffCalculation Calculate(TariffRequest req, TariffCatalog cat);
    TariffCalculation CalculateHospitalTariff(string packageNumber, decimal weightCoefficient, string? admissionType, bool isMountain, bool hasMultiSurgery = false, int? patientAge = null, DsgTariffSetting? settings = null);
    TariffCalculation CalculateOutpatientTariff(decimal classCoefficient, bool isMountain = false, DsgTariffSetting? settings = null);
    List<PmgDsg> ResolveDsgCandidates(TariffCatalog cat, string? packageNumber, string? icd, IEnumerable<string> services);
    PmgPackage9Class? ResolveOutpatientClass(TariffCatalog cat, IEnumerable<string> services, string? icd, string? serviceNumber);
}

/// <summary>
/// Автономний тарифний движок ПМГ-2026 (Постанова КМУ № 1808).
/// Стаціонар (3, 4, 47): Тариф = Base × Wg(ДСГ) × k_share(0.55 | 0.60) × k_план(0.80) × k_гір(1.25) × k_мульти(1.30) × k_неонат(1.54)
/// Амбулаторія (9):       Тариф = 155 × K_класу × k_гір
/// Фіксовані пакети:      ставка за випадок / курс / дослідження (dsg_package_tariff_rule)
/// Реабілітація (53/54):  ставка циклу × K_АР
/// </summary>
public class PmgTariffCalculatorService : IPmgTariffCalculatorService
{
    private readonly ITariffCatalogProvider _catalog;
    public PmgTariffCalculatorService(ITariffCatalogProvider catalog) { _catalog = catalog; }

    public static readonly CultureInfo Ua = CultureInfo.GetCultureInfo("uk-UA");

    public async Task<TariffCalculation> CalculateAsync(TariffRequest req, CancellationToken ct = default)
        => Calculate(req, await _catalog.GetAsync(ct));

    public static string NormalizeIcd(string? code)
    {
        if (string.IsNullOrWhiteSpace(code)) return string.Empty;
        var c = code.Trim().ToUpperInvariant();
        var m = Regex.Match(c, @"[A-Z]\d{2}(?:\.\d{1,2})?");
        if (m.Success) return m.Value;
        if (c.Length > 3 && !c.Contains('.')) return c[..3] + "." + c[3..];
        return c;
    }

    public static string NormalizePackage(string? packageName)
    {
        if (string.IsNullOrWhiteSpace(packageName) || packageName.Trim() == "-") return string.Empty;
        var m = Regex.Match(packageName.Trim(), @"^(\d+)");
        return m.Success ? m.Groups[1].Value : packageName.Trim();
    }

    /// <summary>Витягує коди АКПІ з тексту колонки 23 («A67014 Консультація Онколога; 30061-02 ...»)</summary>
    public static List<string> ExtractServiceCodes(string? interventions)
    {
        var res = new List<string>();
        if (string.IsNullOrWhiteSpace(interventions) || interventions.Trim() == "-") return res;
        foreach (Match m in Regex.Matches(interventions, @"\b(\d{5}-\d{2}|[A-Z]\d{5}|[A-Z]{1,2}\d{4,5}(?:-\d{2})?)\b"))
        {
            if (!res.Contains(m.Value)) res.Add(m.Value);
        }
        return res;
    }

    /// <summary>Код МКХ-10 з тексту колонки 18 («ICD10: C61 Злоякісне ...»)</summary>
    public static string ExtractIcd(string? diagnosisText)
    {
        if (string.IsNullOrWhiteSpace(diagnosisText)) return string.Empty;
        var m = Regex.Match(diagnosisText, @"\b([A-Z]\d{2}(?:\.\d{1,2})?)\b");
        return m.Success ? m.Groups[1].Value : string.Empty;
    }

    public static List<string> ExtractIcdList(string? text)
    {
        var res = new List<string>();
        if (string.IsNullOrWhiteSpace(text) || text.Trim() == "-") return res;
        foreach (Match m in Regex.Matches(text, @"\b([A-Z]\d{2}(?:\.\d{1,2})?)\b"))
            if (!res.Contains(m.Value)) res.Add(m.Value);
        return res;
    }

    public List<PmgDsg> ResolveDsgCandidates(TariffCatalog cat, string? packageNumber, string? icd, IEnumerable<string> services)
    {
        var result = new List<PmgDsg>();
        var icdN = NormalizeIcd(icd);
        if (string.IsNullOrEmpty(icdN)) return result;
        HashSet<int>? byDiag = null;
        if (!cat.DsgIdsByDiag.TryGetValue(icdN, out byDiag))
        {
            // спробувати 3-значний код (C18 для C18.0) та зворотно
            var short3 = icdN.Length > 3 ? icdN[..3] : icdN;
            cat.DsgIdsByDiag.TryGetValue(short3, out byDiag);
        }
        if (byDiag == null || byDiag.Count == 0) return result;

        var svcList = services.Select(s => s.Trim()).Where(s => s.Length > 0).ToList();
        HashSet<int>? bySvc = null;
        foreach (var s in svcList)
        {
            if (cat.DsgIdsByService.TryGetValue(s, out var ids))
            {
                bySvc ??= new HashSet<int>();
                bySvc.UnionWith(ids);
            }
        }

        IEnumerable<int> ids2 = byDiag;
        if (!string.IsNullOrEmpty(packageNumber))
            ids2 = ids2.Where(id => cat.DsgById.TryGetValue(id, out var d) && d.PackageNumber == packageNumber);

        var candidates = ids2.Select(id => cat.DsgById[id]).ToList();
        if (bySvc != null)
        {
            // ДСГ, що вимагають послуг: беремо лише ті, де збіглась послуга; ДСГ без послуг — лишаються
            var withSvc = candidates.Where(d => d.SvcCount == 0 || bySvc.Contains(d.Id)).ToList();
            if (withSvc.Count > 0) candidates = withSvc;
            // хірургічні ДСГ (з послугами) мають пріоритет над терапевтичними, якщо послуга збіглась
            var surgical = candidates.Where(d => d.SvcCount > 0 && bySvc.Contains(d.Id)).ToList();
            if (surgical.Count > 0) candidates = surgical;
        }
        else
        {
            // без послуг — ДСГ, що не вимагають операції, якщо такі є
            var noSvc = candidates.Where(d => d.SvcCount == 0).ToList();
            if (noSvc.Count > 0) candidates = noSvc;
        }
        return candidates.OrderByDescending(d => d.WeightCoef).ToList();
    }

    public PmgPackage9Class? ResolveOutpatientClass(TariffCatalog cat, IEnumerable<string> services, string? icd, string? serviceNumber)
    {
        // 1) за номером класу у колонці 36 («C0050 Педіатрія» → клас C0050 не є номером; але «1.1 МРТ» → 1.1)
        if (!string.IsNullOrWhiteSpace(serviceNumber))
        {
            var m = Regex.Match(serviceNumber, @"^(\d+(?:\.\d+)?)\b");
            if (m.Success && cat.ClassByNumber.TryGetValue(m.Groups[1].Value, out var byNum)) return byNum;
        }
        // 2) за кодами послуг (найдорожчий клас серед відповідних)
        var ids = new HashSet<int>();
        foreach (var s in services)
            if (cat.ClassIdsByService.TryGetValue(s, out var set)) ids.UnionWith(set);
        if (ids.Count > 0)
        {
            var icdN = NormalizeIcd(icd);
            var list = ids.Select(i => cat.ClassById[i]).ToList();
            if (!string.IsNullOrEmpty(icdN) && cat.ClassIdsByDiag.TryGetValue(icdN, out var byDiag))
            {
                var narrowed = list.Where(c => byDiag.Contains(c.Id)).ToList();
                if (narrowed.Count > 0) list = narrowed;
            }
            return list.OrderByDescending(c => c.Coefficient).First();
        }
        return null;
    }

    public TariffCalculation Calculate(TariffRequest req, TariffCatalog cat)
    {
        var s = cat.Settings;
        var pkg = NormalizePackage(req.PackageNumber);
        var calc = new TariffCalculation { PackageNumber = pkg };
        if (string.IsNullOrEmpty(pkg))
        {
            calc.Model = "NONE";
            calc.Notes.Add("Пакет послуг не визначено НСЗУ («-») — запис не віднесено до жодного пакету; тариф 0 ₴.");
            if (req.EstimatePotential) Estimate(req, cat, calc, mountain: req.IsMountain ? s.MountainCoef : 1m);
            return calc;
        }
        cat.PackageRules.TryGetValue(pkg, out var rule);
        var model = rule?.Model ?? "FALLBACK";
        calc.Model = model;
        calc.PerPatientPeriod = rule?.PerPatientPeriod ?? false;
        var mountain = req.IsMountain ? s.MountainCoef : 1m;

        switch (model)
        {
            case "DSG":
            {
                PmgDsg? dsg = null;
                if (!string.IsNullOrWhiteSpace(req.AdsgCode) && req.AdsgCode.Trim() != "-")
                {
                    var code = req.AdsgCode.Trim();
                    if (!cat.DsgByPkgCode.TryGetValue($"{pkg}|{code}", out dsg) && cat.DsgByCode.TryGetValue(code, out var l)) dsg = l[0];
                }
                dsg ??= ResolveDsgCandidates(cat, pkg, req.PrimaryIcd10Code, req.ServiceCodes).FirstOrDefault();
                if (dsg == null)
                {
                    calc.Notes.Add("ДСГ не визначено: основний діагноз не входить до переліку діагнозів пакету або відсутня обов'язкова інтервенція АКПІ.");
                    calc.BaseRate = s.BaseRate;
                    if (req.EstimatePotential) Estimate(req, cat, calc, mountain);
                    return calc;
                }
                calc.Resolved = true;
                calc.DsgCode = dsg.DsgCode; calc.DsgName = dsg.Name;
                var share = pkg == "47" ? s.OneDaySurgeryShare : (dsg.GlobalRateShare > 0 ? dsg.GlobalRateShare : s.GlobalRateShare);
                var planned = (pkg == "3" || pkg == "4") && IsPlanned(req.Priority) ? (dsg.PlannedCoef ?? s.PlannedHospitalizationCoef) : 1m;
                var multi = req.HasMultiSurgery && pkg != "4" ? s.MultiSurgeryCoef : 1m;
                var age = req.PatientAge.HasValue && req.PatientAge.Value < s.NeonatalAgeLimitYears && pkg != "47" ? s.NeonatalCoef : 1m;
                return Hospital(calc, s.BaseRate, dsg.WeightCoef, share, planned, mountain, multi, age, dsg.DsgCode);
            }
            case "CLASS":
            {
                var cls = ResolveOutpatientClass(cat, req.ServiceCodes, req.PrimaryIcd10Code, req.ServiceNumber);
                if (cls == null)
                {
                    calc.Notes.Add("Амбулаторний клас не визначено за кодами послуг (колонка 23) — застосовано базову ставку класу 1.00.");
                    return Outpatient(calc, s.OutpatientBaseRate, 1m, mountain, null);
                }
                calc.Resolved = true;
                return Outpatient(calc, s.OutpatientBaseRate, cls.Coefficient, mountain, cls);
            }
            case "FIXED":
            case "FIXED_AGE":
            {
                var rate = rule!.AdultRate;
                var caption = $"Ставка пакету {pkg}";
                if (model == "FIXED_AGE" && rule.ChildRate.HasValue && req.PatientAge.HasValue && req.PatientAge.Value < (rule.ChildAgeLimit ?? 18))
                { rate = rule.ChildRate.Value; caption = $"Дитяча ставка пакету {pkg} (вік < {rule.ChildAgeLimit ?? 18})"; }
                calc.Resolved = true;
                calc.BaseRate = rate; calc.MountainCoef = mountain;
                var total = Math.Round(rate * mountain, 2);
                calc.FullTariff = calc.Tariff = total;
                calc.Steps.Add(new CalculationStep { Code = "BASE", Caption = caption, Value = rate, Operation = "=", RunningTotal = rate, NormativeReference = rule.Source });
                if (mountain != 1m) calc.Steps.Add(new CalculationStep { Code = "PK-04", Caption = "Гірський коефіцієнт", Value = mountain, Operation = "×", RunningTotal = total });
                calc.Formula = mountain != 1m ? $"{Money(rate)} × {mountain} = {Money(total)}" : $"{Money(rate)} (фіксована ставка пакету {pkg})";
                if (rule.Note != null) calc.Notes.Add(rule.Note);
                return calc;
            }
            case "PER_WEEK":
            {
                var weeks = Math.Max(1, req.Weeks);
                var rate = rule!.AdultRate;
                var total = Math.Round(rate * weeks * mountain, 2);
                calc.Resolved = true; calc.BaseRate = rate; calc.Quantity = weeks; calc.MountainCoef = mountain;
                calc.FullTariff = calc.Tariff = total;
                calc.Steps.Add(new CalculationStep { Code = "BASE", Caption = "Ставка за тиждень", Value = rate, Operation = "=", RunningTotal = rate });
                calc.Steps.Add(new CalculationStep { Code = "QTY", Caption = "Кількість тижнів", Value = weeks, Operation = "×", RunningTotal = rate * weeks });
                calc.Formula = $"{Money(rate)} × {weeks} тижн. = {Money(total)}";
                if (rule.Note != null) calc.Notes.Add(rule.Note);
                return calc;
            }
            case "REHAB_CYCLE":
            {
                var rate = rule!.AdultRate;
                var group = req.RehabGroup;
                if (string.IsNullOrEmpty(group))
                {
                    var icdN = NormalizeIcd(req.PrimaryIcd10Code);
                    if (cat.RehabByDiag.TryGetValue(icdN, out var rows) && rows.Count > 0)
                        group = (rows[0].ArGroups ?? "").Split(',', StringSplitOptions.RemoveEmptyEntries).FirstOrDefault();
                }
                var k = 1m;
                if (!string.IsNullOrEmpty(group) && cat.RehabGroups.TryGetValue(group, out var g)) { k = g.Coefficient; calc.Resolved = true; calc.DsgCode = group; }
                else calc.Notes.Add("Групу реабілітації АР не визначено за діагнозом — застосовано АР1 (1.0).");
                var total = Math.Round(rate * k * mountain, 2);
                calc.BaseRate = rate; calc.WeightCoef = k; calc.MountainCoef = mountain; calc.FullTariff = calc.Tariff = total;
                calc.Steps.Add(new CalculationStep { Code = "BASE", Caption = "Ставка реабілітаційного циклу", Value = rate, Operation = "=", RunningTotal = rate });
                calc.Steps.Add(new CalculationStep { Code = "AR", Caption = $"Коефіцієнт групи {group ?? "АР1"}", Value = k, Operation = "×", RunningTotal = rate * k });
                calc.Formula = $"{Money(rate)} × {k} ({group ?? "АР1"}) = {Money(total)}";
                return calc;
            }
            case "GLOBAL":
                calc.Resolved = true;
                calc.Notes.Add(rule?.Note ?? "Глобальна / капітаційна ставка: вартість окремого ЕМЗ не нараховується.");
                calc.Formula = "Глобальна ставка (0 ₴ за ЕМЗ)";
                return calc;
            default:
                if (cat.Packages.TryGetValue(pkg, out var p) && p.BaseRate > 0)
                {
                    calc.Model = "FIXED"; calc.Resolved = true; calc.BaseRate = p.BaseRate;
                    calc.FullTariff = calc.Tariff = Math.Round(p.BaseRate * mountain, 2);
                    calc.Steps.Add(new CalculationStep { Code = "BASE", Caption = $"Базова ставка пакету {pkg} ({p.PaymentModel})", Value = p.BaseRate, Operation = "=", RunningTotal = p.BaseRate });
                    calc.Formula = $"{Money(p.BaseRate)} ({p.RatePeriod})";
                    calc.Notes.Add("Тариф взято з реєстру пакетів; модель оплати пакету потребує підтвердження економістом.");
                    return calc;
                }
                calc.Notes.Add($"Для пакету {pkg} тарифна модель не налаштована (dsg_package_tariff_rule).");
                return calc;
        }
    }

    /// <summary>Оцінка потенційного тарифу для відхилених ЕМЗ без пакету/ДСГ (Lost Revenue = скільки міг би отримати заклад при коректному кодуванні)</summary>
    private void Estimate(TariffRequest req, TariffCatalog cat, TariffCalculation calc, decimal mountain)
    {
        var s = cat.Settings;
        var dsg = ResolveDsgCandidates(cat, null, req.PrimaryIcd10Code, req.ServiceCodes).FirstOrDefault();
        if (dsg != null && (req.EmzType == null || req.EmzType.StartsWith("Взаємод")) && (req.InteractionClass == null || req.InteractionClass.Contains("стаціонар", StringComparison.OrdinalIgnoreCase)))
        {
            var share = dsg.PackageNumber == "47" ? s.OneDaySurgeryShare : s.GlobalRateShare;
            var planned = IsPlanned(req.Priority) && dsg.PackageNumber != "47" ? (dsg.PlannedCoef ?? s.PlannedHospitalizationCoef) : 1m;
            Hospital(calc, s.BaseRate, dsg.WeightCoef, share, planned, mountain, 1m, 1m, dsg.DsgCode);
            calc.Model = "ESTIMATED_DSG"; calc.DsgCode = dsg.DsgCode; calc.DsgName = dsg.Name; calc.PackageNumber = dsg.PackageNumber;
            calc.Notes.Add($"Оцінка: при коректному кодуванні випадок відповідає ДСГ {dsg.DsgCode} пакету {dsg.PackageNumber}.");
            return;
        }
        var cls = ResolveOutpatientClass(cat, req.ServiceCodes, req.PrimaryIcd10Code, null);
        if (cls != null)
        {
            Outpatient(calc, s.OutpatientBaseRate, cls.Coefficient, mountain, cls);
            calc.Model = "ESTIMATED_CLASS"; calc.PackageNumber = "9";
            calc.Notes.Add($"Оцінка: послуги відповідають класу {cls.ClassName} Пакету 9.");
        }
    }

    public static bool IsPlanned(string? priority)
    {
        if (string.IsNullOrWhiteSpace(priority)) return false;
        var p = priority.Trim().ToLowerInvariant();
        return p.StartsWith("план");
    }

    public TariffCalculation CalculateHospitalTariff(string packageNumber, decimal weight, string? admissionType, bool isMountain, bool hasMultiSurgery = false, int? patientAge = null, DsgTariffSetting? settings = null)
    {
        var s = settings ?? new DsgTariffSetting();
        var pkg = NormalizePackage(packageNumber);
        var share = pkg == "47" ? s.OneDaySurgeryShare : s.GlobalRateShare;
        var planned = (pkg == "3" || pkg == "4") && IsPlanned(admissionType) ? s.PlannedHospitalizationCoef : 1m;
        var multi = hasMultiSurgery && pkg != "4" ? s.MultiSurgeryCoef : 1m;
        var age = patientAge.HasValue && patientAge.Value < s.NeonatalAgeLimitYears && pkg != "47" ? s.NeonatalCoef : 1m;
        return Hospital(new TariffCalculation { PackageNumber = pkg, Model = "DSG", Resolved = true }, s.BaseRate, weight, share, planned, isMountain ? s.MountainCoef : 1m, multi, age, null);
    }

    public TariffCalculation CalculateOutpatientTariff(decimal classCoefficient, bool isMountain = false, DsgTariffSetting? settings = null)
    {
        var s = settings ?? new DsgTariffSetting();
        return Outpatient(new TariffCalculation { PackageNumber = "9", Model = "CLASS", Resolved = true }, s.OutpatientBaseRate, classCoefficient, isMountain ? s.MountainCoef : 1m, null);
    }

    private static TariffCalculation Hospital(TariffCalculation c, decimal baseRate, decimal weight, decimal share, decimal planned, decimal mountain, decimal multi, decimal age, string? dsgCode)
    {
        c.BaseRate = baseRate; c.WeightCoef = weight; c.GlobalShare = share; c.PlannedCoef = planned; c.MountainCoef = mountain; c.MultiSurgeryCoef = multi; c.AgeCoef = age;
        decimal run = baseRate;
        c.Steps.Add(new CalculationStep { Code = "BASE", Caption = "Базова ставка (Постанова КМУ № 1808)", Value = baseRate, Operation = "=", RunningTotal = run });
        run *= weight;
        c.Steps.Add(new CalculationStep { Code = "PK-12", Caption = $"Ваговий коефіцієнт ДСГ {dsgCode ?? c.DsgCode}", Value = weight, Operation = "×", RunningTotal = Math.Round(run, 2), NormativeReference = "Додаток 1 до Постанови № 1808 (вагові коефіцієнти ДСГ)" });
        c.FullTariff = Math.Round(run, 2);
        run *= share;
        c.Steps.Add(new CalculationStep { Code = "SHARE", Caption = $"Частка глобальної ставки ({share:0.00})", Value = share, Operation = "×", RunningTotal = Math.Round(run, 2) });
        if (planned != 1m) { run *= planned; c.Steps.Add(new CalculationStep { Code = "PK-02", Caption = "Планова госпіталізація", Value = planned, Operation = "×", RunningTotal = Math.Round(run, 2) }); }
        if (age != 1m) { run *= age; c.Steps.Add(new CalculationStep { Code = "PK-06", Caption = "Неонатальний коефіцієнт (вік < 1 року)", Value = age, Operation = "×", RunningTotal = Math.Round(run, 2) }); }
        if (mountain != 1m) { run *= mountain; c.Steps.Add(new CalculationStep { Code = "PK-04", Caption = "Гірський коефіцієнт", Value = mountain, Operation = "×", RunningTotal = Math.Round(run, 2), NormativeReference = "Закон України «Про статус гірських населених пунктів»" }); }
        if (multi != 1m) { run *= multi; c.Steps.Add(new CalculationStep { Code = "PK-05", Caption = "Мультихірургія (симультанні операції)", Value = multi, Operation = "×", RunningTotal = Math.Round(run, 2) }); }
        c.Tariff = Math.Round(run, 2);
        c.Steps.Add(new CalculationStep { Code = "TOTAL", Caption = "Підсумковий тариф", Value = c.Tariff, Operation = "=", RunningTotal = c.Tariff });
        var parts = new List<string> { Money(baseRate), weight.ToString("0.###", CultureInfo.InvariantCulture), share.ToString("0.00", CultureInfo.InvariantCulture) };
        if (planned != 1m) parts.Add(planned.ToString("0.00", CultureInfo.InvariantCulture) + " (план.)");
        if (age != 1m) parts.Add(age.ToString("0.00", CultureInfo.InvariantCulture) + " (неонат.)");
        if (mountain != 1m) parts.Add(mountain.ToString("0.00", CultureInfo.InvariantCulture) + " (гір.)");
        if (multi != 1m) parts.Add(multi.ToString("0.00", CultureInfo.InvariantCulture) + " (мультихір.)");
        c.Formula = string.Join(" × ", parts) + " = " + Money(c.Tariff);
        return c;
    }

    private static TariffCalculation Outpatient(TariffCalculation c, decimal baseRate, decimal k, decimal mountain, PmgPackage9Class? cls)
    {
        c.BaseRate = baseRate; c.WeightCoef = k; c.MountainCoef = mountain;
        if (cls != null) { c.ClassNumber = cls.ClassNumber; c.DsgCode = cls.ClassNumber; c.DsgName = cls.ClassName; }
        decimal run = baseRate;
        c.Steps.Add(new CalculationStep { Code = "BASE", Caption = "Базова ставка амбулаторної послуги", Value = baseRate, Operation = "=", RunningTotal = run });
        run *= k;
        c.Steps.Add(new CalculationStep { Code = "CLASS", Caption = $"Коефіцієнт класу {cls?.ClassName ?? "1.00"}", Value = k, Operation = "×", RunningTotal = Math.Round(run, 2), NormativeReference = "Пакет 9, перелік 148 класів" });
        c.FullTariff = Math.Round(run, 2);
        if (mountain != 1m) { run *= mountain; c.Steps.Add(new CalculationStep { Code = "PK-04", Caption = "Гірський коефіцієнт", Value = mountain, Operation = "×", RunningTotal = Math.Round(run, 2) }); }
        c.Tariff = Math.Round(run, 2);
        c.Steps.Add(new CalculationStep { Code = "TOTAL", Caption = "Підсумковий тариф", Value = c.Tariff, Operation = "=", RunningTotal = c.Tariff });
        c.Formula = $"{Money(baseRate)} × {k.ToString("0.###", CultureInfo.InvariantCulture)}" + (mountain != 1m ? $" × {mountain}" : "") + $" = {Money(c.Tariff)}";
        return c;
    }

    public static string Money(decimal v) => v.ToString("#,##0.00", CultureInfo.InvariantCulture).Replace(",", " ") + " ₴";
}
