using System.Text.Json;
using MedLink.Pmg.Module.Data;
using MedLink.Pmg.Module.Models;
using MedLink.Pmg.Module.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace MedLink.Pmg.Module.Controllers;

/// <summary>Довідники ПМГ-2026 (читання + адміністрування налаштувань тарифів, правил, словника помилок, бібліотеки еталонів)</summary>
[ApiController]
[Route("api/v1/pmg/dictionaries")]
public class PmgDictionariesController : ControllerBase
{
    private readonly PmgDbContext _db;
    private readonly ITariffCatalogProvider _catalog;
    public PmgDictionariesController(PmgDbContext db, ITariffCatalogProvider catalog) { _db = db; _catalog = catalog; }

    private static JsonElement? Parse(string? json) { if (string.IsNullOrWhiteSpace(json)) return null; try { return JsonSerializer.Deserialize<JsonElement>(json); } catch { return null; } }

    // ---------------------------------------------------------------- packages
    [HttpGet("packages")]
    public async Task<IActionResult> Packages([FromQuery] string? category, [FromQuery] string? q)
    {
        var query = _db.Packages.AsNoTracking().AsQueryable();
        if (!string.IsNullOrEmpty(category)) query = query.Where(p => p.Category == category);
        if (!string.IsNullOrEmpty(q)) query = query.Where(p => p.Name.Contains(q) || p.PackageId == q || p.Code.Contains(q));
        var rules = await _db.PackageTariffRules.AsNoTracking().ToDictionaryAsync(r => r.PackageNumber, r => r);
        var list = await query.ToListAsync();
        return Ok(list.OrderBy(p => p.PackageNumber).Select(p => ToPackageDto(p, rules.GetValueOrDefault(p.PackageId))));
    }

    [HttpGet("packages/{id}")]
    public async Task<IActionResult> Package(string id)
    {
        var p = await _db.Packages.AsNoTracking().FirstOrDefaultAsync(x => x.PackageId == id || x.Code == id);
        if (p == null) return NotFound(new { error = $"Package {id} not found" });
        var rule = await _db.PackageTariffRules.AsNoTracking().FirstOrDefaultAsync(r => r.PackageNumber == p.PackageId);
        var dsgCount = await _db.Dsg.CountAsync(d => d.PackageNumber == p.PackageId);
        return Ok(new { package = ToPackageDto(p, rule), dsgCount, tariffRule = rule });
    }

    private static object ToPackageDto(PmgPackage p, DsgPackageTariffRule? rule) => new
    {
        id = p.PackageId, packageId = p.PackageId, packageNumber = p.PackageNumber, code = p.Code, name = p.Name, category = p.Category, payment_model = p.PaymentModel, paymentModel = p.PaymentModel,
        base_rate = p.BaseRate, baseRate = p.BaseRate, rate_period = p.RatePeriod, ratePeriod = p.RatePeriod, chapter_cmu = p.ChapterCmu, formula = p.Formula, description = p.Description,
        coefficients = Parse(p.CoefficientsJson), law_references = Parse(p.LawReferencesJson), ehealth_validations = Parse(p.EhealthValidationsJson), group_file = p.GroupFile,
        tariffModel = rule?.Model, tariffNote = rule?.Note,
    };

    [HttpGet("packages-categories")]
    public async Task<IActionResult> Categories() => Ok(await _db.Packages.AsNoTracking().GroupBy(p => p.Category).Select(g => new { category = g.Key, count = g.Count() }).ToListAsync());

    // ---------------------------------------------------------------- DSG
    [HttpGet("dsg")]
    public async Task<IActionResult> Dsg([FromQuery] string? q, [FromQuery] string? package, [FromQuery] string? serviceType, [FromQuery] int page = 1, [FromQuery] int pageSize = 100)
    {
        var query = _db.Dsg.AsNoTracking().AsQueryable();
        if (!string.IsNullOrEmpty(package) && package != "all") query = query.Where(d => d.PackageNumber == package);
        if (!string.IsNullOrEmpty(serviceType)) query = query.Where(d => d.ServiceType == serviceType);
        if (!string.IsNullOrEmpty(q)) query = query.Where(d => d.DsgCode.StartsWith(q.ToUpper()) || d.Name.Contains(q));
        var total = await query.CountAsync();
        var items = await query.OrderBy(d => d.PackageNumber).ThenBy(d => d.DsgCode).Skip((page - 1) * pageSize).Take(Math.Clamp(pageSize, 1, 500)).ToListAsync();
        return Ok(new { total, page, pageSize, items });
    }

