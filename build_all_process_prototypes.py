import os

PROTOTYPE_DIR = "c:/__MEDLINK___/PMG/prototype"
os.makedirs(PROTOTYPE_DIR, exist_ok=True)

# Common HTML Head
COMMON_HEAD = """
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --ml-primary: #0e508b;
      --ml-primary-dark: #0a3a66;
      --ml-primary-light: #166ba8;
      --ml-accent: #0086ff;
      --ml-accent-cyan: #00c0f0;
      --ml-bg: #f8fafc;
      --ml-card-bg: #ffffff;
      --ml-text: #1e293b;
      --ml-text-muted: #64748b;
      --ml-border: #e2e8f0;
      --ml-success: #10b981;
      --ml-success-light: #ecfdf5;
      --ml-warning: #f59e0b;
      --ml-warning-light: #fffbeb;
      --ml-danger: #ef4444;
      --ml-danger-light: #fef2f2;
      --ml-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
      --ml-shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.05);
      --radius: 10px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    body { background-color: var(--ml-bg); color: var(--ml-text); min-height: 100vh; display: flex; flex-direction: column; }

    .ml-header {
      background: linear-gradient(135deg, var(--ml-primary-dark) 0%, var(--ml-primary) 100%);
      color: white; padding: 0.75rem 1.5rem; display: flex; justify-content: space-between; align-items: center;
      border-bottom: 3px solid var(--ml-accent); box-shadow: var(--ml-shadow); position: sticky; top: 0; z-index: 100;
    }
    .ml-brand { display: flex; align-items: center; gap: 12px; }
    .ml-logo-box {
      width: 42px; height: 42px; background: white; border-radius: 8px;
      display: flex; align-items: center; justify-content: center; overflow: hidden;
      box-shadow: 0 2px 4px rgba(0,0,0,0.15); font-weight: 800; color: var(--ml-primary); font-size: 1.2rem;
    }
    .ml-brand-titles h1 { font-size: 1.15rem; font-weight: 800; letter-spacing: -0.02em; display: flex; align-items: center; gap: 8px; }
    .ml-brand-titles h1 span.badge-pro {
      background: var(--ml-accent-cyan); color: #0a3a66; font-size: 0.65rem;
      padding: 2px 7px; border-radius: 4px; font-weight: 800; text-transform: uppercase;
    }
    .ml-brand-titles p { font-size: 0.75rem; color: #cbd5e1; }

    .hosp-select {
      background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3);
      color: white; padding: 7px 12px; border-radius: 8px; font-size: 0.825rem; font-weight: 600;
      cursor: pointer; outline: none;
    }
    .hosp-select option { background: #0a3a66; color: white; }

    .ml-nav {
      background: white; border-bottom: 1px solid var(--ml-border);
      padding: 0 1.5rem; display: flex; gap: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.03); overflow-x: auto;
    }
    .nav-btn {
      padding: 12px 14px; border: none; background: transparent; font-size: 0.825rem; font-weight: 600;
      color: var(--ml-text-muted); cursor: pointer; display: flex; align-items: center; gap: 6px;
      border-bottom: 3px solid transparent; text-decoration: none; white-space: nowrap; transition: all 0.2s ease;
    }
    .nav-btn:hover { color: var(--ml-primary); background: #f8fafc; }
    .nav-btn.active { color: var(--ml-primary); border-bottom-color: var(--ml-accent); font-weight: 700; }
    .nav-btn .pill { background: #e2e8f0; color: #475569; font-size: 0.7rem; padding: 2px 6px; border-radius: 10px; font-weight: 700; }
    .nav-btn.active .pill { background: var(--ml-accent); color: white; }

    .ml-container { max-width: 1560px; margin: 1.5rem auto; padding: 0 1.5rem; flex: 1; width: 100%; }

    .process-banner {
      background: #eff6ff; border: 1px solid #bfdbfe; border-left: 5px solid var(--ml-accent);
      border-radius: var(--radius); padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; box-shadow: var(--ml-shadow);
    }
    .process-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
    .process-title { font-size: 1.1rem; font-weight: 800; color: #1e3a8a; display: flex; align-items: center; gap: 8px; }
    .process-meta-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-top: 10px; font-size: 0.8rem; border-top: 1px solid #dbeafe; padding-top: 10px; }
    .process-meta-item strong { display: block; color: #1e40af; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 2px; }
    .process-meta-item span { color: #1e3a8a; }

    .content-card {
      background: white; border-radius: var(--radius); border: 1px solid var(--ml-border);
      box-shadow: var(--ml-shadow); padding: 1.5rem; margin-bottom: 1.5rem;
    }
    .card-header {
      display: flex; justify-content: space-between; align-items: center;
      margin-bottom: 1.25rem; padding-bottom: 0.75rem; border-bottom: 1px solid var(--ml-border);
    }
    .card-header h2 { font-size: 1.1rem; font-weight: 700; color: var(--ml-primary); display: flex; align-items: center; gap: 8px; }
    .card-header p { font-size: 0.8rem; color: var(--ml-text-muted); }

    .btn {
      padding: 9px 16px; border-radius: 8px; font-size: 0.85rem; font-weight: 600;
      border: none; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; text-decoration: none; transition: all 0.2s;
    }
    .btn-primary { background: var(--ml-accent); color: white; }
    .btn-primary:hover { background: #0070d6; }
    .btn-outline { background: white; border: 1px solid var(--ml-border); color: var(--ml-text); }
    .btn-outline:hover { background: #f1f5f9; border-color: #cbd5e1; }
    .btn-success { background: var(--ml-success); color: white; }
    .btn-success:hover { background: #059669; }

    .badge { display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 0.725rem; font-weight: 700; white-space: nowrap; }
    .badge-success { background: var(--ml-success-light); color: var(--ml-success); border: 1px solid #a7f3d0; }
    .badge-info { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }
    .badge-danger { background: var(--ml-danger-light); color: var(--ml-danger); border: 1px solid #fecaca; }
    .badge-warning { background: var(--ml-warning-light); color: #b45309; border: 1px solid #fde68a; }
    .badge-gray { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }

    .code-tag {
      font-family: 'JetBrains Mono', monospace; font-size: 0.775rem; background: #f1f5f9;
      padding: 2px 6px; border-radius: 4px; border: 1px solid #cbd5e1; color: #0f172a;
    }

    .search-input {
      padding: 9px 14px; border: 1px solid var(--ml-border); border-radius: 8px; font-size: 0.875rem;
      min-width: 260px; outline: none; transition: border-color 0.2s;
    }
    .search-input:focus { border-color: var(--ml-accent); box-shadow: 0 0 0 3px rgba(0, 134, 255, 0.15); }

    .encounter-field { background: #f8fafc; border: 1px solid var(--ml-border); padding: 8px 12px; border-radius: 6px; font-size: 0.8rem; }
    .encounter-field strong { display: block; color: #64748b; font-size: 0.7rem; text-transform: uppercase; margin-bottom: 2px; }

    .table-responsive { width: 100%; overflow-x: auto; border: 1px solid var(--ml-border); border-radius: 8px; }
    .ml-table { width: 100%; border-collapse: collapse; font-size: 0.825rem; text-align: left; }
    .ml-table th { background: #f8fafc; color: #475569; font-weight: 700; padding: 10px 12px; border-bottom: 2px solid var(--ml-border); white-space: nowrap; }
    .ml-table td { padding: 9px 12px; border-bottom: 1px solid var(--ml-border); color: var(--ml-text); vertical-align: middle; }
    .ml-table tr:hover { background-color: #f1f5f9; }
    .ml-table tr.row-rejected { background-color: #fffafb; }

    .ml-footer {
      background: white; border-top: 1px solid var(--ml-border); padding: 1.25rem 1.5rem;
      font-size: 0.8rem; color: var(--ml-text-muted); display: flex; justify-content: space-between; align-items: center; margin-top: auto;
    }
  </style>
"""

