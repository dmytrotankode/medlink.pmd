using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MedLink.Pmg.Module.Models;

// ============================================================================
// Домен dsg_* — звіти НСЗУ, результати аналізу, розбіжності, налаштування тарифів.
// Назви таблиць збігаються з ядром evomis-test (dsg_nszu_statement, dsg_nszu_statement_line,
// dsg_analysis_result, dsg_tariff_setting, dsg_rule_config).
// ============================================================================

public static class NszuInclusion
{
    public const string DirectPay = "Так";
    public const string GlobalBudget = "ГБ";
    public const string Rejected = "Ні";
}

/// <summary>Статус 2-Way звірки рядка звіту з ЕМЗ МІС</summary>
public enum MatchStatus
{
    New = 0,
    /// <summary>Знайдено в МІС, НСЗУ зарахувала («Так» або «ГБ»)</summary>
    MatchedPaid = 1,
    /// <summary>Знайдено в МІС, НСЗУ відхилила («Ні») — розбіжність для виправлення</summary>
    DiscrepancyRejected = 2,
    /// <summary>Є у звіті НСЗУ, але не знайдено в МІС (внесено в іншій МІС або відсутній ehealth_id)</summary>
    MissingInMis = 3,
    /// <summary>Є у МІС (підписано, відправлено), але відсутній у звіті НСЗУ — прихована дефектура</summary>
    MissingInNhsu = 4,
}

/// <summary>Заголовок імпортованого звіту НСЗУ (.xlsx, 4 аркуші)</summary>
[Table("dsg_nszu_statement")]
public class NszuStatement : CoreEntity
{
    [Column("organization_id")] public Guid OrganizationId { get; set; }
    [Column("organization_name")] [MaxLength(500)] public string OrganizationName { get; set; } = string.Empty;
    [Column("edrpou")] [MaxLength(16)] public string Edrpou { get; set; } = string.Empty;
    [Column("report_year")] public int ReportYear { get; set; }
    [Column("report_month")] public int ReportMonth { get; set; }
    [Column("period_from")] public DateTime PeriodFrom { get; set; }
    [Column("period_to")] public DateTime PeriodTo { get; set; }
    [Column("file_name")] [MaxLength(500)] public string FileName { get; set; } = string.Empty;
    [Column("file_size_bytes")] public long FileSizeBytes { get; set; }
    [Column("imported_at")] public DateTime ImportedAt { get; set; } = DateTime.UtcNow;
    [Column("imported_by")] public Guid? ImportedBy { get; set; }
    [Column("last_emz_inserted_at")] [MaxLength(64)] public string? LastEmzInsertedAt { get; set; }
    [Column("nszu_last_review_at")] [MaxLength(64)] public string? NszuLastReviewAt { get; set; }
    [Column("generated_at")] [MaxLength(64)] public string? GeneratedAt { get; set; }

    /// <summary>Uploaded / Parsed / Tariffed / Reconciled / Failed</summary>
    [Column("status")] [MaxLength(32)] public string Status { get; set; } = "Uploaded";
    [Column("processing_log_json")] public string? ProcessingLogJson { get; set; }
    [Column("parse_duration_ms")] public long ParseDurationMs { get; set; }

    [Column("total_records")] public int TotalRecords { get; set; }
    [Column("direct_pay_records")] public int DirectPayRecords { get; set; }
    [Column("global_budget_records")] public int GlobalBudgetRecords { get; set; }
    [Column("rejected_records")] public int RejectedRecords { get; set; }
    [Column("direct_pay_amount")] public decimal DirectPayAmount { get; set; }
    [Column("global_budget_amount")] public decimal GlobalBudgetAmount { get; set; }
    [Column("lost_revenue_amount")] public decimal LostRevenueAmount { get; set; }
    [Column("recoverable_amount")] public decimal RecoverableAmount { get; set; }
    [Column("patients_rows")] public int PatientsRows { get; set; }
    [Column("report_rows")] public int ReportRows { get; set; }
    [Column("error_descriptions_rows")] public int ErrorDescriptionsRows { get; set; }

    [Column("reconciled_at")] public DateTime? ReconciledAt { get; set; }
    [Column("matched_paid_count")] public int MatchedPaidCount { get; set; }
    [Column("discrepancy_count")] public int DiscrepancyCount { get; set; }
    [Column("missing_in_mis_count")] public int MissingInMisCount { get; set; }
    [Column("missing_in_nhsu_count")] public int MissingInNhsuCount { get; set; }
    [Column("missing_in_nhsu_amount")] public decimal MissingInNhsuAmount { get; set; }
}

