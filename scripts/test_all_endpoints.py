import urllib.request, json

def test(url, method='GET', data=None):
    req = urllib.request.Request(url, method=method)
    if data:
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(data).encode('utf-8')
    else:
        body = None
    with urllib.request.urlopen(req, data=body) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        return resp.status, len(res) if isinstance(res, (list, dict)) else 1

endpoints = [
    ('GET', 'http://localhost:8085/api/v1/nszu/statements', None),
    ('POST', 'http://localhost:8085/api/v1/nszu/statements/upload', {'fileName': 'test.xlsx'}),
    ('GET', 'http://localhost:8085/api/v1/nszu/statements/stmt-cherkasy-2026-09/lines', None),
    ('POST', 'http://localhost:8085/api/v1/nszu/statements/stmt-cherkasy-2026-09/reconcile', None),
    ('GET', 'http://localhost:8085/api/v1/nszu/discrepancies', None),
    ('GET', 'http://localhost:8085/api/v1/nszu/reports/summary', None),
    ('POST', 'http://localhost:8085/api/v1/pmg/prebilling/calculate', {'icdCode': 'C180', 'serviceCode': '32003-00', 'doctorPosition': 'P157'}),
    ('GET', 'http://localhost:8085/api/v1/pmg/dictionaries/dsg?q=O01', None),
    ('GET', 'http://localhost:8085/api/v1/pmg/dictionaries/classes?q=C01', None),
    ('GET', 'http://localhost:8085/api/v1/pmg/dictionaries/doctor-positions?q=32003', None),
    ('GET', 'http://localhost:8085/api/v1/pmg/dictionaries/errors?q=ERR_DOC', None),
    ('GET', 'http://localhost:8085/api/v1/pmg/dictionaries/lab-tests?q=A34011', None)
]

for method, url, data in endpoints:
    status, size = test(url, method, data)
    path = url.replace('http://localhost:8085', '')
    print(f'[{status} OK] {method} {path} (items/fields: {size})')
