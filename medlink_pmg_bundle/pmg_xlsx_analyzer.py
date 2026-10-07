import openpyxl
import os
import json
import sqlite3
import datetime
from collections import Counter

def analyze_xlsx_statement(file_path, db_path=None):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
    if 'Розшифровка' not in wb.sheetnames:
        wb.close()
        raise ValueError("Sheet 'Розшифровка' not found in workbook")

    ws = wb['Розшифровка']
    rows = list(ws.iter_rows(values_only=True))
    wb.close()

    if len(rows) < 5:
        raise ValueError("File contains insufficient rows")

    org_name = str(rows[0][0]).strip() if rows[0][0] else "Невідомий ЗОЗ"
    edrpou = str(rows[1][0]).strip() if rows[1][0] else "00000000"

    headers = [str(h).strip() if h is not None else f"Колонка_{i+1}" for i, h in enumerate(rows[3])]

    total_records = len(rows) - 4
    accepted_records = 0
    rejected_records = 0
    guaranteed_budget_records = 0

    packages_counter = Counter()
    errors_counter = Counter()
    doctors_data = {}
    sample_records = []

    # PMG Tariff Constants (Resolution No. 1808)
    BASE_RATE_HOSPITAL = 8735.00
    BASE_RATE_OUTPATIENT = 155.00

    total_billed_uah = 0.0
    accepted_uah = 0.0
    lost_revenue_uah = 0.0
    recoverable_uah = 0.0

    parsed_lines = []

    for idx, r in enumerate(rows[4:], start=1):
        # 45 Columns Mapping
        # Col 1: Year (r[0]), Col 2: Month (r[1]), Col 3: EmzType (r[2]), Col 4: ID ЕМЗ (r[3])
        # Col 6: DocPos (r[5]), Col 7: DoctorName (r[6]), Col 8: Location (r[7])
        # Col 13: EpisodeType (r[12]), Col 14: DateStart (r[13]), Col 16: DateEnd (r[15]), Col 17: LengthOfStay (r[16])
        # Col 18: PrimaryDiag (r[17]), Col 23: Interventions (r[22])
        # Col 34: ADSG (r[33]), Col 35: Package (r[34]), Col 36: ServiceNumber (r[35])
        # Col 37: IncStats (r[36]), Col 38: IncReport (r[37]), Col 39: ErrorComment (r[38])
        # Col 40: CompletenessDetails (r[39]), Col 41: VerificationDetails (r[40]), Col 42: GroupingConflict (r[41])

        emz_id = str(r[3]).strip() if r[3] else f"EMZ-ROW-{idx}"
        doc_name = str(r[6]).strip() if r[6] else "Невідомий лікар"
        doc_pos = str(r[5]).strip() if r[5] else ""
        pkg_str = str(r[34]).strip() if r[34] else "-"
        adsg_code = str(r[33]).strip() if r[33] else ""
        primary_diag = str(r[17]).strip() if r[17] else ""
        interventions = str(r[22]).strip() if r[22] else ""
        inc_report = str(r[37]).strip().lower() if r[37] else "ні"
        error_comment = str(r[38]).strip() if r[38] else ""

        packages_counter[pkg_str] += 1

        # Determine package number from string
        pkg_num = "9"
        if pkg_str.startswith("4 ") or "хірургіч" in pkg_str.lower():
            pkg_num = "4"
        elif pkg_str.startswith("3 ") or "стаціонарна допомога" in pkg_str.lower():
            pkg_num = "3"
        elif pkg_str.startswith("47") or "одного дня" in pkg_str.lower():
            pkg_num = "47"
        elif pkg_str.startswith("17") or pkg_str.startswith("18") or "хіміотерап" in pkg_str.lower():
            pkg_num = "18"
        elif pkg_str.startswith("54") or "реабілітаційна" in pkg_str.lower():
            pkg_num = "54"

        # Calculate estimated tariff
        est_tariff = 0.0
        if pkg_num in ["3", "4", "47"]:
            weight = 2.45
            if "O01" in adsg_code: weight = 5.07
            elif "G0" in adsg_code: weight = 1.82
            k_glob = 0.60 if pkg_num == "4" else 0.55
            est_tariff = round(BASE_RATE_HOSPITAL * weight * k_glob * 0.80, 2)
        elif pkg_num == "18":
            est_tariff = 17865.00
        elif pkg_num == "54":
            est_tariff = 10820.00
        else: # Outpatient package 9
            weight = 1.35
            est_tariff = round(BASE_RATE_OUTPATIENT * weight, 2)

        total_billed_uah += est_tariff

        if inc_report in ["так", "гб"]:
            accepted_records += 1
            accepted_uah += est_tariff
            if inc_report == "гб":
                guaranteed_budget_records += 1
            status_text = "Так"
        else:
            rejected_records += 1
            lost_revenue_uah += est_tariff
            status_text = "Ні"
            if error_comment:
                errors_counter[error_comment] += 1
            else:
                errors_counter["Не вказано коментар НСЗУ"] += 1

            # Estimate recoverable revenue (around 65% of rejected cases can be fixed)
            if "не відповідає жодному пакету" in error_comment.lower() or "взаємодія для мвтн" in error_comment.lower() or "тривалість" in error_comment.lower():
                recoverable_uah += est_tariff * 0.85
            else:
                recoverable_uah += est_tariff * 0.40

        # Aggregate doctors
        if doc_name not in doctors_data:
            doctors_data[doc_name] = {
                "name": doc_name,
                "position": doc_pos,
                "total": 0,
                "accepted": 0,
                "rejected": 0,
                "revenueUah": 0.0,
                "lostUah": 0.0
            }
        doctors_data[doc_name]["total"] += 1
        if inc_report in ["так", "гб"]:
            doctors_data[doc_name]["accepted"] += 1
            doctors_data[doc_name]["revenueUah"] += est_tariff
        else:
            doctors_data[doc_name]["rejected"] += 1
            doctors_data[doc_name]["lostUah"] += est_tariff

        # Sample first 20 records for preview
        if idx <= 20 or (inc_report == "ні" and len(sample_records) < 30):
            sample_records.append({
                "rowNum": idx,
                "emzId": emz_id,
                "emzType": str(r[2]) if r[2] else "Взаємодія",
                "doctorName": doc_name,
                "doctorPosition": doc_pos,
                "dateStart": str(r[13])[:10] if r[13] else "",
                "dateEnd": str(r[15])[:10] if r[15] else "",
                "primaryDiagnosis": primary_diag,
                "interventions": interventions,
                "packageName": pkg_str,
                "adsgCode": adsg_code,
                "includedInReport": status_text,
                "errorComment": error_comment,
                "tariffUah": est_tariff,
                "isAccepted": inc_report in ["так", "гб"]
            })

    # Prepare Top Doctors sorted by lost revenue
    top_doctors_lost = sorted(doctors_data.values(), key=lambda d: d["lostUah"], reverse=True)[:10]
    top_doctors_revenue = sorted(doctors_data.values(), key=lambda d: d["revenueUah"], reverse=True)[:10]

    report_result = {
        "fileName": os.path.basename(file_path),
        "filePath": file_path,
        "organizationName": org_name,
        "edrpou": edrpou,
        "totalRecords": total_records,
        "acceptedRecords": accepted_records,
        "rejectedRecords": rejected_records,
        "guaranteedBudgetRecords": guaranteed_budget_records,
        "acceptanceRatePercent": round((accepted_records / total_records * 100), 2) if total_records > 0 else 0,
        "financials": {
            "totalBilledTariffUah": round(total_billed_uah, 2),
            "acceptedTariffUah": round(accepted_uah, 2),
            "lostRevenueUah": round(lost_revenue_uah, 2),
            "recoverableRevenueUah": round(recoverable_uah, 2),
            "recoveryRatePercent": round((recoverable_uah / lost_revenue_uah * 100), 1) if lost_revenue_uah > 0 else 0
        },
        "topErrors": [{"errorText": k, "count": v, "sharePercent": round(v / rejected_records * 100, 1) if rejected_records > 0 else 0} for k, v in errors_counter.most_common(8)],
        "packagesDistribution": [{"packageName": k, "count": v, "sharePercent": round(v / total_records * 100, 1)} for k, v in packages_counter.most_common(10)],
        "topDoctorsWithDefektura": top_doctors_lost,
        "topDoctorsRevenue": top_doctors_revenue,
        "sampleLines": sample_records[:25]
    }

    # Optionally persist summary to SQLite if db_path provided
    if db_path and os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            stmt_id = f"stmt-{edrpou}-{datetime.date.today().strftime('%Y%m')}"
            # Extract year/month from row 5 if available
            r_year = rows[4][0] if len(rows) > 4 and rows[4][0] else 2026
            r_month = rows[4][1] if len(rows) > 4 and rows[4][1] else 9
            period_from = f"{r_year}-{int(r_month):02d}-01"
            period_to = f"{r_year}-{int(r_month):02d}-30"

            cur.execute("""
                INSERT OR REPLACE INTO dsg_nszu_statement (
                    id, organization_id, organization_name, period_from, period_to, file_name, imported_at, imported_by,
                    total_records, accepted_records, rejected_records, accepted_amount, rejected_amount, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                stmt_id, edrpou, org_name, period_from, period_to, os.path.basename(file_path), datetime.datetime.now().isoformat(),
                "System Auto-Parser", total_records, accepted_records, rejected_records,
                round(accepted_uah, 2), round(lost_revenue_uah, 2), "Parsed & Analyzed"
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Warning: could not save statement summary to SQLite: {e}")

    return report_result

if __name__ == '__main__':
    res1 = analyze_xlsx_statement(r'C:\__MEDLINK___\PMG\Вересень 26.xlsx', r'C:\__MEDLINK___\PMG\pmg_database.sqlite')
    print("Report 1 Analyzed:", res1["organizationName"], "Total:", res1["totalRecords"], "Lost UAH:", res1["financials"]["lostRevenueUah"])
    res2 = analyze_xlsx_statement(r'C:\__MEDLINK___\PMG\02000334_SF_2026_08_20260910.xlsx', r'C:\__MEDLINK___\PMG\pmg_database.sqlite')
    print("Report 2 Analyzed:", res2["organizationName"], "Total:", res2["totalRecords"], "Lost UAH:", res2["financials"]["lostRevenueUah"])