/// <summary>Рядок аркуша «Розшифровка» — усі 45 офіційних колонок + поля автономного розрахунку та 2-Way звірки</summary>
[Table("dsg_nszu_statement_line")]
public class NszuStatementLine : CoreEntity
{
    [Column("statement_id")] public Guid StatementId { get; set; }
    [ForeignKey(nameof(StatementId))] public virtual NszuStatement? Statement { get; set; }
    [Column("line_number")] public int LineNumber { get; set; }

    // ----- 45 колонок аркуша «Розшифровка» (нумерація згідно з офіційним файлом НСЗУ) -----
    [Column("report_year")] public int? ReportYear { get; set; }                                   // 1
    [Column("report_month")] public int? ReportMonth { get; set; }                                 // 2
    [Column("emz_type")] [MaxLength(64)] public string? EmzType { get; set; }                       // 3
    [Column("encounter_ehealth_id")] public Guid? EncounterEhealthId { get; set; }                  // 4
    [Column("ehealth_inserted_at")] public DateTime? EhealthInsertedAt { get; set; }                // 5
    [Column("practitioner_position")] [MaxLength(255)] public string? PractitionerPosition { get; set; } // 6
    [Column("practitioner_name")] [MaxLength(255)] public string? PractitionerName { get; set; }   // 7
    [Column("service_location")] [MaxLength(500)] public string? ServiceLocation { get; set; }     // 8
    [Column("referral_type")] [MaxLength(128)] public string? ReferralType { get; set; }           // 9
    [Column("referral_edrpou")] [MaxLength(32)] public string? ReferralEdrpou { get; set; }        // 10
    [Column("referral_doc_position")] [MaxLength(255)] public string? ReferralDocPosition { get; set; } // 11
    [Column("episode_id")] public Guid? EpisodeId { get; set; }                                     // 12
    [Column("episode_type")] [MaxLength(128)] public string? EpisodeType { get; set; }             // 13
    [Column("episode_start")] public DateTime? EpisodeStart { get; set; }                           // 14
    [Column("period_start")] public DateTime? PeriodStart { get; set; }                             // 15
    [Column("period_end")] public DateTime? PeriodEnd { get; set; }                                 // 16
    [Column("length_of_stay_days")] public int? LengthOfStayDays { get; set; }                     // 17
    [Column("primary_diagnosis")] [MaxLength(1000)] public string? PrimaryDiagnosis { get; set; }  // 18 (повний текст)
    [Column("primary_diag_conf_status")] [MaxLength(64)] public string? PrimaryDiagConfStatus { get; set; } // 19
    [Column("primary_diag_clin_status")] [MaxLength(64)] public string? PrimaryDiagClinStatus { get; set; } // 20
    [Column("secondary_diagnoses")] public string? SecondaryDiagnoses { get; set; }                 // 21
    [Column("rejected_diagnoses")] public string? RejectedDiagnoses { get; set; }                   // 22
    [Column("interventions")] public string? Interventions { get; set; }                           // 23
    [Column("interaction_class")] [MaxLength(128)] public string? InteractionClass { get; set; }   // 24
    [Column("priority")] [MaxLength(32)] public string? Priority { get; set; }                     // 25
    [Column("interaction_type")] [MaxLength(255)] public string? InteractionType { get; set; }     // 26
    [Column("admission_reason")] [MaxLength(255)] public string? AdmissionReason { get; set; }     // 27
    [Column("discharge_outcome")] [MaxLength(255)] public string? DischargeOutcome { get; set; }   // 28
    [Column("patient_id_hash")] [MaxLength(64)] public string? PatientIdHash { get; set; }         // 29
    [Column("has_declaration")] public bool? HasDeclaration { get; set; }                           // 30
    [Column("patient_gender")] [MaxLength(16)] public string? PatientGender { get; set; }          // 31
    [Column("patient_age")] public int? PatientAge { get; set; }                                   // 32
    [Column("additional_emz_info")] public string? AdditionalEmzInfo { get; set; }                  // 33
    [Column("adsg_code")] [MaxLength(32)] public string? AdsgCode { get; set; }                    // 34
    [Column("package_name")] [MaxLength(500)] public string? PackageName { get; set; }             // 35
    [Column("service_number")] [MaxLength(255)] public string? ServiceNumber { get; set; }         // 36
    [Column("included_in_stats")] [MaxLength(16)] public string? IncludedInStats { get; set; }     // 37
    [Column("included_in_report")] [MaxLength(16)] public string? IncludedInReport { get; set; }   // 38 (Так / ГБ / Ні)
    [Column("error_comment")] [MaxLength(1000)] public string? ErrorComment { get; set; }          // 39
    [Column("completeness_details_json")] public string? CompletenessDetailsJson { get; set; }     // 40
    [Column("verification_details")] public string? VerificationDetails { get; set; }              // 41
    [Column("grouping_conflict_details")] public string? GroupingConflictDetails { get; set; }     // 42
    [Column("nszu_review_details")] public string? NszuReviewDetails { get; set; }                 // 43
    [Column("additional_remarks")] public string? AdditionalRemarks { get; set; }                   // 44
    [Column("nszu_review_date")] public DateTime? NszuReviewDate { get; set; }                      // 45

