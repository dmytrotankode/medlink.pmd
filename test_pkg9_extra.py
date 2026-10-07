import urllib.request
import urllib.parse
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base = "https://info-pmg.com/serve.php?f=pkg9-search&"

def test_act(act, extra={}):
    p = {'action': act}
    p.update(extra)
    url = base + urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            print(f"Action '{act}' (len {len(data)}): {data[:300].decode('utf-8', errors='ignore')}")
            return data
    except Exception as e:
        print(f"Action '{act}' error: {e}")

test_act('all-services')
test_act('referral-split')
test_act('details', {'id': '1', 'type': 'diags'})
test_act('details', {'id': '1', 'type': 'services'})
test_act('details', {'id': '1', 'type': 'positions'})
