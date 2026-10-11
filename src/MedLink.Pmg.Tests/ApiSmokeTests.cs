using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

namespace MedLink.Pmg.Tests;

/// <summary>
/// Інтеграційні тести API на реальній SQLite-базі у тимчасовому каталозі: сідинг довідників,
/// імпорт реального звіту НСЗУ, 2-Way звірка, CRUD ЕМЗ та статусні переходи.
/// </summary>
public class ApiFixture : WebApplicationFactory<Program>, IAsyncLifetime
{
    public string TempDir { get; } = Path.Combine(Path.GetTempPath(), "pmg-tests-" + Guid.NewGuid().ToString("N")[..8]);
    public HttpClient Client { get; private set; } = null!;

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        Directory.CreateDirectory(TempDir);
        var root = FindRepoRoot();
        builder.UseSetting("ConnectionStrings:PmgSqlite", $"Data Source={Path.Combine(TempDir, "pmg-test.sqlite")}");
        builder.UseSetting("Pmg:SeedPath", Path.Combine(root, "seed"));
        builder.UseSetting("Pmg:SampleReportsPath", root);
        builder.UseSetting("Pmg:WebRootPath", Path.Combine(root, "src", "MedLink.Pmg.Web"));
        builder.UseSetting("Pmg:UploadsPath", Path.Combine(TempDir, "uploads"));
        builder.UseSetting("Pmg:ImportSampleReportsOnStartup", "false");
        builder.UseSetting("Urls", "http://127.0.0.1:0");
    }

    public static string FindRepoRoot()
    {
        var dir = new DirectoryInfo(AppContext.BaseDirectory);
        while (dir != null && !File.Exists(Path.Combine(dir.FullName, "CLAUDE.md"))) dir = dir.Parent;
        return dir?.FullName ?? throw new DirectoryNotFoundException("repo root (CLAUDE.md) not found");
    }

    public Task InitializeAsync() { Client = CreateClient(); return Task.CompletedTask; }
    public new async Task DisposeAsync() { await base.DisposeAsync(); try { Directory.Delete(TempDir, true); } catch { } }
}

[CollectionDefinition("api")] public class ApiCollection : ICollectionFixture<ApiFixture> { }

[Collection("api")]
public class ApiSmokeTests
{
    private readonly HttpClient _c;
    private static readonly JsonSerializerOptions J = new() { PropertyNameCaseInsensitive = true };
    public ApiSmokeTests(ApiFixture f) { _c = f.Client; }

    [Fact]
    public async Task Health_And_Dictionaries_Seeded()
    {
        var health = await _c.GetFromJsonAsync<JsonElement>("/api/v1/system/health");
        Assert.Equal("ok", health.GetProperty("status").GetString());
        var stats = await _c.GetFromJsonAsync<JsonElement>("/api/v1/pmg/dictionaries/stats");
        Assert.Equal(465, stats.GetProperty("dsg").GetInt32());
        Assert.Equal(148, stats.GetProperty("classes").GetInt32());
        Assert.Equal(186, stats.GetProperty("errors").GetInt32());
        Assert.True(stats.GetProperty("dsgDiagnoses").GetInt32() > 280000);
        var pkgs = await _c.GetFromJsonAsync<JsonElement>("/api/v1/pmg/dictionaries/packages");
        Assert.Equal(46, pkgs.GetArrayLength());
    }

    [Fact]
    public async Task Prebilling_Hemicolectomy_And_AntiDefektura()
    {
        var ok = await (await _c.PostAsJsonAsync("/api/v1/pmg/prebilling/evaluate", new { icdCode = "C18.0", services = new[] { "32003-00" }, doctorPosition = "P157", packageNumber = "3", priority = "Ургентний" })).Content.ReadFromJsonAsync<JsonElement>();
        Assert.True(ok.GetProperty("tariff").GetDecimal() > 0);
        Assert.NotEqual("REJECTED_DEFEKTURA", ok.GetProperty("status").GetString());
        var bad = await (await _c.PostAsJsonAsync("/api/v1/pmg/prebilling/evaluate", new { icdCode = "C18.0", services = new[] { "32003-00" }, doctorPosition = "P122", packageNumber = "3" })).Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal("REJECTED_DEFEKTURA", bad.GetProperty("status").GetString());
        Assert.Equal(0m, bad.GetProperty("tariff").GetDecimal());
    }

