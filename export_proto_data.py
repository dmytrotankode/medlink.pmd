import sqlite3
import json
import pandas as pd
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

db_path = "c:/__MEDLINK___/PMG/pmg_database.sqlite"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Packages meta
cursor.execute("SELECT package_id, name, base_rate, meta_json FROM pmg_packages")
packages = []
for r in cursor.fetchall():
    packages.append({
        'id': r[0],
        'name': r[1],
        'base_rate': r[2],
        'meta': json.loads(r[3]) if r[3] else {}
    })

# 2. Key DSGs for packages 3, 4, 47
cursor.execute("""
SELECT id, package_id, drg_name, coefficient, coeff_numeric, base_rate, price,
       additional_requirements, req_package_1, diag_count, svc_count,
       diags_json, services_json
FROM pmg_dsg
ORDER BY package_id, id
""")
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
        # Sample of diags and svcs
        'sample_diags': diags[:15],
        'sample_svcs': svcs[:15]
    })

# 3. Package 9 Classes
cursor.execute("""
SELECT id, service_id_name, class_name, class_number, coefficient, cost,
       diag_count, svc_count, pos_count, svc_codes_json
FROM pmg_package9_classes
ORDER BY class_number
""")
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
cursor.execute("""
SELECT diag_code, diag_name, ar_groups, cr_code, cr_group, is_main, is_main_note, note
FROM pmg_package54_rehab
LIMIT 60
""")
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

# 5. Real report data from серпень 2.xlsx
report_path = r"C:\__MEDLINK___\серпень 2.xlsx"
df_rozsh = pd.read_excel(report_path, sheet_name='Розшифровка', skiprows=2, nrows=100)
report_records = []

for idx, row in df_rozsh.iterrows():
    emz_id = str(row.iloc[3]) if pd.notna(row.iloc[3]) else f"emz-{idx}"
    doc_pos = str(row.iloc[6]) if pd.notna(row.iloc[6]) else ""
    doc_name = str(row.iloc[7]) if pd.notna(row.iloc[7]) else ""
    date_emz = str(row.iloc[5]) if pd.notna(row.iloc[5]) else ""
    diag_main = str(row.iloc[18]) if pd.notna(row.iloc[18]) else ""
    diag_extra = str(row.iloc[21]) if pd.notna(row.iloc[21]) else ""
    services = str(row.iloc[23]) if pd.notna(row.iloc[23]) else ""
    patient_code = str(row.iloc[29]) if pd.notna(row.iloc[29]) else f"P-{120000+idx}"
    age_val = row.iloc[32]
    age = int(age_val) if pd.notna(age_val) and str(age_val).isdigit() else 55
    adsg = str(row.iloc[34]) if pd.notna(row.iloc[34]) else ""
    pkg_num = str(row.iloc[35]) if pd.notna(row.iloc[35]) else ""
    included_stat = str(row.iloc[37]) if pd.notna(row.iloc[37]) else ""
    included_report = str(row.iloc[38]) if pd.notna(row.iloc[38]) else ""
    err_comment = str(row.iloc[39]) if pd.notna(row.iloc[39]) else ""
    err_details = str(row.iloc[40]) if pd.notna(row.iloc[40]) else ""
    err_grouping = str(row.iloc[42]) if len(row) > 42 and pd.notna(row.iloc[42]) else ""

    # Status determination
    status = "accepted" if included_report.strip().lower() in ['так', 'yes', '1'] else "rejected"
    if status == "rejected" and not err_comment and not err_details and not err_grouping:
        err_comment = "Відхилено автоматичною валідацією НСЗУ (невідповідність умов закупівлі)"

    report_records.append({
        'id': idx + 1,
        'emz_id': emz_id,
        'patient_id': patient_code,
        'doc_name': doc_name,
        'doc_pos': doc_pos,
        'date': date_emz[:10],
        'diag_main': diag_main,
        'diag_extra': diag_extra,
        'services': services,
        'age': age,
        'adsg': adsg,
        'package': pkg_num,
        'status': status,
        'included': included_report,
        'error_comment': err_comment,
        'error_details': err_details,
        'error_grouping': err_grouping
    })

data_export = {
    'packages': packages,
    'dsgs': dsgs,
    'pkg9_classes': pkg9_classes,
    'pkg54_sample': pkg54_sample,
    'report_records': report_records
}

os.makedirs("c:/__MEDLINK___/PMG/prototype", exist_ok=True)
with open("c:/__MEDLINK___/PMG/prototype/prototype_data.json", "w", encoding="utf-8") as f:
    json.dump(data_export, f, ensure_ascii=False, indent=2)

print("Exported prototype data successfully!")
print(f"Total DSGs exported: {len(dsgs)}")
print(f"Total Package 9 classes: {len(pkg9_classes)}")
print(f"Total real report records exported: {len(report_records)}")
conn.close()
