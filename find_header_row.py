import pandas as pd
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\__MEDLINK___\серпень 2.xlsx"
df = pd.read_excel(path, sheet_name='Розшифровка', header=None, nrows=6)
for r in range(len(df)):
    print(f"\n--- ROW {r} ---")
    row_vals = [f"Col {c}: {df.iloc[r, c]}" for c in range(min(20, df.shape[1])) if pd.notna(df.iloc[r, c])]
    print(" | ".join(row_vals[:10]))
