import os
import re

pat = re.compile(r'password\s*[:=]\s*[\'\"]([^\'\"]+)[\'\"]', re.IGNORECASE)

found_pwds = set()
for sdir in [r'c:\Projects\MedProfit', r'c:\Projects\MedProfit2', r'c:\Projects\DSG', r'c:\Projects\DSGImport']:
    for root, dirs, files in os.walk(sdir):
        for f in files:
            if f.endswith(('.pas', '.dfm', '.ini', '.inc', '.sql')):
                fp = os.path.join(root, f)
                try:
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as fp_in:
                        for line in fp_in:
                            m = pat.search(line)
                            if m:
                                found_pwds.add(m.group(1))
                except Exception:
                    pass

print("Found candidate passwords in code:", found_pwds)
