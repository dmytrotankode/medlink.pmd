using MedLink.Pmg.Module.Models;
using Microsoft.EntityFrameworkCore;

namespace MedLink.Pmg.Module.Data;

/// <summary>
/// EF Core контекст модуля ПМГ-2026. У автономному режимі — SQLite; у evomis — ті самі
/// DbSet-и додаються до ApplicationDbContext (PostgreSQL, провайдер Npgsql) без зміни мапінгів.
/// </summary>
public class PmgDbContext : DbContext
{
    public PmgDbContext(DbContextOptions<PmgDbContext> options) : base(options) { }

    // --- Ядро МІС «Медлінк» ---
    public DbSet<OrgLegalEntity> LegalEntities => Set<OrgLegalEntity>();
    public DbSet<OrgDepartment> Departments => Set<OrgDepartment>();
    public DbSet<OrgEmployee> Employees => Set<OrgEmployee>();
    public DbSet<MisPatientCard> Patients => Set<MisPatientCard>();
    public DbSet<MisEncounter> Encounters => Set<MisEncounter>();
    public DbSet<EheResyncQueue> ResyncQueue => Set<EheResyncQueue>();

    // --- Домен dsg_* ---
    public DbSet<NszuStatement> Statements => Set<NszuStatement>();
    public DbSet<NszuStatementLine> StatementLines => Set<NszuStatementLine>();
    public DbSet<NszuStatementPatient> StatementPatients => Set<NszuStatementPatient>();
    public DbSet<NszuStatementReportRow> StatementReportRows => Set<NszuStatementReportRow>();
    public DbSet<NszuErrorDescription> ErrorDescriptions => Set<NszuErrorDescription>();
    public DbSet<DsgAnalysisResult> AnalysisResults => Set<DsgAnalysisResult>();
    public DbSet<DsgTariffSetting> TariffSettings => Set<DsgTariffSetting>();
    public DbSet<DsgPackageTariffRule> PackageTariffRules => Set<DsgPackageTariffRule>();
    public DbSet<DsgRuleConfig> RuleConfigs => Set<DsgRuleConfig>();
    public DbSet<NszuEncounterDiscrepancy> Discrepancies => Set<NszuEncounterDiscrepancy>();

    // --- Довідники pmg_* ---
    public DbSet<PmgPackage> Packages => Set<PmgPackage>();
    public DbSet<PmgDsg> Dsg => Set<PmgDsg>();
    public DbSet<PmgDsgDiagnosis> DsgDiagnoses => Set<PmgDsgDiagnosis>();
    public DbSet<PmgDsgService> DsgServices => Set<PmgDsgService>();
    public DbSet<PmgIcd10> Icd10 => Set<PmgIcd10>();
    public DbSet<PmgAchi> Achi => Set<PmgAchi>();
    public DbSet<PmgPackage9Class> Package9Classes => Set<PmgPackage9Class>();
    public DbSet<PmgPackage9ClassService> Package9ClassServices => Set<PmgPackage9ClassService>();
    public DbSet<PmgPackage9ClassDiagnosis> Package9ClassDiagnoses => Set<PmgPackage9ClassDiagnosis>();
    public DbSet<PmgPackage9ClassPosition> Package9ClassPositions => Set<PmgPackage9ClassPosition>();
    public DbSet<PmgRehabGroup> RehabGroups => Set<PmgRehabGroup>();
    public DbSet<PmgRehabRule> RehabRules => Set<PmgRehabRule>();
    public DbSet<PmgRehabDiagnosis> RehabDiagnoses => Set<PmgRehabDiagnosis>();
    public DbSet<PmgRehabService> RehabServices => Set<PmgRehabService>();
    public DbSet<PmgNhsuErrorDictionary> ErrorDictionary => Set<PmgNhsuErrorDictionary>();
    public DbSet<PmgServiceDoctorPosition> ServiceDoctorPositions => Set<PmgServiceDoctorPosition>();
    public DbSet<PmgLaboratoryCatalog> LaboratoryCatalog => Set<PmgLaboratoryCatalog>();
    public DbSet<PmgClassificationRule> ClassificationRules => Set<PmgClassificationRule>();
    public DbSet<PmgServiceGroup> ServiceGroups => Set<PmgServiceGroup>();
    public DbSet<PmgServiceCatalog> ServiceCatalog => Set<PmgServiceCatalog>();
    public DbSet<PmgServiceCombination> ServiceCombinations => Set<PmgServiceCombination>();
    public DbSet<PmgCombinationLibrary> CombinationLibrary => Set<PmgCombinationLibrary>();

