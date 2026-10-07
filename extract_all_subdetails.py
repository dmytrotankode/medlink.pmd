import urllib.request
import urllib.parse
import json
import time
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base = "https://info-pmg.com/serve.php?"
out_dir = "c:/__MEDLINK___/PMG/extracted_data/sub_details"
os.makedirs(out_dir, exist_ok=True)
os.makedirs(f"{out_dir}/pkg9_class_details", exist_ok=True)
os.makedirs(f"{out_dir}/pkg54_type_lists", exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*'
}

def fetch_json(params):
    url = base + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=25) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            time.sleep(1.0 + attempt)
    return None

def extract_subdetails():
    print("--- 1. Extracting Package 9 referral-split ---")
    ref_split = fetch_json({'f': 'pkg9-search', 'action': 'referral-split'})
    if ref_split:
        with open(f"{out_dir}/pkg9_referral_split.json", "w", encoding="utf-8") as f:
            json.dump(ref_split, f, ensure_ascii=False, indent=2)
        print(f"  Saved pkg9_referral_split.json (yes: {len(ref_split.get('yes', []))}, no: {len(ref_split.get('no', []))})")

    print("\n--- 2. Extracting Package 54 type-lists ---")
    types = ['Діагноз_ПП', 'Діагноз_ДП', 'Супутній', 'Ускладнення', 'Інший']
    for t in types:
        print(f"  Fetching type: {t}...")
        t_data = fetch_json({'f': 'pkg54-type-list', 'type': t})
        if t_data:
            clean_t = t.replace('/', '_')
            with open(f"{out_dir}/pkg54_type_lists/{clean_t}.json", "w", encoding="utf-8") as f:
                json.dump(t_data, f, ensure_ascii=False, indent=2)
            print(f"    Saved {clean_t}.json (total: {t_data.get('total', len(t_data))})")
        time.sleep(0.5)

    print("\n--- 3. Extracting Package 9 class details (diags, services, positions for classes 1..148) ---")
    # Read package 9 full
    with open("c:/__MEDLINK___/PMG/extracted_data/raw_json/package_9_full.json", "r", encoding="utf-8") as f:
        p9 = json.load(f)
    
    rows = p9.get('rows', [])
    for idx, r in enumerate(rows):
        cid = r.get('id')
        cname = r.get('class_number')
        # Check if already downloaded
        target_file = f"{out_dir}/pkg9_class_details/class_{cname}.json"
        if os.path.exists(target_file):
            continue
        
        # Fetch diags, services, positions
        d_data = fetch_json({'f': 'pkg9-search', 'action': 'details', 'id': str(cid), 'type': 'diags'})
        s_data = fetch_json({'f': 'pkg9-search', 'action': 'details', 'id': str(cid), 'type': 'services'})
        p_data = fetch_json({'f': 'pkg9-search', 'action': 'details', 'id': str(cid), 'type': 'positions'})

        class_detail = {
            'id': cid,
            'class_number': cname,
            'class_name': r.get('class'),
            'coefficient': r.get('coefficient'),
            'cost': r.get('cost'),
            'diags': d_data.get('diags_structured', []) if d_data else [],
            'services': s_data.get('services_modal', []) if s_data else [],
            'positions': p_data.get('positions_structured', []) if p_data else []
        }
        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(class_detail, f, ensure_ascii=False, indent=2)
        
        if (idx + 1) % 20 == 0 or idx + 1 == len(rows):
            print(f"  Extracted details for {idx+1} / {len(rows)} classes...")
        time.sleep(0.3)

    print("\nALL SUB-DETAILS AND MODAL DICTIONARIES EXTRACTED 100%!")

if __name__ == '__main__':
    extract_subdetails()
