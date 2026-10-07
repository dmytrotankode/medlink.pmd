import os
import subprocess

os.makedirs('c:/__MEDLINK___/PMG/prototype/screenshots', exist_ok=True)
chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

with open('c:/__MEDLINK___/PMG/prototype/index.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

# Helper to write modified html
def write_tmp(name, mod_script):
    # Insert js execution at the very end of window.onload
    tmp_content = base_html.replace(
        'window.onload = function() {',
        f'window.onload = function() {{\n      {mod_script}'
    )
    path = os.path.join('c:/__MEDLINK___/PMG/prototype', name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(tmp_content)
    return path

# Create views
f_report = 'c:/__MEDLINK___/PMG/prototype/index.html'
f_rejected = write_tmp('tmp_rejected.html', "switchTab('tab-rejected');")
f_doctors = write_tmp('tmp_doctors.html', "switchTab('tab-doctors');")
f_sim = write_tmp('tmp_sim.html', "switchTab('tab-simulator');")
f_cat = write_tmp('tmp_cat.html', "switchTab('tab-catalog');")
f_modal2way = write_tmp('tmp_modal2way.html', "openEncounterModal(1);")
f_modal45 = write_tmp('tmp_modal45.html', "openDetailsModal(1);")

# For Sumy Hospital
tmp_sumy_content = base_html.replace(
    "let currentHospKey = 'oco';",
    "let currentHospKey = 'dkl';"
).replace(
    'value="oco"',
    'value="oco"'
).replace(
    'window.onload = function() {',
    "window.onload = function() {\n      document.getElementById('hosp-select').value = 'dkl';\n      onHospitalChange();"
)
f_sumy = os.path.join('c:/__MEDLINK___/PMG/prototype', 'tmp_sumy.html')
with open(f_sumy, 'w', encoding='utf-8') as f:
    f.write(tmp_sumy_content)

tasks = [
    (f_report, '01_dashboard_report.png'),
    (f_rejected, '02_rejected_lost_revenue.png'),
    (f_doctors, '03_doctors_summary.png'),
    (f_sim, '04_prebilling_simulator.png'),
    (f_cat, '05_catalog_dsg.png'),
    (f_modal2way, '06_modal_2way_correction.png'),
    (f_modal45, '07_modal_45_columns.png'),
    (f_sumy, '08_sumy_children_hospital.png')
]

for src, out_name in tasks:
    out_path = os.path.join('c:/__MEDLINK___/PMG/prototype/screenshots', out_name)
    cmd = [
        chrome,
        '--headless=new',
        '--disable-gpu',
        '--window-size=1600,1150',
        f'--screenshot={out_path}',
        f'file:///{src}'
    ]
    subprocess.run(cmd, capture_output=True)
    size = os.path.getsize(out_path) if os.path.exists(out_path) else 0
    print(f'Captured: {out_name} (Size: {size:,} bytes)')

# Clean up
for tmp in ['tmp_rejected.html', 'tmp_doctors.html', 'tmp_sim.html', 'tmp_cat.html', 'tmp_modal2way.html', 'tmp_modal45.html', 'tmp_sumy.html']:
    p = os.path.join('c:/__MEDLINK___/PMG/prototype', tmp)
    if os.path.exists(p):
        os.remove(p)

print('All 8 screenshots successfully generated!')
