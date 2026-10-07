import re

HTML_PATH = r"c:\__MEDLINK___\PMG\prototype_medlink\index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Reconciliation to Navigation Drawer
old_drawer_item = """            <q-item clickable v-ripple :active="currentView === 'upload'" @click="currentView = 'upload'">
              <q-item-section avatar><q-icon name="cloud_upload" size="20px" color="cyan-3"></q-icon></q-item-section>
              <q-item-section>
                <q-item-label>Імпорт файлу НСЗУ</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-badge color="info" label="П2" style="font-size: 10px;"></q-badge>
              </q-item-section>
              <q-tooltip v-if="miniState" anchor="center right" self="center left">Імпорт файлу НСЗУ</q-tooltip>
            </q-item>"""

new_drawer_items = """            <q-item clickable v-ripple :active="currentView === 'upload'" @click="currentView = 'upload'">
              <q-item-section avatar><q-icon name="cloud_upload" size="20px" color="cyan-3"></q-icon></q-item-section>
              <q-item-section>
                <q-item-label>1. Імпорт звіту OpenXML</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-badge color="info" label="API" style="font-size: 10px;"></q-badge>
              </q-item-section>
              <q-tooltip v-if="miniState" anchor="center right" self="center left">1. Імпорт звіту OpenXML</q-tooltip>
            </q-item>

            <q-item clickable v-ripple :active="currentView === 'reconciliation'" @click="currentView = 'reconciliation'">
              <q-item-section avatar><q-icon name="sync_alt" size="20px" color="purple-3"></q-icon></q-item-section>
              <q-item-section>
                <q-item-label>3. 2-Way Звірка (Прихована)</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-badge color="negative" label="5 нов." style="font-size: 10px;"></q-badge>
              </q-item-section>
              <q-tooltip v-if="miniState" anchor="center right" self="center left">3. 2-Way Звірка (Прихована дефектура)</q-tooltip>
            </q-item>"""

if old_drawer_item in content:
    content = content.replace(old_drawer_item, new_drawer_items)
    print("1. Drawer updated with 2-Way Reconciliation.")
else:
    print("1. Warning: old_drawer_item not found.")

# 2. Add Workflow Stepper Bar right after breadcrumbs
old_breadcrumbs = """        <!-- MedLink Breadcrumbs (Exact MedLink) -->
        <q-breadcrumbs class="text-grey-8 q-px-lg q-pt-sm text-uppercase text-caption text-weight-light">
          <q-breadcrumbs-el label="Головна" icon="home"></q-breadcrumbs-el>
          <q-breadcrumbs-el label="Аналітика ПМГ 2026"></q-breadcrumbs-el>
          <q-breadcrumbs-el :label="currentViewTitle" class="text-primary text-weight-bold"></q-breadcrumbs-el>
        </q-breadcrumbs>

        <!-- PAGE BODY -->"""

