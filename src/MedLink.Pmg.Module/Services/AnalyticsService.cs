using MedLink.Pmg.Module.Data;
using MedLink.Pmg.Module.Models;
using Microsoft.EntityFrameworkCore;

namespace MedLink.Pmg.Module.Services;

/// <summary>Аналітичні зрізи: аудит 45 колонок, звіт за лікарями/відділеннями (аналог аркуша «Звіт»), зведення помилок</summary>
public class AnalyticsService
{
    private readonly PmgDbContext _db;
    public AnalyticsService(PmgDbContext db) { _db = db; }

    public IQueryable<NszuStatementLine> AuditQuery(Guid statementId, string? status, string? package, string? search, string? errorCategory, int? matchStatus, string? doctor, string? emzType)
    {
        var q = _db.StatementLines.AsNoTracking().Where(l => l.StatementId == statementId);
        if (!string.IsNullOrEmpty(status) && status != "all")
        {
            var s = status switch { "accepted" => NszuInclusion.DirectPay, "gb" => NszuInclusion.GlobalBudget, "rejected" => NszuInclusion.Rejected, _ => status };
            q = q.Where(l => l.IncludedInReport == s);
        }
        if (!string.IsNullOrEmpty(package) && package != "all") q = q.Where(l => l.PackageNumber == package);
        if (!string.IsNullOrEmpty(errorCategory)) q = q.Where(l => l.ErrorCategory == errorCategory);
        if (matchStatus.HasValue) q = q.Where(l => l.MatchStatus == matchStatus);
        if (!string.IsNullOrEmpty(doctor)) q = q.Where(l => l.PractitionerName != null && l.PractitionerName.Contains(doctor));
        if (!string.IsNullOrEmpty(emzType)) q = q.Where(l => l.EmzType == emzType);
        if (!string.IsNullOrEmpty(search))
        {
            var s = search.Trim();
            var sIcd = s.Replace(".", "").ToUpperInvariant();
            q = q.Where(l => (l.PractitionerName != null && l.PractitionerName.Contains(s)) || (l.PrimaryDiagnosis != null && l.PrimaryDiagnosis.Contains(s)) ||
                             (l.PrimaryIcd10Code != null && l.PrimaryIcd10Code.Replace(".", "").ToUpper().StartsWith(sIcd)) || (l.Interventions != null && l.Interventions.Contains(s)) ||
                             (l.ErrorComment != null && l.ErrorComment.Contains(s)) || (l.DsgCode != null && l.DsgCode == s) || (l.PatientIdHash != null && l.PatientIdHash.StartsWith(s)) ||
                             (l.EncounterEhealthId != null && l.EncounterEhealthId.ToString()!.StartsWith(s.ToLower())));
        }
        return q;
    }

    public async Task<object> SummaryAsync(Guid statementId, CancellationToken ct)
    {
        var st = await _db.Statements.AsNoTracking().FirstOrDefaultAsync(s => s.Id == statementId, ct) ?? throw new KeyNotFoundException("Statement not found");
        var org = await _db.LegalEntities.AsNoTracking().FirstOrDefaultAsync(o => o.Id == st.OrganizationId, ct);
        var byPackage = await _db.StatementLines.AsNoTracking().Where(l => l.StatementId == statementId)
            .GroupBy(l => new { l.PackageNumber, l.PackageName })
            .Select(g => new
            {
                packageNumber = g.Key.PackageNumber ?? "-", packageName = g.Key.PackageName ?? "Не віднесено",
                total = g.Count(), directPay = g.Count(x => x.IncludedInReport == "Так"), globalBudget = g.Count(x => x.IncludedInReport == "ГБ"), rejected = g.Count(x => x.IncludedInReport == "Ні"),
                directPayAmount = g.Where(x => x.IncludedInReport == "Так").Sum(x => x.MisAmount ?? 0), globalBudgetAmount = g.Where(x => x.IncludedInReport == "ГБ").Sum(x => x.MisAmount ?? 0),
                lostAmount = g.Sum(x => x.LostRevenue), recoverable = g.Sum(x => x.RecoverableAmount),
            }).OrderByDescending(x => x.total).ToListAsync(ct);
        var byStatus = await _db.StatementLines.AsNoTracking().Where(l => l.StatementId == statementId).GroupBy(l => l.IncludedInReport)
            .Select(g => new { status = g.Key, count = g.Count(), amount = g.Sum(x => x.MisAmount ?? 0) }).ToListAsync(ct);
        var byMatch = await _db.StatementLines.AsNoTracking().Where(l => l.StatementId == statementId).GroupBy(l => l.MatchStatus)
            .Select(g => new { matchStatus = g.Key, name = "", count = g.Count(), amount = g.Sum(x => x.MisAmount ?? 0) }).ToListAsync(ct);
        var byEmzType = await _db.StatementLines.AsNoTracking().Where(l => l.StatementId == statementId).GroupBy(l => l.EmzType)
            .Select(g => new { emzType = g.Key, count = g.Count() }).ToListAsync(ct);
        var errors = await ErrorsSummaryAsync(statementId, ct);
        var discrepancies = await _db.Discrepancies.AsNoTracking().Where(d => d.StatementId == statementId).GroupBy(d => d.Status)
            .Select(g => new { status = g.Key, count = g.Count(), lost = g.Sum(x => x.LostAmount), recoverable = g.Sum(x => x.RecoverableAmount) }).ToListAsync(ct);
        return new
        {
            statement = st, organization = org,
            kpi = new
            {
                totalRecords = st.TotalRecords, directPayRecords = st.DirectPayRecords, globalBudgetRecords = st.GlobalBudgetRecords, rejectedRecords = st.RejectedRecords,
                directPayAmount = st.DirectPayAmount, globalBudgetAmount = st.GlobalBudgetAmount, totalAccruedAmount = st.DirectPayAmount + st.GlobalBudgetAmount,
                lostRevenue = st.LostRevenueAmount, recoverable = st.RecoverableAmount, recoveryRatePercent = st.LostRevenueAmount > 0 ? Math.Round(st.RecoverableAmount / st.LostRevenueAmount * 100, 1) : 0,
                rejectionRatePercent = st.TotalRecords > 0 ? Math.Round((decimal)st.RejectedRecords / st.TotalRecords * 100, 2) : 0,
                hiddenDefekturaCount = st.MissingInNhsuCount, hiddenDefekturaAmount = st.MissingInNhsuAmount, matchedPaid = st.MatchedPaidCount, missingInMis = st.MissingInMisCount,
            },
            byPackage, byStatus,
            byMatch = byMatch.Select(m => new { m.matchStatus, name = ((MatchStatus)m.matchStatus).ToString(), m.count, m.amount }),
            byEmzType, topErrors = errors, discrepancies,
        };
    }

