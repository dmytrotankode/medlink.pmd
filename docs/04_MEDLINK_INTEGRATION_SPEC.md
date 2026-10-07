# Інструкція розробника: Інтеграція модуля ПМГ-2026 в МІС «Медлінк» (evomis)

Цей документ містить покрокові технічні інструкції з переносу та інтеграції розроблених рішень у вихідний код МІС «Медлінк» (`C:\__MEDLINK___\__MEDLINK\evomis`).

---

## 1. Структура розміщення компонентів у репозиторії evomis

```
evomis/
├── src/
│   ├── App.Domain/
│   │   └── Models/
│   │       └── pmg/                         <-- НОВІ ДОМЕННІ СУТНОСТІ
│   │           ├── PmgDsg.cs
│   │           ├── PmgDsgDiagnosis.cs
│   │           ├── PmgDsgService.cs
│   │           ├── PmgOutpatientClass.cs
│   │           ├── NszuReport.cs
│   │           ├── NszuReportDetail.cs       <-- 45 колонок звіту НСЗУ
│   │           └── NszuEncounterDiscrepancy.cs
│   ├── App.DataAccess/
│   │   ├── Context/ApplicationDbContext.cs  <-- Додавання DbSet<T> та мапінгів
│   │   └── Migrations/                      <-- EF Core міграція
│   ├── App.Mdc.Module/                      <-- ОНОВЛЕННЯ СТАРОГО МОДУЛЯ MDC
│   │   └── Data/
│   │       └── csv/                         <-- Заміна CSV 2024 року на ПМГ 2026
│   ├── App.XlsxAnalyzer.Module/             <-- ПРОЦЕСОР ЗВІТІВ НСЗУ
│   │   └── Processors/
│   │       └── Internal/
│   │           └── NszuReportXlsxProcessor.cs <-- Реалізація IXlsxProcessor
│   ├── App.Business/
│   │   └── Services/
│   │       └── ApplicationServices/
│   │           ├── PmgTariffCalculatorService.cs <-- Движок розрахунку тарифів
│   │           └── NszuAuditService.cs           <-- 2-way звірка та рекомендації
│   ├── App.Api/
│   │   └── Controllers/
│   │       └── PmgAnalyticsController.cs     <-- REST API контролер
│   └── App.View/                            <-- ФРОНТЕНД (Quasar / Vue.js)
│       └── src/
│           ├── components/
│           │   └── encounters/
│           │       └── PmgPrebillingWidget.vue  <-- Віджет у картці лікаря
│           ├── pages/
│           │   └── pmg/
│           │       ├── NszuReportsDashboard.vue <-- Дашборд звітів та втрат
│           │       └── EncounterCorrectionModal.vue <-- Модалка 2-way виправлення
│           └── utils/
│               └── mdc-helpers/
│                   └── pmgCalculator.js         <-- Клієнтські формули ПМГ 2026
```

---

## 2. Крок 1: База даних та міграція EF Core

Перенести таблиці з `c:\__MEDLINK___\PMG\pmg_database.sqlite` у PostgreSQL через EF Core.

### C# Модель для 45 колонок звіту (`NszuReportDetail.cs`):

