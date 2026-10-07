HTML_PATH = r"c:\__MEDLINK___\PMG\prototype_medlink\index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add Diff Modal Dialog before closing layout
diff_modal_markup = """
      <!-- ================= MODAL: CODE DIFF FOR DETAILS.VUE (FOR DEVELOPER & ANALYST) ================= -->
      <q-dialog v-model="detailsDiffModal" maximized>
        <q-card class="bg-grey-10 text-white">
          <q-bar class="bg-primary text-white">
            <q-icon name="code" />
            <span class="text-weight-bold">Інструкція модифікації: src/pages/medicalEvents/encounter/subpages/Details.vue</span>
            <q-space />
            <q-btn dense flat icon="close" v-close-popup />
          </q-bar>

          <q-card-section class="q-pa-lg">
            <div class="text-h6 text-white q-mb-xs">
              Як доповнити існуючу форму картки взаємодії МІС «Медлінк» без її зламу
            </div>
            <div class="text-caption text-grey-4 q-mb-md">
              Файл: <code>c:/__MEDLINK___/__MEDLINK/evomis/src/App.View/src/pages/medicalEvents/encounter/subpages/Details.vue</code>
            </div>

            <div class="bg-black q-pa-md rounded-borders text-body2" style="font-family: monospace; line-height: 1.6; border: 1px solid #334155;">
              <span class="text-grey-6">// 1. У шаблоні Details.vue (розділ кнопок дій, рядки 200-220):</span><br>
              <span class="text-grey-5">&nbsp;&nbsp;&lt;q-btn v-if="canEditEncounter && !allowsOperatingWithoutEhealth"</span><br>
              <span class="text-grey-5">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;icon="fas fa-signature" color="primary q-mr-sm"</span><br>
              <span class="text-grey-5">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;@click="createWithSign" :label="labelCreateEncounterWithSignBtn" /&gt;</span><br><br>

              <span class="text-positive text-weight-bold">// +++++ ВСТАВИТИ НАСТУПНИЙ БЛОК ВІДЖЕТА ПРЕ-БІЛІНГУ (НЕ ЛАМАЮЧИ КНОПКУ КЕП) +++++</span><br>
              <span class="text-positive">&nbsp;&nbsp;&lt;!-- Anti-Defektura перевірка спеціальності лікаря перед підписанням КЕП --&gt;</span><br>
              <span class="text-positive">&nbsp;&nbsp;&lt;pmg-prebilling-badge</span><br>
              <span class="text-positive">&nbsp;&nbsp;&nbsp;&nbsp;:encounter-data="encounterInformation"</span><br>
              <span class="text-positive">&nbsp;&nbsp;&nbsp;&nbsp;:doctor-position="user.positionCode"</span><br>
              <span class="text-positive">&nbsp;&nbsp;&nbsp;&nbsp;@validation-result="onPmgValidationChecked"</span><br>
              <span class="text-positive">&nbsp;&nbsp;/&gt;</span><br><br>

              <span class="text-grey-5">&nbsp;&nbsp;&lt;q-btn v-if="canEditEncounter" @click="showDsgRecommendedCodesDialog"</span><br>
              <span class="text-grey-5">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:label="isEncounterEdit ? labelSaveEncounterBtn : createEncounterButtonLabel" /&gt;</span><br><br>

              <span class="text-grey-6">// 2. У блоці скрипта Details.vue (імпорт та реєстрація компонента):</span><br>
              <span class="text-positive">&nbsp;&nbsp;import PmgPrebillingBadge from "@/components/pmg/PmgPrebillingBadge.vue";</span><br>
              <span class="text-positive">&nbsp;&nbsp;components: { PmgPrebillingBadge, ... }</span>
            </div>

            <div class="row q-gutter-md q-mt-md">
              <q-banner dense class="bg-blue-9 text-white rounded-borders col">
                <strong>Для аналітика:</strong> Процес лікаря залишається звичним: лікар натискає кнопку збереження, система викликає бекенд <code>/api/v1/pmg/prebilling/calculate</code>, валідує відповідність посади спеціальності інтервенції та виводить розраховану суму до виплати.
              </q-banner>
              <q-banner dense class="bg-green-9 text-white rounded-borders col">
                <strong>Для розробника:</strong> Жодних змін у моделях EF Core <code>mis_encounter</code> чи валідаціях eHealth. Віджет працює асинхронно і не блокує стандартний життєвий цикл компонента.
              </q-banner>
            </div>
          </q-card-section>
        </q-card>
      </q-dialog>
"""

# Insert modal before </q-layout>
if "</q-layout>" in text and "detailsDiffModal" not in text:
    text = text.replace("</q-layout>", diff_modal_markup + "\n    </q-layout>")
    print("Added detailsDiffModal markup!")

# Add data properties to Vue instance
target_data = "reconcileFilter: 'all',"
replacement_data = """reconcileFilter: 'all',
          detailsDiffModal: false,
          selectedEncounterTab: 'encounter-edit',
          simDoctorPos: 'P157',
          simAdmissionType: 'Планова',
          doctorPositionOptions: [
            { label: 'Хірург-онколог (P157) — Відповідає вимогам хірургії', value: 'P157' },
            { label: 'Терапевт (P122) — Викличе блокуючу помилку ERR_DOC_SPEC_04!', value: 'P122' },
            { label: 'Хірург загальний (P58) — Дозволено для окремих операцій', value: 'P58' },
            { label: 'Онколог хіміотерапевт (P158) — Дозволено для пакетів 4 та 17', value: 'P158' }
          ],"""

if target_data in text and "detailsDiffModal: false" not in text:
    text = text.replace(target_data, replacement_data)
    print("Added data properties for encounter view!")

# Add onSignEncounter method
target_method = "runApiReconciliation: function() {"
method_add = """onSignEncounter: function() {
          if (this.simResult.warning && this.simResult.warning.severity === 'CRITICAL') {
            this.$q.notify({
              message: '⛔ ДІЮ ЗАБЛОКОВАНО: Спеціальність лікаря P122 призведе до дефектури (0 ₴)! Змініть посаду лікаря на P157 перед накладанням КЕП.',
              color: 'negative',
              icon: 'report_problem',
              timeout: 6000
            });
          } else {
            this.$q.notify({
              message: '✓ КЕП успішно накладено! Взаємодію підписано та передано до eHealth (Очікуваний тариф: ' + this.simResult.total.toLocaleString('uk-UA') + ' ₴)',
              color: 'positive',
              icon: 'verified'
            });
          }
        },
        runApiReconciliation: function() {"""

if target_method in text and "onSignEncounter:" not in text:
    text = text.replace(target_method, method_add)
    print("Added onSignEncounter method!")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("Modal and data properties added successfully!")
