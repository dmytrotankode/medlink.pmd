using System.Text.Json;
using MedLink.Pmg.Module.Data;
using MedLink.Pmg.Module.Models;
using MedLink.Pmg.Module.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace MedLink.Pmg.Module.Controllers;

/// <summary>
/// Сутності ядра МІС «Медлінк» (заклади, відділення, співробітники, пацієнти, ЕМЗ): повний CRUD,
/// м'яке видалення (record_state = 4) та життєвий цикл ЕМЗ (Draft → Signed → Submitted → Accepted/Rejected → Corrected → Resubmitted).
/// У бойовому evomis ці операції виконує існуюче ядро; тут вони потрібні для автономного стенду та тестів.
/// </summary>
[ApiController]
[Route("api/v1/medlink")]
public class MedLinkEntitiesController : ControllerBase
{
    private readonly PmgDbContext _db;
    private readonly PrebillingService _prebilling;
    public MedLinkEntitiesController(PmgDbContext db, PrebillingService prebilling) { _db = db; _prebilling = prebilling; }

    private static void Touch(CoreEntity e, Guid? user) { e.ModifiedOn = DateTime.UtcNow; e.ModifiedBy = user ?? Guid.Empty; }

    // ---------------------------------------------------------------- legal entities
    [HttpGet("legal-entities")]
    public async Task<IActionResult> LegalEntities([FromQuery] bool includeDeleted = false)
    {
        var list = await _db.LegalEntities.AsNoTracking().Where(o => includeDeleted || o.RecordState == 2).OrderBy(o => o.ShortName).ToListAsync();
        var stats = await _db.Encounters.AsNoTracking().Where(e => e.RecordState == 2).GroupBy(e => e.LegalEntityId).Select(g => new { g.Key, c = g.Count() }).ToDictionaryAsync(x => x.Key, x => x.c);
        var stmts = await _db.Statements.AsNoTracking().Where(s => s.RecordState == 2).GroupBy(s => s.OrganizationId).Select(g => new { g.Key, c = g.Count() }).ToDictionaryAsync(x => x.Key, x => x.c);
        return Ok(list.Select(o => new { entity = o, encounters = stats.GetValueOrDefault(o.Id), statements = stmts.GetValueOrDefault(o.Id) }));
    }

    [HttpGet("legal-entities/{id:guid}")]
    public async Task<IActionResult> LegalEntity(Guid id)
    {
        var o = await _db.LegalEntities.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        return o == null ? NotFound() : Ok(o);
    }

    [HttpPost("legal-entities")]
    public async Task<IActionResult> CreateLegalEntity([FromBody] OrgLegalEntity o)
    {
        if (string.IsNullOrWhiteSpace(o.ShortName)) return BadRequest(new { error = "ShortName обов'язковий" });
        o.Id = Guid.NewGuid(); o.CreatedOn = DateTime.UtcNow; o.RecordState = 2; o.Caption ??= o.ShortName;
        _db.LegalEntities.Add(o); await _db.SaveChangesAsync();
        return Created($"/api/v1/medlink/legal-entities/{o.Id}", o);
    }

    [HttpPut("legal-entities/{id:guid}")]
    public async Task<IActionResult> UpdateLegalEntity(Guid id, [FromBody] OrgLegalEntity o)
    {
        var x = await _db.LegalEntities.FirstOrDefaultAsync(z => z.Id == id);
        if (x == null) return NotFound();
        x.Edrpou = o.Edrpou; x.ShortName = o.ShortName; x.FullName = o.FullName; x.Region = o.Region; x.IsMountain = o.IsMountain; x.EhealthLegalEntityId = o.EhealthLegalEntityId; x.Caption = o.Caption ?? o.ShortName; Touch(x, o.ModifiedBy);
        await _db.SaveChangesAsync();
        return Ok(x);
    }