def make_nav(active_file):
    items = [
        ("index.html", "🌐 Портал (Всі процеси)", ""),
        ("process_1_prebilling.html", "1. Пре-білінг лікаря", "П1"),
        ("process_2_upload.html", "2. Імпорт звіту НСЗУ", "П2"),
        ("process_3_financial_audit.html", "3. Фінансовий аудит (45 колонок)", "П3"),
        ("process_4_discrepancies.html", "4. Журнал розбіжностей 2-Way", "П4"),
        ("process_5_correction.html", "5. Асистент виправлення", "П5"),
        ("process_6_catalog.html", "6. Довідник нормативів", "П6"),
    ]
    lines = ['<nav class="ml-nav">']
    for fn, title, pill in items:
        is_act = (fn == active_file)
        cls = "nav-btn active" if is_act else "nav-btn"
        p_html = f' <span class="pill">{pill}</span>' if pill else ''
        lines.append(f'  <a href="{fn}" class="{cls}"><span>{title}</span>{p_html}</a>')
    lines.append('</nav>')
    return '\n'.join(lines)

# Write template helper
def write_proto(filename, title, process_num, role_str, norm_str, desc_str, effect_str, body_html, js_script=""):
    nav_html = make_nav(filename)
    full_html = f"""<!DOCTYPE html>
<html lang="uk">
<head>
  <title>{title} — MedLink PMG Pro</title>
  {COMMON_HEAD}
</head>
<body>
  <header class="ml-header">
    <div class="ml-brand">
      <div class="ml-logo-box">ML</div>
      <div class="ml-brand-titles">
        <h1>MedLink PMG Analytics <span class="badge-pro">PRO 2026</span></h1>
        <p>Процес {process_num}: {title}</p>
      </div>
    </div>
    <div style="display:flex; align-items:center; gap:12px;">
      <span class="badge badge-info">● {role_str}</span>
      <a href="../TZ_MedLink_PMG_Analytics.html#process-{process_num}" class="btn btn-outline" style="background:rgba(255,255,255,0.15); color:white; border-color:rgba(255,255,255,0.3); font-size:0.75rem;">📖 Читати в ТЗ →</a>
    </div>
  </header>

  {nav_html}

  <main class="ml-container">
    <div class="process-banner">
      <div class="process-header">
        <div class="process-title">
          <span>⚡</span> БІЗНЕС-ПРОЦЕС {process_num}: {title}
        </div>
        <span class="badge badge-success" style="font-size:0.8rem;">Прототип готовий</span>
      </div>
      <p style="font-size:0.85rem; color:#1e3a8a; line-height:1.5;">
        <strong>Суть процесу:</strong> {desc_str}
      </p>
      <div class="process-meta-grid">
        <div class="process-meta-item">
          <strong>Хто виконує:</strong>
          <span>{role_str}</span>
        </div>
        <div class="process-meta-item">
          <strong>Нормативна база:</strong>
          <span>{norm_str}</span>
        </div>
        <div class="process-meta-item">
          <strong>Точка входу в Медлінку:</strong>
          <span>Компонент МІС «Медлінк»</span>
        </div>
        <div class="process-meta-item">
          <strong>Бізнес-ефект:</strong>
          <span>{effect_str}</span>
        </div>
      </div>
    </div>

    {body_html}
  </main>

  <footer class="ml-footer">
    <div>МІС «Медлінк» • Процес {process_num}: {title}</div>
    <div>Нормативна база: Постанова КМУ №1808 від 27.12.2024</div>
  </footer>

  <script src="data.js"></script>
  <script>
    {js_script}
  </script>
</body>
</html>
"""
    with open(os.path.join(PROTOTYPE_DIR, filename), "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Written: {filename}")

