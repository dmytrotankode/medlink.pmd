using System.Text.Json.Serialization;
using MedLink.Pmg.Module.Data;
using MedLink.Pmg.Module.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.FileProviders;

var builder = WebApplication.CreateBuilder(args);

// 1. Kestrel: порт 8085 (як у прототипі MedLink PMG), перевизначається через appsettings "Urls" або --urls
builder.Services.AddControllers().AddJsonOptions(o =>
{
    o.JsonSerializerOptions.DefaultIgnoreCondition = JsonIgnoreCondition.Never;
    o.JsonSerializerOptions.Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping;
    o.JsonSerializerOptions.ReferenceHandler = ReferenceHandler.IgnoreCycles;
});
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new Microsoft.OpenApi.Models.OpenApiInfo
    {
        Title = "MedLink PMG-2026 Analytics API (.NET 8)", Version = "v1",
        Description = "Модуль аналітики ПМГ-2026, ДСГ, аудиту звітів НСЗУ та 2-Way звірки з ЕМЗ МІС «Медлінк» (evomis). Автономний стенд: EF Core + SQLite, без авторизації.",
    });
    var xml = Path.Combine(AppContext.BaseDirectory, "MedLink.Pmg.Module.xml");
    if (File.Exists(xml)) c.IncludeXmlComments(xml);
});

// 2. SQLite (у evomis — PostgreSQL/Npgsql з тими самими мапінгами)
var cs = builder.Configuration.GetConnectionString("PmgSqlite") ?? "Data Source=App_Data/pmg_medlink.sqlite";
var dbFile = cs.Split(';').Select(p => p.Trim()).FirstOrDefault(p => p.StartsWith("Data Source=", StringComparison.OrdinalIgnoreCase))?["Data Source=".Length..];
if (!string.IsNullOrEmpty(dbFile) && !Path.IsPathRooted(dbFile))
{
    var full = Path.Combine(builder.Environment.ContentRootPath, dbFile);
    Directory.CreateDirectory(Path.GetDirectoryName(full)!);
    cs = cs.Replace(dbFile, full);
}
builder.Services.AddDbContext<PmgDbContext>(o => o.UseSqlite(cs));

// 3. Сервіси модуля
builder.Services.AddScoped<DatabaseSeeder>();
builder.Services.AddSingleton<ITariffCatalogProvider, TariffCatalogProvider>();
builder.Services.AddSingleton<IPmgTariffCalculatorService, PmgTariffCalculatorService>();
builder.Services.AddSingleton<NszuErrorClassifier>();
builder.Services.AddSingleton<RecommendationEngine>();
builder.Services.AddScoped<INszuStatementXlsxProcessor, NszuStatementXlsxProcessor>();
builder.Services.AddScoped<ReconciliationService>();
builder.Services.AddScoped<MedLinkDemoDataService>();
builder.Services.AddScoped<PrebillingService>();
builder.Services.AddScoped<CombinationService>();
builder.Services.AddScoped<CorrectionService>();
builder.Services.AddScoped<AnalyticsService>();

// 4. CORS для фронтенду Quasar
builder.Services.AddCors(o => o.AddPolicy("AllowAll", p => p.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader()));

var app = builder.Build();

// 5. Створення схеми та сідинг довідників при старті
using (var scope = app.Services.CreateScope())
{
    var seeder = scope.ServiceProvider.GetRequiredService<DatabaseSeeder>();
    await seeder.SeedAsync();
}

app.UseCors("AllowAll");
app.UseSwagger();
app.UseSwaggerUI(c => { c.SwaggerEndpoint("/swagger/v1/swagger.json", "MedLink PMG API v1"); c.RoutePrefix = "swagger"; });

// 6. Фронтенд (Quasar v1 / Vue 2 SPA) та документація проєкту як статичні файли
var webRoot = DatabaseSeeder.ResolvePath(app.Environment.ContentRootPath, app.Configuration["Pmg:WebRootPath"] ?? "../MedLink.Pmg.Web");
if (Directory.Exists(webRoot))
{
    var fp = new PhysicalFileProvider(webRoot);
    app.UseDefaultFiles(new DefaultFilesOptions { FileProvider = fp, RequestPath = "" });
    app.UseStaticFiles(new StaticFileOptions { FileProvider = fp, RequestPath = "", ServeUnknownFileTypes = true });
}
var docsRoot = DatabaseSeeder.ResolvePath(app.Environment.ContentRootPath, app.Configuration["Pmg:SampleReportsPath"] ?? "../..");
if (Directory.Exists(Path.Combine(docsRoot, "docs")))
    app.UseStaticFiles(new StaticFileOptions { FileProvider = new PhysicalFileProvider(Path.Combine(docsRoot, "docs")), RequestPath = "/docs", ServeUnknownFileTypes = true });

app.MapControllers();
app.MapGet("/api", () => Results.Redirect("/swagger"));

// 7. Автоімпорт вбудованих реальних звітів НСЗУ при першому старті (фоново)
if (app.Configuration.GetValue("Pmg:ImportSampleReportsOnStartup", false))
{
    _ = Task.Run(async () =>
    {
        await Task.Delay(500);
        using var scope = app.Services.CreateScope();
        var log = scope.ServiceProvider.GetRequiredService<ILoggerFactory>().CreateLogger("SampleImport");
        var db = scope.ServiceProvider.GetRequiredService<PmgDbContext>();
        if (await db.Statements.AnyAsync()) { log.LogInformation("Sample reports already imported — skipping"); return; }
        var processor = scope.ServiceProvider.GetRequiredService<INszuStatementXlsxProcessor>();
        var demo = scope.ServiceProvider.GetRequiredService<MedLinkDemoDataService>();
        var rec = scope.ServiceProvider.GetRequiredService<ReconciliationService>();
        var root = DatabaseSeeder.ResolvePath(app.Environment.ContentRootPath, app.Configuration["Pmg:SampleReportsPath"] ?? "../..");
        foreach (var name in app.Configuration.GetSection("Pmg:SampleReports").Get<string[]>() ?? Array.Empty<string>())
        {
            var path = new[] { Path.Combine(root, name), Path.Combine(root, "medlink_pmg_bundle", "sample_reports", name) }.FirstOrDefault(File.Exists);
            if (path == null) { log.LogWarning("Sample report not found: {Name}", name); continue; }
            try
            {
                await using var fs = File.OpenRead(path);
                var r = await processor.ProcessAsync(fs, name, fs.Length, null, false, null);
                if (app.Configuration.GetValue("Pmg:GenerateMedLinkDemoEntities", true)) await demo.EnsureDemoEntitiesAsync(r.StatementId);
                await rec.ReconcileAsync(r.StatementId);
                log.LogInformation("Sample report imported: {Name} ({N} lines)", name, r.TotalRecords);
            }
            catch (Exception ex) { log.LogError(ex, "Sample import failed: {Name}", name); }
        }
    });
}

var urls = app.Configuration["Urls"] ?? "http://0.0.0.0:8085";
Console.WriteLine("================================================================================");
Console.WriteLine("MedLink PMG-2026 Analytics — .NET 8 Web API started");
Console.WriteLine($"Frontend (Quasar/Vue):   {urls.Replace("0.0.0.0", "localhost")}/");
Console.WriteLine($"Swagger:                 {urls.Replace("0.0.0.0", "localhost")}/swagger");
Console.WriteLine($"Database (SQLite):       {cs}");
Console.WriteLine($"Web root:                {webRoot}");
Console.WriteLine("================================================================================");

app.Run();

public partial class Program { }
