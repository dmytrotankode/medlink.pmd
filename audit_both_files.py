import openpyxl
import pandas as pd
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

f1 = r"C:\__MEDLINK___\PMG\Вересень 26.xlsx"
f2 = r"C:\__MEDLINK___\PMG\02000334_SF_2026_08_20260910.xlsx"

def analyze_file(path):
    fname = os.path.basename(path)
    print(f"\n=======================================================")
    print(f"DEEP AUDIT OF: {fname}")
    print(f"=======================================================")
    
    # Read Rozshyfrovka
    df = pd.read_excel(path, sheet_name='Розшифровка', skiprows=3)
    print(f"Total rows in 'Розшифровка': {len(df)}")
    
    # Identify key columns by index (Col 0..44)
    # Col 0: Рік, Col 1: Місяць, Col 2: Тип ЕМЗ, Col 3: ID ЕМЗ, Col 5: Посада, Col 6: ПІБ лікаря
    # Col 17: Основний діагноз, Col 22: Інтервенції, Col 33: АДСГ, Col 34: Пакет послуг, Col 35: Номер послуги
    # Col 36: Статистика, Col 37: Включення до звіту, Col 38: Помилки, Col 39..42: Деталі помилок
    
    col_emz = df.columns[3]
    col_doc_pos = df.columns[5]
    col_doc_name = df.columns[6]
    col_diag = df.columns[17]
    col_svc = df.columns[22]
    col_adsg = df.columns[33]
    col_pkg = df.columns[34]
    col_included = df.columns[37]
    col_err_comm = df.columns[38]
    col_err_det = df.columns[39]
    col_err_group = df.columns[41]

    # Package distribution
    pkg_counts = df[col_pkg].value_counts(dropna=False)
    print("\n--- Package Distribution (Top 8) ---")
    for pkg, cnt in pkg_counts.head(8).items():
        print(f"  Пакет {pkg}: {cnt} ЕМЗ ({(cnt/len(df)*100):.1f}%)")

    # Status: Included vs Rejected
    inc_counts = df[col_included].value_counts(dropna=False)
    print("\n--- Inclusion in NHSU Report (Status) ---")
    accepted_cnt = 0
    rejected_cnt = 0
    for stat, cnt in inc_counts.items():
        print(f"  '{stat}': {cnt} ЕМЗ ({(cnt/len(df)*100):.1f}%)")
        if str(stat).strip().lower() in ['так', 'yes', '1']:
            accepted_cnt += cnt
        else:
            rejected_cnt += cnt

    # Common errors in rejected records
    rejected_df = df[~df[col_included].astype(str).str.strip().str.lower().isin(['так', 'yes', '1'])]
    print(f"\n--- Rejected Records Analysis ({len(rejected_df)} records) ---")
    
    # Top error comments
    err_counts = rejected_df[col_err_comm].value_counts(dropna=False)
    print("Top Error Reasons (Column 38):")
    for err, cnt in err_counts.head(6).items():
        err_str = str(err)[:120].replace('\n', ' ')
        print(f"  [{cnt} разів]: {err_str}")

    # Top grouping conflict details (Column 41)
    if col_err_group in rejected_df.columns:
        group_counts = rejected_df[col_err_group].dropna().value_counts()
        if len(group_counts) > 0:
            print("\nTop Grouping Conflict Details (Column 41):")
            for err, cnt in group_counts.head(5).items():
                print(f"  [{cnt} разів]: {str(err)[:120]}")

    # Financial estimation:
    # How much money is involved?
    # Estimate accepted revenue vs lost revenue
    # Inpatient base rate = 8735, avg coeff ~ 2.5 * 0.55 = ~12,000 UAH
    # Outpatient base rate = 155, avg coeff ~ 1.5 = ~230 UAH
    # Chemo / onco package ~ 17,865 UAH
    
    total_est_sum = 0
    lost_est_sum = 0
    
    for _, row in df.iterrows():
        pkg = str(row[col_pkg]).strip()
        diag = str(row[col_diag]).strip()
        is_acc = str(row[col_included]).strip().lower() in ['так', 'yes', '1']
        
        # Estimate tariff
        tariff = 0
        if pkg in ['3', '4', '47']:
            tariff = 8735.0 * 2.2 * 0.55 # ~10,500 грн
        elif pkg == '9':
            tariff = 155.0 * 1.35 # ~209 грн
        elif pkg in ['17', '18']:
            tariff = 17865.0
        elif pkg in ['24']:
            tariff = 10000.0
        elif pkg in ['27']:
            tariff = 512.0
        else:
            tariff = 1200.0
            
        if is_acc:
            total_est_sum += tariff
        else:
            lost_est_sum += tariff
            
    print(f"\n--- Financial Impact Estimate ---")
    print(f"  Accepted estimated revenue: {total_est_sum:,.2f} UAH")
    print(f"  LOST REVENUE due to errors: {lost_est_sum:,.2f} UAH ({(lost_est_sum/(total_est_sum+lost_est_sum)*100):.1f}% lost!)")

analyze_file(f1)
analyze_file(f2)