new_breadcrumbs = """        <!-- MedLink Breadcrumbs (Exact MedLink) -->
        <q-breadcrumbs class="text-grey-8 q-px-lg q-pt-sm text-uppercase text-caption text-weight-light">
          <q-breadcrumbs-el label="Головна" icon="home"></q-breadcrumbs-el>
          <q-breadcrumbs-el label="Аналітика ПМГ 2026"></q-breadcrumbs-el>
          <q-breadcrumbs-el :label="currentViewTitle" class="text-primary text-weight-bold"></q-breadcrumbs-el>
        </q-breadcrumbs>

        <!-- ================= INTERACTIVE WORKFLOW STEP-BY-STEP BAR ================= -->
        <div class="q-px-lg q-pt-sm q-pb-none">
          <div class="bg-white q-pa-sm rounded-borders shadow-1 row items-center justify-between no-wrap overflow-auto" style="border-left: 4px solid #4274A7;">
            <div class="row items-center no-wrap q-gutter-xs">
              <q-btn dense :flat="currentView !== 'upload'" :color="currentView === 'upload' ? 'primary' : 'grey-8'"
                     icon="cloud_upload" label="1. Імпорт OpenXML" @click="currentView = 'upload'">
                <q-tooltip>Крок 1: Завантаження та 5-стадійний SAX-аналіз звіту НСЗУ</q-tooltip>
              </q-btn>
              <q-icon name="chevron_right" color="grey-5" size="20px"></q-icon>

              <q-btn dense :flat="currentView !== 'audit'" :color="currentView === 'audit' ? 'primary' : 'grey-8'"
                     icon="table_chart" label="2. Аудит 45 колонок" @click="currentView = 'audit'">
                <q-tooltip>Крок 2: Перевірка 45 колонок та тарифи Постанови №1808</q-tooltip>
              </q-btn>
              <q-icon name="chevron_right" color="grey-5" size="20px"></q-icon>

              <q-btn dense :flat="currentView !== 'reconciliation'" :color="currentView === 'reconciliation' ? 'primary' : 'grey-8'"
                     icon="sync_alt" label="3. 2-Way Звірка" @click="currentView = 'reconciliation'">
                <q-badge color="negative" floating>5 невидимих</q-badge>
                <q-tooltip>Крок 3: Виявлення прихованої дефектури (0 ₴) між МІС та НСЗУ</q-tooltip>
              </q-btn>
              <q-icon name="chevron_right" color="grey-5" size="20px"></q-icon>

              <q-btn dense :flat="currentView !== 'discrepancies'" :color="currentView === 'discrepancies' ? 'primary' : 'grey-8'"
                     icon="warning" label="4. Дефектура (186)" @click="currentView = 'discrepancies'">
                <q-tooltip>Крок 4: Усунення 186 кодів помилок НСЗУ та ре-експорт в eHealth</q-tooltip>
              </q-btn>
              <q-icon name="chevron_right" color="grey-5" size="20px"></q-icon>

              <q-btn dense :flat="currentView !== 'doctors'" :color="currentView === 'doctors' ? 'primary' : 'grey-8'"
                     icon="bar_chart" label="5. Звіт керівництва" @click="currentView = 'doctors'">
                <q-tooltip>Крок 5: Зведений аркуш «Звіт» за лікарями та відділеннями</q-tooltip>
              </q-btn>
              <q-icon name="chevron_right" color="grey-5" size="20px"></q-icon>

              <q-btn dense :flat="currentView !== 'encounter'" :color="currentView === 'encounter' ? 'primary' : 'grey-8'"
                     icon="medical_services" label="6. АРМ Лікаря" @click="currentView = 'encounter'">
                <q-tooltip>Крок 6: Пре-білінг та Anti-Defektura перевірка посади (MedProfit P157)</q-tooltip>
              </q-btn>
              <q-icon name="chevron_right" color="grey-5" size="20px"></q-icon>

              <q-btn dense :flat="!currentView.startsWith('catalog')" :color="currentView.startsWith('catalog') ? 'primary' : 'grey-8'"
                     icon="menu_book" label="7. Довідники ПМГ" @click="currentView = 'catalog-dsg'">
                <q-tooltip>Крок 7: База знань 465 ДСГ, 148 класів, 1 257 посад</q-tooltip>
              </q-btn>
            </div>

            <!-- Live API connection indicator -->
            <div class="row items-center q-gutter-xs text-caption text-weight-bold text-positive q-pl-md">
              <q-badge color="positive" class="q-mr-xs" label="API LIVE"></q-badge>
              <span>localhost:8085 • SQLite SQL</span>
            </div>
          </div>
        </div>

        <!-- PAGE BODY -->"""

if old_breadcrumbs in content:
    content = content.replace(old_breadcrumbs, new_breadcrumbs)
    print("2. Workflow Stepper Bar added.")
else:
    print("2. Warning: old_breadcrumbs not found.")

