using System.Data.Common;
using System.Diagnostics;
using System.Text.Json;
using MedLink.Pmg.Module.Models;
using Microsoft.EntityFrameworkCore;

namespace MedLink.Pmg.Module.Data;

/// <summary>
/// Первинне наповнення бази довідниками ПМГ-2026 з каталогу seed/*.json (побудованого tools/build_seed.py).
/// Ідемпотентний: кожен довідник заповнюється лише якщо таблиця порожня.
/// Працює через DbCommand, тому однаково придатний для SQLite та PostgreSQL (Npgsql).
/// </summary>
public class DatabaseSeeder
{
    private readonly PmgDbContext _db;
    private readonly ILogger<DatabaseSeeder> _log;
    private readonly string _seedPath;
    private static readonly JsonSerializerOptions JsonOpts = new() { PropertyNameCaseInsensitive = true };

    public DatabaseSeeder(PmgDbContext db, ILogger<DatabaseSeeder> log, IConfiguration cfg, IHostEnvironment env)
    {
        _db = db;
        _log = log;
        _seedPath = ResolvePath(env.ContentRootPath, cfg["Pmg:SeedPath"] ?? "../../seed");
    }

    public static string ResolvePath(string contentRoot, string configured)
    {
        if (Path.IsPathRooted(configured)) return configured;
        var candidate = Path.GetFullPath(Path.Combine(contentRoot, configured));
        if (Directory.Exists(candidate) || File.Exists(candidate)) return candidate;
        // walk up from content root to find a folder with the same leaf name (dotnet run from bin/…)
        var leaf = Path.GetFileName(configured.TrimEnd('/', '\\'));
        var dir = new DirectoryInfo(contentRoot);
        while (dir != null)
        {
            var probe = Path.Combine(dir.FullName, leaf);
            if (Directory.Exists(probe) || File.Exists(probe)) return probe;
            dir = dir.Parent;
        }
        return candidate;
    }

    public string SeedPath => _seedPath;

    public async Task SeedAsync(CancellationToken ct = default)
    {
        var sw = Stopwatch.StartNew();
        await _db.Database.EnsureCreatedAsync(ct);
        _log.LogInformation("Seed path: {Path}", _seedPath);
        if (!Directory.Exists(_seedPath))
        {
            _log.LogWarning("Seed folder not found — dictionaries will stay empty. Run: python tools/build_seed.py");
        }

        await SeedTariffSettingsAsync(ct);
        await SeedPackageTariffRulesAsync(ct);
        await SeedRuleConfigsAsync(ct);
        await SeedPackagesAsync(ct);
        await SeedDsgAsync(ct);
        await SeedCodeNamesAsync(ct);
        await SeedPackage9Async(ct);
        await SeedRehabAsync(ct);
        await SeedErrorsAsync(ct);
        await SeedDoctorPositionsAsync(ct);
        await SeedLabAsync(ct);
        await SeedRulesAsync(ct);
        await SeedServicesAsync(ct);
        _log.LogInformation("Seeding finished in {Ms} ms", sw.ElapsedMilliseconds);
    }

    private T? Load<T>(string file)
    {
        var path = Path.Combine(_seedPath, file);
        if (!File.Exists(path)) { _log.LogWarning("Seed file missing: {File}", path); return default; }
        using var fs = File.OpenRead(path);
        return JsonSerializer.Deserialize<T>(fs, JsonOpts);
    }

    private static string? J(JsonElement e, string name)
    {
        if (!e.TryGetProperty(name, out var v) || v.ValueKind == JsonValueKind.Null) return null;
        return v.ValueKind == JsonValueKind.String ? v.GetString() : v.GetRawText();
    }
    private static decimal D(JsonElement e, string name, decimal def = 0)
    {
        if (!e.TryGetProperty(name, out var v)) return def;
        return v.ValueKind switch
        {
            JsonValueKind.Number => v.GetDecimal(),
            JsonValueKind.String => decimal.TryParse(v.GetString()?.Replace(' ', ' ').Replace(" ", "").Replace(',', '.'), System.Globalization.NumberStyles.Any, System.Globalization.CultureInfo.InvariantCulture, out var d) ? d : def,
            _ => def
        };
    }
    private static int I(JsonElement e, string name, int def = 0) => (int)D(e, name, def);
    private static bool B(JsonElement e, string name)
    {
        if (!e.TryGetProperty(name, out var v)) return false;
        return v.ValueKind == JsonValueKind.True || (v.ValueKind == JsonValueKind.Number && v.GetInt32() != 0) || (v.ValueKind == JsonValueKind.String && v.GetString() == "True");
    }
    private static string[] Arr(JsonElement e, string name)
    {
        if (!e.TryGetProperty(name, out var v) || v.ValueKind != JsonValueKind.Array) return Array.Empty<string>();
        return v.EnumerateArray().Select(x => x.ValueKind == JsonValueKind.String ? x.GetString() ?? "" : x.GetRawText()).ToArray();
    }

