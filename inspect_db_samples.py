import psycopg2
import json

conn = psycopg2.connect(
    host='192.168.255.1',
    port=5432,
    dbname='evomis-test',
    user='d.tanko',
    password=r'u37[kDm4f=.*{49j=S\!.O'
)
cur = conn.cursor()

# Check count of Encounters
cur.execute('SELECT count(*) FROM "Encounters";')
print('Encounters count:', cur.fetchone()[0])

# Check sample Encounter
cur.execute('SELECT "Id", "RecordState", "Status", "EhealthId", "JsonData" FROM "Encounters" WHERE "JsonData" IS NOT NULL LIMIT 1;')
row = cur.fetchone()
if row:
    enc_id, rstate, status, eh_id, js = row
    print(f'Sample Encounter: Id={enc_id}, Status={status}, EhealthId={eh_id}')
    try:
        data = json.loads(js)
        print('JsonData keys:', list(data.keys()))
        if 'period' in data:
            print('period:', data.get('period'))
        if 'class' in data:
            print('class:', data.get('class'))
        if 'diagnoses' in data:
            print('diagnoses:', data.get('diagnoses')[:2])
        if 'actions' in data:
            print('actions:', data.get('actions')[:2])
        if 'performer' in data:
            print('performer:', data.get('performer'))
    except Exception as e:
        print('JSON parse error:', e)

# Check dsg_tariff_setting
print('\n=== dsg_tariff_setting ===')
cur.execute('SELECT * FROM dsg_tariff_setting;')
for r in cur.fetchall():
    print(' ', r)

# Check dsg_group_weight sample
print('\n=== dsg_group_weight sample ===')
cur.execute('SELECT caption, weight_coef, multi_ops_weight_coef, attributes FROM dsg_group_weight LIMIT 5;')
for r in cur.fetchall():
    print(' ', r)

# Check dsg_rule_config sample
print('\n=== dsg_rule_config sample ===')
cur.execute('SELECT id, record_state, caption FROM dsg_rule_config LIMIT 5;')
for r in cur.fetchall():
    print(' ', r)

cur.close()
conn.close()
