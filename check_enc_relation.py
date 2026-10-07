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
    SELECT DISTINCT main_entity_name, related_entity_name, relation_type
    FROM ehe_entity_relation
    WHERE main_entity_name ILIKE '%encounter%' OR related_entity_name ILIKE '%encounter%'
    LIMIT 20;
""")
rows = cur.fetchall()
print("Encounter relations in ehe_entity_relation:")
for r in rows:
    print(' ', r)

cur.close()
conn.close()