    [HttpGet("dsg/{id:int}")]
    public async Task<IActionResult> DsgDetail(int id)
    {
        var d = await _db.Dsg.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        if (d == null) return NotFound();
        var cat = await _catalog.GetAsync();
        var diags = await _db.DsgDiagnoses.AsNoTracking().Where(x => x.DsgId == id).Select(x => x.DiagCode).ToListAsync();
        var svcs = await _db.DsgServices.AsNoTracking().Where(x => x.DsgId == id).Select(x => x.ServiceCode).ToListAsync();
        return Ok(new
        {
            dsg = d, diagnoses = diags.Select(c => new { code = c, name = cat.Icd10Names.GetValueOrDefault(c) }), services = svcs.Select(c => new { code = c, name = cat.AchiNames.GetValueOrDefault(c) }),
            ageNotes = Parse(d.AgeNotesJson), additionalRequirementsServices = Parse(d.AdditionalRequirementsServicesJson),
        });
    }

    [HttpGet("dsg/by-code/{code}")]
    public async Task<IActionResult> DsgByCode(string code)
    {
        var list = await _db.Dsg.AsNoTracking().Where(d => d.DsgCode == code).ToListAsync();
        return list.Count == 0 ? NotFound() : Ok(list);
    }

    /// <summary>Пошук ДСГ за діагнозом (у які ДСГ/пакети входить код МКХ-10)</summary>
    [HttpGet("dsg/by-diagnosis/{icd}")]
    public async Task<IActionResult> DsgByDiagnosis(string icd)
    {
        var n = PmgTariffCalculatorService.NormalizeIcd(icd);
        var ids = await _db.DsgDiagnoses.AsNoTracking().Where(x => x.DiagCode == n).Select(x => x.DsgId).Distinct().ToListAsync();
        var list = await _db.Dsg.AsNoTracking().Where(d => ids.Contains(d.Id)).OrderByDescending(d => d.WeightCoef).ToListAsync();
        return Ok(list);
    }

    // ---------------------------------------------------------------- classes / rehab / codes
    [HttpGet("classes")]
    public async Task<IActionResult> Classes([FromQuery] string? q, [FromQuery] string? serviceType)
    {
        var query = _db.Package9Classes.AsNoTracking().AsQueryable();
        if (!string.IsNullOrEmpty(serviceType)) query = query.Where(c => c.ServiceType == serviceType);
        if (!string.IsNullOrEmpty(q)) query = query.Where(c => c.ClassName.Contains(q) || c.ClassNumber.StartsWith(q));
        var list = await query.OrderBy(c => c.Id).ToListAsync();
        return Ok(list.Select(c => new { c.Id, c.ClassNumber, c.ClassName, c.ServiceType, c.Coefficient, c.Cost, c.DiagCount, c.SvcCount, c.Note, c.AdditionalRequirementsCode, positions = Parse(c.PositionsJson), episode = Parse(c.EpisodeJson) }));
    }

    [HttpGet("classes/{id:int}")]
    public async Task<IActionResult> ClassDetail(int id)
    {
        var c = await _db.Package9Classes.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        if (c == null) return NotFound();
        var cat = await _catalog.GetAsync();
        var svcs = await _db.Package9ClassServices.AsNoTracking().Where(x => x.ClassId == id).Select(x => x.ServiceCode).ToListAsync();
        var diags = await _db.Package9ClassDiagnoses.AsNoTracking().Where(x => x.ClassId == id).Select(x => x.DiagCode).ToListAsync();
        var pos = await _db.Package9ClassPositions.AsNoTracking().Where(x => x.ClassId == id).ToListAsync();
        return Ok(new { @class = c, services = svcs.Select(s => new { code = s, name = cat.AchiNames.GetValueOrDefault(s) }), diagnoses = diags.Select(d => new { code = d, name = cat.Icd10Names.GetValueOrDefault(d) }), positions = pos });
    }

