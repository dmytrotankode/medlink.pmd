import os

target = "157.90.118.38"
search_roots = [r"c:\Projects", r"c:\__MEDLINK___", r"C:\Users\tanko\AppData\Roaming\DBeaverData", r"C:\Users\tanko\AppData\Roaming\postgresql", r"C:\Users\tanko"]

found = []
for root_path in search_roots:
    if not os.path.exists(root_path):
        continue
    for root, dirs, files in os.walk(root_path):
        # skip massive git and node_modules
        if any(skip in root for skip in ['.git', 'node_modules', '.gemini', 'AppData\\Local\\Microsoft', 'AppData\\Local\\Google']):
            continue
        for f in files:
            if f.endswith(('.json', '.xml', '.ini', '.txt', '.conf', '.cfg', '.yaml', '.yml', '.env', '.properties', '.sql', '.py', '.pas', '.dfm', '.dpr', '.cs')):
                fp = os.path.join(root, f)
                try:
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as fp_in:
                        content = fp_in.read()
                        if target in content:
                            found.append(fp)
                except Exception:
                    pass

print(f"Total matching files with {target}: {len(found)}")
for fp in found:
    print(' ', fp)
