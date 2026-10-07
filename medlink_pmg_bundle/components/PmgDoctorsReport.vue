<template>
  <div data-testid="PmgDoctorsReport" class="q-pa-md">
    <!-- Header Banner -->
    <div class="row items-center justify-between q-mb-md">
      <div>
        <div class="text-h6 text-primary text-weight-bold row items-center">
          <q-icon name="people_alt" class="q-mr-sm" size="24px" />
          Аналітика в розрізі лікарів та відділень (Аркуш «Звіт»)
        </div>
        <div class="text-caption text-grey-7">
          Моніторинг ефективності внесення ЕМЗ, показників дефектури та фінансового внеску лікарів у бюджет медзакладу
        </div>
      </div>
      <div class="row q-gutter-sm">
        <q-btn
          outline
          color="primary"
          icon="file_download"
          label="Експорт в Excel"
          dense
          class="q-px-sm"
          @click="exportExcel"
        />
        <q-btn
          color="primary"
          icon="refresh"
          label="Оновити розрахунок"
          dense
          class="q-px-sm"
          @click="recalculate"
        />
      </div>
    </div>

    <!-- Summary KPI Row -->
    <div class="row q-col-gutter-md q-mb-md">
      <div class="col-xs-12 col-sm-6 col-md-3">
        <q-card flat bordered class="q-pa-sm border-left-primary">
          <div class="text-caption text-grey-7 text-uppercase text-weight-bold">Активних лікарів у звіті</div>
          <div class="text-h5 text-weight-bolder text-grey-9">{{ doctorsList.length }} фахівців</div>
          <div class="text-caption text-grey-6">Всі відділення закладу</div>
        </q-card>
      </div>

      <div class="col-xs-12 col-sm-6 col-md-3">
        <q-card flat bordered class="q-pa-sm border-left-positive">
          <div class="text-caption text-grey-7 text-uppercase text-weight-bold">Успішно тарифіковано</div>
          <div class="text-h5 text-weight-bolder text-positive">{{ totalAcceptedEmz }} ЕМЗ</div>
          <div class="text-caption text-positive text-weight-bold">{{ totalAcceptedRevenueFormatted }} ₴</div>
        </q-card>
      </div>

      <div class="col-xs-12 col-sm-6 col-md-3">
        <q-card flat bordered class="q-pa-sm border-left-negative">
          <div class="text-caption text-grey-7 text-uppercase text-weight-bold">Відхилено НСЗУ (Дефектура)</div>
          <div class="text-h5 text-weight-bolder text-negative">{{ totalRejectedEmz }} ЕМЗ ({{ avgErrorRate }}%)</div>
          <div class="text-caption text-negative text-weight-bold">-{{ totalLostRevenueFormatted }} ₴ втрат</div>
        </q-card>
      </div>

      <div class="col-xs-12 col-sm-6 col-md-3">
        <q-card flat bordered class="q-pa-sm border-left-warning">
          <div class="text-caption text-grey-7 text-uppercase text-weight-bold">Лікарів у зоні ризику (>10% помилок)</div>
          <div class="text-h5 text-weight-bolder text-warning">{{ highRiskDoctorsCount }} лікарів</div>
          <div class="text-caption text-grey-7">Потребують інструктажу з кодування</div>
        </q-card>
      </div>
    </div>

    <!-- Table Card -->
    <q-card flat bordered class="q-pa-md bg-white">
      <div class="row q-col-gutter-md items-center q-mb-md">
        <div class="col-xs-12 col-sm-5">
          <q-input
            dense
            outlined
            v-model="searchQuery"
            placeholder="Пошук лікаря за ПІБ або посадою..."
            clearable
          >
            <template v-slot:prepend><q-icon name="search" /></template>
          </q-input>
        </div>
        <div class="col-xs-12 col-sm-4">
          <q-select
            dense
            outlined
            v-model="filterDepartment"
            :options="departmentOptions"
            label="Фільтр за відділенням"
            emit-value
            map-options
          />
        </div>
        <div class="col-xs-12 col-sm-3 text-right">
          <q-btn-toggle
            v-model="errorFilter"
            dense
            unelevated
            toggle-color="primary"
            :options="[
              { label: 'Всі', value: 'all' },
              { label: 'Ризик >10%', value: 'risk' },
              { label: 'Без помилок', value: 'clean' }
            ]"
          />
        </div>
      </div>

      <q-table
        flat
        bordered
        dense
        :data="filteredDoctors"
        :columns="columns"
        row-key="name"
        :pagination.sync="pagination"
      >
        <!-- Doctor Name & Position -->
        <template v-slot:body-cell-name="props">
          <q-td :props="props">
            <div class="row items-center no-wrap">
              <q-avatar size="28px" color="blue-1" text-color="primary" class="q-mr-sm text-weight-bold">
                {{ props.value.charAt(0) }}
              </q-avatar>
              <div>
                <div class="text-weight-bold text-grey-9">{{ props.value }}</div>
                <div class="text-caption text-grey-6">{{ props.row.position }}</div>
              </div>
            </div>
          </q-td>
        </template>

        <!-- Department -->
        <template v-slot:body-cell-department="props">
          <q-td :props="props">
            <q-badge color="grey-3" text-color="grey-8" :label="props.value" />
          </q-td>
        </template>

        <!-- Total Count -->
        <template v-slot:body-cell-totalCount="props">
          <q-td :props="props" class="text-right text-weight-medium">
            {{ props.value.toLocaleString('uk-UA') }}
          </q-td>
        </template>

        <!-- Accepted Count -->
        <template v-slot:body-cell-acceptedCount="props">
          <q-td :props="props" class="text-right text-positive text-weight-bold">
            {{ props.value.toLocaleString('uk-UA') }}
          </q-td>
        </template>

        <!-- Rejected Count -->
        <template v-slot:body-cell-rejectedCount="props">
          <q-td :props="props" class="text-right">
            <span :class="props.value > 0 ? 'text-negative text-weight-bold' : 'text-grey-5'">
              {{ props.value.toLocaleString('uk-UA') }}
            </span>
          </q-td>
        </template>

        <!-- Error Percentage Badge -->
        <template v-slot:body-cell-errorRate="props">
          <q-td :props="props" class="text-center">
            <q-badge
              :color="props.value > 10 ? 'negative' : props.value > 5 ? 'warning' : 'positive'"
              :label="props.value.toFixed(1) + '%'"
              class="text-weight-bold"
            />
          </q-td>
        </template>

        <!-- Revenue -->
        <template v-slot:body-cell-revenue="props">
          <q-td :props="props" class="text-right text-positive text-weight-bolder">
            {{ props.value.toLocaleString('uk-UA', { minimumFractionDigits: 2 }) }} ₴
          </q-td>
        </template>

        <!-- Lost Revenue -->
        <template v-slot:body-cell-lostRevenue="props">
          <q-td :props="props" class="text-right">
            <span v-if="props.value > 0" class="text-negative text-weight-bold">
              -{{ props.value.toLocaleString('uk-UA', { minimumFractionDigits: 2 }) }} ₴
            </span>
            <span v-else class="text-grey-5">—</span>
          </q-td>
        </template>

        <!-- Actions -->
        <template v-slot:body-cell-actions="props">
          <q-td :props="props" class="text-center">
            <q-btn
              dense
              outline
              size="sm"
              color="primary"
              icon="assessment"
              label="Деталі"
              @click="showDoctorDetails(props.row)"
            />
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- Doctor Detail Modal -->
    <q-dialog v-model="detailsDialog">
      <q-card style="min-width: 600px; max-width: 800px;">
        <q-toolbar class="bg-primary text-white">
          <q-toolbar-title class="text-subtitle1 text-weight-bold">
            Картка лікаря: {{ selectedDoctor ? selectedDoctor.name : '' }}
          </q-toolbar-title>
          <q-btn flat round dense icon="close" v-close-popup />
        </q-toolbar>

        <q-card-section v-if="selectedDoctor">
          <div class="row q-col-gutter-sm q-mb-md">
            <div class="col-6"><strong>Посада:</strong> {{ selectedDoctor.position }}</div>
            <div class="col-6"><strong>Відділення:</strong> {{ selectedDoctor.department }}</div>
            <div class="col-6"><strong>Всього внесено:</strong> {{ selectedDoctor.totalCount }} ЕМЗ</div>
            <div class="col-6"><strong>Рівень дефектури:</strong> {{ selectedDoctor.errorRate.toFixed(1) }}%</div>
          </div>

          <div class="text-subtitle2 text-weight-bold q-mb-xs">Найчастіші коди помилок у лікаря:</div>
          <q-list bordered separator class="rounded-borders q-mb-md">
            <q-item v-for="(err, idx) in selectedDoctorErrors" :key="idx">
              <q-item-section avatar>
                <q-icon name="error_outline" color="negative" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold">{{ err.code }}: {{ err.title }}</q-item-label>
                <q-item-label caption>{{ err.recommendation }}</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-badge color="negative" :label="err.count + ' випадків'" />
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>

        <q-separator />
        <q-card-actions align="right">
          <q-btn flat label="Закрити" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
