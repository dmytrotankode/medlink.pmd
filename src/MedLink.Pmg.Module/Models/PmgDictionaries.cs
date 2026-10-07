using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MedLink.Pmg.Module.Models;

// ============================================================================
// Довідники ПМГ-2026 (pmg_*): пакети, ДСГ, амбулаторні класи, реабілітація,
// помилки НСЗУ, вимоги до посад, лабораторія, правила MedProfit, послуги/комбінації.
// Усі таблиці — довідкові (без CoreEntity), заповнюються DatabaseSeeder з seed/*.json.
// ============================================================================

/// <summary>46 пакетів медичних гарантій 2026 (Постанова КМУ № 1808)</summary>
[Table("pmg_packages")]
public class PmgPackage
{
    [Key] [Column("package_id")] [MaxLength(16)] public string PackageId { get; set; } = string.Empty;
    [Column("code")] [MaxLength(16)] public string Code { get; set; } = string.Empty;
    [Column("name")] [MaxLength(500)] public string Name { get; set; } = string.Empty;
    [Column("category")] [MaxLength(255)] public string Category { get; set; } = string.Empty;
    [Column("payment_model")] [MaxLength(255)] public string? PaymentModel { get; set; }
    [Column("base_rate")] public decimal BaseRate { get; set; }
    [Column("rate_period")] [MaxLength(255)] public string? RatePeriod { get; set; }
    [Column("chapter_cmu")] [MaxLength(255)] public string? ChapterCmu { get; set; }
    [Column("formula")] public string? Formula { get; set; }
    [Column("description")] public string? Description { get; set; }
    [Column("coefficients_json")] public string? CoefficientsJson { get; set; }
    [Column("law_references_json")] public string? LawReferencesJson { get; set; }
    [Column("ehealth_validations_json")] public string? EhealthValidationsJson { get; set; }
    [Column("group_file")] [MaxLength(255)] public string? GroupFile { get; set; }
    [NotMapped] public int PackageNumber => int.TryParse(PackageId, out var n) ? n : 0;
}

/// <summary>465 діагностично-споріднених груп (AR-DRG) пакетів 3, 4, 47</summary>
[Table("pmg_dsg")]
public class PmgDsg
{
    [Key] [Column("id")] public int Id { get; set; }
    [Column("package_number")] [MaxLength(16)] public string PackageNumber { get; set; } = string.Empty;
    [Column("dsg_code")] [MaxLength(32)] public string DsgCode { get; set; } = string.Empty;
    [Column("name")] [MaxLength(500)] public string Name { get; set; } = string.Empty;
    [Column("service_type")] [MaxLength(32)] public string? ServiceType { get; set; }
    [Column("coefficient_text")] [MaxLength(64)] public string? CoefficientText { get; set; }
    [Column("weight_coef")] public decimal WeightCoef { get; set; }
    [Column("base_rate")] public decimal BaseRate { get; set; } = 8735.00m;
    [Column("global_rate_share")] public decimal GlobalRateShare { get; set; } = 0.55m;
    [Column("full_tariff")] public decimal FullTariff { get; set; }
    [Column("share_tariff")] public decimal ShareTariff { get; set; }
    [Column("planned_coef")] public decimal? PlannedCoef { get; set; }
    [Column("additional_requirements")] [MaxLength(255)] public string? AdditionalRequirements { get; set; }
    [Column("additional_requirements_code")] [MaxLength(255)] public string? AdditionalRequirementsCode { get; set; }
    [Column("additional_requirements_services_json")] public string? AdditionalRequirementsServicesJson { get; set; }
    [Column("additional_requirements_referral")] [MaxLength(255)] public string? AdditionalRequirementsReferral { get; set; }
    [Column("required_packages")] [MaxLength(128)] public string? RequiredPackages { get; set; }
    [Column("episode")] [MaxLength(255)] public string? Episode { get; set; }
    [Column("diag_count")] public int DiagCount { get; set; }
    [Column("svc_count")] public int SvcCount { get; set; }
    [Column("age_notes_json")] public string? AgeNotesJson { get; set; }
}

