import glob
import re
import os

def update():
    files = glob.glob(r'c:\__MEDLINK___\PMG\docs_html\*.html')

    ch10_nav = """      <li class="nav-item">
        <a href="10_service_directory_norms_methodologies_combinations.html"><i class="material-icons">miscellaneous_services</i> 10. Справочник послуг та комбінації</a>
      </li>"""

    sql11_nav = """      <li class="nav-item"><a href="#" onclick="openFileModal('11_seed_service_combinations_and_groups.sql')"><i class="material-icons">schema</i> 11_service_combinations.sql</a></li>"""

    pattern_ch9 = r'(<a href="09_all_pmg_packages_normative_guide\.html">[\s\S]*?</a>\s*</li>)'
    pattern_sql10 = r'(<a href="#" onclick="openFileModal\(\'10_seed_all_pmg2026_packages\.sql\'\)">[\s\S]*?</a>\s*</li>)'

    for fp in files:
        if '10_service_directory_norms_methodologies_combinations.html' in fp or 'index.html' in fp:
            continue
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        # Add Ch10 link if not present
        if '10_service_directory_norms_methodologies_combinations.html' not in content:
            new_content, count = re.subn(pattern_ch9, r'\1\n' + ch10_nav, content)
            if count > 0:
                content = new_content
                changed = True
                print(f"Added Ch10 nav link to: {os.path.basename(fp)}")

        # Add SQL 11 link if not present
        if '11_seed_service_combinations_and_groups.sql' not in content:
            new_content, count = re.subn(pattern_sql10, r'\1\n' + sql11_nav, content)
            if count > 0:
                content = new_content
                changed = True
                print(f"Added SQL 11 modal link to: {os.path.basename(fp)}")

        if changed:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(content)

    # Now update TZ_MedLink_PMG_Analytics.html
    tz_path = r'c:\__MEDLINK___\PMG\TZ_MedLink_PMG_Analytics.html'
    with open(tz_path, 'r', encoding='utf-8') as f:
        tz_content = f.read()

    tz_changed = False

    # Update quick-proto-nav
    if '📚 Технічна документація (9 розділів)' in tz_content:
        tz_content = tz_content.replace(
            '📚 Технічна документація (9 розділів)',
            '📚 Технічна документація (10 розділів)'
        )
        tz_changed = True

    if '10_service_directory_norms_methodologies_combinations.html' not in tz_content:
        # Add link in quick nav
        target_nav_item = '<a href="normative_packages/index.html" target="_blank" style="background: #059669;">⚖️ Всі 46 пакетів ПМГ (12 досьє) ↗</a>'
        addition_nav_item = '\n    <a href="docs_html/10_service_directory_norms_methodologies_combinations.html" target="_blank" style="background: #0d9488;">🩺 Справочник послуг та комбінацій (АКПІ) ↗</a>'
        if target_nav_item in tz_content:
            tz_content = tz_content.replace(target_nav_item, target_nav_item + addition_nav_item, 1)
            tz_changed = True

        # Add subsection 2.5
        sec2_end = """        Деталізовані нормативні досьє, законодавчі акти та таблиці валідацій див. у 
        <a href="docs_html/09_all_pmg_packages_normative_guide.html" target="_blank" style="color: var(--ml-accent); font-weight: 700;">Розділі 9 технічної документації ↗</a>
        та автономному браузері <a href="normative_packages/index.html" target="_blank" style="color: var(--ml-accent); font-weight: 700;">normative_packages/index.html ↗</a>.
      </p>
    </section>"""

        sec25_html = """        Деталізовані нормативні досьє, законодавчі акти та таблиці валідацій див. у 
        <a href="docs_html/09_all_pmg_packages_normative_guide.html" target="_blank" style="color: var(--ml-accent); font-weight: 700;">Розділі 9 технічної документації ↗</a>
        та автономному браузері <a href="normative_packages/index.html" target="_blank" style="color: var(--ml-accent); font-weight: 700;">normative_packages/index.html ↗</a>.
      </p>

      <h3 class="sub-title">2.5. Справочник послуг (АКПІ): норми, методики та конфігуратор усіх можливих комбінацій (Delphi Re-engineering)</h3>
      <p>
        На основі реверс-інжинірингу класичної системи Delphi (модулі <code>fMain.pas</code>, <code>d53_54.pas</code> та таблиці правил <code>dct_mp_service_odk_rule_detail</code>) розширено підсистему класифікатора послуг АКПІ:
      </p>
      <div style="background: #f0fdfa; border: 1px solid #99f6e4; border-radius: 8px; padding: 14px; margin-bottom: 14px; font-size: 0.875rem;">
        <ul style="margin-bottom: 0;">
          <li><strong>12 клініко-технологічних груп послуг:</strong> загальна хірургія, онкохірургія, ендоскопія, інтенсивна терапія, анестезіологія, діагностика та реабілітація.</li>
          <li><strong>Паспорт послуги та клінічні норми:</strong> нормативний час виконання (хв), тип анестезії, мінімальний та максимальний термін госпіталізації (ліжко-дні), вікові цензи (мін/макс), статева специфічність, кваліфікаційні вимоги до лікаря (спеціальність та сертифікат).</li>
          <li><strong>Матриця комбінацій та валідатор:</strong> перевірка комбінацій у реальному часі (обов'язкові супутні ко-реквізити, несумісні інтервенції, сумісні МКХ-10, допустимі/заборонені посади лікарів).</li>
          <li><strong>Підвищувальний коефіцієнт мультихірургії (1.30):</strong> при одночасному виконанні додаткових хірургічних втручань тариф базової ДСГ помножується на коефіцієнт мультихірургії <strong>1.30</strong> (наприклад, 21 257.50 ₴ → 27 634.75 ₴), захищаючи лікарню від дефектури та недофінансування.</li>
          <li><strong>Бібліотека еталонних комбінацій (аналог <code>myAddLib</code>):</strong> збереження затверджених шаблонів комбінацій, порівняння з поточним протоколом та підсвічування різниці вартості (зелений прибуток / червоний збиток).</li>
          <li><strong>Наскрізний Drill-down до реальних пацієнтів та 45 колонок:</strong> прямий перехід від картки послуги та правила до таблиці виписаних ЕМЗ пацієнтів і повного аудиту аркуша «Розшифровка».</li>
        </ul>
      </div>
      <p>
        Детальний технічний опис, DDL та інтерактивний симулятор див. у 
        <a href="docs_html/10_service_directory_norms_methodologies_combinations.html" target="_blank" style="color: #0f766e; font-weight: 700;">Розділі 10 технічної документації ↗</a>
        та SQL-скрипті <code>sql/11_seed_service_combinations_and_groups.sql</code>.
      </p>
    </section>"""

        if sec2_end in tz_content:
            tz_content = tz_content.replace(sec2_end, sec25_html, 1)
            tz_changed = True
            print("Added subsection 2.5 to TZ.")

        # Add DDL in Section 6
        target_ddl = "// 5. Журнал розбіжностей звіту НСЗУ з ЕМЗ Медлінка"
        addition_ddl = """// 6. Довідник груп послуг (12 клінічних груп)
CREATE TABLE pmg_service_groups (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_id VARCHAR(50),
    description TEXT,
    service_count INT DEFAULT 0
);

// 7. Справочник послуг АКПІ з клінічними нормами
CREATE TABLE pmg_service_catalog (
    service_code VARCHAR(30) PRIMARY KEY,
    service_name VARCHAR(500) NOT NULL,
    group_id VARCHAR(50) REFERENCES pmg_service_groups(id),
    category VARCHAR(50),
    base_time_minutes INT,
    anesthesia_type VARCHAR(50),
    min_bed_days INT,
    max_bed_days INT,
    allowed_gender VARCHAR(10),
    min_age INT,
    max_age INT,
    doctor_qualification_req TEXT,
    standard_cost_uah NUMERIC(12,2),
    is_active BOOLEAN DEFAULT TRUE
);

// 8. Матриця комбінацій послуг (Delphi dct_mp_service_odk_rule_detail)
CREATE TABLE pmg_service_combinations (
    id UUID PRIMARY KEY,
    service_code VARCHAR(30) REFERENCES pmg_service_catalog(service_code),
    rule_name VARCHAR(255) NOT NULL,
    allowed_icd_codes TEXT,
    mandatory_companion_services TEXT,
    multi_surgery_companion_services TEXT,
    multi_surgery_coefficient NUMERIC(4,2) DEFAULT 1.30,
    prohibited_companion_services TEXT,
    allowed_doctor_positions TEXT,
    prohibited_doctor_positions TEXT,
    standard_tariff_uah NUMERIC(12,2),
    is_library_standard BOOLEAN DEFAULT FALSE
);

"""
        if target_ddl in tz_content:
            tz_content = tz_content.replace(target_ddl, addition_ddl + target_ddl, 1)
            tz_changed = True
            print("Added DDL for service catalog & combinations to Section 6 of TZ.")

    if tz_changed:
        with open(tz_path, 'w', encoding='utf-8') as f:
            f.write(tz_content)
        print("Updated TZ_MedLink_PMG_Analytics.html successfully.")

if __name__ == '__main__':
    update()
