HTML_PATH = r"c:\__MEDLINK___\PMG\prototype_medlink\index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    content = f.read()

target = "dataStore: d,"
replacement = """dataStore: d,
          apiBase: '/api/v1',
          apiLoading: false,
          reconcileFilter: 'all',
          reconcileRowsData: [
            { id: 'rec-1', statusClass: 'bg-red-1', badgeColor: 'negative', statusLabel: '🔴 MISSING_IN_NHSU', ehealth_id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', patient: 'Іваненко В. М. (2981412345)', doctor: 'Коваленко О. С. • Хірургічне №1', pkg: '3', icd: 'C18.0', service: '32003-00 Резекція кишки', amount: 36900.00, reason: 'Прихована дефектура: запис є в МІС, але НСЗУ проігнорувала його у звіті (0 ₴)' },
            { id: 'rec-2', statusClass: 'bg-red-1', badgeColor: 'negative', statusLabel: '🔴 MISSING_IN_NHSU', ehealth_id: 'b2c3d4e5-f6a7-8901-bcde-f12345678901', patient: 'Петренко О. С. (3124509876)', doctor: 'Коваленко О. С. • Хірургічне №1', pkg: '3', icd: 'C16.2', service: '30518-00 Гастректомія', amount: 31200.00, reason: 'Прихована дефектура: випадок зник у шлюзі eHealth' },
            { id: 'rec-3', statusClass: 'bg-red-1', badgeColor: 'negative', statusLabel: '🔴 MISSING_IN_NHSU', ehealth_id: 'c3d4e5f6-a7b8-9012-cdef-123456789012', patient: 'Сидоренко М. П. (2876543210)', doctor: 'Мельник Т. В. • Хіміотерапія', pkg: '4', icd: 'C50.9', service: '96199-00 Хіміотерапія', amount: 22800.00, reason: 'Прихована дефектура: не підтверджено центральним компонентом' },
            { id: 'rec-4', statusClass: 'bg-red-1', badgeColor: 'negative', statusLabel: '🔴 MISSING_IN_NHSU', ehealth_id: 'd4e5f6a7-b8c9-0123-def1-234567890123', patient: 'Лисенко Г. Д. (3298714563)', doctor: 'Шевченко В. І. • Радіологія', pkg: '4', icd: 'C61', service: '15269-00 Променева терапія', amount: 28600.00, reason: 'Прихована дефектура: технічний збій синхронізації' },
            { id: 'rec-5', statusClass: 'bg-red-1', badgeColor: 'negative', statusLabel: '🔴 MISSING_IN_NHSU', ehealth_id: 'e5f6a7b8-c9d0-1234-ef12-345678901234', patient: 'Ткаченко А. В. (3012456789)', doctor: 'Кравченко Ю. М. • Хірургія одного дня', pkg: '47', icd: 'C43.5', service: '30071-00 Висічення меланоми', amount: 65000.00, reason: 'Прихована дефектура: помилка тарифікації шлюзу' },
            { id: 'rec-6', statusClass: 'bg-amber-1', badgeColor: 'warning', statusLabel: '🟡 DISCREPANCY', ehealth_id: 'f6a7b8c9-d0e1-2345-f123-456789012345', patient: 'Мороз Н. О. (2954316782)', doctor: 'Бондаренко І. П. • Терапія', pkg: '3', icd: 'C18.0', service: '32003-00 Резекція', amount: 13285.94, reason: 'ERR_DOC_SPEC_04: Спеціальність терапевта не відповідає хірургії' },
            { id: 'rec-7', statusClass: 'bg-amber-1', badgeColor: 'warning', statusLabel: '🟡 DISCREPANCY', ehealth_id: 'a7b8c9d0-e1f2-3456-1234-567890123456', patient: 'Кузьменко С. В. (3187654321)', doctor: 'Мельник Т. В. • Хіміотерапія', pkg: '4', icd: 'C50.9', service: '96199-00 Введення', amount: 7600.00, reason: 'ERR_MVTN_01: Перетин періодів перебування з іншим стаціонаром' },
            { id: 'rec-8', statusClass: '', badgeColor: 'positive', statusLabel: '🟢 MATCHED_PAID', ehealth_id: 'b8c9d0e1-f2a3-4567-2345-678901234567', patient: 'Григоренко Л. І. (2765432198)', doctor: 'Коваленко О. С. • Хірургічне №1', pkg: '3', icd: 'C18.0', service: '32003-00 Резекція', amount: 10630.84, reason: '✓ Повністю збіглося та підтверджено НСЗУ' }
          ],"""

if target in content:
    content = content.replace(target, replacement)
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("Reconcile rows successfully added to data()!")
else:
    print("Error: target not found.")
