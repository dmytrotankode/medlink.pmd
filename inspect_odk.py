with open(r"C:\Projects\MedProfit2\DCTImport\fmDctMPServiceODK\fDctMPServiceODK.pas", "r", encoding="windows-1251", errors="ignore") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, l in enumerate(lines):
    if any(k in l.lower() for k in ['excel', 'import', 'insert into', 'sheet', 'odk', 'rule', 'fieldbyname', 'open']):
        print(f"L{i+1}: {l.strip()[:100]}")
