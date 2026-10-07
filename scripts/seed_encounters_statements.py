import sqlite3
import uuid
import random
from datetime import datetime, timedelta

DB_PATH = r"c:\__MEDLINK___\PMG\pmg_database.sqlite"

def seed_statements_and_encounters():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DELETE FROM dsg_nszu_statement;")
    cur.execute("DELETE FROM dsg_nszu_statement_line;")
    cur.execute("DELETE FROM mis_encounter;")

    stmt_id = "stmt-cherkasy-2026-09"
    org_id = "org-cherkasy-onco"
    org_name = "КНП «Черкаський обласний клінічний онкологічний центр ЧОР»"

    doctors = [
        {"id": "doc-1", "name": "Коваленко Олександр Сергійович", "dept_id": "dept-surg", "dept": "Хірургічне відділення №1", "pos_code": "P157", "pos_name": "Хірург-онколог"},
        {"id": "doc-2", "name": "Мельник Тетяна Володимирівна", "dept_id": "dept-chem", "dept": "Відділення хіміотерапії", "pos_code": "P158", "pos_name": "Онколог"},
        {"id": "doc-3", "name": "Шевченко Віктор Іванович", "dept_id": "dept-rad", "dept": "Радіологічне відділення", "pos_code": "P159", "pos_name": "Радіолог-онколог"},
        {"id": "doc-4", "name": "Бондаренко Ірина Петрівна", "dept_id": "dept-outpatient", "dept": "Консультативно-діагностичне відділення", "pos_code": "P122", "pos_name": "Терапевт"},
        {"id": "doc-5", "name": "Кравченко Юрій Миколайович", "dept_id": "dept-daysurg", "dept": "Відділення малоінвазивної та денної хірургії", "pos_code": "P157", "pos_name": "Хірург-онколог"}
    ]

    patients = [
        ("2981412345", "Іваненко Василь Миколайович"),
        ("3124509876", "Петренко Олена Сергіївна"),
        ("2876543210", "Сидоренко Михайло Павлович"),
        ("3298714563", "Лисенко Галина Дмитрівна"),
        ("3012456789", "Ткаченко Андрій Вікторович"),
        ("2954316782", "Мороз Наталія Олексіївна"),
        ("3187654321", "Кузьменко Сергій Володимирович"),
        ("2765432198", "Григоренко Лариса Іванівна"),
        ("3345678901", "Федоренко Володимир Тарасович"),
        ("3098765432", "Марченко Вікторія Юріївна"),
        ("3156789012", "Дмитренко Ігор Анатолійович"),
        ("2890123456", "Пономаренко Олена Григорівна")
    ]

    # Clinical scenarios
    scenarios = [
        # (pkg, dsg, dsg_name, weight, icd_code, icd_name, srv_code, srv_name, adm_type, doctor_idx, is_accepted, err_code, err_text, legal)
        ("3", "O0101", "Великі хірургічні втручання на ободовій кишці", 2.766, "C18.0", "Злоякісне новоутворення сліпої кишки", "32003-00", "Резекція ободової кишки", "Планова", 0, 1, None, None, None),
        ("3", "O0201", "Хірургічні операції на шлунку при новоутвореннях", 2.340, "C16.2", "Злоякісне новоутворення тіла шлунка", "30518-00", "Часткова гастректомія з анастомозом", "Планова", 0, 1, None, None, None),
        ("4", "O6001", "Хіміотерапія злоякісних новоутворень, рівень 1", 1.450, "C50.9", "Злоякісне новоутворення молочної залози", "96199-00", "Внутрішньовенне введення антинеопластичних засобів", "Планова", 1, 1, None, None, None),
        ("4", "O6101", "Променева терапія злоякісних новоутворень", 1.820, "C61", "Злоякісне новоутворення передміхурової залози", "15269-00", "Конформна дистанційна променева терапія", "Планова", 2, 1, None, None, None),
        ("47", "D0101", "Хірургія одного дня: біопсія та резекція шкірних новоутворень", 0.650, "C43.5", "Злоякісна меланома тулуба", "30071-00", "Висічення меланоми", "Планова", 4, 1, None, None, None),
        ("9", "C01", "Амбулаторна консультація онколога та огляд", 1.000, "C50.1", "Злоякісне новоутворення центральної частини молочної залози", "11600-00", "Спеціалізована консультація онколога", "Планова", 3, 1, None, None, None),
        ("9", "C05", "Амбулаторна пункційна біопсія під контролем УЗД", 1.200, "C73", "Злоякісне новоутворення щитоподібної залози", "31548-00", "Тонкоголкова аспіраційна біопсія", "Планова", 3, 1, None, None, None),
        ("9", "C12", "Ургентний амбулаторний огляд при больовому синдромі", 1.000, "R52.1", "Хронічний некупований біль", "11600-00", "Ургентна консультація", "Ургентна", 3, 1, None, None, None),
        # Defektura items (rejected by NHSU)
        ("3", "O0101", "Великі хірургічні втручання на ободовій кишці", 2.766, "C18.0", "Злоякісне новоутворення сліпої кишки", "32003-00", "Резекція ободової кишки", "Планова", 3, 0, "ERR_DOC_SPEC_04", "Спеціальність лікаря P122 не відповідає вимогам для хірургії", "Наказ МОЗ № 410, п. 4.1"),
        ("4", "O6001", "Хіміотерапія злоякісних новоутворень", 1.450, "C50.9", "Злоякісне новоутворення молочної залози", "96199-00", "Введення хіміопрепаратів", "Планова", 1, 0, "ERR_MVTN_01", "Перетин періодів стаціонарного лікування з іншим ЗОЗ (Overlap)", "Постанова КМУ № 1808, п. 29"),
        ("47", "D0101", "Хірургія одного дня: біопсія", 0.650, "C43.5", "Злоякісна меланома", "30071-00", "Висічення меланоми", "Планова", 4, 0, "ERR_SURG_NO_OP_05", "Хірургічний пакет без належного коду операції", "Постанова КМУ № 1808, п. 41"),
        ("9", "C01", "Амбулаторна консультація", 1.000, "C50.1", "Злоякісне новоутворення", "11600-00", "Консультація", "Планова", 3, 0, "ERR_DUPLICATE_ENC_09", "Дублювання електронного медичного запису в eHealth", "Порядок ведення РЕМЗ, Наказ МОЗ № 587"),
        ("3", "O0201", "Операції на шлунку", 2.340, "R10.4", "Інший біль у животі (симптом замість нозології)", "30518-00", "Гастректомія", "Планова", 0, 0, "ERR_PRIMARY_DIAG_07", "Неприпустимий основний діагноз (R-код)", "Постанова КМУ № 1808, Додаток 1")
    ]

    base_rate = 8735.0
    outpatient_rate = 155.0
    line_number = 1
    total_acc_amt = 0.0
    total_rej_amt = 0.0
    accepted_cnt = 0
    rejected_cnt = 0

    print("Generating statement lines and matching encounters...")

    for i in range(40):
        scen = scenarios[i % len(scenarios)]
        pat = patients[i % len(patients)]
        doc = doctors[scen[9]]

        eh_id = str(uuid.uuid4())
        line_id = str(uuid.uuid4())
        enc_id = str(uuid.uuid4())

        pkg = scen[0]
        dsg_code = scen[1]
        dsg_name = scen[2]
        weight = scen[3]
        icd_code = scen[4]
        icd_name = scen[5]
        srv_code = scen[6]
        srv_name = scen[7]
        adm_type = scen[8]
        is_acc = scen[10]
        err_code = scen[11]
        err_text = scen[12]
        legal = scen[13]

        # Calculate tariff
        if pkg == "9":
            mis_amt = round(outpatient_rate * weight, 2)
        else:
            k_glob = 0.60 if pkg == "4" else 0.55
            k_plan = 0.80 if adm_type == "Планова" else 1.0
            mis_amt = round(base_rate * weight * k_glob * k_plan, 2)

        nszu_amt = mis_amt if is_acc else 0.0
        diff = mis_amt - nszu_amt

        if is_acc:
            accepted_cnt += 1
            total_acc_amt += nszu_amt
            match_status = 1 # MATCHED_PAID
        else:
            rejected_cnt += 1
            total_rej_amt += mis_amt
            match_status = 2 # DISCREPANCY_ERROR

        dt_start = (datetime(2026, 9, 1) + timedelta(days=(i % 25))).strftime("%Y-%m-%d 09:00:00")
        dt_end = (datetime(2026, 9, 1) + timedelta(days=(i % 25) + 3)).strftime("%Y-%m-%d 14:00:00")

        # Insert statement line
        cur.execute("""
        INSERT INTO dsg_nszu_statement_line (
            id, statement_id, line_number, encounter_ehealth_id, patient_rnokpp, patient_full_name,
            doctor_id, doctor_full_name, department_id, department_name, package_number, admission_type,
            date_start, date_end, primary_icd10_code, primary_icd10_name, interventions,
            dsg_code, dsg_name, weight_coef, service_class_code, service_class_name,
            nszu_amount, mis_amount, difference, is_accepted, rejection_reason_code,
            rejection_reason_text, legal_basis, matched_encounter_id, match_status, raw_payload_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            line_id, stmt_id, line_number, eh_id, pat[0], pat[1],
            doc["id"], doc["name"], doc["dept_id"], doc["dept"], pkg, adm_type,
            dt_start, dt_end, icd_code, icd_name, f"{srv_code} {srv_name}",
            dsg_code, dsg_name, weight, dsg_code if pkg == "9" else None, dsg_name if pkg == "9" else None,
            nszu_amt, mis_amt, diff, is_acc, err_code, err_text, legal, enc_id, match_status,
            '{"col45_audit": "valid", "k_mountain": 1.0, "k_plan": 0.8}'
        ))

        # Insert corresponding MIS encounter
        cur.execute("""
        INSERT INTO mis_encounter (
            id, ehealth_id, patient_id, patient_rnokpp, patient_full_name,
            doctor_id, doctor_full_name, doctor_position_code, doctor_position_name,
            department_id, department_name, date_start, date_end, package_number,
            admission_type, primary_icd10_code, primary_icd10_name, interventions,
            dsg_code, weight_coef, calculated_amount, status, ehealth_status,
            ehealth_error_code, ehealth_error_message, is_urgent_month_counted, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            enc_id, eh_id, f"pat-{i%len(patients)}", pat[0], pat[1],
            doc["id"], doc["name"], doc["pos_code"], doc["pos_name"],
            doc["dept_id"], doc["dept"], dt_start, dt_end, pkg,
            adm_type, icd_code, icd_name, f"{srv_code} {srv_name}",
            dsg_code, weight, mis_amt, "COMPLETED",
            "ACCEPTED" if is_acc else "REJECTED",
            err_code, err_text, 1 if i % 2 == 0 else 0, dt_start
        ))

        line_number += 1

    # 4. Insert 5 cases of "ПРИХОВАНА ДЕФЕКТУРА" (MISSING_IN_NHSU):
    # These exist in MedLink mis_encounter, but WERE DROPPED and are NOT in the NHSU statement!
    print("Generating 5 'Invisible Defektura' (MISSING_IN_NHSU) cases in MIS...")
    missing_scenarios = [
        ("3", "O0101", "Великі хірургічні втручання на ободовій кишці", 2.766, "C18.0", "Злоякісне новоутворення сліпої кишки", "32003-00", "Резекція ободової кишки", "Планова", 0),
        ("3", "O0201", "Хірургічні операції на шлунку", 2.340, "C16.2", "Злоякісне новоутворення шлунка", "30518-00", "Гастректомія", "Планова", 0),
        ("4", "O6001", "Хіміотерапія злоякісних новоутворень", 1.450, "C50.9", "Злоякісне новоутворення молочної залози", "96199-00", "Введення хіміопрепаратів", "Планова", 1),
        ("4", "O6101", "Променева терапія новоутворень", 1.820, "C61", "Рак простати", "15269-00", "Променева терапія", "Планова", 2),
        ("47", "D0101", "Хірургія одного дня: резекція новоутворень", 0.650, "C43.5", "Меланома тулуба", "30071-00", "Висічення", "Планова", 4)
    ]

    for j, ms in enumerate(missing_scenarios):
        m_eh_id = str(uuid.uuid4())
        m_enc_id = str(uuid.uuid4())
        doc = doctors[ms[9]]
        pat = patients[(j + 5) % len(patients)]
        pkg = ms[0]
        dsg_code = ms[1]
        weight = ms[3]
        k_glob = 0.60 if pkg == "4" else 0.55
        calc_amt = round(base_rate * weight * k_glob * 0.80, 2)
        dt = (datetime(2026, 9, 5) + timedelta(days=j*3)).strftime("%Y-%m-%d 10:00:00")

        cur.execute("""
        INSERT INTO mis_encounter (
            id, ehealth_id, patient_id, patient_rnokpp, patient_full_name,
            doctor_id, doctor_full_name, doctor_position_code, doctor_position_name,
            department_id, department_name, date_start, date_end, package_number,
            admission_type, primary_icd10_code, primary_icd10_name, interventions,
            dsg_code, weight_coef, calculated_amount, status, ehealth_status,
            ehealth_error_code, ehealth_error_message, is_urgent_month_counted, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            m_enc_id, m_eh_id, f"pat-miss-{j}", pat[0], pat[1],
            doc["id"], doc["name"], doc["pos_code"], doc["pos_name"],
            doc["dept_id"], doc["dept"], dt, dt, pkg,
            ms[8], ms[4], ms[5], f"{ms[6]} {ms[7]}",
            dsg_code, weight, calc_amt, "COMPLETED", "SENT",
            "MISSING_IN_NHSU", "Запис відправлено в eHealth, але НСЗУ не включила його у звіт (Оплата 0 ₴)", 1, dt
        ))

    # Insert Statement header
    cur.execute("""
    INSERT INTO dsg_nszu_statement (
        id, organization_id, organization_name, period_from, period_to, file_name,
        imported_at, imported_by, total_records, accepted_records, rejected_records,
        accepted_amount, rejected_amount, reconciled_at, status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        stmt_id, org_id, org_name, "2026-09-01", "2026-09-30", "Вересень 26.xlsx",
        "2026-10-06 20:30:00", "Економіст відділу моніторингу", line_number - 1, accepted_cnt, rejected_cnt,
        total_acc_amt, total_rej_amt, "2026-10-06 20:35:00", "RECONCILED"
    ))

    conn.commit()
    print(f"Statement {stmt_id} created with {line_number-1} lines.")
    print(f"Accepted: {accepted_cnt} ({total_acc_amt:,.2f} UAH), Rejected: {rejected_cnt} ({total_rej_amt:,.2f} UAH).")
    print(f"Added 5 invisible defektura cases to mis_encounter.")
    conn.close()

if __name__ == '__main__':
    seed_statements_and_encounters()
