import sqlite3

conn = sqlite3.connect(r'c:\__MEDLINK___\PMG\pmg_database.sqlite')
cur = conn.cursor()

cur.execute("SELECT DISTINCT interventions FROM dsg_nszu_statement_line WHERE interventions IS NOT NULL AND interventions != '' LIMIT 15")
rows = cur.fetchall()
print("Distinct interventions in statements:")
for r in rows:
    print(" ", r[0])

cur.execute("SELECT DISTINCT interventions FROM mis_encounter WHERE interventions IS NOT NULL AND interventions != '' LIMIT 15")
rows_mis = cur.fetchall()
print("\nDistinct interventions in mis_encounter:")
for r in rows_mis:
    print(" ", r[0])

conn.close()
