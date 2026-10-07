import os
import re

files_to_check = [
    'TZ_MedLink_PMG_Analytics.html',
    'prototype/index.html',
    'prototype/process_1_prebilling.html',
    'prototype/process_2_upload.html',
    'prototype/process_3_financial_audit.html',
    'prototype/process_4_discrepancies.html',
    'prototype/process_5_correction.html',
    'prototype/process_6_catalog.html',
    'README.md'
]

base_dir = r'c:\__MEDLINK___\PMG'
errors = []

for rel_path in files_to_check:
    full_path = os.path.join(base_dir, rel_path)
    if not os.path.exists(full_path):
        errors.append(f'Missing file: {rel_path}')
        continue
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', content)
    cur_dir = os.path.dirname(full_path)
    for link in links:
        if link.startswith('http') or link.startswith('//') or link.startswith('#') or link.startswith('javascript:'):
            continue
        clean_link = link.split('#')[0]
        if not clean_link:
            continue
        target = os.path.normpath(os.path.join(cur_dir, clean_link))
        if not os.path.exists(target):
            errors.append(f'{rel_path}: broken link to "{link}" -> target "{target}" does not exist')

print('--- Verification Summary ---')
if errors:
    print(f'Found {len(errors)} broken links:')
    for e in errors:
        print('  [FAIL]', e)
else:
    print('ALL HYPERLINKS AND PATHS ARE VALID AND POINT TO REAL FILES!')
