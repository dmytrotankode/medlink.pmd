using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Core.Base.Data;

namespace App.Domain.Models.dsg
{
    [Table("dsg_nszu_statement")]
    public class NszuStatement : CoreEntity
    {
        [Column("organization_id")]
        public Guid OrganizationId { get; set; }

        [Column("period_from")]
        public DateTime PeriodFrom { get; set; }

        [Column("period_to")]
        public DateTime PeriodTo { get; set; }

        [Column("file_name")]
        [MaxLength(500)]
        public string FileName { get; set; }

        [Column("imported_at")]
        public DateTime ImportedAt { get; set; } = DateTime.UtcNow;

        [Column("imported_by")]
        public Guid? ImportedBy { get; set; }
    }

    [Table("dsg_nszu_statement_line")]
    public class NszuStatementLine : CoreEntity
    {
        [Column("statement_id")]
        public Guid StatementId { get; set; }

        [Column("encounter_ehealth_id")]
        public Guid? EncounterEhealthId { get; set; }

        [Column("matched_encounter_id")]
        public Guid? MatchedEncounterId { get; set; }

        [Column("dsg_code")]
        [MaxLength(64)]
        public string DsgCode { get; set; }

        [Column("package_number")]
        [MaxLength(32)]
        public string PackageNumber { get; set; }

        [Column("nszu_amount")]
        public decimal NszuAmount { get; set; }

        [Column("mis_amount")]
        public decimal? MisAmount { get; set; }

        [Column("difference")]
        public decimal? Difference { get; set; }

        [Column("match_status")]
        public int MatchStatus { get; set; }

        [ForeignKey("StatementId")]
        public virtual NszuStatement Statement { get; set; }
    }

    [Table("pmg_packages")]
    public class PmgPackage
    {
        [Key]
        [Column("package_id")]
        [MaxLength(10)]
        public string PackageId { get; set; } = string.Empty;

        [Required]
        [Column("name")]
        [MaxLength(255)]
        public string Name { get; set; } = string.Empty;

        [Column("base_rate")]
        public decimal BaseRate { get; set; }

        [Column("meta_json")]
        public string? MetaJson { get; set; }
    }
}
