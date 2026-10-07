import re

with open(r"C:\Projects\MedProfit\fMain.pas", "r", encoding="windows-1251", errors="ignore") as f:
    lines = f.readlines()

print("Header:")
for l in lines[:70]:
    print(l.rstrip())