    /// <summary>Повний масив 45 значень рядка (JSON) для інспектора колонок</summary>
    [Column("raw_payload_json")] public string? RawPayloadJson { get; set; }

    // ----- Похідні (нормалізовані) поля -----
    [Column("package_number")] [MaxLength(16)] public string? PackageNumber { get; set; }
    [Column("primary_icd10_code")] [MaxLength(16)] public string? PrimaryIcd10Code { get; set; }
    [Column("intervention_codes_json")] public string? InterventionCodesJson { get; set; }

    // ----- Автономний розрахунок тарифу (Постанова КМУ № 1808) -----
    [Column("dsg_code")] [MaxLength(64)] public string? DsgCode { get; set; }
    [Column("dsg_name")] [MaxLength(500)] public string? DsgName { get; set; }
    [Column("weight_coef")] public decimal WeightCoef { get; set; }
    [Column("tariff_model")] [MaxLength(32)] public string? TariffModel { get; set; }
    [Column("nszu_amount")] public decimal NszuAmount { get; set; }
    [Column("mis_amount")] public decimal? MisAmount { get; set; }
    [Column("difference")] public decimal? Difference { get; set; }
    [Column("lost_revenue")] public decimal LostRevenue { get; set; }
    [Column("recoverable_amount")] public decimal RecoverableAmount { get; set; }
    [Column("calculation_json")] public string? CalculationJson { get; set; }

    // ----- Класифікація помилки -----
    [Column("error_code")] [MaxLength(64)] public string? ErrorCode { get; set; }
    [Column("error_category")] [MaxLength(128)] public string? ErrorCategory { get; set; }

    // ----- 2-Way звірка з МІС -----
    [Column("matched_encounter_id")] public Guid? MatchedEncounterId { get; set; }
    [Column("matched_employee_id")] public Guid? MatchedEmployeeId { get; set; }
    [Column("matched_department_id")] public Guid? MatchedDepartmentId { get; set; }
    [Column("matched_patient_id")] public Guid? MatchedPatientId { get; set; }
    [Column("match_status")] public int MatchStatus { get; set; }
}

/// <summary>Рядок аркуша «Пацієнти» (деперсоналізований реєстр пацієнтів за пакетами)</summary>
[Table("dsg_nszu_statement_patient")]
public class NszuStatementPatient : CoreEntity
{
    [Column("statement_id")] public Guid StatementId { get; set; }
    [Column("report_year")] public int? ReportYear { get; set; }
    [Column("report_month")] public int? ReportMonth { get; set; }
    [Column("patient_id_hash")] [MaxLength(64)] public string? PatientIdHash { get; set; }
    [Column("package_name")] [MaxLength(500)] public string? PackageName { get; set; }
    [Column("package_number")] [MaxLength(16)] public string? PackageNumber { get; set; }
    [Column("service_number")] [MaxLength(255)] public string? ServiceNumber { get; set; }
    [Column("included_in_stats")] [MaxLength(16)] public string? IncludedInStats { get; set; }
    [Column("service_status")] [MaxLength(500)] public string? ServiceStatus { get; set; }
    [Column("additional_info")] public string? AdditionalInfo { get; set; }
    [Column("emz_list_json")] public string? EmzListJson { get; set; }
    [Column("matched_patient_id")] public Guid? MatchedPatientId { get; set; }
}

/// <summary>Рядок аркуша «Звіт» (зведена статистика загальна та в розрізі лікарів)</summary>
[Table("dsg_nszu_statement_report_row")]
public class NszuStatementReportRow : CoreEntity
{
    [Column("statement_id")] public Guid StatementId { get; set; }
    /// <summary>Total | Doctor</summary>
    [Column("section")] [MaxLength(16)] public string Section { get; set; } = "Total";
    [Column("doctor_name")] [MaxLength(255)] public string? DoctorName { get; set; }
    /// <summary>Package | Error</summary>
    [Column("row_kind")] [MaxLength(16)] public string RowKind { get; set; } = "Package";
    [Column("row_caption")] [MaxLength(500)] public string RowCaption { get; set; } = string.Empty;
    [Column("package_number")] [MaxLength(16)] public string? PackageNumber { get; set; }
    [Column("emz_count")] public int EmzCount { get; set; }
    [Column("patient_count")] public int? PatientCount { get; set; }
    [Column("service_count")] public int? ServiceCount { get; set; }
    [Column("percent_of_total")] public decimal? PercentOfTotal { get; set; }
    [Column("is_total_row")] public bool IsTotalRow { get; set; }
    [Column("matched_employee_id")] public Guid? MatchedEmployeeId { get; set; }
}

