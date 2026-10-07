import glob
import re
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

docs_dir = r"c:\__MEDLINK___\PMG\extracted_data"
files = glob.glob(f"{docs_dir}/docs_html/*.html") + glob.glob(f"{docs_dir}/pages_html/*.html")

legal_citations = []

keywords = ['постанов', 'наказ', 'закон', 'кму', 'моз', 'нсзу', 'порядок', 'перелік', 'правил', 'інструкц']

for f in files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        html = fp.read()
    
    # Strip basic tags or search text
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)

    # Search for occurrences of keywords followed by numbers or dates
    matches = re.finditer(r'(?:постанов[а-я]{0,4}|наказ[а-я]{0,4}|закон[а-я]{0,4}|розпорядженн[а-я]{0,4})\s+(?:кму|моз|україни)?[^.;:]{0,120}(?:№\s*[\d\w\-\/]+|\d{1,2}\s+[а-яіїє]+\s+\d{4}|\d{2}\.\d{2}\.\d{4})', text, re.I)
    for m in matches:
        legal_citations.append((os.path.basename(f), m.group(0).strip()))

    # Also look for any hrefs inside HTML
    hrefs = re.findall(r'href=[\'"]([^\'"]+)[\'"]', html, re.I)
    for h in hrefs:
        if any(term in h.lower() for term in ['rada', 'moz', 'nszu', 'zakon', 'gov.ua', '.pdf', '.docx', '.xlsx', 'drive.google', 'document']):
            legal_citations.append((os.path.basename(f), f"HREF: {h}"))

print(f"Total legal citations and document references found: {len(legal_citations)}")
for fn, cit in legal_citations[:60]:
    print(f"[{fn}] {cit}")
