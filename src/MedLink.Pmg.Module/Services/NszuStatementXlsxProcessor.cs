using System.Diagnostics;
using System.Globalization;
using System.Text.Json;
using System.Text.RegularExpressions;
using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Spreadsheet;
using MedLink.Pmg.Module.Data;
using MedLink.Pmg.Module.Models;
using Microsoft.EntityFrameworkCore;

namespace MedLink.Pmg.Module.Services;

public interface INszuStatementXlsxProcessor
{
    /// <summary>Потоковий (SAX) імпорт офіційного звіту НСЗУ: 4 аркуші, 45 колонок, тарифікація, класифікація помилок.</summary>
    Task<StatementImportResult> ProcessAsync(Stream xlsx, string fileName, long fileSize, Guid? organizationId, bool isMountain, Guid? importedBy, CancellationToken ct = default);
}

/// <summary>Легкий SAX-парсер аркушів XLSX: повертає рядки як масиви рядкових значень за індексом колонки</summary>
public static class XlsxSax
{
    public static List<string> LoadSharedStrings(WorkbookPart wb)
    {
        var list = new List<string>();
        var sst = wb.SharedStringTablePart;
        if (sst == null) return list;
        using var reader = OpenXmlReader.Create(sst);
        while (reader.Read())
        {
            if (reader.ElementType == typeof(SharedStringItem) && reader.IsStartElement)
            {
                var item = (SharedStringItem)reader.LoadCurrentElement()!;
                list.Add(item.InnerText);
            }
        }
        return list;
    }

    public static int ColumnIndex(string? cellRef)
    {
        if (string.IsNullOrEmpty(cellRef)) return -1;
        int idx = 0;
        foreach (var ch in cellRef)
        {
            if (ch >= 'A' && ch <= 'Z') idx = idx * 26 + (ch - 'A' + 1);
            else if (ch >= 'a' && ch <= 'z') idx = idx * 26 + (ch - 'a' + 1);
            else break;
        }
        return idx - 1;
    }

    public static WorksheetPart? FindSheet(WorkbookPart wb, params string[] names)
    {
        var sheets = wb.Workbook.Descendants<Sheet>().ToList();
        foreach (var n in names)
        {
            var s = sheets.FirstOrDefault(x => string.Equals(x.Name?.Value?.Trim(), n, StringComparison.OrdinalIgnoreCase));
            if (s?.Id?.Value != null) return (WorksheetPart)wb.GetPartById(s.Id.Value);
        }
        return null;
    }

    /// <summary>Ітерує рядки аркуша: (номер рядка, значення клітинок за індексом колонки)</summary>
    public static IEnumerable<(int rowIndex, string?[] cells)> Rows(WorksheetPart ws, List<string> shared, int maxCols = 64)
    {
        using var reader = OpenXmlReader.Create(ws);
        while (reader.Read())
        {
            if (reader.ElementType != typeof(Row) || !reader.IsStartElement) continue;
            var row = (Row)reader.LoadCurrentElement()!;
            int rowIndex = (int)(row.RowIndex?.Value ?? 0);
            var cells = new string?[maxCols];
            int autoCol = 0;
            foreach (var cell in row.Elements<Cell>())
            {
                int col = ColumnIndex(cell.CellReference?.Value);
                if (col < 0) col = autoCol;
                autoCol = col + 1;
                if (col >= maxCols) continue;
                cells[col] = CellText(cell, shared);
            }
            yield return (rowIndex, cells);
        }
    }

    private static string? CellText(Cell cell, List<string> shared)
    {
        if (cell.DataType?.Value == CellValues.SharedString)
        {
            var raw = cell.CellValue?.InnerText;
            return int.TryParse(raw, out var i) && i >= 0 && i < shared.Count ? shared[i] : raw;
        }
        if (cell.DataType?.Value == CellValues.InlineString)
            return cell.InlineString?.InnerText ?? cell.InnerText;
        if (cell.DataType?.Value == CellValues.Boolean)
            return cell.CellValue?.InnerText == "1" ? "Так" : "Ні";
        return cell.CellValue?.InnerText;
    }
}