    [HttpGet("rehab")]
    public async Task<IActionResult> Rehab([FromQuery] string? q, [FromQuery] string? ar, [FromQuery] int page = 1, [FromQuery] int pageSize = 100)
    {
        var query = _db.RehabDiagnoses.AsNoTracking().AsQueryable();
        if (!string.IsNullOrEmpty(q)) query = query.Where(d => d.DiagCode.StartsWith(q.ToUpper()) || (d.Name != null && d.Name.Contains(q)));
        if (!string.IsNullOrEmpty(ar)) query = query.Where(d => d.ArGroups != null && d.ArGroups.Contains(ar));
        var total = await query.CountAsync();
        var items = await query.OrderBy(d => d.Id).Skip((page - 1) * pageSize).Take(Math.Clamp(pageSize, 1, 500)).ToListAsync();
        return Ok(new { total, page, pageSize, items, groups = await _db.RehabGroups.AsNoTracking().ToListAsync(), rules = await _db.RehabRules.AsNoTracking().ToListAsync(), services = await _db.RehabServices.AsNoTracking().ToListAsync() });
    }

    [HttpGet("icd10")]
    public async Task<IActionResult> Icd10([FromQuery] string q, [FromQuery] int take = 30)
    {
        var n = (q ?? "").Trim().ToUpperInvariant();
        return Ok(await _db.Icd10.AsNoTracking().Where(x => x.Code.StartsWith(n) || x.Name.Contains(q ?? "")).OrderBy(x => x.Code).Take(Math.Clamp(take, 1, 200)).ToListAsync());
    }

    [HttpGet("achi")]
    public async Task<IActionResult> Achi([FromQuery] string q, [FromQuery] int take = 30)
    {
        var n = (q ?? "").Trim();
        return Ok(await _db.Achi.AsNoTracking().Where(x => x.Code.StartsWith(n) || x.Name.Contains(n)).OrderBy(x => x.Code).Take(Math.Clamp(take, 1, 200)).ToListAsync());
    }

    [HttpGet("positions")]
    public IActionResult Positions() => Ok(MedLinkDemoDataService.PositionCodes.Select(kv => new { code = kv.Value, name = kv.Key }).OrderBy(x => int.Parse(x.code[1..])));

    // ---------------------------------------------------------------- errors (CRUD)
    [HttpGet("errors")]
    public async Task<IActionResult> Errors([FromQuery] string? q, [FromQuery] string? category, [FromQuery] int? severity)
    {
        var query = _db.ErrorDictionary.AsNoTracking().AsQueryable();
        if (!string.IsNullOrEmpty(category)) query = query.Where(e => e.Category == category);
        if (severity.HasValue) query = query.Where(e => e.Severity == severity);
        if (!string.IsNullOrEmpty(q)) query = query.Where(e => e.ErrorCode.Contains(q.ToUpper()) || e.Title.Contains(q) || e.Description.Contains(q));
        return Ok(await query.OrderBy(e => e.Id).ToListAsync());
    }

    [HttpGet("errors/official")]
    public async Task<IActionResult> OfficialErrors() => Ok(await _db.ErrorDescriptions.AsNoTracking().OrderBy(e => e.Section).ThenBy(e => e.CommentText).ToListAsync());

    [HttpPost("errors")]
    public async Task<IActionResult> CreateError([FromBody] PmgNhsuErrorDictionary e)
    {
        if (await _db.ErrorDictionary.AnyAsync(x => x.ErrorCode == e.ErrorCode)) return Conflict(new { error = "Код помилки вже існує" });
        e.Id = (await _db.ErrorDictionary.MaxAsync(x => (int?)x.Id) ?? 0) + 1;
        _db.ErrorDictionary.Add(e); await _db.SaveChangesAsync(); _catalog.Invalidate();
        return Created($"/api/v1/pmg/dictionaries/errors/{e.Id}", e);
    }

    [HttpPut("errors/{id:int}")]
    public async Task<IActionResult> UpdateError(int id, [FromBody] PmgNhsuErrorDictionary e)
    {
        var x = await _db.ErrorDictionary.FirstOrDefaultAsync(z => z.Id == id);
        if (x == null) return NotFound();
        x.Title = e.Title; x.Description = e.Description; x.NormativeReference = e.NormativeReference; x.RemediationAdvice = e.RemediationAdvice; x.Severity = e.Severity; x.Category = e.Category; x.RecoverabilityPercent = e.RecoverabilityPercent; x.NszuCommentPattern = e.NszuCommentPattern;
        await _db.SaveChangesAsync(); _catalog.Invalidate();
        return Ok(x);
    }

