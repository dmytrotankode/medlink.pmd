import pandas as pd
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\__MEDLINK___\серпень 2.xlsx"

# Read row 2 (index 1) as header
df_rozsh = pd.read_excel(path, sheet_name='Розшифровка', header=1, nrows=3)
print("=== Розшифровка Columns (header=1) ===")
for i, col in enumerate(df_rozsh.columns):
    print(f"Col {i}: {col}")

df_err = pd.read_excel(path, sheet_name='Опис помилок', header=1, nrows=10)
print("\n=== Опис помилок Sample ===")
print(df_err.head(10))
