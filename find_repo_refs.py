import os

targets = ['dsg_analysis_result', 'dsg_rule_config', 'PK-02', 'B72', '8735']
paths_to_check = [r'c:\__MEDLINK___', r'c:\Projects']

found = []
for base in paths_to_check:
    if not os.path.exists(base):
        continue
    for root, dirs, files in os.walk(base):
        # skip git and node_modules
        if '.git' in root or 'node_modules' in root or 'bin' in root or 'obj' in root:
            continue
        for f in files:
            if f.endswith(('.cs', '.py', '.sql', '.json', '.md', '.ts', '.js')):
                fp = os.path.join(root, f)
                try:
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as fp_in:
                        content = fp_in.read()
                        if 'dsg_analysis_result' in content or 'dsg_rule_config' in content:
                            found.append((fp, 'dsg_analysis_result'))
                except Exception:
                    pass

print(f"Total matching files found: {len(found)}")
for f, kw in found:
    print(f"  {f}")
