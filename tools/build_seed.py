# -*- coding: utf-8 -*-
"""
MedLink PMG-2026 — побудова компактних seed-файлів для DatabaseSeeder (.NET 8 / EF Core SQLite).

Джерела:
  extracted_data/raw_json/package_{3,4,47}_full.json   -> seed/dsg.json (+ icd10_names.json, achi_names.json)
  extracted_data/raw_json/package_9_full.json
  extracted_data/sub_details/pkg9_class_details/*.json -> seed/pkg9_classes.json
  extracted_data/raw_json/package_54_full.json, pkg54_info.json -> seed/pkg54_rehab.json
  normative_packages/all_packages_manifest.json         -> seed/packages.json
  sql/04..11 (PostgreSQL / SQLite seeds)                 -> seed/{dsg_catalog,pkg9_catalog,errors,doctor_positions,lab_tests,rules,service_groups,service_catalog,service_combinations}.json

Запуск:  python tools/build_seed.py
"""
import json, os, re, sqlite3, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'extracted_data', 'raw_json')
SUB = os.path.join(ROOT, 'extracted_data', 'sub_details')
OUT = os.path.join(ROOT, 'seed')
os.makedirs(OUT, exist_ok=True)


def dump(name, obj):
    path = os.path.join(OUT, name)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))
    print(f'  {name:32} {os.path.getsize(path)/1024:9.1f} KB')


def split_code(s):
    """'B63 - Деменція ...' -> ('B63', 'Деменція ...')"""
    s = (s or '').strip()
    m = re.match(r'^(\S+)\s+-\s+(.*)$', s)
    if m:
        return m.group(1), m.group(2)
    m = re.match(r'^([A-Z0-9][A-Z0-9.\-]*)\s+(.*)$', s)
    if m:
        return m.group(1), m.group(2)
    return s, s


def first_num(s):
    s = str(s or '').replace('\xa0', '').replace(' ', '')
    m = re.search(r'[-+]?\d+(?:[.,]\d+)?', s)
    return float(m.group(0).replace(',', '.')) if m else 0.0


# ---------------------------------------------------------------- packages
manifest = json.load(open(os.path.join(ROOT, 'normative_packages', 'all_packages_manifest.json'), encoding='utf-8'))
dump('packages.json', manifest)

# ---------------------------------------------------------------- DSG (packages 3, 4, 47)
icd_names, achi_names = {}, {}
dsg_rows = []
for pkg in ('3', '4', '47'):
    d = json.load(open(os.path.join(RAW, f'package_{pkg}_full.json'), encoding='utf-8'))
    meta = d.get('meta', {})
    for r in d['rows']:
        code, name = split_code(r['drg'])
        diags, services = [], []
        for x in r.get('diags_structured', []):
            diags.append(x['code'])
            icd_names.setdefault(x['code'], x.get('name', ''))
        for x in r.get('services_structured', []):
            services.append(x['code'])
            achi_names.setdefault(x['code'], x.get('name', ''))
        notes = {}
        for k, v in (r.get('diag_notes') or {}).items():
            if isinstance(v, dict) and (v.get('children') == 'no' or v.get('adults') == 'no'):
                notes[k] = v
        dsg_rows.append({
            'pkg': pkg,
            'code': code,
            'name': name,
            'coefficient_text': str(r.get('coefficient', '')),
            'weight': first_num(r.get('coefficient')),
            'base_rate': float(meta.get('RATE', 8735.0)),
            'share': float(meta.get('COEFF', 0.55)),
            'full_tariff': float(r.get('base_rate_raw') or 0),
            'share_tariff': float(r.get('price_raw') or 0),
            'add_req': r.get('additional_requirements') or '',
            'add_req_code': r.get('additional_requirements_code') or '',
            'add_req_services': [split_code(x)[0] for x in (r.get('additional_requirements_code_btn') or [])],
            'add_req_referral': r.get('additional_requirements_referral') or '',
            'req_pkg': [p for p in (r.get('additional_requirements_package_1'), r.get('additional_requirements_package_2'), r.get('additional_requirements_package_3')) if p],
            'episode': r.get('episode') or '',
            'planned_coeff': 0.8 if 'coeff-0.8' in (r.get('badges_html') or '') else None,
            'diags': diags,
            'services': services,
            'age_notes': notes,
        })
dump('dsg.json', dsg_rows)
templates = json.load(open(os.path.join(RAW, 'additional_requirements_templates.json'), encoding='utf-8'))
dump('dsg_requirement_templates.json', templates)

# ---------------------------------------------------------------- package 9 (148 classes)
d9 = json.load(open(os.path.join(RAW, 'package_9_full.json'), encoding='utf-8'))
details = {}
for p in glob.glob(os.path.join(SUB, 'pkg9_class_details', 'class_*.json')):
    x = json.load(open(p, encoding='utf-8'))
    details[str(x['class_number'])] = x
pkg9 = []
for r in d9['rows']:
    cn = str(r['class_number'])
    det = details.get(cn, {})
    svc_codes = []
    for s in (det.get('services') or r.get('svc_codes') or []):
        c, n = split_code(s)
        svc_codes.append(c)
        achi_names.setdefault(c, n)
    diag_codes = []
    for x in det.get('diags') or []:
        diag_codes.append(x['code'])
        icd_names.setdefault(x['code'], x.get('name', ''))
    pkg9.append({
        'id': int(r['id']),
        'class_number': cn,
        'class_name': r['class'],
        'service_type': r['service_id'],
        'coefficient': first_num(r['coefficient']),
        'cost': first_num(r['cost']),
        'note': r.get('note'),
        'add_req_code': r.get('additional_requirements_code'),
        'episode': r.get('episode') or [],
        'services': svc_codes,
        'diags': diag_codes,
        'positions': det.get('positions') or [],
    })
