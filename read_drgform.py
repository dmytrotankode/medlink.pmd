with open(r"C:\Projects\MedProfit2\fDRGForm\fmDRGForm.pas", "r", encoding="windows-1251", errors="ignore") as f:
    text = f.read()

print("=== fmDRGForm.pas ===")
print(text[:2000])
