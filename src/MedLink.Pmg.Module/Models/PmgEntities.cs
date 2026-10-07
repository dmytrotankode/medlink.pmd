using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MedLink.Pmg.Module.Models
{
    /// <summary>
    /// Базовий клас сутностей МІС «Медлінк» (відповідник CoreEntity в App.Domain)
    /// </summary>
    public abstract class CoreEntity
    {
        [Key]
        [Column("id")]
        public Guid Id { get; set; } = Guid.NewGuid();

        [Column("created_date")]
        public DateTime CreatedDate { get; set; } = DateTime.UtcNow;

        [Column("created_by")]
        public Guid? CreatedBy { get; set; }

        [Column("modified_date")]
        public DateTime? ModifiedDate { get; set; }

        [Column("modified_by")]
        public Guid? ModifiedBy { get; set; }

        [Column("is_deleted")]
        public bool IsDeleted { get; set; } = false;
    }

    /// <summary>
    /// Звіт НСЗУ (аркуш «Розшифровка» та «Звіт»)
    /// </summary>
    [Table("dsg_nszu_statement")]
    public class NszuStatement
    {
        [Key]
        [Column("id")]
        public string Id { get; set; } = Guid.NewGuid().ToString();

        [Column("organization_id")]
        public string OrganizationId { get; set; } = string.Empty;

        [Column("organization_name")]
        public string OrganizationName { get; set; } = string.Empty;

        [Column("period_from")]
        public string PeriodFrom { get; set; } = string.Empty;

        [Column("period_to")]
        public string PeriodTo { get; set; } = string.Empty;

        [Column("file_name")]
        public string FileName { get; set; } = string.Empty;

        [Column("imported_at")]
        public string ImportedAt { get; set; } = DateTime.UtcNow.ToString("o");

        [Column("imported_by")]
        public string? ImportedBy { get; set; }

        [Column("total_records")]
        public int TotalRecords { get; set; }

        [Column("accepted_records")]
        public int AcceptedRecords { get; set; }

        [Column("rejected_records")]
        public int RejectedRecords { get; set; }

        [Column("accepted_amount")]
        public double AcceptedAmount { get; set; }

        [Column("rejected_amount")]
        public double RejectedAmount { get; set; }

        [Column("reconciled_at")]
        public string? ReconciledAt { get; set; }

        [Column("status")]
        public string Status { get; set; } = "Uploaded";

        // Navigation property to lines
        public virtual ICollection<NszuStatementLine> Lines { get; set; } = new List<NszuStatementLine>();
    }

    /// <summary>
    /// Рядок звіту НСЗУ (45 колонок аркуша «Розшифровка»)
    /// </summary>
    [Table("dsg_nszu_statement_line")]
    public class NszuStatementLine
    {
        [Key]
        [Column("id")]
        public string Id { get; set; } = Guid.NewGuid().ToString();

        [Column("statement_id")]
        public string StatementId { get; set; } = string.Empty;

        [Column("line_number")]
        public int LineNumber { get; set; }

        [Column("encounter_ehealth_id")]
        public string? EncounterEhealthId { get; set; }

        [Column("patient_rnokpp")]
        public string? PatientRnokpp { get; set; }

        [Column("patient_full_name")]
        public string? PatientFullName { get; set; }

        [Column("doctor_id")]
        public string? DoctorId { get; set; }

        [Column("doctor_full_name")]
        public string? DoctorFullName { get; set; }

        [Column("department_id")]
        public string? DepartmentId { get; set; }

        [Column("department_name")]
        public string? DepartmentName { get; set; }

        [Column("package_number")]
        public string? PackageNumber { get; set; }

        [Column("admission_type")]
        public string? AdmissionType { get; set; }

        [Column("date_start")]
        public string? DateStart { get; set; }

        [Column("date_end")]
        public string? DateEnd { get; set; }

        [Column("primary_icd10_code")]
        public string? PrimaryIcd10Code { get; set; }

        [Column("primary_icd10_name")]
        public string? PrimaryIcd10Name { get; set; }

        [Column("interventions")]
        public string? Interventions { get; set; }

        [Column("dsg_code")]
        public string? DsgCode { get; set; }

        [Column("dsg_name")]
        public string? DsgName { get; set; }

        [Column("weight_coef")]
        public double WeightCoef { get; set; } = 1.0;

        [Column("service_class_code")]
        public string? ServiceClassCode { get; set; }

        [Column("service_class_name")]
        public string? ServiceClassName { get; set; }

        [Column("nszu_amount")]
        public double NszuAmount { get; set; }

        [Column("mis_amount")]
        public double? MisAmount { get; set; }

        [Column("difference")]
        public double? Difference { get; set; }

        [Column("is_accepted")]
        public int IsAccepted { get; set; }

        [Column("rejection_reason_code")]
        public string? RejectionReasonCode { get; set; }

        [Column("rejection_reason_text")]
        public string? RejectionReasonText { get; set; }

        [Column("legal_basis")]
        public string? LegalBasis { get; set; }

        [Column("matched_encounter_id")]
        public string? MatchedEncounterId { get; set; }

        [Column("match_status")]
        public int MatchStatus { get; set; }

        [Column("raw_payload_json")]
        public string? RawPayloadJson { get; set; }

        // Зв'язки із сутностями Медлінка (Logical mappings to MedLink entities)
        [NotMapped]
        public virtual MisEncounter? LinkedEncounter { get; set; }

        [NotMapped]
        public virtual OrgEmployee? LinkedDoctor { get; set; }

        [NotMapped]
        public virtual OrgDepartment? LinkedDepartment { get; set; }
    }

    /// <summary>
    /// Існуюча сутність ЕМЗ у Медлінку (App.Domain.Models.Encounter)
    /// </summary>
    [Table("mis_encounter")]
    public class MisEncounter : CoreEntity
    {
        [Column("ehealth_id")]
        public string EhealthId { get; set; } = string.Empty;

        [Column("patient_id")]
        public Guid PatientId { get; set; }

        [Column("doctor_id")]
        public Guid DoctorId { get; set; }

        [Column("department_id")]
        public Guid? DepartmentId { get; set; }

        [Column("date_start")]
        public DateTime DateStart { get; set; }

        [Column("date_end")]
        public DateTime? DateEnd { get; set; }

        [Column("primary_diagnosis")]
        public string PrimaryDiagnosis { get; set; } = string.Empty;

        [Column("interventions_json")]
        public string? InterventionsJson { get; set; }

        [Column("status")]
        public string Status { get; set; } = "Completed";

        [Column("is_signed")]
        public bool IsSigned { get; set; } = true;
    }

    /// <summary>
    /// Співробітник / лікар у Медлінку (App.Domain.Models.OrgEmployee)
    /// </summary>
    [Table("org_employee")]
    public class OrgEmployee : CoreEntity
    {
        [Column("full_name")]
        public string FullName { get; set; } = string.Empty;

        [Column("position_code")]
        public string PositionCode { get; set; } = string.Empty;

        [Column("position_name")]
        public string PositionName { get; set; } = string.Empty;

        [Column("department_id")]
        public Guid? DepartmentId { get; set; }

        [Column("is_active")]
        public bool IsActive { get; set; } = true;
    }

    /// <summary>
    /// Відділення закладу у Медлінку (App.Domain.Models.OrgDepartment)
    /// </summary>
    [Table("org_department")]
    public class OrgDepartment : CoreEntity
    {
        [Column("name")]
        public string Name { get; set; } = string.Empty;

        [Column("code")]
        public string Code { get; set; } = string.Empty;
    }

    /// <summary>
    /// Пацієнт у Медлінку (App.Domain.Models.Patient)
    /// </summary>
    [Table("mis_patient")]
    public class MisPatient : CoreEntity
    {
        [Column("full_name")]
        public string FullName { get; set; } = string.Empty;

        [Column("rnokpp")]
        public string? Rnokpp { get; set; }

        [Column("birth_date")]
        public DateTime? BirthDate { get; set; }

        [Column("gender")]
        public string? Gender { get; set; }
    }

    /// <summary>
    /// Довідник 46 пакетів ПМГ-2026
    /// </summary>
    [Table("pmg_packages")]
    public class PmgPackage
    {
        [Key]
        [Column("package_id")]
        public string PackageId { get; set; } = string.Empty;

        [Column("name")]
        public string Name { get; set; } = string.Empty;

        [Column("base_rate")]
        public double BaseRate { get; set; }

        [Column("meta_json")]
        public string? MetaJson { get; set; }

        [NotMapped]
        public int PackageNumber => int.TryParse(PackageId, out int n) ? n : 0;

        [NotMapped]
        public string Category { get; set; } = string.Empty;

        [NotMapped]
        public string? PaymentModel { get; set; }

        [NotMapped]
        public string? CalculationFormula { get; set; }

        [NotMapped]
        public string? EhealthValidationRules { get; set; }
    }

    /// <summary>
    /// Класифікатор 465 ДСГ стаціонару
    /// </summary>
    [Table("pmg_dsg")]
    public class PmgDsg
    {
        [Key]
        [Column("id")]
        public int Id { get; set; }

        [Column("package_id")]
        public string PackageId { get; set; } = string.Empty;

        [Column("drg_name")]
        public string DrgName { get; set; } = string.Empty;

        [Column("coeff_numeric")]
        public double CoeffNumeric { get; set; }

        [Column("base_rate")]
        public double BaseRate { get; set; } = 8735.00;

        [Column("price")]
        public double Price { get; set; }

        [Column("req_package_1")]
        public string? ReqPackage1 { get; set; }

        [Column("diags_json")]
        public string? DiagsJson { get; set; }

        [Column("services_json")]
        public string? ServicesJson { get; set; }

        [NotMapped]
        public string DsgCode => Id.ToString();
    }

    /// <summary>
    /// Класифікатор 148 амбулаторних класів (Пакет 9)
    /// </summary>
    [Table("pmg_package9_classes")]
    public class PmgPackage9Class
    {
        [Key]
        [Column("id")]
        public int Id { get; set; }

        [Column("class_name")]
        public string ClassName { get; set; } = string.Empty;

        [Column("class_number")]
        public string ClassNumber { get; set; } = string.Empty;

        [Column("coefficient")]
        public double Coefficient { get; set; }

        [Column("cost")]
        public double Cost { get; set; }

        [NotMapped]
        public string ClassCode => ClassNumber;

        [NotMapped]
        public double WeightCoefficient => Coefficient;

        [NotMapped]
        public double CalculatedTariff => Cost;
    }

    /// <summary>
    /// Довідник 186 кодів помилок дефектури НСЗУ
    /// </summary>
    [Table("dsg_nhsu_error_dictionary")]
    public class PmgNhsuErrorDictionary
    {
        [Key]
        [Column("id")]
        public int Id { get; set; }

        [Column("error_code")]
        public string ErrorCode { get; set; } = string.Empty;

        [Column("title")]
        public string Title { get; set; } = string.Empty;

        [Column("description")]
        public string Description { get; set; } = string.Empty;

        [Column("legal_basis")]
        public string? LegalBasis { get; set; }

        [Column("recommendation_action")]
        public string? RecommendationAction { get; set; }

        [Column("severity")]
        public string Severity { get; set; } = "MEDIUM";

        [Column("category")]
        public string? Category { get; set; }

        [NotMapped]
        public string ErrorDescription => Description;

        [NotMapped]
        public string ErrorCategory => Category ?? "Загальні";

        [NotMapped]
        public string? ResolutionGuidance => RecommendationAction;

        [NotMapped]
        public double RecoverabilityPercent { get; set; } = 50.0;
    }

    /// <summary>
    /// 12 Клінічних груп послуг
    /// </summary>
    [Table("pmg_service_groups")]
    public class PmgServiceGroup
    {
        [Key]
        [Column("id")]
        public string Id { get; set; } = string.Empty;

        [Column("code")]
        public string Code { get; set; } = string.Empty;

        [Column("name")]
        public string Name { get; set; } = string.Empty;

        [Column("description")]
        public string? Description { get; set; }

        [NotMapped]
        public int ServiceCount { get; set; }
    }

    /// <summary>
    /// Каталог медичних послуг АКПІ з клінічними нормами
    /// </summary>
    [Table("pmg_service_catalog")]
    public class PmgServiceCatalog
    {
        [Key]
        [Column("service_code")]
        public string ServiceCode { get; set; } = string.Empty;

        [Column("name")]
        public string Name { get; set; } = string.Empty;

        [Column("group_id")]
        public string GroupId { get; set; } = string.Empty;

        [Column("category")]
        public string Category { get; set; } = string.Empty;

        [Column("base_norm_time_minutes")]
        public int BaseNormTimeMinutes { get; set; } = 60;

        [Column("anesthesia_required")]
        public int AnesthesiaRequired { get; set; } = 0;

        [Column("min_stay_days")]
        public int MinStayDays { get; set; } = 1;

        [Column("max_stay_days")]
        public int MaxStayDays { get; set; } = 10;

        [Column("gender_restriction")]
        public string GenderRestriction { get; set; } = "ALL";

        [Column("age_min")]
        public int AgeMin { get; set; } = 0;

        [Column("age_max")]
        public int AgeMax { get; set; } = 120;

        [Column("doctor_position_allowed")]
        public string? DoctorPositionAllowed { get; set; }

        [Column("base_tariff_uah")]
        public double BaseTariffUah { get; set; }

        [Column("package_ids")]
        public string? PackageIds { get; set; }
    }

    /// <summary>
    /// Матриця комбінацій послуг (Delphi dct_mp_service_odk_rule_detail)
    /// </summary>
    [Table("pmg_service_combinations")]
    public class PmgServiceCombination
    {
        [Key]
        [Column("id")]
        public string Id { get; set; } = string.Empty;

        [Column("service_code")]
        public string ServiceCode { get; set; } = string.Empty;

        [Column("combination_name")]
        public string CombinationName { get; set; } = string.Empty;

        [Column("compatible_icd_codes")]
        public string? CompatibleIcdCodes { get; set; }

        [Column("mandatory_companions")]
        public string? MandatoryCompanions { get; set; }

        [Column("optional_multisurg_companions")]
        public string? OptionalMultisurgCompanions { get; set; }

        [Column("incompatible_services")]
        public string? IncompatibleServices { get; set; }

        [Column("allowed_doctor_positions")]
        public string? AllowedDoctorPositions { get; set; }

        [Column("prohibited_doctor_positions")]
        public string? ProhibitedDoctorPositions { get; set; }

        [Column("expected_package_number")]
        public string? ExpectedPackageNumber { get; set; }

        [Column("expected_dsg_code")]
        public string? ExpectedDsgCode { get; set; }

        [Column("weight_coef")]
        public double WeightCoef { get; set; } = 1.0;

        [Column("calculated_tariff")]
        public double CalculatedTariff { get; set; }

        [Column("calculation_formula")]
        public string? CalculationFormula { get; set; }

        [Column("rule_condition")]
        public string? RuleCondition { get; set; }

        [Column("is_library_standard")]
        public int IsLibraryStandard { get; set; } = 0;
    }
}