    protected override void OnModelCreating(ModelBuilder mb)
    {
        base.OnModelCreating(mb);

        // Composite keys of link tables
        mb.Entity<PmgDsgDiagnosis>().HasKey(x => new { x.PackageNumber, x.DsgId, x.DiagCode });
        mb.Entity<PmgDsgDiagnosis>().HasIndex(x => x.DiagCode).HasDatabaseName("idx_pmg_dsg_diag_code");
        mb.Entity<PmgDsgService>().HasKey(x => new { x.PackageNumber, x.DsgId, x.ServiceCode });
        mb.Entity<PmgDsgService>().HasIndex(x => x.ServiceCode).HasDatabaseName("idx_pmg_dsg_service_code");
        mb.Entity<PmgPackage9ClassService>().HasKey(x => new { x.ClassId, x.ServiceCode });
        mb.Entity<PmgPackage9ClassService>().HasIndex(x => x.ServiceCode).HasDatabaseName("idx_pmg_p9_service_code");
        mb.Entity<PmgPackage9ClassDiagnosis>().HasKey(x => new { x.ClassId, x.DiagCode });
        mb.Entity<PmgPackage9ClassDiagnosis>().HasIndex(x => x.DiagCode).HasDatabaseName("idx_pmg_p9_diag_code");
        mb.Entity<PmgPackage9ClassPosition>().HasKey(x => new { x.ClassId, x.PositionCode });

        mb.Entity<PmgDsg>().HasIndex(x => new { x.PackageNumber, x.DsgCode }).HasDatabaseName("idx_pmg_dsg_pkg_code");
        mb.Entity<PmgPackage9Class>().HasIndex(x => x.ClassNumber).HasDatabaseName("idx_pmg_p9_class_number");
        mb.Entity<PmgRehabDiagnosis>().HasIndex(x => x.DiagCode).HasDatabaseName("idx_pmg_rehab_diag_code");
        mb.Entity<PmgNhsuErrorDictionary>().HasIndex(x => x.ErrorCode).IsUnique().HasDatabaseName("idx_pmg_error_code");
        mb.Entity<PmgServiceDoctorPosition>().HasIndex(x => x.ServiceCode).HasDatabaseName("idx_pmg_pos_service_code");
        mb.Entity<PmgLaboratoryCatalog>().HasIndex(x => x.TestCode).HasDatabaseName("idx_pmg_lab_code");
        mb.Entity<PmgServiceCombination>().HasIndex(x => x.ServiceCode).HasDatabaseName("idx_pmg_comb_service");

        // Core MedLink indexes
        mb.Entity<MisEncounter>().HasIndex(x => x.EhealthId).HasDatabaseName("idx_mis_encounter_ehealth_id");
        mb.Entity<MisEncounter>().HasIndex(x => new { x.LegalEntityId, x.DateStart }).HasDatabaseName("idx_mis_encounter_org_date");
        mb.Entity<MisEncounter>().HasIndex(x => x.EmployeeId).HasDatabaseName("idx_mis_encounter_employee");
        mb.Entity<MisPatientCard>().HasIndex(x => x.EhealthPatientHash).HasDatabaseName("idx_mis_patient_hash");
        mb.Entity<OrgEmployee>().HasIndex(x => new { x.LegalEntityId, x.FullName }).HasDatabaseName("idx_org_employee_org_name");

        // dsg_* indexes (as in 01_ddl_tables.sql)
        mb.Entity<NszuStatement>().HasIndex(x => new { x.OrganizationId, x.PeriodFrom, x.PeriodTo }).HasDatabaseName("idx_dsg_nszu_stmt_org_period");
        mb.Entity<NszuStatementLine>().HasIndex(x => x.StatementId).HasDatabaseName("idx_dsg_nszu_stmt_line_stmt_id");
        mb.Entity<NszuStatementLine>().HasIndex(x => x.EncounterEhealthId).HasDatabaseName("idx_dsg_nszu_stmt_line_eh_id");
        mb.Entity<NszuStatementLine>().HasIndex(x => x.MatchedEncounterId).HasDatabaseName("idx_dsg_nszu_stmt_line_matched_enc");
        mb.Entity<NszuStatementLine>().HasIndex(x => new { x.StatementId, x.IncludedInReport }).HasDatabaseName("idx_dsg_nszu_stmt_line_status");
        mb.Entity<NszuStatementLine>().HasOne(x => x.Statement).WithMany().HasForeignKey(x => x.StatementId).OnDelete(DeleteBehavior.Cascade);
        mb.Entity<NszuStatementPatient>().HasIndex(x => x.StatementId).HasDatabaseName("idx_dsg_nszu_stmt_patient_stmt");
        mb.Entity<NszuStatementReportRow>().HasIndex(x => x.StatementId).HasDatabaseName("idx_dsg_nszu_stmt_report_stmt");
        mb.Entity<NszuErrorDescription>().HasIndex(x => x.CommentText).HasDatabaseName("idx_dsg_nszu_err_desc_text");
        mb.Entity<DsgAnalysisResult>().HasIndex(x => x.EncounterId).HasDatabaseName("idx_dsg_analysis_enc_id");
        mb.Entity<DsgAnalysisResult>().HasIndex(x => new { x.EmployeeId, x.DepartmentId }).HasDatabaseName("idx_dsg_analysis_emp_dept");
        mb.Entity<NszuEncounterDiscrepancy>().HasIndex(x => x.StatementId).HasDatabaseName("idx_dsg_discrepancy_stmt");
        mb.Entity<NszuEncounterDiscrepancy>().HasIndex(x => x.EncounterId).HasDatabaseName("idx_dsg_discrepancy_enc");
        mb.Entity<NszuEncounterDiscrepancy>().HasIndex(x => x.Status).HasDatabaseName("idx_dsg_discrepancy_status");
        mb.Entity<DsgPackageTariffRule>().HasIndex(x => x.PackageNumber).HasDatabaseName("idx_dsg_pkg_rule_pkg");

        // decimal → REAL in SQLite / numeric(18,4) in PostgreSQL
        foreach (var entity in mb.Model.GetEntityTypes())
        {
            foreach (var prop in entity.GetProperties())
            {
                if (prop.ClrType == typeof(decimal) || prop.ClrType == typeof(decimal?))
                    prop.SetPrecision(18);
                if (prop.ClrType == typeof(decimal) || prop.ClrType == typeof(decimal?))
                    prop.SetScale(4);
            }
        }
    }
}