    [HttpDelete("legal-entities/{id:guid}")]
    public async Task<IActionResult> DeleteLegalEntity(Guid id)
    {
        var x = await _db.LegalEntities.FirstOrDefaultAsync(z => z.Id == id);
        if (x == null) return NotFound();
        if (await _db.Statements.AnyAsync(s => s.OrganizationId == id && s.RecordState == 2)) return Conflict(new { error = "Заклад має імпортовані звіти — спершу видаліть або архівуйте їх" });
        x.RecordState = 4; Touch(x, null); await _db.SaveChangesAsync();
        return Ok(new { deleted = true, soft = true });
    }

    // ---------------------------------------------------------------- departments
    [HttpGet("departments")]
    public async Task<IActionResult> Departments([FromQuery] Guid? legalEntityId, [FromQuery] bool includeDeleted = false)
    {
        var q = _db.Departments.AsNoTracking().Where(d => includeDeleted || d.RecordState == 2);
        if (legalEntityId.HasValue) q = q.Where(d => d.LegalEntityId == legalEntityId);
        var list = await q.OrderBy(d => d.Name).ToListAsync();
        var emp = await _db.Employees.AsNoTracking().Where(e => e.RecordState == 2).GroupBy(e => e.DepartmentId).Select(g => new { g.Key, c = g.Count() }).ToDictionaryAsync(x => x.Key ?? Guid.Empty, x => x.c);
        var enc = await _db.Encounters.AsNoTracking().Where(e => e.RecordState == 2).GroupBy(e => e.DepartmentId).Select(g => new { g.Key, c = g.Count() }).ToDictionaryAsync(x => x.Key ?? Guid.Empty, x => x.c);
        return Ok(list.Select(d => new { department = d, employees = emp.GetValueOrDefault(d.Id), encounters = enc.GetValueOrDefault(d.Id) }));
    }

    [HttpPost("departments")]
    public async Task<IActionResult> CreateDepartment([FromBody] OrgDepartment d)
    {
        if (string.IsNullOrWhiteSpace(d.Name)) return BadRequest(new { error = "Name обов'язковий" });
        d.Id = Guid.NewGuid(); d.CreatedOn = DateTime.UtcNow; d.RecordState = 2; d.Caption ??= d.Name;
        if (string.IsNullOrEmpty(d.Code)) d.Code = "D" + (await _db.Departments.CountAsync(x => x.LegalEntityId == d.LegalEntityId) + 1).ToString("00");
        _db.Departments.Add(d); await _db.SaveChangesAsync();
        return Created($"/api/v1/medlink/departments/{d.Id}", d);
    }

    [HttpPut("departments/{id:guid}")]
    public async Task<IActionResult> UpdateDepartment(Guid id, [FromBody] OrgDepartment d)
    {
        var x = await _db.Departments.FirstOrDefaultAsync(z => z.Id == id);
        if (x == null) return NotFound();
        x.Name = d.Name; x.Code = d.Code; x.DepartmentType = d.DepartmentType; x.LegalEntityId = d.LegalEntityId == Guid.Empty ? x.LegalEntityId : d.LegalEntityId; x.Caption = d.Caption ?? d.Name; Touch(x, d.ModifiedBy);
        await _db.SaveChangesAsync();
        return Ok(x);
    }

    [HttpDelete("departments/{id:guid}")]
    public async Task<IActionResult> DeleteDepartment(Guid id)
    {
        var x = await _db.Departments.FirstOrDefaultAsync(z => z.Id == id);
        if (x == null) return NotFound();
        x.RecordState = 4; Touch(x, null); await _db.SaveChangesAsync();
        return Ok(new { deleted = true, soft = true });
    }

