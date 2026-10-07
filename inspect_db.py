import psycopg2

conn = psycopg2.connect(
    host='192.168.255.1',
    port=5432,
    dbname='evomis-test',
    user='d.tanko',
    password=r'u37[kDm4f=.*{49j=S\!.O'
)
cur = conn.cursor()

# Check all dsg_* tables
cur.execute('''
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' AND table_name LIKE 'dsg_%'
    ORDER BY table_name;
''')
dsg_tables = [r[0] for r in cur.fetchall()]
print('=== DSG TABLES IN EVOMIS-TEST ===')
for t in dsg_tables:
    try:
        cur.execute(f'SELECT count(*) FROM "{t}";')
        cnt = cur.fetchone()[0]
        print(f'  {t}: {cnt} rows')
    except Exception as e:
        print(f'  {t}: ERROR {e}')
        conn.rollback()

print('\n=== COLUMNS FOR KEY DSG TABLES ===')
for t in ['dsg_codes', 'dsg_group_weight', 'dsg_package_codes', 'dsg_packages', 'dsg_nszu_statement', 'dsg_nszu_statement_line', 'dsg_tariff_setting']:
    if t in dsg_tables:
        cur.execute(f'''
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = '{t}'
            ORDER BY ordinal_position;
        ''')
        cols = cur.fetchall()
        print(f'\nTable {t}:')
        for c in cols:
            print(f'   {c[0]} ({c[1]}, nullable={c[2]})')

# Check sample data in dsg_packages & dsg_codes
print('\n=== SAMPLE DATA dsg_packages ===')
try:
    cur.execute('SELECT * FROM dsg_packages LIMIT 5;')
    rows = cur.fetchall()
    for r in rows:
        print(' ', r)
except Exception as e:
    print('Error:', e)
    conn.rollback()

# Check Encounters columns
print('\n=== COLUMNS FOR Encounters ===')
cur.execute('''
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = 'Encounters'
    ORDER BY ordinal_position;
''')
cols = cur.fetchall()
for c in cols[:30]:
    print(f'   {c[0]} ({c[1]}, nullable={c[2]})')
if len(cols) > 30:
    print(f'   ... and {len(cols) - 30} more columns')

cur.close()
conn.close()
