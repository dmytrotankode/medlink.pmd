import os
import sys
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "https://info-pmg.com"
OUTPUT_DIR = "c:/__MEDLINK___/PMG/extracted_data"
os.makedirs(f"{OUTPUT_DIR}/raw_json", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/docs_html", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/pages_html", exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/html, */*'
}

def fetch_url(url, is_json=False):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read()
            if is_json:
                return json.loads(content.decode('utf-8', errors='ignore'))
            return content.decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"[ERROR] Failed {url}: {e}")
        return None

def fetch_serve(params, is_json=True):
    qs = urllib.parse.urlencode(params)
    url = f"{BASE_URL}/serve.php?{qs}"
    return fetch_url(url, is_json=is_json)

def extract_all():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting info-pmg.com extraction...")

    # 1. Download core pages
    pages = ['/', '/3-package', '/4-package', '/9-package', '/47-package', '/54-package', '/nszu-file-analysis', '/pmg-2026']
    for p in pages:
        name = 'home' if p == '/' else p.strip('/').replace('/', '_')
        print(f"Fetching page: {p}...")
        html = fetch_url(f"{BASE_URL}{p}", is_json=False)
        if html:
            with open(f"{OUTPUT_DIR}/pages_html/{name}.html", "w", encoding="utf-8") as f:
                f.write(html)

    # 2. Additional requirements templates
    print("Fetching additional-requirements-templates...")
    templates = fetch_serve({'f': 'json/additional-requirements-templates'}, is_json=True)
    if templates:
        with open(f"{OUTPUT_DIR}/raw_json/additional_requirements_templates.json", "w", encoding="utf-8") as f:
            json.dump(templates, f, ensure_ascii=False, indent=2)

    # 3. Package 54 Info
    print("Fetching pkg54-info...")
    p54_info = fetch_serve({'f': 'pkg54-info'}, is_json=True)
    if p54_info:
        with open(f"{OUTPUT_DIR}/raw_json/pkg54_info.json", "w", encoding="utf-8") as f:
            json.dump(p54_info, f, ensure_ascii=False, indent=2)

    # 4. Coeff details for packages 3, 4, 47
    for pkg in ['3', '4', '47']:
        print(f"Fetching coeff-details for package {pkg}...")
        c_html = fetch_url(f"{BASE_URL}/serve.php?f=coeff-details&package={pkg}", is_json=False)
        if c_html:
            with open(f"{OUTPUT_DIR}/docs_html/coeff_details_pkg{pkg}.html", "w", encoding="utf-8") as f:
                f.write(c_html)

    # 5. Documents / info
    info_docs = [
        '3_procurement_conditions', '3_clarification', '3_list',
        '4_procurement_conditions', '4_clarification', '4_list',
        '9_procurement_conditions', '9_clarification', '9_list',
        '47_procurement_conditions', '47_clarification', '47_list',
        '54_procurement_conditions', '54_clarification'
    ]
    for doc in info_docs:
        print(f"Fetching info doc: {doc}...")
        d_html = fetch_url(f"{BASE_URL}/serve.php?f=info/{doc}", is_json=False)
        if d_html:
            with open(f"{OUTPUT_DIR}/docs_html/{doc}.html", "w", encoding="utf-8") as f:
                f.write(d_html)

    # 6. DSG Packages 3, 4, 47 (pkg-search)
    for pkg_id in ['3', '4', '47']:
        print(f"\n--- Extracting all DSG rows for Package {pkg_id} ---")
        all_rows = []
        offset = 0
        limit = 100
        total = None
        meta = None

        while True:
            params = {
                'f': 'pkg-search',
                'package': pkg_id,
                'action': 'search',
                'offset': str(offset),
                'limit': str(limit)
            }
            res = fetch_serve(params, is_json=True)
            if not res or 'rows' not in res:
                break
            rows = res.get('rows', [])
            total = res.get('total', 0)
            meta = res.get('meta', meta)
            all_rows.extend(rows)
            print(f"  Pkg {pkg_id}: fetched {len(all_rows)} / {total}")
            offset += len(rows)
            if offset >= total or len(rows) == 0:
                break
            time.sleep(0.1)

        pkg_data = {
            'package': pkg_id,
            'total': len(all_rows),
            'meta': meta,
            'rows': all_rows
        }
        with open(f"{OUTPUT_DIR}/raw_json/package_{pkg_id}_full.json", "w", encoding="utf-8") as f:
            json.dump(pkg_data, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(all_rows)} rows for Package {pkg_id}")

    # 7. Package 9 (pkg9-search)
    print(f"\n--- Extracting all rows for Package 9 ---")
    p9_rows = []
    offset = 0
    limit = 100
    p9_meta = None
    p9_available_svc = None

    while True:
        params = {
            'f': 'pkg9-search',
            'action': 'search',
            'offset': str(offset),
            'limit': str(limit)
        }
        res = fetch_serve(params, is_json=True)
        if not res or 'rows' not in res:
            break
        rows = res.get('rows', [])
        total = res.get('total', 0)
        p9_meta = res.get('meta', p9_meta)
        p9_available_svc = res.get('available_svc_types', p9_available_svc)
        p9_rows.extend(rows)
        print(f"  Pkg 9: fetched {len(p9_rows)} / {total}")
        offset += len(rows)
        if offset >= total or len(rows) == 0:
            break
        time.sleep(0.1)

    p9_data = {
        'package': '9',
        'total': len(p9_rows),
        'meta': p9_meta,
        'available_svc_types': p9_available_svc,
        'rows': p9_rows
    }
    with open(f"{OUTPUT_DIR}/raw_json/package_9_full.json", "w", encoding="utf-8") as f:
        json.dump(p9_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(p9_rows)} rows for Package 9")

    # 8. Package 54 (pkg54-search)
    print(f"\n--- Extracting all rows for Package 54 ---")
    p54_rows = []
    offset = 0
    limit = 200

    while True:
        params = {
            'f': 'pkg54-search',
            'offset': str(offset),
            'limit': str(limit)
        }
        res = fetch_serve(params, is_json=True)
        if not res or 'rows' not in res:
            break
        rows = res.get('rows', [])
        total = res.get('total', 0)
        p54_rows.extend(rows)
        if offset % 1000 == 0 or offset + len(rows) >= total:
            print(f"  Pkg 54: fetched {len(p54_rows)} / {total}")
        offset += len(rows)
        if offset >= total or len(rows) == 0:
            break
        time.sleep(0.05)

    p54_data = {
        'package': '54',
        'total': len(p54_rows),
        'rows': p54_rows
    }
    with open(f"{OUTPUT_DIR}/raw_json/package_54_full.json", "w", encoding="utf-8") as f:
        json.dump(p54_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(p54_rows)} rows for Package 54")

    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ALL DATA EXTRACTED SUCCESSFULLY!")

if __name__ == '__main__':
    extract_all()
