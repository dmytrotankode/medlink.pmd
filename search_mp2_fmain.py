with open(r"C:\Projects\MedProfit2\fMain\fMain.pas", "r", encoding="windows-1251", errors="ignore") as f:
    text = f.read()

print("Length of MedProfit2 fMain.pas:", len(text))
lines = text.split('\n')
for i, l in enumerate(lines):
    if any(k in l.lower() for k in ['ehealth', 'drg', 'tariff', 'calculate', 'calc', 'patient', 'encounter', '53', '54']):
        print(f"L{i+1}: {l.strip()[:100]}")
