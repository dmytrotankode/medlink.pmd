import sqlite3
conn = sqlite3.connect(r'c:\__MEDLINK___\PMG\pmg_database.sqlite')
r = conn.cursor().execute("SELECT service_code, required_position_code, required_position_name FROM dsg_doctor_position_rule LIMIT 5").fetchall()
print("Sample rules:", r)
r2 = conn.cursor().execute("SELECT service_code, required_position_code FROM dsg_doctor_position_rule WHERE service_code LIKE '%32003%'").fetchall()
print("32003 rules:", r2)
