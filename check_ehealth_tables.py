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

cur.execute("""
    SELECT table_name FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND (table_name LIKE 'ehe_%' OR table_name LIKE 'ehd_%' OR table_name LIKE 'ehealth_%')
    ORDER BY table_name;
""")
tables = [r[0] for r in cur.fetchall()]
print(f"=== EHEALTH TABLES ({len(tables)}) ===")
for t in tables:
    cur.execute(f'SELECT count(*) FROM "{t}";')
    cnt = cur.fetchone()[0]
    if cnt > 0:
        print(f"  {t}: {cnt:,} rows")

cur.close()
conn.close()
