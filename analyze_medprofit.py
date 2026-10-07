import re

file_path = r"C:\Projects\MedProfit\fMain.pas"
with open(file_path, "r", encoding="windows-1251", errors="ignore") as f:
    lines = f.readlines()

print(f"Total lines in fMain.pas: {len(lines)}")

# Search for interesting procedure / function declarations
proc_lines = [f"Line {i+1}: {l.strip()}" for i, l in enumerate(lines) if re.match(r'^(procedure|function)\b', l.strip(), re.I)]
print(f"Procedures/Functions count: {len(proc_lines)}")
for p in proc_lines[:30]:
    print(" ", p)

# Search for SQL or calculation keywords
calc_lines = [f"Line {i+1}: {l.strip()}" for i, l in enumerate(lines) if any(k in l.lower() for k in ['select ', 'insert ', 'update ', 'tariff', 'nszu', 'нсзу', 'dsg', 'дсг', 'коеф', 'stavka', 'ставка'])]
print(f"\nSQL/Tariff lines count: {len(calc_lines)}")
for c in calc_lines[:30]:
    print(" ", c)