# ----------------- PROCESS 1 -----------------
b1 = """
<div class="content-card">
  <div class="card-header">
    <div>
      <h2><span>🩺</span> Робоче місце лікаря-онколога • Створення стаціонарної взаємодії</h2>
      <p>Пацієнт: Мельник Олексій Володимирович (58 років, Історія хвороби №125601)</p>
    </div>
    <span class="badge badge-gray">Чернетка ЕМЗ</span>
  </div>

  <div style="display:grid; grid-template-columns: 1.15fr 1fr; gap: 24px;">
    <div style="background:#f8fafc; border:1px solid var(--ml-border); border-radius:10px; padding:1.25rem;">
      <h3 style="font-size:0.95rem; font-weight:700; color:var(--ml-primary); margin-bottom:12px;">Клінічні дані ЕМЗ</h3>
      <div style="margin-bottom:12px;">
        <label style="font-size:0.775rem; font-weight:700; color:#334155; display:block; margin-bottom:4px;">Пакет медичних послуг:</label>
        <select id="sim-package" class="search-input" style="width:100%;" onchange="recalc()">
          <option value="4" selected>Пакет 4: Хірургічні операції у стаціонарі</option>
          <option value="3">Пакет 3: Стаціонарна допомога без операцій (терапія)</option>
          <option value="47">Пакет 47: Хірургія одного дня</option>
          <option value="9">Пакет 9: Амбулаторна допомога</option>
          <option value="17">Пакет 17: Хіміотерапевтичне лікування онкохворих</option>
        </select>
      </div>

      <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-bottom:12px;">
        <div>
          <label style="font-size:0.775rem; font-weight:700; color:#334155; display:block; margin-bottom:4px;">Основний діагноз (МКХ-10):</label>
          <input type="text" id="sim-diag" class="search-input" style="width:100%; font-weight:600;" value="C18.0" oninput="recalc()">
        </div>
        <div>
          <label style="font-size:0.775rem; font-weight:700; color:#334155; display:block; margin-bottom:4px;">Послуга АКПІ (Інтервенція):</label>
          <input type="text" id="sim-svc" class="search-input" style="width:100%; font-weight:600;" value="30061-02" oninput="recalc()">
        </div>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; margin-top:15px; border-top:1px dashed #cbd5e1; padding-top:12px;">
        <button class="btn btn-outline" onclick="document.getElementById('sim-svc').value=''; recalc();">⚠️ Стерти АКПІ (Перевірка алерта)</button>
        <button class="btn btn-success" onclick="alert('✅ Взаємодію підписано КЕП та передано в ЕСОЗ!')">🔏 Підписати КЕП</button>
      </div>
    </div>

    <div id="prebilling-box" style="background:#f0fdf4; border:2px solid #86efac; border-radius:12px; padding:1.5rem; display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; border-bottom:1px solid #bbf7d0; padding-bottom:8px;">
          <span style="font-weight:800; color:#15803d; font-size:0.95rem;">⚡ ВІДЖЕТ ПРЕ-БІЛІНГУ МЕДЛІНКА</span>
          <span id="p1-badge" class="badge badge-success">Валідацію пройдено</span>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:12px;">
          <div class="encounter-field"><strong>ДСГ випадку:</strong><span id="p1-dsg" style="font-weight:700; color:var(--ml-primary);">G01</span></div>
          <div class="encounter-field"><strong>Коефіцієнт:</strong><span id="p1-coeff" style="font-weight:700;">5.070</span></div>
          <div class="encounter-field"><strong>Базова ставка:</strong><span>8 735.00 ₴</span></div>
          <div class="encounter-field"><strong>Коригувальний K:</strong><span>0.55</span></div>
        </div>
        <div class="encounter-field" style="margin-bottom:12px;">
          <strong>Клінічна назва групи:</strong><span id="p1-name">Резекція прямої кишки та складні втручання на ободовій кишці</span>
        </div>
        <div id="p1-msg" style="background:white; border:1px solid #bbf7d0; border-left:4px solid #16a34a; padding:10px 12px; border-radius:6px; font-size:0.8rem; color:#166534;">
          ✓ Кодування коректне. Інтервенція відповідає діагнозу. Ризик відхилення 0%.
        </div>
      </div>
      <div style="background:white; border:2px solid #86efac; border-radius:10px; padding:15px; display:flex; justify-content:space-between; align-items:center; margin-top:15px;">
        <div>
          <span style="font-size:0.75rem; font-weight:700; color:#166534; text-transform:uppercase;">Очікуваний дохід:</span>
          <div id="p1-sum" style="font-size:1.85rem; font-weight:800; color:#15803d; line-height:1.1;">24 357.55 ₴</div>
        </div>
        <span class="badge badge-success">Тариф ПМГ-2026</span>
      </div>
    </div>
  </div>
</div>
"""
js1 = """
function recalc() {
  const pkg = document.getElementById('sim-package').value;
  const diag = (document.getElementById('sim-diag').value || '').trim();
  const svc = (document.getElementById('sim-svc').value || '').trim();
  const box = document.getElementById('prebilling-box');
  const badge = document.getElementById('p1-badge');
  const msg = document.getElementById('p1-msg');
  const sum = document.getElementById('p1-sum');

  if (!svc && (pkg === '4' || pkg === '47')) {
    box.style.background = '#fef2f2'; box.style.borderColor = '#fca5a5';
    badge.className = 'badge badge-danger'; badge.textContent = 'Ризик відхилення (100%)';
    msg.style.borderColor = '#fca5a5'; msg.style.borderLeftColor = '#ef4444'; msg.style.color = '#991b1b';
    msg.innerHTML = '❌ <strong>УВАГА:</strong> Для діагнозу ' + diag + ' у пакеті 4 обов’язкова процедура розділу 30061. Без неї тариф 0 ₴!';
    sum.textContent = '0.00 ₴'; sum.style.color = '#dc2626';
    document.getElementById('p1-dsg').textContent = '—';
    return;
  }
  box.style.background = '#f0fdf4'; box.style.borderColor = '#86efac';
  badge.className = 'badge badge-success'; badge.textContent = 'Валідацію пройдено';
  msg.style.borderColor = '#bbf7d0'; msg.style.borderLeftColor = '#16a34a'; msg.style.color = '#166534';
  msg.innerHTML = '✓ Кодування коректне. Інтервенція відповідає діагнозу. Ризик відхилення 0%.';
  sum.textContent = '24 357.55 ₴'; sum.style.color = '#15803d';
  document.getElementById('p1-dsg').textContent = 'G01';
}
"""