/// <summary>Нормалізований індекс МКХ-10 → ДСГ (285 554 зв'язки)</summary>
[Table("pmg_dsg_diagnoses")]
public class PmgDsgDiagnosis
{
    [Column("package_number")] [MaxLength(16)] public string PackageNumber { get; set; } = string.Empty;
    [Column("dsg_id")] public int DsgId { get; set; }
    [Column("dsg_code")] [MaxLength(32)] public string DsgCode { get; set; } = string.Empty;
    [Column("diag_code")] [MaxLength(16)] public string DiagCode { get; set; } = string.Empty;
}

/// <summary>Нормалізований індекс АКПІ → ДСГ (28 167 зв'язків)</summary>
[Table("pmg_dsg_services")]
public class PmgDsgService
{
    [Column("package_number")] [MaxLength(16)] public string PackageNumber { get; set; } = string.Empty;
    [Column("dsg_id")] public int DsgId { get; set; }
    [Column("dsg_code")] [MaxLength(32)] public string DsgCode { get; set; } = string.Empty;
    [Column("service_code")] [MaxLength(32)] public string ServiceCode { get; set; } = string.Empty;
}

/// <summary>Довідник МКХ-10 (назви діагнозів з нормативних пакетів)</summary>
[Table("pmg_icd10")]
public class PmgIcd10
{
    [Key] [Column("code")] [MaxLength(16)] public string Code { get; set; } = string.Empty;
    [Column("name")] [MaxLength(1000)] public string Name { get; set; } = string.Empty;
}

/// <summary>Довідник АКПІ / ACHI (назви інтервенцій)</summary>
[Table("pmg_achi")]
public class PmgAchi
{
    [Key] [Column("code")] [MaxLength(32)] public string Code { get; set; } = string.Empty;
    [Column("name")] [MaxLength(1000)] public string Name { get; set; } = string.Empty;
}

/// <summary>148 амбулаторних класів Пакету 9</summary>
[Table("pmg_package9_classes")]
public class PmgPackage9Class
{
    [Key] [Column("id")] public int Id { get; set; }
    [Column("class_number")] [MaxLength(16)] public string ClassNumber { get; set; } = string.Empty;
    [Column("class_name")] [MaxLength(255)] public string ClassName { get; set; } = string.Empty;
    [Column("service_type")] [MaxLength(128)] public string ServiceType { get; set; } = string.Empty;
    [Column("coefficient")] public decimal Coefficient { get; set; }
    [Column("cost")] public decimal Cost { get; set; }
    [Column("note")] public string? Note { get; set; }
    [Column("additional_requirements_code")] [MaxLength(255)] public string? AdditionalRequirementsCode { get; set; }
    [Column("episode_json")] public string? EpisodeJson { get; set; }
    [Column("diag_count")] public int DiagCount { get; set; }
    [Column("svc_count")] public int SvcCount { get; set; }
    [Column("positions_json")] public string? PositionsJson { get; set; }
}

[Table("pmg_package9_class_services")]
public class PmgPackage9ClassService
{
    [Column("class_id")] public int ClassId { get; set; }
    [Column("class_number")] [MaxLength(16)] public string ClassNumber { get; set; } = string.Empty;
    [Column("service_code")] [MaxLength(32)] public string ServiceCode { get; set; } = string.Empty;
}

[Table("pmg_package9_class_diagnoses")]
public class PmgPackage9ClassDiagnosis
{
    [Column("class_id")] public int ClassId { get; set; }
    [Column("class_number")] [MaxLength(16)] public string ClassNumber { get; set; } = string.Empty;
    [Column("diag_code")] [MaxLength(16)] public string DiagCode { get; set; } = string.Empty;
}

[Table("pmg_package9_class_positions")]
public class PmgPackage9ClassPosition
{
    [Column("class_id")] public int ClassId { get; set; }
    [Column("class_number")] [MaxLength(16)] public string ClassNumber { get; set; } = string.Empty;
    [Column("position_code")] [MaxLength(16)] public string PositionCode { get; set; } = string.Empty;
    [Column("position_name")] [MaxLength(255)] public string PositionName { get; set; } = string.Empty;
}

