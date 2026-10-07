import urllib.request
import urllib.parse
import json

base_url = "https://info-pmg.com/serve.php?"

def test_limits():
    # test package 3
    q3 = urllib.parse.urlencode({'f': 'pkg-search', 'package': '3', 'action': 'search', 'offset': '0', 'limit': '500'})
    req = urllib.request.Request(base_url + q3, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        d3 = json.loads(resp.read().decode('utf-8'))
        print(f"Package 3: requested 500, received {len(d3.get('rows', []))} rows (total {d3.get('total')})")

    # test package 9
    q9 = urllib.parse.urlencode({'f': 'pkg9-search', 'action': 'search', 'offset': '0', 'limit': '500'})
    req = urllib.request.Request(base_url + q9, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        d9 = json.loads(resp.read().decode('utf-8'))
        print(f"Package 9: requested 500, received {len(d9.get('rows', []))} rows (total {d9.get('total')})")

    # test package 54
    q54 = urllib.parse.urlencode({'f': 'pkg54-search', 'offset': '0', 'limit': '1000'})
    req = urllib.request.Request(base_url + q54, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        d54 = json.loads(resp.read().decode('utf-8'))
        print(f"Package 54: requested 1000, received {len(d54.get('rows', []))} rows (total {d54.get('total')})")

test_limits()
