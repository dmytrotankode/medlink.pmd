import os
import shutil
import zipfile

bundle_dir = r"c:\__MEDLINK___\PMG\medlink_pmg_bundle"
if os.path.exists(bundle_dir):
    shutil.rmtree(bundle_dir)
os.makedirs(bundle_dir, exist_ok=True)

# 1. Copy prototype_medlink
shutil.copytree(r"c:\__MEDLINK___\PMG\prototype_medlink", os.path.join(bundle_dir, "prototype_medlink"))

# 2. Copy components (including PmgPackagesCatalog.vue)
shutil.copytree(r"c:\__MEDLINK___\PMG\prototype_medlink\components", os.path.join(bundle_dir, "components"))

# 3. Copy docs_html (all 9 chapters, index, and modal viewer)
shutil.copytree(r"c:\__MEDLINK___\PMG\docs_html", os.path.join(bundle_dir, "docs_html"))

# 4. Copy normative_packages (all 12 HTML dossiers + manifest + index)
shutil.copytree(r"c:\__MEDLINK___\PMG\normative_packages", os.path.join(bundle_dir, "normative_packages"))

# 5. Copy normative PDFs
normative_docs_src = r"c:\__MEDLINK___\PMG\extracted_data\normative_docs"
if os.path.exists(normative_docs_src):
    shutil.copytree(normative_docs_src, os.path.join(bundle_dir, "normative_docs"))

# 6. Copy sql (all 10 scripts)
shutil.copytree(r"c:\__MEDLINK___\PMG\sql", os.path.join(bundle_dir, "sql"))

# 7. Copy pre-seeded SQLite database & standalone API server
shutil.copy2(r"c:\__MEDLINK___\PMG\pmg_database.sqlite", os.path.join(bundle_dir, "pmg_database.sqlite"))
shutil.copy2(r"c:\__MEDLINK___\PMG\serve.py", os.path.join(bundle_dir, "serve.py"))
shutil.copy2(r"c:\__MEDLINK___\PMG\TZ_MedLink_PMG_Analytics.html", os.path.join(bundle_dir, "TZ_MedLink_PMG_Analytics.html"))

# 8. Create csharp folder and populate files
csharp_dir = os.path.join(bundle_dir, "csharp")
os.makedirs(csharp_dir, exist_ok=True)

# Write C# Entities
with open(os.path.join(csharp_dir, "NszuStatementEntities.cs"), "w", encoding="utf-8") as f:
    f.write('''using System;
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
''')

# Write C# Service
with open(os.path.join(csharp_dir, "PmgTariffCalculatorService.cs"), "w", encoding="utf-8") as f:
    f.write('''using System;
using System.Collections.Generic;
using System.Text.Json;

namespace App.Business.Services.Pmg
{
    public class PmgTariffCalculatorService
    {
        private const decimal InpatientBaseRate = 8735.00m;
        private const decimal OutpatientBaseRate = 155.00m;
        private const decimal MountainMultiplier = 1.25m;

        public decimal CalculateInpatient(string dsgCode, decimal weightCoef, int packageNumber, bool isMountain)
        {
            decimal rate = InpatientBaseRate * weightCoef;
            decimal coef = (packageNumber == 4) ? 0.60m : 0.55m;
            decimal tariff = rate * coef;
            if (isMountain) tariff *= MountainMultiplier;
            return Math.Round(tariff, 2);
        }

        public decimal CalculateOutpatient(int classNumber, decimal classCoef, bool isMountain)
        {
            decimal tariff = OutpatientBaseRate * classCoef;
            if (isMountain) tariff *= MountainMultiplier;
            return Math.Round(tariff, 2);
        }
    }
}
''')

# 9. Copy sample Excel reports
sample_dir = os.path.join(bundle_dir, "sample_reports")
os.makedirs(sample_dir, exist_ok=True)
if os.path.exists(r"c:\__MEDLINK___\PMG\Вересень 26.xlsx"):
    shutil.copy2(r"c:\__MEDLINK___\PMG\Вересень 26.xlsx", os.path.join(sample_dir, "Вересень 26.xlsx"))