/// <summary>Реабілітаційні групи АР1–АР4 (Пакет 54 / 53)</summary>
[Table("pmg_rehab_groups")]
public class PmgRehabGroup
{
    [Key] [Column("code")] [MaxLength(16)] public string Code { get; set; } = string.Empty;
    [Column("coefficient")] public decimal Coefficient { get; set; }
    [Column("requirements")] public string? Requirements { get; set; }
    [Column("episode")] public string? Episode { get; set; }
    [Column("plan")] public string? Plan { get; set; }
    [Column("referral")] public string? Referral { get; set; }
    [Column("reports")] public string? Reports { get; set; }
    [Column("procedures")] public string? Procedures { get; set; }
    [Column("duration")] public string? Duration { get; set; }
    [Column("duration_short")] [MaxLength(255)] public string? DurationShort { get; set; }
}

/// <summary>Критерії кодування CR (80 правил) реабілітації</summary>
[Table("pmg_rehab_rules")]
public class PmgRehabRule
{
    [Key] [Column("code")] [MaxLength(16)] public string Code { get; set; } = string.Empty;
    [Column("rule_group")] [MaxLength(255)] public string? RuleGroup { get; set; }
    [Column("rule_text")] public string? RuleText { get; set; }
    [Column("examples_json")] public string? ExamplesJson { get; set; }
}

/// <summary>Матриця діагнозів реабілітації (5 866 рядків): МКХ-10 → групи АР, тип діагнозу, CR</summary>
[Table("pmg_rehab_diagnoses")]
public class PmgRehabDiagnosis
{
    [Key] [Column("id")] public int Id { get; set; }
    [Column("diag_code")] [MaxLength(16)] public string DiagCode { get; set; } = string.Empty;
    [Column("name")] [MaxLength(1000)] public string? Name { get; set; }
    [Column("ar_groups")] [MaxLength(128)] public string? ArGroups { get; set; }
    [Column("cr_code")] [MaxLength(32)] public string? CrCode { get; set; }
    [Column("cr_group")] [MaxLength(255)] public string? CrGroup { get; set; }
    [Column("is_main")] public bool IsMain { get; set; }
    [Column("is_main_note")] [MaxLength(500)] public string? IsMainNote { get; set; }
    [Column("diag_types")] [MaxLength(255)] public string? DiagTypes { get; set; }
    [Column("referral_pmd")] public bool ReferralPmd { get; set; }
    [Column("marker")] [MaxLength(128)] public string? Marker { get; set; }
    [Column("note")] public string? Note { get; set; }
}

/// <summary>331 послуга реабілітації з прив'язкою до АР-груп та фахівців</summary>
[Table("pmg_rehab_services")]
public class PmgRehabService
{
    [Key] [Column("id")] public int Id { get; set; }
    [Column("intervention")] [MaxLength(500)] public string Intervention { get; set; } = string.Empty;
    [Column("service_code")] [MaxLength(32)] public string? ServiceCode { get; set; }
    [Column("ar_groups")] [MaxLength(128)] public string? ArGroups { get; set; }
    [Column("specialist")] [MaxLength(500)] public string? Specialist { get; set; }
    [Column("service_type")] [MaxLength(255)] public string? ServiceType { get; set; }
}

/// <summary>186 кодів помилок дефектури НСЗУ з нормативними посиланнями та порадами</summary>
[Table("pmg_nhsu_error_dictionary")]
public class PmgNhsuErrorDictionary
{
    [Key] [Column("id")] public int Id { get; set; }
    [Column("error_code")] [MaxLength(32)] public string ErrorCode { get; set; } = string.Empty;
    [Column("title")] [MaxLength(255)] public string Title { get; set; } = string.Empty;
    [Column("normative_reference")] [MaxLength(255)] public string? NormativeReference { get; set; }
    [Column("description")] public string Description { get; set; } = string.Empty;
    [Column("remediation_advice")] public string? RemediationAdvice { get; set; }
    /// <summary>1 = Попередження, 2 = Блокуюча помилка (дефектура)</summary>
    [Column("severity")] public int Severity { get; set; } = 2;
    [Column("category")] [MaxLength(64)] public string? Category { get; set; }
    [Column("recoverability_percent")] public decimal RecoverabilityPercent { get; set; } = 50m;
    [Column("nszu_comment_pattern")] [MaxLength(255)] public string? NszuCommentPattern { get; set; }
}

