import sqlite3

conn = sqlite3.connect(r'c:\__MEDLINK___\PMG\pmg_database.sqlite')
cursor = conn.cursor()
tables = [r[0] for r in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("Tables in pmg_database.sqlite:", tables)

for t in tables[:10]:
    cnt = cursor.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
    print(f"  {t}: {cnt} rows")

conn.close()