public class NszuStatementXlsxProcessor : INszuStatementXlsxProcessor
{
    private readonly PmgDbContext _db;
    private readonly ITariffCatalogProvider _catalogProvider;
    private readonly IPmgTariffCalculatorService _calc;
    private readonly NszuErrorClassifier _classifier;
    private readonly ILogger<NszuStatementXlsxProcessor> _log;
    private static readonly JsonSerializerOptions JsonOpts = new() { Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping };

    public const int BatchSize = 500;

    public NszuStatementXlsxProcessor(PmgDbContext db, ITariffCatalogProvider catalogProvider, IPmgTariffCalculatorService calc, NszuErrorClassifier classifier, ILogger<NszuStatementXlsxProcessor> log)
    {
        _db = db; _catalogProvider = catalogProvider; _calc = calc; _classifier = classifier; _log = log;
    }

    public async Task<StatementImportResult> ProcessAsync(Stream xlsx, string fileName, long fileSize, Guid? organizationId, bool isMountain, Guid? importedBy, CancellationToken ct = default)
    {
        var total = Stopwatch.StartNew();
        var stages = new List<ProcessingStage>();
        var result = new StatementImportResult { FileName = fileName };
        var cat = await _catalogProvider.GetAsync(ct);

        // Stage 1 — validate format
        var sw = Stopwatch.StartNew();
        using var doc = SpreadsheetDocument.Open(xlsx, false);
        var wb = doc.WorkbookPart ?? throw new InvalidDataException("WorkbookPart відсутній — файл не є XLSX");
        var sheetNames = wb.Workbook.Descendants<Sheet>().Select(s => s.Name?.Value ?? "").ToList();
        var wsMain = XlsxSax.FindSheet(wb, "Розшифровка", "Деталізація послуг") ?? throw new InvalidDataException("Аркуш «Розшифровка» не знайдено. Аркуші у файлі: " + string.Join(", ", sheetNames));
        var wsPatients = XlsxSax.FindSheet(wb, "Пацієнти");
        var wsReport = XlsxSax.FindSheet(wb, "Звіт");
        var wsErrors = XlsxSax.FindSheet(wb, "Опис помилок");
        foreach (var missing in new[] { ("Пацієнти", wsPatients), ("Звіт", wsReport), ("Опис помилок", wsErrors) })
            if (missing.Item2 == null) result.Warnings.Add($"Аркуш «{missing.Item1}» відсутній — відповідний блок пропущено.");
        stages.Add(new ProcessingStage { Stage = 1, Name = "Підготовка та валідація формату (4 аркуші)", DurationMs = sw.ElapsedMilliseconds, Details = string.Join(", ", sheetNames) });

        // Stage 2 — shared strings
        sw.Restart();
        var shared = XlsxSax.LoadSharedStrings(wb);
        stages.Add(new ProcessingStage { Stage = 2, Name = "Потокове завантаження таблиці рядків (SharedStrings)", DurationMs = sw.ElapsedMilliseconds, Details = $"{shared.Count} унікальних рядків" });

        // Stage 3 — parse «Розшифровка»
        sw.Restart();
        var statement = new NszuStatement
        {
            FileName = fileName, FileSizeBytes = fileSize, ImportedBy = importedBy, Status = "Parsing",
            OrganizationId = organizationId ?? Guid.Empty,
        };
        var lines = new List<NszuStatementLine>();
        string?[]? header = null;
        int lineNo = 0;
        foreach (var (rowIndex, cells) in XlsxSax.Rows(wsMain, shared, 48))
        {
            ct.ThrowIfCancellationRequested();
            if (rowIndex == 1) { statement.OrganizationName = Clean(cells[0]) ?? ""; continue; }
            if (rowIndex == 2) { statement.Edrpou = Clean(cells[0]) ?? ""; continue; }
            if (header == null)
            {
                if (IsHeaderRow(cells)) { header = cells; continue; }
                continue;
            }
            if (cells.All(c => string.IsNullOrWhiteSpace(c))) continue;
            lineNo++;
            lines.Add(MapLine(cells, statement.Id, lineNo));
        }
        if (header == null) throw new InvalidDataException("Рядок заголовків (45 колонок, «Звітний рік» …) не знайдено на аркуші «Розшифровка»");
        stages.Add(new ProcessingStage { Stage = 3, Name = "SAX-парсинг аркуша «Розшифровка» (45 колонок)", DurationMs = sw.ElapsedMilliseconds, Details = $"{lines.Count} ЕМЗ" });

        // Organization
        var org = await ResolveOrganizationAsync(statement, organizationId, isMountain, ct);
        statement.OrganizationId = org.Id;
        statement.Caption = $"{org.ShortName} — {fileName}";
        var first = lines.FirstOrDefault(l => l.ReportYear.HasValue);
        statement.ReportYear = first?.ReportYear ?? DateTime.UtcNow.Year;
        statement.ReportMonth = first?.ReportMonth ?? DateTime.UtcNow.Month;
        statement.PeriodFrom = new DateTime(statement.ReportYear, statement.ReportMonth, 1);
        statement.PeriodTo = statement.PeriodFrom.AddMonths(1).AddSeconds(-1);

        // Stage 4 — tariffs & classification
        sw.Restart();
        var mountain = isMountain || org.IsMountain;
        var topErrors = new Dictionary<string, ErrorFrequency>();
        var pkgs = new Dictionary<string, PackageBreakdown>();
        foreach (var l in lines) TariffLine(l, cat, mountain);
        DistributePerPatientPeriod(lines, cat);
        foreach (var l in lines)
        {
            // aggregates
            var key = string.IsNullOrEmpty(l.PackageNumber) ? "-" : l.PackageNumber;
            if (!pkgs.TryGetValue(key, out var pb))
                pkgs[key] = pb = new PackageBreakdown { PackageNumber = key, PackageName = l.PackageName ?? "Не віднесено до пакету" };
            pb.Total++;
            switch (l.IncludedInReport)
            {
                case NszuInclusion.DirectPay: pb.DirectPay++; pb.DirectPayAmount += l.MisAmount ?? 0; statement.DirectPayRecords++; statement.DirectPayAmount += l.MisAmount ?? 0; break;
                case NszuInclusion.GlobalBudget: pb.GlobalBudget++; pb.GlobalBudgetAmount += l.MisAmount ?? 0; statement.GlobalBudgetRecords++; statement.GlobalBudgetAmount += l.MisAmount ?? 0; break;
                default:
                    pb.Rejected++; pb.LostAmount += l.LostRevenue; statement.RejectedRecords++; statement.LostRevenueAmount += l.LostRevenue; statement.RecoverableAmount += l.RecoverableAmount;
                    var text = string.IsNullOrWhiteSpace(l.ErrorComment) || l.ErrorComment == "-" ? "Відхилено без коментаря" : l.ErrorComment!;
                    if (!topErrors.TryGetValue(text, out var ef)) topErrors[text] = ef = new ErrorFrequency { ErrorText = text, ErrorCode = l.ErrorCode, Category = l.ErrorCategory };
                    ef.Count++; ef.LostAmount += l.LostRevenue; ef.RecoverableAmount += l.RecoverableAmount;
                    break;
            }
        }
        statement.TotalRecords = lines.Count;
        stages.Add(new ProcessingStage { Stage = 4, Name = "Тарифікація за Постановою № 1808 та класифікація помилок (186 кодів)", DurationMs = sw.ElapsedMilliseconds, Details = $"ДСГ/класи визначено для {lines.Count(l => l.MisAmount > 0)} ЕМЗ" });

        // Stage 5 — other sheets
        sw.Restart();
        var patients = wsPatients != null ? ParsePatients(wsPatients, shared, statement.Id) : new();
        var reportRows = wsReport != null ? ParseReport(wsReport, shared, statement, cat) : new();
        var errorDescs = wsErrors != null ? ParseErrorDescriptions(wsErrors, shared) : new();
        statement.PatientsRows = patients.Count; statement.ReportRows = reportRows.Count; statement.ErrorDescriptionsRows = errorDescs.Count;
        stages.Add(new ProcessingStage { Stage = 5, Name = "Аркуші «Пацієнти», «Звіт», «Опис помилок»", DurationMs = sw.ElapsedMilliseconds, Details = $"{patients.Count} пацієнт-рядків, {reportRows.Count} рядків звіту, {errorDescs.Count} описів помилок" });

        // Stage 6 — persist in batches
        sw.Restart();
        statement.Status = "Tariffed";
        statement.ParseDurationMs = total.ElapsedMilliseconds;
        _db.Statements.Add(statement);
        await _db.SaveChangesAsync(ct);
        await BulkInsertAsync(lines, ct);
        await BulkInsertAsync(patients, ct);
        await BulkInsertAsync(reportRows, ct);
        await UpsertErrorDescriptionsAsync(errorDescs, statement.Id, ct);
        stages.Add(new ProcessingStage { Stage = 6, Name = $"Транзакційний запис у БД пакетами по {BatchSize} рядків", DurationMs = sw.ElapsedMilliseconds });

        statement.ProcessingLogJson = JsonSerializer.Serialize(stages, JsonOpts);
        statement.ParseDurationMs = total.ElapsedMilliseconds;
        await _db.SaveChangesAsync(ct);

        result.StatementId = statement.Id;
        result.OrganizationName = statement.OrganizationName; result.Edrpou = statement.Edrpou;
        result.ReportYear = statement.ReportYear; result.ReportMonth = statement.ReportMonth;
        result.Status = statement.Status; result.ParseDurationMs = statement.ParseDurationMs;
        result.TotalRecords = statement.TotalRecords; result.DirectPayRecords = statement.DirectPayRecords; result.GlobalBudgetRecords = statement.GlobalBudgetRecords; result.RejectedRecords = statement.RejectedRecords;
        result.DirectPayAmountUah = Round2(statement.DirectPayAmount); result.GlobalBudgetAmountUah = Round2(statement.GlobalBudgetAmount);
        result.LostRevenueUah = Round2(statement.LostRevenueAmount); result.RecoverableRevenueUah = Round2(statement.RecoverableAmount);
        result.RecoveryRatePercent = statement.LostRevenueAmount > 0 ? Math.Round(statement.RecoverableAmount / statement.LostRevenueAmount * 100, 1) : 0;
        result.PatientsRows = patients.Count; result.ReportRows = reportRows.Count; result.ErrorDescriptionsRows = errorDescs.Count;
        result.ProcessingStages = stages;
        result.TopErrors = topErrors.Values.OrderByDescending(e => e.Count).Take(15).Select(e =>
        {
            e.SharePercent = statement.RejectedRecords > 0 ? Math.Round((decimal)e.Count / statement.RejectedRecords * 100, 1) : 0;
            e.LostAmount = Round2(e.LostAmount); e.RecoverableAmount = Round2(e.RecoverableAmount);
            return e;
        }).ToList();
        result.Packages = pkgs.Values.OrderByDescending(p => p.Total).Select(p => { p.DirectPayAmount = Round2(p.DirectPayAmount); p.GlobalBudgetAmount = Round2(p.GlobalBudgetAmount); p.LostAmount = Round2(p.LostAmount); return p; }).ToList();
        _log.LogInformation("Imported {File}: {N} lines in {Ms} ms (rejected {R}, lost {L})", fileName, lines.Count, total.ElapsedMilliseconds, statement.RejectedRecords, statement.LostRevenueAmount);
        return result;
    }

