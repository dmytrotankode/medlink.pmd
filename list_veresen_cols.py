import pandas as pd
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\__MEDLINK___\PMG\Вересень 26.xlsx"
df_cols = pd.read_excel(path, sheet_name='Розшифровка', header=None, skiprows=3, nrows=2)
print("=== All 45 Columns in Вересень 26.xlsx ===")
for c in range(df_cols.shape[1]):
    print(f"Col {c:2d}: {df_cols.iloc[0, c]}")
