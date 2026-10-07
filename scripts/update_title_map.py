HTML_PATH = r"c:\__MEDLINK___\PMG\prototype_medlink\index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    text = f.read()

target = "'audit': 'Моніторинг та аудит тарифів ПМГ',"
replacement = "'audit': 'Моніторинг та аудит тарифів ПМГ',\n            'reconciliation': '2-Way Звірка (Звіт НСЗУ ↔ МІС «Медлінк»)',"

if target in text:
    text = text.replace(target, replacement)
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print("Updated currentViewTitle map successfully!")
else:
    print("Target not found.")