write_proto(
    "process_1_prebilling.html",
    "Пре-білінг та онлайн-контроль у картці лікаря",
    1,
    "Лікар-клініцист (стаціонар / амбулаторія)",
    "Постанова КМУ №1808 (Додаток 1), Наказ №377",
    "Реактивний розрахунок австралійської ДСГ та тарифу в момент заповнення ЕМЗ до підписання КЕП. Попередження про забуті коди АКПІ та ризики обнулення виплат.",
    "Усунення 100% помилок незаповнення обов'язкових послуг до відправки в ЕСОЗ.",
    b1, js1
)

# ----------------- PROCESS 2 -----------------
b2 = """
<div class="content-card">
  <div class="card-header">
    <div>
      <h2><span>📂</span> Модуль завантаження та потокового розбору звітів НСЗУ</h2>
      <p>Потоковий OpenXML процесор для миттєвої обробки файлів до 50 000 рядків</p>
    </div>
  </div>

  <div style="border: 2px dashed #93c5fd; background: #f0f7ff; border-radius: 12px; padding: 2.5rem; text-align: center; margin-bottom: 1.5rem;">
    <div style="font-size: 2.5rem; margin-bottom: 8px;">📊</div>
    <h3 style="font-size: 1.1rem; font-weight: 700; color: #1e40af; margin-bottom: 4px;">Перетягніть файл звіту НСЗУ (.xlsx) сюди</h3>
    <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 15px;">або оберіть зі зразків реальних звітів нижче</p>
    <div style="display:flex; justify-content:center; gap:12px;">
      <button class="btn btn-primary" onclick="simulateUpload('oco')">📂 Завантажити зразок: «Вересень 26.xlsx» (КНП "ОЦО", 5 490 ЕМЗ)</button>
      <button class="btn btn-outline" onclick="simulateUpload('dkl')">📂 Завантажити зразок: «02000334_SF_2026.xlsx» (КНП "ДКЛ Св. Зінаїди", 4 394 ЕМЗ)</button>
    </div>
  </div>

  <div id="ingest-card" style="display:none; background:#f8fafc; border:1px solid var(--ml-border); border-radius:10px; padding:1.25rem;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
      <strong id="ingest-title" style="color:var(--ml-primary); font-size:0.95rem;">Обробка...</strong>
      <span id="ingest-badge" class="badge badge-info">Обробка</span>
    </div>
    <div style="width:100%; height:8px; background:#e2e8f0; border-radius:4px; overflow:hidden; margin-bottom:15px;">
      <div id="ingest-bar" style="width:0%; height:100%; background:var(--ml-accent); transition:width 0.4s ease;"></div>
    </div>
    <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; font-size:0.8rem; margin-bottom:15px;">
      <div class="encounter-field"><strong>1. Аркуші:</strong><span id="s1" style="color:#059669; font-weight:700;">Очікування...</span></div>
      <div class="encounter-field"><strong>2. 45 Колонок:</strong><span id="s2" style="color:#059669; font-weight:700;">Очікування...</span></div>
      <div class="encounter-field"><strong>3. Тарифікація:</strong><span id="s3" style="color:#059669; font-weight:700;">Очікування...</span></div>
      <div class="encounter-field"><strong>4. 2-Way звірка:</strong><span id="s4" style="color:#059669; font-weight:700;">Очікування...</span></div>
    </div>
    <div id="ingest-res" style="display:none; background:#ecfdf5; border:1px solid #a7f3d0; border-radius:8px; padding:12px; font-size:0.85rem; color:#065f46;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>✓ <strong>Звіт успішно імпортовано!</strong> Оброблено <span id="r-rows" style="font-weight:700;">5 490</span> записів. Виявлено втрат на <span id="r-lost" style="font-weight:700; color:#dc2626;">4 974 842 ₴</span>.</div>
        <a href="process_3_financial_audit.html" class="btn btn-success" style="font-size:0.8rem;">Перейти до фінансового аудиту (Процес 3) →</a>
      </div>
    </div>
  </div>
</div>
"""
js2 = """
function simulateUpload(type) {
  const card = document.getElementById('ingest-card');
  const bar = document.getElementById('ingest-bar');
  const title = document.getElementById('ingest-title');
  const badge = document.getElementById('ingest-badge');
  const res = document.getElementById('ingest-res');

  card.style.display = 'block'; res.style.display = 'none';
  bar.style.width = '20%'; badge.textContent = 'Читання Excel...';
  title.textContent = (type === 'oco') ? 'Аналіз файлу: Вересень 26.xlsx (ОЦО)...' : 'Аналіз файлу: 02000334_SF_2026.xlsx (ДКЛ)...';
  document.getElementById('s1').textContent = '4 аркуші знайдено ✓';

  setTimeout(() => { bar.style.width = '55%'; document.getElementById('s2').textContent = '45 колонок верифіковано ✓'; }, 400);
  setTimeout(() => { bar.style.width = '80%'; document.getElementById('s3').textContent = 'Тарифи ПМГ нараховано ✓'; }, 800);
  setTimeout(() => {
    bar.style.width = '100%'; badge.className = 'badge badge-success'; badge.textContent = 'Готово';
    document.getElementById('s4').textContent = '2-Way співставлено ✓';
    res.style.display = 'block';
    document.getElementById('r-rows').textContent = (type === 'oco') ? '5 490 ЕМЗ' : '4 394 ЕМЗ';
    document.getElementById('r-lost').textContent = (type === 'oco') ? '4 974 842 ₴' : '3 674 400 ₴';
  }, 1200);
}
"""

