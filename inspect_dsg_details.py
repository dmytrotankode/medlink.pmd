import psycopg2

conn = psycopg2.connect(
    host='192.168.255.1',
    port=5432,
    dbname='evomis-test',
    user='d.tanko',
    password=r'u37[kDm4f=.*{49j=S\!.O'
)
cur = conn.cursor()

print("=== dsg_organization_profile ===")
cur.execute('SELECT * FROM dsg_organization_profile;')
for r in cur.fetchall():
    print(' ', r)

print("\n=== dsg_rule_config (all 58 rows) ===")
cur.execute('SELECT id, caption FROM dsg_rule_config;')
for r in cur.fetchall():
    print(' ', r)

print("\n=== dsg_analysis_audit_log ===")
cur.execute('SELECT * FROM dsg_analysis_audit_log LIMIT 5;')
for r in cur.fetchall():
    print(' ', r)

print("\n=== dsg_analysis_result ===")
cur.execute('SELECT * FROM dsg_analysis_result;')
for r in cur.fetchall():
    print(' ', r)

cur.close()
conn.close()
