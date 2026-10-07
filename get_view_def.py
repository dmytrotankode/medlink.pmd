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
    SELECT definition FROM pg_views 
    WHERE schemaname = 'public' AND viewname = 'vw_encounters';
""")
row = cur.fetchone()
if row:
    print("=== vw_encounters DEFINITION ===")
    print(row[0])

cur.close()
conn.close()