write_proto(
    "process_2_upload.html",
    "Імпорт та потоковий парсинг звіту НСЗУ",
    2,
    "Головний економіст / Медичний директор",
    "Формат вивантаження ЕСОЗ/НСЗУ 2026 року",
    "Потокова обробка щомісячного файлу НСЗУ через NszuReportXlsxProcessor. Перевірка наявності 4 аркушів, структури 45 колонок, ініціація розрахунку тарифів.",
    "Автоматичний аудит 5 000+ записів менше ніж за 2 секунди.",
    b2, js2
)

# ----------------- PROCESS 3 -----------------
b3 = """
<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
  <div style="background:white; border-radius:10px; padding:1.15rem; border:1px solid var(--ml-border); border-left:4px solid var(--ml-accent);">
    <div style="font-size:0.75rem; font-weight:700; color:#64748b;">ВСЬОГО ЗАПИСІВ</div>
    <div id="p3-total" style="font-size:1.6rem; font-weight:800; color:#0f172a;">5 490 ЕМЗ</div>
  </div>
  <div style="background:white; border-radius:10px; padding:1.15rem; border:1px solid var(--ml-border); border-left:4px solid var(--ml-success);">
    <div style="font-size:0.75rem; font-weight:700; color:#059669;">ПРИЙНЯТО ДО ОПЛАТИ (ТАК)</div>
    <div id="p3-tak" style="font-size:1.6rem; font-weight:800; color:#15803d;">38 449 353 ₴</div>
    <div style="font-size:0.725rem; color:#059669;">✓ 355 ЕМЗ прямої оплати</div>
  </div>
  <div style="background:white; border-radius:10px; padding:1.15rem; border:1px solid var(--ml-border); border-left:4px solid #3b82f6;">
    <div style="font-size:0.75rem; font-weight:700; color:#1d4ed8;">ГЛОБАЛЬНИЙ БЮДЖЕТ (ГБ)</div>
    <div id="p3-gb" style="font-size:1.6rem; font-weight:800; color:#1e40af;">7 553 769 ₴</div>
    <div style="font-size:0.725rem; color:#2563eb;">🏢 4 421 ЕМЗ капітації</div>
  </div>
  <div style="background:white; border-radius:10px; padding:1.15rem; border:1px solid var(--ml-border); border-left:4px solid var(--ml-danger);">
    <div style="font-size:0.75rem; font-weight:700; color:#b91c1c;">ВТРАЧЕНО (СТАТУС «НІ»)</div>
    <div id="p3-lost" style="font-size:1.6rem; font-weight:800; color:#dc2626;">4 974 842 ₴</div>
    <div style="font-size:0.725rem; color:#dc2626;">⚠ 714 ЕМЗ з нульовим тарифом</div>
  </div>
  <div style="background:white; border-radius:10px; padding:1.15rem; border:1px solid var(--ml-border); border-left:4px solid var(--ml-warning);">
    <div style="font-size:0.75rem; font-weight:700; color:#b45309;">ПІДЛЯГАЄ ВІДНОВЛЕННЮ</div>
    <div id="p3-rec" style="font-size:1.6rem; font-weight:800; color:#b45309;">3 780 880 ₴</div>
  </div>
</div>

<div class="content-card">
  <div class="card-header">
    <div>
      <h2><span>📋</span> Реєстр ЕМЗ з автономно розрахованими тарифами (45 колонок)</h2>
      <p>Всі розрахунки виконано незалежним математичним модулем за формулами Кабміну</p>
    </div>
    <div style="display:flex; gap:10px;">
      <select id="p3-hosp" class="search-input" onchange="renderP3()">
        <option value="oco">КНП "Обласний центр онкології" (Вересень 2026)</option>
        <option value="dkl">КНП "ДКЛ Святої Зінаїди" СМР (Серпень 2026)</option>
      </select>
    </div>
  </div>

  <div class="table-responsive">
    <table class="ml-table">
      <thead>
        <tr>
          <th>#</th>
          <th>ID ЕМЗ (Кол. 4)</th>
          <th>Дата</th>
          <th>Лікар</th>
          <th>Пакет послуг</th>
          <th>Діагноз (МКХ-10)</th>
          <th>Розрахований тариф</th>
          <th>Статус НСЗУ (Кол. 38)</th>
          <th>Причина помилки (Кол. 39)</th>
          <th>Дія</th>
        </tr>
      </thead>
      <tbody id="p3-tbody"></tbody>
    </table>
  </div>
</div>
"""
js3 = """
function renderP3() {
  const k = document.getElementById('p3-hosp').value;
  const hosp = window.PROTOTYPE_DATA.hospitals[k];
  const tb = document.getElementById('p3-tbody');
  tb.innerHTML = '';

  if (k === 'oco') {
    document.getElementById('p3-total').textContent = '5 490 ЕМЗ';
    document.getElementById('p3-tak').textContent = '38 449 353 ₴';
    document.getElementById('p3-gb').textContent = '7 553 769 ₴';
    document.getElementById('p3-lost').textContent = '4 974 842 ₴';
    document.getElementById('p3-rec').textContent = '3 780 880 ₴';
  } else {
    document.getElementById('p3-total').textContent = '4 394 ЕМЗ';
    document.getElementById('p3-tak').textContent = '14 168 200 ₴';
    document.getElementById('p3-gb').textContent = '8 912 400 ₴';
    document.getElementById('p3-lost').textContent = '3 674 400 ₴';
    document.getElementById('p3-rec').textContent = '2 790 000 ₴';
  }

  (hosp.records || []).slice(0, 35).forEach((r, idx) => {
    const tr = document.createElement('tr');
    if (r.included === 'Ні') tr.className = 'row-rejected';
    let b = '<span class="badge badge-success">Так</span>';
    if (r.included === 'ГБ') b = '<span class="badge badge-info">ГБ</span>';
    if (r.included === 'Ні') b = '<span class="badge badge-danger">Ні</span>';
    let cost = r.included === 'Ні' ? '24 357.55 ₴' : '199.95 ₴';

    tr.innerHTML = `
      <td>${idx + 1}</td>
      <td><span class="code-tag">${r.emz_id.slice(0, 8)}...</span></td>
      <td>${r.date}</td>
      <td><strong>${r.doc_name}</strong><br><small style="color:#64748b;">${r.doc_pos}</small></td>
      <td><span class="badge badge-gray">${r.package ? r.package.slice(0, 16) : '—'}</span></td>
      <td><span class="code-tag">${r.diag_main ? r.diag_main.slice(0, 20) : '—'}</span></td>
      <td><strong style="color:${r.included === 'Ні' ? '#b91c1c' : '#15803d'}">${cost}</strong></td>
      <td>${b}</td>
      <td style="max-width:220px; font-size:0.75rem; color:${r.included === 'Ні' ? '#991b1b' : '#64748b'}">${r.error_comment || '—'}</td>
      <td>${r.included === 'Ні' ? `<a href="process_5_correction.html" class="btn btn-primary" style="padding:4px 8px; font-size:0.7rem;">⚡ Виправити</a>` : '—'}</td>
    `;
    tb.appendChild(tr);
  });
}
window.onload = renderP3;
"""

