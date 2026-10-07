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
    AND table_name ILIKE '%encounter%';
""")
tables = [r[0] for r in cur.fetchall()]
print("=== ENCOUNTER TABLES ===")
for t in tables:
    cur.execute(f'SELECT count(*) FROM "{t}";')
    cnt = cur.fetchone()[0]
    print(f'  {t}: {cnt:,} rows')

print("\n=== COLUMNS OF mis_encounter (or similar) ===")
for t in tables:
    if 'diagnosis' not in t and 'reason' not in t:
        cur.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'public' AND table_name = '{t}';
        """)
        cols = cur.fetchall()
        print(f"\nTable {t}:")
        for c in cols[:15]:
            print(f"  {c[0]} ({c[1]})")

cur.close()
conn.close()