    // ------------------------------------------------------------------ line mapping

    private static bool IsHeaderRow(string?[] cells)
    {
        var a = Clean(cells[0]); var d = Clean(cells[3]);
        return a != null && a.StartsWith("Звітний рік", StringComparison.OrdinalIgnoreCase) && d != null && d.Contains("ЕМЗ", StringComparison.OrdinalIgnoreCase);
    }

    private NszuStatementLine MapLine(string?[] c, Guid statementId, int lineNo)
    {
        string? G(int col1) => Clean(c[col1 - 1]);
        var l = new NszuStatementLine
        {
            StatementId = statementId, LineNumber = lineNo,
            ReportYear = ToInt(G(1)), ReportMonth = ToInt(G(2)), EmzType = G(3), EncounterEhealthId = ToGuid(G(4)), EhealthInsertedAt = ToDate(G(5)),
            PractitionerPosition = G(6), PractitionerName = G(7), ServiceLocation = G(8), ReferralType = G(9), ReferralEdrpou = G(10), ReferralDocPosition = G(11),
            EpisodeId = ToGuid(G(12)), EpisodeType = G(13), EpisodeStart = ToDate(G(14)), PeriodStart = ToDate(G(15)), PeriodEnd = ToDate(G(16)), LengthOfStayDays = ToInt(G(17)),
            PrimaryDiagnosis = Trunc(G(18), 1000), PrimaryDiagConfStatus = G(19), PrimaryDiagClinStatus = G(20), SecondaryDiagnoses = G(21), RejectedDiagnoses = G(22), Interventions = G(23),
            InteractionClass = G(24), Priority = G(25), InteractionType = G(26), AdmissionReason = G(27), DischargeOutcome = G(28), PatientIdHash = G(29),
            HasDeclaration = G(30) == null || G(30) == "-" ? null : G(30) == "Так", PatientGender = G(31), PatientAge = ToInt(G(32)), AdditionalEmzInfo = G(33), AdsgCode = G(34),
            PackageName = G(35), ServiceNumber = G(36), IncludedInStats = G(37), IncludedInReport = G(38), ErrorComment = Trunc(G(39), 1000), CompletenessDetailsJson = G(40),
            VerificationDetails = G(41), GroupingConflictDetails = G(42), NszuReviewDetails = G(43), AdditionalRemarks = G(44), NszuReviewDate = ToDate(G(45)),
        };
        l.Caption = $"{l.EmzType} {l.EncounterEhealthId}";
        l.RawPayloadJson = JsonSerializer.Serialize(c.Take(45).Select(Clean).ToArray(), JsonOpts);
        l.PackageNumber = PmgTariffCalculatorService.NormalizePackage(l.PackageName);
        l.PrimaryIcd10Code = PmgTariffCalculatorService.ExtractIcd(l.PrimaryDiagnosis);
        var codes = PmgTariffCalculatorService.ExtractServiceCodes(l.Interventions);
        l.InterventionCodesJson = JsonSerializer.Serialize(codes, JsonOpts);
        if (string.IsNullOrEmpty(l.IncludedInReport)) l.IncludedInReport = "-";
        return l;
    }

