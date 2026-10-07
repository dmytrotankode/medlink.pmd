import urllib.request
import json

url = "https://info-pmg.com/serve.php?f=json/additional-requirements-templates"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode('utf-8'))

with open("c:/__MEDLINK___/PMG/additional_requirements_templates.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Downloaded templates successfully!")
print("Top keys:", list(data.keys()))
for k, v in data.items():
    if isinstance(v, dict):
        print(f"Key '{k}': {len(v)} entries, sample keys: {list(v.keys())[:5]}")
    elif isinstance(v, list):
        print(f"Key '{k}': list with {len(v)} items")
