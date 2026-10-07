import re

with open("c:/__MEDLINK___/PMG/downloaded_js/js_stac-compiled.js", "r", encoding="utf-8") as f:
    stac_js = f.read()

m = re.search(r'function apiCall\(.*?\n\}', stac_js, re.DOTALL)
if m:
    print("=== apiCall in stac ===")
    print(m.group(0)[:1500])
else:
    # search where apiCall is defined
    idx = stac_js.find('apiCall(')
    print("=== apiCall context ===")
    print(stac_js[max(0, idx-100):idx+500])

with open("c:/__MEDLINK___/PMG/downloaded_js/js_pkg9-compiled.js", "r", encoding="utf-8") as f:
    pkg9_js = f.read()

m9 = re.search(r'function apiCall9\(.*?\n\}', pkg9_js, re.DOTALL)
if m9:
    print("=== apiCall9 in pkg9 ===")
    print(m9.group(0)[:1500])
else:
    idx9 = pkg9_js.find('function apiCall9')
    print("=== apiCall9 context ===")
    print(pkg9_js[idx9:idx9+1000])