write_proto(
    "process_3_financial_audit.html",
    "Фінансовий аудит та автономний розрахунок тарифів",
    3,
    "Медичний директор / Заступник з економіки",
    "Постанова КМУ №1808 (Базові ставки 8 735 ₴ / 155 ₴)",
    "Автономний розрахунок повної вартості кожної взаємодії за 45 колонками звіту НСЗУ. Фіксація сум прямої оплати («Так»), глобального бюджету («ГБ») та недоотриманого доходу («Ні»).",
    "Повне відкриття фінансової картини нарахувань лікарні без очікування роз'яснень НСЗУ.",
    b3, js3
)

# ----------------- PROCESS 4 -----------------
b4 = """
<div class="content-card">
  <div class="card-header">
    <div>
      <h2><span>⚠️</span> Реєстр розбіжностей та втраченого доходу (Lost Revenue)</h2>
      <p>Записи зі статусом «Ні», співставлені з первинними ЕМЗ МІС Медлінк за ID ЕМЗ</p>
    </div>
  </div>

  <div class="table-responsive">
    <table class="ml-table">
      <thead>
        <tr>
          <th>ID ЕМЗ</th>
          <th>Пацієнт</th>
          <th>Лікар</th>
          <th>Діагноз / Послуга</th>
          <th>Причина відхилення НСЗУ (Кол. 39)</th>
          <th>Втрачений дохід</th>
          <th>Дія</th>
        </tr>
      </thead>
      <tbody id="p4-tbody"></tbody>
    </table>
  </div>
</div>
"""
js4 = """
function renderP4() {
  const tb = document.getElementById('p4-tbody');
  tb.innerHTML = '';
  const hosp = window.PROTOTYPE_DATA.hospitals.oco;
  const rej = (hosp.records || []).filter(r => r.included === 'Ні');

  rej.forEach(r => {
    const tr = document.createElement('tr');
    tr.className = 'row-rejected';
    tr.innerHTML = `
      <td><span class="code-tag">${r.emz_id.slice(0, 12)}...</span></td>
      <td>Пацієнт #${r.patient_id.slice(0, 8)}...<br><small style="color:#64748b;">Вік: ${r.age} р.</small></td>
      <td><strong>${r.doc_name}</strong><br><small style="color:#64748b;">${r.doc_pos}</small></td>
      <td><span class="code-tag">${r.diag_main ? r.diag_main.slice(0, 22) : '—'}</span></td>
      <td style="max-width:280px; font-size:0.775rem; color:#7f1d1d; font-weight:600;">${r.error_comment || 'Не відповідає жодному пакету/послузі'}</td>
      <td><strong style="color:#dc2626; font-size:0.95rem;">-24 357.55 ₴</strong></td>
      <td><a href="process_5_correction.html" class="btn btn-primary" style="padding:6px 12px; font-size:0.75rem;">⚡ Відкрити в Медлінку</a></td>
    `;
    tb.appendChild(tr);
  });
}
window.onload = renderP4;
"""