    [Fact]
    public async Task Import_RealReport_Reconcile_Correct_Workflow()
    {
        var resp = await _c.PostAsync("/api/v1/nszu/statements/process-sample?fileName=02000334_SF_2026_08_20260910.xlsx", null);
        Assert.Equal(HttpStatusCode.OK, resp.StatusCode);
        var body = await resp.Content.ReadFromJsonAsync<JsonElement>();
        var result = body.GetProperty("result");
        Assert.Equal(4394, result.GetProperty("totalRecords").GetInt32());
        Assert.Equal(146, result.GetProperty("rejectedRecords").GetInt32());
        var stId = result.GetProperty("statementId").GetGuid();

        var lines = await _c.GetFromJsonAsync<JsonElement>($"/api/v1/nszu/statements/{stId}/lines?status=rejected&pageSize=5");
        Assert.Equal(146, lines.GetProperty("total").GetInt32());
        Assert.Equal(45, lines.GetProperty("items")[0].GetProperty("rawPayloadJson").GetString()!.Split("\",\"").Length);

        var summary = await _c.GetFromJsonAsync<JsonElement>($"/api/v1/nszu/statements/{stId}/summary");
        Assert.True(summary.GetProperty("kpi").GetProperty("hiddenDefekturaCount").GetInt32() > 0);
        var doctors = await _c.GetFromJsonAsync<JsonElement>($"/api/v1/nszu/statements/{stId}/doctors-summary");
        Assert.True(doctors.GetProperty("doctors").GetArrayLength() > 10);

        // discrepancy with MIS encounter → apply correction → resync queue → statuses
        var disc = await _c.GetFromJsonAsync<JsonElement>($"/api/v1/pmg/analytics/discrepancies?statementId={stId}&type=Rejected&pageSize=50");
        var item = disc.GetProperty("items").EnumerateArray().First(i => i.GetProperty("discrepancy").GetProperty("encounterId").ValueKind == JsonValueKind.String);
        var discId = item.GetProperty("discrepancy").GetProperty("id").GetGuid();
        var corr = await (await _c.PostAsJsonAsync("/api/v1/pmg/analytics/apply-correction", new { discrepancyId = discId, acceptRecommendation = true, addServices = new[] { "30061-02" }, note = "test" })).Content.ReadFromJsonAsync<JsonElement>();
        Assert.True(corr.GetProperty("success").GetBoolean());
        var qId = corr.GetProperty("resyncQueueId").GetGuid();
        foreach (var st in new[] { "SignedKep", "Sent", "Accepted" })
        {
            var r = await _c.PostAsJsonAsync($"/api/v1/pmg/analytics/resync-queue/{qId}/status", new { status = st });
            Assert.Equal(HttpStatusCode.OK, r.StatusCode);
        }
        var d2 = await _c.GetFromJsonAsync<JsonElement>($"/api/v1/pmg/analytics/discrepancies/{discId}");
        Assert.Equal("Resubmitted", d2.GetProperty("discrepancy").GetProperty("status").GetString());
        var badTransition = await _c.PostAsJsonAsync($"/api/v1/pmg/analytics/discrepancies/{discId}/status", new { status = "New" });
        Assert.Equal(HttpStatusCode.BadRequest, badTransition.StatusCode);
    }

