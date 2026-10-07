using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using MedLink.Pmg.Module.Data;
using MedLink.Pmg.Module.Models;
using Microsoft.EntityFrameworkCore;

namespace MedLink.Pmg.Module.Services;

/// <summary>
/// Емуляція ядра МІС «Медлінк» для автономного стенду: з рядків звіту НСЗУ формує
/// org_employee / org_department / mis_patient_card / mis_encounter так, ніби ці ЕМЗ
/// були створені лікарями у Медлінку та відправлені в ЕСОЗ. Детерміновано (за хешем ehealth_id):
///   • ~94 % ЕМЗ зі звіту існують у МІС (2-Way знайде їх за ehealth_id);
///   • ~6 % відсутні (внесено іншою МІС) → MissingInMis;
///   • додатково ~1 % «прихованої дефектури» — підписані ЕМЗ у МІС, яких немає у звіті → MissingInNhsu.
/// У бойовому evomis цей сервіс не потрібен — таблиці вже наповнені реальними записами.
/// </summary>
public class MedLinkDemoDataService
{
    private readonly PmgDbContext _db;
    private readonly ILogger<MedLinkDemoDataService> _log;
    public MedLinkDemoDataService(PmgDbContext db, ILogger<MedLinkDemoDataService> log) { _db = db; _log = log; }

    /// <summary>Мапа «назва посади (колонка 6)» → код посади ЕСОЗ (довідник POSITION)</summary>
    public static readonly Dictionary<string, string> PositionCodes = new(StringComparer.OrdinalIgnoreCase)
    {
        ["Лікар-педіатр"] = "P8", ["Лікар-терапевт"] = "P10", ["Лікар-акушер-гінеколог"] = "P34", ["Лікар-алерголог"] = "P35", ["Лікар-анестезіолог"] = "P37",
        ["Лікар-гастроентеролог"] = "P41", ["Лікар-гематолог"] = "P43", ["Лікар-гематолог дитячий"] = "P44", ["Лікар-генетик"] = "P45", ["Лікар-дерматовенеролог"] = "P53",
        ["Лікар-ендокринолог"] = "P56", ["Лікар-ендокринолог дитячий"] = "P57", ["Лікар-ендоскопіст"] = "P58", ["Лікар-імунолог"] = "P61", ["Лікар-інфекціоніст"] = "P64",
        ["Лікар-кардіолог"] = "P67", ["Лікар-лаборант"] = "P71", ["Лікар-невропатолог"] = "P85", ["Лікар-невролог дитячий"] = "P86", ["Лікар-нефролог"] = "P87",
        ["Лікар-нейрохірург"] = "P89", ["Лікар-онколог"] = "P91", ["Лікар-онколог дитячий"] = "P92", ["Лікар-ортопед-травматолог"] = "P93", ["Лікар-ортопед-травматолог дитячий"] = "P94",
        ["Лікар-отоларинголог"] = "P95", ["Лікар-отоларинголог дитячий"] = "P96", ["Лікар-офтальмолог"] = "P98", ["Лікар-офтальмолог дитячий"] = "P99", ["Лікар-патологоанатом"] = "P101",
        ["Лікар-педіатр-неонатолог"] = "P103", ["Лікар приймальної палати (відділення)"] = "P104", ["Лікар з променевої терапії"] = "P105", ["Лікар-психіатр"] = "P107",
        ["Лікар-психолог"] = "P113", ["Лікар-пульмонолог"] = "P116", ["Лікар-рентгенолог"] = "P122", ["Лікар-ревматолог"] = "P123", ["Лікар-уролог"] = "P150", ["Лікар-уролог дитячий"] = "P151",
        ["Лікар-фізіотерапевт"] = "P152", ["Лікар-фтизіатр"] = "P153", ["Лікар-хірург"] = "P157", ["Лікар-хірург дитячий"] = "P158", ["Лікар-хірург-онколог"] = "P159",
        ["Лікар-хірург судинний"] = "P160", ["Лікар-хірург серцево-судинний"] = "P161", ["Лікар-хірург торакальний"] = "P162", ["Лікар-хірург проктолог"] = "P163",
        ["Лікар фізичної та реабілітаційної медицини"] = "P164", ["Лікар-кардіолог дитячий"] = "P246", ["Лікар з радіаційної онкології"] = "P282", ["Лікар з ядерної медицини"] = "P283",
        ["Лікар з ультразвукової діагностики"] = "P149", ["Лікар-радіолог"] = "P121", ["Лікар загальної практики - сімейний лікар"] = "P9", ["Сестра медична"] = "P195", ["Фізичний терапевт"] = "P262",
        ["Ерготерапевт"] = "P263", ["Лікар-анестезіолог дитячий"] = "P38", ["Лікар-дієтолог"] = "P55", ["Лікар-гінеколог-онколог"] = "P48", ["Лікар-отоларинголог-онколог"] = "P97", ["Лікар-хірург щелепно-лицевий"] = "P270",
    };

