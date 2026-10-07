import json

def inspect_json(path, name):
    with open(path, "r", encoding="utf-8") as f:
        d = json.load(f)
    print(f"\n==================== {name} ====================")
    if isinstance(d, dict):
        print("Keys:", list(d.keys()))
        if 'meta' in d:
            print("Meta:", d['meta'])
        if 'rows' in d and len(d['rows']) > 0:
            first = d['rows'][0]
            print("Total rows:", len(d['rows']))
            print("Row keys:", list(first.keys()))
            # print sample row with truncated long lists
            sample = {}
            for k, v in first.items():
                if isinstance(v, list) and len(v) > 3:
                    sample[k] = f"[List of {len(v)} items: {v[:2]}...]"
                elif isinstance(v, dict) and len(v) > 3:
                    sample[k] = f"[Dict with {len(v)} keys: {list(v.keys())[:3]}...]"
                else:
                    sample[k] = v
            print("Sample row:", json.dumps(sample, ensure_ascii=False, indent=2))
    elif isinstance(d, list):
        print(f"List with {len(d)} items")

inspect_json("c:/__MEDLINK___/PMG/extracted_data/raw_json/package_3_full.json", "Package 3 (DSG Inpatient)")
inspect_json("c:/__MEDLINK___/PMG/extracted_data/raw_json/package_4_full.json", "Package 4 (DSG Surgery)")
inspect_json("c:/__MEDLINK___/PMG/extracted_data/raw_json/package_47_full.json", "Package 47 (Day Surgery)")
inspect_json("c:/__MEDLINK___/PMG/extracted_data/raw_json/package_9_full.json", "Package 9 (Outpatient)")
inspect_json("c:/__MEDLINK___/PMG/extracted_data/raw_json/package_54_full.json", "Package 54 (Rehab)")
