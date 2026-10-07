import urllib.request
import re
import json

base_url = "https://info-pmg.com"

def get(path):
    url = base_url + path if path.startswith('/') else path
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            return resp.status, resp.headers, content
    except Exception as e:
        return None, None, str(e)

status, headers, content = get('/')
print("Status:", status)
html = content.decode('utf-8', errors='ignore') if content else ""
print("HTML length:", len(html))

# Check robots.txt and sitemap.xml
r_status, _, r_content = get('/robots.txt')
print("/robots.txt status:", r_status)
if r_content:
    print(r_content.decode('utf-8', errors='ignore')[:500])

s_status, _, s_content = get('/sitemap.xml')
print("/sitemap.xml status:", s_status)
if s_content and s_status == 200:
    print(s_content.decode('utf-8', errors='ignore')[:1000])

# Extract links
links = set(re.findall(r'href=[\'"]([^\'"#]+)[\'"]', html))
print(f"\nUnique links found ({len(links)}):")
for l in sorted(links):
    print(" ", l)

# Extract scripts
scripts = set(re.findall(r'src=[\'"]([^\'"#]+)[\'"]', html))
print(f"\nUnique scripts found ({len(scripts)}):")
for s in sorted(scripts):
    print(" ", s)