    [HttpDelete("errors/{id:int}")]
    public async Task<IActionResult> DeleteError(int id)
    {
        var x = await _db.ErrorDictionary.FirstOrDefaultAsync(z => z.Id == id);
        if (x == null) return NotFound();
        _db.ErrorDictionary.Remove(x); await _db.SaveChangesAsync(); _catalog.Invalidate();
        return Ok(new { deleted = true });
    }

    // ---------------------------------------------------------------- doctor positions / lab / rules
    [HttpGet("doctor-positions")]
    public async Task<IActionResult> DoctorPositions([FromQuery] string? q, [FromQuery] int take = 200)
    {
        var query = _db.ServiceDoctorPositions.AsNoTracking().AsQueryable();
        if (!string.IsNullOrEmpty(q)) query = query.Where(p => p.ServiceCode.StartsWith(q) || p.ServiceName.Contains(q) || p.PositionRequirements.Contains(q.ToUpper()));
        return Ok(await query.OrderBy(p => p.ServiceCode).Take(Math.Clamp(take, 1, 2000)).ToListAsync());
    }

    [HttpGet("lab-tests")]
    public async Task<IActionResult> LabTests([FromQuery] string? q, [FromQuery] string? group)
    {
        var query = _db.LaboratoryCatalog.AsNoTracking().AsQueryable();
        if (!string.IsNullOrEmpty(group)) query = query.Where(t => t.TestGroup == group);
        if (!string.IsNullOrEmpty(q)) query = query.Where(t => t.TestCode.StartsWith(q.ToUpper()) || t.TestName.Contains(q));
        return Ok(await query.OrderBy(t => t.TestCode).ToListAsync());
    }

    [HttpGet("rules")]
    public async Task<IActionResult> Rules([FromQuery] string? type)
    {
        var q = _db.ClassificationRules.AsNoTracking().AsQueryable();
        if (!string.IsNullOrEmpty(type)) q = q.Where(r => r.RuleType == type);
        var list = await q.OrderBy(r => r.Id).ToListAsync();
        return Ok(list.Select(r => new { r.Id, r.LegacyRuleId, r.RuleType, r.RuleCode, r.RuleGroup, ruleData = Parse(r.RuleDataJson) }));
    }

    // ---------------------------------------------------------------- services / groups / combinations
    [HttpGet("service-groups")]
    public async Task<IActionResult> ServiceGroups()
    {
        var groups = await _db.ServiceGroups.AsNoTracking().OrderBy(g => g.Code).ToListAsync();
        var counts = await _db.ServiceCatalog.AsNoTracking().GroupBy(s => s.GroupId).Select(g => new { g.Key, c = g.Count() }).ToDictionaryAsync(x => x.Key ?? "", x => x.c);
        return Ok(groups.Select(g => new { g.Id, g.Code, g.Name, g.ParentId, g.Level, g.Description, service_count = counts.GetValueOrDefault(g.Id), serviceCount = counts.GetValueOrDefault(g.Id) }));
    }

    [HttpGet("services")]
    public async Task<IActionResult> Services([FromQuery] string? groupId, [FromQuery] string? category, [FromQuery] string? q)
    {
        var query = _db.ServiceCatalog.AsNoTracking().AsQueryable();
        if (!string.IsNullOrEmpty(groupId)) query = query.Where(s => s.GroupId == groupId);
        if (!string.IsNullOrEmpty(category)) query = query.Where(s => s.Category == category);
        if (!string.IsNullOrEmpty(q)) query = query.Where(s => s.ServiceCode.StartsWith(q) || s.Name.Contains(q));
        var list = await query.OrderBy(s => s.ServiceCode).ToListAsync();
        return Ok(list.Select(s => new { s.ServiceCode, service_code = s.ServiceCode, s.Name, name = s.Name, s.GroupId, s.GroupName, s.Category, s.BaseNormTimeMinutes, s.AnesthesiaRequired, s.MinStayDays, s.MaxStayDays, s.AgeMin, s.AgeMax, s.GenderRestriction, s.PackageIds, s.DsgCodes, s.BaseTariff, s.ClinicalNormNotes }));
    }

