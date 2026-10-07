import psycopg2
import uuid
from datetime import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== STARTING END-TO-END PROCESS TEST AGAINST evomis-test ===")

conn = psycopg2.connect(
    host='192.168.255.1',
    port=5432,
    dbname='evomis-test',
    user='d.tanko',
    password=r'u37[kDm4f=.*{49j=S\!.O'
)
conn.autocommit = False
cur = conn.cursor()

try:
    # 1. Check existing encounters with ehealth_id in mis_encounter
    cur.execute('''
        SELECT id, ehealth_id, organization_id, employee_id, department_id 
        FROM mis_encounter 
        WHERE ehealth_id IS NOT NULL 
        LIMIT 5;
    ''')
    existing_encounters = cur.fetchall()
    print(f"1. Found {len(existing_encounters)} sample clinical encounters in mis_encounter:")
    for enc in existing_encounters:
        print(f"   - MIS ID: {enc[0]} | eHealth ID: {enc[1]}")

    test_stmt_id = str(uuid.uuid4())
    org_id = existing_encounters[0][2] if existing_encounters else str(uuid.uuid4())

    # 2. Insert test statement header
    cur.execute('''
        INSERT INTO dsg_nszu_statement 
        (id, record_state, caption, organization_id, period_from, period_to, file_name, imported_at)
        VALUES (%s, 2, %s, %s, %s, %s, %s, %s);
    ''', (
        test_stmt_id,
        "Тестовий звіт НСЗУ (E2E Перевірка)",
        org_id,
        datetime(2026, 9, 1),
        datetime(2026, 9, 30),
        "E2E_Test_Report_2026.xlsx",
        datetime.utcnow()
    ))
    print(f"2. Successfully created statement in dsg_nszu_statement: ID = {test_stmt_id}")

    # 3. Insert test statement lines:
    # Line 1: Matches an existing encounter in MIS
    # Line 2: Another match with mountain flag
    # Line 3: External encounter not in MIS (unmatched)
    sample_ehealth_id_1 = existing_encounters[0][1] if existing_encounters else str(uuid.uuid4())
    sample_ehealth_id_2 = existing_encounters[1][1] if len(existing_encounters) > 1 else str(uuid.uuid4())
    unmatched_ehealth_id = str(uuid.uuid4())

    lines_to_insert = [
        (str(uuid.uuid4()), test_stmt_id, sample_ehealth_id_1, "B72", "4", 0.0, 0),
        (str(uuid.uuid4()), test_stmt_id, sample_ehealth_id_2, "R02A", "47", 0.0, 0),
        (str(uuid.uuid4()), test_stmt_id, unmatched_ehealth_id, "E65B", "3", 0.0, 0)
    ]

    for line_id, stmt_id, eh_id, dsg, pkg, amt, st in lines_to_insert:
        cur.execute('''
            INSERT INTO dsg_nszu_statement_line
            (id, record_state, statement_id, encounter_ehealth_id, dsg_code, package_number, nszu_amount, match_status)
            VALUES (%s, 2, %s, %s, %s, %s, %s, %s);
        ''', (line_id, stmt_id, eh_id, dsg, pkg, amt, st))
    print(f"3. Inserted {len(lines_to_insert)} lines into dsg_nszu_statement_line")

    # 4. Run 2-Way Reconciliation Query (matches by ehealth_id)
    cur.execute('''
        UPDATE dsg_nszu_statement_line sl
        SET matched_encounter_id = e.id,
            match_status = 1
        FROM mis_encounter e
        WHERE sl.encounter_ehealth_id = e.ehealth_id
        AND sl.statement_id = %s;
    ''', (test_stmt_id,))
    matched_count = cur.rowcount
    print(f"4. 2-Way Reconciliation executed: matched {matched_count} rows with mis_encounter!")

    # 5. Tariff Engine Execution (Resolution No. 1808)
    # Base rate = 8735.0, B72 weight = 2.101, surgical k=0.60
    # R02A weight = 3.0, chemo k=0.55
    tariff_b72 = round(8735.0 * 2.101 * 0.60, 2)
    tariff_r02a = round(8735.0 * 3.0 * 0.55, 2)

    cur.execute('''
        UPDATE dsg_nszu_statement_line
        SET mis_amount = %s,
            difference = %s - nszu_amount
        WHERE statement_id = %s AND dsg_code = 'B72';
    ''', (tariff_b72, tariff_b72, test_stmt_id))

    cur.execute('''
        UPDATE dsg_nszu_statement_line
        SET mis_amount = %s,
            difference = %s - nszu_amount
        WHERE statement_id = %s AND dsg_code = 'R02A';
    ''', (tariff_r02a, tariff_r02a, test_stmt_id))
    print(f"5. Tariffs computed: B72 = {tariff_b72} ₴, R02A = {tariff_r02a} ₴")

    # 6. Verify and output results
    cur.execute('''
        SELECT dsg_code, package_number, encounter_ehealth_id, matched_encounter_id, mis_amount, match_status
        FROM dsg_nszu_statement_line
        WHERE statement_id = %s;
    ''', (test_stmt_id,))
    results = cur.fetchall()
    print("\n=== RECONCILIATION & TARIFF RESULTS ===")
    for r in results:
        status_label = "MATCHED (Звірено)" if r[5] == 1 else "UNMATCHED (Нема в МІС)"
        print(f"   ДСГ: {r[0]} (Пакет {r[1]}) | eHealth: {r[2]} | МІС ID: {r[3]} | Сума: {r[4]} ₴ | Статус: {status_label}")

    # Roll back so we leave the test DB clean
    conn.rollback()
    print("\n✓ E2E Process completed successfully! Transaction rolled back to keep DB clean.")

except Exception as e:
    conn.rollback()
    print("X E2E Test failed:", e)
finally:
    cur.close()
    conn.close()
