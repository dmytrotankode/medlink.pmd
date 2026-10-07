import glob
import re

for js_path in glob.glob("c:/__MEDLINK___/PMG/downloaded_js/*.js"):
    with open(js_path, "r", encoding="utf-8") as f:
        text = f.read()
    matches = re.finditer(r'/serve\.php\?f=info/([^"\'`\s\)]+)', text)
    for m in matches:
        print(f"[{js_path}] info match: {m.group(0)}")
    # also search for info/
    matches2 = re.finditer(r'[\'"]info/([^\'"]+)[\'"]', text)
    for m in matches2:
        print(f"[{js_path}] 'info/...' match: {m.group(0)}")
