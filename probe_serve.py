import urllib.request
import urllib.parse
import json

base_url = "https://info-pmg.com/serve.php?f="

candidates = [
    # json candidates
    "json/packages", "json/pkg", "json/dsg", "json/tariffs", "json/rates", "json/rules",
    "json/diagnoses", "json/services", "json/positions", "json/coeffs", "json/coefficients",
    "json/pmg-2026", "json/pmg2026", "json/pmg_2026", "json/changelog", "json/history",
    "json/package3", "json/package4", "json/package9", "json/package47", "json/package54",
    "json/pkg3", "json/pkg4", "json/pkg9", "json/pkg47", "json/pkg54",
    # info candidates
    "info/3", "info/4", "info/9", "info/47", "info/54", "info/pmg-2026", "info/pmg",
    # endpoints
    "pkg-search", "pkg9-search", "pkg54-search", "pkg3-search", "pkg4-search", "pkg47-search",
    "pkg3-info", "pkg4-info", "pkg9-info", "pkg47-info", "pkg54-info",
    "coeff-details", "coeff-details&package=4", "coeff-details&package=9", "coeff-details&package=47", "coeff-details&package=54",
    "analyze-nszu", "changelog", "history", "packages", "stats",
    # python-api
    "python-api/analyze", "python-api/predict", "python-api/dsg",
    # js-modules
    "js-modules/stac", "js-modules/pkg9", "js-modules/pkg54"
]

results = {}
for c in candidates:
    url = base_url + c
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            results[c] = (resp.status, len(data), resp.headers.get_content_type())
            print(f"[FOUND {resp.status}] {c}: {len(data)} bytes ({resp.headers.get_content_type()})")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"[HTTP {e.code}] {c}")
    except Exception as e:
        pass
