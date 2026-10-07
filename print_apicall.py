with open("c:/__MEDLINK___/PMG/downloaded_js/js_stac-compiled.js", "r", encoding="utf-8") as f:
    stac_js = f.read()

idx = stac_js.find('function apiCall(')
print("=== stac apiCall ===")
print(stac_js[idx:idx+2000])

with open("c:/__MEDLINK___/PMG/downloaded_js/js_pkg9-compiled.js", "r", encoding="utf-8") as f:
    pkg9_js = f.read()

idx9 = pkg9_js.find('function apiCall9(')
print("\n=== pkg9 apiCall9 ===")
print(pkg9_js[idx9:idx9+2000])
