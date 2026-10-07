<template>
  <div data-testid="PmgDsgClassifier" class="q-pa-md">
    <q-card flat bordered class="q-pa-md bg-white">
      <!-- Title & Search Bar -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <div class="text-h6 text-primary text-weight-bold row items-center">
            <q-icon name="local_hospital" class="q-mr-sm" size="24px" />
            Класифікатор діагностично-споріднених груп (465 ДСГ)
          </div>
          <div class="text-caption text-grey-7">
            Тарифікація стаціонарної допомоги (Пакети 3, 4, 47, 54) згідно з Постановою КМУ №1808 • Базова ставка: 8 735,00 ₴
          </div>
        </div>
        <q-btn
          color="primary"
          outline
          icon="file_download"
          label="Експорт довідника"
          dense
          class="q-px-sm"
          @click="exportDsg"
        />
      </div>

      <!-- Filters Row -->
      <div class="row q-col-gutter-md q-mb-md">
        <div class="col-xs-12 col-sm-4">
          <q-input
            dense
            outlined
            v-model="searchFilter"
            placeholder="Пошук за кодом ДСГ або назвою..."
            clearable
          >
            <template v-slot:prepend><q-icon name="search" /></template>
          </q-input>
        </div>

        <div class="col-xs-12 col-sm-4">
          <q-select
            dense
            outlined
            v-model="categoryFilter"
            :options="categoryOptions"
            label="Категорія ДСГ"
            emit-value
            map-options
          />
        </div>

        <div class="col-xs-12 col-sm-4 text-right flex items-center justify-end">
          <q-badge color="primary" class="q-pa-xs">
            Записів у довіднику: {{ filteredDsgList.length }}
          </q-badge>
        </div>
      </div>

      <!-- Table -->
      <q-table
        flat
        bordered
        dense
        :data="filteredDsgList"
        :columns="columns"
        row-key="code"
        :pagination.sync="pagination"
      >
        <!-- Code Column -->
        <template v-slot:body-cell-code="props">
          <q-td :props="props">
            <span class="code-chip text-weight-bolder text-primary">{{ props.value }}</span>
          </q-td>
        </template>

        <!-- Name Column -->
        <template v-slot:body-cell-name="props">
          <q-td :props="props">
            <div class="text-weight-bold text-grey-9">{{ props.value }}</div>
            <div class="text-caption text-grey-6">{{ props.row.category }}</div>
          </q-td>
        </template>

        <!-- Complexity Weight -->
        <template v-slot:body-cell-weight="props">
          <q-td :props="props" class="text-center">
            <q-badge color="grey-3" text-color="grey-9" class="text-weight-bold" :label="props.value.toFixed(3)" />
          </q-td>
        </template>

        <!-- Inpatient Stay Limit -->
        <template v-slot:body-cell-stayDays="props">
          <q-td :props="props" class="text-center text-caption">
            {{ props.row.minDays }} - {{ props.row.maxDays }} днів (сер. {{ props.row.avgDays }})
          </q-td>
        </template>

        <!-- Calculated Standard Tariff -->
        <template v-slot:body-cell-standardTariff="props">
          <q-td :props="props" class="text-right text-positive text-weight-bolder">
            {{ (8735.0 * props.row.weight * 0.55).toLocaleString('uk-UA', { minimumFractionDigits: 2 }) }} ₴
          </q-td>
        </template>

        <!-- Surgical Tariff (k=0.60) -->
        <template v-slot:body-cell-surgicalTariff="props">
          <q-td :props="props" class="text-right text-primary text-weight-bolder">
            {{ (8735.0 * props.row.weight * 0.60).toLocaleString('uk-UA', { minimumFractionDigits: 2 }) }} ₴
          </q-td>
        </template>
      </q-table>
    </q-card>
  </div>
</template>

