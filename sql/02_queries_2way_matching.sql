-- ============================================================================
-- MEDLINK PMG-2026: РЕЄСТР ОСНОВНИХ SQL ЗАПИТІВ ДЛЯ АНАЛІТИКИ ТА ЗВІРКИ
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. ЗАПИТ 2-WAY ЗВІРКИ: СПІВСТАВЛЕННЯ ЗВІТУ НСЗУ З ТАБЛИЦЕЮ ВЗАЄМОДІЙ МІС
-- ----------------------------------------------------------------------------
-- Співставляє колонку 4 звіту (encounter_ehealth_id) із mis_encounter.ehealth_id
-- та встановлює локальний ключ matched_encounter_id і статус 'Звірено' (1)
UPDATE public.dsg_nszu_statement_line sl
SET 
    matched_encounter_id = e.id,
    match_status = 1,
    modified_on = (now() AT TIME ZONE 'utc')
FROM public.mis_encounter e
WHERE sl.encounter_ehealth_id = e.ehealth_id
  AND sl.statement_id = :statementId;

-- Маркування записів, яких немає в МІС (незареєстровані або сторонні ЕМЗ)
UPDATE public.dsg_nszu_statement_line
SET match_status = 2 -- Не знайдено в базі МІС
WHERE statement_id = :statementId
  AND matched_encounter_id IS NULL;


-- ----------------------------------------------------------------------------
-- 2. ЗАПИТ РОЗРАХУНКУ ТАРИФІВ ПМГ-2026 ТА ДЕФЕКТУРИ (ПОСТАНОВА КМУ №1808)
-- ----------------------------------------------------------------------------
-- Розраховує тариф для стаціонарних ДСГ на основі ваги (dsg_group_weight)
-- та базової ставки 8 735,00 ₴
UPDATE public.dsg_nszu_statement_line sl
SET 
    mis_amount = ROUND(
        8735.00 * gw.weight_coef * (CASE WHEN sl.package_number = '4' THEN 0.60 ELSE 0.55 END), 
        2
    ),
    difference = ROUND(
        8735.00 * gw.weight_coef * (CASE WHEN sl.package_number = '4' THEN 0.60 ELSE 0.55 END) - sl.nszu_amount, 
        2
    ),
    modified_on = (now() AT TIME ZONE 'utc')
FROM public.dsg_group_weight gw
WHERE sl.statement_id = :statementId
  AND sl.dsg_code = gw.caption;


-- ----------------------------------------------------------------------------
-- 3. АГРЕГОВАНИЙ ЗВІТ ПО ЛІКАРЯХ ТА ВІДДІЛЕННЯХ (АРКУШ «ЗВІТ» НСЗУ)
-- ----------------------------------------------------------------------------
-- Аналізує кількість внесених ЕМЗ, відсоток відхилених записів та втрачений дохід
SELECT 
    emp.id AS employee_id,
    COALESCE(p.last_name || ' ' || SUBSTRING(p.first_name, 1, 1) || '. ' || SUBSTRING(p.second_name, 1, 1) || '.', emp.caption) AS doctor_name,
    COALESCE(pos.caption, 'Лікар') AS position_name,
    COALESCE(dept.caption, 'Загальноклінічне') AS department_name,
    COUNT(sl.id) AS total_emz,
    COUNT(CASE WHEN sl.match_status = 1 AND sl.mis_amount > 0 THEN 1 END) AS accepted_count,
    COUNT(CASE WHEN sl.match_status = 3 OR sl.raw_payload_json->>'included' = 'Ні' THEN 1 END) AS rejected_count,
    ROUND(
        COUNT(CASE WHEN sl.match_status = 3 OR sl.raw_payload_json->>'included' = 'Ні' THEN 1 END)::numeric / 
        NULLIF(COUNT(sl.id), 0) * 100, 
        2
    ) AS error_percentage,
    COALESCE(SUM(CASE WHEN sl.raw_payload_json->>'included' != 'Ні' THEN sl.mis_amount ELSE 0 END), 0) AS total_revenue,
    COALESCE(SUM(CASE WHEN sl.raw_payload_json->>'included' = 'Ні' THEN sl.mis_amount ELSE 0 END), 0) AS lost_revenue
FROM public.dsg_nszu_statement_line sl
JOIN public.mis_encounter enc ON sl.matched_encounter_id = enc.id
LEFT JOIN public.org_employee emp ON enc.employee_id = emp.id
LEFT JOIN public.cmn_person p ON emp.person_id = p.id
LEFT JOIN public.ehd_dictionary pos ON emp.position_id = pos.id
LEFT JOIN public.org_department dept ON enc.department_id = dept.id
WHERE sl.statement_id = :statementId
GROUP BY emp.id, p.last_name, p.first_name, p.second_name, emp.caption, pos.caption, dept.caption
ORDER BY lost_revenue DESC, total_emz DESC;


-- ----------------------------------------------------------------------------
-- 4. РЕЄСТР ВІДХИЛЕНИХ ЗАПИСІВ (LOST REVENUE JOURNAL)
-- ----------------------------------------------------------------------------
-- Вибірка випадків, які отримали статус «Ні» від НСЗУ, із сумою втрат для виправлення
SELECT 
    sl.id AS line_id,
    sl.encounter_ehealth_id,
    sl.matched_encounter_id,
    enc.created_on AS encounter_date,
    sl.package_number,
    sl.dsg_code,
    sl.mis_amount AS potential_lost_amount,
    sl.raw_payload_json->>'error_comment' AS nszu_error_reason,
    sl.raw_payload_json->>'diag_main' AS current_diagnosis,
    sl.raw_payload_json->>'services' AS current_services
FROM public.dsg_nszu_statement_line sl
LEFT JOIN public.mis_encounter enc ON sl.matched_encounter_id = enc.id
WHERE sl.statement_id = :statementId
  AND (sl.raw_payload_json->>'included' = 'Ні' OR sl.match_status = 3)
ORDER BY sl.mis_amount DESC;


-- ----------------------------------------------------------------------------
-- 5. ПОВНИЙ ЗРІЗ 45 КОЛОНОК ІЗ ТАРИФІКАЦІЄЮ (AUDIT GRID VIEW)
-- ----------------------------------------------------------------------------
SELECT 
    sl.id,
    sl.encounter_ehealth_id,
    enc.id AS mis_encounter_id,
    sl.package_number,
    sl.dsg_code,
    sl.mis_amount AS calculated_tariff,
    sl.raw_payload_json->>'included' AS nszu_status,
    sl.raw_payload_json->>'doc_name' AS doctor_name,
    sl.raw_payload_json->>'diag_main' AS primary_diagnosis,
    sl.raw_payload_json->>'patient_id' AS patient_ehealth_id,
    sl.raw_payload_json AS all_45_columns
FROM public.dsg_nszu_statement_line sl
LEFT JOIN public.mis_encounter enc ON sl.matched_encounter_id = enc.id
WHERE sl.statement_id = :statementId
ORDER BY sl.id;
