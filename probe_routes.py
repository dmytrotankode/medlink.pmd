import urllib.request
import re
import json

base_url = "https://info-pmg.com"

def get(path):
    url = base_url + path if path.startswith('/') else path
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest'
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            return resp.status, resp.headers, content
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read()
    except Exception as e:
        return None, None, str(e)

pages = [
    '/',
    '/3-package',
    '/4-package',
    '/9-package',
    '/47-package',
    '/54-package',
    '/nszu-file-analysis',
    '/pmg-2026'
]

print("--- Testing discovered pages ---")
for p in pages:
    st, hd, ct = get(p)
    sz = len(ct) if ct else 0
    print(f"{p}: status {st}, size {sz} bytes")

print("\n--- Testing package numbers 1..60 ---")
found_pkgs = []
for i in range(1, 65):
    p = f"/{i}-package"
    st, hd, ct = get(p)
    if st == 200:
        found_pkgs.append(p)
        print(f"Found {p} (size {len(ct)})")

print(f"\nAll valid package routes found: {found_pkgs}")