    // ------------------------------------------------------------------ settings

    private async Task SeedTariffSettingsAsync(CancellationToken ct)
    {
        if (await _db.TariffSettings.AnyAsync(ct)) return;
        _db.TariffSettings.Add(new DsgTariffSetting
        {
            Id = Guid.Parse("a6410a01-0000-4000-8000-000000000001"),
            Caption = "Тарифи ПМГ-2026 (Постанова КМУ № 1808 від 31.12.2025)",
        });
        await _db.SaveChangesAsync(ct);
    }

    private async Task SeedPackageTariffRulesAsync(CancellationToken ct)
    {
        if (await _db.PackageTariffRules.AnyAsync(ct)) return;
        var src = "Постанова КМУ № 1808 (Додатки 1–2) + калібрування на звітах НСЗУ 2026";
        var rules = new List<DsgPackageTariffRule>
        {
            new() { PackageNumber = "3", Model = "DSG", AdultRate = 8735m, Note = "Хірургічні операції у стаціонарі: 8 735 ₴ × Wg(ДСГ) × 0.55 × K_план × K_гір × K_мульти", Source = src },
            new() { PackageNumber = "4", Model = "DSG", AdultRate = 8735m, Note = "Стаціонарна допомога без операцій: 8 735 ₴ × Wg(ДСГ) × 0.55 × K_план × K_гір", Source = src },
            new() { PackageNumber = "47", Model = "DSG", AdultRate = 8735m, Note = "Хірургія одного дня: 8 735 ₴ × Wg(ДСГ) × 0.60 × K_гір", Source = src },
            new() { PackageNumber = "9", Model = "CLASS", AdultRate = 155m, Note = "Амбулаторна допомога: 155 ₴ × K_класу (1..148) × K_гір", Source = src },
            new() { PackageNumber = "17", Model = "FIXED_AGE", AdultRate = 17865m, PerPatientPeriod = true, ChildRate = 90131m, ChildAgeLimit = 18, Note = "Хіміотерапевтичне лікування: ставка на пацієнта за місяць лікування (дорослі / діти до 18)", Source = src },
            new() { PackageNumber = "18", Model = "FIXED", AdultRate = 54089m, PerPatientPeriod = true, Note = "Радіологічне лікування: ставка за курс променевої терапії", Source = src },
            new() { PackageNumber = "38", Model = "FIXED", AdultRate = 54000m, PerPatientPeriod = true, Note = "Лікування та супровід пацієнтів з гематологічними та онкогематологічними захворюваннями: ставка за випадок", Source = src },
            new() { PackageNumber = "10", Model = "FIXED", AdultRate = 248.64m, Note = "Мамографія: за 1 дослідження", Source = src },
            new() { PackageNumber = "11", Model = "FIXED", AdultRate = 2394.20m, Note = "Гістероскопія: за 1 дослідження", Source = src },
            new() { PackageNumber = "12", Model = "FIXED", AdultRate = 912.72m, Note = "ЕГДС: за 1 дослідження", Source = src },
            new() { PackageNumber = "13", Model = "FIXED", AdultRate = 1149.96m, Note = "Колоноскопія: за 1 дослідження", Source = src },
            new() { PackageNumber = "14", Model = "FIXED", AdultRate = 976.95m, Note = "Цистоскопія: за 1 дослідження", Source = src },
            new() { PackageNumber = "15", Model = "FIXED", AdultRate = 1178.97m, Note = "Бронхоскопія: за 1 дослідження", Source = src },
            new() { PackageNumber = "23", Model = "FIXED", AdultRate = 8735m, PerPatientPeriod = true, Note = "Стаціонарна паліативна допомога: ставка за пролікований випадок", Source = src },
            new() { PackageNumber = "24", Model = "PER_WEEK", AdultRate = 1333.19m, PerPatientPeriod = true, Note = "Мобільна паліативна допомога: 1 333,19 ₴ за тиждень візитів (кількість тижнів з колонки 33)", Source = src },
            new() { PackageNumber = "25", Model = "FIXED", AdultRate = 8735m, PerPatientPeriod = true, Note = "Реабілітація немовлят: за курс", Source = src },
            new() { PackageNumber = "53", Model = "REHAB_CYCLE", AdultRate = 19776m, PerPatientPeriod = true, Note = "Стаціонарна реабілітація: 19 776 ₴ × K_АР (АР1 1.0 / АР2 0.7 / АР3 0.4 / АР4 0.5)", Source = src },
            new() { PackageNumber = "54", Model = "REHAB_CYCLE", AdultRate = 10820m, PerPatientPeriod = true, Note = "Амбулаторна реабілітація: 10 820 ₴ × K_АР", Source = src },
            new() { PackageNumber = "5", Model = "FIXED", AdultRate = 15636m, Note = "Гострий мозковий інсульт: за випадок", Source = src },
            new() { PackageNumber = "6", Model = "FIXED", AdultRate = 25261m, Note = "Гострий інфаркт міокарда: за випадок", Source = src },
            new() { PackageNumber = "7", Model = "FIXED", AdultRate = 15137m, Note = "Пологи: за випадок", Source = src },
            new() { PackageNumber = "8", Model = "FIXED", AdultRate = 8735m, Note = "Неонатальна допомога: за випадок за кодами послуг", Source = src },
            new() { PackageNumber = "16", Model = "FIXED", AdultRate = 2492m, Note = "Гемодіаліз: за сеанс", Source = src },
            new() { PackageNumber = "57", Model = "GLOBAL", AdultRate = 0m, Note = "Готовність та забезпечення надання допомоги населенню: глобальна ставка закладу (ЕМЗ обліковуються, вартість випадку не нараховується)", Source = src },
            new() { PackageNumber = "1", Model = "GLOBAL", AdultRate = 0m, Note = "Первинна допомога: капітаційна ставка (не розраховується за ЕМЗ)", Source = src },
            new() { PackageNumber = "2", Model = "GLOBAL", AdultRate = 0m, Note = "Екстрена допомога: глобальна ставка", Source = src },
        };
        foreach (var r in rules) r.Caption = $"Пакет {r.PackageNumber} — {r.Model}";
        _db.PackageTariffRules.AddRange(rules);
        await _db.SaveChangesAsync(ct);
    }

