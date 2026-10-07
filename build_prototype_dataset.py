import openpyxl
import json
import sqlite3
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

db_path = 'c:/__MEDLINK___/PMG/pmg_database.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Packages meta
cursor.execute('SELECT package_id, name, base_rate, meta_json FROM pmg_packages')
packages = []
for r in cursor.fetchall():
    packages.append({
        'id': r[0],
        'name': r[1],
        'base_rate': r[2],
        'meta': json.loads(r[3]) if r[3] else {}
    })

# 2. Key DSGs
cursor.execute('''
SELECT id, package_id, drg_name, coefficient, coeff_numeric, base_rate, price,
       additional_requirements, req_package_1, diag_count, svc_count,
       diags_json, services_json
FROM pmg_dsg
ORDER BY package_id, id
''')
dsgs = []
for r in cursor.fetchall():
    diags = json.loads(r[11]) if r[11] else []
    svcs = json.loads(r[12]) if r[12] else []
    dsgs.append({
        'id': r[0],
        'package_id': r[1],
        'drg_name': r[2],
        'coefficient': r[3],
        'coeff_numeric': r[4],
        'base_rate': r[5],
        'price': r[6],
        'additional_requirements': r[7],
        'req_package_1': r[8],
        'diag_count': r[9],
        'svc_count': r[10],
        'sample_diags': diags[:15],
        'sample_svcs': svcs[:15]
    })

# 3. Package 9 Classes
cursor.execute('''
SELECT id, service_id_name, class_name, class_number, coefficient, cost,
       diag_count, svc_count, pos_count, svc_codes_json
FROM pmg_package9_classes
ORDER BY class_number
''')
pkg9_classes = []
for r in cursor.fetchall():
    pkg9_classes.append({
        'id': r[0],
        'service_id': r[1],
        'class_name': r[2],
        'class_number': r[3],
        'coefficient': r[4],
        'cost': r[5],
        'diag_count': r[6],
        'svc_count': r[7],
        'pos_count': r[8],
        'sample_svcs': (json.loads(r[9]) if r[9] else [])[:10]
    })

# 4. Package 54 Rehab sample
cursor.execute('''
SELECT diag_code, diag_name, ar_groups, cr_code, cr_group, is_main, is_main_note, note
FROM pmg_package54_rehab
LIMIT 80
''')
pkg54_sample = []
for r in cursor.fetchall():
    pkg54_sample.append({
        'code': r[0],
        'name': r[1],
        'ar': r[2],
        'cr_code': r[3],
        'cr_group': r[4],
        'is_main': bool(r[5]),
        'is_main_note': r[6],
        'note': r[7]
    })

conn.close()

# Error definitions from sheet 'Опис помилок'
wb_err = openpyxl.load_workbook('c:/__MEDLINK___/PMG/Вересень 26.xlsx', read_only=True)
ws_err = wb_err['Опис помилок']
error_dict = {}
for r in ws_err.iter_rows(values_only=True):
    non_empty = [v for v in r if v is not None]
    if len(non_empty) >= 2 and isinstance(non_empty[0], str) and len(non_empty[0]) > 3:
        error_dict[non_empty[0].strip()] = str(non_empty[1]).strip()

