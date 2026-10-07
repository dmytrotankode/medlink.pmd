with open(r"C:\Projects\MedProfit\fMain.pas", "r", encoding="windows-1251", errors="ignore") as f:
    lines = f.readlines()

print("--- SEARCHING FOR 'service' or 'услуг' or 'комбина' or 'норм' or 'методик' in fMain.pas ---")
for i, line in enumerate(lines):
    l_lower = line.lower()
    if any(k in l_lower for k in ['service_group', 'myservice', 'tservice', 'method', 'norm', 'combin', 'tariff', 'calc', 'diag', 'akpi']):
        if any(keyword in l_lower for keyword in ['procedure', 'function', 'select', 'where', 'sql.text', 'caption', 'btn']):
            print(f"L{i+1}: {line.strip()[:100]}")
