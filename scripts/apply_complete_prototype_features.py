import re

HTML_PATH = r"c:\__MEDLINK___\PMG\prototype_medlink\index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Insert Screen 3 before Discrepancies view
target_str = '<div v-else-if="currentView === \'discrepancies\'">'

reconciliation_screen = """<!-- ================= VIEW 3: DEDICATED 2-WAY RECONCILIATION SCREEN ================= -->
          <div v-else-if="currentView === 'reconciliation'">
            <!-- Alert Banner -->
            <q-banner dense class="bg-purple-1 text-purple-10 q-mb-md rounded-borders" style="border: 1px solid #d8b4fe; border-left: 5px solid #9333ea;">
              <template v-slot:avatar>
                <q-icon name="sync_alt" color="purple"></q-icon>
              </template>
              <div class="text-body2">
                <strong>Крок 3: Двостороння 2-Way звірка між звітом НСЗУ та внутрішньою БД МІС «Медлінк» (<code>mis_encounter</code>):</strong>
                Виявлення <strong>«Прихованої дефектури» (Invisible Defektura)</strong>. Коли випадок відправлено до eHealth,
                але центральний компонент не включив його до звіту, у звіті НСЗУ оплата дорівнює 0 ₴ і немає коду помилки.
                Ці випадки виявляються виключно через локальний SQL <code>FULL OUTER JOIN</code> у базі даних SQLite!
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
                  <q-btn color="purple" icon="play_arrow" label="⚡ Запустити 2-Way звірку через API" :loading="apiLoading" @click="runApiReconciliation" />
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
                  <div class="kpi-label text-negative text-weight-bold">🔴 ПРИХОВАНА ДЕФЕКТУРА (MISSING_IN_NHSU)</div>
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
          </div>\n\n          """

if target_str in content:
    content = content.replace(target_str, reconciliation_screen + target_str)
    print("Screen 3 inserted successfully.")
else:
    print("Warning: target_str not found.")

# 2. Add reconciliation data & methods to Vue instance
vue_data_anchor = "dataStore: DATA_STORE,"
vue_data_add = """dataStore: DATA_STORE,
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

if vue_data_anchor in content:
    content = content.replace(vue_data_anchor, vue_data_add)
    print("Vue data updated with reconcile variables.")
else:
    print("Warning: vue_data_anchor not found.")

# 3. Add computed property for filteredReconcileRows
vue_computed_anchor = "currentTourStepData: function () {"
vue_computed_add = """filteredReconcileRows: function() {
          if (this.reconcileFilter === 'missing') return this.reconcileRowsData.filter(r => r.statusLabel.includes('MISSING'));
          if (this.reconcileFilter === 'rejected') return this.reconcileRowsData.filter(r => r.statusLabel.includes('DISCREPANCY'));
          if (this.reconcileFilter === 'paid') return this.reconcileRowsData.filter(r => r.statusLabel.includes('MATCHED'));
          return this.reconcileRowsData;
        },
        currentTourStepData: function () {"""

if vue_computed_anchor in content:
    content = content.replace(vue_computed_anchor, vue_computed_add)
    print("Vue computed property filteredReconcileRows added.")
else:
    print("Warning: vue_computed_anchor not found.")

# 4. Add API methods to Vue instance
vue_methods_anchor = "executeTourAction: function (step) {"
vue_methods_add = """runApiReconciliation: function() {
          this.apiLoading = true;
          const self = this;
          fetch('/api/v1/nszu/statements/stmt-cherkasy-2026-09/reconcile', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
              self.apiLoading = false;
              self.$q.notify({
                message: `API Live (SQLite): 2-Way звірку виконано! Виявлено ${data.invisibleDefekturaCount} невидимих записів на ${data.invisibleDefekturaAmountUah.toLocaleString('uk-UA')} ₴!`,
                color: 'warning',
                icon: 'warning',
                timeout: 5000
              });
            })
            .catch(err => {
              self.apiLoading = false;
              self.$q.notify({ message: 'API Error: ' + err.message, color: 'negative' });
            });
        },
        executeTourAction: function (step) {"""

if vue_methods_anchor in content:
    content = content.replace(vue_methods_anchor, vue_methods_add)
    print("runApiReconciliation method added.")
else:
    print("Warning: vue_methods_anchor not found.")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("All prototype updates applied successfully.")
