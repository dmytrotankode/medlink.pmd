import re

with open(r"C:\Projects\MedProfit\fMain.pas", "r", encoding="windows-1251", errors="ignore") as f:
    text = f.read()

tabs = re.findall(r'(\w+):\s*TcxTabSheet;', text)
print("Tabs:", tabs)

queries = re.findall(r'(\w+):\s*TMyQuery;', text)
print("Queries:", queries)