    private async Task SeedRuleConfigsAsync(CancellationToken ct)
    {
        if (await _db.RuleConfigs.AnyAsync(ct)) return;
        _db.RuleConfigs.AddRange(
            new DsgRuleConfig { RuleCode = "FR-01", Caption = "Перевірка унікальності ЕМЗ (ehealth_id)", PackageNumber = "ALL", Severity = 2, NormativeReference = "Порядок ведення Реєстру ЕМЗ (Наказ МОЗ № 587)" },
            new DsgRuleConfig { RuleCode = "FR-02", Caption = "Відповідність основного діагнозу переліку ДСГ пакету", PackageNumber = "3,4,47", Severity = 2, NormativeReference = "Постанова КМУ № 1808, Додаток 1" },
            new DsgRuleConfig { RuleCode = "FR-03", Caption = "Валідація кодів послуг за номенклатурою МОЗ (АКПІ)", PackageNumber = "ALL", Severity = 1, NormativeReference = "Наказ МОЗ України № 517" },
            new DsgRuleConfig { RuleCode = "FR-04", Caption = "Хірургічний пакет вимагає коду операції АКПІ", PackageNumber = "3,47", Severity = 2, NormativeReference = "Постанова КМУ № 1808, специфікація пакетів 3 та 47" },
            new DsgRuleConfig { RuleCode = "FR-05", Caption = "Посада лікаря відповідає вимогам послуги (Anti-Defektura, MedProfit)", PackageNumber = "ALL", Severity = 2, NormativeReference = "Умови закупівлі ПМГ-2026, вимоги до спеціалістів" },
            new DsgRuleConfig { RuleCode = "FR-06", Caption = "Вік / стать пацієнта відповідають клінічним нормам послуги", PackageNumber = "ALL", Severity = 1, NormativeReference = "Клінічні норми довідника послуг" },
            new DsgRuleConfig { RuleCode = "PK-01A", Caption = "Коефіцієнт короткотривалого перебування (≤ 3 доби)", PackageNumber = "4", Severity = 1, NormativeReference = "ПМГ-2026, умови для Пакету № 4" },
            new DsgRuleConfig { RuleCode = "PK-02", Caption = "Коефіцієнт планової госпіталізації 0.80", PackageNumber = "3,4", Severity = 0, NormativeReference = "Постанова КМУ № 1808, п. 'пріоритет звернення'" },
            new DsgRuleConfig { RuleCode = "PK-04", Caption = "Гірський коефіцієнт 1.25", PackageNumber = "ALL", Severity = 0, NormativeReference = "Закон України «Про статус гірських населених пунктів»" },
            new DsgRuleConfig { RuleCode = "PK-05", Caption = "Коефіцієнт мультихірургії 1.30", PackageNumber = "3,47", Severity = 0, NormativeReference = "Матриця комбінацій (реінженерія MedProfit/Delphi)" },
            new DsgRuleConfig { RuleCode = "PK-06", Caption = "Неонатальний коефіцієнт 1.54 (вік < 1 року)", PackageNumber = "3,4", Severity = 0, NormativeReference = "Постанова КМУ № 1808, Додаток 1" },
            new DsgRuleConfig { RuleCode = "PK-12", Caption = "Розрахунок за ваговим коефіцієнтом ДСГ", PackageNumber = "3,4,47", Severity = 0, NormativeReference = "Таблиця вагових коефіцієнтів ДСГ 2026" },
            new DsgRuleConfig { RuleCode = "RD-01", Caption = "Реабілітація: обов'язкове кодування функціональних обмежень (МКФ) та діагнозу першопричини", PackageNumber = "53,54", Severity = 2, NormativeReference = "Критерії CR_* Пакету 54" }
        );
        await _db.SaveChangesAsync(ct);
    }