    private void TariffLine(NszuStatementLine l, TariffCatalog cat, bool mountain)
    {
        var codes = string.IsNullOrEmpty(l.InterventionCodesJson) ? new List<string>() : JsonSerializer.Deserialize<List<string>>(l.InterventionCodesJson) ?? new();
        var req = new TariffRequest
        {
            PackageNumber = l.PackageNumber, AdsgCode = l.AdsgCode, PrimaryIcd10Code = l.PrimaryIcd10Code, ServiceCodes = codes, ServiceNumber = l.ServiceNumber,
            Priority = l.Priority, EmzType = l.EmzType, InteractionClass = l.InteractionClass, PatientAge = l.PatientAge, LengthOfStayDays = l.LengthOfStayDays, IsMountain = mountain,
            Weeks = ExtractWeeks(l.AdditionalEmzInfo), EstimatePotential = l.IncludedInReport == NszuInclusion.Rejected,
        };
        var calc = _calc.Calculate(req, cat);
        l.DsgCode = calc.DsgCode; l.DsgName = calc.DsgName; l.WeightCoef = calc.WeightCoef; l.TariffModel = calc.Model;
        l.MisAmount = calc.Tariff; l.NszuAmount = 0m; l.Difference = calc.Tariff;
        l.CalculationJson = JsonSerializer.Serialize(new { calc.Model, calc.Formula, calc.Steps, calc.Notes, calc.Resolved }, JsonOpts);
        if (l.IncludedInReport == NszuInclusion.Rejected)
        {
            l.LostRevenue = calc.Tariff;
            var cls = _classifier.Classify(l.ErrorComment);
            l.ErrorCode = string.IsNullOrEmpty(cls.ErrorCode) ? null : cls.ErrorCode;
            l.ErrorCategory = string.IsNullOrEmpty(cls.Category) ? null : cls.Category;
            var pct = cls.RecoverabilityPercent;
            if (l.ErrorCode != null && cat.ErrorsByCode.TryGetValue(l.ErrorCode, out var e) && pct == 0 && e.RecoverabilityPercent > 0 && cls.Action != "RemoveDuplicate") pct = e.RecoverabilityPercent;
            l.RecoverableAmount = Math.Round(calc.Tariff * pct / 100m, 2);
        }
    }

