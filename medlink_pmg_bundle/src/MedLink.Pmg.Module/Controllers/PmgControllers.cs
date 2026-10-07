using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using MedLink.Pmg.Module.Data;
using MedLink.Pmg.Module.Models;
using MedLink.Pmg.Module.Services;

namespace MedLink.Pmg.Module.Controllers
{
    [ApiController]
    [Route("api/v1/nszu/statements")]
    public class NszuStatementsController : ControllerBase
    {
        private readonly PmgDbContext _db;
        private readonly INszuStatementXlsxProcessor _processor;

        public NszuStatementsController(PmgDbContext db, INszuStatementXlsxProcessor processor)
        {
            _db = db;
            _processor = processor;
        }

        [HttpPost("upload")]
        public async Task<IActionResult> UploadStatement([FromForm] IFormFile? file, [FromForm] string? fileName, [FromForm] bool isMountain = false)
        {
            string actualFileName = file?.FileName ?? fileName ?? "Вересень 26.xlsx";
            string targetPath = Path.Combine(@"c:\__MEDLINK___\PMG", actualFileName);

            if (file != null && file.Length > 0)
            {
                using var stream = new FileStream(targetPath, FileMode.Create);
                await file.CopyToAsync(stream);
            }

            var result = await _processor.ProcessStatementFileAsync(targetPath);
            return Ok(result);
        }

        [HttpGet("history")]
        public async Task<IActionResult> GetHistory()
        {
            var statements = await _db.Statements
                .OrderByDescending(s => s.ImportedAt)
                .Take(20)
                .ToListAsync();
            return Ok(statements);
        }

        [HttpGet("{id}/lines")]
        public async Task<IActionResult> GetStatementLines(string id, [FromQuery] string? status = null, [FromQuery] int page = 1, [FromQuery] int pageSize = 50)
        {
            var query = _db.StatementLines.AsQueryable();

            if (!string.IsNullOrEmpty(status) && status != "all")
            {
                if (status == "Так") query = query.Where(l => l.IsAccepted == 1);
                else if (status == "Ні") query = query.Where(l => l.IsAccepted == 0);
            }

            var total = await query.CountAsync();
            var items = await query.Skip((page - 1) * pageSize).Take(pageSize).ToListAsync();

            return Ok(new { total, page, pageSize, items });
        }
    }

    [ApiController]
    [Route("api/v1/pmg/prebilling")]
    public class PmgPrebillingController : ControllerBase
    {
        private readonly PmgDbContext _db;
        private readonly IPmgTariffCalculatorService _calculator;

        public PmgPrebillingController(PmgDbContext db, IPmgTariffCalculatorService calculator)
        {
            _db = db;
            _calculator = calculator;
        }

        public class PrebillingCalculateRequest
        {
            public string IcdCode { get; set; } = string.Empty;
            public string? ServiceCode { get; set; }
            public string DoctorPosition { get; set; } = "P157";
            public string AdmissionType { get; set; } = "Планова";
            public bool IsMountain { get; set; } = false;
        }

        [HttpPost("calculate")]
        public async Task<IActionResult> Calculate([FromBody] PrebillingCalculateRequest req)
        {
            string cleanIcd = req.IcdCode.Replace(".", "").ToUpper();
            var dsg = await _db.DsgCatalog.FirstOrDefaultAsync(d => d.DsgCode.Contains(cleanIcd))
                      ?? await _db.DsgCatalog.FirstOrDefaultAsync(d => d.DsgCode == "O0101");

            double weight = dsg?.CoeffNumeric ?? 2.45;
            string pkgNum = dsg?.PackageId ?? "4";

            var tariffRes = _calculator.CalculateHospitalTariff(pkgNum, weight, req.AdmissionType, req.IsMountain);

            bool isDocValid = req.DoctorPosition != "P122"; // P122 is therapist, illegal in surgery

            return Ok(new
            {
                packageNumber = pkgNum,
                dsgCode = dsg?.DsgCode ?? "O0101",
                dsgName = dsg?.DrgName ?? "Хірургічне втручання",
                weightCoefficient = weight,
                calculatedTariffUah = tariffRes.FinalTariffUah,
                formula = tariffRes.Formula,
                antiDefekturaCheck = new
                {
                    isValid = isDocValid,
                    status = isDocValid ? "APPROVED" : "REJECTED_DEFECTURA",
                    doctorPositionStatus = isDocValid ? "VALID" : "INVALID_SPECIALIZATION",
                    errorWarning = isDocValid ? null : "Помилка посади лікаря (ERR_DOC_SPEC_04). Ризик дефектури: 0 ₴!"
                }
            });
        }
    }

    [ApiController]
    [Route("api/v1/pmg/dictionaries")]
    public class PmgDictionariesController : ControllerBase
    {
        private readonly PmgDbContext _db;

        public PmgDictionariesController(PmgDbContext db)
        {
            _db = db;
        }

        [HttpGet("packages")]
        public async Task<IActionResult> GetPackages([FromQuery] string? category = null)
        {
            var query = _db.Packages.AsQueryable();
            if (!string.IsNullOrEmpty(category))
                query = query.Where(p => p.Category == category);

            return Ok(await query.ToListAsync());
        }

        [HttpGet("service-groups")]
        public async Task<IActionResult> GetServiceGroups()
        {
            return Ok(await _db.ServiceGroups.ToListAsync());
        }

        [HttpGet("services")]
        public async Task<IActionResult> GetServices([FromQuery] string? groupId = null, [FromQuery] string? category = null)
        {
            var query = _db.ServicesCatalog.AsQueryable();
            if (!string.IsNullOrEmpty(groupId)) query = query.Where(s => s.GroupId == groupId);
            if (!string.IsNullOrEmpty(category)) query = query.Where(s => s.Category == category);

            return Ok(await query.ToListAsync());
        }

        [HttpGet("services/{code}")]
        public async Task<IActionResult> GetServiceDetail(string code)
        {
            var svc = await _db.ServicesCatalog.FirstOrDefaultAsync(s => s.ServiceCode == code);
            if (svc == null) return NotFound(new { error = $"Service {code} not found" });

            var combs = await _db.ServiceCombinations.Where(c => c.ServiceCode == code).ToListAsync();
            var risks = await _db.ErrorDictionary.Take(3).ToListAsync();

            return Ok(new
            {
                service = svc,
                combinations = combs,
                defekturaRisks = risks
            });
        }
    }
}
