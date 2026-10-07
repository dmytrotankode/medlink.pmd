import re
with open("c:/__MEDLINK___/PMG/downloaded_js/js_nszu-analyzer-compiled.js", "r", encoding="utf-8") as f:
    text = f.read()

print("Length of nszu analyzer js:", len(text))
# Check for file input handling, Excel parsing, SheetJS, XLSX, PapaParse, upload to server, etc.
keywords = ['xlsx', 'read', 'upload', 'file', 'analyze', 'formData', 'post', 'fetch', 'drop', 'parse']
for kw in keywords:
    matches = [m.start() for m in re.finditer(re.escape(kw), text, re.I)]
    print(f"Keyword '{kw}': {len(matches)} occurrences")

# Find where files are read or posted
idx = text.find('fetch(')
while idx != -1:
    print("\nFetch occurrence:")
    print(text[max(0, idx-50):min(len(text), idx+250)])
    idx = text.find('fetch(', idx+1)
