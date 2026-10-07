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

print("=== COLUMNS OF ehe_entity_relation ===")
cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_schema = 'public' AND table_name = 'ehe_entity_relation'
    ORDER BY ordinal_position;
""")
for c in cur.fetchall():
    print(f"  {c[0]} ({c[1]})")

print("\n=== SAMPLE ehe_entity_relation ===")
cur.execute("""
    SELECT * FROM ehe_entity_relation LIMIT 5;
""")
for r in cur.fetchall():
    print(' ', r)

cur.close()
conn.close()
