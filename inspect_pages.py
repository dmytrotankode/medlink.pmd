import urllib.request
import re
import json

base_url = "https://info-pmg.com"

pages = [
    '/',
    '/3-package',
    '/4-package',
    '/9-package',
    '/47-package',
    '/54-package',
    '/nszu-file-analysis',
    '/pmg-2026'
]

def fetch_page(path):
    url = base_url + path
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode('utf-8', errors='ignore')

for p in pages:
    html = fetch_page(p)
    print(f"\n==================== PAGE: {p} (len {len(html)}) ====================")
    # Find all script src
    scripts = re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', html, re.I)
    print(f"Scripts: {scripts}")
    # Find all inline scripts that contain fetch, ajax, post, get, url, api, json
    inline_scripts = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', html, re.I | re.DOTALL)
    for idx, s in enumerate(inline_scripts):
        s_clean = s.strip()
        if any(term in s_clean for term in ['fetch', '$.ajax', '$.post', '$.get', 'XMLHttpRequest', '/app/', '/json/', '/python-api/', '/php-modules/', 'api', '.json', '.php']):
            print(f"--- Inline script {idx} mentions network/API ---")
            lines = [line.strip() for line in s_clean.split('\n') if any(term in line for term in ['fetch', 'ajax', 'post', 'get', 'url', 'api', 'json', 'php', 'data', 'endpoint'])][:20]
            print("\n".join(lines[:15]))
    
    # Check for data-* attributes or embedded JSON
    embedded_data = re.findall(r'data-[\w\-]+="[^"]*"', html)
    print(f"Data attributes sample: {embedded_data[:5]}")