/// <summary>1 257 вимог до посад лікарів за послугами (MedProfit Anti-Defektura)</summary>
[Table("pmg_service_doctor_positions")]
public class PmgServiceDoctorPosition
{
    [Key] [Column("id")] public int Id { get; set; }
    [Column("service_code")] [MaxLength(64)] public string ServiceCode { get; set; } = string.Empty;
    [Column("service_name")] [MaxLength(500)] public string ServiceName { get; set; } = string.Empty;
    [Column("service_type")] [MaxLength(32)] public string? ServiceType { get; set; }
    [Column("class_number")] [MaxLength(32)] public string? ClassNumber { get; set; }
    [Column("class_name")] [MaxLength(255)] public string? ClassName { get; set; }
    [Column("mdc_requirements")] [MaxLength(64)] public string? MdcRequirements { get; set; }
    /// <summary>Дозволені коди посад через кому: P157,P158,P58</summary>
    [Column("position_requirements")] [MaxLength(255)] public string PositionRequirements { get; set; } = string.Empty;
}

/// <summary>408 лабораторних досліджень (A34xxx, A35xxx)</summary>
[Table("pmg_laboratory_catalog")]
public class PmgLaboratoryCatalog
{
    [Key] [Column("id")] public int Id { get; set; }
    [Column("test_code")] [MaxLength(32)] public string TestCode { get; set; } = string.Empty;
    [Column("test_name")] [MaxLength(500)] public string TestName { get; set; } = string.Empty;
    [Column("test_group")] [MaxLength(255)] public string TestGroup { get; set; } = string.Empty;
}

/// <summary>185 правил класифікації MedProfit (dct_mp_service_odk_rule)</summary>
[Table("pmg_classification_rules")]
public class PmgClassificationRule
{
    [Key] [Column("id")] public int Id { get; set; }
    [Column("legacy_rule_id")] public int LegacyRuleId { get; set; }
    [Column("rule_type")] [MaxLength(64)] public string RuleType { get; set; } = string.Empty;
    [Column("rule_code")] [MaxLength(64)] public string? RuleCode { get; set; }
    [Column("rule_group")] [MaxLength(64)] public string? RuleGroup { get; set; }
    [Column("rule_data")] public string RuleDataJson { get; set; } = "{}";
}

/// <summary>12 клініко-технологічних груп послуг</summary>
[Table("pmg_service_groups")]
public class PmgServiceGroup
{
    [Key] [Column("id")] [MaxLength(32)] public string Id { get; set; } = string.Empty;
    [Column("code")] [MaxLength(16)] public string Code { get; set; } = string.Empty;
    [Column("name")] [MaxLength(255)] public string Name { get; set; } = string.Empty;
    [Column("parent_id")] [MaxLength(32)] public string? ParentId { get; set; }
    [Column("level")] public int Level { get; set; } = 1;
    [Column("description")] public string? Description { get; set; }
    [NotMapped] public int ServiceCount { get; set; }
}