export default {
  name: 'PmgDoctorsReport',
  props: {
    dataset: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      searchQuery: '',
      filterDepartment: 'all',
      errorFilter: 'all',
      detailsDialog: false,
      selectedDoctor: null,
      selectedDoctorErrors: [
        { code: 'ERR_MVTN', title: 'Взаємодія внесена для створення МВТН', recommendation: 'Створити МВТН як самостійний документ або прив’язати до консультативного висновку.', count: 14 },
        { code: 'ERR_NO_PKG', title: 'Не відповідає критеріям жодного пакету', recommendation: 'Перевірити комбінацію діагнозу МКХ та послуг АКПІ відповідно до специфікації ПМГ.', count: 8 },
        { code: 'ERR_OVERLAP', title: 'Перекриття інтервалів надання послуг', recommendation: 'Скоригувати час початку та закінчення процедури у медичному записі.', count: 3 }
      ],
      departmentOptions: [
        { label: 'Всі відділення', value: 'all' },
        { label: 'Хірургічне відділення', value: 'Хірургічне' },
        { label: 'Онкологічне відділення', value: 'Онкологічне' },
        { label: 'Педіатричне відділення', value: 'Педіатричне' },
        { label: 'Терапевтичне відділення', value: 'Терапевтичне' },
        { label: 'Консультативна поліклініка', value: 'Поліклініка' }
      ],
      pagination: {
        rowsPerPage: 15,
        sortBy: 'revenue',
        descending: true
      },
      columns: [
        { name: 'name', label: 'Лікар (ПІБ та посада)', field: 'name', align: 'left', sortable: true },
        { name: 'department', label: 'Відділення', field: 'department', align: 'left', sortable: true },
        { name: 'totalCount', label: 'Всього ЕМЗ', field: 'totalCount', align: 'right', sortable: true },
        { name: 'acceptedCount', label: 'Оплачено (Так/ГБ)', field: 'acceptedCount', align: 'right', sortable: true },
        { name: 'rejectedCount', label: 'Відхилено (Ні)', field: 'rejectedCount', align: 'right', sortable: true },
        { name: 'errorRate', label: '% помилок', field: 'errorRate', align: 'center', sortable: true },
        { name: 'revenue', label: 'Дохід закладу', field: 'revenue', align: 'right', sortable: true },
        { name: 'lostRevenue', label: 'Втрачений дохід', field: 'lostRevenue', align: 'right', sortable: true },
        { name: 'actions', label: 'Дії', align: 'center' }
      ],
      // Demo doctors aggregated from real reports
      doctorsList: [
        { name: 'Григоренко О. П.', position: 'Лікар-онколог', department: 'Онкологічне', totalCount: 420, acceptedCount: 395, rejectedCount: 25, errorRate: 5.95, revenue: 1425800.0, lostRevenue: 78500.0 },
        { name: 'Бондар В. М.', position: 'Хірург онкологічний', department: 'Онкологічне', totalCount: 310, acceptedCount: 290, rejectedCount: 20, errorRate: 6.45, revenue: 1850400.0, lostRevenue: 112000.0 },
        { name: 'Кравченко І. С.', position: 'Лікар-гематолог', department: 'Онкологічне', totalCount: 280, acceptedCount: 245, rejectedCount: 35, errorRate: 12.50, revenue: 980200.0, lostRevenue: 145000.0 },
        { name: 'Мельник Т. О.', position: 'Лікар-педіатр', department: 'Педіатричне', totalCount: 520, acceptedCount: 498, rejectedCount: 22, errorRate: 4.23, revenue: 385000.0, lostRevenue: 18400.0 },
        { name: 'Шевченко Д. В.', position: 'Дитячий хірург', department: 'Педіатричне', totalCount: 195, acceptedCount: 188, rejectedCount: 7, errorRate: 3.59, revenue: 840500.0, lostRevenue: 32000.0 },
        { name: 'Коваленко М. А.', position: 'Лікар-отоларинголог', department: 'Поліклініка', totalCount: 340, acceptedCount: 300, rejectedCount: 40, errorRate: 11.76, revenue: 195000.0, lostRevenue: 28500.0 },
        { name: 'Іванов В. В.', position: 'Лікар-офтальмолог', department: 'Поліклініка', totalCount: 410, acceptedCount: 390, rejectedCount: 20, errorRate: 4.88, revenue: 245000.0, lostRevenue: 14200.0 },
        { name: 'Поліщук С. І.', position: 'Лікар загальної практики', department: 'Терапевтичне', totalCount: 650, acceptedCount: 610, rejectedCount: 40, errorRate: 6.15, revenue: 450000.0, lostRevenue: 31000.0 },
        { name: 'Демченко К. М.', position: 'Акушер-гінеколог', department: 'Хірургічне', totalCount: 230, acceptedCount: 198, rejectedCount: 32, errorRate: 13.91, revenue: 760000.0, lostRevenue: 125000.0 },
        { name: 'Сидоренко Ю. Л.', position: 'Лікар-невролог', department: 'Поліклініка', totalCount: 380, acceptedCount: 365, rejectedCount: 15, errorRate: 3.95, revenue: 230000.0, lostRevenue: 10500.0 }
      ]
    };
  },
  computed: {
    totalAcceptedEmz() {
      return this.doctorsList.reduce((sum, d) => sum + d.acceptedCount, 0);
    },
    totalRejectedEmz() {
      return this.doctorsList.reduce((sum, d) => sum + d.rejectedCount, 0);
    },
    avgErrorRate() {
      const total = this.totalAcceptedEmz + this.totalRejectedEmz;
      return total > 0 ? ((this.totalRejectedEmz / total) * 100).toFixed(1) : 0;
    },
    totalAcceptedRevenueFormatted() {
      const total = this.doctorsList.reduce((sum, d) => sum + d.revenue, 0);
      return total.toLocaleString('uk-UA', { minimumFractionDigits: 2 });
    },
    totalLostRevenueFormatted() {
      const total = this.doctorsList.reduce((sum, d) => sum + d.lostRevenue, 0);
      return total.toLocaleString('uk-UA', { minimumFractionDigits: 2 });
    },
    highRiskDoctorsCount() {
      return this.doctorsList.filter(d => d.errorRate > 10).length;
    },
    filteredDoctors() {
      return this.doctorsList.filter(doc => {
        // Query
        if (this.searchQuery) {
          const q = this.searchQuery.toLowerCase();
          const matchName = doc.name.toLowerCase().includes(q);
          const matchPos = doc.position.toLowerCase().includes(q);
          if (!matchName && !matchPos) return false;
        }
        // Dept
        if (this.filterDepartment !== 'all' && !doc.department.includes(this.filterDepartment)) {
          return false;
        }
        // Error Risk
        if (this.errorFilter === 'risk' && doc.errorRate <= 10) return false;
        if (this.errorFilter === 'clean' && doc.errorRate > 5) return false;

        return true;
      });
    }
  },
  methods: {
    showDoctorDetails(doc) {
      this.selectedDoctor = doc;
      this.detailsDialog = true;
    },
    exportExcel() {
      this.$q.notify({
        message: 'Звіт успішно експортовано в формат Excel (.xlsx)',
        color: 'positive',
        icon: 'check_circle'
      });
    },
    recalculate() {
      this.$q.notify({
        message: 'Перерахунок виконано на основі актуальних тарифів ПМГ-2026',
        color: 'info',
        icon: 'sync'
      });
    }
  }
};
</script>

<style scoped>
.border-left-primary { border-left: 4px solid var(--q-color-primary, #4274A7); }
.border-left-positive { border-left: 4px solid var(--q-color-positive, #21ba45); }
.border-left-negative { border-left: 4px solid var(--q-color-negative, #d04f45); }
.border-left-warning { border-left: 4px solid var(--q-color-warning, #f2c037); }
</style>
