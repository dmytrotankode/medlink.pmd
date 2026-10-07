import json
import os

def generate_ch9_html():
    manifest_path = r'c:\__MEDLINK___\PMG\normative_packages\all_packages_manifest.json'
    with open(manifest_path, 'r', encoding='utf-8') as f:
        packages = json.load(f)

    # Generate HTML table rows for all 46 packages
    rows_html = []
    for p in packages:
        p_id = p.get('id')
        code = p.get('code')
        name = p.get('name')
        cat = p.get('category')
        model = p.get('payment_model')
        rate = p.get('base_rate', 0)
        rate_str = f"{rate:,.2f} ₴".replace(',', ' ') if rate > 0 else "За формулою"
        period = p.get('rate_period', '')
        formula = p.get('formula', '')
        chapter = p.get('chapter_cmu', '')
        group_file = p.get('group_file', 'index.html')

        rows_html.append(f"""
        <tr id="row-pkg-{p_id}">
          <td style="text-align: center;"><span class="badge badge-primary">{code}</span></td>
          <td>
            <strong>{name}</strong>
            <div style="font-size: 11px; color: #64748b; margin-top: 2px;">{chapter}</div>
          </td>
          <td><span class="badge badge-info">{cat}</span></td>
          <td style="text-align: center;"><span class="badge badge-secondary">{model}</span></td>
          <td style="text-align: right; font-weight: 700; color: #16a34a;">
            {rate_str}
            <div style="font-size: 10px; color: #64748b;">{period}</div>
          </td>
          <td style="font-family: monospace; font-size: 11px; color: #0284c7; max-width: 280px; word-break: break-all;">
            {formula}
          </td>
          <td style="text-align: center; white-space: nowrap;">
            <a href="../normative_packages/{group_file}#pkg-{p_id}" target="_blank" class="btn-dossier" title="Відкрити нормативне досьє">
              <i class="material-icons" style="font-size: 14px; vertical-align: middle;">menu_book</i> Досьє
            </a>
          </td>
        </tr>
        """)

    packages_table_body = "\n".join(rows_html)

    html_content = f"""<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Розділ 9: Реєстр, нормативне регулювання та тарифи всіх 46 пакетів ПМГ-2026 — MedLink PMG Pro</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <link href="https://use.fontawesome.com/releases/v5.15.4/css/all.css" rel="stylesheet">
  <link rel="stylesheet" href="modal_viewer.css">

  <style>
    :root {{
      --primary: #4274A7;
      --primary-dark: #2c5277;
      --accent: #0178BC;
      --positive: #21ba45;
      --negative: #d04f45;
      --warning: #f2c037;
      --dark-sidebar: #212121;
      --bg-page: #f8fafc;
      --border-color: #e2e8f0;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Source Sans Pro', sans-serif;
      font-size: 15px;
      color: #334155;
      background-color: var(--bg-page);
      display: flex;
      min-height: 100vh;
    }}

    .sidebar {{
      width: 280px;
      background-color: var(--dark-sidebar);
      color: #f1f5f9;
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      position: sticky;
      top: 0;
      height: 100vh;
      border-right: 1px solid #333;
    }}

    .brand-header {{
      padding: 18px 20px;
      display: flex;
      align-items: center;
      gap: 12px;
      border-bottom: 1px solid #333;
      background: #1a1a1a;
    }}
    .brand-title {{ font-weight: 700; font-size: 16px; color: #fff; letter-spacing: 0.5px; }}
    .brand-sub {{ font-size: 11px; color: #94a3b8; }}

    .nav-list {{ list-style: none; padding: 12px 8px; overflow-y: auto; flex-grow: 1; }}
    .nav-section-title {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #64748b;
      padding: 12px 14px 6px 14px;
    }}
    .nav-item a {{
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 10px 14px;
      border-radius: 6px;
      color: #cbd5e1;
      text-decoration: none;
      font-size: 14px;
      transition: all 0.2s;
    }}
    .nav-item a:hover {{ background: rgba(255, 255, 255, 0.08); color: #fff; }}
    .nav-item.active a {{ background: var(--primary); color: #fff; font-weight: 600; }}
    .nav-item i {{ font-size: 18px; width: 20px; text-align: center; }}

    .prototype-btn-box {{ padding: 16px; border-top: 1px solid #333; background: #1a1a1a; }}
    .btn-proto {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      width: 100%;
      padding: 10px;
      background: #0284c7;
      color: #fff;
      text-decoration: none;
      border-radius: 6px;
      font-weight: 600;
      font-size: 13px;
      text-transform: uppercase;
    }}

    .main-content {{
      flex-grow: 1;
      padding: 32px 48px;
      overflow-y: auto;
      max-width: 1280px;
    }}
    .header-bar {{
      margin-bottom: 24px;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 16px;
    }}
    .h1-title {{
      font-size: 26px;
      font-weight: 800;
      color: #0f172a;
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 8px;
    }}
    .subtitle {{
      color: #64748b;
      font-size: 14px;
      line-height: 1.5;
    }}

    .callout {{
      padding: 14px 18px;
      border-radius: 6px;
      margin: 16px 0;
      font-size: 13px;
      line-height: 1.5;
    }}
    .callout-info {{ background: #eff6ff; border: 1px solid #bfdbfe; border-left: 4px solid #2563eb; color: #1e3a8a; }}
    .callout-success {{ background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid #16a34a; color: #14532d; }}
    .callout-warning {{ background: #fffbeb; border: 1px solid #fde68a; border-left: 4px solid #d97706; color: #78350f; }}

    .card-box {{
      background: #fff;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .card-title {{
      font-size: 18px;
      font-weight: 700;
      color: #0f172a;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    table.guide-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }}
    table.guide-table th {{ background: #f1f5f9; text-align: left; padding: 10px; border: 1px solid #cbd5e1; font-weight: 700; color: #1e293b; }}
    table.guide-table td {{ padding: 10px; border: 1px solid #cbd5e1; vertical-align: middle; }}

    .badge {{
      display: inline-block;
      padding: 3px 7px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
    }}
    .badge-primary {{ background: #e0e7ff; color: #3730a3; }}
    .badge-info {{ background: #e0f2fe; color: #0369a1; }}
    .badge-secondary {{ background: #f1f5f9; color: #475569; }}
    .badge-success {{ background: #dcfce7; color: #15803d; }}

    .btn-dossier {{
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      color: #1e293b;
      padding: 4px 8px;
      border-radius: 4px;
      text-decoration: none;
      font-size: 11px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: background 0.15s;
    }}
    .btn-dossier:hover {{
      background: #e2e8f0;
      color: #0284c7;
    }}

    .code-box {{
      background: #0f172a;
      border-radius: 6px;
      padding: 16px;
      margin: 12px 0;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      color: #f8fafc;
      overflow-x: auto;
      line-height: 1.5;
    }}

    .cluster-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
      margin-top: 14px;
    }}
    .cluster-card {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 16px;
      transition: transform 0.15s, border-color 0.15s;
    }}
    .cluster-card:hover {{
      transform: translateY(-2px);
      border-color: var(--primary);
    }}
    .cluster-title {{
      font-weight: 700;
      font-size: 14px;
      color: #0f172a;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .cluster-pkgs {{
      font-size: 12px;
      color: #64748b;
      margin-bottom: 10px;
    }}
  </style>
</head>
<body>

  <aside class="sidebar">
    <div class="brand-header">
      <img src="../prototype_medlink/medlink_small.svg" alt="MedLink Logo">
      <div>
        <div class="brand-title">MEDLINK PMG</div>
        <div class="brand-sub">Архітектура ПМГ 2026</div>
      </div>
    </div>

    <ul class="nav-list">
      <li class="nav-section-title">Головна навігація</li>
      <li class="nav-item"><a href="index.html"><i class="material-icons">dashboard</i> Архітектурний огляд</a></li>

      <li class="nav-section-title">Технічні специфікації</li>
      <li class="nav-item"><a href="01_database_schema.html"><i class="material-icons">storage</i> 1. Специфікація БД (EF Core)</a></li>
      <li class="nav-item"><a href="02_api_endpoints.html"><i class="material-icons">api</i> 2. Реєстр API Ендпоінтів</a></li>
      <li class="nav-item"><a href="03_business_logic_and_math.html"><i class="material-icons">calculate</i> 3. Математика тарифів</a></li>
      <li class="nav-item"><a href="04_openxml_processor.html"><i class="material-icons">description</i> 4. Процесор OpenXML</a></li>
      <li class="nav-item"><a href="05_frontend_integration_guide.html"><i class="material-icons">web</i> 5. Інтеграція у фронтенд</a></li>
      <li class="nav-item"><a href="06_pmg_dictionaries_catalog.html"><i class="material-icons">menu_book</i> 6. Довідники та MedProfit</a></li>
      <li class="nav-item"><a href="07_nszu_file_analysis_literal_compliance.html"><i class="material-icons">verified</i> 7. Аудит відповідності (info-pmg)</a></li>
      <li class="nav-item"><a href="08_medlink_existing_ui_augmentation_guide.html"><i class="material-icons">extension</i> 8. Доповнення існуючих форм МІС</a></li>
      <li class="nav-item active"><a href="09_all_pmg_packages_normative_guide.html"><i class="material-icons">library_books</i> 9. Всі 46 пакетів ПМГ-2026</a></li>
    </ul>

    <ul class="nav-list" style="margin-top: 10px; border-top: 1px solid #333;">
      <li class="nav-section-title">SQL Скрипти та DDL</li>
      <li class="nav-item"><a href="#" onclick="openFileModal('01_ddl_tables.sql')"><i class="material-icons">table_chart</i> 01_ddl_tables.sql</a></li>
      <li class="nav-item"><a href="#" onclick="openFileModal('02_queries_2way_matching.sql')"><i class="material-icons">search</i> 02_queries_matching.sql</a></li>
      <li class="nav-item"><a href="#" onclick="openFileModal('04_seed_dsg_catalog_465.sql')"><i class="material-icons">dns</i> 04_dsg_catalog_465.sql</a></li>
      <li class="nav-item"><a href="#" onclick="openFileModal('07_seed_doctor_position_requirements.sql')"><i class="material-icons">person</i> 07_doctor_positions.sql</a></li>
      <li class="nav-item"><a href="#" onclick="openFileModal('08_seed_laboratory_tests_408.sql')"><i class="material-icons">biotech</i> 08_lab_tests_408.sql</a></li>
      <li class="nav-item"><a href="#" onclick="openFileModal('10_seed_all_pmg2026_packages.sql')"><i class="material-icons">collections_bookmark</i> 10_seed_all_46_packages.sql</a></li>
    </ul>

    <div class="prototype-btn-box">
      <a href="../prototype_medlink/index.html" target="_blank" class="btn-proto">
        <i class="material-icons" style="font-size:18px;">play_circle_filled</i>
        Запустити прототип
      </a>
    </div>
  </aside>

  <main class="main-content">
    <div class="header-bar">
      <h1 class="h1-title">
        <i class="material-icons" style="font-size: 32px; color: var(--primary);">library_books</i>
        9. Повний реєстр, нормативне регулювання, тарифи та формули всіх 46 пакетів ПМГ-2026
      </h1>
      <p class="subtitle">
        Вичерпний технічний посібник для розробників та медичних аналітиків МІС «Медлінк»:
        нормативне регулювання згідно з <strong>Постановою Кабінету Міністрів України від 31.12.2025 № 1808 (зі змінами)</strong>,
        наказами МОЗ, розрахунковими формулами, ваговими коефіцієнтами ДСГ, моделями оплати та правилами верифікації eHealth.
      </p>
    </div>

    <div class="callout callout-success">
      <strong>⚖️ Нормативно-правова база 2026 року:</strong>
      Покриває не лише окремі стаціонарні пакети (3, 4, 9, 47), а <strong>всі 46 офіційних медичних пакетів Програми медичних гарантій 2026 року</strong>.
      Кожен пакет має своє автономне нормативне досьє у папці <code>normative_packages/</code>, закріплену законодавчу статтю Постанови № 1808,
      правила накладання КЕП, перевірки посад лікарів та ризики отримання дефектури (0 ₴) від НСЗУ.
    </div>

    <!-- Cluster Overview Cards -->
    <div class="card-box">
      <div class="card-title">
        <i class="material-icons" style="color: var(--primary);">grid_view</i>
        12 Клініко-економічних кластерів ПМГ-2026 (Постанова КМУ № 1808)
      </div>
      <p style="font-size: 13px; color: #64748b; margin-bottom: 12px;">
        Для структурованого ведення у МІС «Медлінк» всі 46 пакетів розподілено за 12 тематичними групами:
      </p>

      <div class="cluster-grid">
        <div class="cluster-card">
          <div class="cluster-title"><i class="material-icons" style="font-size: 18px; color: #0d9488;">healing</i> 1. Первинна допомога</div>
          <div class="cluster-pkgs">Пакет 1 (ПМД). Капітаційна ставка 1 007,30 ₴/рік. Вікові та гірські коефіцієнти.</div>
          <a href="../normative_packages/01_primary_care.html" target="_blank" class="btn-dossier">Відкрити досьє →</a>
        </div>

        <div class="cluster-card">
          <div class="cluster-title"><i class="material-icons" style="font-size: 18px; color: #dc2626;">airport_shuttle</i> 2. Екстрена допомога</div>
          <div class="cluster-pkgs">Пакет 2 (ЕМД). Капітаційна ставка 340,50 ₴/рік на мешканця області.</div>
          <a href="../normative_packages/02_emergency_care.html" target="_blank" class="btn-dossier">Відкрити досьє →</a>
        </div>

        <div class="cluster-card">
          <div class="cluster-title"><i class="material-icons" style="font-size: 18px; color: #4338ca;">local_hospital</i> 3. Спеціалізована та ДСГ</div>
          <div class="cluster-pkgs">Пакети 3 (Терапія), 4 (Хірургія), 47 (Хірургія 1-дня). База 8 735 ₴, 465 ДСГ.</div>
          <a href="../normative_packages/03_specialized_surgery_and_therapy_dsg.html" target="_blank" class="btn-dossier">Відкрити досьє →</a>
        </div>

        <div class="cluster-card">
          <div class="cluster-title"><i class="material-icons" style="font-size: 18px; color: #ea580c;">favorite</i> 4. Пріоритетні пакети</div>
          <div class="cluster-pkgs">Пакети 5 (Інсульт до 137k ₴), 6 (Інфаркт 44k..55k ₴), 7 (Пологи), 8 (Неонатологія), 35.</div>
          <a href="../normative_packages/04_priority_stroke_infarct_maternity.html" target="_blank" class="btn-dossier">Відкрити досьє →</a>
        </div>

        <div class="cluster-card">
          <div class="cluster-title"><i class="material-icons" style="font-size: 18px; color: #0284c7;">medical_services</i> 5. Амбулаторія та онкоскринінг</div>
          <div class="cluster-pkgs">Пакет 9 (148 класів, 155 ₴), Пакети 10..15 (6 онкоскринінгів), 16, 34 (Стоматологія), 42.</div>
          <a href="../normative_packages/05_ambulatory_outpatient_and_screening.html" target="_blank" class="btn-dossier">Відкрити досьє →</a>
        </div>

        <div class="cluster-card">
          <div class="cluster-title"><i class="material-icons" style="font-size: 18px; color: #9333ea;">biotech</i> 6. Онкологія та гематологія</div>
          <div class="cluster-pkgs">Пакет 18 (Хіміотерапія до 35 730 ₴), 19 (Радіологія до 131 499 ₴), 26 (Онкогематологія).</div>
          <a href="../normative_packages/06_oncology_and_hematology.html" target="_blank" class="btn-dossier">Відкрити досьє →</a>
        </div>

        <div class="cluster-card">
          <div class="cluster-title"><i class="material-icons" style="font-size: 18px; color: #16a34a;">accessibility_new</i> 7. Реабілітація</div>
          <div class="cluster-pkgs">Пакети 25 (Стаціонар 19 776..33 619 ₴), 53 (Монопрофільна 41 500 ₴), 54 (Амбулаторна 10 820 ₴).</div>
          <a href="../normative_packages/07_rehabilitation_care.html" target="_blank" class="btn-dossier">Відкрити досьє →</a>
        </div>

        <div class="cluster-card">
          <div class="cluster-title"><i class="material-icons" style="font-size: 18px; color: #78350f;">night_shelter</i> 8. Паліативна допомога</div>
          <div class="cluster-pkgs">Пакет 23 (Стаціонарна паліативна: 18 900 ₴), 24 (Мобільна паліативна: 14 200 ₴).</div>
          <a href="../normative_packages/08_palliative_care.html" target="_blank" class="btn-dossier">Відкрити досьє →</a>
        </div>

        <div class="cluster-card">
          <div class="cluster-title"><i class="material-icons" style="font-size: 18px; color: #475569;">psychology</i> 9. Психіатрія та терапія</div>
          <div class="cluster-pkgs">Пакети 22 (Стаціонарна психіатрія: 13 151 ₴), 27 (Мобільна: 10 535 ₴), 28 (ЗПТ), 30 (Первинка: 183 ₴).</div>
          <a href="../normative_packages/09_psychiatry_and_addiction.html" target="_blank" class="btn-dossier">Відкрити досьє →</a>
        </div>

        <div class="cluster-card">
          <div class="cluster-title"><i class="material-icons" style="font-size: 18px; color: #d97706;">coronavirus</i> 10. Інфекційні патології</div>
          <div class="cluster-pkgs">Пакети 20 (Туберкульоз: 43 780 ₴), 21 (ВІЛ/СНІД: 2 100 ₴), 29 (Вірусні гепатити).</div>
          <a href="../normative_packages/10_infectious_tb_hiv.html" target="_blank" class="btn-dossier">Відкрити досьє →</a>
        </div>

        <div class="cluster-card">
          <div class="cluster-title"><i class="material-icons" style="font-size: 18px; color: #0891b2;">science</i> 11. Високі технології</div>
          <div class="cluster-pkgs">Пакети 43 (Гемодіаліз: 2 460 ₴/сеанс), 46 (Перитонеальний), 59 (ДРТ: 60 324 ₴), 60 (Органи), 61 (ТКМ).</div>
          <a href="../normative_packages/11_high_tech_art_transplant.html" target="_blank" class="btn-dossier">Відкрити досьє →</a>
        </div>

        <div class="cluster-card">
          <div class="cluster-title"><i class="material-icons" style="font-size: 18px; color: #334155;">military_tech</i> 12. ВЛК та готовність</div>
          <div class="cluster-pkgs">Пакети 40 (Готовність ЗОЗ), 41 (НС), 44 (ВЛК: 883 ₴), 45 (Військовослужбовці), 58 (Зубопротезування: 14 984 ₴).</div>
          <a href="../normative_packages/12_defense_readiness_vlk.html" target="_blank" class="btn-dossier">Відкрити досьє →</a>
        </div>
      </div>
    </div>

    <!-- Master Table of 46 Packages -->
    <div class="card-box">
      <div class="card-title">
        <i class="material-icons" style="color: var(--primary);">table_chart</i>
        Повний реєстр 46 пакетів ПМГ-2026: Тарифи, Формули та Нормативне регулювання
      </div>
      <p style="font-size: 13px; color: #64748b; margin-bottom: 12px;">
        Дані синхронізовані з базою даних SQLite (<code>pmg_packages</code>), REST API (<code>/api/v1/pmg/dictionaries/packages</code>)
        та файлом сіду <a href="#" onclick="openFileModal('10_seed_all_pmg2026_packages.sql')">10_seed_all_pmg2026_packages.sql</a>:
      </p>

      <table class="guide-table">
        <thead>
          <tr>
            <th style="width: 70px; text-align: center;">Код</th>
            <th>Назва медичного пакета</th>
            <th>Категорія</th>
            <th style="text-align: center;">Модель оплати</th>
            <th style="text-align: right; width: 140px;">Базовий тариф</th>
            <th>Формула розрахунку</th>
            <th style="text-align: center; width: 90px;">Досьє</th>
          </tr>
        </thead>
        <tbody>
          {packages_table_body}
        </tbody>
      </table>
    </div>

    <!-- Database Schema & EF Core Integration -->
    <div class="card-box">
      <div class="card-title">
        <i class="material-icons" style="color: var(--primary);">storage</i>
        Схема бази даних: Сутність PmgPackage та зв'язок з MedLink (evomis)
      </div>
      <p style="font-size: 13px; color: #64748b; margin-bottom: 12px;">
        Для повної сумісності з EF Core сутність <code>PmgPackage</code> зв'язується з таблицями <code>dsg_nszu_statement_line</code>
        та <code>mis_encounter</code> через зовнішній ключ <code>package_id</code>:
      </p>

      <div class="code-box">
// C# Entity Framework Core: PmgPackage.cs
[Table("pmg_packages")]
public class PmgPackage
{{
    [Key]
    [Column("package_id")]
    [MaxLength(10)]
    public string PackageId {{ get; set; }} = string.Empty; // "1", "2", "3", "4", "47", "54"...

    [Required]
    [Column("name")]
    [MaxLength(255)]
    public string Name {{ get; set; }} = string.Empty;

    [Column("base_rate")]
    public decimal BaseRate {{ get; set; }}

    [Column("meta_json")]
    public string? MetaJson {{ get; set; }} // Повне досьє: формули, коефіцієнти, закони, валідації eHealth

    // Navigation properties
    public virtual ICollection&lt;DsgNszuStatementLine&gt; StatementLines {{ get; set; }} = new List&lt;DsgNszuStatementLine&gt;();
    public virtual ICollection&lt;MisEncounter&gt; Encounters {{ get; set; }} = new List&lt;MisEncounter&gt;();
}}
      </div>

      <div class="callout callout-info">
        <strong>SQL DDL & Скрипт завантаження:</strong>
        Усі 46 пакетів із формулами, посиланнями на закони та валідаціями доступні у файлі
        <a href="#" onclick="openFileModal('10_seed_all_pmg2026_packages.sql')">10_seed_all_pmg2026_packages.sql</a>.
        Файл можна переглянути та виконати прямо з інтерфейсу документації у спливаючому модальному вікні.
      </div>
    </div>

    <!-- REST API Controller -->
    <div class="card-box">
      <div class="card-title">
        <i class="material-icons" style="color: var(--primary);">api</i>
        REST API Ендпоінти класифікатора пакетів (PmgPackagesController)
      </div>
      <p style="font-size: 13px; color: #64748b; margin-bottom: 12px;">
        У бекенді реалізовано високопродуктивні ендпоінти для пошуку, фільтрації за категоріями та отримання повного досьє:
      </p>

      <table class="guide-table">
        <thead>
          <tr>
            <th>Метод & URI</th>
            <th>Параметри</th>
            <th>Призначення</th>
            <th>Відповідь</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>GET /api/v1/pmg/dictionaries/packages</code></td>
            <td><code>q</code> (пошук), <code>category</code> (категорія)</td>
            <td>Отримання списку всіх 46 пакетів або відфільтрованої вибірки</td>
            <td><code>200 OK</code>: JSON масив об'єктів пакетів з тарифами та формулами</td>
          </tr>
          <tr>
            <td><code>GET /api/v1/pmg/dictionaries/packages/{{id}}</code></td>
            <td><code>id</code> (номер пакета, напр. "4", "47", "54")</td>
            <td>Отримання вичерпного нормативного досьє обраного пакета</td>
            <td><code>200 OK</code>: Детальний JSON з коефіцієнтами, посиланнями на закони та eHealth валідаціями</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Frontend Quasar Component -->
    <div class="card-box">
      <div class="card-title">
        <i class="material-icons" style="color: var(--primary);">web</i>
        Фронтенд-компонент Quasar / Vue (PmgPackagesCatalog.vue)
      </div>
      <p style="font-size: 13px; color: #64748b; margin-bottom: 12px;">
        У каталозі <code>prototype_medlink/components/</code> створено готовий файл <code>PmgPackagesCatalog.vue</code>.
        Він містить інтерактивну таблицю з пошуком, фільтрами категорій, бейджами тарифів та модальним вікном <code>detailsDialog</code>.
      </p>
      <div class="code-box">
// Підключення у роутер MedLink (App.View/src/router/routes.js):
{{
  path: 'pmg/catalog-packages',
  name: 'pmg-catalog-packages',
  component: () => import('components/pmg/PmgPackagesCatalog.vue'),
  meta: {{ title: 'Всі 46 пакетів ПМГ-2026', requiresAuth: true }}
}}
      </div>
    </div>

    <!-- Regulatory Source Files Links -->
    <div class="card-box">
      <div class="card-title">
        <i class="material-icons" style="color: var(--primary);">picture_as_pdf</i>
        Офіційні першоджерела нормативної документації (PDF)
      </div>
      <p style="font-size: 13px; color: #64748b; margin-bottom: 12px;">
        У проєкті завантажено та доступно для безпосереднього перегляду офіційні текстові першоджерела НСЗУ:
      </p>
      <ul style="list-style-type: none; display: flex; flex-direction: column; gap: 8px;">
        <li>
          <a href="../extracted_data/normative_docs/pmg-2026.pdf" target="_blank" class="btn-dossier" style="font-size: 13px; padding: 8px 12px;">
            <i class="material-icons" style="color: #dc2626;">picture_as_pdf</i>
            <strong>pmg-2026.pdf</strong> — Офіційний повний текст Постанови КМУ № 1808 (43 сторінки)
          </a>
        </li>
        <li>
          <a href="../extracted_data/normative_docs/Додаток-1.pdf" target="_blank" class="btn-dossier" style="font-size: 13px; padding: 8px 12px;">
            <i class="material-icons" style="color: #0d9488;">picture_as_pdf</i>
            <strong>Додаток-1.pdf</strong> — Таблиця 465 Діагностично-споріднених груп (ДСГ) та вагові коефіцієнти (35 сторінок)
          </a>
        </li>
        <li>
          <a href="../extracted_data/normative_docs/Додаток-2.pdf" target="_blank" class="btn-dossier" style="font-size: 13px; padding: 8px 12px;">
            <i class="material-icons" style="color: #4338ca;">picture_as_pdf</i>
            <strong>Додаток-2.pdf</strong> — Перелік медичних послуг для хірургії одного дня (Пакет 47, 5 сторінок)
          </a>
        </li>
        <li>
          <a href="../normative_packages/index.html" target="_blank" class="btn-dossier" style="font-size: 13px; padding: 8px 12px; background: #e0f2fe; border-color: #0284c7; color: #0369a1;">
            <i class="material-icons" style="color: #0284c7;">language</i>
            <strong>normative_packages/index.html</strong> — Автономний браузер 12 нормативних HTML-досьє всіх 46 пакетів
          </a>
        </li>
      </ul>
    </div>

  </main>

  <script src="modal_viewer.js"></script>
</body>
</html>
"""

    output_path = r'c:\__MEDLINK___\PMG\docs_html\09_all_pmg_packages_normative_guide.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated {output_path} successfully ({len(packages)} packages rendered)!")

if __name__ == '__main__':
    generate_ch9_html()
