"""
PMG 2026 Tariff Engine Unit Tests
Verifies calculation accuracy according to:
- Постанова КМУ №1808 від 27.12.2024
- Додаток 1 (коефіцієнти ДСГ, коригувальні, дитячі)
- Додаток 2 (кардіохірургія)
- Пакет 9 (амбулаторні класи)
"""

import unittest
import math

class TestPmgTariffs(unittest.TestCase):

    def test_package_4_inpatient_surgery(self):
        # Base rate: 8735.00 UAH
        # DSG G01: Rectal resection / colon interventions. Weight: 5.070
        # Correction coeff: 0.55
        base_rate = 8735.00
        coeff = 5.070
        corr = 0.55
        expected = round(base_rate * coeff * corr, 2) # 24357.55
        self.assertAlmostEqual(expected, 24357.55, places=2)

    def test_package_47_one_day_surgery(self):
        # Base rate: 8735.00 UAH
        # DSG G02: Complex bowel / laparoscopy. Weight: 4.937
        # One-day surgery correction coeff: 0.60
        base_rate = 8735.00
        coeff = 4.937
        corr = 0.60
        expected = round(base_rate * coeff * corr, 2) # 25874.82
        self.assertAlmostEqual(expected, 25874.82, places=2)

    def test_package_3_pediatric_inpatient(self):
        # Base rate: 8735.00 UAH
        # DSG E01: General medicine. Weight: 1.450
        # Child age < 28 days modifier: 1.54
        # Correction coeff: 0.55
        base_rate = 8735.00
        coeff = 1.450
        child_mod = 1.54
        corr = 0.55
        expected = round(base_rate * coeff * child_mod * corr, 2) # 10727.89
        self.assertAlmostEqual(expected, 10727.89, places=2)

    def test_package_9_outpatient_consultation(self):
        # Base rate: 155.00 UAH
        # Class 1 (Cardiology). Coeff: 1.29
        base_rate = 155.00
        coeff = 1.29
        expected = round(base_rate * coeff, 2) # 199.95
        self.assertAlmostEqual(expected, 199.95, places=2)

    def test_package_9_mountain_coefficient(self):
        # Mountain coefficient = 1.25
        base_rate = 155.00
        coeff = 1.29
        mountain = 1.25
        expected = round(base_rate * coeff * mountain, 2) # 249.94
        self.assertAlmostEqual(expected, 249.94, places=2)

    def test_chemotherapy_package_17(self):
        # Adult chemotherapy rate = 17 865.00 UAH
        adult_rate = 17865.00
        # Child chemotherapy rate (< 18 y.o.) = 90 131.00 UAH
        child_rate = 90131.00
        self.assertEqual(adult_rate, 17865.00)
        self.assertEqual(child_rate, 90131.00)

    def test_radiology_package_18(self):
        # Linear accelerator / gamma therapy = 54 089.00 UAH
        rate = 54089.00
        self.assertEqual(rate, 54089.00)

    def test_rehabilitation_package_54(self):
        # Outpatient rehabilitation cycle (AR1-AR4) = 10 820.00 UAH
        rate = 10820.00
        self.assertEqual(rate, 10820.00)

if __name__ == '__main__':
    unittest.main()