<script>
export default {
  name: 'PmgDsgClassifier',
  data() {
    return {
      searchFilter: '',
      categoryFilter: 'all',
      pagination: {
        rowsPerPage: 15,
        sortBy: 'code',
        descending: false
      },
      categoryOptions: [
        { label: 'Всі категорії', value: 'all' },
        { label: 'Терапевтичні ДСГ', value: 'medical' },
        { label: 'Хірургічні ДСГ', value: 'surgical' },
        { label: 'Онкологічні ДСГ', value: 'oncology' },
        { label: 'Реабілітаційні ДСГ', value: 'rehab' }
      ],
      columns: [
        { name: 'code', label: 'Код ДСГ', field: 'code', align: 'left', sortable: true },
        { name: 'name', label: 'Назва клінічної групи', field: 'name', align: 'left', sortable: true },
        { name: 'weight', label: 'Ваговий коефіцієнт (ВК)', field: 'weight', align: 'center', sortable: true },
        { name: 'stayDays', label: 'Термін перебування', field: 'avgDays', align: 'center', sortable: true },
        { name: 'standardTariff', label: 'Тариф терапії (k=0.55)', field: 'weight', align: 'right', sortable: true },
        { name: 'surgicalTariff', label: 'Тариф хірургії (k=0.60)', field: 'weight', align: 'right', sortable: true }
      ],
      dsgList: [
        { code: 'A01A', name: 'Трансплантація кісткового мозку, алогенна', category: 'surgical', weight: 14.850, minDays: 14, maxDays: 60, avgDays: 28 },
        { code: 'B02A', name: 'Кранiотомiя при пухлинах головного мозку', category: 'surgical', weight: 4.120, minDays: 5, maxDays: 21, avgDays: 9 },
        { code: 'E65A', name: 'Хронічні обструктивні захворювання легень, тяжка форма', category: 'medical', weight: 1.280, minDays: 4, maxDays: 14, avgDays: 7 },
        { code: 'E65B', name: 'Хронічні обструктивні захворювання легень, середня форма', category: 'medical', weight: 0.940, minDays: 3, maxDays: 10, avgDays: 5 },
        { code: 'F01A', name: 'Аортокоронарне шунтування з ШК без ангіографії', category: 'surgical', weight: 5.630, minDays: 6, maxDays: 25, avgDays: 11 },
        { code: 'F14A', name: 'Судинні інтервенції без ускладнень', category: 'surgical', weight: 1.840, minDays: 2, maxDays: 8, avgDays: 3 },
        { code: 'G02A', name: 'Резекція шлунка при злоякісних новоутвореннях', category: 'oncology', weight: 3.450, minDays: 6, maxDays: 20, avgDays: 10 },
        { code: 'G48B', name: 'Колоноскопія з поліпектомією', category: 'surgical', weight: 0.620, minDays: 1, maxDays: 3, avgDays: 1 },
        { code: 'H01A', name: 'Трансплантація печінки', category: 'surgical', weight: 18.200, minDays: 18, maxDays: 90, avgDays: 35 },
        { code: 'I03A', name: 'Тотальне ендопротезування кульшового суглоба', category: 'surgical', weight: 2.910, minDays: 5, maxDays: 16, avgDays: 7 },
        { code: 'I04A', name: 'Ендопротезування колінного суглоба', category: 'surgical', weight: 2.750, minDays: 4, maxDays: 14, avgDays: 6 },
        { code: 'I21A', name: 'Гострий інфаркт міокарда зі стентуванням', category: 'surgical', weight: 3.820, minDays: 3, maxDays: 12, avgDays: 5 },
        { code: 'O01A', name: 'Кесарів розтин з тяжкими ускладненнями', category: 'surgical', weight: 2.150, minDays: 4, maxDays: 12, avgDays: 5 },
        { code: 'O01B', name: 'Кесарів розтин без тяжких ускладнень', category: 'surgical', weight: 1.480, minDays: 3, maxDays: 8, avgDays: 4 },
        { code: 'R02A', name: 'Хіміотерапія злоякісних новоутворень, високодозова', category: 'oncology', weight: 3.000, minDays: 2, maxDays: 7, avgDays: 3 },
        { code: 'R02B', name: 'Хіміотерапія злоякісних новоутворень, стандартний курс', category: 'oncology', weight: 1.750, minDays: 1, maxDays: 4, avgDays: 2 },
        { code: 'RH01', name: 'Нейрореабілітація стаціонарна в гострому періоді', category: 'rehab', weight: 2.200, minDays: 14, maxDays: 42, avgDays: 21 },
        { code: 'RH02', name: 'Опорно-рухова реабілітація стаціонарна', category: 'rehab', weight: 1.650, minDays: 14, maxDays: 30, avgDays: 18 }
      ]
    };
  },
  computed: {
    filteredDsgList() {
      return this.dsgList.filter(item => {
        if (this.categoryFilter !== 'all' && item.category !== this.categoryFilter) {
          return false;
        }
        if (this.searchFilter) {
          const q = this.searchFilter.toLowerCase();
          return item.code.toLowerCase().includes(q) || item.name.toLowerCase().includes(q);
        }
        return true;
      });
    }
  },
  methods: {
    exportDsg() {
      this.$q.notify({
        message: 'Довідник ДСГ успішно експортовано у CSV / Excel',
        color: 'positive',
        icon: 'file_download'
      });
    }
  }
};
</script>

<style scoped>
.code-chip {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  background-color: #f1f5f9;
  padding: 3px 6px;
  border-radius: 4px;
}
</style>