    // ---------------------------------------------------------------- employees
    [HttpGet("employees")]
    public async Task<IActionResult> Employees([FromQuery] Guid? legalEntityId, [FromQuery] Guid? departmentId, [FromQuery] string? q, [FromQuery] bool includeDeleted = false, [FromQuery] int take = 500)
    {
        var query = _db.Employees.AsNoTracking().Where(e => includeDeleted || e.RecordState == 2);
        if (legalEntityId.HasValue) query = query.Where(e => e.LegalEntityId == legalEntityId);
        if (departmentId.HasValue) query = query.Where(e => e.DepartmentId == departmentId);
        if (!string.IsNullOrEmpty(q)) query = query.Where(e => e.FullName.Contains(q) || e.PositionName.Contains(q) || e.PositionCode == q.ToUpper());
        var list = await query.OrderBy(e => e.FullName).Take(Math.Clamp(take, 1, 5000)).ToListAsync();
        var depts = await _db.Departments.AsNoTracking().ToDictionaryAsync(d => d.Id, d => d.Name);
        var enc = await _db.Encounters.AsNoTracking().Where(e => e.RecordState == 2).GroupBy(e => e.EmployeeId).Select(g => new { g.Key, c = g.Count(), rejected = g.Count(x => x.Status == "Rejected" || x.CodingCorrected) }).ToDictionaryAsync(x => x.Key ?? Guid.Empty, x => x);
        return Ok(list.Select(e => new { employee = e, departmentName = e.DepartmentId != null ? depts.GetValueOrDefault(e.DepartmentId.Value) : null, encounters = enc.GetValueOrDefault(e.Id)?.c ?? 0, corrected = enc.GetValueOrDefault(e.Id)?.rejected ?? 0 }));
    }

    [HttpGet("employees/{id:guid}")]
    public async Task<IActionResult> Employee(Guid id)
    {
        var e = await _db.Employees.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        if (e == null) return NotFound();
        var dept = e.DepartmentId != null ? await _db.Departments.AsNoTracking().FirstOrDefaultAsync(d => d.Id == e.DepartmentId) : null;
        var encounters = await _db.Encounters.AsNoTracking().Where(x => x.EmployeeId == id && x.RecordState == 2).OrderByDescending(x => x.DateStart).Take(50).ToListAsync();
        var discrepancies = await _db.Discrepancies.AsNoTracking().Where(d => d.EmployeeId == id && d.RecordState == 2).OrderByDescending(d => d.LostAmount).Take(50).ToListAsync();
        var allowedServices = await _db.ServiceDoctorPositions.AsNoTracking().Where(p => p.PositionRequirements.Contains(e.PositionCode)).Take(50).ToListAsync();
        return Ok(new { employee = e, department = dept, encounters, discrepancies, allowedServicesSample = allowedServices, stats = new { encounters = await _db.Encounters.CountAsync(x => x.EmployeeId == id && x.RecordState == 2), lost = discrepancies.Sum(d => d.LostAmount) } });
    }

    [HttpPost("employees")]
    public async Task<IActionResult> CreateEmployee([FromBody] OrgEmployee e)
    {
        if (string.IsNullOrWhiteSpace(e.FullName) && string.IsNullOrWhiteSpace(e.LastName)) return BadRequest(new { error = "FullName або LastName обов'язкові" });
        e.Id = Guid.NewGuid(); e.CreatedOn = DateTime.UtcNow; e.RecordState = 2;
        if (string.IsNullOrWhiteSpace(e.FullName)) e.FullName = $"{e.LastName} {e.FirstName} {e.SecondName}".Trim();
        if (string.IsNullOrWhiteSpace(e.PositionCode)) e.PositionCode = MedLinkDemoDataService.PositionCodeFor(e.PositionName);
        e.Caption ??= $"{e.FullName} ({e.PositionName})";
        _db.Employees.Add(e); await _db.SaveChangesAsync();
        return Created($"/api/v1/medlink/employees/{e.Id}", e);
    }

