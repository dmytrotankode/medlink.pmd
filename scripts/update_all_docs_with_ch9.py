import glob
import re

def update():
    files = glob.glob(r'c:\__MEDLINK___\PMG\docs_html\*.html')

    ch9_nav = """      <li class="nav-item">
        <a href="09_all_pmg_packages_normative_guide.html"><i class="material-icons">library_books</i> 9. Всі 46 пакетів ПМГ-2026</a>
      </li>"""

    sql10_nav = """      <li class="nav-item"><a href="#" onclick="openFileModal('10_seed_all_pmg2026_packages.sql')"><i class="material-icons">collections_bookmark</i> 10_seed_all_46_packages.sql</a></li>"""

    pattern_ch8 = r'(<a href="08_medlink_existing_ui_augmentation_guide\.html">[\s\S]*?</a>\s*</li>)'
    pattern_sql8 = r'(<a href="#" onclick="openFileModal\(\'08_seed_laboratory_tests_408\.sql\'\)">[\s\S]*?</a>\s*</li>)'

    for fp in files:
        if '09_all_pmg_packages_normative_guide.html' in fp:
            continue
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        # Add Ch9 link if not present
        if '09_all_pmg_packages_normative_guide.html' not in content:
            new_content, count = re.subn(pattern_ch8, r'\1\n' + ch9_nav, content)
            if count > 0:
                content = new_content
                changed = True
                print(f"Added Ch9 nav link to: {fp}")

        # Add SQL 10 link if not present
        if '10_seed_all_pmg2026_packages.sql' not in content:
            new_content, count = re.subn(pattern_sql8, r'\1\n' + sql10_nav, content)
            if count > 0:
                content = new_content
                changed = True
                print(f"Added SQL 10 modal link to: {fp}")

        if changed:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(content)

    # Now add Card 9 to docs_html/index.html
    index_path = r'c:\__MEDLINK___\PMG\docs_html\index.html'
    with open(index_path, 'r', encoding='utf-8') as f:
        idx_content = f.read()

    card9_html = """
      <!-- Doc 9 -->
      <div class="card" style="grid-column: span 2; background: #eef2ff; border: 1px solid #c7d2fe;">
        <div class="card-title">
          <span style="color: #3730a3;"><i class="material-icons" style="vertical-align: middle; margin-right: 6px;">library_books</i> 9. Реєстр та нормативне регулювання всіх 46 пакетів ПМГ-2026</span>
          <span class="badge badge-primary" style="background: #e0e7ff; color: #3730a3;">Постанова КМУ № 1808 (Всі 46 пакетів)</span>
        </div>
        <p class="card-desc" style="color: #312e81; font-size: 14px; line-height: 1.5;">
          Повний каталог та регулювання <strong>всіх 46 медичних пакетів Програми медичних гарантій 2026 року</strong> (не лише 3, 4, 9, 47):
          12 клініко-економічних кластерів, офіційні тарифи Постанови № 1808, математичні формули, вагові коефіцієнти ДСГ, критерії входу та валідації eHealth.
          Включає 12 автономних нормативних досьє в папці <code>normative_packages/</code>, зв'язок з EF Core (<code>pmg_packages</code>) та SQL сід <code>10_seed_all_pmg2026_packages.sql</code>.
        </p>
        <a href="09_all_pmg_packages_normative_guide.html" class="card-link" style="color: #3730a3; font-weight: 700;">Переглянути реєстр 46 пакетів та нормативну базу →</a>
      </div>
"""

    card8_end = """        <a href="08_medlink_existing_ui_augmentation_guide.html" class="card-link" style="color: #7e22ce; font-weight: 700;">Переглянути інструкцію модифікації існуючих форм →</a>
      </div>"""

    if card8_end in idx_content and '09_all_pmg_packages_normative_guide.html' not in idx_content:
        idx_content = idx_content.replace(card8_end, card8_end + card9_html, 1)
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(idx_content)
        print("Added Card 9 to docs_html/index.html")

    print("update_all_docs_with_ch9 completed.")

if __name__ == '__main__':
    update()