    /// <summary>Для пакетів зі ставкою «на пацієнта за період» (курс хіміотерапії, цикл реабілітації, тиждень паліативу)
    /// ставка нараховується один раз на (пацієнт, пакет) і розподіляється між ЕМЗ цього пацієнта, щоб суми не дублювались.</summary>
    private static void DistributePerPatientPeriod(List<NszuStatementLine> lines, TariffCatalog cat)
    {
        var perPeriod = cat.PackageRules.Values.Where(r => r.PerPatientPeriod).Select(r => r.PackageNumber).ToHashSet();
        foreach (var grp in lines.Where(l => l.PackageNumber != null && perPeriod.Contains(l.PackageNumber) && (l.MisAmount ?? 0) > 0)
                                 .GroupBy(l => (l.PatientIdHash ?? l.Id.ToString(), l.PackageNumber, l.IncludedInReport)))
        {
            var members = grp.ToList();
            if (members.Count <= 1) continue;
            var total = members.Max(m => m.MisAmount ?? 0);
            var share = Math.Round(total / members.Count, 2);
            foreach (var m in members)
            {
                m.MisAmount = share; m.Difference = share;
                if (m.IncludedInReport == NszuInclusion.Rejected) { var ratio = m.LostRevenue > 0 ? m.RecoverableAmount / m.LostRevenue : 0; m.LostRevenue = share; m.RecoverableAmount = Math.Round(share * ratio, 2); }
                m.CalculationJson = (m.CalculationJson ?? "{}").TrimEnd('}') + $",\"perPatientPeriod\":{{\"groupSize\":{members.Count},\"periodTariff\":{total.ToString(CultureInfo.InvariantCulture)},\"lineShare\":{share.ToString(CultureInfo.InvariantCulture)}}}}}";
            }
        }
    }

