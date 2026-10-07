// ============================================================================
// MEDLINK PMG-2026: УНІВЕРСАЛЬНИЙ ПОПАП-ПЕРЕГЛЯДАЧ ФАЙЛІВ ТА SQL ЗАПИТІВ
// ============================================================================

const EMBEDDED_FILES = {
  "01_ddl_tables.sql": {
    title: "01_ddl_tables.sql — DDL Схема таблиць (PostgreSQL 14+)",
    badge: "SQL DDL",
    path: "../sql/01_ddl_tables.sql",
    content: `-- ============================================================================
-- MEDLINK PMG-2026: DDL СХЕМА ТАБЛИЦЬ (POSTGRESQL 14+)
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.dsg_nszu_statement (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_state INTEGER NOT NULL DEFAULT 2,
    caption VARCHAR(255),
    organization_id UUID NOT NULL,
    period_from TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    period_to TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    file_name VARCHAR(500),
    imported_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (now() AT TIME ZONE 'utc')
);

CREATE TABLE IF NOT EXISTS public.dsg_nszu_statement_line (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_state INTEGER NOT NULL DEFAULT 2,
    caption VARCHAR(255),
    statement_id UUID NOT NULL REFERENCES public.dsg_nszu_statement(id) ON DELETE CASCADE,
    encounter_ehealth_id UUID,
    dsg_code VARCHAR(64),
    package_number VARCHAR(32),
    nszu_amount NUMERIC(18, 4) NOT NULL DEFAULT 0.0000,
    matched_encounter_id UUID REFERENCES public.mis_encounter(id) ON DELETE SET NULL,
    mis_amount NUMERIC(18, 4),
    difference NUMERIC(18, 4),
    match_status INTEGER NOT NULL DEFAULT 0,
    raw_payload_json JSONB
);

CREATE TABLE IF NOT EXISTS public.dsg_analysis_result (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_state INTEGER NOT NULL DEFAULT 2,
    encounter_id UUID NOT NULL REFERENCES public.mis_encounter(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL,
    package_number VARCHAR(16),
    dsg_group_code VARCHAR(32),
    status INTEGER NOT NULL DEFAULT 0,
    tariff NUMERIC(18, 4) NOT NULL DEFAULT 0.0000,
    estimated_payment NUMERIC(18, 4) NOT NULL DEFAULT 0.0000,
    weight_coef NUMERIC(18, 4) NOT NULL DEFAULT 1.0000,
    calculation JSONB NOT NULL,
    findings JSONB NOT NULL
);`
  },

  "02_queries_2way_matching.sql": {
    title: "02_queries_2way_matching.sql — Запити двостороннього звірення МІС ↔ НСЗУ",
    badge: "SQL Queries",
    path: "../sql/02_queries_2way_matching.sql",
    content: `-- 1. Двостороннє звірення ЕМЗ (2-Way Matching)
SELECT 
    l.id AS statement_line_id,
    l.encounter_ehealth_id,
    l.dsg_code AS nszu_dsg_code,
    l.nszu_amount,
    e.id AS mis_encounter_id,
    e.caption AS mis_encounter_caption,
    e.date_start,
    e.date_end,
    ar.tariff AS mis_calculated_tariff,
    ar.estimated_payment AS mis_estimated_payment,
    (COALESCE(ar.estimated_payment, 0) - l.nszu_amount) AS payment_difference,
    CASE 
        WHEN e.id IS NULL THEN 'NOT_FOUND_IN_MIS'
        WHEN l.nszu_amount = 0 AND COALESCE(ar.estimated_payment, 0) > 0 THEN 'REJECTED_BY_NSZU'
        WHEN ABS(COALESCE(ar.estimated_payment, 0) - l.nszu_amount) < 1.00 THEN 'MATCHED_EXACT'
        ELSE 'AMOUNT_MISMATCH'
    END AS reconciliation_status
FROM public.dsg_nszu_statement_line l
LEFT JOIN public.mis_encounter e ON e.ehealth_id = l.encounter_ehealth_id
LEFT JOIN public.dsg_analysis_result ar ON ar.encounter_id = e.id;`
  },

  "03_seed_pmg2026_data.sql": {
    title: "03_seed_pmg2026_data.sql — Базові тарифи та конфігурація ПМГ-2026",
    badge: "SQL Seed",
    path: "../sql/03_seed_pmg2026_data.sql",
    content: `-- Базові тарифи ПМГ-2026 (Постанова КМУ №1808)
INSERT INTO public.dsg_tariff_setting 
(id, record_state, caption, base_rate, global_rate_share, valid_from, budget_balance_coef)
VALUES 
('a6410a01-0000-4000-8000-000000000001', 2, 'Тарифи ПМГ-2026 (Постанова №1808)', 8735.0000, 0.5500, '2026-01-01 00:00:00', 1.0000)
ON CONFLICT (id) DO UPDATE 
SET base_rate = EXCLUDED.base_rate, global_rate_share = EXCLUDED.global_rate_share;`
  },

  "04_seed_dsg_catalog_465.sql": {
    title: "04_seed_dsg_catalog_465.sql — Довідник 465 ДСГ стаціонару (Постанова №1808)",
    badge: "465 ДСГ",
    path: "../sql/04_seed_dsg_catalog_465.sql",
    content: `-- Довідник 465 Діагностично-споріднених груп (ДСГ / DRG) для Пакетів 3, 4, 47
-- Базова ставка стаціонару: 8 735,00 грн. Частка глобальної ставки: 0,55 (55%)
-- Повний файл містить 465 рядків INSERT для таблиць pmg_dsg_catalog та dsg_group_weight`
  },

  "05_seed_package9_classes_148.sql": {
    title: "05_seed_package9_classes_148.sql — 148 Амбулаторних класів Пакету 9",
    badge: "148 Класів",
    path: "../sql/05_seed_package9_classes_148.sql",
    content: `-- Довідник 148 амбулаторних класів Пакету 9 (Базова ставка: 155,00 грн)
-- Напрями: Консультування (K=1.29), Діагностика (K до 7.85), Процедури (K до 11.22)
-- Повний файл містить JSON-масиви кодів АКПІ для кожного класу`
  },

  "06_seed_nhsu_error_dictionary_186.sql": {
    title: "06_seed_nhsu_error_dictionary_186.sql — 186 Помилок валідації НСЗУ",
    badge: "186 Помилок",
    path: "../sql/06_seed_nhsu_error_dictionary_186.sql",
    content: `-- Класифікатор 186 причин відхилення оплати НСЗУ (Дефектура та попередження)
-- Включає нормативне посилання, опис порушення та текст авто-рекомендації лікарю`
  },

  "07_seed_doctor_position_requirements.sql": {
    title: "07_seed_doctor_position_requirements.sql — Відповідність послуг і посад лікарів (MedProfit)",
    badge: "1 257 Послуг",
    path: "../sql/07_seed_doctor_position_requirements.sql",
    content: `-- Справочник соответствия услуг и разрешенных кодов должностей врачей (P157, P122 тощо)
-- Джерело: База medprofit (таблиці procedures та instrumental_diagnostics)
-- Використовується для запобігання відхилення звіту за помилкою ERR_DOC_SPEC`
  },

  "08_seed_laboratory_tests_408.sql": {
    title: "08_seed_laboratory_tests_408.sql — Каталог 408 Лабораторних досліджень (MedProfit)",
    badge: "408 Тестів",
    path: "../sql/08_seed_laboratory_tests_408.sql",
    content: `-- Справочник лабораторных исследований eHealth (A34xxx, A35xxx)
-- Джерело: База medprofit (таблиця laboratory_tests)`
  },

  "09_seed_medprofit_rules_185.sql": {
    title: "09_seed_medprofit_rules_185.sql — 185 Правил класифікації ОДК (MedProfit)",
    badge: "185 Правил",
    path: "../sql/09_seed_medprofit_rules_185.sql",
    content: `-- Логические правила классификации ОДК и ДСГ из базы medprofit_dsg
-- Джерело: База medprofit_dsg (таблиця dct_mp_service_odk_rule)`
  },

  "PmgTariffCalculatorService.cs": {
    title: "PmgTariffCalculatorService.cs — Математичний движок C#",
    badge: "C# Service",
    path: "../csharp/PmgTariffCalculatorService.cs",
    content: `public class PmgTariffCalculatorService : IPmgTariffCalculatorService
{
    private const decimal InpatientBaseRate = 8735.00m;
    private const decimal OutpatientBaseRate = 155.00m;
    private const decimal MountainMultiplier = 1.25m;

    public CalculationOutput CalculateInpatient(string dsgCode, decimal weightCoef, int packageNumber, bool isMountain)
    {
        var steps = new List<CalculationStepDto>();
        decimal runningTotal = InpatientBaseRate;
        steps.Add(new CalculationStepDto { Code = "BASE", Caption = "Базова ставка", Value = InpatientBaseRate, Operation = "=" });

        runningTotal *= weightCoef;
        steps.Add(new CalculationStepDto { Code = "WEIGHT", Caption = $"ВК ДСГ {dsgCode}", Value = weightCoef, Operation = "×" });

        decimal packageCoef = (packageNumber == 4) ? 0.60m : 0.55m;
        runningTotal *= packageCoef;
        steps.Add(new CalculationStepDto { Code = "SHARE", Caption = $"Частка ({packageCoef})", Value = packageCoef, Operation = "×" });

        if (isMountain)
        {
            runningTotal *= MountainMultiplier;
            steps.Add(new CalculationStepDto { Code = "MOUNTAIN", Caption = "Гірський коефіцієнт 1.25", Value = MountainMultiplier, Operation = "×" });
        }

        return new CalculationOutput { TotalTariff = Math.Round(runningTotal, 2), CalculationJson = JsonSerializer.Serialize(steps) };
    }
}`
  }
};