    [HttpPut("employees/{id:guid}")]
    public async Task<IActionResult> UpdateEmployee(Guid id, [FromBody] OrgEmployee e)
    {
        var x = await _db.Employees.FirstOrDefaultAsync(z => z.Id == id);
        if (x == null) return NotFound();
        x.LastName = e.LastName; x.FirstName = e.FirstName; x.SecondName = e.SecondName; x.FullName = string.IsNullOrWhiteSpace(e.FullName) ? $"{e.LastName} {e.FirstName} {e.SecondName}".Trim() : e.FullName;
        x.PositionCode = string.IsNullOrWhiteSpace(e.PositionCode) ? MedLinkDemoDataService.PositionCodeFor(e.PositionName) : e.PositionCode; x.PositionName = e.PositionName; x.DepartmentId = e.DepartmentId; x.IsActive = e.IsActive; x.EhealthEmployeeId = e.EhealthEmployeeId;
        if (e.LegalEntityId != Guid.Empty) x.LegalEntityId = e.LegalEntityId;
        x.Caption = $"{x.FullName} ({x.PositionName})"; Touch(x, e.ModifiedBy);
        await _db.SaveChangesAsync();
        return Ok(x);
    }

    [HttpDelete("employees/{id:guid}")]
    public async Task<IActionResult> DeleteEmployee(Guid id)
    {
        var x = await _db.Employees.FirstOrDefaultAsync(z => z.Id == id);
        if (x == null) return NotFound();
        x.RecordState = 4; x.IsActive = false; Touch(x, null); await _db.SaveChangesAsync();
        return Ok(new { deleted = true, soft = true });
    }

    // ---------------------------------------------------------------- patients
    [HttpGet("patients")]
    public async Task<IActionResult> Patients([FromQuery] Guid? legalEntityId, [FromQuery] string? q, [FromQuery] int page = 1, [FromQuery] int pageSize = 50, [FromQuery] bool includeDeleted = false)
    {
        var query = _db.Patients.AsNoTracking().Where(p => includeDeleted || p.RecordState == 2);
        if (legalEntityId.HasValue) query = query.Where(p => p.LegalEntityId == legalEntityId);
        if (!string.IsNullOrEmpty(q)) query = query.Where(p => p.FullName.Contains(q) || (p.EhealthPatientHash != null && p.EhealthPatientHash.StartsWith(q.ToUpper())) || (p.Rnokpp != null && p.Rnokpp.StartsWith(q)));
        var total = await query.CountAsync();
        var items = await query.OrderBy(p => p.FullName).Skip((page - 1) * pageSize).Take(Math.Clamp(pageSize, 1, 500)).ToListAsync();
        return Ok(new { total, page, pageSize, items });
    }

    [HttpGet("patients/{id:guid}")]
    public async Task<IActionResult> Patient(Guid id)
    {
        var p = await _db.Patients.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        if (p == null) return NotFound();
        var encounters = await _db.Encounters.AsNoTracking().Where(e => e.PatientId == id && e.RecordState == 2).OrderByDescending(e => e.DateStart).ToListAsync();
        var nszu = p.EhealthPatientHash != null ? await _db.StatementPatients.AsNoTracking().Where(s => s.PatientIdHash == p.EhealthPatientHash).ToListAsync() : new();
        return Ok(new { patient = p, encounters, nszuPatientRows = nszu });
    }

    [HttpPost("patients")]
    public async Task<IActionResult> CreatePatient([FromBody] MisPatientCard p)
    {
        if (string.IsNullOrWhiteSpace(p.FullName)) return BadRequest(new { error = "FullName обов'язковий" });
        p.Id = Guid.NewGuid(); p.CreatedOn = DateTime.UtcNow; p.RecordState = 2; p.Caption ??= p.FullName;
        _db.Patients.Add(p); await _db.SaveChangesAsync();
        return Created($"/api/v1/medlink/patients/{p.Id}", p);
    }

