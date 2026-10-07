import os
import sys
import json
import time
import random
import urllib.request
import urllib.parse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "https://info-pmg.com"
OUTPUT_DIR = "c:/__MEDLINK___/PMG/extracted_data"
os.makedirs(f"{OUTPUT_DIR}/raw_json", exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/html, */*',
    'Accept-Language': 'uk,en;q=0.9',
    'X-Requested-With': 'XMLHttpRequest'
}

def fetch_with_retry(url, max_retries=5, delay=1.0):
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                content = resp.read()
                return json.loads(content.decode('utf-8', errors='ignore'))
        except urllib.error.HTTPError as e:
            wait = (attempt + 1) * 2 + random.uniform(0.5, 1.5)
            print(f"  [Attempt {attempt+1}] HTTP {e.code} for {url}. Waiting {wait:.1f}s...")
            time.sleep(wait)
        except Exception as e:
            wait = (attempt + 1) * 2 + random.uniform(0.5, 1.5)
            print(f"  [Attempt {attempt+1}] Error: {e}. Waiting {wait:.1f}s...")
            time.sleep(wait)
    print(f"  [FAILED] Exceeded max retries for {url}")
    return None

def fetch_pkg9_complete():
    print("Completing Package 9 extraction...")
    # Read existing 100 rows if present
    pkg9_file = f"{OUTPUT_DIR}/raw_json/package_9_full.json"
    rows = []
    meta = None
    avail_svc = None
    if os.path.exists(pkg9_file):
        try:
            with open(pkg9_file, "r", encoding="utf-8") as f:
                d = json.load(f)
                rows = d.get('rows', [])[:100]
                meta = d.get('meta')
                avail_svc = d.get('available_svc_types')
        except:
            pass

    offset = len(rows)
    limit = 100
    while True:
        url = f"{BASE_URL}/serve.php?f=pkg9-search&action=search&offset={offset}&limit={limit}"
        data = fetch_with_retry(url)
        if not data:
            break
        curr_rows = data.get('rows', [])
        total = data.get('total', 148)
        meta = data.get('meta', meta)
        avail_svc = data.get('available_svc_types', avail_svc)
        rows.extend(curr_rows)
        print(f"  Package 9: fetched {len(rows)} / {total}")
        offset += len(curr_rows)
        if offset >= total or len(curr_rows) == 0:
            break
        time.sleep(1.0)

    p9_data = {
        'package': '9',
        'total': len(rows),
        'meta': meta,
        'available_svc_types': avail_svc,
        'rows': rows
    }
    with open(pkg9_file, "w", encoding="utf-8") as f:
        json.dump(p9_data, f, ensure_ascii=False, indent=2)
    print(f"Successfully saved all {len(rows)} rows for Package 9!\n")

def fetch_pkg54_complete():
    print("Extracting Package 54 (rehabilitation)...")
    pkg54_file = f"{OUTPUT_DIR}/raw_json/package_54_full.json"
    rows = []
    offset = 0
    limit = 200
    total = 5865

    while offset < total:
        url = f"{BASE_URL}/serve.php?f=pkg54-search&offset={offset}&limit={limit}"
        data = fetch_with_retry(url)
        if not data:
            print(f"Failed at offset {offset}, saving partial rows ({len(rows)})...")
            break
        curr_rows = data.get('rows', [])
        total = data.get('total', total)
        rows.extend(curr_rows)
        offset += len(curr_rows)
        if offset % 1000 == 0 or offset >= total:
            print(f"  Package 54: fetched {len(rows)} / {total} ({(len(rows)/total*100):.1f}%)")
        if len(curr_rows) == 0:
            break
        time.sleep(1.0 + random.uniform(0.1, 0.4))

    p54_data = {
        'package': '54',
        'total': len(rows),
        'rows': rows
    }
    with open(pkg54_file, "w", encoding="utf-8") as f:
        json.dump(p54_data, f, ensure_ascii=False, indent=2)
    print(f"Successfully saved all {len(rows)} rows for Package 54!\n")

if __name__ == '__main__':
    fetch_pkg9_complete()
    fetch_pkg54_complete()
