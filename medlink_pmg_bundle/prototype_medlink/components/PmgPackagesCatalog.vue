<template>
  <div data-testid="PmgPackagesCatalog" class="q-pa-md">
    <q-card flat bordered class="q-pa-md bg-white">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <div class="text-h6 text-primary text-weight-bold row items-center">
            <q-icon name="menu_book" class="q-mr-sm" size="24px" />
            Повний класифікатор медичних пакетів ПМГ-2026 (46 пакетів)
          </div>
          <div class="text-caption text-grey-7">
            Тарифи, специфікації, формули та валідації eHealth відповідно до Постанови КМУ № 1808 від 31.12.2025 (зі змінами)
          </div>
        </div>
        <div class="row q-gutter-sm">
          <q-btn
            color="primary"
            outline
            icon="description"
            label="Нормативний портал (12 досьє)"
            dense
            class="q-px-sm"
            @click="openDossierPortal"
          />
          <q-btn
            color="primary"
            icon="file_download"
            label="Експорт JSON/CSV"
            dense
            class="q-px-sm"
            @click="exportPackages"
          />
        </div>
      </div>

      <!-- Filters & Summary Row -->
      <div class="row q-col-gutter-md q-mb-md">
        <div class="col-xs-12 col-sm-4">
          <q-input
            dense
            outlined
            v-model="searchQuery"
            placeholder="Пошук за кодом, назвою, формулою чи описом..."
            clearable
          >
            <template v-slot:prepend><q-icon name="search" /></template>
          </q-input>
        </div>

        <div class="col-xs-12 col-sm-5">
          <q-select
            dense
            outlined
            v-model="selectedCategory"
            :options="categoryOptions"
            label="Категорія медичної допомоги"
            emit-value
            map-options
          />
        </div>

        <div class="col-xs-12 col-sm-3 text-right flex items-center justify-end">
          <q-badge color="primary" class="q-pa-xs text-subtitle2">
            Всього пакетів: {{ filteredPackages.length }} / {{ packages.length }}
          </q-badge>
        </div>
      </div>

      <!-- Category Filter Chips -->
      <div class="row q-gutter-xs q-mb-md">
        <q-chip
          v-for="cat in quickCategories"
          :key="cat.value"
          clickable
          :selected="selectedCategory === cat.value"
          @click="selectedCategory = cat.value"
          :color="selectedCategory === cat.value ? 'primary' : 'grey-2'"
          :text-color="selectedCategory === cat.value ? 'white' : 'grey-9'"
          size="sm"
        >
          {{ cat.label }}
        </q-chip>
      </div>

      <!-- Packages Table -->
      <q-table
        flat
        bordered
        dense
        :data="filteredPackages"
        :columns="columns"
        row-key="id"
        :pagination.sync="pagination"
      >
        <template v-slot:body-cell-code="props">
          <q-td :props="props" class="text-center">
            <q-chip
              dense
              color="primary"
              text-color="white"
              class="text-weight-bold cursor-pointer"
              @click="openPackageDetails(props.row)"
            >
              {{ props.value }}
              <q-tooltip>Клікніть для перегляду нормативного досьє</q-tooltip>
            </q-chip>
          </q-td>
        </template>

        <template v-slot:body-cell-category="props">
          <q-td :props="props">
            <q-badge :color="getCategoryColor(props.value)" :label="props.value" />
          </q-td>
        </template>

        <template v-slot:body-cell-base_rate="props">
          <q-td :props="props" class="text-right">
            <div v-if="props.value > 0" class="text-positive text-weight-bolder">
              {{ Number(props.value).toLocaleString('uk-UA', { minimumFractionDigits: 2 }) }} ₴
            </div>
            <div v-else class="text-grey-6 text-weight-bold">
              За формулою
            </div>
            <div class="text-caption text-grey-7" style="font-size: 10px;">
              {{ props.row.rate_period }}
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-actions="props">
          <q-td :props="props" class="text-center">
            <q-btn
              dense
              size="sm"
              color="primary"
              icon="info"
              label="Досьє"
              class="q-mr-xs"
              @click="openPackageDetails(props.row)"
            >
              <q-tooltip>Нормативна база, формули та валідації eHealth</q-tooltip>
            </q-btn>
            <q-btn
              dense
              size="sm"
              flat
              color="grey-8"
              icon="open_in_new"
              @click="openDossierPage(props.row.group_file, props.row.id)"
            >
              <q-tooltip>Відкрити автономне HTML-досьє</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- Dialog: Comprehensive Package Normative Dossier -->
    <q-dialog v-model="detailsDialog" maximized transition-show="slide-up" transition-hide="slide-down">
      <q-card class="bg-grey-1" v-if="selectedPackage">
        <q-toolbar class="bg-primary text-white">
          <q-icon name="menu_book" size="22px" class="q-mr-sm" />
          <q-toolbar-title class="text-subtitle1 text-weight-bold">
            Пакет {{ selectedPackage.id }} ({{ selectedPackage.code }}): {{ selectedPackage.name }}
          </q-toolbar-title>
          <q-btn flat round dense icon="close" v-close-popup />
        </q-toolbar>

        <q-card-section class="q-pa-md">
          <!-- Summary card -->
          <div class="row q-col-gutter-md q-mb-md">
            <div class="col-xs-12 col-md-8">
              <div class="bg-white q-pa-md rounded-borders shadow-1">
                <div class="row items-center q-gutter-sm q-mb-sm">
                  <q-badge color="primary" class="text-subtitle2 q-pa-xs">Пакет {{ selectedPackage.id }}</q-badge>
                  <q-badge :color="getCategoryColor(selectedPackage.category)">{{ selectedPackage.category }}</q-badge>
                  <q-badge color="teal">Модель: {{ selectedPackage.payment_model }}</q-badge>
                </div>
                <div class="text-h6 text-primary text-weight-bolder q-mb-xs">{{ selectedPackage.name }}</div>
                <div class="text-body2 text-grey-8">{{ selectedPackage.description }}</div>
              </div>
            </div>

            <div class="col-xs-12 col-md-4">
              <div class="bg-white q-pa-md rounded-borders shadow-1">
                <div class="text-caption text-uppercase text-grey-7 text-weight-bold">Базовий тариф 2026 року</div>
                <div class="text-h5 text-positive text-weight-bolder q-my-xs">
                  {{ selectedPackage.base_rate > 0 ? Number(selectedPackage.base_rate).toLocaleString('uk-UA', { minimumFractionDigits: 2 }) + ' ₴' : 'За калькуляцією' }}
                </div>
                <div class="text-caption text-grey-8 q-mb-sm">
                  Періодичність / Одиниця: <strong>{{ selectedPackage.rate_period }}</strong>
                </div>
                <div class="text-caption text-primary text-weight-bold">
                  Постанова КМУ № 1808 ({{ selectedPackage.chapter_cmu }})
                </div>
              </div>
            </div>
          </div>

          <!-- Formula & Calculation Box -->
          <div class="bg-white q-pa-md rounded-borders shadow-1 q-mb-md" style="border-left: 4px solid #00897b;">
            <div class="text-subtitle1 text-teal-9 text-weight-bold row items-center q-mb-xs">
              <q-icon name="functions" class="q-mr-xs" size="20px" />
              Офіційна формула розрахунку тарифу (Постанова КМУ № 1808)
            </div>
            <div class="bg-grey-2 q-pa-sm rounded-borders text-mono text-weight-bold text-teal-10 q-mb-sm" style="font-family: Consolas, monospace; font-size: 13px;">
              {{ selectedPackage.formula || 'Тариф розраховується згідно із фактичним обсягом медичних записів.' }}
            </div>

            <!-- Coefficients Table/Grid -->
            <div v-if="selectedPackage.coefficients && Object.keys(selectedPackage.coefficients).length > 0">
              <div class="text-caption text-weight-bold text-grey-9 q-mb-xs">Коригувальні коефіцієнти:</div>
              <div class="row q-col-gutter-xs">
                <div
                  class="col-xs-12 col-sm-6 col-md-4"
                  v-for="(val, k) in selectedPackage.coefficients"
                  :key="k"
                >
                  <div class="q-pa-xs bg-grey-1 rounded-borders border text-caption">
                    <strong>{{ k }}:</strong>
                    <span v-if="typeof val === 'object'">
                      <span v-for="(subV, subK) in val" :key="subK" class="q-ml-xs">
                        <q-badge color="grey-7" :label="subK + ': ' + subV" />
                      </span>
                    </span>
                    <span v-else class="text-primary text-weight-bold q-ml-xs">{{ val }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Two Column Requirements & Legal -->
          <div class="row q-col-gutter-md q-mb-md">
            <div class="col-xs-12 col-md-6">
              <div class="bg-white q-pa-md rounded-borders shadow-1 h-100" style="border-left: 4px solid #1976d2;">
                <div class="text-subtitle1 text-primary text-weight-bold row items-center q-mb-sm">
                  <q-icon name="fact_check" class="q-mr-xs" size="20px" />
                  Вимоги eHealth та валідація ЕМЗ
                </div>
                <q-list dense>
                  <q-item
                    v-for="(req, idx) in selectedPackage.ehealth_validations"
                    :key="idx"
                    class="q-px-none"
                  >
                    <q-item-section avatar min-width="24px">
                      <q-icon name="check_circle" color="positive" size="18px" />
                    </q-item-section>
                    <q-item-section class="text-caption text-grey-9">{{ req }}</q-item-section>
                  </q-item>
                </q-list>
              </div>
            </div>

            <div class="col-xs-12 col-md-6">
              <div class="bg-white q-pa-md rounded-borders shadow-1 h-100" style="border-left: 4px solid #c62828;">
                <div class="text-subtitle1 text-negative text-weight-bold row items-center q-mb-sm">
                  <q-icon name="gavel" class="q-mr-xs" size="20px" />
                  Нормативна база та накази МОЗ
                </div>
                <q-list dense>
                  <q-item
                    v-for="(law, idx) in selectedPackage.law_references"
                    :key="idx"
                    class="q-px-none"
                  >
                    <q-item-section avatar min-width="24px">
                      <q-icon name="gavel" color="primary" size="18px" />
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

          <!-- Direct Links to PDFs and HTML Dossiers -->
          <div class="row q-gutter-sm justify-center q-mt-md">
            <q-btn
              color="primary"
              icon="description"
              label="Відкрити нормативне досьє (HTML)"
              @click="openDossierPage(selectedPackage.group_file, selectedPackage.id)"
            />
            <q-btn
              outline
              color="primary"
              icon="picture_as_pdf"
              label="Постанова № 1808 (PDF)"
              @click="openExternal('/extracted_data/normative_docs/pmg-2026.pdf')"
            />
            <q-btn
              outline
              color="teal"
              icon="picture_as_pdf"
              label="Додаток 1: 465 ДСГ (PDF)"
              @click="openExternal('/extracted_data/normative_docs/Додаток-1.pdf')"
            />
            <q-btn
              outline
              color="indigo"
              icon="picture_as_pdf"
              label="Додаток 2: Хірургія 1-дня (PDF)"
              @click="openExternal('/extracted_data/normative_docs/Додаток-2.pdf')"
            />
          </div>
        </q-card-section>

        <q-separator />
        <q-card-actions align="right" class="bg-white">
          <q-btn flat label="Закрити" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
export default {
  name: 'PmgPackagesCatalog',
  data() {
    return {
      searchQuery: '',
      selectedCategory: 'ALL',
      packages: [],
      selectedPackage: null,
      detailsDialog: false,
      pagination: { rowsPerPage: 15 },
      categoryOptions: [
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
      quickCategories: [
        { label: 'Всі 46', value: 'ALL' },
        { label: 'ДСГ (3, 4, 47)', value: 'Спеціалізована та хірургічна допомога (ДСГ)' },
        { label: 'Пріоритетні (5, 6, 7, 8)', value: 'Пріоритетні стаціонарні пакети' },
        { label: 'Амбулаторія (9, 10..15)', value: 'Амбулаторна допомога та скринінги' },
        { label: 'Онкологія (18, 19, 26)', value: 'Онкологія та онкогематологія' },
        { label: 'Реабілітація (25, 53, 54)', value: 'Реабілітація' },
        { label: 'ВЛК та Оборона (40..58)', value: 'Оборонна готовність та ВЛК' }
      ],
      columns: [
        { name: 'code', label: 'Пакет', field: 'code', align: 'center', sortable: true },
        { name: 'name', label: 'Назва медичного пакета', field: 'name', align: 'left', sortable: true },
        { name: 'category', label: 'Категорія', field: 'category', align: 'left', sortable: true },
        { name: 'payment_model', label: 'Модель оплати', field: 'payment_model', align: 'center', sortable: true },
        { name: 'base_rate', label: 'Базовий тариф 2026', field: 'base_rate', align: 'right', sortable: true },
        { name: 'formula', label: 'Формула Постанови № 1808', field: 'formula', align: 'left' },
        { name: 'actions', label: 'Нормативка', field: 'id', align: 'center' }
      ]
    };
  },
  computed: {
    filteredPackages() {
      const q = (this.searchQuery || '').trim().toLowerCase();
      const cat = this.selectedCategory;
      return this.packages.filter(p => {
        if (cat !== 'ALL' && p.category !== cat) return false;
        if (q) {
          const match =
            String(p.id).includes(q) ||
            (p.code || '').toLowerCase().includes(q) ||
            (p.name || '').toLowerCase().includes(q) ||
            (p.description || '').toLowerCase().includes(q) ||
            (p.formula || '').toLowerCase().includes(q) ||
            (p.chapter_cmu || '').toLowerCase().includes(q);
          if (!match) return false;
        }
        return true;
      });
    }
  },
  methods: {
    getCategoryColor(cat) {
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

    openPackageDetails(pkg) {
      this.selectedPackage = pkg;
      this.detailsDialog = true;
    },

    openDossierPage(groupFile, pkgId) {
      const file = groupFile || 'index.html';
      const url = `/normative_packages/${file}#pkg-${pkgId || ''}`;
      window.open(url, '_blank');
    },

    openDossierPortal() {
      window.open('/normative_packages/index.html', '_blank');
    },

    openExternal(url) {
      window.open(url, '_blank');
    },

    exportPackages() {
      const jsonStr = JSON.stringify(this.packages, null, 2);
      const blob = new Blob([jsonStr], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'pmg_2026_all_46_packages.json';
      a.click();
      URL.revokeObjectURL(url);
    },

    async fetchPackages() {
      try {
        const res = await fetch('/api/v1/pmg/dictionaries/packages');
        if (res.ok) {
          this.packages = await res.json();
        } else if (window.PROTOTYPE_DATA && window.PROTOTYPE_DATA.packages) {
          this.packages = window.PROTOTYPE_DATA.packages;
        }
      } catch (err) {
        if (window.PROTOTYPE_DATA && window.PROTOTYPE_DATA.packages) {
          this.packages = window.PROTOTYPE_DATA.packages;
        }
      }
    }
  },
  mounted() {
    this.fetchPackages();
  }
};
</script>

<style scoped>
.text-mono {
  font-family: Consolas, Menlo, Monaco, monospace;
}
</style>
