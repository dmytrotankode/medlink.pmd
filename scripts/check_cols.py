import sqlite3

conn = sqlite3.connect(r'c:\__MEDLINK___\PMG\pmg_database.sqlite')
cur = conn.cursor()

for tbl in ['dsg_nszu_statement_line', 'mis_encounter']:
    cur.execute(f"PRAGMA table_info({tbl})")
    cols = [r[1] for r in cur.fetchall()]
    print(f"Table {tbl} columns: {cols}")

conn.close()
