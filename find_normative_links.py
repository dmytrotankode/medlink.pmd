import glob
import re
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

docs_dir = r"c:\__MEDLINK___\PMG\extracted_data"
all_files = glob.glob(f"{docs_dir}/**/*.html", recursive=True) + glob.glob(f"{docs_dir}/**/*.json", recursive=True)

urls = set()
normative_mentions = set()

url_pattern = re.compile(r'https?://[^\s"\'<>]+')
# Patterns for Ukrainian legal acts: Постанова, Наказ МОЗ, Закон, Порядок
act_pattern = re.compile(r'(?:Постанова|Наказ|Закон|Розпорядження|Порядок)\s+(?:КМУ|Кабінету Міністрів|МОЗ|Міністерства охорони здоров[\'’]я|України)?[^\.\n;]{5,100}(?:№\s*[\d\w\-\/]+|\d{2}\.\d{2}\.\d{4})?', re.I)

for f in all_files:
    try:
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            text = fp.read()
            for u in url_pattern.findall(text):
                # Filter interesting domains
                if any(dom in u for dom in ['rada.gov.ua', 'moz.gov.ua', 'nszu.gov.ua', 'gov.ua', 'zakon', 'drive.google', 't.me', 'document']):
                    urls.add(u)
            for m in act_pattern.findall(text):
                normative_mentions.add(m.strip())
    except Exception as e:
        pass

print(f"=== External Normative / Gov URLs Found ({len(urls)}) ===")
for u in sorted(urls):
    print(" ", u)

print(f"\n=== Normative Acts Mentions Found ({len(normative_mentions)}) ===")
for m in sorted(normative_mentions)[:40]:
    print(" -", m)