    public static string PositionCodeFor(string? positionName)
    {
        if (string.IsNullOrWhiteSpace(positionName)) return "P0";
        if (PositionCodes.TryGetValue(positionName.Trim(), out var c)) return c;
        var key = PositionCodes.Keys.FirstOrDefault(k => positionName.Contains(k, StringComparison.OrdinalIgnoreCase));
        return key != null ? PositionCodes[key] : "P0";
    }

    public static string DepartmentFor(string? packageNumber, string? emzType, string? position)
    {
        return packageNumber switch
        {
            "3" or "4" or "47" => "Хірургічний стаціонар",
            "17" => "Відділення хіміотерапії",
            "18" => "Радіологічне відділення",
            "38" => "Гематологічне відділення",
            "23" or "24" => "Паліативне відділення",
            "9" => (position ?? "").Contains("лаборант", StringComparison.OrdinalIgnoreCase) ? "Клініко-діагностична лабораторія" : "Консультативно-діагностична поліклініка",
            "10" or "12" or "13" or "15" => "Відділення ендоскопії та променевої діагностики",
            "53" or "54" or "25" => "Відділення реабілітації",
            "57" => "Приймальне відділення",
            _ => emzType == "Діагностичний звіт" ? "Діагностичне відділення" : "Поліклінічне відділення",
        };
    }

    public static uint Hash(string s)
    {
        var bytes = MD5.HashData(Encoding.UTF8.GetBytes(s));
        return BitConverter.ToUInt32(bytes, 0);
    }

    public class DemoResult { public int Encounters { get; set; } public int Employees { get; set; } public int Departments { get; set; } public int Patients { get; set; } public int HiddenDefektura { get; set; } public int SkippedAsForeign { get; set; } }

