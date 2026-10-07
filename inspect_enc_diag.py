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

print("=== COLUMNS OF mis_encounter_diagnosis ===")
cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_schema = 'public' AND table_name = 'mis_encounter_diagnosis'
    ORDER BY ordinal_position;
""")
for c in cur.fetchall():
    print(f"  {c[0]} ({c[1]})")

print("\n=== SAMPLE mis_encounter_diagnosis ===")
cur.execute("""
    SELECT ed.id, ed.encounter_id, ed.condition_id, ed.role_code, ed.rank, 
           c.code, c.caption
    FROM mis_encounter_diagnosis ed
    LEFT JOIN ehe_condition c ON ed.condition_id = c.id
    LIMIT 3;
""")
try:
    for r in cur.fetchall():
        print(' ', r)
except Exception as e:
    print("Error joining ehe_condition, let's select raw:", e)
    conn.rollback()
    cur.execute("SELECT * FROM mis_encounter_diagnosis LIMIT 3;")
    for r in cur.fetchall():
        print(' ', r)

cur.close()
conn.close()
