import urllib.request
import json
import sys

def test():
    sys.stdout.reconfigure(encoding='utf-8')
    for fname in ['Вересень 26.xlsx', '02000334_SF_2026_08_20260910.xlsx']:
        req = urllib.request.Request(
            'http://localhost:8085/api/v1/nszu/statements/upload',
            data=json.dumps({'fileName': fname}).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read().decode('utf-8'))
        print(f"=== Upload & Process: {fname} ===")
        print(f"  Org: {data['organizationName']} | EDRPOU: {data['edrpou']}")
        print(f"  Total Rows: {data['totalProcessedRows']} | Accepted: {data['acceptedCount']} | Rejected: {data['rejectedCount']}")
        acc_rev = data['acceptedRevenue']
        lost_rev = data['lostRevenue']
        rec_rev = data['recoverableRevenue']
        rate = data['recoveryRatePercent']
        print(f"  Accepted UAH: {acc_rev:,.2f} | Lost UAH: {lost_rev:,.2f}")
        print(f"  Recoverable UAH: {rec_rev:,.2f} ({rate}%)")
        print(f"  Top Errors ({len(data['topErrors'])} categories):")
        for err in data['topErrors'][:3]:
            print(f"    - {err['errorText'][:80]} ({err['count']} cases)")

if __name__ == '__main__':
    test()