    /// <summary>Генерує сутності МІС для звіту, якщо для закладу ще немає ЕМЗ за цей період</summary>
    public async Task<DemoResult> EnsureDemoEntitiesAsync(Guid statementId, CancellationToken ct = default)
    {
        var res = new DemoResult();
        var st = await _db.Statements.FirstOrDefaultAsync(s => s.Id == statementId, ct) ?? throw new KeyNotFoundException("Statement not found");
        var org = await _db.LegalEntities.FirstAsync(o => o.Id == st.OrganizationId, ct);
        var exists = await _db.Encounters.AnyAsync(e => e.LegalEntityId == org.Id && e.DateStart >= st.PeriodFrom && e.DateStart <= st.PeriodTo, ct);
        if (exists) { _log.LogInformation("Demo entities already exist for {Org} {Period}", org.ShortName, st.PeriodFrom); return res; }

        var lines = await _db.StatementLines.AsNoTracking().Where(l => l.StatementId == statementId).OrderBy(l => l.LineNumber).ToListAsync(ct);
        var departments = await _db.Departments.Where(d => d.LegalEntityId == org.Id).ToDictionaryAsync(d => d.Name, d => d, ct);
        var employees = await _db.Employees.Where(e => e.LegalEntityId == org.Id).ToDictionaryAsync(e => e.FullName + "|" + e.PositionName, e => e, ct);
        var patients = await _db.Patients.Where(p => p.LegalEntityId == org.Id && p.EhealthPatientHash != null).ToDictionaryAsync(p => p.EhealthPatientHash!, p => p, ct);
        var existingEh = new HashSet<Guid>(await _db.Encounters.Where(e => e.EhealthId != null).Select(e => e.EhealthId!.Value).ToListAsync(ct));

        OrgDepartment Dept(string name)
        {
            if (departments.TryGetValue(name, out var d)) return d;
            d = new OrgDepartment { LegalEntityId = org.Id, Name = name, Code = "D" + (departments.Count + 1).ToString("00"), Caption = name, DepartmentType = name.Contains("стаціонар", StringComparison.OrdinalIgnoreCase) ? "Inpatient" : "Outpatient" };
            departments[name] = d; _db.Departments.Add(d); res.Departments++;
            return d;
        }
        OrgEmployee Emp(string? fullName, string? position, OrgDepartment dept)
        {
            var name = string.IsNullOrWhiteSpace(fullName) ? "Невідомий лікар" : fullName.Trim();
            var pos = string.IsNullOrWhiteSpace(position) ? "Лікар" : position.Trim();
            var key = name + "|" + pos;
            if (employees.TryGetValue(key, out var e)) return e;
            var parts = name.Split(' ', StringSplitOptions.RemoveEmptyEntries);
            e = new OrgEmployee
            {
                LegalEntityId = org.Id, DepartmentId = dept.Id, FullName = name, LastName = parts.ElementAtOrDefault(0) ?? name, FirstName = parts.ElementAtOrDefault(1) ?? "", SecondName = parts.ElementAtOrDefault(2),
                PositionName = pos, PositionCode = PositionCodeFor(pos), Caption = $"{name} ({pos})", EhealthEmployeeId = Guid.NewGuid(),
            };
            employees[key] = e; _db.Employees.Add(e); res.Employees++;
            return e;
        }
        MisPatientCard Pat(NszuStatementLine l)
        {
            var hash = l.PatientIdHash ?? ("anon-" + l.LineNumber);
            if (patients.TryGetValue(hash, out var p)) return p;
            var birth = l.PatientAge.HasValue ? new DateTime(Math.Max(1900, (l.PeriodStart ?? st.PeriodFrom).Year - l.PatientAge.Value), 1, 1).AddDays((int)(Hash(hash) % 365)) : (DateTime?)null;
            p = new MisPatientCard
            {
                LegalEntityId = org.Id, EhealthPatientHash = hash, FullName = "Пацієнт " + hash[..Math.Min(8, hash.Length)], Gender = l.PatientGender, BirthDate = birth, HasDeclaration = l.HasDeclaration ?? false,
                Caption = "Пацієнт " + hash[..Math.Min(8, hash.Length)],
            };
            patients[hash] = p; _db.Patients.Add(p); res.Patients++;
            return p;
        }

        int n = 0;
        foreach (var l in lines)
        {
            if (l.EncounterEhealthId == null || existingEh.Contains(l.EncounterEhealthId.Value)) continue;
            var h = Hash(l.EncounterEhealthId.Value.ToString());
            if (h % 100 < 6) { res.SkippedAsForeign++; continue; } // ~6 % ЕМЗ внесено іншою МІС
            var dept = Dept(DepartmentFor(l.PackageNumber, l.EmzType, l.PractitionerPosition));
            var emp = Emp(l.PractitionerName, l.PractitionerPosition, dept);
            var pat = Pat(l);
            var enc = BuildEncounter(l, org.Id, dept.Id, emp.Id, pat.Id, l.EncounterEhealthId.Value);
            _db.Encounters.Add(enc);
            existingEh.Add(l.EncounterEhealthId.Value);
            res.Encounters++;
            // ~1 % прихованої дефектури: підписаний ЕМЗ у МІС, якого НСЗУ не побачила
            if (h % 100 >= 94 && h % 100 < 95 && (l.IncludedInReport == NszuInclusion.DirectPay || l.IncludedInReport == NszuInclusion.GlobalBudget) && (l.MisAmount ?? 0) > 0)
            {
                var ghostId = Guid.NewGuid();
                var ghost = BuildEncounter(l, org.Id, dept.Id, emp.Id, pat.Id, ghostId);
                ghost.DateStart = (l.PeriodStart ?? st.PeriodFrom).AddDays(1);
                ghost.DateEnd = ghost.DateStart?.AddHours(1);
                ghost.CorrectionNote = "Демо: ЕМЗ підписано та відправлено в ЕСОЗ, але відсутній у звіті НСЗУ (прихована дефектура)";
                _db.Encounters.Add(ghost);
                res.HiddenDefektura++;
            }
            if (++n % 500 == 0) { await _db.SaveChangesAsync(ct); }
        }
        await _db.SaveChangesAsync(ct);
        _db.ChangeTracker.Clear();
        _log.LogInformation("Demo MedLink entities for {Org}: {E} encounters, {Emp} employees, {D} departments, {P} patients, {H} hidden-defektura", org.ShortName, res.Encounters, res.Employees, res.Departments, res.Patients, res.HiddenDefektura);
        return res;
    }

    private static MisEncounter BuildEncounter(NszuStatementLine l, Guid orgId, Guid deptId, Guid empId, Guid patId, Guid ehealthId)
    {
        var secondary = PmgTariffCalculatorService.ExtractIcdList(l.SecondaryDiagnoses);
        return new MisEncounter
        {
            LegalEntityId = orgId, EhealthId = ehealthId, EpisodeId = l.EpisodeId, PatientId = patId, EmployeeId = empId, DepartmentId = deptId,
            EmzType = l.EmzType ?? "Взаємодія", EncounterClass = l.InteractionClass, EncounterType = l.InteractionType, Priority = l.Priority,
            DateStart = l.PeriodStart ?? l.EpisodeStart, DateEnd = l.PeriodEnd, LengthOfStayDays = l.LengthOfStayDays,
            PrimaryIcd10Code = string.IsNullOrEmpty(l.PrimaryIcd10Code) ? null : l.PrimaryIcd10Code, PrimaryIcd10Name = l.PrimaryDiagnosis,
            SecondaryDiagnosesJson = JsonSerializer.Serialize(secondary), InterventionsJson = l.InterventionCodesJson,
            PackageNumber = string.IsNullOrEmpty(l.PackageNumber) ? null : l.PackageNumber, ServiceNumber = l.ServiceNumber, PatientAge = l.PatientAge, PatientGender = l.PatientGender,
            Status = "Submitted", IsSigned = true, SignedAt = l.EhealthInsertedAt, Caption = $"{l.EmzType} {l.PrimaryIcd10Code} {l.PractitionerName}",
            CreatedOn = l.EhealthInsertedAt ?? DateTime.UtcNow,
        };
    }
}
