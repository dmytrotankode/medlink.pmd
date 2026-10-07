using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MedLink.Pmg.Module.Models;

// ============================================================================
// Сутності ядра МІС «Медлінк» (evomis), з якими інтегрується модуль ПМГ.
// У автономному режимі вони зберігаються у тій самій SQLite-базі; у бойовому
// evomis відповідні таблиці вже існують (LegalEntities, org_department,
// org_employee, mis_patient_card, mis_encounter) — тоді ці класи замінюються
// посиланнями на App.Domain.Models.* без зміни PMG-таблиць.
// ============================================================================

/// <summary>Юридична особа / заклад охорони здоров'я (evomis: LegalEntities)</summary>
[Table("org_legal_entity")]
public class OrgLegalEntity : CoreEntity
{
    [Column("edrpou")] [MaxLength(16)] public string Edrpou { get; set; } = string.Empty;
    [Column("short_name")] [MaxLength(255)] public string ShortName { get; set; } = string.Empty;
    [Column("full_name")] [MaxLength(500)] public string? FullName { get; set; }
    [Column("region")] [MaxLength(255)] public string? Region { get; set; }
    [Column("is_mountain")] public bool IsMountain { get; set; }
    [Column("ehealth_legal_entity_id")] public Guid? EhealthLegalEntityId { get; set; }
}

/// <summary>Відділення закладу (evomis: org_department)</summary>
[Table("org_department")]
public class OrgDepartment : CoreEntity
{
    [Column("legal_entity_id")] public Guid LegalEntityId { get; set; }
    [Column("code")] [MaxLength(32)] public string Code { get; set; } = string.Empty;
    [Column("name")] [MaxLength(255)] public string Name { get; set; } = string.Empty;
    [Column("department_type")] [MaxLength(64)] public string? DepartmentType { get; set; }
}

/// <summary>Співробітник / лікар (evomis: org_employee + cmn_person + ehd_dictionary посад)</summary>
[Table("org_employee")]
public class OrgEmployee : CoreEntity
{
    [Column("legal_entity_id")] public Guid LegalEntityId { get; set; }
    [Column("department_id")] public Guid? DepartmentId { get; set; }
    [Column("last_name")] [MaxLength(128)] public string LastName { get; set; } = string.Empty;
    [Column("first_name")] [MaxLength(128)] public string FirstName { get; set; } = string.Empty;
    [Column("second_name")] [MaxLength(128)] public string? SecondName { get; set; }
    [Column("full_name")] [MaxLength(400)] public string FullName { get; set; } = string.Empty;
    /// <summary>Код посади за довідником ЕСОЗ (POSITION), напр. P157 — Лікар-хірург</summary>
    [Column("position_code")] [MaxLength(16)] public string PositionCode { get; set; } = string.Empty;
    [Column("position_name")] [MaxLength(255)] public string PositionName { get; set; } = string.Empty;
    [Column("ehealth_employee_id")] public Guid? EhealthEmployeeId { get; set; }
    [Column("is_active")] public bool IsActive { get; set; } = true;
}

/// <summary>Картка пацієнта (evomis: mis_patient_card)</summary>
[Table("mis_patient_card")]
public class MisPatientCard : CoreEntity
{
    [Column("legal_entity_id")] public Guid LegalEntityId { get; set; }
    /// <summary>Унікальний код пацієнта зі звіту НСЗУ (колонка 29 — хеш)</summary>
    [Column("ehealth_patient_hash")] [MaxLength(64)] public string? EhealthPatientHash { get; set; }
    [Column("ehealth_patient_id")] public Guid? EhealthPatientId { get; set; }
    [Column("full_name")] [MaxLength(400)] public string FullName { get; set; } = string.Empty;
    [Column("rnokpp")] [MaxLength(16)] public string? Rnokpp { get; set; }
    [Column("birth_date")] public DateTime? BirthDate { get; set; }
    [Column("gender")] [MaxLength(16)] public string? Gender { get; set; }
    [Column("has_declaration")] public bool HasDeclaration { get; set; }
}

