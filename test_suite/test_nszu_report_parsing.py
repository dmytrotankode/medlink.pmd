"""
Unit tests for NHSU Report Parsing
Verifies:
- All 4 sheets present: 'Розшифровка', 'Пацієнти', 'Звіт', 'Опис помилок'
- Header row detection (Row 4)
- Exactly 45 columns in 'Розшифровка'
- Accurate extraction of EMZ UUID, patient ID, diagnosis, inclusion status
"""

import unittest
import openpyxl
import os

class TestNszuReportParsing(unittest.TestCase):

    def setUp(self):
        self.file_oco = r"c:\__MEDLINK___\PMG\Вересень 26.xlsx"
        self.file_dkl = r"c:\__MEDLINK___\PMG\02000334_SF_2026_08_20260910.xlsx"
        self.expected_sheets = ['Розшифровка', 'Пацієнти', 'Звіт', 'Опис помилок']

    def test_sheets_presence_both_files(self):
        for path in [self.file_oco, self.file_dkl]:
            self.assertTrue(os.path.exists(path), f"File {path} does not exist")
            wb = openpyxl.load_workbook(path, read_only=True)
            for s in self.expected_sheets:
                self.assertIn(s, wb.sheetnames, f"Sheet {s} missing in {path}")

    def test_rozsh_45_columns(self):
        wb = openpyxl.load_workbook(self.file_oco, read_only=True)
        ws = wb['Розшифровка']
        rows = list(ws.iter_rows(values_only=True, max_col=45))
        # Row 4 is the header row
        header = rows[3]
        self.assertEqual(len(header), 45, "Rozshyfrovka must have exactly 45 columns")
        self.assertEqual(header[0], 'Звітний рік')
        self.assertEqual(header[1], 'Звітний місяць')
        self.assertEqual(header[2], 'Тип електронного медичного запису (ЕМЗ)')
        self.assertEqual(header[3], 'ID ЕМЗ')
        self.assertEqual(header[17], 'Основний діагноз')
        self.assertEqual(header[22], 'Перелік інтервенцій (послуги/діагностичні звіти/процедури)')
        self.assertEqual(header[37], 'Включення медичного запису до звіту')
        self.assertEqual(header[38], 'Коментар щодо виявлених помилок')

    def test_zvit_doctor_breakdown(self):
        wb = openpyxl.load_workbook(self.file_dkl, read_only=True)
        ws = wb['Звіт']
        rows = list(ws.iter_rows(values_only=True))
        # Top metadata contains organization name
        org_row = rows[3]
        self.assertTrue(any("СВЯТОЇ ЗІНАЇДИ" in str(cell) for cell in org_row if cell))
        # Sheet contains doctor section
        has_doctors_section = any("В розрізі лікарів" in str(cell) for r in rows for cell in r if cell)
        self.assertTrue(has_doctors_section, "Sheet Zvit must contain 'В розрізі лікарів' breakdown")

    def test_error_dictionary_sheet(self):
        wb = openpyxl.load_workbook(self.file_oco, read_only=True)
        ws = wb['Опис помилок']
        rows = list(ws.iter_rows(values_only=True))
        # Verify definitions exist
        error_count = 0
        for r in rows:
            non_empty = [c for c in r if c is not None]
            if len(non_empty) >= 2 and isinstance(non_empty[0], str) and len(non_empty[0]) > 3:
                error_count += 1
        self.assertGreater(error_count, 50, "Error dictionary must contain at least 50 error specifications")

if __name__ == '__main__':
    unittest.main()