    private static int ExtractWeeks(string? info)
    {
        if (string.IsNullOrEmpty(info)) return 1;
        var m = Regex.Match(info, @"тижн[^\d]{0,40}(\d+)", RegexOptions.IgnoreCase);
        return m.Success && int.TryParse(m.Groups[1].Value, out var w) && w > 0 ? w : 1;
    }

    // ------------------------------------------------------------------ other sheets

    private List<NszuStatementPatient> ParsePatients(WorksheetPart ws, List<string> shared, Guid statementId)
    {
        var list = new List<NszuStatementPatient>();
        bool header = false;
        foreach (var (rowIndex, c) in XlsxSax.Rows(ws, shared, 12))
        {
            var a = Clean(c[0]);
            if (!header) { if (a != null && a.StartsWith("Звітний рік", StringComparison.OrdinalIgnoreCase)) header = true; continue; }
            if (c.All(string.IsNullOrWhiteSpace)) continue;
            var p = new NszuStatementPatient
            {
                StatementId = statementId, ReportYear = ToInt(a), ReportMonth = ToInt(Clean(c[1])), PatientIdHash = Clean(c[2]), PackageName = Clean(c[3]), ServiceNumber = Clean(c[4]),
                IncludedInStats = Clean(c[5]), ServiceStatus = Clean(c[6]), AdditionalInfo = Clean(c[7]), EmzListJson = Clean(c[8]),
            };
            p.PackageNumber = PmgTariffCalculatorService.NormalizePackage(p.PackageName);
            p.Caption = $"{p.PatientIdHash} / {p.PackageNumber}";
            list.Add(p);
        }
        return list;
    }

