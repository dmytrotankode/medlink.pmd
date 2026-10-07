import sqlite3
import re
import uuid

DB_PATH = r"c:\__MEDLINK___\PMG\pmg_database.sqlite"

def seed_accurate():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. NHSU Errors (186 errors)
    print("1. Parsing and inserting 186 NHSU Errors...")
    cur.execute("DELETE FROM dsg_nhsu_error_dictionary;")
    with open(r"c:\__MEDLINK___\PMG\sql\06_seed_nhsu_error_dictionary_186.sql", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    cnt_err = 0
    in_values = False
    for line in lines:
        if "VALUES" in line:
            in_values = True
            continue
        if in_values and line.strip().startswith("("):
            # Parse line: ('ERR_...', 'Title', 'Normative', 'Description', 'Remediation', severity)
            # Use regex for quoted strings and number
            parts = re.findall(r"'((?:''|[^'])*)'", line)
            num_match = re.search(r",\s*([0-9]+)\s*\)", line)
            if len(parts) >= 5 and num_match:
                err_code = parts[0].replace("''", "'")
                title = parts[1].replace("''", "'")
                normative = parts[2].replace("''", "'")
                desc = parts[3].replace("''", "'")
                remediation = parts[4].replace("''", "'")
                sev_num = int(num_match.group(1))
                sev = "ERROR" if sev_num == 2 else "WARNING"
                category = "CLINICAL" if "SURG" in err_code or "DIAG" in err_code else "ADMINISTRATIVE"
                if "DOC" in err_code: category = "SPECIALTY"
                if "DUP" in err_code: category = "DUPLICATE"

                cur.execute("""
                INSERT OR REPLACE INTO dsg_nhsu_error_dictionary (
                    id, error_code, title, description, legal_basis, recommendation_action, category, severity
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (str(uuid.uuid4()), err_code, title, desc, normative, remediation, category, sev))
                cnt_err += 1

    print(f"   -> Inserted {cnt_err} NHSU errors.")

    # 2. Doctor Position Requirements (1,257 rules from MedProfit)
    print("2. Parsing and inserting 1,257 Doctor Position Rules...")
    cur.execute("DELETE FROM dsg_doctor_position_rule;")
    with open(r"c:\__MEDLINK___\PMG\sql\07_seed_doctor_position_requirements.sql", "r", encoding="utf-8") as f:
        lines_pos = f.readlines()
    
    cnt_pos = 0
    in_values_pos = False
    for line in lines_pos:
        if "VALUES" in line:
            in_values_pos = True
            continue
        if in_values_pos and line.strip().startswith("("):
            parts = re.findall(r"'((?:''|[^'])*)'", line)
            # ('service_code', 'service_name', 'service_type', 'class_number', 'class_name', 'mdc_requirements', 'position_requirements')
            if len(parts) >= 7:
                srv_code = parts[0].replace("''", "'")
                srv_name = parts[1].replace("''", "'")
                mdc = parts[5].replace("''", "'")
                pos_req = parts[6].replace("''", "'")
                cur.execute("""
                INSERT INTO dsg_doctor_position_rule (
                    id, service_code, required_position_code, required_position_name, mdc_code, description
                ) VALUES (?, ?, ?, ?, ?, ?)
                """, (str(uuid.uuid4()), srv_code, pos_req, srv_name, mdc, f"Вимоги MDC: {mdc}, Дозволені посади: {pos_req}"))
                cnt_pos += 1

    print(f"   -> Inserted {cnt_pos} Doctor Position Rules.")

    # 3. Laboratory Tests (408 tests)
    print("3. Parsing and inserting 408 Laboratory Tests...")
    cur.execute("DELETE FROM dsg_laboratory_test;")
    with open(r"c:\__MEDLINK___\PMG\sql\08_seed_laboratory_tests_408.sql", "r", encoding="utf-8") as f:
        lines_lab = f.readlines()
    
    cnt_lab = 0
    in_values_lab = False
    for line in lines_lab:
        if "VALUES" in line:
            in_values_lab = True
            continue
        if in_values_lab and line.strip().startswith("("):
            parts = re.findall(r"'((?:''|[^'])*)'", line)
            if len(parts) >= 3:
                code = parts[0].replace("''", "'")
                name = parts[1].replace("''", "'")
                grp = parts[2].replace("''", "'")
                cur.execute("""
                INSERT OR REPLACE INTO dsg_laboratory_test (
                    id, test_code, test_name, observation_code, tariff
                ) VALUES (?, ?, ?, ?, ?)
                """, (str(uuid.uuid4()), code, name, grp, 65.0))
                cnt_lab += 1

    print(f"   -> Inserted {cnt_lab} Laboratory Tests.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_accurate()
