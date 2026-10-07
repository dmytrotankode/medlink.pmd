import urllib.request
import json
import urllib.parse
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base_url = "https://info-pmg.com/serve.php?"

def test_p54_extra():
    # Test pkg54-diag
    q_diag = urllib.parse.urlencode({'f': 'pkg54-diag', 'code': 'A06.6'})
    req = urllib.request.Request(base_url + q_diag, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            print(f"pkg54-diag (A06.6): {len(data)} bytes -> {data.decode('utf-8')[:300]}")
    except Exception as e:
        print("pkg54-diag error:", e)

    # Test pkg54-type-list
    q_type = urllib.parse.urlencode({'f': 'pkg54-type-list', 'type': 'Діагноз_ПП'})
    req2 = urllib.request.Request(base_url + q_type, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req2) as resp:
            data2 = resp.read()
            print(f"pkg54-type-list (Діагноз_ПП): {len(data2)} bytes -> {data2.decode('utf-8')[:300]}")
    except Exception as e:
        print("pkg54-type-list error:", e)

test_p54_extra()