    private List<NszuStatementReportRow> ParseReport(WorksheetPart ws, List<string> shared, NszuStatement st, TariffCatalog cat)
    {
        var list = new List<NszuStatementReportRow>();
        string section = "Total"; string? doctor = null; string kind = "Package";
        foreach (var (rowIndex, c) in XlsxSax.Rows(ws, shared, 8))
        {
            var a = Clean(c[0]); var b = Clean(c[1]);
            if (a == null && b == null) continue;
            if (rowIndex <= 6)
            {
                foreach (var v in new[] { a, b })
                {
                    if (v == null) continue;
                    if (v.StartsWith("Дата час останього внесення", StringComparison.OrdinalIgnoreCase) || v.StartsWith("Дата час останнього внесення", StringComparison.OrdinalIgnoreCase)) st.LastEmzInsertedAt = After(v, ':');
                    else if (v.StartsWith("Остання дата перегляду", StringComparison.OrdinalIgnoreCase)) st.NszuLastReviewAt = After(v, ':');
                    else if (v.StartsWith("Дата та час формування", StringComparison.OrdinalIgnoreCase)) st.GeneratedAt = After(v, ':');
                    else if (v.StartsWith("Звітний період", StringComparison.OrdinalIgnoreCase))
                    {
                        var m = Regex.Match(v, @"з\s+(\d{4}-\d{2}-\d{2})\s+по\s+(\d{4}-\d{2}-\d{2})");
                        if (m.Success && DateTime.TryParse(m.Groups[1].Value, out var f) && DateTime.TryParse(m.Groups[2].Value, out var t)) { st.PeriodFrom = f; st.PeriodTo = t.AddDays(1).AddSeconds(-1); }
                    }
                    else if (v.StartsWith("КОМУНАЛЬНЕ", StringComparison.OrdinalIgnoreCase) || v.StartsWith("ТОВ", StringComparison.OrdinalIgnoreCase) || v.StartsWith("ПРИВАТНЕ", StringComparison.OrdinalIgnoreCase)) st.Caption ??= v;
                }
                continue;
            }
            if (a != null && a.StartsWith("В розрізі лікарів", StringComparison.OrdinalIgnoreCase)) { section = "Doctor"; doctor = null; continue; }
            if (a != null && a.StartsWith("Загальна статистика", StringComparison.OrdinalIgnoreCase)) { section = "Total"; kind = "Package"; continue; }
            if (a != null && a.StartsWith("Пакет послуг", StringComparison.OrdinalIgnoreCase)) { kind = "Package"; continue; }
            if (a != null && a.StartsWith("Статистика щодо виявлених помилок", StringComparison.OrdinalIgnoreCase)) { kind = "Error"; continue; }
            if (section == "Doctor" && b == null && a != null && !a.StartsWith("Всього") && !Regex.IsMatch(a, @"^\d")) { doctor = a; kind = "Package"; continue; }
            if (a == null) continue;
            var row = new NszuStatementReportRow
            {
                StatementId = st.Id, Section = section, DoctorName = section == "Doctor" ? doctor : null, RowKind = kind, RowCaption = a, IsTotalRow = a.StartsWith("Всього", StringComparison.OrdinalIgnoreCase),
                EmzCount = ToInt(b) ?? 0,
            };
            if (kind == "Package") { row.PatientCount = ToInt(Clean(c[2])); row.ServiceCount = ToInt(Clean(c[3])); row.PackageNumber = row.IsTotalRow ? null : PmgTariffCalculatorService.NormalizePackage(a); }
            else row.PercentOfTotal = ToDec(Clean(c[2]));
            row.Caption = $"{(doctor ?? "Загалом")} / {a}";
            list.Add(row);
        }
        return list;
    }

    private List<NszuErrorDescription> ParseErrorDescriptions(WorksheetPart ws, List<string> shared)
    {
        var list = new List<NszuErrorDescription>();
        string? section = null; bool header = false;
        foreach (var (rowIndex, c) in XlsxSax.Rows(ws, shared, 8))
        {
            var a = Clean(c[0]); var b = Clean(c[1]);
            if (!header) { if (a != null && a.StartsWith("Текст коментаря", StringComparison.OrdinalIgnoreCase)) header = true; continue; }
            if (a == null) continue;
            if (b == null) { section = a; continue; }
            var cls = _classifier.Classify(a);
            list.Add(new NszuErrorDescription { Section = section, CommentText = Trunc(a, 1000)!, Description = b, MappedErrorCode = string.IsNullOrEmpty(cls.ErrorCode) ? null : cls.ErrorCode, Caption = Trunc(a, 255) });
        }
        return list;
    }