    public async Task<List<object>> ErrorsSummaryAsync(Guid statementId, CancellationToken ct)
    {
        var rejected = await _db.StatementLines.AsNoTracking().Where(l => l.StatementId == statementId && l.IncludedInReport == "Ні").CountAsync(ct);
        var rows = await _db.StatementLines.AsNoTracking().Where(l => l.StatementId == statementId && l.IncludedInReport == "Ні")
            .GroupBy(l => new { l.ErrorComment, l.ErrorCode, l.ErrorCategory })
            .Select(g => new { errorText = g.Key.ErrorComment ?? "—", errorCode = g.Key.ErrorCode, category = g.Key.ErrorCategory, count = g.Count(), lostAmount = g.Sum(x => x.LostRevenue), recoverableAmount = g.Sum(x => x.RecoverableAmount) })
            .OrderByDescending(x => x.count).ToListAsync(ct);
        return rows.Select(r => (object)new { r.errorText, r.errorCode, r.category, r.count, sharePercent = rejected > 0 ? Math.Round((decimal)r.count / rejected * 100, 1) : 0, r.lostAmount, r.recoverableAmount }).ToList();
    }

    public async Task<object> DoctorsSummaryAsync(Guid statementId, CancellationToken ct)
    {
        var lines = await _db.StatementLines.AsNoTracking().Where(l => l.StatementId == statementId)
            .Select(l => new { l.PractitionerName, l.PractitionerPosition, l.MatchedEmployeeId, l.MatchedDepartmentId, l.IncludedInReport, l.MisAmount, l.LostRevenue, l.RecoverableAmount, l.PackageNumber })
            .ToListAsync(ct);
        var employees = await _db.Employees.AsNoTracking().ToDictionaryAsync(e => e.Id, e => e, ct);
        var departments = await _db.Departments.AsNoTracking().ToDictionaryAsync(d => d.Id, d => d, ct);
        var doctors = lines.GroupBy(l => new { l.PractitionerName, l.PractitionerPosition }).Select(g =>
        {
            var empId = g.Select(x => x.MatchedEmployeeId).FirstOrDefault(x => x != null);
            var deptId = g.Select(x => x.MatchedDepartmentId).FirstOrDefault(x => x != null);
            var rejected = g.Count(x => x.IncludedInReport == "Ні");
            return new
            {
                employeeId = empId, name = g.Key.PractitionerName ?? "—", position = g.Key.PractitionerPosition ?? "—",
                positionCode = empId != null && employees.TryGetValue(empId.Value, out var e) ? e.PositionCode : MedLinkDemoDataService.PositionCodeFor(g.Key.PractitionerPosition),
                departmentId = deptId, department = deptId != null && departments.TryGetValue(deptId.Value, out var d) ? d.Name : "—",
                totalCount = g.Count(), acceptedCount = g.Count(x => x.IncludedInReport == "Так"), globalBudgetCount = g.Count(x => x.IncludedInReport == "ГБ"), rejectedCount = rejected,
                errorRate = g.Count() > 0 ? Math.Round((decimal)rejected / g.Count() * 100, 2) : 0,
                generatedRevenue = Math.Round(g.Where(x => x.IncludedInReport != "Ні").Sum(x => x.MisAmount ?? 0), 2), lostRevenue = Math.Round(g.Sum(x => x.LostRevenue), 2), recoverable = Math.Round(g.Sum(x => x.RecoverableAmount), 2),
                packages = g.GroupBy(x => x.PackageNumber ?? "-").Select(p => new { package = p.Key, count = p.Count() }).OrderByDescending(p => p.count).ToList(),
                inMis = empId != null,
            };
        }).OrderByDescending(d => d.generatedRevenue).ToList();
        var byDept = doctors.GroupBy(d => d.department).Select(g => new
        {
            department = g.Key, doctors = g.Count(), totalCount = g.Sum(x => x.totalCount), rejectedCount = g.Sum(x => x.rejectedCount),
            generatedRevenue = g.Sum(x => x.generatedRevenue), lostRevenue = g.Sum(x => x.lostRevenue), recoverable = g.Sum(x => x.recoverable),
            errorRate = g.Sum(x => x.totalCount) > 0 ? Math.Round((decimal)g.Sum(x => x.rejectedCount) / g.Sum(x => x.totalCount) * 100, 2) : 0,
        }).OrderByDescending(d => d.generatedRevenue).ToList();
        var official = await _db.StatementReportRows.AsNoTracking().Where(r => r.StatementId == statementId).OrderBy(r => r.CreatedOn).ToListAsync(ct);
        return new { doctors, departments = byDept, officialReportRows = official };
    }
}