    [HttpPut("patients/{id:guid}")]
    public async Task<IActionResult> UpdatePatient(Guid id, [FromBody] MisPatientCard p)
    {
        var x = await _db.Patients.FirstOrDefaultAsync(z => z.Id == id);
        if (x == null) return NotFound();
        x.FullName = p.FullName; x.Rnokpp = p.Rnokpp; x.BirthDate = p.BirthDate; x.Gender = p.Gender; x.HasDeclaration = p.HasDeclaration; x.EhealthPatientHash = p.EhealthPatientHash ?? x.EhealthPatientHash; x.EhealthPatientId = p.EhealthPatientId; x.Caption = p.FullName; Touch(x, p.ModifiedBy);
        if (p.LegalEntityId != Guid.Empty) x.LegalEntityId = p.LegalEntityId;
        await _db.SaveChangesAsync();
        return Ok(x);
    }

    [HttpDelete("patients/{id:guid}")]
    public async Task<IActionResult> DeletePatient(Guid id)
    {
        var x = await _db.Patients.FirstOrDefaultAsync(z => z.Id == id);
        if (x == null) return NotFound();
        x.RecordState = 4; Touch(x, null); await _db.SaveChangesAsync();
        return Ok(new { deleted = true, soft = true });
    }

    // ---------------------------------------------------------------- encounters (ЕМЗ)
    [HttpGet("encounters")]
    public async Task<IActionResult> Encounters([FromQuery] Guid? legalEntityId, [FromQuery] Guid? employeeId, [FromQuery] Guid? patientId, [FromQuery] Guid? departmentId, [FromQuery] string? status, [FromQuery] string? package, [FromQuery] string? q, [FromQuery] bool? corrected, [FromQuery] DateTime? from, [FromQuery] DateTime? to, [FromQuery] int page = 1, [FromQuery] int pageSize = 50, [FromQuery] bool includeDeleted = false)
    {
        var query = _db.Encounters.AsNoTracking().Where(e => includeDeleted || e.RecordState == 2);
        if (legalEntityId.HasValue) query = query.Where(e => e.LegalEntityId == legalEntityId);
        if (employeeId.HasValue) query = query.Where(e => e.EmployeeId == employeeId);
        if (patientId.HasValue) query = query.Where(e => e.PatientId == patientId);
        if (departmentId.HasValue) query = query.Where(e => e.DepartmentId == departmentId);
        if (!string.IsNullOrEmpty(status) && status != "all") query = query.Where(e => e.Status == status);
        if (!string.IsNullOrEmpty(package)) query = query.Where(e => e.PackageNumber == package);
        if (corrected.HasValue) query = query.Where(e => e.CodingCorrected == corrected);
        if (from.HasValue) query = query.Where(e => e.DateStart >= from);
        if (to.HasValue) query = query.Where(e => e.DateStart <= to);
        if (!string.IsNullOrEmpty(q)) query = query.Where(e => (e.PrimaryIcd10Code != null && e.PrimaryIcd10Code.StartsWith(q.ToUpper())) || (e.Caption != null && e.Caption.Contains(q)) || (e.EhealthId != null && e.EhealthId.ToString()!.StartsWith(q.ToLower())));
        var total = await query.CountAsync();
        var items = await query.OrderByDescending(e => e.DateStart).Skip((page - 1) * pageSize).Take(Math.Clamp(pageSize, 1, 500)).ToListAsync();
        var empIds = items.Where(i => i.EmployeeId != null).Select(i => i.EmployeeId!.Value).Distinct().ToList();
        var emps = await _db.Employees.AsNoTracking().Where(e => empIds.Contains(e.Id)).ToDictionaryAsync(e => e.Id, e => new { e.FullName, e.PositionName, e.PositionCode });
        var patIds = items.Where(i => i.PatientId != null).Select(i => i.PatientId!.Value).Distinct().ToList();
        var pats = await _db.Patients.AsNoTracking().Where(p => patIds.Contains(p.Id)).ToDictionaryAsync(p => p.Id, p => p.FullName);
        var byStatus = await _db.Encounters.AsNoTracking().Where(e => e.RecordState == 2 && (!legalEntityId.HasValue || e.LegalEntityId == legalEntityId)).GroupBy(e => e.Status).Select(g => new { status = g.Key, count = g.Count() }).ToListAsync();
        return Ok(new
        {
            total, page, pageSize, byStatus,
            items = items.Select(e => new { encounter = e, employee = e.EmployeeId != null ? emps.GetValueOrDefault(e.EmployeeId.Value) : null, patientName = e.PatientId != null ? pats.GetValueOrDefault(e.PatientId.Value) : null, allowedTransitions = Workflows.Encounter.GetValueOrDefault(e.Status) ?? Array.Empty<string>() }),
        });
    }

