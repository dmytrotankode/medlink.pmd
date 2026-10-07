import psycopg2
import sys

sys.stdout.reconfigure(encoding='utf-8')

conn = psycopg2.connect(
    host='192.168.255.1',
    port=5432,
    dbname='evomis-test',
    user='d.tanko',
    password=r'u37[kDm4f=.*{49j=S\!.O'
)
cur = conn.cursor()

print("=== dsg_analysis_result ===")
cur.execute('SELECT * FROM dsg_analysis_result;')
for r in cur.fetchall():
    print(' ', r)

print("\n=== dsg_analysis_audit_log (sample 3) ===")
cur.execute('SELECT id, caption, created_on FROM dsg_analysis_audit_log LIMIT 3;')
for r in cur.fetchall():
    print(' ', r)

print("\n=== COLUMNS FOR dsg_analysis_result ===")
cur.execute('''
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = 'dsg_analysis_result'
    ORDER BY ordinal_position;
''')
for c in cur.fetchall():
    print(f'   {c[0]} ({c[1]})')

cur.close()
conn.close()
