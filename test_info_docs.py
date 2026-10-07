import urllib.request

base_url = "https://info-pmg.com/serve.php?f=info/"

pkgs = ['3', '4', '9', '47', '54']
types = ['procurement_conditions', 'clarification', 'list']

for p in pkgs:
    for t in types:
        name = f"{p}_{t}"
        url = base_url + name
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                print(f"[FOUND {resp.status}] {name}: {len(data)} bytes ({resp.headers.get_content_type()})")
        except urllib.error.HTTPError as e:
            print(f"[HTTP {e.code}] {name}")
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
