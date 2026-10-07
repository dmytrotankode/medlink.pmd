import urllib.request
import urllib.parse
import json
import sqlite3
import os
import sys

def verify_all():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=== STARTING FULL PMG-2026 SYSTEM VERIFICATION ===")
    errors = []

    # 1. Check SQLite Database
    db_path = r'c:\__MEDLINK___\PMG\pmg_database.sqlite'
    if not os.path.exists(db_path):
        errors.append(f"Database not found: {db_path}")
    else:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        tables = [
            ("pmg_packages", 46),
            ("pmg_dsg", 465),
            ("pmg_package9_classes", 148),
            ("dsg_nhsu_error_dictionary", 186),
            ("dsg_doctor_position_rule", 1257),
            ("pmg_service_groups", 12),
            ("pmg_service_catalog", 12),
            ("pmg_service_combinations", 6)
        ]
        for tbl, expected_min in tables:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {tbl}")
                cnt = cur.fetchone()[0]
                if cnt >= expected_min:
                    print(f"  [OK] Table '{tbl}': {cnt} rows (expected >= {expected_min})")
                else:
                    errors.append(f"Table '{tbl}' has {cnt} rows, expected at least {expected_min}")
            except Exception as e:
                errors.append(f"Error querying table '{tbl}': {e}")
        conn.close()

    # 2. Check REST API on localhost:8085
    base_url = "http://localhost:8085"
    cat_query = urllib.parse.quote("Онкологія та гематологія")
    api_tests = [
        ("/api/v1/pmg/dictionaries/packages", 46, "All 46 packages list"),
        ("/api/v1/pmg/dictionaries/packages/47", "стаціонару одного дня", "Package 47 detail"),
        ("/api/v1/pmg/dictionaries/packages/54", "амбулаторних умовах", "Package 54 detail"),
        (f"/api/v1/pmg/dictionaries/packages?category={cat_query}", 3, "Oncology cluster query (3 pkgs)"),
        ("/api/v1/pmg/dictionaries/service-groups", 12, "Service Groups (12 clinical groups)"),
        ("/api/v1/pmg/dictionaries/services", 12, "Services Catalog (>= 12 core services)"),
        ("/api/v1/pmg/dictionaries/services/32003-00", "геміколектомія", "Service Passport 32003-00 detail")
    ]

    for endpoint, check_val, desc in api_tests:
        try:
            req = urllib.request.urlopen(base_url + endpoint, timeout=5)
            data = json.loads(req.read().decode('utf-8'))
            if isinstance(check_val, int):
                if len(data) >= check_val:
                    print(f"  [OK] API {desc}: returned {len(data)} items")
                else:
                    errors.append(f"API {desc}: expected >= {check_val} items, got {len(data)}")
            elif isinstance(check_val, str):
                if check_val in json.dumps(data, ensure_ascii=False):
                    print(f"  [OK] API {desc}: contains expected text '{check_val}'")
                else:
                    errors.append(f"API {desc}: did not find text '{check_val}'")
        except Exception as e:
            errors.append(f"API test failed for {endpoint}: {e}")

    # 3. Check Prebilling API POST
    try:
        calc_url = base_url + "/api/v1/pmg/prebilling/calculate"
        payload = json.dumps({
            "icdCode": "C180",
            "serviceCode": "32003-00",
            "doctorPosition": "P157",
            "admissionType": "Планова",
            "isMountain": False
        }).encode('utf-8')
        req = urllib.request.Request(calc_url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')
        resp = urllib.request.urlopen(req, timeout=5)
        calc_res = json.loads(resp.read().decode('utf-8'))
        if calc_res.get("calculatedTariffUah", 0) > 0:
            print(f"  [OK] API Pre-billing calculate: Tariff = {calc_res.get('calculatedTariffUah')} UAH, Valid = {calc_res.get('antiDefekturaCheck', {}).get('isValid')}")
        else:
            errors.append(f"Pre-billing calculate returned 0 or error: {calc_res}")
    except Exception as e:
        errors.append(f"Pre-billing POST test failed: {e}")

    # 4. Check Service Combination Matrix & Validator POST
    try:
        val_url = base_url + "/api/v1/pmg/combinations/validate"
        payload = json.dumps({
            "service_code": "32003-00",
            "icd_code": "C18.0",
            "patient_age": 55,
            "patient_gender": "Чоловіча",
            "doctor_position": "P157",
            "companion_services": ["30075-01", "30440-00"]
        }).encode('utf-8')
        req = urllib.request.Request(val_url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')
        resp = urllib.request.urlopen(req, timeout=5)
        val_res = json.loads(resp.read().decode('utf-8'))
        if val_res.get("is_valid") is True and val_res.get("applied_coefficient") == 1.30:
            print(f"  [OK] API Service Combination Validator: Valid = True, Coeff = {val_res.get('applied_coefficient')}, Tariff = {val_res.get('calculated_tariff')} UAH")
        else:
            errors.append(f"Combination validate failed or didn't apply 1.30: {val_res}")
    except Exception as e:
        errors.append(f"Combination validate POST test failed: {e}")

    # 5. Check Normative Dossiers
    norm_dir = r'c:\__MEDLINK___\PMG\normative_packages'
    expected_dossiers = [
        "01_primary_care.html",
        "02_emergency_care.html",
        "03_specialized_surgery_and_therapy_dsg.html",
        "04_priority_stroke_infarct_maternity.html",
        "05_ambulatory_outpatient_and_screening.html",
        "06_oncology_and_hematology.html",
        "07_rehabilitation_care.html",
        "08_palliative_care.html",
        "09_psychiatry_and_addiction.html",
        "10_infectious_tb_hiv.html",
        "11_high_tech_art_transplant.html",
        "12_defense_readiness_vlk.html",
        "all_packages_manifest.json",
        "index.html"
    ]
    for d in expected_dossiers:
        fp = os.path.join(norm_dir, d)
        if os.path.exists(fp) and os.path.getsize(fp) > 0:
            print(f"  [OK] Normative Dossier file: {d} ({os.path.getsize(fp):,} bytes)")
        else:
            errors.append(f"Missing or empty normative dossier: {d}")

    # 6. Check Documentation Chapters (10 Chapters)
    docs_dir = r'c:\__MEDLINK___\PMG\docs_html'
    expected_docs = [f"{i:02d}" for i in range(1, 11)]
    for num in expected_docs:
        matches = [f for f in os.listdir(docs_dir) if f.startswith(num)]
        if matches:
            print(f"  [OK] Documentation Chapter {num}: {matches[0]}")
        else:
            errors.append(f"Missing Documentation Chapter {num}")

    # 7. Check SQL Scripts (11 Scripts)
    sql_dir = r'c:\__MEDLINK___\PMG\sql'
    expected_sqls = [
        "01_ddl_tables.sql",
        "02_queries_2way_matching.sql",
        "03_seed_pmg2026_data.sql",
        "04_seed_dsg_catalog_465.sql",
        "05_seed_package9_classes_148.sql",
        "06_seed_nhsu_error_dictionary_186.sql",
        "07_seed_doctor_position_requirements.sql",
        "08_seed_laboratory_tests_408.sql",
        "09_seed_medprofit_rules_185.sql",
        "10_seed_all_pmg2026_packages.sql",
        "11_seed_service_combinations_and_groups.sql"
    ]
    for sql_name in expected_sqls:
        sfp = os.path.join(sql_dir, sql_name)
        if os.path.exists(sfp) and os.path.getsize(sfp) > 0:
            print(f"  [OK] SQL Seed Script: {sql_name} ({os.path.getsize(sfp):,} bytes)")
        else:
            errors.append(f"Missing or empty SQL script: {sql_name}")

    # 8. Check ZIP Bundle
    zip_path = r'c:\__MEDLINK___\PMG\medlink_pmg_complete.zip'
    if os.path.exists(zip_path) and os.path.getsize(zip_path) > 10_000_000:
        print(f"  [OK] ZIP Bundle: {zip_path} ({os.path.getsize(zip_path):,} bytes)")
    else:
        errors.append(f"ZIP Bundle missing or too small: {zip_path}")

    # 9. Check Single-File Components
    expected_comps = [
        "PmgPackagesCatalog.vue",
        "PmgServicesCatalog.vue"
    ]
    for cname in expected_comps:
        comp_file = os.path.join(r'c:\__MEDLINK___\PMG\prototype_medlink\components', cname)
        if os.path.exists(comp_file):
            print(f"  [OK] Single-File Component: {cname}")
        else:
            errors.append(f"{cname} not found")

    print("\n=== SUMMARY ===")
    if errors:
        print(f"FAILED with {len(errors)} errors:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("ALL 9 VERIFICATION CRITERIA (DATABASE, API, VALIDATOR, DOSSIERS, DOCS, SQL, ZIP, VUE) PASSED 100% PERFECTLY! No errors found.")
        sys.exit(0)

if __name__ == '__main__':
    verify_all()