```csharp
namespace App.Domain.Models.pmg
{
    public class NszuReportDetail
    {
        public Guid Id { get; set; } = Guid.NewGuid();
        public Guid ReportId { get; set; }
        public virtual NszuReport Report { get; set; }

        public int RowNumber { get; set; }
        public int ReportYear { get; set; }                   // Кол 1
        public int ReportMonth { get; set; }                  // Кол 2
        public string EmzType { get; set; }                   // Кол 3
        public string EhealthEmzId { get; set; }              // Кол 4 (ID ЕМЗ)
        public DateTime? EhealthInsertedAt { get; set; }       // Кол 5
        public string PractitionerPosition { get; set; }      // Кол 6
        public string PractitionerName { get; set; }          // Кол 7
        public string ServiceLocation { get; set; }           // Кол 8
        public string ReferralType { get; set; }              // Кол 9
        public string ReferralEdrpou { get; set; }            // Кол 10
        public string ReferralDocPosition { get; set; }       // Кол 11
        public string EpisodeId { get; set; }                 // Кол 12
        public string EpisodeType { get; set; }               // Кол 13
        public DateTime? StartDate { get; set; }              // Кол 14
        public DateTime? PeriodStart { get; set; }            // Кол 15
        public DateTime? EndDate { get; set; }                // Кол 16
        public int? LengthOfStay { get; set; }                // Кол 17
        public string PrimaryDiagnosis { get; set; }          // Кол 18
        public string PrimaryDiagConfStatus { get; set; }     // Кол 19
        public string PrimaryDiagClinStatus { get; set; }     // Кол 20
        public string SecondaryDiagnoses { get; set; }        // Кол 21
        public string RejectedDiagnoses { get; set; }         // Кол 22
        public string Interventions { get; set; }             // Кол 23 (АКПІ)
        public string InteractionClass { get; set; }          // Кол 24
        public string Priority { get; set; }                  // Кол 25
        public string InteractionType { get; set; }           // Кол 26
        public string AdmissionReason { get; set; }           // Кол 27
        public string DischargeOutcome { get; set; }          // Кол 28
        public string PatientIdHash { get; set; }             // Кол 29
        public bool HasDeclaration { get; set; }              // Кол 30
        public string PatientGender { get; set; }             // Кол 31
        public int? PatientAge { get; set; }                  // Кол 32
        public string AdditionalEmzInfo { get; set; }         // Кол 33
        public string AdsgCode { get; set; }                  // Кол 34
        public string PackageName { get; set; }               // Кол 35
        public string ServiceCode { get; set; }               // Кол 36
        public string IncludedInStats { get; set; }           // Кол 37
        public string IncludedInReport { get; set; }          // Кол 38 (Так, ГБ, Ні)
        public string ErrorComment { get; set; }              // Кол 39
        public string CompletenessDetailsJson { get; set; }   // Кол 40
        public string VerificationDetails { get; set; }       // Кол 41
        public string GroupingConflictDetails { get; set; }   // Кол 42
        public string NszuReviewDetails { get; set; }         // Кол 43
        public string AdditionalRemarks { get; set; }         // Кол 44
        public DateTime? NszuReviewDate { get; set; }         // Кол 45

        // Автономні поля МІС Медлінк:
        public decimal CalculatedTariff { get; set; }
        public decimal CalculatedLostRevenue { get; set; }
        public Guid? LinkedEncounterId { get; set; }
        public virtual Encounter LinkedEncounter { get; set; }
    }
}
```

---

## 3. Крок 2: Реалізація потокового процесора імпорту Excel

У модулі `src/App.XlsxAnalyzer.Module` реалізувати інтерфейс `IXlsxProcessor`:

```csharp
namespace App.XlsxAnalyzer.Module.Processors.Internal
{
    public class NszuReportXlsxProcessor : IXlsxProcessor
    {
        private readonly IPmgTariffCalculatorService _calculator;
        private readonly ApplicationDbContext _db;

        public NszuReportXlsxProcessor(IPmgTariffCalculatorService calculator, ApplicationDbContext db)
        {
            _calculator = calculator;
            _db = db;
        }

        public async Task<ProcessResult> ProcessAsync(Stream excelStream, Guid reportId, CancellationToken ct)
        {
            using var workbook = new XLWorkbook(excelStream);
            var wsRozsh = workbook.Worksheet("Розшифровка");
            
            // Рядок 4 - заголовки колонок, дані починаються з рядка 5
            var rows = wsRozsh.RowsUsed().Skip(4);
            var batch = new List<NszuReportDetail>();

            foreach (var row in rows)
            {
                var detail = MapRowToDetail(row, reportId);
                
                // 1. Автономний розрахунок тарифу за формулами ПМГ-2026
                detail.CalculatedTariff = _calculator.CalculateRowTariff(detail);
                
                // 2. Якщо відхилено (статус 'Ні') -> фіксація збитку
                if (detail.IncludedInReport == "Ні")
                {
                    detail.CalculatedLostRevenue = detail.CalculatedTariff;
                }

                // 3. Двосторонній пошук ЕМЗ у базі Медлінка за UUID
                var localEncounter = await _db.Encounters
                    .AsNoTracking()
                    .FirstOrDefaultAsync(e => e.EhealthId == detail.EhealthEmzId, ct);

                if (localEncounter != null)
                {
                    detail.LinkedEncounterId = localEncounter.Id;
                }

                batch.Add(detail);

                if (batch.Count >= 500)
                {
                    await _db.NszuReportDetails.AddRangeAsync(batch, ct);
                    await _db.SaveChangesAsync(ct);
                    batch.Clear();
                }
            }

            if (batch.Any())
            {
                await _db.NszuReportDetails.AddRangeAsync(batch, ct);
                await _db.SaveChangesAsync(ct);
            }

            return ProcessResult.Success();
        }
    }
}
```

---

## 4. Крок 3: Розрахунковий сервіс `PmgTariffCalculatorService`