    private async Task UpsertErrorDescriptionsAsync(List<NszuErrorDescription> descs, Guid statementId, CancellationToken ct)
    {
        if (descs.Count == 0) return;
        var existing = await _db.ErrorDescriptions.ToDictionaryAsync(e => e.CommentText, e => e, ct);
        foreach (var d in descs)
        {
            if (existing.TryGetValue(d.CommentText, out var e)) { e.Occurrences++; e.Description = d.Description; e.Section = d.Section; e.ModifiedOn = DateTime.UtcNow; }
            else { d.Occurrences = 1; d.FirstSeenStatementId = statementId; _db.ErrorDescriptions.Add(d); existing[d.CommentText] = d; }
        }
        await _db.SaveChangesAsync(ct);
        _db.ChangeTracker.Clear();
    }

    private async Task<OrgLegalEntity> ResolveOrganizationAsync(NszuStatement st, Guid? organizationId, bool isMountain, CancellationToken ct)
    {
        OrgLegalEntity? org = null;
        if (organizationId.HasValue && organizationId != Guid.Empty) org = await _db.LegalEntities.FirstOrDefaultAsync(o => o.Id == organizationId, ct);
        if (org == null && !string.IsNullOrEmpty(st.Edrpou)) org = await _db.LegalEntities.FirstOrDefaultAsync(o => o.Edrpou == st.Edrpou, ct);
        if (org == null)
        {
            org = new OrgLegalEntity { Edrpou = st.Edrpou, ShortName = string.IsNullOrEmpty(st.OrganizationName) ? $"ЗОЗ {st.Edrpou}" : st.OrganizationName, IsMountain = isMountain, Caption = st.OrganizationName };
            _db.LegalEntities.Add(org);
            await _db.SaveChangesAsync(ct);
        }
        else if (string.IsNullOrEmpty(org.ShortName) && !string.IsNullOrEmpty(st.OrganizationName)) { org.ShortName = st.OrganizationName; await _db.SaveChangesAsync(ct); }
        return org;
    }

    private async Task BulkInsertAsync<T>(List<T> items, CancellationToken ct) where T : class
    {
        if (items.Count == 0) return;
        _db.ChangeTracker.AutoDetectChangesEnabled = false;
        try
        {
            for (int i = 0; i < items.Count; i += BatchSize)
            {
                var batch = items.Skip(i).Take(BatchSize).ToList();
                await _db.Set<T>().AddRangeAsync(batch, ct);
                await _db.SaveChangesAsync(ct);
                _db.ChangeTracker.Clear();
            }
        }
        finally { _db.ChangeTracker.AutoDetectChangesEnabled = true; }
    }

    // ------------------------------------------------------------------ helpers

    public static string? Clean(string? v)
    {
        if (v == null) return null;
        var t = v.Trim();
        return t.Length == 0 ? null : t;
    }
    private static string? Trunc(string? v, int max) => v == null ? null : (v.Length <= max ? v : v[..max]);
    private static string After(string v, char ch) { var i = v.IndexOf(ch); return i < 0 ? v : v[(i + 1)..].Trim(); }
    private static int? ToInt(string? v)
    {
        if (string.IsNullOrEmpty(v) || v == "-") return null;
        if (int.TryParse(v, NumberStyles.Any, CultureInfo.InvariantCulture, out var i)) return i;
        if (double.TryParse(v, NumberStyles.Any, CultureInfo.InvariantCulture, out var d)) return (int)d;
        return null;
    }
    private static decimal? ToDec(string? v)
    {
        if (string.IsNullOrEmpty(v) || v == "-") return null;
        return decimal.TryParse(v.Replace(',', '.'), NumberStyles.Any, CultureInfo.InvariantCulture, out var d) ? d : null;
    }
    private static Guid? ToGuid(string? v) => Guid.TryParse(v, out var g) ? g : null;
    private static DateTime? ToDate(string? v)
    {
        if (string.IsNullOrEmpty(v) || v == "-") return null;
        if (DateTime.TryParse(v, CultureInfo.InvariantCulture, DateTimeStyles.AssumeLocal, out var d)) return DateTime.SpecifyKind(d, DateTimeKind.Unspecified);
        if (double.TryParse(v, NumberStyles.Any, CultureInfo.InvariantCulture, out var oa) && oa > 20000 && oa < 80000) return DateTime.FromOADate(oa);
        return null;
    }
    private static decimal Round2(decimal v) => Math.Round(v, 2);
}
