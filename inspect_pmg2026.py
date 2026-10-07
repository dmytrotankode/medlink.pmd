import re

with open("c:/__MEDLINK___/PMG/inspect_pages.py", "r") as f:
    pass

# We fetched /pmg-2026 earlier and it was 43,229 bytes. Let's inspect its text content and headings.
import urllib.request
url = "https://info-pmg.com/pmg-2026"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

with open("c:/__MEDLINK___/PMG/pmg_2026_page.html", "w", encoding="utf-8") as out:
    out.write(html)

headings = re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', html, re.I | re.DOTALL)
print(f"Headings in pmg-2026 ({len(headings)}):")
for h in headings[:20]:
    clean = re.sub(r'<[^>]+>', '', h).strip()
    print(" -", clean)
