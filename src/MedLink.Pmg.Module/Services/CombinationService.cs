using System.Text.Json;
using MedLink.Pmg.Module.Data;
using MedLink.Pmg.Module.Models;
using Microsoft.EntityFrameworkCore;

namespace MedLink.Pmg.Module.Services;

/// <summary>
/// 5-рівневий валідатор комбінацій послуг (реінженерія Delphi MedProfit): сумісність МКХ-10,
/// обов'язкові ко-реквізити, несумісні послуги, посада лікаря, мультихірургія 1.30 + бібліотека еталонів myAddLib.
/// </summary>
public class CombinationService
{
    private readonly PmgDbContext _db;
    private readonly IPmgTariffCalculatorService _calc;
    private readonly ITariffCatalogProvider _catalog;
    private record CodeName(string code, string? name);

    public CombinationService(PmgDbContext db, IPmgTariffCalculatorService calc, ITariffCatalogProvider catalog) { _db = db; _calc = calc; _catalog = catalog; }

    private static List<CodeName> Codes(string? json)
    {
        if (string.IsNullOrWhiteSpace(json)) return new();
        try
        {
            using var doc = JsonDocument.Parse(json);
            var list = new List<CodeName>();
            foreach (var el in doc.RootElement.EnumerateArray())
            {
                if (el.ValueKind == JsonValueKind.String) list.Add(new CodeName(el.GetString() ?? "", null));
                else list.Add(new CodeName(el.TryGetProperty("code", out var c) ? c.GetString() ?? "" : "", el.TryGetProperty("name", out var n) ? n.GetString() : null));
            }
            return list;
        }
        catch { return new(); }
    }

