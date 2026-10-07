import re

with open("c:/__MEDLINK___/PMG/downloaded_js/js_pkg9-compiled.js", "r", encoding="utf-8") as f:
    text = f.read()

calls = set(re.findall(r'apiCall9\([\'"]([^\'"]+)[\'"]', text))
print("apiCall9 actions:", calls)
