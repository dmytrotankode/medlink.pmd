HTML_PATH = r"c:\__MEDLINK___\PMG\prototype_medlink\index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    text = f.read()

bar_audit = """
            <!-- Bottom Workflow Transition Bar -->
            <div class="row justify-between items-center q-mt-md q-pa-md bg-white rounded-borders shadow-1">
              <q-btn outline color="grey-8" icon="arrow_back" label="⬅ Крок 1: Імпорт OpenXML" @click="currentView = 'upload'" />
              <div class="text-caption text-grey-7">
                Крок 2: 45 колонок проаналізовано, тарифи Постанови №1808 розраховано. Перейдіть до 2-Way звірки.
              </div>
              <q-btn color="primary" icon-right="arrow_forward" label="Крок 3: Запустити 2-Way звірку з МІС ➡" @click="currentView = 'reconciliation'" />
            </div>
          </div>
"""

bar_doctors = """
            <!-- Bottom Workflow Transition Bar -->
            <div class="row justify-between items-center q-mt-md q-pa-md bg-white rounded-borders shadow-1">
              <q-btn outline color="grey-8" icon="arrow_back" label="⬅ Крок 4: Журнал дефектури" @click="currentView = 'discrepancies'" />
              <div class="text-caption text-grey-7">
                Крок 5: Зведений аркуш «Звіт» сформовано з урахуванням обмеження 1 ургентного випадку Пакета 9 на пацієнта.
              </div>
              <q-btn color="primary" icon-right="arrow_forward" label="Крок 6: Перейти до АРМ Лікаря (Пре-білінг) ➡" @click="currentView = 'encounter'" />
            </div>
          </div>
"""

bar_encounter = """
            <!-- Bottom Workflow Transition Bar -->
            <div class="row justify-between items-center q-mt-md q-pa-md bg-white rounded-borders shadow-1">
              <q-btn outline color="grey-8" icon="arrow_back" label="⬅ Крок 5: Звіт керівництва" @click="currentView = 'doctors'" />
              <div class="text-caption text-grey-7">
                Крок 6: Пре-білінг та валідація спеціальності лікаря (MedProfit Anti-Defektura) виконані перед підписом КЕП.
              </div>
              <q-btn color="primary" icon-right="arrow_forward" label="Крок 7: Переглянути довідники ПМГ ➡" @click="currentView = 'catalog-dsg'" />
            </div>
          </div>
"""

# 1. Audit transition bar
anchor_v2 = '<!-- ================= VIEW 2: OPENXML INGESTION SIMULATOR ================= -->'
if anchor_v2 in text and "Крок 3: Запустити 2-Way звірку з МІС" not in text:
    text = text.replace(anchor_v2, bar_audit + "\n\n          " + anchor_v2)
    print("Added bar_audit!")

# 2. Doctors transition bar
anchor_v5 = '<!-- ================= VIEW 5: ENCOUNTER PRE-BILLING SIMULATOR ================= -->'
if anchor_v5 in text and "Крок 6: Перейти до АРМ Лікаря" not in text:
    text = text.replace(anchor_v5, bar_doctors + "\n\n          " + anchor_v5)
    print("Added bar_doctors!")

# 3. Encounter transition bar
anchor_v6 = '<!-- ================= VIEW 6: CLASSIFIERS & DICTIONARIES ================= -->'
if anchor_v6 in text and "Крок 7: Переглянути довідники ПМГ" not in text:
    text = text.replace(anchor_v6, bar_encounter + "\n\n          " + anchor_v6)
    print("Added bar_encounter!")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved all missing bars!")
