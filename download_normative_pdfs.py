import urllib.request
import urllib.parse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base_url = "https://info-pmg.com"
out_dir = "c:/__MEDLINK___/PMG/extracted_data/normative_docs"
os.makedirs(out_dir, exist_ok=True)

files_to_download = [
    "info/files/pmg-2026/pmg-2026.pdf",
    "info/files/pmg-2026/Додаток-1.pdf",
    "info/files/pmg-2026/Додаток-2.pdf",
    "info/files/pmg-2026/Додаток-3.pdf",
    "info/files/pmg-2026/Додаток-4.pdf",
    "info/files/pmg-2026/Додаток-5.pdf",
    "info/files/pmg-2026/Додаток-6.pdf",
]

for fpath in files_to_download:
    url = f"{base_url}/serve.php?f={urllib.parse.quote(fpath)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
            fname = os.path.basename(fpath)
            local_path = os.path.join(out_dir, fname)
            with open(local_path, "wb") as out_f:
                out_f.write(data)
            print(f"[DOWNLOADED] {fname} ({len(data):,} bytes)")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"[HTTP {e.code}] {fpath}")
    except Exception as e:
        print(f"[ERROR] {fpath}: {e}")
