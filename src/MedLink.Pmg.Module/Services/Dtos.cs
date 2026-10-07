using System.Text.Json.Serialization;

namespace MedLink.Pmg.Module.Services;

/// <summary>Крок розрахунку тарифу (дерево calculation у dsg_analysis_result)</summary>
public class CalculationStep
{
    public string Code { get; set; } = string.Empty;
    public string Caption { get; set; } = string.Empty;
    public decimal Value { get; set; }
    /// <summary>= × + −</summary>
    public string Operation { get; set; } = "×";
    public decimal RunningTotal { get; set; }
    public string? NormativeReference { get; set; }
}

/// <summary>Результат роботи тарифного движка</summary>
public class TariffCalculation
{
    public string? PackageNumber { get; set; }
    /// <summary>DSG | CLASS | FIXED | FIXED_AGE | REHAB_CYCLE | PER_WEEK | GLOBAL | NONE</summary>
    public string Model { get; set; } = "NONE";
    public string? DsgCode { get; set; }
    public string? DsgName { get; set; }
    public string? ClassNumber { get; set; }
    public decimal BaseRate { get; set; }
    public decimal WeightCoef { get; set; } = 1m;
    public decimal GlobalShare { get; set; } = 1m;
    public decimal PlannedCoef { get; set; } = 1m;
    public decimal MountainCoef { get; set; } = 1m;
    public decimal MultiSurgeryCoef { get; set; } = 1m;
    public decimal AgeCoef { get; set; } = 1m;
    public decimal Quantity { get; set; } = 1m;
    /// <summary>Повний нормативний тариф (до застосування частки глобальної ставки)</summary>
    public decimal FullTariff { get; set; }
    /// <summary>Сума, що очікується до оплати закладу</summary>
    public decimal Tariff { get; set; }
    public string Formula { get; set; } = string.Empty;
    public List<CalculationStep> Steps { get; set; } = new();
    public List<string> Notes { get; set; } = new();
    /// <summary>Чи вдалося визначити ДСГ / клас</summary>
    public bool Resolved { get; set; }
    /// <summary>Ставка на пацієнта за період — розподіляється між ЕМЗ пацієнта у пакеті</summary>
    public bool PerPatientPeriod { get; set; }
}

/// <summary>Вхідні параметри для розрахунку тарифу одного випадку</summary>
public class TariffRequest
{
    public string? PackageNumber { get; set; }
    public string? AdsgCode { get; set; }
    public string? PrimaryIcd10Code { get; set; }
    public List<string> SecondaryIcd10Codes { get; set; } = new();
    public List<string> ServiceCodes { get; set; } = new();
    public string? ServiceNumber { get; set; }
    public string? Priority { get; set; }
    public string? EmzType { get; set; }
    public string? InteractionClass { get; set; }
    public int? PatientAge { get; set; }
    public int? LengthOfStayDays { get; set; }
    public bool IsMountain { get; set; }
    public bool HasMultiSurgery { get; set; }
    public int Weeks { get; set; } = 1;
    public string? RehabGroup { get; set; }
    /// <summary>Оцінювати потенційний тариф для записів без пакету / нерозпізнаних ДСГ (Lost Revenue)</summary>
    public bool EstimatePotential { get; set; }
}

/// <summary>Знахідка валідації (findings у dsg_analysis_result)</summary>
public class Finding
{
    public string RuleCode { get; set; } = string.Empty;
    /// <summary>0=Info, 1=Warning, 2=Error (ризик дефектури)</summary>
    public int Severity { get; set; }
    public string Message { get; set; } = string.Empty;
    public string? NormativeReference { get; set; }
    public string? ErrorCode { get; set; }
    public string? Suggestion { get; set; }
}

public class PrebillingRequest
{
    public Guid? OrganizationId { get; set; }
    public Guid? EncounterId { get; set; }
    public Guid? EmployeeId { get; set; }
    public string? PackageNumber { get; set; }
    [JsonPropertyName("icdCode")] public string? IcdCode { get; set; }
    public string? PrimaryIcd10Code { get; set; }
    public List<string>? SecondaryIcd10Codes { get; set; }
    public string? ServiceCode { get; set; }
    public List<string>? Services { get; set; }
    public List<string>? CompanionServices { get; set; }
    public string? DoctorPosition { get; set; }
    public string? AdmissionType { get; set; }
    public string? Priority { get; set; }
    public int? PatientAge { get; set; }
    public string? PatientGender { get; set; }
    public int? LengthOfStayDays { get; set; }
    public bool IsMountain { get; set; }
    public bool? HasMultiSurgery { get; set; }
    public string? RehabGroup { get; set; }
    public bool Persist { get; set; }
}

public class PrebillingResponse
{
    public bool IsValid { get; set; }
    /// <summary>APPROVED | WARNING | REJECTED_DEFEKTURA</summary>
    public string Status { get; set; } = "APPROVED";
    public string? PackageNumber { get; set; }
    public string? DsgCode { get; set; }
    public string? DsgName { get; set; }
    public string? ClassNumber { get; set; }
    public decimal WeightCoef { get; set; }
    public decimal BaseRate { get; set; }
    public decimal Tariff { get; set; }
    public decimal FullTariff { get; set; }
    public string Formula { get; set; } = string.Empty;
    public bool MultisurgeryApplied { get; set; }
    public List<CalculationStep> CalculationSteps { get; set; } = new();
    public List<Finding> Findings { get; set; } = new();
    public object? AntiDefekturaCheck { get; set; }
    public List<object> DsgCandidates { get; set; } = new();
    public Guid? AnalysisResultId { get; set; }

