import re

def update_tz():
    file_path = r'c:\__MEDLINK___\PMG\TZ_MedLink_PMG_Analytics.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update quick-proto-nav
    nav_old = """  <!-- Interactive Prototypes Quick Bar -->
  <div class="quick-proto-nav">
    <strong>🌐 Прототипи ПМГ-2026:</strong>
    <a href="prototype/index.html" class="main-link" target="_blank">Головний портал (Всі процеси) ↗</a>
    <a href="prototype/process_1_prebilling.html" target="_blank">П1: Пре-білінг лікаря ↗</a>
    <a href="prototype/process_2_upload.html" target="_blank">П2: Імпорт звіту НСЗУ ↗</a>
    <a href="prototype/process_3_financial_audit.html" target="_blank">П3: Фінансовий аудит ↗</a>
    <a href="prototype/process_4_discrepancies.html" target="_blank">П4: Журнал розбіжностей ↗</a>
    <a href="prototype/process_5_correction.html" target="_blank">П5: Асистент виправлення ↗</a>
    <a href="prototype/process_6_catalog.html" target="_blank">П6: Довідник нормативів ↗</a>
  </div>"""

    nav_new = """  <!-- Interactive Prototypes Quick Bar -->
  <div class="quick-proto-nav">
    <strong>🌐 Прототипи та Документація ПМГ-2026:</strong>
    <a href="prototype_medlink/index.html" class="main-link" target="_blank">MedLink Quasar Прототип (Всі 7 кроків + 46 пакетів) ↗</a>
    <a href="docs_html/index.html" target="_blank" style="background: #2563eb;">📚 Технічна документація (9 розділів) ↗</a>
    <a href="normative_packages/index.html" target="_blank" style="background: #059669;">⚖️ Всі 46 пакетів ПМГ (12 досьє) ↗</a>
    <a href="prototype/index.html" target="_blank">HTML Прототип ↗</a>
    <a href="prototype/process_1_prebilling.html" target="_blank">П1: Пре-білінг ↗</a>
    <a href="prototype/process_2_upload.html" target="_blank">П2: Імпорт ↗</a>
    <a href="prototype/process_3_financial_audit.html" target="_blank">П3: Аудит ↗</a>
    <a href="prototype/process_4_discrepancies.html" target="_blank">П4: Розбіжності ↗</a>
    <a href="prototype/process_5_correction.html" target="_blank">П5: Виправлення ↗</a>
    <a href="prototype/process_6_catalog.html" target="_blank">П6: Довідники ↗</a>
  </div>"""

    if nav_old in html:
        html = html.replace(nav_old, nav_new, 1)
        print("1. Updated quick-proto-nav in TZ.")

    # 2. Add subsection 2.4 in Section 2
    sec2_end = """        <li><strong>Пакети 53 та 54 (Реабілітаційна допомога)</strong>: Стаціонарна = 19 776.00 грн за цикл; Амбулаторна = 10 820.00 грн за цикл за умови виконання вимог матриць <strong>АР1..АР4</strong> та <strong>CR</strong>.</li>
      </ul>
    </section>"""

    sec2_addition = """        <li><strong>Пакети 53 та 54 (Реабілітаційна допомога)</strong>: Стаціонарна = 19 776.00 грн за цикл; Амбулаторна = 10 820.00 грн за цикл за умови виконання вимог матриць <strong>АР1..АР4</strong> та <strong>CR</strong>.</li>
      </ul>

      <h3 class="sub-title">2.4. Повний реєстр 46 пакетів ПМГ-2026 та 12 клініко-економічних кластерів</h3>
      <p>
        На вимогу повної відповідності нормативній базі у системі імплементовано регулювання <strong>всіх 46 офіційних пакетів медичних гарантій 2026 року</strong>, згрупованих у 12 кластерів:
      </p>
      <div style="background: #f8fafc; border: 1px solid var(--ml-border); border-radius: 8px; padding: 14px; margin-bottom: 14px; font-size: 0.875rem;">
        <ul style="margin-bottom: 0;">
          <li><strong>Кластер 1. Первинна медична допомога:</strong> Пакет 1 (ПМД, 1 007.30 ₴/рік, капітація).</li>
          <li><strong>Кластер 2. Екстрена медична допомога:</strong> Пакет 2 (ЕМД, 340.50 ₴/рік, капітація).</li>
          <li><strong>Кластер 3. Спеціалізована та хірургічна допомога (ДСГ):</strong> Пакети 3 (Терапія), 4 (Хірургія), 47 (Хірургія 1-дня) — база 8 735.00 ₴, 465 ДСГ, коригувальні 0.55 / 0.60.</li>
          <li><strong>Кластер 4. Пріоритетні стаціонарні пакети:</strong> Пакети 5 (Інсульт, 15 250..137 000 ₴), 6 (Інфаркт, 44 400..55 200 ₴), 7 (Пологи, 15 137..27 240 ₴), 8 (Неонатологія, 33 000..135 000 ₴), 35 (Ведення вагітності, 800 ₴/міс).</li>
          <li><strong>Кластер 5. Амбулаторна допомога та онкоскринінги:</strong> Пакет 9 (148 класів, база 155 ₴), Пакети 10..15 (Мамографія, гістеро-, езофагогастро-, колоно-, цисто-, бронхоскопія: 512..1 180 ₴), Пакет 16 (Лікування безпліддя), Пакет 34 (Стоматологія, 145 ₴), Пакет 42 (Мобільна амбулаторія).</li>
          <li><strong>Кластер 6. Онкологія та онкогематологія:</strong> Пакет 18 (Хіміотерапія, 17 865..35 730 ₴), Пакет 19 (Радіотерапія, 54 089..131 499 ₴), Пакет 26 (Онкогематологія, 61 200..122 400 ₴).</li>
          <li><strong>Кластер 7. Реабілітаційна допомога:</strong> Пакет 25 (Стаціонарна, 19 776..33 619 ₴), Пакет 53 (Монопрофільна складна, 41 500 ₴), Пакет 54 (Амбулаторна, 10 820 ₴).</li>
          <li><strong>Кластер 8. Паліативна допомога:</strong> Пакет 23 (Стаціонарна, 18 900 ₴), Пакет 24 (Мобільна, 14 200 ₴).</li>
          <li><strong>Кластер 9. Психіатрія та терапія залежностей:</strong> Пакет 22 (Стаціонарна психіатрія, 13 151 ₴), Пакет 27 (Мобільна психіатрія, 10 535 ₴), Пакет 28 (ЗПТ), Пакет 30 (Первинка психіатрія, 183 ₴).</li>
          <li><strong>Кластер 10. Інфекційні патології:</strong> Пакет 20 (Туберкульоз, 43 780 ₴), Пакет 21 (ВІЛ/СНІД, 2 100 ₴), Пакет 29 (Вірусні гепатити).</li>
          <li><strong>Кластер 11. Високі технології та трансплантація:</strong> Пакет 43 (Гемодіаліз, 2 460 ₴/сеанс), Пакет 46 (Перитонеальний діаліз, 1 820 ₴/доба), Пакет 59 (ДРТ / ЕКЗ, 60 324 ₴), Пакет 60 (Трансплантація органів, 350 000..900 000 ₴), Пакет 61 (ТКМ / ГСК, 750 000..1 400 000 ₴).</li>
          <li><strong>Кластер 12. Оборонна готовність, ВЛК та ветерани:</strong> Пакет 40 (Готовність ЗОЗ до криз, глобальна ставка), Пакет 41 (НС), Пакет 44 (Медичний огляд ВЛК, 883 ₴), Пакет 45 (Лікування військовослужбовців), Пакет 58 (Зубопротезування ветеранів, 14 984 ₴).</li>
        </ul>
      </div>
      <p>
        Деталізовані нормативні досьє, законодавчі акти та таблиці валідацій див. у 
        <a href="docs_html/09_all_pmg_packages_normative_guide.html" target="_blank" style="color: var(--ml-accent); font-weight: 700;">Розділі 9 технічної документації ↗</a>
        та автономному браузері <a href="normative_packages/index.html" target="_blank" style="color: var(--ml-accent); font-weight: 700;">normative_packages/index.html ↗</a>.
      </p>
    </section>"""

    if sec2_end in html:
        html = html.replace(sec2_end, sec2_addition, 1)
        print("2. Added section 2.4 in TZ.")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("TZ_MedLink_PMG_Analytics.html updated successfully!")

if __name__ == '__main__':
    update_tz()