    [HttpGet("encounters/{id:guid}")]
    public async Task<IActionResult> Encounter(Guid id)
    {
        var e = await _db.Encounters.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        if (e == null) return NotFound();
        var emp = e.EmployeeId != null ? await _db.Employees.AsNoTracking().FirstOrDefaultAsync(x => x.Id == e.EmployeeId) : null;
        var pat = e.PatientId != null ? await _db.Patients.AsNoTracking().FirstOrDefaultAsync(x => x.Id == e.PatientId) : null;
        var dept = e.DepartmentId != null ? await _db.Departments.AsNoTracking().FirstOrDefaultAsync(x => x.Id == e.DepartmentId) : null;
        var lines = e.EhealthId != null ? await _db.StatementLines.AsNoTracking().Where(l => l.EncounterEhealthId == e.EhealthId).Select(l => new { l.Id, l.StatementId, l.IncludedInReport, l.MisAmount, l.LostRevenue, l.ErrorComment, l.DsgCode, l.MatchStatus }).ToListAsync() : null;
        var disc = await _db.Discrepancies.AsNoTracking().Where(d => d.EncounterId == id).ToListAsync();
        var analyses = await _db.AnalysisResults.AsNoTracking().Where(a => a.EncounterId == id).OrderByDescending(a => a.AnalyzedAt).Take(10).ToListAsync();
        var queue = await _db.ResyncQueue.AsNoTracking().Where(q => q.EncounterId == id).OrderByDescending(q => q.CreatedOn).ToListAsync();
        return Ok(new { encounter = e, employee = emp, patient = pat, department = dept, nszuLines = lines, discrepancies = disc, analysisResults = analyses, resyncQueue = queue, allowedTransitions = Workflows.Encounter.GetValueOrDefault(e.Status) ?? Array.Empty<string>() });
    }

    /// <summary>Створення ЕМЗ (картка лікаря). Статус за замовчуванням Draft; services — масив кодів АКПІ</summary>
    [HttpPost("encounters")]
    public async Task<IActionResult> CreateEncounter([FromBody] EncounterDto dto, CancellationToken ct)
    {
        if (dto.LegalEntityId == Guid.Empty) return BadRequest(new { error = "LegalEntityId обов'язковий" });
        var e = new MisEncounter { Id = Guid.NewGuid(), LegalEntityId = dto.LegalEntityId, Status = "Draft", IsSigned = false, EhealthId = dto.EhealthId ?? Guid.NewGuid() };
        Apply(e, dto);
        _db.Encounters.Add(e); await _db.SaveChangesAsync(ct);
        var preb = dto.RunPrebilling ? await _prebilling.EvaluateAsync(new PrebillingRequest { EncounterId = e.Id, OrganizationId = e.LegalEntityId, Persist = true }, ct) : null;
        return Created($"/api/v1/medlink/encounters/{e.Id}", new { encounter = e, prebilling = preb });
    }

