import os
import sys
import sqlite3
import pandas as pd
import openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class PmgReportAnalyzer:
    def __init__(self, db_path="c:/__MEDLINK___/PMG/pmg_database.sqlite"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def analyze_row(self, package_id, diag_code, service_code=None, doctor_pos=None, age=None, patient_is_military=False):
        """
        Calculates expected DSG, rules, and tariff for a given record.
        Handles case where NHSU report cost column is present or absent.
        """
        result = {
            'valid': False,
            'package_id': package_id,
            'dsg_code': None,
            'coeff': 0.0,
            'base_rate': 0.0,
            'expected_cost': 0.0,
            'warnings': [],
            'errors': []
        }

        package_id = str(package_id).strip()
        diag_code = str(diag_code).strip() if diag_code else ""
        service_code = str(service_code).strip() if service_code else ""

        # --- Inpatient Packages (3, 4, 47) ---
        if package_id in ['3', '4', '47']:
            # Search DSG by diagnosis and optionally service
            query = """
            SELECT d.dsg_id, d.drg_name, g.coefficient, g.coeff_numeric, g.base_rate, g.price, d.notes,
                   g.additional_requirements, g.req_package_1
            FROM pmg_dsg_diagnoses d
            JOIN pmg_dsg g ON d.package_id = g.package_id AND d.dsg_id = g.id
            WHERE d.package_id = ? AND d.diag_code = ?
            """
            self.cursor.execute(query, (package_id, diag_code))
            matches = self.cursor.fetchall()

            if not matches:
                result['errors'].append(f"Діагноз {diag_code} не входить до переліку ДСГ пакета {package_id}")
                return result

            # If service is specified, check intersection
            chosen_match = None
            if service_code:
                for m in matches:
                    dsg_id = m[0]
                    self.cursor.execute("""
                    SELECT 1 FROM pmg_dsg_services
                    WHERE package_id = ? AND dsg_id = ? AND service_code = ?
                    """, (package_id, dsg_id, service_code))
                    if self.cursor.fetchone():
                        chosen_match = m
                        break

            if not chosen_match:
                chosen_match = matches[0]
                if service_code:
                    result['warnings'].append(f"Послуга {service_code} не специфікована окремо в обраній ДСГ, розрахунок за основним діагнозом")

            result['valid'] = True
            result['dsg_code'] = chosen_match[1]
            result['coeff'] = chosen_match[3]
            result['base_rate'] = chosen_match[4]
            result['expected_cost'] = chosen_match[5] if chosen_match[5] > 0 else (chosen_match[3] * chosen_match[4])
            
            # Check requirements
            if chosen_match[7]: # additional_requirements
                result['warnings'].append(f"Додаткові вимоги: {chosen_match[7]}")
            if chosen_match[8]: # req_package_1
                result['warnings'].append(f"Пов'язаний пакет: {chosen_match[8]}")

        # --- Outpatient Package 9 ---
        elif package_id == '9':
            # Check service class
            if service_code:
                self.cursor.execute("""
                SELECT id, class_name, coefficient, cost, svc_codes_json
                FROM pmg_package9_classes
                WHERE svc_codes_json LIKE ?
                """, (f'%"{service_code}%',))
                row = self.cursor.fetchone()
                if row:
                    result['valid'] = True
                    result['dsg_code'] = row[1]
                    result['coeff'] = row[2]
                    result['base_rate'] = 155.0
                    result['expected_cost'] = row[3]
                else:
                    result['errors'].append(f"Послуга {service_code} не знайдена у класифікаторі Пакету 9")
            else:
                result['errors'].append("Для амбулаторного пакета 9 обов'язковий код послуги")

        # --- Rehabilitation Package 54 ---
        elif package_id == '54':
            self.cursor.execute("""
            SELECT diag_code, diag_name, ar_groups, is_main, note
            FROM pmg_package54_rehab
            WHERE diag_code = ?
            """, (diag_code,))
            row = self.cursor.fetchone()
            if row:
                result['valid'] = True
                result['dsg_code'] = f"Реабілітація ({row[2]})"
                result['warnings'].append(f"Вимоги АР: {row[2]}")
                if row[4]:
                    result['warnings'].append(row[4])
                # Base rate for rehab
                result['expected_cost'] = 10500.0 # example standard cycle rate
            else:
                result['errors'].append(f"Діагноз {diag_code} не входить до дозволених реабілітаційних станів Пакету 54")

        else:
            result['warnings'].append(f"Пакет {package_id} має індивідуальні специфікації розрахунку")

        return result

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    analyzer = PmgReportAnalyzer()
    print("--- Test Analysis: Inpatient Case ---")
    res1 = analyzer.analyze_row(package_id='3', diag_code='I21.0', service_code='38215-00')
    print(res1)

    print("\n--- Test Analysis: Outpatient Case ---")
    res2 = analyzer.analyze_row(package_id='9', diag_code='I10', service_code='T67002')
    print(res2)

    print("\n--- Test Analysis: Rehab Case ---")
    res3 = analyzer.analyze_row(package_id='54', diag_code='I69.3')
    print(res3)

    print("\n--- Test Analysis: Invalid Case ---")
    res4 = analyzer.analyze_row(package_id='3', diag_code='INVALID_CODE')
    print(res4)

    analyzer.close()