    // ------------------------------------------------------------------ dictionaries

    private async Task SeedPackagesAsync(CancellationToken ct)
    {
        if (await _db.Packages.AnyAsync(ct)) return;
        var arr = Load<List<JsonElement>>("packages.json");
        if (arr == null) return;
        foreach (var p in arr)
        {
            _db.Packages.Add(new PmgPackage
            {
                PackageId = J(p, "id") ?? "",
                Code = J(p, "code") ?? "",
                Name = J(p, "name") ?? "",
                Category = J(p, "category") ?? "",
                PaymentModel = J(p, "payment_model"),
                BaseRate = D(p, "base_rate"),
                RatePeriod = J(p, "rate_period"),
                ChapterCmu = J(p, "chapter_cmu"),
                Formula = J(p, "formula"),
                Description = J(p, "description"),
                CoefficientsJson = J(p, "coefficients"),
                LawReferencesJson = J(p, "law_references"),
                EhealthValidationsJson = J(p, "ehealth_validations"),
                GroupFile = J(p, "group_file"),
            });
        }
        await _db.SaveChangesAsync(ct);
        _log.LogInformation("Seeded pmg_packages: {N}", arr.Count);
    }

    private async Task SeedDsgAsync(CancellationToken ct)
    {
        if (await _db.Dsg.AnyAsync(ct)) return;
        var rows = Load<List<JsonElement>>("dsg.json");
        if (rows == null) return;
        var catalog = Load<List<JsonElement>>("dsg_catalog.json") ?? new();
        var typeByCode = catalog.ToDictionary(c => J(c, "dsg_code") ?? "", c => J(c, "service_type"), StringComparer.OrdinalIgnoreCase);

        var dsgList = new List<PmgDsg>();
        int id = 0;
        foreach (var r in rows)
        {
            id++;
            var code = J(r, "code") ?? "";
            var d = new PmgDsg
            {
                Id = id,
                PackageNumber = J(r, "pkg") ?? "",
                DsgCode = code,
                Name = J(r, "name") ?? "",
                ServiceType = typeByCode.GetValueOrDefault(code),
                CoefficientText = J(r, "coefficient_text"),
                WeightCoef = D(r, "weight"),
                BaseRate = D(r, "base_rate", 8735m),
                GlobalRateShare = D(r, "share", 0.55m),
                FullTariff = D(r, "full_tariff"),
                ShareTariff = D(r, "share_tariff"),
                PlannedCoef = r.TryGetProperty("planned_coeff", out var pc) && pc.ValueKind == JsonValueKind.Number ? pc.GetDecimal() : null,
                AdditionalRequirements = J(r, "add_req"),
                AdditionalRequirementsCode = J(r, "add_req_code"),
                AdditionalRequirementsServicesJson = J(r, "add_req_services"),
                AdditionalRequirementsReferral = J(r, "add_req_referral"),
                RequiredPackages = string.Join(",", Arr(r, "req_pkg")),
                Episode = J(r, "episode"),
                DiagCount = Arr(r, "diags").Length,
                SvcCount = Arr(r, "services").Length,
                AgeNotesJson = J(r, "age_notes"),
            };
            dsgList.Add(d);
        }
        _db.Dsg.AddRange(dsgList);
        await _db.SaveChangesAsync(ct);

        // link tables — bulk via DbCommand inside one transaction
        var conn = _db.Database.GetDbConnection();
        if (conn.State != System.Data.ConnectionState.Open) await conn.OpenAsync(ct);
        await using var tx = await conn.BeginTransactionAsync(ct);
        await using var cmdD = conn.CreateCommand();
        cmdD.Transaction = tx;
        cmdD.CommandText = "INSERT OR IGNORE INTO pmg_dsg_diagnoses (package_number, dsg_id, dsg_code, diag_code) VALUES (@p, @i, @c, @d)";
        var pD = AddParams(cmdD, "@p", "@i", "@c", "@d");
        await using var cmdS = conn.CreateCommand();
        cmdS.Transaction = tx;
        cmdS.CommandText = "INSERT OR IGNORE INTO pmg_dsg_services (package_number, dsg_id, dsg_code, service_code) VALUES (@p, @i, @c, @s)";
        var pS = AddParams(cmdS, "@p", "@i", "@c", "@s");
        int nd = 0, ns = 0;
        id = 0;
        foreach (var r in rows)
        {
            id++;
            var pkg = J(r, "pkg") ?? ""; var code = J(r, "code") ?? "";
            foreach (var diag in Arr(r, "diags"))
            {
                pD[0].Value = pkg; pD[1].Value = id; pD[2].Value = code; pD[3].Value = diag;
                nd += await cmdD.ExecuteNonQueryAsync(ct);
            }
            foreach (var svc in Arr(r, "services"))
            {
                pS[0].Value = pkg; pS[1].Value = id; pS[2].Value = code; pS[3].Value = svc;
                ns += await cmdS.ExecuteNonQueryAsync(ct);
            }
        }
        await tx.CommitAsync(ct);
        _log.LogInformation("Seeded pmg_dsg: {N}, diagnoses links: {D}, service links: {S}", dsgList.Count, nd, ns);
    }