/// <summary>Електронний медичний запис / взаємодія (evomis: mis_encounter / App.Domain.Models.Encounter)</summary>
[Table("mis_encounter")]
public class MisEncounter : CoreEntity
{
    [Column("legal_entity_id")] public Guid LegalEntityId { get; set; }
    /// <summary>UUID ЕМЗ у центральному компоненті eHealth — ключ 2-Way звірки (колонка 4 звіту)</summary>
    [Column("ehealth_id")] public Guid? EhealthId { get; set; }
    [Column("episode_id")] public Guid? EpisodeId { get; set; }
    [Column("patient_id")] public Guid? PatientId { get; set; }
    [Column("employee_id")] public Guid? EmployeeId { get; set; }
    [Column("department_id")] public Guid? DepartmentId { get; set; }
    /// <summary>Взаємодія / Діагностичний звіт / Процедура</summary>
    [Column("emz_type")] [MaxLength(64)] public string EmzType { get; set; } = "Взаємодія";
    [Column("encounter_class")] [MaxLength(128)] public string? EncounterClass { get; set; }
    [Column("encounter_type")] [MaxLength(128)] public string? EncounterType { get; set; }
    [Column("priority")] [MaxLength(32)] public string? Priority { get; set; }
    [Column("date_start")] public DateTime? DateStart { get; set; }
    [Column("date_end")] public DateTime? DateEnd { get; set; }
    [Column("length_of_stay_days")] public int? LengthOfStayDays { get; set; }
    [Column("primary_icd10_code")] [MaxLength(16)] public string? PrimaryIcd10Code { get; set; }
    [Column("primary_icd10_name")] [MaxLength(500)] public string? PrimaryIcd10Name { get; set; }
    /// <summary>JSON-масив кодів супутніх діагнозів</summary>
    [Column("secondary_diagnoses_json")] public string? SecondaryDiagnosesJson { get; set; }
    /// <summary>JSON-масив кодів інтервенцій АКПІ (ACHI)</summary>
    [Column("interventions_json")] public string? InterventionsJson { get; set; }
    [Column("package_number")] [MaxLength(16)] public string? PackageNumber { get; set; }
    [Column("service_number")] [MaxLength(128)] public string? ServiceNumber { get; set; }
    [Column("patient_age")] public int? PatientAge { get; set; }
    [Column("patient_gender")] [MaxLength(16)] public string? PatientGender { get; set; }
    /// <summary>Draft / Signed / Submitted / Corrected / Resubmitted</summary>
    [Column("status")] [MaxLength(32)] public string Status { get; set; } = "Signed";
    [Column("is_signed")] public bool IsSigned { get; set; } = true;
    [Column("signed_at")] public DateTime? SignedAt { get; set; }
    [Column("coding_corrected")] public bool CodingCorrected { get; set; }
    [Column("corrected_at")] public DateTime? CorrectedAt { get; set; }
    [Column("correction_note")] public string? CorrectionNote { get; set; }
}

/// <summary>Черга повторної синхронізації ЕМЗ з ЕСОЗ після коригування (evomis: ehe_* домен)</summary>
[Table("ehe_resync_queue")]
public class EheResyncQueue : CoreEntity
{
    [Column("encounter_id")] public Guid EncounterId { get; set; }
    [Column("discrepancy_id")] public Guid? DiscrepancyId { get; set; }
    [Column("reason")] [MaxLength(500)] public string Reason { get; set; } = string.Empty;
    /// <summary>Queued / SignedKep / Sent / Accepted / Failed</summary>
    [Column("status")] [MaxLength(32)] public string Status { get; set; } = "Queued";
    [Column("payload_json")] public string? PayloadJson { get; set; }
    [Column("attempts")] public int Attempts { get; set; }
    [Column("sent_at")] public DateTime? SentAt { get; set; }
    [Column("last_error")] public string? LastError { get; set; }
}