# 3. Add Dedicated 2-Way Reconciliation Screen (Screen 3)
reconciliation_screen = """
          <!-- ================= VIEW 3: DEDICATED 2-WAY RECONCILIATION SCREEN ================= -->
          <div v-else-if="currentView === 'reconciliation'">
            <!-- Alert Banner -->
            <q-banner dense class="bg-purple-1 text-purple-10 q-mb-md rounded-borders" style="border: 1px solid #d8b4fe; border-left: 5px solid #9333ea;">
              <template v-slot:avatar>
                <q-icon name="sync_alt" color="purple"></q-icon>
              </template>
              <div class="text-body2">
                <strong>Крок 3: Двостороння 2-Way звірка між звітом НСЗУ та БД МІС «Медлінк» (<code>mis_encounter</code>):</strong>
                Виявлення <strong>«Прихованої дефектури» (Invisible Defektura)</strong>. Коли випадок відправлено до eHealth,
                але центральний компонент не включив його до звіту, у звіті НСЗУ оплата дорівнює 0 ₴ і немає коду помилки.
                Ці записи виявляються виключно через локальний SQL <code>FULL OUTER JOIN</code>.
              </div>
            </q-banner>

            <!-- Execution Action Card -->
            <div class="page-card q-mb-md">
              <div class="row items-center justify-between">
                <div>
                  <div class="text-subtitle1 text-weight-bold text-grey-9">
                    <q-icon name="storage" color="purple" class="q-mr-xs"></q-icon>
                    Локальна 2-Way синхронізація через REST API
                  </div>
                  <div class="text-caption text-grey-7">
                    Ендпоінт: <code>POST /api/v1/nszu/statements/stmt-cherkasy-2026-09/reconcile</code> (Таблиці: <code>dsg_nszu_statement_line</code> ↔ <code>mis_encounter</code>)
                  </div>
                </div>
                <div class="row q-gutter-sm">
                  <q-btn color="purple" icon="play_arrow" label="⚡ Запустити 2-Way звірку наживо" :loading="apiLoading" @click="runApiReconciliation" />
                  <q-btn outline color="grey-8" icon="file_download" label="Експорт протоколу розбіжностей" @click="$q.notify({ message: 'Завантаження reconciliation_protocol_2026.xlsx...', color: 'info' })" />
                </div>
              </div>
            </div>

            <!-- KPI Cards Row -->
            <div class="row q-col-gutter-md q-mb-md">
              <div class="col-xs-12 col-sm-6 col-md-3">
                <div class="kpi-stat-card success">
                  <div class="kpi-label">Збіглися та оплачено (MATCHED_PAID)</div>
                  <div class="kpi-num text-positive">25 ЕМЗ</div>
                  <div class="kpi-sub text-positive text-weight-bold">119 618,05 ₴ підтверджено НСЗУ</div>
                </div>
              </div>
              <div class="col-xs-12 col-sm-6 col-md-3">
                <div class="kpi-stat-card warning">
                  <div class="kpi-label">Відхилено НСЗУ (DISCREPANCY_ERROR)</div>
                  <div class="kpi-num text-warning">15 ЕМЗ</div>
                  <div class="kpi-sub text-warning text-weight-bold">85 071,51 ₴ втрат (потрібно виправлення)</div>
                </div>
              </div>
              <div class="col-xs-12 col-sm-6 col-md-3">
                <div class="kpi-stat-card danger" style="border: 2px solid #ef4444; background: #fef2f2;">
                  <div class="kpi-label text-negative font-weight-bold">🔴 ПРИХОВАНА ДЕФЕКТУРА (MISSING_IN_NHSU)</div>
                  <div class="kpi-num text-negative">5 ЕМЗ</div>
                  <div class="kpi-sub text-negative text-weight-bold">184 500,00 ₴ не враховано НСЗУ!</div>
                </div>
              </div>
              <div class="col-xs-12 col-sm-6 col-md-3">
                <div class="kpi-stat-card info">
                  <div class="kpi-label">Фантомні записи (GHOST_ENCOUNTER)</div>
                  <div class="kpi-num">0 ЕМЗ</div>
                  <div class="kpi-sub">Записів без відповідника у МІС не виявлено</div>
                </div>
              </div>
            </div>

            <!-- Reconciliation Results Table -->
            <div class="page-card">
              <div class="row items-center justify-between q-mb-sm">
                <div class="text-subtitle2 text-weight-bold text-grey-8">
                  Реєстр результатів 2-Way звірки (База даних SQLite <code>mis_encounter</code>)
                </div>
                <q-btn-toggle
                  v-model="reconcileFilter"
                  toggle-color="purple"
                  :options="[
                    { label: 'Всі записи (45)', value: 'all' },
                    { label: '🔴 Прихована дефектура (5)', value: 'missing' },
                    { label: '🟡 Відхилені (15)', value: 'rejected' },
                    { label: '🟢 Оплачені (25)', value: 'paid' }
                  ]"
                  dense
                />
              </div>

              <q-markup-table dense flat bordered separator="horizontal">
                <thead>
                  <tr class="bg-grey-2 text-left">
                    <th>Статус 2-Way</th>
                    <th>eHealth ID ЕМЗ</th>
                    <th>Пацієнт (РНОКПП)</th>
                    <th>Лікар / Відділення</th>
                    <th>Пакет</th>
                    <th>Діагноз / Послуга</th>
                    <th>Тариф Постанови №1808</th>
                    <th>Причина розбіжності</th>
                    <th class="text-center">Дія</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="r in filteredReconcileRows" :key="r.id" :class="r.statusClass">
                    <td><q-badge :color="r.badgeColor" :label="r.statusLabel" /></td>
                    <td class="code-chip">{{ r.ehealth_id.slice(0, 13) }}...</td>
                    <td>{{ r.patient }}</td>
                    <td>{{ r.doctor }}</td>
                    <td class="text-center"><q-badge color="primary">П{{ r.pkg }}</q-badge></td>
                    <td>{{ r.icd }} • {{ r.service }}</td>
                    <td class="text-right text-weight-bold">{{ r.amount.toLocaleString('uk-UA') }} ₴</td>
                    <td class="text-caption text-grey-8">{{ r.reason }}</td>
                    <td class="text-center">
                      <q-btn dense size="sm" color="purple" icon="edit" label="Виправити в МІС" @click="currentView = 'discrepancies'" />
                    </td>
                  </tr>
                </tbody>
              </q-markup-table>
            </div>

            <!-- Bottom Workflow Transition Bar -->
            <div class="row justify-between items-center q-mt-md q-pa-md bg-white rounded-borders shadow-1">
              <q-btn outline color="grey-8" icon="arrow_back" label="⬅ Крок 2: Аудит 45 колонок" @click="currentView = 'audit'" />
              <div class="text-caption text-grey-7">
                Крок 3 виконано: Виявлено 5 прихованих записів на 184 500 ₴. Перейдіть до журналу для їх усунення.
              </div>
              <q-btn color="primary" icon-right="arrow_forward" label="Крок 4: Усунення дефектури (186 помилок) ➡" @click="currentView = 'discrepancies'" />
            </div>
          </div>
"""

# Insert reconciliation_screen right before v-else-if="currentView === 'discrepancies'"
target_discr = "          <!-- ================= VIEW 3: DISCREPANCIES JOURNAL ================= -->\n          <div v-else-if=\"currentView === 'discrepancies'\">"
if target_discr in content:
    content = content.replace(target_discr, reconciliation_screen + "\n" + target_discr)
    print("3. Dedicated Reconciliation Screen inserted successfully.")
else:
    print("3. Warning: target_discr not found.")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Saved updated prototype_medlink/index.html")