    private static DbParameter[] AddParams(DbCommand cmd, params string[] names)
    {
        var list = new List<DbParameter>();
        foreach (var n in names)
        {
            var p = cmd.CreateParameter(); p.ParameterName = n; cmd.Parameters.Add(p); list.Add(p);
        }
        return list.ToArray();
    }

    private async Task SeedCodeNamesAsync(CancellationToken ct)
    {
        if (!await _db.Icd10.AnyAsync(ct))
        {
            var icd = Load<Dictionary<string, string>>("icd10_names.json");
            if (icd != null)
            {
                await BulkPairsAsync("pmg_icd10", icd, ct);
                _log.LogInformation("Seeded pmg_icd10: {N}", icd.Count);
            }
        }
        if (!await _db.Achi.AnyAsync(ct))
        {
            var achi = Load<Dictionary<string, string>>("achi_names.json");
            if (achi != null)
            {
                await BulkPairsAsync("pmg_achi", achi, ct);
                _log.LogInformation("Seeded pmg_achi: {N}", achi.Count);
            }
        }
    }

    private async Task BulkPairsAsync(string table, Dictionary<string, string> pairs, CancellationToken ct)
    {
        var conn = _db.Database.GetDbConnection();
        if (conn.State != System.Data.ConnectionState.Open) await conn.OpenAsync(ct);
        await using var tx = await conn.BeginTransactionAsync(ct);
        await using var cmd = conn.CreateCommand();
        cmd.Transaction = tx;
        cmd.CommandText = $"INSERT OR IGNORE INTO {table} (code, name) VALUES (@c, @n)";
        var p = AddParams(cmd, "@c", "@n");
        foreach (var kv in pairs)
        {
            if (string.IsNullOrWhiteSpace(kv.Key)) continue;
            p[0].Value = kv.Key.Trim(); p[1].Value = kv.Value ?? "";
            await cmd.ExecuteNonQueryAsync(ct);
        }
        await tx.CommitAsync(ct);
    }

