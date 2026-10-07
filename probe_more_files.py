import urllib.request
import urllib.parse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base_url = "https://info-pmg.com"
out_dir = "c:/__MEDLINK___/PMG/extracted_data/normative_docs"

candidates = [
    "info/files/pmg-2026/Постанова-1808.pdf",
    "info/files/pmg-2026/Порядок.pdf",
    "info/files/pmg-2026/Тарифи.pdf",
    "info/files/3/conditions.pdf",
    "info/files/4/conditions.pdf",
    "info/files/9/conditions.pdf",
    "info/files/47/conditions.pdf",
    "info/files/54/conditions.pdf",
    "info/files/nakaz-377.pdf",
    "info/files/pmg-2026/Додаток-3.pdf"
]

for c in candidates:
    url = f"{base_url}/serve.php?f={urllib.parse.quote(c)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            fname = os.path.basename(c)
            with open(os.path.join(out_dir, fname), "wb") as f:
                f.write(data)
            print(f"[FOUND] {c}: {len(data)} bytes")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"[{e.code}] {c}")
    except Exception as e:
        pass