/// <summary>Каталог послуг АКПІ з клінічними нормами (час, анестезія, ліжко-дні, вік, стать)</summary>
[Table("pmg_service_catalog")]
public class PmgServiceCatalog
{
    [Key] [Column("service_code")] [MaxLength(32)] public string ServiceCode { get; set; } = string.Empty;
    [Column("name")] [MaxLength(500)] public string Name { get; set; } = string.Empty;
    [Column("group_id")] [MaxLength(32)] public string? GroupId { get; set; }
    [Column("group_name")] [MaxLength(255)] public string? GroupName { get; set; }
    [Column("category")] [MaxLength(64)] public string Category { get; set; } = string.Empty;
    [Column("base_norm_time_minutes")] public int BaseNormTimeMinutes { get; set; } = 60;
    [Column("anesthesia_required")] public int AnesthesiaRequired { get; set; }
    [Column("min_stay_days")] public int MinStayDays { get; set; }
    [Column("max_stay_days")] public int MaxStayDays { get; set; } = 14;
    [Column("age_min")] public int AgeMin { get; set; }
    [Column("age_max")] public int AgeMax { get; set; } = 120;
    [Column("gender_restriction")] [MaxLength(16)] public string GenderRestriction { get; set; } = "ALL";
    [Column("package_ids")] [MaxLength(64)] public string? PackageIds { get; set; }
    [Column("dsg_codes")] [MaxLength(128)] public string? DsgCodes { get; set; }
    [Column("base_tariff")] public decimal BaseTariff { get; set; }
    [Column("clinical_norm_notes")] public string? ClinicalNormNotes { get; set; }
}

/// <summary>Матриця комбінацій послуг (реінженерія Delphi dct_mp_service_odk_rule_detail)</summary>
[Table("pmg_service_combinations")]
public class PmgServiceCombination
{
    [Key] [Column("id")] [MaxLength(64)] public string Id { get; set; } = string.Empty;
    [Column("service_code")] [MaxLength(32)] public string ServiceCode { get; set; } = string.Empty;
    [Column("combination_name")] [MaxLength(500)] public string CombinationName { get; set; } = string.Empty;
    [Column("compatible_icd_codes")] public string? CompatibleIcdCodesJson { get; set; }
    [Column("mandatory_companions")] public string? MandatoryCompanionsJson { get; set; }
    [Column("optional_multisurg_companions")] public string? OptionalMultisurgCompanionsJson { get; set; }
    [Column("incompatible_services")] public string? IncompatibleServicesJson { get; set; }
    [Column("allowed_doctor_positions")] public string? AllowedDoctorPositionsJson { get; set; }
    [Column("prohibited_doctor_positions")] public string? ProhibitedDoctorPositionsJson { get; set; }
    [Column("expected_package_number")] [MaxLength(16)] public string? ExpectedPackageNumber { get; set; }
    [Column("expected_dsg_code")] [MaxLength(32)] public string? ExpectedDsgCode { get; set; }
    [Column("weight_coef")] public decimal WeightCoef { get; set; } = 1.0m;
    [Column("calculated_tariff")] public decimal CalculatedTariff { get; set; }
    [Column("calculation_formula")] [MaxLength(500)] public string? CalculationFormula { get; set; }
    [Column("rule_condition")] public string? RuleCondition { get; set; }
    [Column("is_library_standard")] public int IsLibraryStandard { get; set; }
}

/// <summary>Бібліотека еталонів лікування відділення (myAddLib)</summary>
[Table("pmg_combination_library")]
public class PmgCombinationLibrary : CoreEntity
{
    [Column("organization_id")] public Guid? OrganizationId { get; set; }
    [Column("department_id")] public Guid? DepartmentId { get; set; }
    [Column("name")] [MaxLength(500)] public string Name { get; set; } = string.Empty;
    [Column("service_code")] [MaxLength(32)] public string ServiceCode { get; set; } = string.Empty;
    [Column("icd_code")] [MaxLength(16)] public string? IcdCode { get; set; }
    [Column("companion_services_json")] public string? CompanionServicesJson { get; set; }
    [Column("doctor_position")] [MaxLength(16)] public string? DoctorPosition { get; set; }
    [Column("package_number")] [MaxLength(16)] public string? PackageNumber { get; set; }
    [Column("dsg_code")] [MaxLength(32)] public string? DsgCode { get; set; }
    [Column("standard_tariff")] public decimal StandardTariff { get; set; }
    [Column("multisurgery_applied")] public bool MultisurgeryApplied { get; set; }
    [Column("is_approved")] public bool IsApproved { get; set; } = true;
}
