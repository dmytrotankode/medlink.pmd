import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import glob
import os

mdc_path = r"C:\__MEDLINK___\__MEDLINK\evomis\src\App.Mdc.Module\Data"
csvs = glob.glob(f"{mdc_path}/csv/*.csv")
for c in csvs:
    with open(c, "r", encoding="utf-8", errors="ignore") as f:
        first_lines = [f.readline().strip() for _ in range(3)]
    print(f"\nCSV: {os.path.basename(c)}")
    for l in first_lines:
        print(" ", l[:120])
