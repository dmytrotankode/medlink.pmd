import openpyxl
import pandas as pd
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

f1 = r"C:\__MEDLINK___\PMG\Вересень 26.xlsx"
f2 = r"C:\__MEDLINK___\PMG\02000334_SF_2026_08_20260910.xlsx"

for path in [f1, f2]:
    print(f"\n=======================================================")
    print(f"FILE: {os.path.basename(path)} ({os.path.getsize(path):,} bytes)")
    print(f"=======================================================")
    wb = openpyxl.load_workbook(path, read_only=True)
    print("Sheets:", wb.sheetnames)

    for sheet in wb.sheetnames:
        print(f"\n--- Sheet: '{sheet}' ---")
        try:
            # Read first 5 rows without header
            df = pd.read_excel(path, sheet_name=sheet, header=None, nrows=6)
            print(f"Shape preview: {df.shape}")
            for r in range(min(5, len(df))):
                vals = [f"[{c}]: {df.iloc[r, c]}" for c in range(min(15, df.shape[1])) if pd.notna(df.iloc[r, c])]
                if vals:
                    print(f"  Row {r}: " + " | ".join(vals[:8]))
        except Exception as e:
            print(f"  Error reading sheet: {e}")