    [HttpGet("services/{code}")]
    public async Task<IActionResult> ServiceDetail(string code)
    {
        var svc = await _db.ServiceCatalog.AsNoTracking().FirstOrDefaultAsync(s => s.ServiceCode == code);
        var cat = await _catalog.GetAsync();
        if (svc == null)
        {
            if (!cat.AchiNames.TryGetValue(code, out var name)) return NotFound(new { error = $"Service {code} not found" });
            svc = new PmgServiceCatalog { ServiceCode = code, Name = name, Category = cat.DsgIdsByService.ContainsKey(code) ? "Surgical" : "Outpatient" };
        }
        var combs = await _db.ServiceCombinations.AsNoTracking().Where(c => c.ServiceCode == code).ToListAsync();
        var doctorRules = await _db.ServiceDoctorPositions.AsNoTracking().Where(p => p.ServiceCode == code).ToListAsync();
        var dsgIds = cat.DsgIdsByService.GetValueOrDefault(code) ?? new HashSet<int>();
        var dsgs = dsgIds.Select(i => cat.DsgById[i]).OrderByDescending(d => d.WeightCoef).Select(d => new { d.Id, d.PackageNumber, d.DsgCode, d.Name, d.WeightCoef, d.ShareTariff }).ToList();
        var classes = (cat.ClassIdsByService.GetValueOrDefault(code) ?? new HashSet<int>()).Select(i => cat.ClassById[i]).Select(c => new { c.Id, c.ClassNumber, c.ClassName, c.Coefficient, c.Cost }).ToList();
        var encounters = await _db.StatementLines.AsNoTracking().Where(l => l.Interventions != null && l.Interventions.Contains(code)).OrderByDescending(l => l.PeriodStart).Take(25)
            .Select(l => new { l.Id, l.StatementId, l.EncounterEhealthId, l.PeriodStart, l.PractitionerName, l.PractitionerPosition, l.PrimaryIcd10Code, l.PackageNumber, l.DsgCode, l.MisAmount, l.IncludedInReport, l.ErrorComment, l.MatchedEncounterId }).ToListAsync();
        var riskCodes = new[] { "ERR_DOC_SPEC_04", "ERR_SURG_NO_OP_05", "ERR_NO_PKG_02", "ERR_STAY_TOO_SHORT_06", "ERR_ONCO_HISTO_11" };
        var risks = await _db.ErrorDictionary.AsNoTracking().Where(e => riskCodes.Contains(e.ErrorCode)).ToListAsync();
        return Ok(new
        {
            service = svc, combinations = combs.Select(c => new
            {
                c.Id, c.ServiceCode, c.CombinationName, compatibleIcdCodes = Parse(c.CompatibleIcdCodesJson), mandatoryCompanions = Parse(c.MandatoryCompanionsJson), optionalMultisurgCompanions = Parse(c.OptionalMultisurgCompanionsJson),
                incompatibleServices = Parse(c.IncompatibleServicesJson), allowedDoctorPositions = Parse(c.AllowedDoctorPositionsJson), prohibitedDoctorPositions = Parse(c.ProhibitedDoctorPositionsJson),
                c.ExpectedPackageNumber, c.ExpectedDsgCode, c.WeightCoef, c.CalculatedTariff, c.CalculationFormula, c.RuleCondition, c.IsLibraryStandard,
            }),
            doctorRules, dsgs, classes, encounters, defekturaRisks = risks,
            library = await _db.CombinationLibrary.AsNoTracking().Where(l => l.ServiceCode == code && l.RecordState == 2).ToListAsync(),
        });
    }

    // ---------------------------------------------------------------- combination library (myAddLib) CRUD
    [HttpGet("library")]
    public async Task<IActionResult> Library([FromQuery] Guid? departmentId) => Ok(await _db.CombinationLibrary.AsNoTracking().Where(l => l.RecordState == 2 && (!departmentId.HasValue || l.DepartmentId == departmentId)).OrderByDescending(l => l.CreatedOn).ToListAsync());

