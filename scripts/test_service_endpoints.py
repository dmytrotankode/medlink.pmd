import urllib.request
import urllib.parse
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def test():
    base = "http://localhost:8085"
    
    # 1. Groups
    print("Testing GET /api/v1/pmg/dictionaries/service-groups...")
    req = urllib.request.Request(f"{base}/api/v1/pmg/dictionaries/service-groups")
    with urllib.request.urlopen(req) as response:
        groups = json.loads(response.read().decode('utf-8'))
        print(f"Groups count: {len(groups)}")
        assert len(groups) == 12, f"Expected 12 groups, got {len(groups)}"
        print(f"Sample group: {groups[0]['code']} - {groups[0]['name']} (services: {groups[0]['service_count']})")

    # 2. Services list
    print("\nTesting GET /api/v1/pmg/dictionaries/services...")
    q_str = urllib.parse.quote("геміколектомія")
    req = urllib.request.Request(f"{base}/api/v1/pmg/dictionaries/services?q={q_str}")
    with urllib.request.urlopen(req) as response:
        services = json.loads(response.read().decode('utf-8'))
        print(f"Services found: {len(services)}")
        assert len(services) > 0, "Expected at least 1 service matching query"
        print(f"Found: {services[0]['service_code']} - {services[0]['name']}")

    # 3. Single service detail
    print("\nTesting GET /api/v1/pmg/dictionaries/services/32003-00...")
    req = urllib.request.Request(f"{base}/api/v1/pmg/dictionaries/services/32003-00")
    with urllib.request.urlopen(req) as response:
        detail = json.loads(response.read().decode('utf-8'))
        print(f"Service: {detail['service']['service_code']} - {detail['service']['name']}")
        print(f"Combinations: {len(detail['combinations'])}")
        print(f"Doctor rules: {len(detail['doctorRules'])}")
        print(f"Recent encounters (drill-down): {len(detail['encounters'])}")
        assert len(detail['combinations']) > 0, "Expected combinations"
        assert len(detail['encounters']) > 0, "Expected drill-down encounters"

    # 4. Combination Validation (Valid case with multisurgery)
    print("\nTesting POST /api/v1/pmg/combinations/validate (Valid Case)...")
    payload = {
        "serviceCode": "32003-00",
        "icdCode": "C18.0",
        "doctorPosition": "P157",
        "companionServices": ["30075-01", "30394-00", "30440-00"], # includes lymph node, drainage, and cholecystectomy for 1.3 multisurg!
        "admissionType": "Планова",
        "isMountain": False,
        "patientAge": 62,
        "patientGender": "ALL"
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(f"{base}/api/v1/pmg/combinations/validate", data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        print(f"Status: {res['status']}, IsValid: {res['isValid']}")
        print(f"Calculated Tariff: {res['calculatedTariffUah']} UAH")
        print(f"Multisurgery applied: {res['multisurgeryApplied']}")
        print(f"Formula: {res['formula']}")
        assert res['isValid'] == True, "Expected valid result"
        assert res['multisurgeryApplied'] == True, "Expected multisurgery coefficient"

    # 5. Combination Validation (Defectura case: wrong doctor position, missing companion)
    print("\nTesting POST /api/v1/pmg/combinations/validate (Defectura Case)...")
    payload_bad = {
        "serviceCode": "32003-00",
        "icdCode": "C18.0",
        "doctorPosition": "P122", # Therapist instead of Surgeon!
        "companionServices": [], # Missing mandatory companion!
        "admissionType": "Планова"
    }
    data_bad = json.dumps(payload_bad).encode('utf-8')
    req = urllib.request.Request(f"{base}/api/v1/pmg/combinations/validate", data=data_bad, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as response:
        res_bad = json.loads(response.read().decode('utf-8'))
        print(f"Status: {res_bad['status']}, IsValid: {res_bad['isValid']}")
        print(f"Errors: {res_bad['errors']}")
        print(f"Warnings: {res_bad['warnings']}")
        assert res_bad['isValid'] == False, "Expected invalid result due to doctor position"
        assert len(res_bad['warnings']) > 0, "Expected missing mandatory companion warning"

    print("\nALL SERVICE COMBINATION REST ENDPOINTS TESTED SUCCESSFULLY!")

if __name__ == "__main__":
    test()