    private async Task SeedPackage9Async(CancellationToken ct)
    {
        if (await _db.Package9Classes.AnyAsync(ct)) return;
        var rows = Load<List<JsonElement>>("pkg9_classes.json");
        if (rows == null) return;
        foreach (var r in rows)
        {
            var id = I(r, "id");
            var cn = J(r, "class_number") ?? "";
            _db.Package9Classes.Add(new PmgPackage9Class
            {
                Id = id,
                ClassNumber = cn,
                ClassName = J(r, "class_name") ?? "",
                ServiceType = J(r, "service_type") ?? "",
                Coefficient = D(r, "coefficient"),
                Cost = D(r, "cost"),
                Note = J(r, "note"),
                AdditionalRequirementsCode = J(r, "add_req_code"),
                EpisodeJson = J(r, "episode"),
                DiagCount = Arr(r, "diags").Length,
                SvcCount = Arr(r, "services").Length,
                PositionsJson = J(r, "positions"),
            });
            foreach (var s in Arr(r, "services").Distinct())
                _db.Package9ClassServices.Add(new PmgPackage9ClassService { ClassId = id, ClassNumber = cn, ServiceCode = s });
            foreach (var d in Arr(r, "diags").Distinct())
                _db.Package9ClassDiagnoses.Add(new PmgPackage9ClassDiagnosis { ClassId = id, ClassNumber = cn, DiagCode = d });
            if (r.TryGetProperty("positions", out var pos) && pos.ValueKind == JsonValueKind.Array)
            {
                var seen = new HashSet<string>();
                foreach (var p in pos.EnumerateArray())
                {
                    var pc = J(p, "code") ?? ""; if (pc == "" || !seen.Add(pc)) continue;
                    _db.Package9ClassPositions.Add(new PmgPackage9ClassPosition { ClassId = id, ClassNumber = cn, PositionCode = pc, PositionName = J(p, "name") ?? "" });
                }
            }
        }
        await _db.SaveChangesAsync(ct);
        _db.ChangeTracker.Clear();
        _log.LogInformation("Seeded pmg_package9_classes: {N}", rows.Count);
    }

    private async Task SeedRehabAsync(CancellationToken ct)
    {
        if (await _db.RehabGroups.AnyAsync(ct)) return;
        var root = Load<JsonElement>("pkg54_rehab.json");
        if (root.ValueKind != JsonValueKind.Object) return;
        if (root.TryGetProperty("ar_groups", out var groups))
            foreach (var g in groups.EnumerateObject())
                _db.RehabGroups.Add(new PmgRehabGroup
                {
                    Code = g.Name, Coefficient = D(g.Value, "coeff", 1m), Requirements = J(g.Value, "requirements"), Episode = J(g.Value, "episode"),
                    Plan = J(g.Value, "plan"), Referral = J(g.Value, "referral"), Reports = J(g.Value, "reports"), Procedures = J(g.Value, "procedures"),
                    Duration = J(g.Value, "duration"), DurationShort = J(g.Value, "duration_short"),
                });
        if (root.TryGetProperty("cr_rules", out var rules))
            foreach (var r in rules.EnumerateObject())
                _db.RehabRules.Add(new PmgRehabRule { Code = r.Name, RuleGroup = J(r.Value, "group"), RuleText = J(r.Value, "rule"), ExamplesJson = J(r.Value, "examples") });
        int sid = 0;
        if (root.TryGetProperty("services", out var svcs))
            foreach (var s in svcs.EnumerateArray())
            {
                var interv = J(s, "intervention") ?? "";
                var code = interv.Split(' ', 2)[0];
                _db.RehabServices.Add(new PmgRehabService { Id = ++sid, Intervention = interv, ServiceCode = code, ArGroups = string.Join(",", Arr(s, "ar")), Specialist = J(s, "specialist"), ServiceType = J(s, "type") });
            }
        int did = 0;
        if (root.TryGetProperty("rows", out var rows))
            foreach (var r in rows.EnumerateArray())
                _db.RehabDiagnoses.Add(new PmgRehabDiagnosis
                {
                    Id = ++did, DiagCode = J(r, "code") ?? "", Name = J(r, "name"), ArGroups = string.Join(",", Arr(r, "ar")), CrCode = J(r, "cr_code"), CrGroup = J(r, "cr_group"),
                    IsMain = B(r, "is_main"), IsMainNote = J(r, "is_main_note"), DiagTypes = string.Join(",", Arr(r, "types")), ReferralPmd = B(r, "referral_pmd"), Marker = J(r, "marker"), Note = J(r, "note"),
                });
        await _db.SaveChangesAsync(ct);
        _db.ChangeTracker.Clear();
        _log.LogInformation("Seeded rehab: diagnoses {D}, services {S}", did, sid);
    }