    [HttpPut("library/{id:guid}")]
    public async Task<IActionResult> UpdateLibrary(Guid id, [FromBody] PmgCombinationLibrary item)
    {
        var x = await _db.CombinationLibrary.FirstOrDefaultAsync(l => l.Id == id);
        if (x == null) return NotFound();
        x.Name = item.Name; x.IcdCode = item.IcdCode; x.CompanionServicesJson = item.CompanionServicesJson; x.DoctorPosition = item.DoctorPosition; x.PackageNumber = item.PackageNumber; x.DsgCode = item.DsgCode; x.StandardTariff = item.StandardTariff; x.MultisurgeryApplied = item.MultisurgeryApplied; x.IsApproved = item.IsApproved; x.DepartmentId = item.DepartmentId; x.ModifiedOn = DateTime.UtcNow;
        await _db.SaveChangesAsync();
        return Ok(x);
    }

    [HttpDelete("library/{id:guid}")]
    public async Task<IActionResult> DeleteLibrary(Guid id)
    {
        var x = await _db.CombinationLibrary.FirstOrDefaultAsync(l => l.Id == id);
        if (x == null) return NotFound();
        x.RecordState = 4; x.ModifiedOn = DateTime.UtcNow; await _db.SaveChangesAsync();
        return Ok(new { deleted = true });
    }

    // ---------------------------------------------------------------- tariff settings / package rules / rule configs (Admin)
    [HttpGet("tariff-settings")]
    public async Task<IActionResult> TariffSettings() => Ok(await _db.TariffSettings.AsNoTracking().OrderByDescending(s => s.ValidFrom).ToListAsync());

    [HttpPut("tariff-settings/{id:guid}")]
    public async Task<IActionResult> UpdateTariffSettings(Guid id, [FromBody] DsgTariffSetting s)
    {
        var x = await _db.TariffSettings.FirstOrDefaultAsync(t => t.Id == id);
        if (x == null) return NotFound();
        x.Caption = s.Caption; x.BaseRate = s.BaseRate; x.OutpatientBaseRate = s.OutpatientBaseRate; x.GlobalRateShare = s.GlobalRateShare; x.OneDaySurgeryShare = s.OneDaySurgeryShare; x.PlannedHospitalizationCoef = s.PlannedHospitalizationCoef;
        x.MountainCoef = s.MountainCoef; x.MultiSurgeryCoef = s.MultiSurgeryCoef; x.NeonatalCoef = s.NeonatalCoef; x.NeonatalAgeLimitYears = s.NeonatalAgeLimitYears; x.RecoverabilityDefaultPercent = s.RecoverabilityDefaultPercent; x.ValidFrom = s.ValidFrom; x.ValidTo = s.ValidTo; x.BudgetBalanceCoef = s.BudgetBalanceCoef; x.IsActive = s.IsActive; x.ModifiedOn = DateTime.UtcNow;
        await _db.SaveChangesAsync(); _catalog.Invalidate();
        return Ok(x);
    }

    [HttpPost("tariff-settings")]
    public async Task<IActionResult> CreateTariffSettings([FromBody] DsgTariffSetting s)
    {
        s.Id = Guid.NewGuid(); s.CreatedOn = DateTime.UtcNow;
        if (s.IsActive) foreach (var o in await _db.TariffSettings.Where(t => t.IsActive).ToListAsync()) o.IsActive = false;
        _db.TariffSettings.Add(s); await _db.SaveChangesAsync(); _catalog.Invalidate();
        return Created($"/api/v1/pmg/dictionaries/tariff-settings/{s.Id}", s);
    }

    [HttpGet("package-rules")]
    public async Task<IActionResult> PackageRules() => Ok(await _db.PackageTariffRules.AsNoTracking().OrderBy(r => r.PackageNumber.Length).ThenBy(r => r.PackageNumber).ToListAsync());

    [HttpPost("package-rules")]
    public async Task<IActionResult> CreatePackageRule([FromBody] DsgPackageTariffRule r)
    {
        r.Id = Guid.NewGuid(); r.CreatedOn = DateTime.UtcNow; r.Caption ??= $"Пакет {r.PackageNumber} — {r.Model}";
        _db.PackageTariffRules.Add(r); await _db.SaveChangesAsync(); _catalog.Invalidate();
        return Created($"/api/v1/pmg/dictionaries/package-rules/{r.Id}", r);
    }

