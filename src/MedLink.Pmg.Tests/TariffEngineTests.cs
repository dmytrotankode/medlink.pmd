using MedLink.Pmg.Module.Models;
using MedLink.Pmg.Module.Services;
using Xunit;

namespace MedLink.Pmg.Tests;

/// <summary>Формули ПМГ-2026 (Постанова КМУ № 1808) — еталонні значення з аналізу (test_suite/test_pmg_tariffs.py)</summary>
public class TariffEngineTests
{
    private static readonly PmgTariffCalculatorService Calc = new(new NullCatalogProvider());
    private static readonly DsgTariffSetting S = new();

    [Fact]
    public void Package4_InpatientSurgery_G01() =>
        Assert.Equal(24357.55m, Calc.CalculateHospitalTariff("4", 5.070m, "Ургентна", false, settings: S).Tariff);

    [Fact]
    public void Package47_OneDaySurgery_Share060() =>
        Assert.Equal(25874.82m, Calc.CalculateHospitalTariff("47", 4.937m, "Планова", false, settings: S).Tariff);

    [Fact]
    public void Package3_Neonatal_154() =>
        Assert.Equal(10727.89m, Calc.CalculateHospitalTariff("3", 1.450m, "Ургентна", false, patientAge: 0, settings: S).Tariff);

    [Fact]
    public void Package3_Planned_080_And_MultiSurgery_130()
    {
        var planned = Calc.CalculateHospitalTariff("3", 5.070m, "Планова", false, settings: S);
        Assert.Equal(19486.04m, planned.Tariff);
        var multi = Calc.CalculateHospitalTariff("3", 5.070m, "Планова", false, hasMultiSurgery: true, settings: S);
        Assert.Equal(Math.Round(19486.04m * 1.30m, 2), multi.Tariff);
        Assert.Contains(multi.Steps, s => s.Code == "PK-05");
    }

    [Fact]
    public void Package9_Class1_Cardiology() => Assert.Equal(199.95m, Calc.CalculateOutpatientTariff(1.29m, settings: S).Tariff);

    [Fact]
    public void Package9_Mountain_125() => Assert.Equal(249.94m, Calc.CalculateOutpatientTariff(1.29m, isMountain: true, settings: S).Tariff);

    [Theory]
    [InlineData("C180", "C18.0")]
    [InlineData("ICD10: C61 Злоякісне новоутворення", "C61")]
    [InlineData(" i21.0 ", "I21.0")]
    public void NormalizeIcd(string input, string expected) => Assert.Equal(expected, PmgTariffCalculatorService.NormalizeIcd(input));

    [Fact]
    public void ExtractServiceCodes_FromColumn23()
    {
        var codes = PmgTariffCalculatorService.ExtractServiceCodes("A67014 Консультація Онколога; 30061-02 Правобічна геміколектомія; 96037-00 Інше обстеження");
        Assert.Equal(new[] { "A67014", "30061-02", "96037-00" }, codes);
    }

    [Theory]
    [InlineData("9 Профілактика, діагностика", "9")]
    [InlineData("47 Хірургічні операції", "47")]
    [InlineData("-", "")]
    public void NormalizePackage(string input, string expected) => Assert.Equal(expected, PmgTariffCalculatorService.NormalizePackage(input));

    private class NullCatalogProvider : ITariffCatalogProvider
    {
        public Task<TariffCatalog> GetAsync(CancellationToken ct = default) => Task.FromResult(new TariffCatalog());
        public void Invalidate() { }
    }
}

/// <summary>Класифікатор коментарів НСЗУ (колонка 39) та матриця життєвих циклів</summary>
public class ClassifierAndWorkflowTests
{
    [Theory]
    [InlineData("Не відповідає жодному пакету/послузі", "ERR_NO_PKG_02", "AddProcedure")]
    [InlineData("Взаємодія для МВТН", "ERR_MVTN_01", "LinkEpisode")]
    [InlineData("Помилковий запис (Entered in error)", "ERR_DUPLICATE_ENC_09", "RemoveDuplicate")]
    [InlineData("Взаємодія для фіксації МКФ", "ERR_REHAB_IND_08", "AddIcfCoding")]
    public void Classify(string comment, string code, string action)
    {
        var c = new NszuErrorClassifier().Classify(comment);
        Assert.Equal(code, c.ErrorCode);
        Assert.Equal(action, c.Action);
    }

    [Fact]
    public void EncounterWorkflow()
    {
        Assert.True(Workflows.CanTransition(Workflows.Encounter, "Draft", "Signed"));
        Assert.True(Workflows.CanTransition(Workflows.Encounter, "Rejected", "Corrected"));
        Assert.True(Workflows.CanTransition(Workflows.Encounter, "Corrected", "Resubmitted"));
        Assert.False(Workflows.CanTransition(Workflows.Encounter, "Draft", "Accepted"));
        Assert.False(Workflows.CanTransition(Workflows.Discrepancy, "Closed", "New"));
        Assert.True(Workflows.CanTransition(Workflows.Resync, "Queued", "SignedKep"));
    }
}
