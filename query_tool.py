import sqlite3
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect("c:/__MEDLINK___/PMG/pmg_database.sqlite")
cursor = conn.cursor()

def test_query_diagnosis(diag):
    print(f"\n==================== DIAGNOSIS LOOKUP: {diag} ====================")
    cursor.execute("""
    SELECT d.package_id, d.drg_name, g.coefficient, g.base_rate, g.price, d.notes
    FROM pmg_dsg_diagnoses d
    JOIN pmg_dsg g ON d.package_id = g.package_id AND d.dsg_id = g.id
    WHERE d.diag_code = ?
    LIMIT 5
    """, (diag,))
    rows = cursor.fetchall()
    print(f"Found in {len(rows)} DSGs:")
    for r in rows:
        print(f"  Pkg {r[0]} | ДСГ: {r[1]} | Коеф: {r[2]} | Базова ставка: {r[3]} грн | Тариф: {r[4]} грн")

def test_query_rehab(diag):
    print(f"\n==================== REHAB LOOKUP: {diag} ====================")
    cursor.execute("""
    SELECT diag_code, diag_name, ar_groups, is_main, is_main_note, note
    FROM pmg_package54_rehab
    WHERE diag_code = ?
    """, (diag,))
    rows = cursor.fetchall()
    for r in rows:
        print(f"  {r[0]} - {r[1]}")
        print(f"    Групи АР: {r[2]} | Основний: {bool(r[3])} ({r[4]})")
        if r[5]:
            print(f"    Примітка: {r[5]}")

def test_query_pkg9(class_num):
    print(f"\n==================== PACKAGE 9 LOOKUP: Class {class_num} ====================")
    cursor.execute("""
    SELECT class_name, coefficient, cost, svc_codes_json
    FROM pmg_package9_classes
    WHERE class_number = ?
    """, (class_num,))
    row = cursor.fetchone()
    if row:
        svc_codes = json.loads(row[3])
        print(f"  Клас: {row[0]} | Коеф: {row[1]} | Тариф: {row[2]} грн | Послуг у класі: {len(svc_codes)}")
        print(f"  Приклади послуг: {svc_codes[:3]}")

test_query_diagnosis("I21.0")
test_query_diagnosis("K35.8")
test_query_rehab("I69.3")
test_query_pkg9(1)
conn.close()