def process_file(filepath, name, edrpou, period, sample_target=200):
    wb = openpyxl.load_workbook(filepath, read_only=True)
    ws = wb['Розшифровка']
    rows = list(ws.iter_rows(values_only=True))
    total_rows = len(rows) - 4
    
    stats = {'total': total_rows, 'tak': 0, 'gb': 0, 'ni': 0, 'packages': {}, 'errors': {}}
    records = []
    
    # We want a high-value representative sample:
    # 1. Rejected records with errors (at least 70-80)
    # 2. Paid records (Так) (at least 50)
    # 3. Global budget records (ГБ) (at least 70)
    rejected_collected = 0
    tak_collected = 0
    gb_collected = 0
    
    for idx, r in enumerate(rows[4:]):
        if len(r) < 40: continue
        inc = str(r[37] or '').strip()
        pkg = str(r[34] or '').strip()
        err = str(r[38] or '').strip()
        
        if inc == 'Так': stats['tak'] += 1
        elif inc == 'ГБ': stats['gb'] += 1
        else: stats['ni'] += 1
        
        stats['packages'][pkg] = stats['packages'].get(pkg, 0) + 1
        if err and err != '-':
            stats['errors'][err] = stats['errors'].get(err, 0) + 1
            
        take = False
        if inc == 'Ні' and rejected_collected < 80:
            take = True
            rejected_collected += 1
        elif inc == 'Так' and tak_collected < 50:
            take = True
            tak_collected += 1
        elif inc == 'ГБ' and gb_collected < 70:
            take = True
            gb_collected += 1
        elif len(records) < sample_target and idx % 25 == 0:
            take = True

        if take:
            records.append({
                'id': len(records) + 1,
                'emz_id': str(r[3] or f'emz-{idx}'),
                'emz_type': str(r[2] or 'Взаємодія'),
                'date': str(r[4] or '')[:10],
                'doc_pos': str(r[5] or ''),
                'doc_name': str(r[6] or ''),
                'dept': str(r[7] or ''),
                'ref_type': str(r[8] or ''),
                'ref_edrpou': str(r[9] or ''),
                'ref_doc_pos': str(r[10] or ''),
                'episode_id': str(r[11] or ''),
                'episode_type': str(r[12] or ''),
                'start_date': str(r[13] or '')[:16],
                'end_date': str(r[15] or '')[:16],
                'los': int(r[16]) if r[16] and str(r[16]).isdigit() else 0,
                'diag_main': str(r[17] or ''),
                'diag_conf': str(r[18] or ''),
                'diag_clin': str(r[19] or ''),
                'diag_extra': str(r[20] or ''),
                'services': str(r[22] or ''),
                'interaction_class': str(r[23] or ''),
                'priority': str(r[24] or ''),
                'interaction_type': str(r[25] or ''),
                'admission_reason': str(r[26] or ''),
                'discharge_outcome': str(r[27] or ''),
                'patient_id': str(r[28] or f'P-{idx}'),
                'has_decl': str(r[29] or ''),
                'gender': str(r[30] or ''),
                'age': int(r[31]) if r[31] and str(r[31]).isdigit() else 0,
                'adsg': str(r[33] or ''),
                'package': pkg,
                'service_code': str(r[35] or ''),
                'stat_included': str(r[36] or ''),
                'included': inc,
                'error_comment': err if err != '-' else '',
                'error_details': str(r[39] or '') if str(r[39] or '') != '-' else '',
                'error_mismatches': str(r[40] or '') if str(r[40] or '') != '-' else '',
                'error_grouping': str(r[41] or '') if str(r[41] or '') != '-' else '',
                'nszu_review_details': str(r[42] or '') if str(r[42] or '') != '-' else '',
                'extra_notes': str(r[43] or '') if str(r[43] or '') != '-' else ''
            })

    return {
        'name': name,
        'edrpou': edrpou,
        'period': period,
        'filename': os.path.basename(filepath),
        'stats': stats,
        'records': records
    }

print("Processing report 1: Вересень 26.xlsx ...")
hosp_oco = process_file('c:/__MEDLINK___/PMG/Вересень 26.xlsx', 'КНП "Обласний центр онкології"', '40929168', 'Вересень 2026')
print(f"Done OCO: {len(hosp_oco['records'])} records sampled from {hosp_oco['stats']['total']}")

print("Processing report 2: 02000334_SF_2026_08_20260910.xlsx ...")
hosp_dkl = process_file('c:/__MEDLINK___/PMG/02000334_SF_2026_08_20260910.xlsx', 'КНП "ДКЛ Святої Зінаїди" СМР', '02000334', 'Серпень 2026')
print(f"Done DKL: {len(hosp_dkl['records'])} records sampled from {hosp_dkl['stats']['total']}")

data_export = {
    'packages': packages,
    'dsgs': dsgs,
    'pkg9_classes': pkg9_classes,
    'pkg54_sample': pkg54_sample,
    'error_dictionary': error_dict,
    'hospitals': {
        'oco': hosp_oco,
        'dkl': hosp_dkl
    }
}

out_json = 'c:/__MEDLINK___/PMG/prototype/prototype_data.json'
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(data_export, f, ensure_ascii=False, indent=2)

out_js = 'c:/__MEDLINK___/PMG/prototype/data.js'
with open(out_js, 'w', encoding='utf-8') as f:
    f.write('window.PROTOTYPE_DATA = ' + json.dumps(data_export, ensure_ascii=False) + ';\n')

print(f"Successfully generated {out_json} and {out_js}!")
