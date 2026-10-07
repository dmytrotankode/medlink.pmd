import sqlite3

conn = sqlite3.connect(r'c:\__MEDLINK___\PMG\pmg_database.sqlite')
cur = conn.cursor()

for tbl in ['pmg_dsg_services', 'pmg_dsg_diagnoses', 'dsg_doctor_position_rule', 'dsg_laboratory_test', 'pmg_package9_classes']:
    cur.execute(f"SELECT COUNT(*) FROM {tbl}")
    cnt = cur.fetchone()[0]
    print(f"Table {tbl}: {cnt} rows")
    cur.execute(f"PRAGMA table_info({tbl})")
    cols = [r[1] for r in cur.fetchall()]
    print(f"  Columns: {cols}")
    cur.execute(f"SELECT * FROM {tbl} LIMIT 2")
    print(f"  Sample: {cur.fetchall()}")

conn.close()
