with open(r"C:\Projects\DSG\fMain.pas", "r", encoding="windows-1251", errors="ignore") as f:
    text = f.read()

print("Length of C:\\Projects\\DSG\\fMain.pas:", len(text))
lines = text.splitlines()
print("Lines:", len(lines))

for i, l in enumerate(lines[:100]):
    if any(k in l.lower() for k in ['type', 'procedure', 'function', 'class']):
        print(f"L{i+1}: {l.strip()}")
