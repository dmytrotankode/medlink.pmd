HTML_PATH = r"c:\__MEDLINK___\PMG\prototype_medlink\index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Let's inspect where currentView === 'encounter' starts and ends
start_tag = '<!-- ================= VIEW 5: ENCOUNTER PRE-BILLING SIMULATOR ================= -->'
end_tag = '<!-- Bottom Workflow Transition Bar -->'

idx_start = text.find(start_tag)
idx_v6 = text.find('<!-- ================= VIEW 6: CLASSIFIERS & DICTIONARIES ================= -->')

print("idx_start:", idx_start, "idx_v6:", idx_v6)

# New Encounter View mimicking Details.vue
new_encounter_view = """<!-- ================= VIEW 5: ENCOUNTER PRE-BILLING SIMULATOR (Details.vue Augmentation) ================= -->
          <div v-else-if="currentView === 'encounter'">
            <!-- Augmentation Banner for Developer & Analyst -->
            <q-banner dense class="bg-purple-1 text-purple-10 q-mb-md rounded-borders" style="border: 1px solid #d8b4fe; border-left: 5px solid #9333ea;">
              <template v-slot:avatar>
                <q-icon name="extension" color="purple"></q-icon>
              </template>
              <div class="row justify-between items-center">
                <div class="text-body2">
                  <strong>Адитивне доповнення існуючої форми:</strong> Нижче відтворено реальну форму МІС <code>Details.vue</code> (<code>pages/medicalEvents/encounter/subpages/Details.vue</code>).
                  Пре-білінг та Anti-Defektura валідація спеціальності вбудовані поруч із існуючою кнопкою <code>createWithSign</code> (Підписати КЕП),
                  не змінюючи наявну логіку та не порушуючи роботу лікаря.
                </div>
                <q-btn color="purple" icon="code" label="Переглянути diff для Details.vue" dense unelevated @click="detailsDiffModal = true" class="q-ml-md" />
              </div>
            </q-banner>

            <!-- REAL MEDLINK PATIENT HEADER (Details.vue line 5-12) -->
            <div class="row justify-between items-center q-pa-sm bg-grey-1 rounded-borders q-mb-sm" style="border: 1px solid #e2e8f0;">
              <div class="row items-center q-gutter-md">
                <q-avatar icon="person" color="primary" text-color="white" size="36px" />
                <div>
                  <div class="text-weight-bold text-subtitle2">Іваненко Василь Миколайович</div>
                  <div class="text-caption text-grey-7">РНОКПП: 2981412345 • Вік: 58 р. • Стать: Чоловіча • ID ЕМЗ: 41a08c45-9ac3-452c-99a1-b6b1f86339b4</div>
                </div>
              </div>
              <div class="row q-gutter-xs">
                <q-btn-dropdown outline color="primary" icon="add" label="Створити рецепт" dense no-caps>
                  <q-list dense><q-item clickable v-close-popup><q-item-section>Лікарський засіб</q-item-section></q-item></q-list>
                </q-btn-dropdown>
                <q-btn-dropdown outline color="primary" icon="add" label="Створити Е-запит" dense no-caps>
                  <q-list dense><q-item clickable v-close-popup><q-item-section>Медичний виріб</q-item-section></q-item><q-item clickable v-close-popup><q-item-section>ДЗР</q-item-section></q-item></q-list>
                </q-btn-dropdown>
                <q-btn-dropdown outline color="primary" label="Додати документ" dense no-caps>
                  <q-list dense>
                    <q-item clickable v-close-popup><q-item-section>Направлення</q-item-section></q-item>
                    <q-item clickable v-close-popup><q-item-section>Діагностичний звіт</q-item-section></q-item>
                    <q-item clickable v-close-popup><q-item-section>Процедуру</q-item-section></q-item>
                    <q-item clickable v-close-popup><q-item-section>План лікування</q-item-section></q-item>
                  </q-list>
                </q-btn-dropdown>
              </div>
            </div>

            <!-- REAL MEDLINK ACTION BAR (Details.vue line 148-220) -->
            <div class="row justify-between items-center q-pa-sm bg-white rounded-borders q-mb-sm shadow-1">
              <div class="row q-gutter-xs items-center">
                <!-- Existing Sign button: reacts to prebilling validation -->
                <q-btn
                  icon="fas fa-signature"
                  :color="(simResult.warning && simResult.warning.severity === 'CRITICAL') ? 'grey-6' : 'primary'"
                  :disable="simResult.warning && simResult.warning.severity === 'CRITICAL'"
                  label="Підписати КЕП"
                  @click="onSignEncounter"
                >
                  <q-tooltip v-if="simResult.warning && simResult.warning.severity === 'CRITICAL'">
                    КЕП заблоковано: Виявлено критичну дефектуру посади лікаря!
                  </q-tooltip>
                </q-btn>

                <!-- Existing DSG button in Details.vue (line 214) -->
                <q-btn color="primary" outline label="Зберегти та перевірити ДСГ" @click="calcSimulation" />
                <q-btn outline color="grey-8" label="Шаблон взаємодії" />
                <q-btn outline color="grey-7" label="Позначити як помилкову" />
              </div>

              <div class="row items-center q-gutter-sm text-caption">
                <span class="text-grey-7">Статус eHealth:</span>
                <q-badge color="warning">ЧЕРНЕТКА (DRAFT)</q-badge>
              </div>
            </div>

            <!-- REAL MEDLINK TABS (Details.vue line 255-268) -->
            <q-card class="q-mb-sm">
              <q-tabs dense v-model="selectedEncounterTab" class="bg-grey-2 text-grey-8" active-color="primary" indicator-color="primary" align="left">
                <q-tab name="encounter-edit" label="Взаємодія" icon="edit" />
                <q-tab name="episodes" label="Епізоди" icon="folder_open" />
                <q-tab name="diagnoses" label="Діагнози (МКХ-10)" icon="local_hospital" />
                <q-tab name="anamnesis" label="Анамнез" icon="history" />
                <q-tab name="pmg-prebilling" label="⭐ ПМГ-2026 Пре-білінг (Адитивний віджет)" icon="calculate" class="text-weight-bold text-accent" />
              </q-tabs>
            </q-card>

            <!-- CARD BODY: PRE-BILLING & ANTI-DEFEKTURA WIDGET -->
            <div class="page-card">
              <!-- Live Warning if Position Mismatch -->
              <q-banner v-if="simResult.warning" dense class="bg-red-1 text-negative q-mb-md rounded-borders" style="border: 2px solid #ef4444;">
                <template v-slot:avatar><q-icon name="report_problem" color="negative" size="32px"></q-icon></template>
                <div class="text-subtitle2 text-weight-bold">⛔ УВАГА! Ризик дефектури НСЗУ (Оплата 0 ₴): {{ simResult.warning.code }}</div>
                <div class="text-body2">{{ simResult.warning.message }}</div>
                <div class="text-caption text-weight-bold q-mt-xs">Норматив: {{ simResult.warning.legalBasis }} • Рекомендація: {{ simResult.warning.advice }}</div>
              </q-banner>

              <div class="row q-col-gutter-lg">
                <!-- Left Input Form -->
                <div class="col-xs-12 col-md-6">
                  <q-card flat bordered class="q-pa-md">
                    <div class="text-subtitle1 text-weight-bold text-grey-9 q-mb-sm">Параметри медичного запису</div>
                    
                    <div class="q-mb-sm">
                      <div class="text-caption text-grey-7 q-mb-xs">Посада та спеціальність лікаря (Перевірка MedProfit):</div>
                      <q-select
                        dense
                        outlined
                        v-model="simDoctorPos"
                        :options="doctorPositionOptions"
                        emit-value
                        map-options
                        @input="calcSimulation"
                      >
                        <template v-slot:prepend><q-icon name="badge" color="primary"></q-icon></template>
                      </q-select>
                    </div>

                    <div class="q-mb-sm">
                      <div class="text-caption text-grey-7 q-mb-xs">Пакет медичних послуг:</div>
                      <q-select
                        dense
                        outlined
                        v-model="simPackage"
                        :options="simPackageOptions"
                        @input="calcSimulation"
                      ></q-select>
                    </div>

                    <div class="q-mb-sm">
                      <div class="text-caption text-grey-7 q-mb-xs">Основний діагноз (підтримує введення без крапок, напр. C180):</div>
                      <q-input
                        dense
                        outlined
                        v-model="simDiag"
                        placeholder="Введіть код МКХ-10 (C180, F700, K358...)"
                        @input="calcSimulation"
                      >
                        <template v-slot:prepend><q-icon name="search" color="primary"></q-icon></template>
                      </q-input>
                    </div>

                    <div class="q-mb-sm">
                      <div class="text-caption text-grey-7 q-mb-xs">Код медичної послуги / інтервенції (АКПІ):</div>
                      <q-select
                        dense
                        outlined
                        v-model="simSvc"
                        :options="[
                          { label: '32003-00 Резекція ободової кишки (Потрібна посада P157 / P58)', value: '32003-00' },
                          { label: '30518-00 Часткова гастректомія з анастомозом (Потрібна посада P157)', value: '30518-00' },
                          { label: '11600-00 Спеціалізована консультація (Пакет 9)', value: '11600-00' }
                        ]"
                        emit-value
                        map-options
                        @input="calcSimulation"
                      ></q-select>
                    </div>

                    <div class="row q-col-gutter-sm q-mb-sm">
                      <div class="col-6">
                        <q-select dense outlined v-model="simAdmissionType" :options="['Планова', 'Ургентна']" label="Тип госпіталізації" @input="calcSimulation"></q-select>
                      </div>
                      <div class="col-6">
                        <q-select dense outlined v-model="simMountain" :options="[ { label: '1.00 (Стандарт)', value: 1.0 }, { label: '1.25 (Гірський)', value: 1.25 } ]" emit-value map-options label="K_гірський" @input="calcSimulation"></q-select>
                      </div>
                    </div>
                  </q-card>
                </div>

                <!-- Right Calculation Widget -->
                <div class="col-xs-12 col-md-6">
                  <q-card flat bordered class="q-pa-md bg-blue-1 text-grey-9" style="border: 1px solid #90caf9;">
                    <div class="row items-center justify-between q-mb-sm">
                      <span class="text-subtitle2 text-weight-bold text-primary">Онлайн-індикатор тарифу ПМГ-2026</span>
                      <q-badge color="accent" :label="simResult.dsgCode"></q-badge>
                    </div>

                    <div class="text-caption text-grey-8 q-mb-sm">{{ simResult.dsgName }}</div>

                    <q-separator class="q-my-sm"></q-separator>

                    <div class="row justify-between text-caption q-my-xs">
                      <span>Базова ставка ПМГ:</span>
                      <strong>{{ simResult.baseRate.toFixed(2) }} ₴</strong>
                    </div>
                    <div class="row justify-between text-caption q-my-xs">
                      <span>Коефіцієнт складності ДСГ:</span>
                      <strong>{{ simResult.coeff.toFixed(3) }}</strong>
                    </div>
                    <div class="row justify-between text-caption q-my-xs">
                      <span>Частка тарифу (Постанова №1808):</span>
                      <strong>0.55 (Хірургія) / 0.80 (Планова)</strong>
                    </div>

                    <q-separator class="q-my-sm"></q-separator>

                    <div class="row justify-between items-center q-my-sm">
                      <span class="text-subtitle2 text-weight-bold">Розрахована сума до виплати:</span>
                      <span class="text-h6 text-weight-bolder text-positive">{{ simResult.total.toLocaleString('uk-UA', {minimumFractionDigits: 2}) }} ₴</span>
                    </div>

                    <div class="text-caption text-grey-7 bg-white q-pa-sm rounded-borders">
                      <strong>Формула:</strong> 8 735.00 × {{ simResult.coeff.toFixed(3) }} × 0.55 × {{ simAdmissionType === 'Планова' ? '0.80' : '1.00' }} = {{ simResult.total.toLocaleString('uk-UA') }} ₴
                    </div>
                  </q-card>
                </div>
              </div>
            </div>

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

# Replace the existing view 5
content_before = text[:idx_start]
content_after = text[idx_v6:]

updated_text = content_before + new_encounter_view + "\n\n          " + content_after

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(updated_text)

print("Encounter view updated with authentic MedLink Details.vue layout!")
