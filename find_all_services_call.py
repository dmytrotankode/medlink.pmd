import re

with open("c:/__MEDLINK___/PMG/downloaded_js/js_pkg9-compiled.js", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('all-services')
while idx != -1:
    print(text[max(0, idx-100):min(len(text), idx+300)])
    print("-" * 50)
    idx = text.find('all-services', idx+1)
