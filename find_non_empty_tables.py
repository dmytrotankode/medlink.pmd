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
    SELECT table_schema, table_name 
    FROM information_schema.tables 
    WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
    ORDER BY table_name;
""")
all_tables = cur.fetchall()

non_empty = []
for schema, t in all_tables:
    try:
        cur.execute(f'SELECT count(*) FROM "{schema}"."{t}";')
        cnt = cur.fetchone()[0]
        if cnt > 0:
            non_empty.append((schema, t, cnt))
    except Exception as e:
        conn.rollback()

non_empty.sort(key=lambda x: x[2], reverse=True)
print(f"Total non-empty tables: {len(non_empty)}")
for schema, t, cnt in non_empty[:50]:
    print(f"  {schema}.{t}: {cnt:,} rows")

cur.close()
conn.close()
