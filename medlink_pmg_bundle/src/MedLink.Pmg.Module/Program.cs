using Microsoft.AspNetCore.Builder;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using MedLink.Pmg.Module.Data;
using MedLink.Pmg.Module.Services;

var builder = WebApplication.CreateBuilder(args);

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
app.UseRouting();
app.MapControllers();

app.Run();
