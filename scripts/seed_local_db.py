import sqlite3
import re
import uuid

DB_PATH = r"c:\__MEDLINK___\PMG\pmg_database.sqlite"

def seed_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Seed 186 NHSU errors from sql/06_seed_nhsu_error_dictionary_186.sql
    print("Seeding NHSU Error Dictionary...")
    cur.execute("DELETE FROM dsg_nhsu_error_dictionary;")
    with open(r"c:\__MEDLINK___\PMG\sql\06_seed_nhsu_error_dictionary_186.sql", "r", encoding="utf-8") as f:
        sql = f.read()
    
    # Match INSERT INTO ... VALUES (...)
    # Pattern: ('ERR_...', 'Title', 'Desc', 'Legal', 'Rec', 'Category', 'Severity')
    pattern = r"\('([^']+)',\s*'([^']+)',\s*'([^']+)',\s*'([^']+)',\s*'([^']+)',\s*'([^']+)',\s*'([^']+)'\)"
    matches = re.findall(pattern, sql)
    print(f"  Found {len(matches)} error matches.")
    for m in matches:
        cur.execute("""
        INSERT OR REPLACE INTO dsg_nhsu_error_dictionary (
            id, error_code, title, description, legal_basis, recommendation_action, category, severity
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (str(uuid.uuid4()), m[0], m[1], m[2], m[3], m[4], m[5], m[6]))

    # 2. Seed 1,257 Doctor Position Rules from sql/07_seed_doctor_position_requirements.sql
    print("Seeding Doctor Position Requirements...")
    cur.execute("DELETE FROM dsg_doctor_position_rule;")
    with open(r"c:\__MEDLINK___\PMG\sql\07_seed_doctor_position_requirements.sql", "r", encoding="utf-8") as f:
        sql_pos = f.read()
    
    pattern_pos = r"\('([^']+)',\s*'([^']+)',\s*'([^']+)',\s*([0-9]+|NULL),\s*'([^']+)'\)"
    matches_pos = re.findall(pattern_pos, sql_pos)
    print(f"  Found {len(matches_pos)} position rule matches.")
    for m in matches_pos:
        mdc = None if m[3] == 'NULL' else str(m[3])
        cur.execute("""
        INSERT INTO dsg_doctor_position_rule (
            id, service_code, required_position_code, required_position_name, mdc_code, description
        ) VALUES (?, ?, ?, ?, ?, ?)
        """, (str(uuid.uuid4()), m[0], m[1], m[2], mdc, m[4]))

    # 3. Seed 408 Laboratory Tests from sql/08_seed_laboratory_tests_408.sql
    print("Seeding Laboratory Tests...")
    cur.execute("DELETE FROM dsg_laboratory_test;")
    with open(r"c:\__MEDLINK___\PMG\sql\08_seed_laboratory_tests_408.sql", "r", encoding="utf-8") as f:
        sql_lab = f.read()

    pattern_lab = r"\('([^']+)',\s*'([^']+)',\s*('([^']+)'|NULL),\s*([0-9\.]+)\)"
    matches_lab = re.findall(pattern_lab, sql_lab)
    print(f"  Found {len(matches_lab)} lab test matches.")
    for m in matches_lab:
        obs = m[3] if m[2] != 'NULL' else None
        cur.execute("""
        INSERT OR REPLACE INTO dsg_laboratory_test (
            id, test_code, test_name, observation_code, tariff
        ) VALUES (?, ?, ?, ?, ?)
        """, (str(uuid.uuid4()), m[0], m[1], obs, float(m[4])))

    conn.commit()
    print("Seeding completed successfully!")
    conn.close()

if __name__ == '__main__':
    seed_data()