```csharp
namespace App.Business.Services.ApplicationServices
{
    public class PmgTariffCalculatorService : IPmgTariffCalculatorService
    {
        private const decimal InpatientBaseRate = 8735.00m;
        private const decimal OutpatientBaseRate = 155.00m;
        private const decimal ChemoAdultRate = 17865.00m;
        private const decimal ChemoChildRate = 90131.00m;
        private const decimal RadiologyRate = 54089.00m;
        private const decimal RehabCycleRate = 10820.00m;

        public decimal CalculateTariff(string package, string diagCode, string serviceCode, int age, bool isMountain)
        {
            decimal mountainK = isMountain ? 1.25m : 1.00m;

            if (package == "4" || package == "3" || package == "47")
            {
                decimal corrK = package == "47" ? 0.60m : 0.55m;
                decimal dsgWeight = LookupDsgWeight(diagCode, serviceCode);
                decimal ageModifier = age < 1 ? 1.54m : 1.00m;

                return Math.Round(InpatientBaseRate * dsgWeight * corrK * ageModifier * mountainK, 2);
            }

            if (package == "9")
            {
                decimal classK = LookupOutpatientClassWeight(serviceCode);
                return Math.Round(OutpatientBaseRate * classK * mountainK, 2);
            }

            if (package == "17" || package == "38")
            {
                return age < 18 ? ChemoChildRate : ChemoAdultRate;
            }

            if (package == "18") return RadiologyRate;
            if (package == "54" || package == "53") return RehabCycleRate;

            return 0.00m;
        }
    }
}
```

---

## 5. Крок 4: Фронтенд-віджет пре-білінгу у `EncounterEdit.vue`

Вбудовується безпосередньо в екран створення стаціонарної або амбулаторної взаємодії:

```html
<!-- src/App.View/src/components/encounters/PmgPrebillingWidget.vue -->
<template>
  <q-card class="pmg-prebilling-card q-pa-sm" :class="cardStatusClass">
    <div class="row items-center justify-between no-wrap">
      <div class="text-subtitle2 text-weight-bold">
        ⚡ Пре-білінг ПМГ-2026:
        <span class="text-primary">{{ dsgCode || 'Не визначено' }}</span>
      </div>
      <q-badge :color="badgeColor" :label="badgeLabel" />
    </div>

    <div class="text-caption text-grey-8 q-my-xs">
      {{ dsgName }} (Вага: {{ dsgWeight }})
    </div>

    <div v-if="warningMessage" class="text-negative text-caption text-weight-bold q-my-xs">
      ⚠️ {{ warningMessage }}
    </div>

    <q-separator class="q-my-xs" />

    <div class="row items-center justify-between">
      <span class="text-caption text-grey-7">Очікувана сума:</span>
      <span class="text-h6 text-weight-bolder text-positive">{{ formattedAmount }} ₴</span>
    </div>
  </q-card>
</template>

<script>
import { computed } from 'vue';
import { calculatePmgTariff } from '@/utils/mdc-helpers/pmgCalculator';

export default {
  props: {
    diagnosisCode: String,
    serviceCode: String,
    packageId: String,
    patientAge: Number
  },
  setup(props) {
    const calcResult = computed(() => {
      return calculatePmgTariff({
        diag: props.diagnosisCode,
        svc: props.serviceCode,
        pkg: props.packageId,
        age: props.patientAge
      });
    });

    return { ...calcResult };
  }
};
</script>
```

---

## 6. Крок 5: REST API Контролер

```csharp
[ApiController]
[Route("api/pmg-analytics")]
public class PmgAnalyticsController : ControllerBase
{
    private readonly INszuAuditService _auditService;
    private readonly IPmgTariffCalculatorService _calculator;

    [HttpPost("upload-report")]
    public async Task<IActionResult> UploadReport([FromForm] IFormFile file)
    {
        var reportId = await _auditService.ProcessReportUploadAsync(file.OpenReadStream());
        return Ok(new { reportId, message = "Звіт успішно проаналізовано за нормативкою ПМГ-2026" });
    }

    [HttpGet("reports/{id}/summary")]
    public async Task<IActionResult> GetReportSummary(Guid id)
    {
        var summary = await _auditService.GetFinancialSummaryAsync(id);
        return Ok(summary);
    }

    [HttpPost("apply-correction")]
    public async Task<IActionResult> ApplyCorrection([FromBody] CorrectionRequestDto dto)
    {
        await _auditService.ApplyCorrectionToEncounterAsync(dto);
        return Ok(new { success = true, message = "Взаємодію успішно скориговано в Медлінку" });
    }
}
```
