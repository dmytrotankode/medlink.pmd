import os
import shutil
import zipfile
import sys

def make_bundle():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=== PACKAGING PMG-2026 COMPLETE BUNDLE ===")

    base_dir = r'c:\__MEDLINK___\PMG'
    bundle_dir = os.path.join(base_dir, 'medlink_pmg_bundle')
    zip_path = os.path.join(base_dir, 'medlink_pmg_complete.zip')

    os.makedirs(bundle_dir, exist_ok=True)

    # 1. Synchronize components
    comp_src = os.path.join(base_dir, 'prototype_medlink', 'components')
    comp_dst = os.path.join(bundle_dir, 'components')
    os.makedirs(comp_dst, exist_ok=True)
    for f in os.listdir(comp_src):
        if f.endswith('.vue'):
            shutil.copy2(os.path.join(comp_src, f), os.path.join(comp_dst, f))
            print(f"  [Component] Synced: {f}")

    # 2. Synchronize SQL
    sql_src = os.path.join(base_dir, 'sql')
    sql_dst = os.path.join(bundle_dir, 'sql')
    os.makedirs(sql_dst, exist_ok=True)
    for f in os.listdir(sql_src):
        if f.endswith('.sql'):
            shutil.copy2(os.path.join(sql_src, f), os.path.join(sql_dst, f))
            print(f"  [SQL] Synced: {f}")

    # 3. Synchronize docs_html
    docs_src = os.path.join(base_dir, 'docs_html')
    docs_dst = os.path.join(bundle_dir, 'docs_html')
    os.makedirs(docs_dst, exist_ok=True)
    for f in os.listdir(docs_src):
        if f.endswith(('.html', '.js', '.css', '.json')):
            shutil.copy2(os.path.join(docs_src, f), os.path.join(docs_dst, f))
    print(f"  [Docs] Synced {len(os.listdir(docs_dst))} doc files.")

    # 4. Synchronize prototype_medlink
    proto_src = os.path.join(base_dir, 'prototype_medlink')
    proto_dst = os.path.join(bundle_dir, 'prototype_medlink')
    os.makedirs(proto_dst, exist_ok=True)
    for f in os.listdir(proto_src):
        src_item = os.path.join(proto_src, f)
        dst_item = os.path.join(proto_dst, f)
        if os.path.isfile(src_item):
            shutil.copy2(src_item, dst_item)
        elif os.path.isdir(src_item) and f != 'components':
            if os.path.exists(dst_item):
                shutil.rmtree(dst_item)
            shutil.copytree(src_item, dst_item)
    print(f"  [Prototype] Synced prototype_medlink files.")

    # 5. Synchronize screenshots (12 high-resolution PNGs)
    ss_src = os.path.join(base_dir, 'screenshots')
    ss_dst = os.path.join(bundle_dir, 'screenshots')
    os.makedirs(ss_dst, exist_ok=True)
    if os.path.exists(ss_src):
        for f in os.listdir(ss_src):
            if f.endswith('.png'):
                shutil.copy2(os.path.join(ss_src, f), os.path.join(ss_dst, f))
        print(f"  [Screenshots] Synced {len(os.listdir(ss_dst))} screen captures.")

    # 6. Synchronize normative_packages
    norm_src = os.path.join(base_dir, 'normative_packages')
    norm_dst = os.path.join(bundle_dir, 'normative_packages')
    if os.path.exists(norm_src):
        if os.path.exists(norm_dst):
            shutil.rmtree(norm_dst)
        shutil.copytree(norm_src, norm_dst)
        print(f"  [Normative Packages] Synced 46 packages dossiers.")

    # 7. Synchronize C# .NET Core 10 Web API module (exclude bin & obj)
    src_net = os.path.join(base_dir, 'src', 'MedLink.Pmg.Module')
    dst_net = os.path.join(bundle_dir, 'src', 'MedLink.Pmg.Module')
    if os.path.exists(src_net):
        if os.path.exists(dst_net):
            shutil.rmtree(dst_net)
        def ignore_build(directory, files):
            return [f for f in files if f in ('bin', 'obj', '.vs')]
        shutil.copytree(src_net, dst_net, ignore=ignore_build)
        print(f"  [.NET Core 10] Synced MedLink.Pmg.Module source code.")

    # 8. Synchronize root items
    root_files_to_sync = [
        'pmg_database.sqlite',
        'serve.py',
        'pmg_xlsx_analyzer.py',
        'TZ_MedLink_PMG_Analytics.html',
        'TZ_MedLink_PMG_Master_Specification.html',
        'ТЗ_MedLink_PMG_Master_Specification.html'
    ]
    for root_file in root_files_to_sync:
        src_f = os.path.join(base_dir, root_file)
        if os.path.exists(src_f):
            shutil.copy2(src_f, os.path.join(bundle_dir, root_file))
            print(f"  [Root File] Synced: {root_file}")

    # 9. Update bundle README.md
    readme_path = os.path.join(bundle_dir, 'README.md')
    with open(os.path.join(base_dir, 'medlink_pmg_bundle', 'README.md'), 'r', encoding='utf-8') as f:
        readme_content = f.read()

    # Ensure README.md reflects 10 components and Chapter 10
    if 'PmgServicesCatalog.vue' not in readme_content:
        comp_old = """### 2. `components/` — 9 готових Single-File Components для `evomis/src/App.View`
1. `PmgPackagesCatalog.vue` — **класифікатор усіх 46 медичних пакетів ПМГ-2026** з пошуком, фільтрами категорій, формулами та нормативними досьє."""
        comp_new = """### 2. `components/` — 10 готових Single-File Components для `evomis/src/App.View`
1. `PmgServicesCatalog.vue` — **довідник послуг (АКПІ), клінічні норми, методики та матриця всіх можливих комбінацій (Delphi re-engineering)**: паспорт послуги, норми часу, анестезії, ліжко-днів, 5-рівневий валідатор комбінацій, коефіцієнт мультихірургії 1.30, бібліотека еталонів `myAddLib` з підсвічуванням прибутку/збитку та наскрізний drill-down до реальних пацієнтів і 45 колонок.
2. `PmgPackagesCatalog.vue` — **класифікатор усіх 46 медичних пакетів ПМГ-2026** з пошуком, фільтрами категорій, формулами та нормативними досьє."""
        readme_content = readme_content.replace(comp_old, comp_new, 1)

    if '10_service_directory_norms_methodologies_combinations.html' not in readme_content:
        doc_old = """* `09_all_pmg_packages_normative_guide.html` — повний реєстр, нормативне регулювання, тарифи та формули всіх 46 пакетів ПМГ-2026."""
        doc_new = """* `09_all_pmg_packages_normative_guide.html` — повний реєстр, нормативне регулювання, тарифи та формули всіх 46 пакетів ПМГ-2026.
* `10_service_directory_norms_methodologies_combinations.html` — довідник послуг АКПІ: клінічні норми, тарифікаційні методики, матриця комбінацій (Delphi Re-engineering), коефіцієнт мультихірургії 1.30, бібліотека еталонів та наскрізний перехід до 45 колонок ЕМЗ."""
        readme_content = readme_content.replace(doc_old, doc_new, 1)

    if '11_seed_service_combinations_and_groups.sql' not in readme_content:
        sql_old = """* `10_seed_all_pmg2026_packages.sql` — **повний реєстр усіх 46 пакетів ПМГ-2026** із тарифами, формулами та валідаціями."""
        sql_new = """* `10_seed_all_pmg2026_packages.sql` — **повний реєстр усіх 46 пакетів ПМГ-2026** із тарифами, формулами та валідаціями.
* `11_seed_service_combinations_and_groups.sql` — **12 клінічних груп, каталог послуг з нормами та матриця правил комбінацій** (`dct_mp_service_odk_rule_detail`), посади лікарів, обов'язкові супутні, коефіцієнт 1.30."""
        readme_content = readme_content.replace(sql_old, sql_new, 1)

    if 'TZ_MedLink_PMG_Master_Specification.html' not in readme_content:
        readme_content += """

### 10. `TZ_MedLink_PMG_Master_Specification.html` — Головне Технічне Завдання в стилі LABA
* Інженерна майстер-специфікація з 12 детальними скриншотами екранів (1600x1050).
* Поглиблений аналіз двох реальних файлів звітності НСЗУ (`Вересень 26.xlsx` на 5 490 ЕМЗ та `02000334_SF` на 4 394 ЕМЗ).
* Дорожня карта відновлення втрачених виплат (+₴) шляхом переподання до 10 числа.
* Інструменти пре-білінгу та планування дій лікаря в ЕМЗ (Anti-Defektura).
* Порівняльний аналіз конкурентів (Helsi, Doctor Eleks, Health24, info-pmg.com).
* Повна архітектура на C# (.NET Core 10) з Entity Framework Core та OpenXML.
"""

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("  [README] Updated medlink_pmg_bundle/README.md.")

    # 10. Create ZIP archive
    print("  [ZIP] Creating medlink_pmg_complete.zip...")
    if os.path.exists(zip_path):
        os.remove(zip_path)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zip_out:
        for root, dirs, files in os.walk(bundle_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, bundle_dir)
                zip_out.write(full_path, rel_path)

    zip_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"  [OK] Generated {zip_path} ({zip_size_mb:.2f} MB)")
    print("=== BUNDLE COMPLETED SUCCESSFULLY ===")

if __name__ == '__main__':
    make_bundle()