    // сумісність з прототипом (camelCase дублікати)
    public decimal CalculatedTariffUah => Tariff;
    public decimal WeightCoefficient => WeightCoef;
}

public class StatementImportResult
{
    public Guid StatementId { get; set; }
    public string FileName { get; set; } = string.Empty;
    public string OrganizationName { get; set; } = string.Empty;
    public string Edrpou { get; set; } = string.Empty;
    public int ReportYear { get; set; }
    public int ReportMonth { get; set; }
    public string Status { get; set; } = string.Empty;
    public long ParseDurationMs { get; set; }
    public int TotalRecords { get; set; }
    public int DirectPayRecords { get; set; }
    public int GlobalBudgetRecords { get; set; }
    public int RejectedRecords { get; set; }
    public decimal DirectPayAmountUah { get; set; }
    public decimal GlobalBudgetAmountUah { get; set; }
    public decimal LostRevenueUah { get; set; }
    public decimal RecoverableRevenueUah { get; set; }
    public decimal RecoveryRatePercent { get; set; }
    public int PatientsRows { get; set; }
    public int ReportRows { get; set; }
    public int ErrorDescriptionsRows { get; set; }
    public List<ProcessingStage> ProcessingStages { get; set; } = new();
    public List<ErrorFrequency> TopErrors { get; set; } = new();
    public List<PackageBreakdown> Packages { get; set; } = new();
    public object? Reconciliation { get; set; }
    public List<string> Warnings { get; set; } = new();
}

public class ProcessingStage
{
    public int Stage { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Status { get; set; } = "COMPLETED";
    public long DurationMs { get; set; }
    public string? Details { get; set; }
}

public class ErrorFrequency
{
    public string ErrorText { get; set; } = string.Empty;
    public string? ErrorCode { get; set; }
    public string? Category { get; set; }
    public int Count { get; set; }
    public decimal SharePercent { get; set; }
    public decimal LostAmount { get; set; }
    public decimal RecoverableAmount { get; set; }
}

public class PackageBreakdown
{
    public string PackageNumber { get; set; } = string.Empty;
    public string PackageName { get; set; } = string.Empty;
    public int Total { get; set; }
    public int DirectPay { get; set; }
    public int GlobalBudget { get; set; }
    public int Rejected { get; set; }
    public decimal DirectPayAmount { get; set; }
    public decimal GlobalBudgetAmount { get; set; }
    public decimal LostAmount { get; set; }
}

/// <summary>Рекомендація асистента виправлення (AI-assistant) для розбіжності</summary>
public class Recommendation
{
    /// <summary>AddProcedure | LinkEpisode | AdjustDates | ReclassifyPackage | FixDiagnosis | AddIcfCoding | ChangeDoctor | Resubmit | ManualReview | RemoveDuplicate</summary>
    public string Action { get; set; } = "ManualReview";
    public string Title { get; set; } = string.Empty;
    public string Explanation { get; set; } = string.Empty;
    public string? SuggestedServiceCode { get; set; }
    public string? SuggestedServiceName { get; set; }
    public string? SuggestedIcdCode { get; set; }
    public string? SuggestedPackageNumber { get; set; }
    public string? TargetDsg { get; set; }
    public decimal ExpectedRevenue { get; set; }
    public decimal Confidence { get; set; }
    public string? NormativeReference { get; set; }
    public List<string> Steps { get; set; } = new();
}

public class ApplyCorrectionRequest
{
    public Guid DiscrepancyId { get; set; }
    public Guid? EncounterId { get; set; }
    public string? NewPrimaryIcd10Code { get; set; }
    public List<string>? AddServices { get; set; }
    public List<string>? RemoveServices { get; set; }
    public string? NewPackageNumber { get; set; }
    public Guid? NewEmployeeId { get; set; }
    public DateTime? NewDateStart { get; set; }
    public DateTime? NewDateEnd { get; set; }
    public Guid? NewEpisodeId { get; set; }
    public string? Note { get; set; }
    public bool EnqueueResync { get; set; } = true;
    public bool AcceptRecommendation { get; set; }
    public Guid? CorrectedBy { get; set; }
}

public class CombinationValidateRequest
{
    public string? ServiceCode { get; set; }
    public string? IcdCode { get; set; }
    public string? DoctorPosition { get; set; }
    public List<string>? CompanionServices { get; set; }
    public string? AdmissionType { get; set; }
    public bool IsMountain { get; set; }
    public int? PatientAge { get; set; }
    public string? PatientGender { get; set; }
    public string? PackageNumber { get; set; }
}

public class CombinationLibrarySaveRequest
{
    public Guid? OrganizationId { get; set; }
    public Guid? DepartmentId { get; set; }
    public string Name { get; set; } = string.Empty;
    public string ServiceCode { get; set; } = string.Empty;
    public string? IcdCode { get; set; }
    public List<string>? CompanionServices { get; set; }
    public string? DoctorPosition { get; set; }
    public string? PackageNumber { get; set; }
    public string? DsgCode { get; set; }
    public decimal StandardTariff { get; set; }
    public bool MultisurgeryApplied { get; set; }
}
