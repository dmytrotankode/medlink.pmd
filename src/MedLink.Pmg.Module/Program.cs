using System.IO;
using Microsoft.AspNetCore.Builder;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.FileProviders;
using Microsoft.Extensions.Hosting;
using MedLink.Pmg.Module.Data;
using MedLink.Pmg.Module.Services;

var builder = WebApplication.CreateBuilder(args);

// Configure port 8085
builder.WebHost.UseUrls("http://0.0.0.0:8085");

// Add services to the container
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();

// Configure SQLite DbContext connecting to real database
var dbPath = @"c:\__MEDLINK___\PMG\pmg_database.sqlite";
builder.Services.AddDbContext<PmgDbContext>(options =>
    options.UseSqlite($"Data Source={dbPath}"));

// Register Business Services
builder.Services.AddScoped<IPmgTariffCalculatorService, PmgTariffCalculatorService>();
builder.Services.AddScoped<INszuStatementXlsxProcessor, NszuStatementXlsxProcessor>();

// CORS configuration for MedLink frontend
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

app.UseCors("AllowAll");

// Serve static files from c:\__MEDLINK___\PMG
var rootPath = @"c:\__MEDLINK___\PMG";
if (Directory.Exists(rootPath))
{
    var fileProvider = new PhysicalFileProvider(rootPath);
    app.UseDefaultFiles(new DefaultFilesOptions
    {
        FileProvider = fileProvider
    });
    app.UseStaticFiles(new StaticFileOptions
    {
        FileProvider = fileProvider,
        RequestPath = ""
    });
}

app.UseRouting();
app.MapControllers();

// Default root redirect to prototype
app.MapGet("/", () => Results.Redirect("/prototype_medlink/index.html"));

app.Run();
