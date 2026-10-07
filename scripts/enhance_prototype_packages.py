import re
import sys

def enhance():
    file_path = r'c:\__MEDLINK___\PMG\prototype_medlink\index.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Drawer Navigation Menu: Add 46 packages item before 465 ДСГ
    drawer_target = """              <q-list class="q-pl-sm">
                <q-item clickable v-ripple :active="currentView === 'catalog-dsg'"""
    
    drawer_replacement = """              <q-list class="q-pl-sm">
                <q-item clickable v-ripple :active="currentView === 'catalog-packages'" @click="currentView = 'catalog-packages'">
                  <q-item-section avatar><q-icon name="menu_book" size="18px" color="amber-3"></q-icon></q-item-section>
                  <q-item-section>
                    <q-item-label class="text-amber-3 text-weight-bold">Всі 46 пакетів ПМГ-2026</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-badge color="accent" label="46"></q-badge>
                  </q-item-section>
                </q-item>

                <q-item clickable v-ripple :active="currentView === 'catalog-dsg'"""

    if drawer_target in html:
        html = html.replace(drawer_target, drawer_replacement, 1)
        print("1. Drawer navigation updated.")
    else:
        print("WARN: drawer_target not found!")

    # 2. Update step bar button 7 to lead to catalog-packages
    step7_old = """label="7. Довідники ПМГ" @click="currentView = 'catalog-dsg'"""
    step7_new = """label="7. Довідники ПМГ (46)" @click="currentView = 'catalog-packages'"""
    if step7_old in html:
        html = html.replace(step7_old, step7_new, 1)
        print("2. Workflow step 7 updated.")

    # 3. Update Catalog Toggle to include catalog-packages
    toggle_old = """                  :options="[
                    { label: '465 ДСГ (Пакети 3, 4, 47)', value: 'catalog-dsg' },"""
    toggle_new = """                  :options="[
                    { label: 'Всі 46 пакетів ПМГ-2026', value: 'catalog-packages' },
                    { label: '465 ДСГ (Пакети 3, 4, 47)', value: 'catalog-dsg' },"""
    if toggle_old in html:
        html = html.replace(toggle_old, toggle_new, 1)
        print("3. Catalog toggle updated.")

    # 4. Insert Sub-view 6-Packages before Sub-view 6A: DSGs
    subview_target = """              <!-- Sub-view 6A: DSGs -->
              <div v-if="currentView === 'catalog-dsg'">"""
    
    subview_new = """              <!-- Sub-view 6-Packages: All 46 Packages -->
              <div v-if="currentView === 'catalog-packages'">
                <!-- Filter bar: Search + Category Chips + Normative Docs Link -->
                <div class="row q-col-gutter-sm items-center q-mb-md">
                  <div class="col-xs-12 col-md-4">
                    <q-input dense outlined v-model="packageCatalogSearch" placeholder="Пошук пакета (назва, номер, формула)..." clearable>
                      <template v-slot:prepend><q-icon name="search"></q-icon></template>
                    </q-input>
                  </div>
                  <div class="col-xs-12 col-md-5">
                    <q-select dense outlined v-model="packageSelectedCategory" :options="packageCategoriesList" label="Категорія медичної допомоги" emit-value map-options></q-select>
                  </div>
                  <div class="col-xs-12 col-md-3 text-right">
                    <q-btn outline color="primary" icon="menu_book" label="Нормативний портал" @click="openDoc('../normative_packages/index.html')">
                      <q-tooltip>Відкрити автономний реєстр 12 нормативних досьє</q-tooltip>
                    </q-btn>
                  </div>
                </div>

                <!-- Summary Badges Bar -->
                <div class="row q-gutter-sm items-center q-mb-sm text-caption text-grey-8">
                  <span class="text-weight-bold">Відображено: {{ filteredPackagesList.length }} з 46 пакетів</span>
                  <q-badge color="primary">Постанова КМУ № 1808</q-badge>
                  <q-badge color="teal">Додаток 1 (465 ДСГ)</q-badge>
                  <q-badge color="indigo">Додаток 2 (Хірургія 1-дня)</q-badge>
                  <q-badge color="accent">148 Амбулаторних класів</q-badge>
                </div>

                <q-table
                  flat
                  bordered
                  dense
                  :data="filteredPackagesList"
                  :columns="packagesCatalogColumns"
                  row-key="id"
                  :pagination="{ rowsPerPage: 15 }"
                >
                  <template v-slot:body-cell-code="props">
                    <q-td :props="props" class="text-center">
                      <q-chip dense color="primary" text-color="white" class="text-weight-bold cursor-pointer" @click="openPackageInfo(props.row.id)">
                        {{ props.value }}
                        <q-tooltip>Клікніть для нормативного досьє та формули</q-tooltip>
                      </q-chip>
                    </q-td>
                  </template>

                  <template v-slot:body-cell-category="props">
                    <q-td :props="props">
                      <q-badge :color="getCategoryColor(props.value)" :label="props.value"></q-badge>
                    </q-td>
                  </template>

                  <template v-slot:body-cell-base_rate="props">
                    <q-td :props="props" class="text-right">
                      <span class="text-weight-bolder text-positive" v-if="props.value > 0">
                        {{ Number(props.value).toLocaleString('uk-UA', {minimumFractionDigits: 2}) }} ₴
                      </span>
                      <span class="text-grey-6 text-weight-bold" v-else>
                        За формулою
                      </span>
                      <div class="text-caption text-grey-7" style="font-size: 10px;">{{ props.row.rate_period }}</div>
                    </q-td>
                  </template>

                  <template v-slot:body-cell-actions="props">
                    <q-td :props="props" class="text-center">
                      <q-btn dense size="sm" color="primary" icon="info" label="Досьє" @click="openPackageInfo(props.row.id)" class="q-mr-xs">
                        <q-tooltip>Нормативна база, формули та валідації eHealth</q-tooltip>
                      </q-btn>
                      <q-btn dense size="sm" flat color="grey-8" icon="open_in_new" @click="openDossierHtml(props.row.group_file, props.row.id)">
                        <q-tooltip>Відкрити повне нормативне досьє у новій вкладці</q-tooltip>
                      </q-btn>
                    </q-td>
                  </template>
                </q-table>
              </div>

              <!-- Sub-view 6A: DSGs -->
              <div v-else-if="currentView === 'catalog-dsg'">"""

    if subview_target in html:
        html = html.replace(subview_target, subview_new, 1)
        print("4. Sub-view 6-Packages inserted.")
    else:
        print("WARN: subview_target not found!")

    # 5. Make Audit table package cell clickable with info icon
    audit_pkg_old = """                <!-- Column: Пакет -->
                <template v-slot:body-cell-package="props">
                  <q-td :props="props">
                    <q-badge color="grey-7" :label="'Пакет ' + props.value"></q-badge>
                  </q-td>
                </template>"""

    audit_pkg_new = """                <!-- Column: Пакет -->
                <template v-slot:body-cell-package="props">
                  <q-td :props="props" class="text-center">
                    <q-chip dense clickable color="indigo-1" text-color="indigo-9" icon-right="info" @click="openPackageInfo(props.value)">
                      Пакет {{ props.value }}
                      <q-tooltip>Клікніть для нормативного досьє, формули та Постанови №1808</q-tooltip>
                    </q-chip>
                  </q-td>
                </template>"""

    if audit_pkg_old in html:
        html = html.replace(audit_pkg_old, audit_pkg_new, 1)
        print("5. Audit table package cell made clickable with info icon.")

    # 6. Make 2-Way Reconcile table package cell clickable with info icon
    rec_pkg_old = """<td class="text-center"><q-badge color="primary">П{{ r.pkg }}</q-badge></td>"""
    rec_pkg_new = """<td class="text-center">
                      <q-chip dense clickable color="indigo-1" text-color="indigo-9" icon-right="info" @click="openPackageInfo(r.pkg)">
                        П{{ r.pkg }}
                        <q-tooltip>Нормативне досьє Пакета {{ r.pkg }} (Постанова №1808)</q-tooltip>
                      </q-chip>
                    </td>"""

    if rec_pkg_old in html:
        html = html.replace(rec_pkg_old, rec_pkg_new, 1)
        print("6. Reconcile table package cell made clickable with info icon.")

    # 7. Make Discrepancies coding cell display package info chip
    disc_coding_old = """                <template v-slot:body-cell-coding="props">
                  <q-td :props="props">
                    <div>МКХ: <strong class="text-primary">{{ props.row.diag_main }}</strong></div>
                    <div>АКПІ: <span class="code-chip">{{ props.row.services || '—' }}</span></div>
                  </q-td>
                </template>"""

    disc_coding_new = """                <template v-slot:body-cell-coding="props">
                  <q-td :props="props">
                    <div>МКХ: <strong class="text-primary">{{ props.row.diag_main }}</strong></div>
                    <div>АКПІ: <span class="code-chip">{{ props.row.services || '—' }}</span></div>
                    <div v-if="props.row.package" class="q-mt-xs">
                      <q-chip dense clickable color="indigo-1" text-color="indigo-9" icon-right="info" size="xs" @click="openPackageInfo(props.row.package)">
                        Пакет {{ props.row.package }}
                        <q-tooltip>Нормативне досьє Пакета {{ props.row.package }}</q-tooltip>
                      </q-chip>
                    </div>
                  </q-td>
                </template>"""

    if disc_coding_old in html:
        html = html.replace(disc_coding_old, disc_coding_new, 1)
        print("7. Discrepancies coding cell updated with package chip.")

    # 8. Add append button with info icon in Pre-billing simPackage select
    prebill_pkg_old = """                    <div class="q-mb-sm">
                      <div class="text-caption text-grey-7 q-mb-xs">Пакет медичних послуг:</div>
                      <q-select
                        dense
                        outlined
                        v-model="simPackage"
                        :options="simPackageOptions"
                        @input="calcSimulation"
                      ></q-select>
                    </div>"""

    prebill_pkg_new = """                    <div class="q-mb-sm">
                      <div class="text-caption text-grey-7 q-mb-xs">Пакет медичних послуг:</div>
                      <q-select
                        dense
                        outlined
                        v-model="simPackage"
                        :options="simPackageOptions"
                        @input="calcSimulation"
                      >
                        <template v-slot:append>
                          <q-btn round dense flat icon="info" color="primary" size="sm" @click.stop="openPackageInfo(simPackage)">
                            <q-tooltip>Нормативна база та формула для обраного пакета</q-tooltip>
                          </q-btn>
                        </template>
                      </q-select>
                    </div>"""

    if prebill_pkg_old in html:
        html = html.replace(prebill_pkg_old, prebill_pkg_new, 1)
        print("8. Pre-billing package select updated with info icon.")

    # 9. Add Doc 9 Link into docLinks array
    doclink_target = """            { title: '5. Посібник інтеграції у фронтенд', badge: 'App.View Quasar', desc: 'Покрокове підключення Vue-компонентів, меню навігації та роутингу.', url: '../docs_html/05_frontend_integration_guide.html' }"""
    doclink_replacement = """            { title: '5. Посібник інтеграції у фронтенд', badge: 'App.View Quasar', desc: 'Покрокове підключення Vue-компонентів, меню навігації та роутингу.', url: '../docs_html/05_frontend_integration_guide.html' },
            { title: '9. Реєстр та нормативка всіх 46 пакетів ПМГ', badge: 'Постанова №1808', desc: 'Повний каталог усіх 46 пакетів ПМГ-2026: тарифи, формули, валідації eHealth, нормативні акти.', url: '../docs_html/09_all_pmg_packages_normative_guide.html' }"""

    if doclink_target in html:
        html = html.replace(doclink_target, doclink_replacement, 1)
        print("9. Technical documentation links updated with Chapter 9.")

    # 10. Add packageInfoDialog Modal
    dialog_insert_before = """      <!-- ================= MODAL: 45 COLUMNS FULL INSPECT ================= -->"""
    package_modal_markup = """      <!-- ================= MODAL: ALL 46 PACKAGES NORMATIVE DOSSIER ================= -->
      <q-dialog v-model="packageInfoDialog" maximized transition-show="slide-up" transition-hide="slide-down">
        <q-card class="bg-grey-1" v-if="selectedPackageInfo">
          <q-toolbar class="bg-primary text-white">
            <q-icon name="menu_book" size="22px" class="q-mr-sm"></q-icon>
            <q-toolbar-title class="text-subtitle1 text-weight-bold">
              Пакет {{ selectedPackageInfo.id }} ({{ selectedPackageInfo.code }}): {{ selectedPackageInfo.name }}
            </q-toolbar-title>
            <q-btn flat round dense icon="close" v-close-popup></q-btn>
          </q-toolbar>

          <q-card-section class="q-pa-md">
            <!-- Header Card with badges -->
            <div class="row q-col-gutter-md q-mb-md">
              <div class="col-xs-12 col-md-8">
                <div class="bg-white q-pa-md rounded-borders shadow-1">
                  <div class="row items-center q-gutter-sm q-mb-sm">
                    <q-badge color="primary" class="text-subtitle2 q-pa-xs">Пакет {{ selectedPackageInfo.id }}</q-badge>
                    <q-badge :color="getCategoryColor(selectedPackageInfo.category)">{{ selectedPackageInfo.category }}</q-badge>
                    <q-badge color="teal">Модель: {{ selectedPackageInfo.payment_model }}</q-badge>
                  </div>
                  <div class="text-h6 text-primary text-weight-bolder q-mb-xs">{{ selectedPackageInfo.name }}</div>
                  <div class="text-body2 text-grey-8">{{ selectedPackageInfo.description }}</div>
                </div>
              </div>

              <div class="col-xs-12 col-md-4">
                <div class="bg-white q-pa-md rounded-borders shadow-1">
                  <div class="text-caption text-uppercase text-grey-7 text-weight-bold">Базовий тариф 2026 року</div>
                  <div class="text-h5 text-positive text-weight-bolder q-my-xs">
                    {{ selectedPackageInfo.base_rate > 0 ? Number(selectedPackageInfo.base_rate).toLocaleString('uk-UA', {minimumFractionDigits: 2}) + ' ₴' : 'За калькуляцією' }}
                  </div>
                  <div class="text-caption text-grey-8 q-mb-sm">Періодичність / Одиниця: <strong>{{ selectedPackageInfo.rate_period }}</strong></div>
                  <div class="text-caption text-primary text-weight-bold">Постанова КМУ № 1808 ({{ selectedPackageInfo.chapter_cmu }})</div>
                </div>
              </div>
            </div>

            <!-- Formula & Math Calculation -->
            <div class="bg-white q-pa-md rounded-borders shadow-1 q-mb-md" style="border-left: 4px solid #00897b;">
              <div class="text-subtitle1 text-teal-9 text-weight-bold row items-center q-mb-xs">
                <q-icon name="functions" class="q-mr-xs" size="20px"></q-icon>
                Офіційна формула розрахунку тарифу (Постанова КМУ № 1808)
              </div>
              <div class="bg-grey-2 q-pa-sm rounded-borders text-mono text-weight-bold text-teal-10 q-mb-sm" style="font-family: Consolas, monospace; font-size: 13px;">
                {{ selectedPackageInfo.formula || 'Тариф нараховується за фактично наданий обсяг медичних послуг.' }}
              </div>
              <!-- Coefficients breakdown -->
              <div v-if="selectedPackageInfo.coefficients && Object.keys(selectedPackageInfo.coefficients).length > 0">
                <div class="text-caption text-weight-bold text-grey-9 q-mb-xs">Коригувальні коефіцієнти:</div>
                <div class="row q-col-gutter-xs">
                  <div class="col-xs-12 col-sm-6 col-md-4" v-for="(val, k) in selectedPackageInfo.coefficients" :key="k">
                    <div class="q-pa-xs bg-grey-1 rounded-borders border text-caption">
                      <strong>{{ k }}:</strong>
                      <span v-if="typeof val === 'object'">
                        <span v-for="(subV, subK) in val" :key="subK" class="q-ml-xs">
                          <q-badge color="grey-7" :label="subK + ': ' + subV"></q-badge>
                        </span>
                      </span>
                      <span v-else class="text-primary text-weight-bold q-ml-xs">{{ val }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- eHealth Validations & Defektura Risks -->
            <div class="row q-col-gutter-md q-mb-md">
              <div class="col-xs-12 col-md-6">
                <div class="bg-white q-pa-md rounded-borders shadow-1 h-100" style="border-left: 4px solid #1976d2;">
                  <div class="text-subtitle1 text-primary text-weight-bold row items-center q-mb-sm">
                    <q-icon name="fact_check" class="q-mr-xs" size="20px"></q-icon>
                    Вимоги eHealth та обов\'язкові поля в ЕМЗ
                  </div>
                  <q-list dense>
                    <q-item v-for="(valReq, idx) in selectedPackageInfo.ehealth_validations" :key="idx" class="q-px-none">
                      <q-item-section avatar min-width="24px">
                        <q-icon name="check_circle" color="positive" size="18px"></q-icon>
                      </q-item-section>
                      <q-item-section class="text-caption text-grey-9">{{ valReq }}</q-item-section>
                    </q-item>
                  </q-list>
                </div>
              </div>

              <div class="col-xs-12 col-md-6">
                <div class="bg-white q-pa-md rounded-borders shadow-1 h-100" style="border-left: 4px solid #c62828;">
                  <div class="text-subtitle1 text-negative text-weight-bold row items-center q-mb-sm">
                    <q-icon name="gavel" class="q-mr-xs" size="20px"></q-icon>
                    Нормативне регулювання та накази МОЗ
                  </div>
                  <q-list dense>
                    <q-item v-for="(law, idx) in selectedPackageInfo.law_references" :key="idx" class="q-px-none">
                      <q-item-section avatar min-width="24px">
                        <q-icon name="gavel" color="primary" size="18px"></q-icon>
                      </q-item-section>
                      <q-item-section>
                        <a :href="law.url" target="_blank" class="text-caption text-primary text-weight-medium">
                          {{ law.title }} ↗
                        </a>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </div>
              </div>
            </div>

            <!-- Action buttons: open full HTML dossier or official PDFs -->
            <div class="row q-gutter-sm justify-center q-mt-md">
              <q-btn color="primary" icon="description" label="Відкрити повне досьє пакета (HTML)" @click="openDossierHtml(selectedPackageInfo.group_file, selectedPackageInfo.id)"></q-btn>
              <q-btn outline color="primary" icon="picture_as_pdf" label="Текст Постанови № 1808 (PDF)" @click="openDoc('../extracted_data/normative_docs/pmg-2026.pdf')"></q-btn>
              <q-btn outline color="teal" icon="picture_as_pdf" label="Додаток 1 (Таблиця ДСГ, PDF)" @click="openDoc('../extracted_data/normative_docs/Додаток-1.pdf')"></q-btn>
              <q-btn outline color="indigo" icon="picture_as_pdf" label="Додаток 2 (Хірургія 1 дня, PDF)" @click="openDoc('../extracted_data/normative_docs/Додаток-2.pdf')"></q-btn>
            </div>
          </q-card-section>

          <q-separator></q-separator>
          <q-card-actions align="right" class="bg-white">
            <q-btn flat label="Закрити" color="primary" v-close-popup></q-btn>
          </q-card-actions>
        </q-card>
      </q-dialog>

"""
    if dialog_insert_before in html:
        html = html.replace(dialog_insert_before, package_modal_markup + dialog_insert_before, 1)
        print("10. packageInfoDialog modal added.")

    # 11. Add Vue data fields
    data_target = """          // Classifiers Catalog
          catalogSearch: '',"""

    data_fields_new = """          // All 46 Packages Catalog
          packageCatalogSearch: '',
          packageSelectedCategory: 'ALL',
          packageCategoriesList: [
            { label: 'Усі категорії (46 пакетів)', value: 'ALL' },
            { label: 'Первинна допомога', value: 'Первинна допомога' },
            { label: 'Екстрена допомога', value: 'Екстрена допомога' },
            { label: 'Спеціалізована та хірургічна допомога (ДСГ)', value: 'Спеціалізована та хірургічна допомога (ДСГ)' },
            { label: 'Пріоритетні стаціонарні пакети', value: 'Пріоритетні стаціонарні пакети' },
            { label: 'Амбулаторна допомога та скринінги', value: 'Амбулаторна допомога та скринінги' },
            { label: 'Онкологія та онкогематологія', value: 'Онкологія та онкогематологія' },
            { label: 'Реабілітація', value: 'Реабілітація' },
            { label: 'Паліативна допомога', value: 'Паліативна допомога' },
            { label: 'Психіатрія та терапія залежностей', value: 'Психіатрія та терапія залежностей' },
            { label: 'Інфекційні захворювання', value: 'Інфекційні захворювання' },
            { label: 'Високотехнологічна допомога та трансплантація', value: 'Високотехнологічна допомога та трансплантація' },
            { label: 'Оборонна готовність та ВЛК', value: 'Оборонна готовність та ВЛК' }
          ],
          packagesList: [],
          packageInfoDialog: false,
          selectedPackageInfo: null,
          packagesCatalogColumns: [
            { name: 'code', label: 'Пакет', field: 'code', align: 'center', sortable: true },
            { name: 'name', label: 'Назва медичного пакета', field: 'name', align: 'left', sortable: true },
            { name: 'category', label: 'Категорія', field: 'category', align: 'left', sortable: true },
            { name: 'payment_model', label: 'Модель оплати', field: 'payment_model', align: 'center', sortable: true },
            { name: 'base_rate', label: 'Базовий тариф 2026', field: 'base_rate', align: 'right', sortable: true },
            { name: 'formula', label: 'Формула Постанови № 1808', field: 'formula', align: 'left' },
            { name: 'actions', label: 'Нормативка', field: 'id', align: 'center' }
          ],

          // Classifiers Catalog
          catalogSearch: '',"""

    if data_target in html:
        html = html.replace(data_target, data_fields_new, 1)
        print("11. Vue data fields added.")

    # 12. Add Vue computed fields: filteredPackagesList & currentViewTitle entry
    computed_title_old = """            'catalog-dsg': 'Довідник 465 ДСГ (Пакети 3, 4, 47)',"""
    computed_title_new = """            'catalog-packages': 'Повний реєстр 46 пакетів медичних гарантій 2026',
            'catalog-dsg': 'Довідник 465 ДСГ (Пакети 3, 4, 47)',"""

    if computed_title_old in html:
        html = html.replace(computed_title_old, computed_title_new, 1)
        print("12. currentViewTitle entry added.")

    computed_target = """        dsgList: function () {"""
    computed_packages_new = """        filteredPackagesList: function () {
          const pkgs = (this.packagesList && this.packagesList.length > 0) ? this.packagesList : (this.dataStore.packages || []);
          const q = (this.packageCatalogSearch || '').trim().toLowerCase();
          const cat = this.packageSelectedCategory;
          return pkgs.filter(p => {
            if (cat !== 'ALL' && p.category !== cat) return false;
            if (q) {
              const match = (String(p.id).includes(q) ||
                             (p.code || '').toLowerCase().includes(q) ||
                             (p.name || '').toLowerCase().includes(q) ||
                             (p.description || '').toLowerCase().includes(q) ||
                             (p.formula || '').toLowerCase().includes(q) ||
                             (p.chapter_cmu || '').toLowerCase().includes(q));
              if (!match) return false;
            }
            return true;
          });
        },
        dsgList: function () {"""

    if computed_target in html:
        html = html.replace(computed_target, computed_packages_new, 1)
        print("13. filteredPackagesList computed property added.")

    # 14. Add Vue methods: getCategoryColor, openPackageInfo, openDossierHtml, fetchPackagesFromApi
    methods_target = """      methods: {
        openTourDialog: function (step) {"""

    methods_new = """      methods: {
        getCategoryColor: function (cat) {
          const map = {
            'Первинна допомога': 'teal-7',
            'Екстрена допомога': 'red-8',
            'Спеціалізована та хірургічна допомога (ДСГ)': 'primary',
            'Пріоритетні стаціонарні пакети': 'deep-orange-7',
            'Амбулаторна допомога та скринінги': 'blue-7',
            'Онкологія та онкогематологія': 'purple-7',
            'Реабілітація': 'green-8',
            'Паліативна допомога': 'brown-6',
            'Психіатрія та терапія залежностей': 'indigo-7',
            'Інфекційні захворювання': 'amber-9',
            'Високотехнологічна допомога та трансплантація': 'cyan-8',
            'Оборонна готовність та ВЛК': 'blue-grey-8'
          };
          return map[cat] || 'grey-7';
        },

        openPackageInfo: function (pkgIdOrCode) {
          if (!pkgIdOrCode) return;
          const rawId = String(pkgIdOrCode).replace(/[^0-9]/g, '');
          const pkgs = (this.packagesList && this.packagesList.length > 0) ? this.packagesList : (this.dataStore.packages || []);
          let found = pkgs.find(p => String(p.id) === String(rawId) || String(p.code).toUpperCase() === String(pkgIdOrCode).toUpperCase());
          if (!found) {
            found = pkgs.find(p => String(p.id) === String(pkgIdOrCode) || (p.name && p.name.includes(String(pkgIdOrCode))));
          }
          if (found) {
            this.selectedPackageInfo = found;
            this.packageInfoDialog = true;
          } else {
            const self = this;
            fetch('/api/v1/pmg/dictionaries/packages/' + (rawId || pkgIdOrCode))
              .then(res => res.json())
              .then(data => {
                self.selectedPackageInfo = data;
                self.packageInfoDialog = true;
              })
              .catch(e => {
                self.$q.notify({ message: 'Пакет ' + pkgIdOrCode + ' не знайдено в базі', color: 'warning' });
              });
          }
        },

        openDossierHtml: function (groupFile, pkgId) {
          const file = groupFile || 'index.html';
          const url = '../normative_packages/' + file + '#pkg-' + (pkgId || '');
          window.open(url, '_blank');
        },

        fetchPackagesFromApi: function () {
          const self = this;
          fetch('/api/v1/pmg/dictionaries/packages')
            .then(res => res.json())
            .then(data => {
              if (Array.isArray(data) && data.length > 0) {
                self.packagesList = data;
              } else {
                self.packagesList = self.dataStore.packages || [];
              }
            })
            .catch(err => {
              console.warn('Fallback to local packages data:', err);
              self.packagesList = self.dataStore.packages || [];
            });
        },

        openTourDialog: function (step) {"""

    if methods_target in html:
        html = html.replace(methods_target, methods_new, 1)
        print("14. Vue methods added.")

    # 15. Call fetchPackagesFromApi in mounted
    mounted_old = """      mounted: function () {
        this.calcSimulation();
      }"""
    mounted_new = """      mounted: function () {
        this.fetchPackagesFromApi();
        this.calcSimulation();
      }"""

    if mounted_old in html:
        html = html.replace(mounted_old, mounted_new, 1)
        print("15. mounted hook updated to call fetchPackagesFromApi().")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("ALL updates to prototype_medlink/index.html completed successfully!")

if __name__ == '__main__':
    enhance()
