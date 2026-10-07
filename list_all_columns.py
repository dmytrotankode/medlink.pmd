import pandas as pd
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\__MEDLINK___\серпень 2.xlsx"
df = pd.read_excel(path, sheet_name='Розшифровка', header=None, skiprows=2, nrows=2)
for c in range(df.shape[1]):
    print(f"Col {c:2d}: {df.iloc[0, c]}")
