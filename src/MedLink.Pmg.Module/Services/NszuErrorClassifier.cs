using System.Text.RegularExpressions;
using MedLink.Pmg.Module.Models;

namespace MedLink.Pmg.Module.Services;

/// <summary>
/// Класифікатор коментарів НСЗУ (колонка 39 «Коментар щодо виявлених помилок») →
/// код словника дефектури (pmg_nhsu_error_dictionary), категорія, відновлюваність та дія асистента.
/// </summary>
public class NszuErrorClassifier
{
    public record Classification(string ErrorCode, string Category, decimal RecoverabilityPercent, string Action, string Title);

    private static readonly (Regex pattern, string code, string category, decimal recover, string action, string title)[] Rules =
    {
        (new Regex("жодному пакету", RegexOptions.IgnoreCase), "ERR_NO_PKG_02", "Кодування пакету / АКПІ", 78m, "AddProcedure", "Не відповідає жодному пакету/послузі"),
        (new Regex("МВТН", RegexOptions.IgnoreCase), "ERR_MVTN_01", "Епізод / МВТН", 85m, "LinkEpisode", "Взаємодія для МВТН без клінічного епізоду"),
        (new Regex("Перекриття", RegexOptions.IgnoreCase), "ERR_MVTN_01", "Перекриття послуг", 55m, "AdjustDates", "Перекриття послуг за періодом"),
        (new Regex("частиною стаціонарного", RegexOptions.IgnoreCase), "ERR_NO_PKG_02", "Перекриття послуг", 35m, "ManualReview", "Послуга є частиною стаціонарного лікування"),
        (new Regex("Необгрунтована тривалість", RegexOptions.IgnoreCase), "ERR_STAY_TOO_SHORT_06", "Тривалість лікування", 60m, "ReclassifyPackage", "Необґрунтована тривалість лікування"),
        (new Regex("Тривалість лікування не відповідає", RegexOptions.IgnoreCase), "ERR_STAY_TOO_SHORT_06", "Тривалість лікування", 50m, "ReclassifyPackage", "Тривалість лікування не відповідає умовам закупівлі"),
        (new Regex("менше 1 доби", RegexOptions.IgnoreCase), "ERR_STAY_TOO_SHORT_06", "Тривалість лікування", 65m, "ReclassifyPackage", "Стаціонарний випадок тривалістю менше 1 доби"),
        (new Regex("умовам закупівлі на пакет", RegexOptions.IgnoreCase), "ERR_NO_PKG_02", "Умови закупівлі пакету", 45m, "ManualReview", "Не відповідає умовам закупівлі на пакет"),
        (new Regex("Помилковий запис|Entered in error", RegexOptions.IgnoreCase), "ERR_DUPLICATE_ENC_09", "Технічні записи", 0m, "RemoveDuplicate", "Помилковий запис (Entered in error)"),
        (new Regex("Дублікат", RegexOptions.IgnoreCase), "ERR_DUPLICATE_ENC_09", "Дублікат", 0m, "RemoveDuplicate", "Дублікат ЕМЗ"),
        (new Regex("Неоплачуваний тип епізоду", RegexOptions.IgnoreCase), "ERR_PRIMARY_DIAG_07", "Основний діагноз / епізод", 70m, "FixDiagnosis", "Неоплачуваний тип епізоду для даного діагнозу"),
        (new Regex("Неоплачуваний тип стаціонарної", RegexOptions.IgnoreCase), "ERR_PRIMARY_DIAG_07", "Тип взаємодії", 60m, "FixDiagnosis", "Неоплачуваний тип стаціонарної взаємодії"),
        (new Regex("не підлягає стаціонарному", RegexOptions.IgnoreCase), "ERR_PRIMARY_DIAG_07", "Основний діагноз / епізод", 50m, "ReclassifyPackage", "Пролікований випадок не підлягає стаціонарному лікуванню"),
        (new Regex("Епізод не був закритий", RegexOptions.IgnoreCase), "ERR_MVTN_01", "Епізод / МВТН", 90m, "LinkEpisode", "Епізод не був закритий"),
        (new Regex("Не за програмою ПМГ", RegexOptions.IgnoreCase), "ERR_NO_PKG_02", "Поза ПМГ", 10m, "ManualReview", "Не за програмою ПМГ"),
        (new Regex("потребують додаткової перевірки", RegexOptions.IgnoreCase), "ERR_PREBILLING_COEF_14", "Верифікація НСЗУ", 40m, "ManualReview", "Виявлені невідповідності, які потребують додаткової перевірки"),
        (new Regex("Відсутній діючий договір|договір на пакет", RegexOptions.IgnoreCase), "ERR_NO_PKG_02", "Договір з НСЗУ", 15m, "ManualReview", "Відсутній договір на пакет"),
        (new Regex("ліцензі", RegexOptions.IgnoreCase), "ERR_NO_PKG_02", "Ліцензія", 10m, "ManualReview", "Відсутня ліцензія"),
        (new Regex("Ідентифікація пацієнта", RegexOptions.IgnoreCase), "ERR_REFERRAL_REQ_10", "Пацієнт", 20m, "ManualReview", "Ідентифікація пацієнта"),
        (new Regex("минулому звітному році", RegexOptions.IgnoreCase), "ERR_NO_PKG_02", "Період", 0m, "ManualReview", "Послуга надана в минулому звітному році"),
        (new Regex("направленн", RegexOptions.IgnoreCase), "ERR_REFERRAL_REQ_10", "Направлення", 65m, "ManualReview", "Проблема з електронним направленням"),
        (new Regex("реабілітац|МКФ", RegexOptions.IgnoreCase), "ERR_REHAB_IND_08", "Реабілітація / МКФ", 75m, "AddIcfCoding", "Реабілітація: відсутнє кодування МКФ / план"),
        (new Regex("посад|спеціальн", RegexOptions.IgnoreCase), "ERR_DOC_SPEC_04", "Посада лікаря", 90m, "ChangeDoctor", "Невідповідність посади лікаря"),
        (new Regex("вік", RegexOptions.IgnoreCase), "ERR_AGE_03", "Вік пацієнта", 40m, "ManualReview", "Невідповідність віку пацієнта"),
        (new Regex("гістолог", RegexOptions.IgnoreCase), "ERR_ONCO_HISTO_11", "Онкологія", 70m, "ManualReview", "Відсутній гістологічний висновок"),
    };

    public Classification Classify(string? comment)
    {
        if (string.IsNullOrWhiteSpace(comment) || comment.Trim() == "-")
            return new Classification("", "", 0m, "", "");
        foreach (var r in Rules)
            if (r.pattern.IsMatch(comment))
                return new Classification(r.code, r.category, r.recover, r.action, r.title);
        return new Classification("ERR_NO_PKG_02", "Інше", 50m, "ManualReview", comment.Trim());
    }

    public static string Humanize(PmgNhsuErrorDictionary? e, string fallback) => e?.Title ?? fallback;
}