    [HttpPut("encounters/{id:guid}")]
    public async Task<IActionResult> UpdateEncounter(Guid id, [FromBody] EncounterDto dto, CancellationToken ct)
    {
        var e = await _db.Encounters.FirstOrDefaultAsync(z => z.Id == id, ct);
        if (e == null) return NotFound();
        if (e.Status is "Submitted" or "Accepted" or "Resubmitted" && !dto.Force) return Conflict(new { error = $"ЕМЗ у статусі {e.Status} редагується лише через коригування (status → Corrected) або з force=true" });
        Apply(e, dto); Touch(e, dto.UserId);
        if (e.Status is "Submitted" or "Accepted" or "Rejected") { e.Status = "Corrected"; e.CodingCorrected = true; e.CorrectedAt = DateTime.UtcNow; }
        await _db.SaveChangesAsync(ct);
        var preb = dto.RunPrebilling ? await _prebilling.EvaluateAsync(new PrebillingRequest { EncounterId = e.Id, OrganizationId = e.LegalEntityId, Persist = true }, ct) : null;
        return Ok(new { encounter = e, prebilling = preb });
    }

    private static void Apply(MisEncounter e, EncounterDto dto)
    {
        if (dto.LegalEntityId != Guid.Empty) e.LegalEntityId = dto.LegalEntityId;
        e.PatientId = dto.PatientId ?? e.PatientId; e.EmployeeId = dto.EmployeeId ?? e.EmployeeId; e.DepartmentId = dto.DepartmentId ?? e.DepartmentId; e.EpisodeId = dto.EpisodeId ?? e.EpisodeId;
        if (dto.EmzType != null) e.EmzType = dto.EmzType;
        e.EncounterClass = dto.EncounterClass ?? e.EncounterClass; e.EncounterType = dto.EncounterType ?? e.EncounterType; e.Priority = dto.Priority ?? e.Priority;
        e.DateStart = dto.DateStart ?? e.DateStart; e.DateEnd = dto.DateEnd ?? e.DateEnd;
        if (e.DateStart.HasValue && e.DateEnd.HasValue) e.LengthOfStayDays = Math.Max(1, (int)Math.Ceiling((e.DateEnd.Value - e.DateStart.Value).TotalDays));
        if (dto.PrimaryIcd10Code != null) e.PrimaryIcd10Code = PmgTariffCalculatorService.NormalizeIcd(dto.PrimaryIcd10Code);
        e.PrimaryIcd10Name = dto.PrimaryIcd10Name ?? e.PrimaryIcd10Name;
        if (dto.SecondaryIcd10Codes != null) e.SecondaryDiagnosesJson = JsonSerializer.Serialize(dto.SecondaryIcd10Codes);
        if (dto.Services != null) e.InterventionsJson = JsonSerializer.Serialize(dto.Services.Select(s => s.Trim()).Where(s => s.Length > 0).Distinct().ToList());
        e.PackageNumber = dto.PackageNumber ?? e.PackageNumber; e.ServiceNumber = dto.ServiceNumber ?? e.ServiceNumber; e.PatientAge = dto.PatientAge ?? e.PatientAge; e.PatientGender = dto.PatientGender ?? e.PatientGender;
        e.Caption = $"{e.EmzType} {e.PrimaryIcd10Code} {e.DateStart:yyyy-MM-dd}";
    }

