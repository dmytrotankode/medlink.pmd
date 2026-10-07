import os
import sys
import json
import sqlite3

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = "c:/__MEDLINK___/PMG/pmg_database.sqlite"
RAW_DIR = "c:/__MEDLINK___/PMG/extracted_data/raw_json"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. Packages table
cursor.execute("""
CREATE TABLE IF NOT EXISTS pmg_packages (
    package_id TEXT PRIMARY KEY,
    name TEXT,
    base_rate REAL,
    meta_json TEXT
)
""")

# 2. DSG Table (Packages 3, 4, 47)
cursor.execute("""
CREATE TABLE IF NOT EXISTS pmg_dsg (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id TEXT,
    drg_name TEXT,
    coefficient TEXT,
    coeff_numeric REAL,
    base_rate REAL,
    price REAL,
    additional_requirements TEXT,
    additional_requirements_code TEXT,
    additional_requirements_referral TEXT,
    req_package_1 TEXT,
    req_package_2 TEXT,
    req_package_3 TEXT,
    episode TEXT,
    diag_count INTEGER,
    svc_count INTEGER,
    diags_json TEXT,
    services_json TEXT,
    diag_notes_json TEXT
)
""")

# 3. DSG Diagnosis index (for fast lookups: given diagnosis -> which DSG and packages)
cursor.execute("""
CREATE TABLE IF NOT EXISTS pmg_dsg_diagnoses (
    package_id TEXT,
    dsg_id INTEGER,
    drg_name TEXT,
    diag_code TEXT,
    diag_name TEXT,
    notes TEXT,
    PRIMARY KEY (package_id, dsg_id, diag_code)
)
""")

# 4. DSG Service index (given ACHI service -> which DSG and packages)
cursor.execute("""
CREATE TABLE IF NOT EXISTS pmg_dsg_services (
    package_id TEXT,
    dsg_id INTEGER,
    drg_name TEXT,
    service_code TEXT,
    service_name TEXT,
    PRIMARY KEY (package_id, dsg_id, service_code)
)
""")

# 5. Package 9 Services & Classes
cursor.execute("""
CREATE TABLE IF NOT EXISTS pmg_package9_classes (
    id INTEGER PRIMARY KEY,
    service_id_name TEXT,
    class_name TEXT,
    class_number INTEGER,
    coefficient REAL,
    cost REAL,
    diag_count INTEGER,
    svc_count INTEGER,
    pos_count INTEGER,
    has_pos_svc_binding INTEGER,
    note TEXT,
    svc_codes_json TEXT,
    svc_diag_counts_json TEXT
)
""")

# 6. Package 54 Rehabilitation
cursor.execute("""
CREATE TABLE IF NOT EXISTS pmg_package54_rehab (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    diag_code TEXT,
    diag_name TEXT,
    ar_groups TEXT,
    cr_code TEXT,
    cr_group TEXT,
    is_main INTEGER,
    is_main_note TEXT,
    types_json TEXT,
    referral_pmd INTEGER,
    marker TEXT,
    note TEXT
)
""")

cursor.execute("CREATE INDEX IF NOT EXISTS idx_dsg_diag ON pmg_dsg_diagnoses(diag_code)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_dsg_svc ON pmg_dsg_services(service_code)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_p54_diag ON pmg_package54_rehab(diag_code)")

conn.commit()

