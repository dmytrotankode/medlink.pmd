import urllib.request
import urllib.parse
import re
import os

base_url = "https://info-pmg.com"
os.makedirs("c:/__MEDLINK___/PMG/downloaded_js", exist_ok=True)

js_files = [
    "js/pkg-status",
    "js/stac-compiled",
    "js/pkg9-compiled",
    "js/pkg54-compiled",
    "js/nszu-analyzer-compiled",
    "js/accordion"
]

for f in js_files:
    url = f"{base_url}/serve.php?f={urllib.parse.quote(f)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            clean_name = f.replace('/', '_') + ".js"
            out_path = f"c:/__MEDLINK___/PMG/downloaded_js/{clean_name}"
            with open(out_path, "wb") as out_f:
                out_f.write(content)
            print(f"Downloaded {f}: {len(content)} bytes -> {clean_name}")
    except Exception as e:
        print(f"Failed {f}: {e}")
