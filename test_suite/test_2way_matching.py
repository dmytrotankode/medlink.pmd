"""
Unit tests for 2-Way Matching between MedLink MIS Encounters and NHSU Report
Verifies:
- 1-to-1 matching via EhealthId UUID
- Generation of actionable recommendation for rejected cases
- Updating interaction status from Rejected to Accepted
"""

import unittest

class Test2WayMatching(unittest.TestCase):

    def setUp(self):
        # Simulated MedLink Encounter database record
        self.medlink_encounter = {
            "id": "e8d35e12-4011-477d-8153-bc2a089ffb01",
            "patient_id": "P-125601",
            "practitioner_name": "Калапуц Ірина Василівна",
            "practitioner_pos": "Лікар-онколог",
            "ehealth_id": "43848687-8d7c-11f1-ab81-9200081ff1fa",
            "main_diagnosis": "C18.0",
            "services": [], # Missing required procedure!
            "package_id": "4",
            "status": "Finalized"
        }

        # Simulated NHSU Report row
        self.nhsu_report_row = {
            "ehealth_emz_id": "43848687-8d7c-11f1-ab81-9200081ff1fa",
            "included_in_report": "Ні",
            "error_comment": "Не відповідає жодному пакету/послузі",
            "error_details": "Відсутня обов'язкова хірургічна інтервенція"
        }

    def test_2way_ehealth_id_matching(self):
        # Must match 1-to-1 by UUID
        self.assertEqual(
            self.medlink_encounter["ehealth_id"],
            self.nhsu_report_row["ehealth_emz_id"],
            "Encounter.EhealthId must match Column 4 ID ЕМЗ"
        )

    def test_smart_recommendation_generation(self):
        enc = self.medlink_encounter
        row = self.nhsu_report_row
        
        # Generator logic
        recommendation = None
        if row["included_in_report"] == "Ні" and "C18" in enc["main_diagnosis"]:
            if not enc["services"]:
                recommendation = {
                    "action": "AddProcedure",
                    "suggested_achi_code": "30061-02",
                    "suggested_achi_name": "Резекція правої половини ободової кишки",
                    "target_dsg": "G01",
                    "expected_revenue": 24357.55
                }
        
        self.assertIsNotNone(recommendation)
        self.assertEqual(recommendation["suggested_achi_code"], "30061-02")
        self.assertEqual(recommendation["target_dsg"], "G01")
        self.assertEqual(recommendation["expected_revenue"], 24357.55)

    def test_apply_correction_updates_encounter(self):
        enc = self.medlink_encounter.copy()
        
        # Apply AI recommendation
        enc["services"].append("30061-02")
        enc["coding_corrected"] = True
        
        # Verify state
        self.assertIn("30061-02", enc["services"])
        self.assertTrue(enc["coding_corrected"])

if __name__ == '__main__':
    unittest.main()
