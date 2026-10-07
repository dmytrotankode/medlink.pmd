import json
import sqlite3

def reseed():
    db_path = r'c:\__MEDLINK___\PMG\pmg_database.sqlite'
    manifest_path = r'c:\__MEDLINK___\PMG\normative_packages\all_packages_manifest.json'

    with open(manifest_path, 'r', encoding='utf-8') as f:
        packages = json.load(f)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pmg_packages (
        package_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        base_rate REAL NOT NULL DEFAULT 0.0,
        meta_json TEXT
    );
    """)

    for p in packages:
        p_id = str(p['id'])
        name = p['name']
        base_rate = float(p.get('base_rate', 0.0))
        meta_json = json.dumps(p, ensure_ascii=False)

        cur.execute("""
        INSERT OR REPLACE INTO pmg_packages (package_id, name, base_rate, meta_json)
        VALUES (?, ?, ?, ?)
        """, (p_id, name, base_rate, meta_json))

    conn.commit()

    # Verify
    cur.execute("SELECT package_id, name, meta_json FROM pmg_packages WHERE package_id = '47'")
    row = cur.fetchone()
    print("Package 47 name in DB:", row[1])
    meta = json.loads(row[2])
    print("Package 47 category:", meta.get('category'))

    cur.execute("SELECT package_id, name, meta_json FROM pmg_packages WHERE package_id = '18'")
    row18 = cur.fetchone()
    meta18 = json.loads(row18[2])
    print("Package 18 category:", meta18.get('category'))

    conn.close()
    print(f"Successfully re-seeded {len(packages)} packages into {db_path} with pristine UTF-8!")

if __name__ == '__main__':
    reseed()
