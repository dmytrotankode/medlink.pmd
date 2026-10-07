using Microsoft.EntityFrameworkCore;
using MedLink.Pmg.Module.Models;

namespace MedLink.Pmg.Module.Data
{
    public class PmgDbContext : DbContext
    {
        public PmgDbContext(DbContextOptions<PmgDbContext> options) : base(options)
        {
        }

        public DbSet<NszuStatement> Statements { get; set; } = null!;
        public DbSet<NszuStatementLine> StatementLines { get; set; } = null!;
        public DbSet<MisEncounter> Encounters { get; set; } = null!;
        public DbSet<OrgEmployee> Employees { get; set; } = null!;
        public DbSet<OrgDepartment> Departments { get; set; } = null!;
        public DbSet<MisPatient> Patients { get; set; } = null!;

        public DbSet<PmgPackage> Packages { get; set; } = null!;
        public DbSet<PmgDsg> DsgCatalog { get; set; } = null!;
        public DbSet<PmgPackage9Class> Package9Classes { get; set; } = null!;
        public DbSet<PmgNhsuErrorDictionary> ErrorDictionary { get; set; } = null!;
        public DbSet<PmgServiceGroup> ServiceGroups { get; set; } = null!;
        public DbSet<PmgServiceCatalog> ServicesCatalog { get; set; } = null!;
        public DbSet<PmgServiceCombination> ServiceCombinations { get; set; } = null!;

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<NszuStatementLine>()
                .HasOne(l => l.LinkedEncounter)
                .WithMany()
                .HasForeignKey(l => l.MatchedEncounterId)
                .IsRequired(false);

            modelBuilder.Entity<NszuStatementLine>()
                .HasOne(l => l.LinkedDoctor)
                .WithMany()
                .HasForeignKey(l => l.DoctorId)
                .IsRequired(false);

            modelBuilder.Entity<NszuStatementLine>()
                .HasOne(l => l.LinkedDepartment)
                .WithMany()
                .HasForeignKey(l => l.DepartmentId)
                .IsRequired(false);
        }
    }
}