write_proto(
    "process_4_discrepancies.html",
    "Журнал розбіжностей та 2-Way звірка за ID ЕМЗ",
    4,
    "Завідувачі відділень / Експерти з кодування",
    "Лист «Опис помилок» НСЗУ (186 правил перевірки)",
    "Автоматичне співставлення відхилених записів НСЗУ з базою МІС Медлінк за полем Encounter.EhealthId. Локалізація відділень та розрахунок точного збитку.",
    "Виявлення та підготовка до відновлення від 3.6 до 6.1 млн грн у кожному звіті.",
    b4, js4
)

# ----------------- PROCESS 5 -----------------
b5 = """
<div class="content-card" style="max-width:960px; margin:0 auto;">
  <div class="card-header">
    <div>
      <h2><span>⚡</span> Асистент 2-Way коригування взаємодії — ЕМЗ #b967f3de-67e8-49a3...</h2>
      <p>Зв'язок за Encounter.EhealthId: пацієнт Іванов І.І., лікар Зенін В.А.</p>
    </div>
    <span class="badge badge-danger">Відхилено НСЗУ</span>
  </div>

  <div style="background:#fef2f2; border:1px solid #fecaca; border-radius:8px; padding:12px; margin-bottom:15px;">
    <h4 style="color:#b91c1c; font-size:0.875rem; margin-bottom:4px;">❌ Помилка НСЗУ: Не відповідає жодному пакету/послузі</h4>
    <p style="font-size:0.8rem; color:#7f1d1d;">Офіційне визначення: відсутня обов'язкова хірургічна інтервенція АКПІ для основного діагнозу C18.0. Тариф обнулено.</p>
  </div>

  <div style="background:#eff6ff; border:1px solid #bfdbfe; border-left:4px solid var(--ml-accent); padding:12px; border-radius:8px; margin-bottom:15px; font-size:0.825rem; color:#1e3a8a;">
    <h4>💡 Підказка асистента Медлінка</h4>
    <p>Для онкологічного діагнозу <strong>C18.0</strong> додайте послугу АКПІ <code>30061-02</code> (резекція правої половини ободової кишки) для віднесення до ДСГ <strong>G01</strong>. Очікувана виплата зросте з 0 ₴ до <strong>24 357.55 ₴</strong>.</p>
  </div>

  <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:15px;">
    <div>
      <label style="font-size:0.75rem; color:#64748b; font-weight:700;">Основний діагноз (МКХ-10):</label>
      <input type="text" class="search-input" style="width:100%; font-weight:600;" value="C18.0 Злоякісне новоутворення сліпої кишки">
    </div>
    <div>
      <label style="font-size:0.75rem; color:#64748b; font-weight:700;">Послуга АКПІ:</label>
      <input type="text" class="search-input" style="width:100%; font-weight:600;" value="30061-02 Резекція правої половини ободової кишки">
    </div>
  </div>

  <div style="padding:15px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px; display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
    <div>
      <span style="font-size:0.8rem; color:#166534; font-weight:600;">Відновлена сума:</span>
      <div style="font-size:1.6rem; font-weight:800; color:#15803d;">+24 357.55 ₴</div>
    </div>
    <span class="badge badge-success">ДСГ G01 буде зараховано</span>
  </div>

  <div style="display:flex; justify-content:flex-end; gap:10px;">
    <a href="process_4_discrepancies.html" class="btn btn-outline">Скасувати</a>
    <button class="btn btn-success" onclick="alert('✅ Взаємодію виправлено у МІС Медлінк!\\nЗапис переведено в чергу повторного підписання КЕП.'); window.location.href='process_4_discrepancies.html';">
      💾 Застосувати виправлення та оновити в Медлінку
    </button>
  </div>
</div>
"""

