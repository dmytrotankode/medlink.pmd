using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MedLink.Pmg.Module.Models;

/// <summary>
/// Базовий клас сутностей МІС «Медлінк» (відповідник Core.Base.Data.CoreEntity у проєкті evomis).
/// Колонки та їх семантика повторюють конвенції PostgreSQL-схеми evomis, що дозволяє
/// перенести таблиці SQLite → PostgreSQL без змін у коді доменної моделі.
/// </summary>
public abstract class CoreEntity
{
    [Key]
    [Column("id")]
    public Guid Id { get; set; } = Guid.NewGuid();

    /// <summary>2 = Active, 4 = Deleted (конвенція evomis)</summary>
    [Column("record_state")]
    public int RecordState { get; set; } = 2;

    [Column("caption")]
    [MaxLength(255)]
    public string? Caption { get; set; }

    [Column("created_by")]
    public Guid CreatedBy { get; set; } = Guid.Empty;

    [Column("created_on")]
    public DateTime CreatedOn { get; set; } = DateTime.UtcNow;

    [Column("modified_by")]
    public Guid ModifiedBy { get; set; } = Guid.Empty;

    [Column("modified_on")]
    public DateTime? ModifiedOn { get; set; }
}
