import glob
import re
import os

files = glob.glob("c:/__MEDLINK___/PMG/downloaded_js/*.js")

for f in files:
    with open(f, "r", encoding="utf-8", errors="ignore") as fp:
        content = fp.read()
    print(f"\n==================== {os.path.basename(f)} (len {len(content)}) ====================")
    # Search for URLs or endpoints
    urls = set(re.findall(r'[\'"](/[\w\-/]+(?:\.\w+)?(?:\?[^\'"\s]*)?)[\'"]', content))
    interesting = [u for u in urls if not u.endswith(('.png', '.svg', '.ico', '.css'))]
    print("Endpoints/Paths found:", interesting[:25])
    
    # Search for fetch / ajax
    fetch_calls = re.findall(r'fetch\([^\)]+\)', content)
    if fetch_calls:
        print("Fetch calls:", fetch_calls[:10])
    
    # Search for post / get
    post_calls = re.findall(r'\.post\([^\)]+\)', content)
    if post_calls:
        print("Post calls:", post_calls[:10])

    # Search for any references to .json or .php or api
    json_refs = set(re.findall(r'[\'"]([^\'"]*(?:\.json|\.php|api|handler)[^\'"]*)[\'"]', content))
    print("JSON/PHP/API refs:", list(json_refs)[:15])