    [Fact]
    public async Task Encounter_Crud_And_Lifecycle()
    {
        var org = await (await _c.PostAsJsonAsync("/api/v1/medlink/legal-entities", new { edrpou = "00000001", shortName = "Тестова лікарня" })).Content.ReadFromJsonAsync<JsonElement>();
        var orgId = org.GetProperty("id").GetGuid();
        var dept = await (await _c.PostAsJsonAsync("/api/v1/medlink/departments", new { legalEntityId = orgId, name = "Хірургія" })).Content.ReadFromJsonAsync<JsonElement>();
        var emp = await (await _c.PostAsJsonAsync("/api/v1/medlink/employees", new { legalEntityId = orgId, departmentId = dept.GetProperty("id").GetGuid(), lastName = "Тест", firstName = "Лікар", positionName = "Лікар-хірург" })).Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal("P157", emp.GetProperty("positionCode").GetString());
        var pat = await (await _c.PostAsJsonAsync("/api/v1/medlink/patients", new { legalEntityId = orgId, fullName = "Пацієнт Тестовий", gender = "чоловіча" })).Content.ReadFromJsonAsync<JsonElement>();

        var enc = await (await _c.PostAsJsonAsync("/api/v1/medlink/encounters", new
        {
            legalEntityId = orgId, employeeId = emp.GetProperty("id").GetGuid(), patientId = pat.GetProperty("id").GetGuid(), primaryIcd10Code = "C18.0", services = new[] { "32003-00" },
            packageNumber = "3", priority = "Ургентний", patientAge = 62, dateStart = DateTime.UtcNow.AddDays(-5), dateEnd = DateTime.UtcNow,
        })).Content.ReadFromJsonAsync<JsonElement>();
        var encId = enc.GetProperty("encounter").GetProperty("id").GetGuid();
        Assert.Equal("Draft", enc.GetProperty("encounter").GetProperty("status").GetString());
        Assert.True(enc.GetProperty("prebilling").GetProperty("tariff").GetDecimal() > 0);

        foreach (var st in new[] { "Signed", "Submitted", "Rejected", "Corrected", "Resubmitted", "Accepted" })
        {
            var r = await _c.PostAsJsonAsync($"/api/v1/medlink/encounters/{encId}/status", new { status = st });
            Assert.True(r.IsSuccessStatusCode, $"{st}: {await r.Content.ReadAsStringAsync()}");
        }
        var upd = await _c.PutAsJsonAsync($"/api/v1/medlink/encounters/{encId}", new { legalEntityId = orgId, primaryIcd10Code = "C18.2", force = true });
        Assert.Equal(HttpStatusCode.OK, upd.StatusCode);
        var get = await _c.GetFromJsonAsync<JsonElement>($"/api/v1/medlink/encounters/{encId}");
        Assert.Equal("C18.2", get.GetProperty("encounter").GetProperty("primaryIcd10Code").GetString());
        Assert.True(get.GetProperty("resyncQueue").GetArrayLength() >= 1);
        var del = await _c.DeleteAsync($"/api/v1/medlink/encounters/{encId}");
        Assert.Equal(HttpStatusCode.OK, del.StatusCode);
        Assert.Equal(HttpStatusCode.OK, (await _c.DeleteAsync($"/api/v1/medlink/employees/{emp.GetProperty("id").GetGuid()}")).StatusCode);
    }

    [Fact]
    public async Task Combinations_Validate_And_Library()
    {
        var v = await (await _c.PostAsJsonAsync("/api/v1/pmg/combinations/validate", new { serviceCode = "32003-00", icdCode = "C18.0", doctorPosition = "P157", companionServices = new[] { "30075-01", "30394-00", "30440-00" }, admissionType = "Планова" })).Content.ReadFromJsonAsync<JsonElement>();
        Assert.True(v.GetProperty("isValid").GetBoolean());
        Assert.True(v.GetProperty("multisurgeryApplied").GetBoolean());
        var save = await _c.PostAsJsonAsync("/api/v1/pmg/combinations/library-save", new { name = "Еталон тест", serviceCode = "32003-00", icdCode = "C18.0", standardTariff = v.GetProperty("calculatedTariffUah").GetDecimal() });
        Assert.Equal(HttpStatusCode.OK, save.StatusCode);
        var lib = await _c.GetFromJsonAsync<JsonElement>("/api/v1/pmg/dictionaries/library");
        Assert.True(lib.GetArrayLength() >= 1);
    }

    [Fact]
    public async Task TariffSettings_Update_Reloads_Catalog()
    {
        var settings = await _c.GetFromJsonAsync<JsonElement>("/api/v1/pmg/dictionaries/tariff-settings");
        var s = settings[0];
        var id = s.GetProperty("id").GetGuid();
        var payload = JsonSerializer.Deserialize<Dictionary<string, object?>>(s.GetRawText())!;
        payload["mountainCoef"] = 1.25m;
        var r = await _c.PutAsJsonAsync($"/api/v1/pmg/dictionaries/tariff-settings/{id}", payload);
        Assert.Equal(HttpStatusCode.OK, r.StatusCode);
        var rules = await _c.GetFromJsonAsync<JsonElement>("/api/v1/pmg/dictionaries/package-rules");
        Assert.True(rules.GetArrayLength() >= 20);
    }
}