write_proto(
    "process_5_correction.html",
    "Асистент виправлення кодування та ресинхронізація",
    5,
    "Лікар (автор запису) / Медичний координатор",
    "Таблиці ОДК НСЗУ, специфікації пакетів 2026",
    "Інтерактивний підбір виправлення на основі рекомендацій алгоритму, коригування запису в МІС в 1 клік та постановка в чергу повторної відправки з КЕП.",
    "Миттєве повернення від 10 500 до 54 089 грн за кожен виправлений випадок.",
    b5, ""
)

# ----------------- PROCESS 6 -----------------
b6 = """
<div class="content-card">
  <div class="card-header">
    <div>
      <h2><span>📖</span> Пошуковий довідник нормативів, ДСГ та тарифів ПМГ-2026</h2>
      <p>465 ДСГ стаціонару, 148 амбулаторних класів, 80 правил реабілітації</p>
    </div>
  </div>

  <div style="display:flex; gap:12px; margin-bottom:15px;">
    <input type="text" id="cat-search" class="search-input" style="flex:1;" placeholder="🔍 Пошук за назвою або кодом (напр. резекція, G01, C18, 30061)..." oninput="filterCat()">
    <select id="cat-pkg" class="search-input" style="min-width:240px;" onchange="filterCat()">
      <option value="4" selected>Пакет 4: Хірургічний стаціонар (190 ДСГ)</option>
      <option value="3">Пакет 3: Терапевтичний стаціонар (201 ДСГ)</option>
      <option value="47">Пакет 47: Хірургія 1 дня (74 ДСГ)</option>
      <option value="9">Пакет 9: Амбулаторні класи (148 класів)</option>
      <option value="54">Пакет 54: Реабілітація (АР1–АР4)</option>
    </select>
  </div>

  <div class="table-responsive">
    <table class="ml-table">
      <thead>
        <tr>
          <th>Код</th>
          <th>Найменування ДСГ / Класу</th>
          <th>Коефіцієнт</th>
          <th>Базова ставка</th>
          <th>Розрахункова вартість</th>
          <th>Діагнозів</th>
          <th>Послуг</th>
          <th>Вимоги</th>
        </tr>
      </thead>
      <tbody id="cat-tbody"></tbody>
    </table>
  </div>
</div>
"""
js6 = """
function filterCat() {
  const pkg = document.getElementById('cat-pkg').value;
  const term = (document.getElementById('cat-search').value || '').toLowerCase();
  const tb = document.getElementById('cat-tbody');
  tb.innerHTML = '';

  if (pkg === '3' || pkg === '4' || pkg === '47') {
    const dsgs = (window.PROTOTYPE_DATA.dsgs || []).filter(d => String(d.package_id) === pkg);
    dsgs.filter(d => !term || d.drg_name.toLowerCase().includes(term)).slice(0, 40).forEach(d => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><span class="code-tag">${d.drg_name.slice(0, 5)}</span></td>
        <td><strong>${d.drg_name}</strong></td>
        <td>${d.coefficient}</td>
        <td>8 735.00 ₴</td>
        <td><strong style="color:#15803d;">${(8735.0 * (d.coeff_numeric || 1) * 0.55).toFixed(2)} ₴</strong></td>
        <td><span class="badge badge-gray">${d.diag_count}</span></td>
        <td><span class="badge badge-gray">${d.svc_count}</span></td>
        <td><small style="color:#64748b;">${d.additional_requirements || 'Стандарт'}</small></td>
      `;
      tb.appendChild(tr);
    });
  } else if (pkg === '9') {
    (window.PROTOTYPE_DATA.pkg9_classes || []).forEach(c => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><span class="code-tag">Клас ${c.class_number}</span></td>
        <td><strong>${c.class_name}</strong></td>
        <td>${c.coefficient}</td>
        <td>155.00 ₴</td>
        <td><strong style="color:#15803d;">${c.cost.toFixed(2)} ₴</strong></td>
        <td><span class="badge badge-gray">${c.diag_count}</span></td>
        <td><span class="badge badge-gray">${c.svc_count}</span></td>
        <td><small style="color:#64748b;">Вимога до посади</small></td>
      `;
      tb.appendChild(tr);
    });
  }
}
window.onload = filterCat;
"""

write_proto(
    "process_6_catalog.html",
    "Довідник нормативів та тарифів ПМГ-2026",
    6,
    "Лікарі / Економісти / Начмеди",
    "Постанова КМУ №1808, Додатки 1 та 2, Наказ №377",
    "Електронний пошуковий каталог 465 австралійських ДСГ, 148 амбулаторних класів та матриць реабілітації. Перевірка вимог до посад та умов включення.",
    "Єдина верифікована нормативна база для всього закладу.",
    b6, js6
)

print("All 6 dedicated process pages built successfully!")
