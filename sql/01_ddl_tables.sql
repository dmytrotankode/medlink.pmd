-- ============================================================================
-- MEDLINK PMG-2026: DDL СХЕМА ТАБЛИЦЬ (POSTGRESQL 14+)
-- Модуль аналітики Програми медичних гарантій 2026 року та звітів НСЗУ
-- ============================================================================

-- 1. Таблиця заголовків звітів НСЗУ (.xlsx)
CREATE TABLE IF NOT EXISTS public.dsg_nszu_statement (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_state INTEGER NOT NULL DEFAULT 2, -- 2 = Active, 4 = Deleted
    caption VARCHAR(255),
    modified_by UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000000'::uuid,
    modified_on TIMESTAMP WITHOUT TIME ZONE,
    created_by UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000000'::uuid,
    created_on TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (now() AT TIME ZONE 'utc'),
    organization_id UUID NOT NULL, -- FK до LegalEntities.Id
    period_from TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    period_to TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    file_name VARCHAR(500),
    imported_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (now() AT TIME ZONE 'utc'),
    imported_by UUID -- FK до Employees.Id
);

CREATE INDEX IF NOT EXISTS idx_dsg_nszu_stmt_org_period 
ON public.dsg_nszu_statement (organization_id, period_from, period_to);

-- 2. Таблиця рядків звіту НСЗУ (Аркуш «Деталізація послуг» - 45 колонок)
CREATE TABLE IF NOT EXISTS public.dsg_nszu_statement_line (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_state INTEGER NOT NULL DEFAULT 2,
    caption VARCHAR(255),
    modified_by UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000000'::uuid,
    modified_on TIMESTAMP WITHOUT TIME ZONE,
    created_by UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000000'::uuid,
    created_on TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (now() AT TIME ZONE 'utc'),
    statement_id UUID NOT NULL REFERENCES public.dsg_nszu_statement(id) ON DELETE CASCADE,
    encounter_ehealth_id UUID, -- Колонка 4 звіту: ID ЕМЗ в eHealth
    dsg_code VARCHAR(64),      -- Код ДСГ або номер класу
    package_number VARCHAR(32), -- Номер пакету медичних послуг (3, 4, 9, 47 тощо)
    nszu_amount NUMERIC(18, 4) NOT NULL DEFAULT 0.0000, -- Сума НСЗУ (0 ₴, якщо відсутня)
    matched_encounter_id UUID REFERENCES public.mis_encounter(id) ON DELETE SET NULL, -- 2-Way зв'язок з МІС
    mis_amount NUMERIC(18, 4), -- Автономно розрахований тариф МІС за Постановою №1808
    difference NUMERIC(18, 4), -- Різниця (mis_amount - nszu_amount), дефіцит або дефектура
    match_status INTEGER NOT NULL DEFAULT 0, -- 0=Новий, 1=Звірено, 2=Не знайдено в МІС, 3=Відхилено НСЗУ
    raw_payload_json JSONB     -- Збереження решти з 45 колонок для повної деталізації
);

CREATE INDEX IF NOT EXISTS idx_dsg_nszu_stmt_line_stmt_id 
ON public.dsg_nszu_statement_line (statement_id);

CREATE INDEX IF NOT EXISTS idx_dsg_nszu_stmt_line_eh_id 
ON public.dsg_nszu_statement_line (encounter_ehealth_id);

CREATE INDEX IF NOT EXISTS idx_dsg_nszu_stmt_line_matched_enc 
ON public.dsg_nszu_statement_line (matched_encounter_id);

-- 3. Таблиця аналітичних результатів та аудиту правил кодування
CREATE TABLE IF NOT EXISTS public.dsg_analysis_result (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_state INTEGER NOT NULL DEFAULT 2,
    caption VARCHAR(255),
    modified_by UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000000'::uuid,
    modified_on TIMESTAMP WITHOUT TIME ZONE,
    created_by UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000000'::uuid,
    created_on TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (now() AT TIME ZONE 'utc'),
    encounter_id UUID NOT NULL REFERENCES public.mis_encounter(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL,
    package_number VARCHAR(16),
    dsg_package_code_id UUID,
    dsg_group_code VARCHAR(32),
    status INTEGER NOT NULL DEFAULT 0, -- 0 = Прийнято, 1 = Попередження, 2 = Відхилено (Дефектура)
    tariff NUMERIC(18, 4) NOT NULL DEFAULT 0.0000,
    estimated_payment NUMERIC(18, 4) NOT NULL DEFAULT 0.0000,
    weight_coef NUMERIC(18, 4) NOT NULL DEFAULT 1.0000,
    calculation JSONB NOT NULL, -- Дерево розрахунку: кроки steps, операції, посилання на нормативку
    findings JSONB NOT NULL,    -- Перелік виявлених дефектів та рекомендацій
    dictionary_versions JSONB,
    request_hash VARCHAR(128),
    trigger INTEGER DEFAULT 1,  -- 1=Manual/Prebilling, 2=Background/Import
    analyzed_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (now() AT TIME ZONE 'utc'),
    primary_icd10_code VARCHAR(32),
    employee_id UUID REFERENCES public.org_employee(id) ON DELETE SET NULL,
    department_id UUID REFERENCES public.org_department(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_dsg_analysis_enc_id 
ON public.dsg_analysis_result (encounter_id);

CREATE INDEX IF NOT EXISTS idx_dsg_analysis_emp_dept 
ON public.dsg_analysis_result (employee_id, department_id);

-- 4. Таблиця глобальних налаштувань тарифів ПМГ-2026 (Постанова №1808)
CREATE TABLE IF NOT EXISTS public.dsg_tariff_setting (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_state INTEGER NOT NULL DEFAULT 2,
    caption VARCHAR(255),
    modified_by UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000000'::uuid,
    modified_on TIMESTAMP WITHOUT TIME ZONE,
    created_by UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000000'::uuid,
    created_on TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (now() AT TIME ZONE 'utc'),
    base_rate NUMERIC(18, 4) NOT NULL DEFAULT 8735.0000, -- Базова ставка стаціонару (8 735,00 ₴)
    global_rate_share NUMERIC(18, 4) NOT NULL DEFAULT 0.5500, -- Частка глобальної ставки (0,55)
    valid_from TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    valid_to TIMESTAMP WITHOUT TIME ZONE,
    budget_balance_coef NUMERIC(18, 4) NOT NULL DEFAULT 1.0000
);

-- 5. Таблиця вагових коефіцієнтів ДСГ (471 група)
CREATE TABLE IF NOT EXISTS public.dsg_group_weight (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_state INTEGER NOT NULL DEFAULT 2,
    caption VARCHAR(255),
    modified_by UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000000'::uuid,
    modified_on TIMESTAMP WITHOUT TIME ZONE,
    created_by UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000000'::uuid,
    created_on TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() AT TIME ZONE 'utc'),
    dictionary_version_id UUID,
    dsg_package_code_id UUID,
    weight_coef NUMERIC(18, 4) NOT NULL,
    multi_ops_weight_coef NUMERIC(18, 4),
    attributes JSONB
);

-- 6. Таблиця правил перевірки відповідності (FR / PK / RD)
CREATE TABLE IF NOT EXISTS public.dsg_rule_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_state INTEGER NOT NULL DEFAULT 2,
    caption VARCHAR(255) NOT NULL,
    rule_code VARCHAR(32),
    package_number VARCHAR(16),
    severity INTEGER DEFAULT 0, -- 0=Info, 1=Warning, 2=Error
    normative_reference TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    config_params JSONB
);
