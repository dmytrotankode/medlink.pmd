import os

keywords = ['157.90.118.38', 'medprofit', 'postgres']
search_dirs = [r'c:\Projects\MedProfit', r'c:\Projects\MedProfit2', r'c:\Projects\DRG_MEDICS', r'c:\Projects\DSG', r'c:\Projects\DSGImport', r'c:\__MEDLINK___\PMG']

matches = []
for sdir in search_dirs:
    if not os.path.exists(sdir):
        continue
    for root, dirs, files in os.walk(sdir):
        for f in files:
            if f.endswith(('.pas', '.dfm', '.ini', '.config', '.json', '.txt', '.py', '.bat', '.sh', '.sql', '.cs', '.php', '.env')):
                fp = os.path.join(root, f)
                try:
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as fp_in:
                        text = fp_in.read()
                        if '157.90.118.38' in text:
                            matches.append((fp, '157.90.118.38'))
                        elif 'medprofit' in text.lower() and ('password' in text.lower() or 'pwd' in text.lower()):
                            matches.append((fp, 'medprofit+password'))
                except Exception:
                    pass

print(f"Found {len(matches)} matches:")
for m in matches:
    print(' ', m)
