import sqlite3
import json

conn = sqlite3.connect(r'c:\__MEDLINK___\PMG\pmg_database.sqlite')
cur = conn.cursor()

# Check encounters services in mis_encounter and dsg_nszu_statement_line
print("=== SERVICES IN STATEMENTS & ENCOUNTERS ===")
cur.execute("SELECT DISTINCT primary_service_code FROM dsg_nszu_statement_line WHERE primary_service_code IS NOT NULL AND primary_service_code != '' LIMIT 20")
stmt_svcs = [r[0] for r in cur.fetchall()]
print("Sample Statement Services:", stmt_svcs)

cur.execute("SELECT DISTINCT service_code FROM mis_encounter WHERE service_code IS NOT NULL AND service_code != '' LIMIT 20")
mis_svcs = [r[0] for r in cur.fetchall()]
print("Sample MIS Services:", mis_svcs)

cur.execute("SELECT DISTINCT service_code, required_position_code, required_position_name FROM dsg_doctor_position_rule LIMIT 10")
rules = cur.fetchall()
print("\nSample Doctor Position Rules:")
for r in rules:
    print(f"  Service: {r[0]}, Positions: {r[1]}, Name: {r[2]}")

conn.close()
