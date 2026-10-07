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

tables_to_check = [
    'Employees', 'Persons', 'Patients', 'HealthcareServices', 
    'Divisions', 'LegalEntities', 'Contracts', 'Episodes'
]

for t in tables_to_check:
    cur.execute(f'SELECT count(*) FROM "{t}";')
    cnt = cur.fetchone()[0]
    print(f'Table "{t}": {cnt} rows')

print("\n=== SAMPLE LegalEntities ===")
cur.execute('SELECT "Id", "Name", "Edrpou" FROM "LegalEntities" LIMIT 3;')
for r in cur.fetchall():
    print(' ', r)

print("\n=== SAMPLE Divisions ===")
cur.execute('SELECT "Id", "Name", "LegalEntityId" FROM "Divisions" LIMIT 3;')
for r in cur.fetchall():
    print(' ', r)

print("\n=== SAMPLE Employees ===")
cur.execute('SELECT "Id", "Position", "LegalEntityId", "PartyId" FROM "Employees" LIMIT 3;')
for r in cur.fetchall():
    print(' ', r)

print("\n=== SAMPLE HealthcareServices ===")
cur.execute('SELECT "Id", "Code", "Name" FROM "HealthcareServices" LIMIT 5;')
for r in cur.fetchall():
    print(' ', r)

cur.close()
conn.close()