    private async Task SeedErrorsAsync(CancellationToken ct)
    {
        if (await _db.ErrorDictionary.AnyAsync(ct)) return;
        var rows = Load<List<JsonElement>>("errors.json");
        if (rows == null) return;
        foreach (var r in rows)
        {
            var code = J(r, "error_code") ?? "";
            var fam = code.Contains('_') ? code[..code.LastIndexOf('_')] : code;
            var (category, pattern, recover) = ClassifyErrorFamily(code, fam);
            _db.ErrorDictionary.Add(new PmgNhsuErrorDictionary
            {
                Id = I(r, "id"), ErrorCode = code, Title = J(r, "title") ?? "", NormativeReference = J(r, "normative_reference"),
                Description = J(r, "description") ?? "", RemediationAdvice = J(r, "remediation_advice"), Severity = I(r, "severity", 2),
                Category = category, NszuCommentPattern = pattern, RecoverabilityPercent = recover,
            });
        }
        await _db.SaveChangesAsync(ct);
        _db.ChangeTracker.Clear();
        _log.LogInformation("Seeded pmg_nhsu_error_dictionary: {N}", rows.Count);
    }

    /// <summary>Категорія, шаблон коментаря НСЗУ (колонка 39) та відновлюваність для ключових кодів помилок</summary>
    private static (string category, string? pattern, decimal recover) ClassifyErrorFamily(string code, string family) => code switch
    {
        "ERR_MVTN_01" => ("Епізод / МВТН", "Взаємодія для МВТН", 85m),
        "ERR_NO_PKG_02" => ("Кодування пакету", "Не відповідає жодному пакету/послузі", 78m),
        "ERR_AGE_03" => ("Вік пацієнта", "вік", 40m),
        "ERR_DOC_SPEC_04" => ("Посада лікаря", "посад", 90m),
        "ERR_SURG_NO_OP_05" => ("Кодування АКПІ", "Відсутня інтервенція", 92m),
        "ERR_STAY_TOO_SHORT_06" => ("Тривалість лікування", "тривалість лікування", 60m),
        "ERR_PRIMARY_DIAG_07" => ("Основний діагноз", "Неоплачуваний тип епізоду для даного діагнозу", 70m),
        "ERR_REHAB_IND_08" => ("Реабілітація / МКФ", "реабілітац", 75m),
        "ERR_DUPLICATE_ENC_09" => ("Дублікат", "Дублікат", 0m),
        "ERR_REFERRAL_REQ_10" => ("Направлення", "направлення", 65m),
        "ERR_ONCO_HISTO_11" => ("Онкологія", "гістолог", 70m),
        "ERR_STROKE_TIME_12" => ("Інсульт", "інсульт", 20m),
        "ERR_HEMODIALYSIS_FREQ_13" => ("Діаліз", "діаліз", 30m),
        "ERR_PREBILLING_COEF_14" => ("Тарифікація", "коефіцієнт", 50m),
        "ERR_MED_DEVICE_CODE_15" => ("Медичні вироби", "медичн.*виріб", 80m),
        _ => (family switch
        {
            "ERR_SURG" => "Хірургія", "ERR_DIAG" => "Діагностика", "ERR_REHAB" => "Реабілітація / МКФ", "ERR_OUTPAT" => "Амбулаторія",
            "ERR_PALLIAT" => "Паліативна допомога", "ERR_NEONAT" => "Неонатологія", "ERR_PSYCH" => "Психіатрія", "ERR_COVID" => "Інфекційні",
            "ERR_STAFF" => "Персонал", "ERR_EQUIP" => "Обладнання", "ERR_ICU" => "Інтенсивна терапія", "ERR_FIN" => "Фінансові умови", _ => "Загальні"
        }, null, 50m)
    };

    private async Task SeedDoctorPositionsAsync(CancellationToken ct)
    {
        if (await _db.ServiceDoctorPositions.AnyAsync(ct)) return;
        var rows = Load<List<JsonElement>>("doctor_positions.json");
        if (rows == null) return;
        foreach (var r in rows)
            _db.ServiceDoctorPositions.Add(new PmgServiceDoctorPosition
            {
                Id = I(r, "id"), ServiceCode = J(r, "service_code") ?? "", ServiceName = J(r, "service_name") ?? "", ServiceType = J(r, "service_type"),
                ClassNumber = J(r, "class_number"), ClassName = J(r, "class_name"), MdcRequirements = J(r, "mdc_requirements"), PositionRequirements = J(r, "position_requirements") ?? "",
            });
        await _db.SaveChangesAsync(ct);
        _db.ChangeTracker.Clear();
        _log.LogInformation("Seeded pmg_service_doctor_positions: {N}", rows.Count);
    }

