with open(r"C:\Projects\MedProfit\fMain.pas", "r", encoding="windows-1251", errors="ignore") as f:
    lines = f.readlines()

for i in range(2180, min(2580, len(lines))):
    l = lines[i].rstrip()
    if any(k in l.lower() for k in ['sql', 'query', 'service', 'group', 'detail', 'select', 'insert', 'delete', 'update', 'caption']):
        print(f"L{i+1}: {l}")
