import sqlite3
import json
import uuid
from datetime import datetime

DB_PATH = r"c:\__MEDLINK___\PMG\pmg_database.sqlite"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("Creating tables in local SQLite database...")

    # 1. Tariff settings
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dsg_tariff_setting (
        id TEXT PRIMARY KEY,
        caption TEXT,
        base_rate REAL NOT NULL DEFAULT 8735.0,
        outpatient_base_rate REAL NOT NULL DEFAULT 155.0,
        planned_hospitalization_coeff REAL NOT NULL DEFAULT 0.80,
        mountain_coeff REAL NOT NULL DEFAULT 1.25,
        global_rate_share_surgery REAL NOT NULL DEFAULT 0.55,
        global_rate_share_therapy REAL NOT NULL DEFAULT 0.60,
        active_from TEXT,
        active_to TEXT,
        is_active INTEGER NOT NULL DEFAULT 1
    );
    """)

    # Insert default settings if not exists
    cur.execute("SELECT count(*) FROM dsg_tariff_setting")
    if cur.fetchone()[0] == 0:
        cur.execute("""
        INSERT INTO dsg_tariff_setting (
            id, caption, base_rate, outpatient_base_rate, planned_hospitalization_coeff, 
            mountain_coeff, global_rate_share_surgery, global_rate_share_therapy, 
            active_from, active_to, is_active
        ) VALUES (
            'setting-2026-default', 'Постанова КМУ №1808 (ПМГ 2026)', 8735.0, 155.0, 0.80,
            1.25, 0.55, 0.60, '2026-01-01', '2026-12-31', 1
        );
        """)

    # 2. NHSU Statements (sessions of imported files)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dsg_nszu_statement (
        id TEXT PRIMARY KEY,
        organization_id TEXT NOT NULL,
        organization_name TEXT NOT NULL,
        period_from TEXT NOT NULL,
        period_to TEXT NOT NULL,
        file_name TEXT NOT NULL,
        imported_at TEXT NOT NULL,
        imported_by TEXT,
        total_records INTEGER DEFAULT 0,
        accepted_records INTEGER DEFAULT 0,
        rejected_records INTEGER DEFAULT 0,
        accepted_amount REAL DEFAULT 0.0,
        rejected_amount REAL DEFAULT 0.0,
        reconciled_at TEXT,
        status TEXT DEFAULT 'PROCESSED'
    );
    """)

    # 3. NHSU Statement Lines (45 columns)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dsg_nszu_statement_line (
        id TEXT PRIMARY KEY,
        statement_id TEXT NOT NULL,
        line_number INTEGER NOT NULL,
        encounter_ehealth_id TEXT,
        patient_rnokpp TEXT,
        patient_full_name TEXT,
        doctor_id TEXT,
        doctor_full_name TEXT,
        department_id TEXT,
        department_name TEXT,
        package_number TEXT,
        admission_type TEXT, -- Ургентна / Планова
        date_start TEXT,
        date_end TEXT,
        primary_icd10_code TEXT,
        primary_icd10_name TEXT,
        interventions TEXT,
        dsg_code TEXT,
        dsg_name TEXT,
        weight_coef REAL DEFAULT 1.0,
        service_class_code TEXT,
        service_class_name TEXT,
        nszu_amount REAL DEFAULT 0.0,
        mis_amount REAL DEFAULT 0.0,
        difference REAL DEFAULT 0.0,
        is_accepted INTEGER DEFAULT 1,
        rejection_reason_code TEXT,
        rejection_reason_text TEXT,
        legal_basis TEXT,
        matched_encounter_id TEXT,
        match_status INTEGER DEFAULT 0, -- 1=MATCHED_PAID, 2=DISCREPANCY_ERROR, 3=MISSING_IN_NHSU, 4=GHOST
        raw_payload_json TEXT,
        FOREIGN KEY (statement_id) REFERENCES dsg_nszu_statement(id)
    );
    """)

    # 4. MIS Encounters (simulating MedLink's internal EMR database)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS mis_encounter (
        id TEXT PRIMARY KEY,
        ehealth_id TEXT UNIQUE,
        patient_id TEXT,
        patient_rnokpp TEXT,
        patient_full_name TEXT,
        doctor_id TEXT,
        doctor_full_name TEXT,
        doctor_position_code TEXT,
        doctor_position_name TEXT,
        department_id TEXT,
        department_name TEXT,
        date_start TEXT,
        date_end TEXT,
        package_number TEXT,
        admission_type TEXT,
        primary_icd10_code TEXT,
        primary_icd10_name TEXT,
        interventions TEXT,
        dsg_code TEXT,
        weight_coef REAL DEFAULT 1.0,
        calculated_amount REAL DEFAULT 0.0,
        status TEXT DEFAULT 'COMPLETED', -- DRAFT, SIGNED, COMPLETED
        ehealth_status TEXT DEFAULT 'SENT', -- NOT_SENT, SENT, ACCEPTED, REJECTED
        ehealth_error_code TEXT,
        ehealth_error_message TEXT,
        is_urgent_month_counted INTEGER DEFAULT 1, -- для Пакета 9
        created_at TEXT,
        updated_at TEXT
    );
    """)

    # 5. NHSU Error Dictionary (186 errors)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dsg_nhsu_error_dictionary (
        id TEXT PRIMARY KEY,
        error_code TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        legal_basis TEXT,
        recommendation_action TEXT,
        severity TEXT DEFAULT 'ERROR', -- WARNING, ERROR, CRITICAL
        category TEXT -- CLINICAL, ADMINISTRATIVE, DUPLICATE, SPECIALTY
    );
    """)

    # 6. Doctor Position Requirements (1,257 rules from MedProfit)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dsg_doctor_position_rule (
        id TEXT PRIMARY KEY,
        service_code TEXT NOT NULL,
        required_position_code TEXT NOT NULL,
        required_position_name TEXT NOT NULL,
        mdc_code TEXT,
        description TEXT
    );
    """)

    # 7. Laboratory tests (408 codes)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dsg_laboratory_test (
        id TEXT PRIMARY KEY,
        test_code TEXT UNIQUE NOT NULL,
        test_name TEXT NOT NULL,
        observation_code TEXT,
        tariff REAL DEFAULT 0.0,
        package_number TEXT DEFAULT '9'
    );
    """)

    # 8. Analysis Result
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dsg_analysis_result (
        id TEXT PRIMARY KEY,
        encounter_id TEXT,
        package_number TEXT,
        dsg_code TEXT,
        status INTEGER DEFAULT 0, -- 0=OK, 1=WARN, 2=REJECTED
        tariff REAL DEFAULT 0.0,
        weight_coef REAL DEFAULT 1.0,
        findings_json TEXT,
        calculation_json TEXT,
        analyzed_at TEXT
    );
    """)

    # Indexes
    cur.execute("CREATE INDEX IF NOT EXISTS idx_stmt_line_stmt ON dsg_nszu_statement_line(statement_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_stmt_line_eh ON dsg_nszu_statement_line(encounter_ehealth_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_mis_enc_eh ON mis_encounter(ehealth_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_doc_pos_srv ON dsg_doctor_position_rule(service_code);")

    conn.commit()
    print("Database tables initialized successfully!")
    conn.close()

if __name__ == '__main__':
    init_db()