dump('pkg9_classes.json', pkg9)

# ---------------------------------------------------------------- package 54 (rehab)
d54 = json.load(open(os.path.join(RAW, 'package_54_full.json'), encoding='utf-8'))
i54 = json.load(open(os.path.join(RAW, 'pkg54_info.json'), encoding='utf-8'))
dump('pkg54_rehab.json', {
    'rate': i54.get('rate', 10820.0),
    'name': i54.get('name'),
    'ar_groups': i54['ar_groups'],
    'diag_types': i54['diag_types'],
    'cr_rules': i54['cr_rules'],
    'services': i54['services'],
    'dagger_info': i54.get('dagger_info'),
    'rows': d54['rows'],
})

# ---------------------------------------------------------------- SQL seeds -> JSON via sqlite
def pg_to_sqlite(sql):
    sql = sql.replace('public.', '')
    sql = re.sub(r'SERIAL PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT', sql)
    sql = sql.replace("::jsonb", '').replace('::uuid', '').replace('::numeric', '')
    sql = re.sub(r"\(now\(\) AT TIME ZONE 'utc'\)", 'CURRENT_TIMESTAMP', sql)
    sql = re.sub(r"now\(\) AT TIME ZONE 'utc'", 'CURRENT_TIMESTAMP', sql)
    sql = sql.replace('TIMESTAMP WITHOUT TIME ZONE', 'TEXT')
    sql = re.sub(r'NUMERIC\(\d+,\s*\d+\)', 'REAL', sql)
    sql = re.sub(r'VARCHAR\(\d+\)', 'TEXT', sql)
    sql = sql.replace('BOOLEAN', 'INTEGER')
    sql = re.sub(r'\bTRUE\b', '1', sql)
    sql = re.sub(r'\bFALSE\b', '0', sql)
    sql = sql.replace('JSONB', 'TEXT')
    # drop ON CONFLICT ... clauses up to ';'
    sql = re.sub(r'ON CONFLICT[^;]*;', ';', sql, flags=re.S)
    # bare (unquoted) text values at tuple start, e.g. "(Тканинна патологія, '...'" -> quote them
    sql = re.sub(r"\n\(([^',\d(][^,]*),", r"\n('\1',", sql)
    sql = re.sub(r'INSERT INTO', 'INSERT OR IGNORE INTO', sql)
    sql = re.sub(r'INSERT OR IGNORE OR REPLACE', 'INSERT OR REPLACE', sql)
    sql = re.sub(r'gen_random_uuid\(\)', "lower(hex(randomblob(16)))", sql)
    sql = re.sub(r'^\s*(BEGIN|START TRANSACTION|COMMIT)\s*;\s*$', '', sql, flags=re.M)
    # drop statements that target MedLink core tables not present here
    sql = re.sub(r'INSERT OR IGNORE INTO dsg_group_weight[^;]*;', '', sql, flags=re.S)
    return sql


def load_sql_tables(files):
    conn = sqlite3.connect(':memory:')
    for f in files:
        sql = open(os.path.join(ROOT, 'sql', f), encoding='utf-8').read()
        conn.executescript(pg_to_sqlite(sql))
    return conn


def table_rows(conn, table, order='rowid'):
    cur = conn.execute(f'SELECT * FROM {table} ORDER BY {order}')
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


conn = load_sql_tables(['04_seed_dsg_catalog_465.sql', '05_seed_package9_classes_148.sql',
                        '06_seed_nhsu_error_dictionary_186.sql', '07_seed_doctor_position_requirements.sql',
                        '08_seed_laboratory_tests_408.sql', '09_seed_medprofit_rules_185.sql',
                        '11_seed_service_combinations_and_groups.sql'])

dsg_catalog = [{k: v for k, v in r.items() if k not in ('is_active', 'created_at')} for r in table_rows(conn, 'pmg_dsg_catalog')]
dump('dsg_catalog.json', dsg_catalog)
errors = [{k: v for k, v in r.items() if k not in ('is_active', 'created_at')} for r in table_rows(conn, 'pmg_nhsu_error_dictionary')]
dump('errors.json', errors)
positions = [{k: v for k, v in r.items() if k not in ('is_active', 'created_at')} for r in table_rows(conn, 'pmg_service_doctor_positions')]
for p in positions:
    achi_names.setdefault(p['service_code'], p['service_name'])
dump('doctor_positions.json', positions)
lab = [{k: v for k, v in r.items() if k not in ('is_active', 'created_at')} for r in table_rows(conn, 'pmg_laboratory_catalog')]
dump('lab_tests.json', lab)
rules = [{k: v for k, v in r.items() if k not in ('is_active', 'created_at')} for r in table_rows(conn, 'pmg_classification_rules')]
dump('rules.json', rules)
dump('service_groups.json', table_rows(conn, 'pmg_service_groups'))
dump('service_catalog.json', table_rows(conn, 'pmg_service_catalog'))
dump('service_combinations.json', table_rows(conn, 'pmg_service_combinations'))

dump('icd10_names.json', icd_names)
dump('achi_names.json', achi_names)
print('DSG rows:', len(dsg_rows), ' ICD-10 codes:', len(icd_names), ' ACHI codes:', len(achi_names),
      ' pkg9 classes:', len(pkg9), ' rehab rows:', len(d54['rows']), ' errors:', len(errors),
      ' positions:', len(positions), ' lab:', len(lab), ' rules:', len(rules))
