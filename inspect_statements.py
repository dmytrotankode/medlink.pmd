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

for t in ['dsg_nszu_statement', 'dsg_nszu_statement_line']:
    print(f"\n=== COLUMNS OF {t} ===")
    cur.execute(f"""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_schema = 'public' AND table_name = '{t}'
        ORDER BY ordinal_position;
    """)
    for c in cur.fetchall():
        print(f"  {c[0]} ({c[1]}, nullable={c[2]}, default={c[3]})")

cur.close()
conn.close()