/// <summary>Офіційний опис помилок НСЗУ (аркуш «Опис помилок»), накопичується з усіх імпортів</summary>
[Table("dsg_nszu_error_description")]
public class NszuErrorDescription : CoreEntity
{
    [Column("section")] [MaxLength(500)] public string? Section { get; set; }
    [Column("comment_text")] [MaxLength(1000)] public string CommentText { get; set; } = string.Empty;
    [Column("description")] public string? Description { get; set; }
    [Column("mapped_error_code")] [MaxLength(64)] public string? MappedErrorCode { get; set; }
    [Column("first_seen_statement_id")] public Guid? FirstSeenStatementId { get; set; }
    [Column("occurrences")] public int Occurrences { get; set; }
}

/// <summary>Результат аудиту взаємодії (пре-білінг або пакетний імпорт) — центральна аналітична сутність</summary>
[Table("dsg_analysis_result")]
public class DsgAnalysisResult : CoreEntity
{
    [Column("encounter_id")] public Guid? EncounterId { get; set; }
    [Column("statement_line_id")] public Guid? StatementLineId { get; set; }
    [Column("organization_id")] public Guid OrganizationId { get; set; }
    [Column("package_number")] [MaxLength(16)] public string? PackageNumber { get; set; }
    [Column("dsg_group_code")] [MaxLength(32)] public string? DsgGroupCode { get; set; }
    /// <summary>0 = Валідовано, 1 = Попередження, 2 = Відхилено / ризик дефектури</summary>
    [Column("status")] public int Status { get; set; }
    [Column("tariff")] public decimal Tariff { get; set; }
    [Column("estimated_payment")] public decimal EstimatedPayment { get; set; }
    [Column("weight_coef")] public decimal WeightCoef { get; set; }
    [Column("calculation")] public string CalculationJson { get; set; } = "{}";
    [Column("findings")] public string FindingsJson { get; set; } = "[]";
    [Column("dictionary_versions")] public string? DictionaryVersionsJson { get; set; }
    [Column("request_hash")] [MaxLength(128)] public string? RequestHash { get; set; }
    /// <summary>1 = Manual / Prebilling, 2 = Background / Import</summary>
    [Column("trigger")] public int Trigger { get; set; } = 1;
    [Column("analyzed_at")] public DateTime AnalyzedAt { get; set; } = DateTime.UtcNow;
    [Column("primary_icd10_code")] [MaxLength(32)] public string? PrimaryIcd10Code { get; set; }
    [Column("employee_id")] public Guid? EmployeeId { get; set; }
    [Column("department_id")] public Guid? DepartmentId { get; set; }
}

/// <summary>Глобальні налаштування тарифів ПМГ-2026 (Постанова КМУ № 1808)</summary>
[Table("dsg_tariff_setting")]
public class DsgTariffSetting : CoreEntity
{
    [Column("base_rate")] public decimal BaseRate { get; set; } = 8735.00m;
    [Column("outpatient_base_rate")] public decimal OutpatientBaseRate { get; set; } = 155.00m;
    [Column("global_rate_share")] public decimal GlobalRateShare { get; set; } = 0.55m;
    [Column("one_day_surgery_share")] public decimal OneDaySurgeryShare { get; set; } = 0.60m;
    [Column("planned_hospitalization_coef")] public decimal PlannedHospitalizationCoef { get; set; } = 0.80m;
    [Column("mountain_coef")] public decimal MountainCoef { get; set; } = 1.25m;
    [Column("multi_surgery_coef")] public decimal MultiSurgeryCoef { get; set; } = 1.30m;
    [Column("neonatal_coef")] public decimal NeonatalCoef { get; set; } = 1.54m;
    [Column("neonatal_age_limit_years")] public int NeonatalAgeLimitYears { get; set; } = 1;
    [Column("recoverability_default_percent")] public decimal RecoverabilityDefaultPercent { get; set; } = 78m;
    [Column("valid_from")] public DateTime ValidFrom { get; set; } = new DateTime(2026, 1, 1);
    [Column("valid_to")] public DateTime? ValidTo { get; set; }
    [Column("budget_balance_coef")] public decimal BudgetBalanceCoef { get; set; } = 1.0m;
    [Column("is_active")] public bool IsActive { get; set; } = true;
}

