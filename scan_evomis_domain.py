import os
import glob

base = r"C:\__MEDLINK___\__MEDLINK\evomis\src"

print("--- Searching for Encounter / Episode / Diagnosis / Service entities in App.Domain ---")
domain_files = glob.glob(f"{base}/App.Domain/**/*.cs", recursive=True)
for f in domain_files:
    fname = os.path.basename(f)
    if any(k in fname.lower() for k in ['encounter', 'episode', 'condition', 'procedure', 'observation', 'diagnostic', 'package', 'tariff', 'ehealth', 'service']):
        rel = os.path.relpath(f, base)
        print(" ", rel)

print("\n--- Searching DbContext in App.Data ---")
data_files = glob.glob(f"{base}/App.Data/**/*.cs", recursive=True)
for f in data_files:
    fname = os.path.basename(f)
    if 'context' in fname.lower() or 'repository' in fname.lower():
        rel = os.path.relpath(f, base)
        print(" ", rel)