if os.path.exists(r"c:\__MEDLINK___\PMG\02000334_SF_2026_08_20260910.xlsx"):
    shutil.copy2(r"c:\__MEDLINK___\PMG\02000334_SF_2026_08_20260910.xlsx", os.path.join(sample_dir, "02000334_SF_2026_08_20260910.xlsx"))

# 10. Write comprehensive master README.md in bundle
readme_content = """# ПАКЕТ ІНТЕГРАЦІЇ МОДУЛЯ ПМГ-2026 ТА АУДИТУ ЗВІТІВ НСЗУ В МІС «МЕДЛІНК»

Цей каталог містить повний набір програмного забезпечення, інтерактивних веб-прототипів, нормативних досьє на всі 46 пакетів, бази даних SQLite, C# моделей, SQL-скриптів та реальних звітів НСЗУ для МІС «Медлінк» (`evomis`).

---

## Структура папки та основні файли

### 1. `prototype_medlink/` — Інтерактивний веб-прототип (Zero-Auth, Quasar 1.15.3, Vue 2)
* `index.html` — повнофункціональний додаток у точній стилістиці та палітрі МІС «Медлінк» (`#4274A7`):
  * **Крок 1**: Імпорт OpenXML та SAX-парсер великих звітів без OutOfMemory.
  * **Крок 2**: Аудит 45 колонок звіту НСЗУ та автономний розрахунок тарифів Постанови № 1808.
  * **Крок 3**: Двостороння 2-Way звірка з виявленням «Прихованої дефектури» (Invisible Defektura).
  * **Крок 4**: Журнал 186 відхилених помилок дефектури та відновлення виплат (+24 357.55 ₴).
  * **Крок 5**: Зведений аналітичний звіт керівництва за лікарями та відділеннями (аналог аркуша «Звіт»).
  * **Крок 6**: АРМ лікаря — віджет пре-білінгу у формі взаємодії та блокування дефектури (Anti-Defektura).
  * **Крок 7**: Нормативно-довідковий модуль — **всі 46 пакетів ПМГ-2026**, 465 ДСГ, 148 класів, 186 помилок.
  * Інтерактивні іконки `info` біля номерів кожного пакета з відкриттям детального нормативного досьє.
* `data.js` — масиви реальних звітів (5 490 ЕМЗ Черкаського онкоцентру та 4 394 ЕМЗ Волинської дитячої лікарні) та повний реєстр 46 пакетів.
* `medlink_small.svg` — векторний фірмовий логотип МІС «Медлінк».

### 2. `components/` — 9 готових Single-File Components для `evomis/src/App.View`
1. `PmgPackagesCatalog.vue` — **класифікатор усіх 46 медичних пакетів ПМГ-2026** з пошуком, фільтрами категорій, формулами та нормативними досьє.
2. `PmgAuditDashboard.vue` — таблиця аудиту 45 колонок та тарифікації.
3. `PmgReportImport.vue` — інтерфейс потокового імпорту звітів НСЗУ (OpenXML).
4. `PmgDiscrepanciesJournal.vue` — журнал відхилених записів (Lost Revenue) та 2-Way виправлення.
5. `PmgDoctorsReport.vue` — звіт за лікарями та відділеннями (аналог аркуша «Звіт»).
6. `PmgEncounterPrebillingDialog.vue` — калькулятор пре-білінгу для робочого місця лікаря (`EncounterEdit.vue`).
7. `PmgDsgClassifier.vue` — класифікатор 465 стаціонарних ДСГ.
8. `PmgOutpatientClasses.vue` — класифікатор 148 амбулаторних класів (Пакет 9).
9. `PmgErrorDictionary.vue` — база знань 186 кодів помилок НСЗУ з алгоритмами усунення.

### 3. `normative_packages/` — Нормативно-правова бібліотека всіх 46 пакетів ПМГ-2026
* `all_packages_manifest.json` — машиночитний майстер-маніфест усіх 46 пакетів з формулами, коефіцієнтами, статтями Постанови № 1808 та eHealth валідаціями.
* `index.html` — інтерактивний автономний пошуковий каталог та фільтр 12 кластерів.
* 12 категоризованих HTML-досьє:
  * `01_primary_care.html` — Пакет 1 (ПМД, капітація 1 007.30 ₴/рік).
  * `02_emergency_care.html` — Пакет 2 (ЕМД, капітація 340.50 ₴/рік).
  * `03_specialized_surgery_and_therapy_dsg.html` — Пакети 3, 4, 47 (база 8 735 ₴, 465 ДСГ).
  * `04_priority_stroke_infarct_maternity.html` — Пакети 5 (Інсульт), 6 (Інфаркт), 7 (Пологи), 8 (Неонатологія), 35 (Вагітність).
  * `05_ambulatory_outpatient_and_screening.html` — Пакети 9 (148 класів), 10..15 (6 скринінгів), 16, 34 (Стоматологія), 42.
  * `06_oncology_and_hematology.html` — Пакети 18 (Хіміотерапія), 19 (Радіологія), 26 (Онкогематологія).
  * `07_rehabilitation_care.html` — Пакети 25, 53 (Стаціонарна), 54 (Амбулаторна).
  * `08_palliative_care.html` — Пакети 23 (Стаціонарна), 24 (Мобільна).
  * `09_psychiatry_and_addiction.html` — Пакети 22, 27 (Мобільна), 28 (ЗПТ), 30 (Первинка).
  * `10_infectious_tb_hiv.html` — Пакети 20 (Туберкульоз), 21 (ВІЛ/СНІД), 29 (Гепатити).
  * `11_high_tech_art_transplant.html` — Пакети 43 (Гемодіаліз), 46, 59 (ДРТ), 60 (Органи), 61 (ТКМ).
  * `12_defense_readiness_vlk.html` — Пакети 40 (Готовність), 41 (НС), 44 (ВЛК: 883 ₴), 45, 58 (Ветерани: 14 984 ₴).

### 4. `normative_docs/` — Офіційні першоджерела НСЗУ (PDF)
* `pmg-2026.pdf` — повний текст Постанови КМУ від 31.12.2025 № 1808 зі змінами (43 сторінки).
* `Додаток-1.pdf` — офіційна таблиця 465 ДСГ та вагових коефіцієнтів (35 сторінок).
* `Додаток-2.pdf` — перелік медичних послуг хірургії одного дня (Пакет 47, 5 сторінок).

### 5. `docs_html/` — Багатороздільна технічна документація та ТЗ (з попап-переглядачем)
* `index.html` — головний портал технічного завдання.
* `01_database_schema.html` — специфікація БД, моделі EF Core та зв'язки з `mis_encounter`.
* `02_api_endpoints.html` — специфікація REST API ендпоінтів контролерів.
* `03_business_logic_and_math.html` — математичний движок Постанови КМУ № 1808.
* `04_openxml_processor.html` — високопродуктивний процесор OpenXML (SAX streaming).
* `05_frontend_integration_guide.html` — покроковий посібник фронтенд-розробника.
* `06_pmg_dictionaries_catalog.html` — довідники ПМГ-2026, аудит MedProfit та перелік SQL-пакетів.
* `07_nszu_file_analysis_literal_compliance.html` — послівний аудит відповідності вимогам info-pmg.com та регламент 7 процесів.
* `08_medlink_existing_ui_augmentation_guide.html` — посібник безшовного доповнення існуючих форм МІС «Медлінк».
* `09_all_pmg_packages_normative_guide.html` — повний реєстр, нормативне регулювання, тарифи та формули всіх 46 пакетів ПМГ-2026.
* `modal_viewer.js` та `modal_viewer.css` — скрипт та стилі великого модального вікна для перегляду DDL, довідників та запитів.

### 6. `sql/` — DDL схеми таблиць, виробничі запити та 7 довідників ПМГ-2026
* `01_ddl_tables.sql` — повний DDL для таблиць `dsg_nszu_statement`, `dsg_nszu_statement_line`, `dsg_analysis_result` тощо.
* `02_queries_2way_matching.sql` — SQL-запити 2-Way звірки за `ehealth_id`, розрахунку тарифів та дефектури.
* `03_seed_pmg2026_data.sql` — базові тарифи ПМГ-2026 (ставка 8 735 ₴) та конфігурація правил валідації.
* `04_seed_dsg_catalog_465.sql` — довідник 465 ДСГ стаціонару (Постанова № 1808, базова ставка 8 735 ₴).
* `05_seed_package9_classes_148.sql` — довідник 148 амбулаторних класів Пакету 9 з кодами АКПІ інтервенцій.
* `06_seed_nhsu_error_dictionary_186.sql` — довідник 186 помилок дефектури НСЗУ з нормативними статтями та порадами.
* `07_seed_doctor_position_requirements.sql` — вимоги до посад лікарів (P157, P122) для 1 257 послуг (MedProfit Anti-Defektura).
* `08_seed_laboratory_tests_408.sql` — каталог 408 лабораторних тестів (A34xxx, A35xxx) з MedProfit.
* `09_seed_medprofit_rules_185.sql` — 185 правил класифікації ОДК з бази medprofit_dsg.
* `10_seed_all_pmg2026_packages.sql` — **повний реєстр усіх 46 пакетів ПМГ-2026** із тарифами, формулами та валідаціями.

### 7. `pmg_database.sqlite` та `serve.py` — Локальна робоча база та REST API сервер
* `pmg_database.sqlite` — робоча локальна SQL база даних з попередньо заповненими 46 пакетами, 465 ДСГ, 148 класами, 186 помилками, 1 257 вимогами до посад та зразками ЕМЗ.
* `serve.py` — автономний HTTP сервер на Python з повним набором REST API ендпоінтів (`/api/v1/pmg/...`).

### 8. `csharp/` — Вихідні C# файли для бекенду `App.Domain` та `App.Business`
* `NszuStatementEntities.cs` — сутності Entity Framework Core (`NszuStatement`, `NszuStatementLine`, `PmgPackage`).
* `PmgTariffCalculatorService.cs` — сервіс розрахунку вартості за формулами КМУ.

### 9. `sample_reports/` — Зразки реальних звітів 2026 року
* `Вересень 26.xlsx` — звіт онкологічного закладу (5 490 ЕМЗ, 4 аркуші, 45 колонок).
* `02000334_SF_2026_08_20260910.xlsx` — звіт дитячої лікарні (4 394 ЕМЗ).

---

## Швидкий запуск та тестування

1. Запустіть автономний REST API сервер:
   ```bash
   python serve.py
   ```
   Сервер запуститься на `http://localhost:8085` та надасть REST API з підтримкою SQLite.

2. Відкрийте прототип у браузері:
   * **Головний прототип MedLink Quasar**: http://localhost:8085/prototype_medlink/index.html
   * **Технічне завдання (9 розділів)**: http://localhost:8085/docs_html/index.html
   * **Браузер усіх 46 пакетів ПМГ**: http://localhost:8085/normative_packages/index.html
   * **Зведене ТЗ**: http://localhost:8085/TZ_MedLink_PMG_Analytics.html
"""

with open(os.path.join(bundle_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_content)

# 11. Create ZIP archive
zip_path = r"c:\__MEDLINK___\PMG\medlink_pmg_complete.zip"
if os.path.exists(zip_path):
    os.remove(zip_path)

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(bundle_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, bundle_dir)
            zipf.write(file_path, arcname)

print(f"Archive successfully created: {zip_path} (Size: {os.path.getsize(zip_path):,} bytes)")