# --- Populate Packages 3, 4, 47 ---
for pkg_id in ['3', '4', '47']:
    p_path = f"{RAW_DIR}/package_{pkg_id}_full.json"
    if not os.path.exists(p_path):
        continue
    with open(p_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    meta = data.get('meta', {})
    base_rate = meta.get('RATE', 8735.0)
    cursor.execute("INSERT OR REPLACE INTO pmg_packages VALUES (?, ?, ?, ?)",
                   (pkg_id, f"Пакет {pkg_id}", base_rate, json.dumps(meta, ensure_ascii=False)))
    
    for r in data.get('rows', []):
        coeff_str = str(r.get('coefficient', ''))
        first_coeff = 0.0
        try:
            first_coeff = float(coeff_str.split('/')[0].strip())
        except:
            pass
        
        cursor.execute("""
        INSERT INTO pmg_dsg (
            package_id, drg_name, coefficient, coeff_numeric, base_rate, price,
            additional_requirements, additional_requirements_code, additional_requirements_referral,
            req_package_1, req_package_2, req_package_3, episode,
            diag_count, svc_count, diags_json, services_json, diag_notes_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pkg_id, r.get('drg'), coeff_str, first_coeff,
            float(r.get('base_rate_raw', 0) or 0), float(r.get('price_raw', 0) or 0),
            r.get('additional_requirements'), r.get('additional_requirements_code'),
            r.get('additional_requirements_referral'),
            r.get('additional_requirements_package_1'), r.get('additional_requirements_package_2'),
            r.get('additional_requirements_package_3'), r.get('episode'),
            r.get('diag_count', 0), r.get('svc_count', 0),
            json.dumps(r.get('diags_structured', []), ensure_ascii=False),
            json.dumps(r.get('services_structured', []), ensure_ascii=False),
            json.dumps(r.get('diag_notes', {}), ensure_ascii=False)
        ))
        dsg_id = cursor.lastrowid
        drg_name = r.get('drg')
        diag_notes = r.get('diag_notes', {})

        # Populate index
        for d in r.get('diags_structured', []):
            d_code = d.get('code')
            d_name = d.get('name')
            d_note = diag_notes.get(d_code)
            d_note_str = json.dumps(d_note, ensure_ascii=False) if d_note else None
            cursor.execute("INSERT OR IGNORE INTO pmg_dsg_diagnoses VALUES (?, ?, ?, ?, ?, ?)",
                           (pkg_id, dsg_id, drg_name, d_code, d_name, d_note_str))

        for s in r.get('services_structured', []):
            s_code = s.get('code')
            s_name = s.get('name')
            cursor.execute("INSERT OR IGNORE INTO pmg_dsg_services VALUES (?, ?, ?, ?, ?)",
                           (pkg_id, dsg_id, drg_name, s_code, s_name))

    print(f"Populated Package {pkg_id} DSG rows & indexes.")

# --- Populate Package 9 ---
p9_path = f"{RAW_DIR}/package_9_full.json"
if os.path.exists(p9_path):
    with open(p9_path, "r", encoding="utf-8") as f:
        p9_data = json.load(f)
    meta9 = p9_data.get('meta', {})
    cursor.execute("INSERT OR REPLACE INTO pmg_packages VALUES (?, ?, ?, ?)",
                   ('9', "Пакет 9 - Амбулаторна допомога", meta9.get('RATE', 155.0), json.dumps(meta9, ensure_ascii=False)))
    for r in p9_data.get('rows', []):
        cost_val = 0.0
        try:
            cost_val = float(r.get('cost', 0))
        except:
            pass
        cursor.execute("""
        INSERT OR REPLACE INTO pmg_package9_classes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r.get('id'), r.get('service_id'), r.get('class'), r.get('class_number'),
            float(r.get('coefficient', 0)), cost_val,
            r.get('diag_count', 0), r.get('svc_count', 0), r.get('pos_count', 0),
            1 if r.get('has_pos_svc_binding') else 0,
            r.get('note'),
            json.dumps(r.get('svc_codes', []), ensure_ascii=False),
            json.dumps(r.get('svc_diag_counts', {}), ensure_ascii=False)
        ))
    print("Populated Package 9 classes & services.")

# --- Populate Package 54 ---
p54_path = f"{RAW_DIR}/package_54_full.json"
if os.path.exists(p54_path):
    with open(p54_path, "r", encoding="utf-8") as f:
        p54_data = json.load(f)
    cursor.execute("INSERT OR REPLACE INTO pmg_packages VALUES (?, ?, ?, ?)",
                   ('54', "Пакет 54 - Амбулаторна реабілітація", 0.0, "{}"))
    for r in p54_data.get('rows', []):
        cursor.execute("""
        INSERT INTO pmg_package54_rehab (
            diag_code, diag_name, ar_groups, cr_code, cr_group,
            is_main, is_main_note, types_json, referral_pmd, marker, note
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r.get('code'), r.get('name'),
            ",".join(r.get('ar', [])) if isinstance(r.get('ar'), list) else str(r.get('ar') or ''),
            r.get('cr_code'), r.get('cr_group'),
            1 if r.get('is_main') else 0, r.get('is_main_note'),
            json.dumps(r.get('types', []), ensure_ascii=False),
            1 if r.get('referral_pmd') else 0,
            r.get('marker'), r.get('note')
        ))
    print("Populated Package 54 rehabilitation rows.")

conn.commit()

# Print stats
cursor.execute("SELECT count(*) FROM pmg_dsg")
dsg_cnt = cursor.fetchone()[0]
cursor.execute("SELECT count(*) FROM pmg_dsg_diagnoses")
diag_cnt = cursor.fetchone()[0]
cursor.execute("SELECT count(*) FROM pmg_dsg_services")
svc_cnt = cursor.fetchone()[0]
cursor.execute("SELECT count(*) FROM pmg_package9_classes")
p9_cnt = cursor.fetchone()[0]
cursor.execute("SELECT count(*) FROM pmg_package54_rehab")
p54_cnt = cursor.fetchone()[0]

print(f"\n--- SQLite Database Build Complete ---")
print(f"Total DSG records: {dsg_cnt}")
print(f"Total Diagnosis-DSG indexed mappings: {diag_cnt}")
print(f"Total Service-DSG indexed mappings: {svc_cnt}")
print(f"Total Package 9 classes: {p9_cnt}")
print(f"Total Package 54 rehab rows: {p54_cnt}")
conn.close()
