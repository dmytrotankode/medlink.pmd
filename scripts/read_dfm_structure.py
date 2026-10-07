with open(r"C:\Projects\MedProfit\fMain.dfm", "r", encoding="windows-1251", errors="ignore") as f:
    text = f.read()

import re
tabs = re.findall(r'object (ts\w+): TcxTabSheet\s+Caption = \'([^\']+)\'', text)
print("=== TABS IN fMain.dfm ===")
for t_name, t_caption in tabs:
    print(f"Tab {t_name}: {t_caption}")

grids = re.findall(r'object (gr\w+): TcxGrid\b', text)
print("\n=== GRIDS IN fMain.dfm ===")
for g in grids:
    print(f"Grid: {g}")

sql_queries = re.findall(r'object (my\w+): TMyQuery[\s\S]*?SQL\.Strings = \(([\s\S]*?)\)', text)
print(f"\n=== TMyQuery OBJECTS IN fMain.dfm: {len(sql_queries)} queries ===")
for q_name, q_sql in sql_queries[:15]:
    cleaned_sql = ' '.join([line.strip().strip("'") for line in q_sql.splitlines() if line.strip() and not line.strip().startswith('object')])
    print(f"\nQuery {q_name}: {cleaned_sql[:200]}...")
