import psycopg2

conn = psycopg2.connect(
    host='192.168.255.1',
    port=5432,
    dbname='evomis-test',
    user='d.tanko',
    password=r'u37[kDm4f=.*{49j=S\!.O'
)
cur = conn.cursor()

print("=== EF MIGRATIONS IN EVOMIS-TEST ===")
cur.execute('SELECT "MigrationId" FROM "__EFMigrationsHistory" ORDER BY "MigrationId" DESC LIMIT 20;')
for r in cur.fetchall():
    print(r[0])

print("\n=== TOTAL TABLES IN EVOMIS-TEST ===")
cur.execute("""
    SELECT table_name FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND (table_name ILIKE '%pmg%' OR table_name ILIKE '%tariff%' OR table_name ILIKE '%nszu%' OR table_name ILIKE '%dsg%');
""")
for r in cur.fetchall():
    print(r[0])

cur.close()
conn.close()