    private async Task SeedLabAsync(CancellationToken ct)
    {
        if (await _db.LaboratoryCatalog.AnyAsync(ct)) return;
        var rows = Load<List<JsonElement>>("lab_tests.json");
        if (rows == null) return;
        foreach (var r in rows)
            _db.LaboratoryCatalog.Add(new PmgLaboratoryCatalog { Id = I(r, "id"), TestCode = J(r, "test_code") ?? "", TestName = J(r, "test_name") ?? "", TestGroup = J(r, "test_group") ?? "" });
        await _db.SaveChangesAsync(ct);
        _db.ChangeTracker.Clear();
    }

    private async Task SeedRulesAsync(CancellationToken ct)
    {
        if (await _db.ClassificationRules.AnyAsync(ct)) return;
        var rows = Load<List<JsonElement>>("rules.json");
        if (rows == null) return;
        foreach (var r in rows)
            _db.ClassificationRules.Add(new PmgClassificationRule { Id = I(r, "id"), LegacyRuleId = I(r, "legacy_rule_id"), RuleType = J(r, "rule_type") ?? "", RuleCode = J(r, "rule_code"), RuleGroup = J(r, "rule_group"), RuleDataJson = J(r, "rule_data") ?? "{}" });
        await _db.SaveChangesAsync(ct);
        _db.ChangeTracker.Clear();
    }

    private async Task SeedServicesAsync(CancellationToken ct)
    {
        if (!await _db.ServiceGroups.AnyAsync(ct))
        {
            var rows = Load<List<JsonElement>>("service_groups.json") ?? new();
            foreach (var r in rows)
                _db.ServiceGroups.Add(new PmgServiceGroup { Id = J(r, "id") ?? "", Code = J(r, "code") ?? "", Name = J(r, "name") ?? "", ParentId = J(r, "parent_id"), Level = I(r, "level", 1), Description = J(r, "description") });
            await _db.SaveChangesAsync(ct);
        }
        if (!await _db.ServiceCatalog.AnyAsync(ct))
        {
            var rows = Load<List<JsonElement>>("service_catalog.json") ?? new();
            foreach (var r in rows)
                _db.ServiceCatalog.Add(new PmgServiceCatalog
                {
                    ServiceCode = J(r, "service_code") ?? "", Name = J(r, "name") ?? "", GroupId = J(r, "group_id"), GroupName = J(r, "group_name"), Category = J(r, "category") ?? "",
                    BaseNormTimeMinutes = I(r, "base_norm_time_minutes", 60), AnesthesiaRequired = I(r, "anesthesia_required"), MinStayDays = I(r, "min_stay_days"), MaxStayDays = I(r, "max_stay_days", 14),
                    AgeMin = I(r, "age_min"), AgeMax = I(r, "age_max", 120), GenderRestriction = J(r, "gender_restriction") ?? "ALL", PackageIds = J(r, "package_ids"), DsgCodes = J(r, "dsg_codes"),
                    BaseTariff = D(r, "base_tariff", 8735m), ClinicalNormNotes = J(r, "clinical_norm_notes"),
                });
            await _db.SaveChangesAsync(ct);
        }
        if (!await _db.ServiceCombinations.AnyAsync(ct))
        {
            var rows = Load<List<JsonElement>>("service_combinations.json") ?? new();
            foreach (var r in rows)
                _db.ServiceCombinations.Add(new PmgServiceCombination
                {
                    Id = J(r, "id") ?? Guid.NewGuid().ToString(), ServiceCode = J(r, "service_code") ?? "", CombinationName = J(r, "combination_name") ?? "",
                    CompatibleIcdCodesJson = J(r, "compatible_icd_codes"), MandatoryCompanionsJson = J(r, "mandatory_companions"), OptionalMultisurgCompanionsJson = J(r, "optional_multisurg_companions"),
                    IncompatibleServicesJson = J(r, "incompatible_services"), AllowedDoctorPositionsJson = J(r, "allowed_doctor_positions"), ProhibitedDoctorPositionsJson = J(r, "prohibited_doctor_positions"),
                    ExpectedPackageNumber = J(r, "expected_package_number"), ExpectedDsgCode = J(r, "expected_dsg_code"), WeightCoef = D(r, "weight_coef", 1m), CalculatedTariff = D(r, "calculated_tariff"),
                    CalculationFormula = J(r, "calculation_formula"), RuleCondition = J(r, "rule_condition"), IsLibraryStandard = I(r, "is_library_standard"),
                });
            await _db.SaveChangesAsync(ct);
        }
        _db.ChangeTracker.Clear();
    }
}