// Inject Modal HTML into Document
document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("codeModalOverlay")) return;

  const modalHtml = `
    <div id="codeModalOverlay" class="code-modal-overlay" style="display: none;">
      <div class="code-modal-container">
        <div class="code-modal-header">
          <div class="row-center">
            <span class="material-icons" style="color: #60a5fa; margin-right: 8px;">description</span>
            <span id="codeModalTitle" class="code-modal-title">Файл</span>
            <span id="codeModalBadge" class="code-modal-badge">SQL</span>
          </div>
          <div class="row-center">
            <button class="btn-modal-action" onclick="copyModalCode()">
              <span class="material-icons" style="font-size: 16px;">content_copy</span> Копіювати
            </button>
            <a id="codeModalDownloadBtn" href="#" download class="btn-modal-action" style="text-decoration:none;">
              <span class="material-icons" style="font-size: 16px;">download</span> Завантажити
            </a>
            <button class="btn-modal-close" onclick="closeFileModal()">✕</button>
          </div>
        </div>

        <div class="code-modal-tabs" id="codeModalTabs">
          <button class="modal-tab" onclick="openFileModal('01_ddl_tables.sql')">01_ddl_tables.sql</button>
          <button class="modal-tab" onclick="openFileModal('02_queries_2way_matching.sql')">02_queries_matching.sql</button>
          <button class="modal-tab" onclick="openFileModal('03_seed_pmg2026_data.sql')">03_seed_pmg2026.sql</button>
          <button class="modal-tab" onclick="openFileModal('04_seed_dsg_catalog_465.sql')">04_dsg_465.sql</button>
          <button class="modal-tab" onclick="openFileModal('05_seed_package9_classes_148.sql')">05_pkg9_148.sql</button>
          <button class="modal-tab" onclick="openFileModal('06_seed_nhsu_error_dictionary_186.sql')">06_errors_186.sql</button>
          <button class="modal-tab" onclick="openFileModal('07_seed_doctor_position_requirements.sql')">07_doctor_positions.sql</button>
          <button class="modal-tab" onclick="openFileModal('08_seed_laboratory_tests_408.sql')">08_lab_tests_408.sql</button>
          <button class="modal-tab" onclick="openFileModal('09_seed_medprofit_rules_185.sql')">09_rules_185.sql</button>
          <button class="modal-tab" onclick="openFileModal('PmgTariffCalculatorService.cs')">CalculatorService.cs</button>
        </div>

        <div class="code-modal-body">
          <pre><code id="codeModalContent">-- Завантаження вмісту...</code></pre>
        </div>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML("beforeend", modalHtml);

  // Close on Escape or click outside
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeFileModal();
  });
  const overlay = document.getElementById("codeModalOverlay");
  if (overlay) {
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) closeFileModal();
    });
  }
});

window.openFileModal = async function(fileKey) {
  const isDocsSubdir = window.location.pathname.includes('/docs_html/');
  const sqlPrefix = isDocsSubdir ? '../sql/' : 'sql/';
  const csPrefix = isDocsSubdir ? '../csharp/' : 'csharp/';

  const fileData = EMBEDDED_FILES[fileKey] || {
    title: fileKey,
    badge: fileKey.endsWith('.cs') ? 'C#' : 'SQL',
    path: fileKey.endsWith('.cs') ? `${csPrefix}${fileKey}` : `${sqlPrefix}${fileKey}`,
    content: `-- Файл: ${fileKey} --`
  };

  const titleEl = document.getElementById("codeModalTitle");
  const badgeEl = document.getElementById("codeModalBadge");
  const contentEl = document.getElementById("codeModalContent");
  const dlBtn = document.getElementById("codeModalDownloadBtn");

  const resolvedPath = fileData.path ? (fileData.path.startsWith('../') && !isDocsSubdir ? fileData.path.replace('../', '') : fileData.path) : `${sqlPrefix}${fileKey}`;

  if (titleEl) titleEl.textContent = fileData.title || fileKey;
  if (badgeEl) badgeEl.textContent = fileData.badge || "SQL";
  if (dlBtn) dlBtn.href = resolvedPath;
  if (contentEl) contentEl.textContent = fileData.content || "-- Завантаження вмісту... --";

  // Active tab state
  const tabs = document.querySelectorAll(".modal-tab");
  tabs.forEach(tab => {
    const txt = tab.textContent.trim();
    if (fileKey.includes(txt) || txt.includes(fileKey.split('.')[0])) {
      tab.classList.add("active");
    } else {
      tab.classList.remove("active");
    }
  });

  const overlay = document.getElementById("codeModalOverlay");
  if (overlay) overlay.style.display = "flex";

  // Live async fetch
  const fetchUrls = [resolvedPath, `${sqlPrefix}${fileKey}`, `sql/${fileKey}`, `../sql/${fileKey}`];
  for (const url of fetchUrls) {
    try {
      const resp = await fetch(url);
      if (resp.ok) {
        const fullText = await resp.text();
        if (contentEl && fullText.trim().length > 0) {
          contentEl.textContent = fullText;
          if (dlBtn) dlBtn.href = url;
          break;
        }
      }
    } catch (err) {
      // try next url
    }
  }
};

window.closeFileModal = function() {
  const overlay = document.getElementById("codeModalOverlay");
  if (overlay) overlay.style.display = "none";
};

window.copyModalCode = function() {
  const code = document.getElementById("codeModalContent").textContent;
  navigator.clipboard.writeText(code).then(() => {
    alert("Код скопійовано в буфер обміну!");
  });
};
