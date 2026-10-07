HTML_PATH = r"c:\__MEDLINK___\PMG\prototype_medlink\index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Check bottom of upload view
upload_end = text.find("<!-- ================= VIEW 2: NHSU FILE UPLOAD")
print("Upload view starts at:", upload_end)

# Let's see the transition bars we can add
bar_upload = """
            <!-- Bottom Workflow Transition Bar -->
            <div class="row justify-between items-center q-mt-md q-pa-md bg-white rounded-borders shadow-1">
              <div class="text-caption text-grey-7">
                Крок 1: Звіт НСЗУ (.xlsx) завантажено та розібрано на 4 аркуші за допомогою SAX OpenXML.
              </div>
              <q-btn color="primary" icon-right="arrow_forward" label="Крок 2: Перейти до Аудиту 45 колонок ➡" @click="currentView = 'audit'" />
            </div>
"""

bar_audit = """
            <!-- Bottom Workflow Transition Bar -->
            <div class="row justify-between items-center q-mt-md q-pa-md bg-white rounded-borders shadow-1">
              <q-btn outline color="grey-8" icon="arrow_back" label="⬅ Крок 1: Імпорт OpenXML" @click="currentView = 'upload'" />
              <div class="text-caption text-grey-7">
                Крок 2: 45 колонок проаналізовано, тарифи Постанови №1808 розраховано. Перейдіть до 2-Way звірки.
              </div>
              <q-btn color="primary" icon-right="arrow_forward" label="Крок 3: Запустити 2-Way звірку з МІС ➡" @click="currentView = 'reconciliation'" />
            </div>
"""

bar_discrepancies = """
            <!-- Bottom Workflow Transition Bar -->
            <div class="row justify-between items-center q-mt-md q-pa-md bg-white rounded-borders shadow-1">
              <q-btn outline color="grey-8" icon="arrow_back" label="⬅ Крок 3: 2-Way Звірка" @click="currentView = 'reconciliation'" />
              <div class="text-caption text-grey-7">
                Крок 4: Помилки дефектури розшифровано за базою знань 186 правил НСЗУ та виправлено.
              </div>
              <q-btn color="primary" icon-right="arrow_forward" label="Крок 5: Зведений звіт по лікарях («Звіт») ➡" @click="currentView = 'doctors'" />
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
"""

# Let's insert bar_audit before the closing div of view audit
audit_closing = '<!-- ================= VIEW 2: NHSU FILE UPLOAD'
if audit_closing in text and "Крок 3: Запустити 2-Way звірку" not in text:
    text = text.replace(audit_closing, bar_audit + "\n          </div>\n\n          " + audit_closing)
    print("Added bar_audit!")

# Insert bar_upload before the closing div of upload view
upload_closing = '<!-- ================= VIEW 3: DEDICATED 2-WAY'
if upload_closing in text and "Крок 2: Перейти до Аудиту 45 колонок" not in text:
    text = text.replace(upload_closing, bar_upload + "\n          </div>\n\n          " + upload_closing)
    print("Added bar_upload!")

# Insert bar_discrepancies before the closing div of discrepancies view
discr_closing = '<!-- ================= VIEW 4: DOCTORS SUMMARY REPORT'
if discr_closing in text and "Крок 5: Зведений звіт по лікарях" not in text:
    text = text.replace(discr_closing, bar_discrepancies + "\n          </div>\n\n          " + discr_closing)
    print("Added bar_discrepancies!")

# Insert bar_doctors before encounter view
doctors_closing = '<!-- ================= VIEW 5: DOCTOR ARM / PRE-BILLING'
if doctors_closing in text and "Крок 6: Перейти до АРМ Лікаря" not in text:
    text = text.replace(doctors_closing, bar_doctors + "\n          </div>\n\n          " + doctors_closing)
    print("Added bar_doctors!")

# Insert bar_encounter before catalog view
encounter_closing = '<!-- ================= VIEW 6: CLASSIFIERS CATALOG'
if encounter_closing in text and "Крок 7: Переглянути довідники ПМГ" not in text:
    text = text.replace(encounter_closing, bar_encounter + "\n          </div>\n\n          " + encounter_closing)
    print("Added bar_encounter!")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("Transition bars added successfully!")