/// <summary>Тарифна модель конкретного пакета ПМГ (для пакетів без ДСГ/класів)</summary>
[Table("dsg_package_tariff_rule")]
public class DsgPackageTariffRule : CoreEntity
{
    [Column("package_number")] [MaxLength(16)] public string PackageNumber { get; set; } = string.Empty;
    /// <summary>DSG | CLASS | FIXED | FIXED_AGE | REHAB_CYCLE | PER_WEEK | GLOBAL | NONE</summary>
    [Column("model")] [MaxLength(32)] public string Model { get; set; } = "FIXED";
    [Column("adult_rate")] public decimal AdultRate { get; set; }
    [Column("child_rate")] public decimal? ChildRate { get; set; }
    [Column("child_age_limit")] public int? ChildAgeLimit { get; set; }
    [Column("note")] [MaxLength(1000)] public string? Note { get; set; }
    [Column("source")] [MaxLength(500)] public string? Source { get; set; }
    /// <summary>Ставка нараховується один раз на пацієнта за період (курс/цикл/місяць), а не за кожен ЕМЗ</summary>
    [Column("per_patient_period")] public bool PerPatientPeriod { get; set; }
    [Column("is_active")] public bool IsActive { get; set; } = true;
}

/// <summary>Правила перевірки відповідності (FR / PK / RD) з нормативними посиланнями</summary>
[Table("dsg_rule_config")]
public class DsgRuleConfig : CoreEntity
{
    [Column("rule_code")] [MaxLength(32)] public string RuleCode { get; set; } = string.Empty;
    [Column("package_number")] [MaxLength(32)] public string? PackageNumber { get; set; }
    /// <summary>0=Info, 1=Warning, 2=Error (блокує дефектуру)</summary>
    [Column("severity")] public int Severity { get; set; }
    [Column("normative_reference")] public string? NormativeReference { get; set; }
    [Column("is_active")] public bool IsActive { get; set; } = true;
    [Column("config_params")] public string? ConfigParamsJson { get; set; }
}

/// <summary>Журнал розбіжностей (Lost Revenue) — рядки «Ні» зі звіту, звірені з ЕМЗ МІС, та прихована дефектура</summary>
[Table("dsg_nszu_discrepancy")]
public class NszuEncounterDiscrepancy : CoreEntity
{
    [Column("statement_id")] public Guid StatementId { get; set; }
    [Column("statement_line_id")] public Guid? StatementLineId { get; set; }
    [Column("encounter_id")] public Guid? EncounterId { get; set; }
    [Column("encounter_ehealth_id")] public Guid? EncounterEhealthId { get; set; }
    [Column("employee_id")] public Guid? EmployeeId { get; set; }
    [Column("department_id")] public Guid? DepartmentId { get; set; }
    [Column("patient_id")] public Guid? PatientId { get; set; }
    /// <summary>Rejected | HiddenDefektura | MissingInMis</summary>
    [Column("discrepancy_type")] [MaxLength(32)] public string DiscrepancyType { get; set; } = "Rejected";
    [Column("error_code")] [MaxLength(64)] public string? ErrorCode { get; set; }
    [Column("error_category")] [MaxLength(128)] public string? ErrorCategory { get; set; }
    [Column("nszu_comment")] [MaxLength(1000)] public string? NszuComment { get; set; }
    [Column("nszu_details")] public string? NszuDetails { get; set; }
    [Column("package_number")] [MaxLength(16)] public string? PackageNumber { get; set; }
    [Column("dsg_code")] [MaxLength(64)] public string? DsgCode { get; set; }
    [Column("primary_icd10_code")] [MaxLength(16)] public string? PrimaryIcd10Code { get; set; }
    [Column("lost_amount")] public decimal LostAmount { get; set; }
    [Column("recoverable_amount")] public decimal RecoverableAmount { get; set; }
    [Column("recommendation_json")] public string? RecommendationJson { get; set; }
    /// <summary>New | InProgress | Corrected | Resubmitted | Dismissed</summary>
    [Column("status")] [MaxLength(32)] public string Status { get; set; } = "New";
    [Column("corrected_at")] public DateTime? CorrectedAt { get; set; }
    [Column("corrected_by")] public Guid? CorrectedBy { get; set; }
    [Column("correction_json")] public string? CorrectionJson { get; set; }
}