    /// <summary>Перехід статусу ЕМЗ за життєвим циклом (Signed = накладено КЕП, Submitted = відправлено в ЕСОЗ, …)</summary>
    [HttpPost("encounters/{id:guid}/status")]
    public async Task<IActionResult> EncounterStatus(Guid id, [FromBody] StatusChange body, CancellationToken ct)
    {
        var e = await _db.Encounters.FirstOrDefaultAsync(z => z.Id == id, ct);
        if (e == null) return NotFound();
        if (body.Status == "Deleted") { e.RecordState = 4; Touch(e, body.UserId); await _db.SaveChangesAsync(ct); return Ok(new { e.Id, status = "Deleted" }); }
        if (!Workflows.CanTransition(Workflows.Encounter, e.Status, body.Status)) return BadRequest(new { error = $"Перехід {e.Status} → {body.Status} не дозволено", allowed = Workflows.Encounter.GetValueOrDefault(e.Status) });
        object? preb = null;
        if (body.Status == "Signed")
        {
            var r = await _prebilling.EvaluateAsync(new PrebillingRequest { EncounterId = e.Id, OrganizationId = e.LegalEntityId, Persist = true }, ct);
            preb = r;
            if (!r.IsValid && body.Note != "force") return BadRequest(new { error = "Anti-Defektura: підписання заблоковано — ризик відхилення НСЗУ", prebilling = r, hint = "Виправте знахідки або надішліть note=\"force\" для підписання під відповідальність лікаря" });
            e.IsSigned = true; e.SignedAt = DateTime.UtcNow;
        }
        if (body.Status == "Draft") { e.IsSigned = false; e.SignedAt = null; }
        if (body.Status == "Corrected") { e.CodingCorrected = true; e.CorrectedAt = DateTime.UtcNow; e.CorrectionNote = body.Note; }
        if (body.Status == "Resubmitted" && !await _db.ResyncQueue.AnyAsync(q => q.EncounterId == e.Id && q.Status == "Queued", ct))
            _db.ResyncQueue.Add(new EheResyncQueue { EncounterId = e.Id, Reason = body.Note ?? "Повторна відправка ЕМЗ в ЕСОЗ", Caption = $"Resync {e.EhealthId}" });
        e.Status = body.Status; Touch(e, body.UserId);
        await _db.SaveChangesAsync(ct);
        return Ok(new { e.Id, e.Status, e.IsSigned, allowed = Workflows.Encounter.GetValueOrDefault(e.Status), prebilling = preb });
    }

    [HttpDelete("encounters/{id:guid}")]
    public async Task<IActionResult> DeleteEncounter(Guid id, [FromQuery] bool hard = false)
    {
        var e = await _db.Encounters.FirstOrDefaultAsync(z => z.Id == id);
        if (e == null) return NotFound();
        if (hard) { _db.Encounters.Remove(e); await _db.ResyncQueue.Where(q => q.EncounterId == id).ExecuteDeleteAsync(); }
        else { e.RecordState = 4; Touch(e, null); }
        await _db.SaveChangesAsync();
        return Ok(new { deleted = true, soft = !hard });
    }

    /// <summary>Пре-білінг для збереженого ЕМЗ (віджет у картці лікаря)</summary>
    [HttpPost("encounters/{id:guid}/prebilling")]
    public async Task<IActionResult> EncounterPrebilling(Guid id, [FromQuery] string? doctorPosition, [FromQuery] bool isMountain = false, CancellationToken ct = default)
    {
        if (!await _db.Encounters.AnyAsync(e => e.Id == id, ct)) return NotFound();
        return Ok(await _prebilling.EvaluateAsync(new PrebillingRequest { EncounterId = id, DoctorPosition = doctorPosition, IsMountain = isMountain, Persist = true }, ct));
    }
}

public class EncounterDto
{
    public Guid LegalEntityId { get; set; }
    public Guid? EhealthId { get; set; }
    public Guid? PatientId { get; set; }
    public Guid? EmployeeId { get; set; }
    public Guid? DepartmentId { get; set; }
    public Guid? EpisodeId { get; set; }
    public string? EmzType { get; set; }
    public string? EncounterClass { get; set; }
    public string? EncounterType { get; set; }
    public string? Priority { get; set; }
    public DateTime? DateStart { get; set; }
    public DateTime? DateEnd { get; set; }
    public string? PrimaryIcd10Code { get; set; }
    public string? PrimaryIcd10Name { get; set; }
    public List<string>? SecondaryIcd10Codes { get; set; }
    public List<string>? Services { get; set; }
    public string? PackageNumber { get; set; }
    public string? ServiceNumber { get; set; }
    public int? PatientAge { get; set; }
    public string? PatientGender { get; set; }
    public bool RunPrebilling { get; set; } = true;
    public bool Force { get; set; }
    public Guid? UserId { get; set; }
}