    [HttpPut("package-rules/{id:guid}")]
    public async Task<IActionResult> UpdatePackageRule(Guid id, [FromBody] DsgPackageTariffRule r)
    {
        var x = await _db.PackageTariffRules.FirstOrDefaultAsync(t => t.Id == id);
        if (x == null) return NotFound();
        x.PackageNumber = r.PackageNumber; x.Model = r.Model; x.AdultRate = r.AdultRate; x.ChildRate = r.ChildRate; x.ChildAgeLimit = r.ChildAgeLimit; x.Note = r.Note; x.Source = r.Source; x.IsActive = r.IsActive; x.Caption = r.Caption; x.ModifiedOn = DateTime.UtcNow;
        await _db.SaveChangesAsync(); _catalog.Invalidate();
        return Ok(x);
    }

    [HttpDelete("package-rules/{id:guid}")]
    public async Task<IActionResult> DeletePackageRule(Guid id)
    {
        var x = await _db.PackageTariffRules.FirstOrDefaultAsync(t => t.Id == id);
        if (x == null) return NotFound();
        _db.PackageTariffRules.Remove(x); await _db.SaveChangesAsync(); _catalog.Invalidate();
        return Ok(new { deleted = true });
    }

    [HttpGet("rule-configs")]
    public async Task<IActionResult> RuleConfigs() => Ok(await _db.RuleConfigs.AsNoTracking().OrderBy(r => r.RuleCode).ToListAsync());

    [HttpPost("rule-configs")]
    public async Task<IActionResult> CreateRuleConfig([FromBody] DsgRuleConfig r)
    {
        r.Id = Guid.NewGuid(); r.CreatedOn = DateTime.UtcNow;
        _db.RuleConfigs.Add(r); await _db.SaveChangesAsync();
        return Created($"/api/v1/pmg/dictionaries/rule-configs/{r.Id}", r);
    }

    [HttpPut("rule-configs/{id:guid}")]
    public async Task<IActionResult> UpdateRuleConfig(Guid id, [FromBody] DsgRuleConfig r)
    {
        var x = await _db.RuleConfigs.FirstOrDefaultAsync(t => t.Id == id);
        if (x == null) return NotFound();
        x.RuleCode = r.RuleCode; x.Caption = r.Caption; x.PackageNumber = r.PackageNumber; x.Severity = r.Severity; x.NormativeReference = r.NormativeReference; x.IsActive = r.IsActive; x.ConfigParamsJson = r.ConfigParamsJson; x.ModifiedOn = DateTime.UtcNow;
        await _db.SaveChangesAsync();
        return Ok(x);
    }

    [HttpDelete("rule-configs/{id:guid}")]
    public async Task<IActionResult> DeleteRuleConfig(Guid id)
    {
        var x = await _db.RuleConfigs.FirstOrDefaultAsync(t => t.Id == id);
        if (x == null) return NotFound();
        _db.RuleConfigs.Remove(x); await _db.SaveChangesAsync();
        return Ok(new { deleted = true });
    }

    /// <summary>Статистика наповнення довідників</summary>
    [HttpGet("stats")]
    public async Task<IActionResult> Stats() => Ok(new
    {
        packages = await _db.Packages.CountAsync(), dsg = await _db.Dsg.CountAsync(), dsgDiagnoses = await _db.DsgDiagnoses.CountAsync(), dsgServices = await _db.DsgServices.CountAsync(),
        icd10 = await _db.Icd10.CountAsync(), achi = await _db.Achi.CountAsync(), classes = await _db.Package9Classes.CountAsync(), rehabDiagnoses = await _db.RehabDiagnoses.CountAsync(), rehabRules = await _db.RehabRules.CountAsync(), rehabServices = await _db.RehabServices.CountAsync(),
        errors = await _db.ErrorDictionary.CountAsync(), officialErrorDescriptions = await _db.ErrorDescriptions.CountAsync(), doctorPositions = await _db.ServiceDoctorPositions.CountAsync(), labTests = await _db.LaboratoryCatalog.CountAsync(), rules = await _db.ClassificationRules.CountAsync(),
        serviceGroups = await _db.ServiceGroups.CountAsync(), services = await _db.ServiceCatalog.CountAsync(), combinations = await _db.ServiceCombinations.CountAsync(), library = await _db.CombinationLibrary.CountAsync(l => l.RecordState == 2),
        tariffSettings = await _db.TariffSettings.CountAsync(), packageRules = await _db.PackageTariffRules.CountAsync(), ruleConfigs = await _db.RuleConfigs.CountAsync(),
    });
}
