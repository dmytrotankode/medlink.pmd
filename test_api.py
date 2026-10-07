import urllib.request
import urllib.parse
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base_url = "https://info-pmg.com/serve.php?"

def test_endpoint(params):
    qs = urllib.parse.urlencode(params)
    url = base_url + qs
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json, text/plain, */*'
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            try:
                js = json.loads(data)
                print(f"[SUCCESS] {params['f']}: json keys: {list(js.keys()) if isinstance(js, dict) else len(js)}")
                return js
            except:
                print(f"[SUCCESS TEXT] {params['f']}: length {len(data)}")
                return data
    except Exception as e:
        print(f"[ERROR] {params['f']}: {e}")
        return None

print("--- Test pkg-search package 3 ---")
res3 = test_endpoint({'f': 'pkg-search', 'package': '3', 'action': 'search', 'offset': '0', 'limit': '5'})
if res3 and isinstance(res3, dict):
    print("Total rows:", res3.get('total'))
    print("Sample row:", json.dumps(res3.get('rows', [])[:1], ensure_ascii=False, indent=2))

print("\n--- Test pkg-search package 4 ---")
res4 = test_endpoint({'f': 'pkg-search', 'package': '4', 'action': 'search', 'offset': '0', 'limit': '5'})
if res4 and isinstance(res4, dict):
    print("Total rows:", res4.get('total'))

print("\n--- Test pkg-search package 47 ---")
res47 = test_endpoint({'f': 'pkg-search', 'package': '47', 'action': 'search', 'offset': '0', 'limit': '5'})
if res47 and isinstance(res47, dict):
    print("Total rows:", res47.get('total'))

print("\n--- Test pkg9-search ---")
res9 = test_endpoint({'f': 'pkg9-search', 'action': 'search', 'offset': '0', 'limit': '5'})
if res9 and isinstance(res9, dict):
    print("Total rows:", res9.get('total'))
    print("Sample row:", json.dumps(res9.get('rows', [])[:1], ensure_ascii=False, indent=2))

print("\n--- Test pkg54-search ---")
res54 = test_endpoint({'f': 'pkg54-search', 'offset': '0', 'limit': '5'})
if res54 and isinstance(res54, dict):
    print("Total rows:", res54.get('total'))
    print("Sample row:", json.dumps(res54.get('rows', [])[:1], ensure_ascii=False, indent=2))

print("\n--- Test additional-requirements-templates ---")
res_req = test_endpoint({'f': 'json/additional-requirements-templates'})
if res_req and isinstance(res_req, dict):
    print("Template keys:", list(res_req.keys()))

print("\n--- Test coeff-details package 3 ---")
res_c3 = test_endpoint({'f': 'coeff-details', 'package': '3'})
if res_c3:
    print("Sample coeff:", str(res_c3)[:200])

print("\n--- Test pkg54-info ---")
res_54i = test_endpoint({'f': 'pkg54-info'})
if res_54i:
    print("Sample 54 info:", str(res_54i)[:200])
