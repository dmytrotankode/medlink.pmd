using MedLink.Pmg.Module.Services;
using Microsoft.AspNetCore.Mvc;

namespace MedLink.Pmg.Module.Controllers;

/// <summary>АРМ лікаря: пре-білінг, Anti-Defektura, матриця комбінацій та бібліотека еталонів</summary>
[ApiController]
[Route("api/v1/pmg")]
public class PmgPrebillingController : ControllerBase
{
    private readonly PrebillingService _prebilling;
    private readonly CombinationService _combinations;
    private readonly IPmgTariffCalculatorService _calc;
    private readonly ITariffCatalogProvider _catalog;

    public PmgPrebillingController(PrebillingService prebilling, CombinationService combinations, IPmgTariffCalculatorService calc, ITariffCatalogProvider catalog)
    { _prebilling = prebilling; _combinations = combinations; _calc = calc; _catalog = catalog; }

    /// <summary>Оцінка взаємодії перед підписанням КЕП (Pre-Flight Check): тариф, дерево розрахунку, знахідки FR/PK, ризик дефектури</summary>
    [HttpPost("prebilling/evaluate")]
    public async Task<IActionResult> Evaluate([FromBody] PrebillingRequest req, CancellationToken ct) => Ok(await _prebilling.EvaluateAsync(req, ct));

    /// <summary>Сумісний з прототипом маршрут (icdCode, serviceCode, doctorPosition, admissionType, isMountain)</summary>
    [HttpPost("prebilling/calculate")]
    public async Task<IActionResult> Calculate([FromBody] PrebillingRequest req, CancellationToken ct)
    {
        var r = await _prebilling.EvaluateAsync(req, ct);
        return Ok(new
        {
            packageNumber = r.PackageNumber, dsgCode = r.DsgCode, dsgName = r.DsgName, classNumber = r.ClassNumber, weightCoefficient = r.WeightCoef, baseRate = r.BaseRate,
            calculatedTariffUah = r.Tariff, fullTariffUah = r.FullTariff, formula = r.Formula, isValid = r.IsValid, status = r.Status, multisurgeryApplied = r.MultisurgeryApplied,
            calculationSteps = r.CalculationSteps, findings = r.Findings, antiDefekturaCheck = r.AntiDefekturaCheck, dsgCandidates = r.DsgCandidates, analysisResultId = r.AnalysisResultId,
        });
    }

    /// <summary>Чистий розрахунок тарифу без правил (для калькулятора та тестів)</summary>
    [HttpPost("tariff/calculate")]
    public async Task<IActionResult> Tariff([FromBody] TariffRequest req, CancellationToken ct) => Ok(await _calc.CalculateAsync(req, ct));

    /// <summary>Кандидати ДСГ за діагнозом та послугами</summary>
    [HttpGet("tariff/dsg-candidates")]
    public async Task<IActionResult> DsgCandidates([FromQuery] string icd, [FromQuery] string? services, [FromQuery] string? package, CancellationToken ct)
    {
        var cat = await _catalog.GetAsync(ct);
        var svc = (services ?? "").Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
        var list = _calc.ResolveDsgCandidates(cat, string.IsNullOrEmpty(package) ? null : package, icd, svc);
        return Ok(list.Select(d => new { d.Id, d.PackageNumber, d.DsgCode, d.Name, d.WeightCoef, d.FullTariff, d.ShareTariff, d.SvcCount, d.DiagCount, d.AdditionalRequirements, d.RequiredPackages }));
    }

    [HttpPost("combinations/validate")]
    public async Task<IActionResult> Validate([FromBody] CombinationValidateRequest req, CancellationToken ct) => Ok(await _combinations.ValidateAsync(req, ct));

    [HttpPost("combinations/library-save")]
    public async Task<IActionResult> LibrarySave([FromBody] CombinationLibrarySaveRequest req, CancellationToken ct)
    {
        var item = await _combinations.SaveToLibraryAsync(req, ct);
        return Ok(new { success = true, message = "Еталон збережено в бібліотеці myAddLib", item });
    }
}