    public async Task<object> ValidateAsync(CombinationValidateRequest req, CancellationToken ct = default)
    {
        var cat = await _catalog.GetAsync(ct);
        var service = (req.ServiceCode ?? "").Trim();
        var icd = PmgTariffCalculatorService.NormalizeIcd(req.IcdCode);
        var position = (req.DoctorPosition ?? "").Trim().ToUpperInvariant();
        var companions = (req.CompanionServices ?? new()).Select(s => s.Trim()).Where(s => s.Length > 0).Distinct().ToList();
        var messages = new List<object>();
        int level = 0; bool valid = true;
        void Msg(int lvl, string status, string text) { messages.Add(new { level = lvl, status, text }); if (status == "ERROR") valid = false; }

        var combos = await _db.ServiceCombinations.AsNoTracking().Where(c => c.ServiceCode == service).ToListAsync(ct);
        var combo = combos.FirstOrDefault(c => string.IsNullOrEmpty(icd) || Codes(c.CompatibleIcdCodesJson).Any(x => icd.StartsWith(x.code, StringComparison.OrdinalIgnoreCase) || x.code.StartsWith(icd, StringComparison.OrdinalIgnoreCase))) ?? combos.FirstOrDefault();

        // Рівень 1 — сумісність діагнозу
        level = 1;
        if (combo != null && !string.IsNullOrEmpty(icd))
        {
            var compatible = Codes(combo.CompatibleIcdCodesJson);
            if (compatible.Count == 0 || compatible.Any(x => icd.StartsWith(x.code, StringComparison.OrdinalIgnoreCase) || x.code.StartsWith(icd, StringComparison.OrdinalIgnoreCase)))
                Msg(level, "OK", $"✓ Діагноз {icd} сумісний з послугою {service}");
            else Msg(level, "ERROR", $"⛔ Діагноз {icd} не входить до сумісних для {service}: {string.Join(", ", compatible.Select(x => x.code))}");
        }
        else if (!string.IsNullOrEmpty(icd))
        {
            var dsgs = _calc.ResolveDsgCandidates(cat, null, icd, new[] { service });
            if (dsgs.Count > 0) Msg(level, "OK", $"✓ Діагноз {icd} та послуга {service} утворюють ДСГ {dsgs[0].DsgCode} (вага {dsgs[0].WeightCoef})");
            else Msg(level, "WARNING", $"⚠ Для пари {icd} + {service} ДСГ стаціонару не знайдено");
        }

        // Рівень 2 — обов'язкові ко-реквізити
        level = 2;
        var missingMandatory = new List<CodeName>();
        if (combo != null)
            foreach (var m in Codes(combo.MandatoryCompanionsJson))
                if (!companions.Contains(m.code)) missingMandatory.Add(m);
        if (missingMandatory.Count > 0) Msg(level, "WARNING", "⚠ Відсутні обов'язкові супутні послуги: " + string.Join(", ", missingMandatory.Select(m => $"{m.code} ({m.name})")));
        else if (combo != null) Msg(level, "OK", "✓ Усі обов'язкові супутні послуги присутні");

        // Рівень 3 — несумісні послуги
        level = 3;
        if (combo != null)
        {
            var incompatible = Codes(combo.IncompatibleServicesJson).Where(x => companions.Contains(x.code)).ToList();
            if (incompatible.Count > 0) Msg(level, "ERROR", "⛔ Несумісні послуги у комбінації: " + string.Join(", ", incompatible.Select(x => $"{x.code} ({x.name})")));
            else Msg(level, "OK", "✓ Несумісних послуг не виявлено");
        }

        // Рівень 4 — посада лікаря
        level = 4;
        var posCheck = PrebillingService.CheckDoctorPosition(cat, position, new List<string> { service }.Concat(companions).ToList(), null);
        if (combo != null && !string.IsNullOrEmpty(position))
        {
            var allowed = Codes(combo.AllowedDoctorPositionsJson).Select(x => x.code.ToUpperInvariant()).ToList();
            var prohibited = Codes(combo.ProhibitedDoctorPositionsJson).Select(x => x.code.ToUpperInvariant()).ToList();
            if (prohibited.Contains(position) || (allowed.Count > 0 && !allowed.Contains(position)))
                Msg(level, "ERROR", $"⛔ Помилка посади лікаря {position} (ERR_DOC_SPEC_04). Дозволено: {string.Join(", ", allowed)}");
            else Msg(level, "OK", $"✓ Посада {position} відповідає вимогам");
        }
        else if (posCheck.applicable)
        {
            if (posCheck.valid) Msg(level, "OK", $"✓ Посада {position} відповідає вимогам послуги {posCheck.service}");
            else Msg(level, "ERROR", $"⛔ Посада {position} не дозволена для {posCheck.service} (ERR_DOC_SPEC_04). Дозволено: {posCheck.allowed}");
        }

        // Рівень 5 — мультихірургія
        level = 5;
        bool multi = false;
        if (combo != null)
        {
            var optional = Codes(combo.OptionalMultisurgCompanionsJson);
            multi = optional.Any(o => companions.Contains(o.code));
        }
        if (!multi) multi = companions.Count(c => cat.DsgIdsByService.ContainsKey(c)) >= 1 && cat.DsgIdsByService.ContainsKey(service);
        if (multi) Msg(level, "OK", "✓ Застосовано коефіцієнт мультихірургії 1.30 (+30 %) за симультанні операції");
        else Msg(level, "INFO", "ℹ Мультихірургія не застосовується (одна операція)");

        // Розрахунок
        var pkg = req.PackageNumber ?? combo?.ExpectedPackageNumber;
        var dsgs2 = _calc.ResolveDsgCandidates(cat, pkg, icd, new[] { service }.Concat(companions));
        var dsg = dsgs2.FirstOrDefault();
        TariffCalculation calc;
        if (dsg != null) calc = _calc.CalculateHospitalTariff(dsg.PackageNumber, dsg.WeightCoef, req.AdmissionType, req.IsMountain, multi, req.PatientAge, cat.Settings);
        else if (combo != null) calc = _calc.CalculateHospitalTariff(combo.ExpectedPackageNumber ?? "3", combo.WeightCoef, req.AdmissionType, req.IsMountain, multi, req.PatientAge, cat.Settings);
        else calc = new TariffCalculation { Formula = "ДСГ не визначено" };

        var baseTariff = dsg != null ? _calc.CalculateHospitalTariff(dsg.PackageNumber, dsg.WeightCoef, req.AdmissionType, req.IsMountain, false, req.PatientAge, cat.Settings).Tariff : (combo?.CalculatedTariff ?? 0);
        var libStd = await _db.CombinationLibrary.AsNoTracking().Where(l => l.ServiceCode == service && l.RecordState == 2).OrderByDescending(l => l.CreatedOn).FirstOrDefaultAsync(ct);
        var finalTariff = valid ? calc.Tariff : 0m;
        return new
        {
            isValid = valid, status = valid ? (messages.Any(m => ((dynamic)m).status == "WARNING") ? "WARNING" : "VALID") : "REJECTED_DEFEKTURA",
            serviceCode = service, icdCode = icd, doctorPosition = position, companionServices = companions,
            packageNumber = dsg?.PackageNumber ?? combo?.ExpectedPackageNumber, dsgCode = dsg?.DsgCode ?? combo?.ExpectedDsgCode, dsgName = dsg?.Name ?? combo?.CombinationName,
            weightCoef = dsg?.WeightCoef ?? combo?.WeightCoef ?? 0, appliedCoefficient = multi ? cat.Settings.MultiSurgeryCoef : 1.0m, multisurgeryApplied = multi,
            baseTariffUah = baseTariff, calculatedTariffUah = finalTariff, deltaUah = Math.Round(finalTariff - baseTariff, 2), formula = calc.Formula, calculationSteps = calc.Steps,
            validationMessages = messages, combination = combo,
            libraryStandard = libStd == null ? null : new { libStd.Id, libStd.Name, libStd.StandardTariff, deltaVsStandard = Math.Round(finalTariff - libStd.StandardTariff, 2) },
        };
    }

    public async Task<PmgCombinationLibrary> SaveToLibraryAsync(CombinationLibrarySaveRequest req, CancellationToken ct = default)
    {
        var item = new PmgCombinationLibrary
        {
            OrganizationId = req.OrganizationId, DepartmentId = req.DepartmentId, Name = string.IsNullOrWhiteSpace(req.Name) ? $"Еталон {req.ServiceCode} / {req.IcdCode}" : req.Name,
            ServiceCode = req.ServiceCode, IcdCode = req.IcdCode, CompanionServicesJson = JsonSerializer.Serialize(req.CompanionServices ?? new()), DoctorPosition = req.DoctorPosition,
            PackageNumber = req.PackageNumber, DsgCode = req.DsgCode, StandardTariff = req.StandardTariff, MultisurgeryApplied = req.MultisurgeryApplied, Caption = req.Name,
        };
        _db.CombinationLibrary.Add(item);
        await _db.SaveChangesAsync(ct);
        return item;
    }
}
