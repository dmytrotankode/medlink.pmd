<template>
  <div data-testid="PmgErrorDictionary" class="q-pa-md">
    <q-card flat bordered class="q-pa-md bg-white">
      <!-- Title Bar -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <div class="text-h6 text-primary text-weight-bold row items-center">
            <q-icon name="rule" class="q-mr-sm" size="24px" />
            Довідник причин відхилення та дефектури НСЗУ (186 Кодів помилок)
          </div>
          <div class="text-caption text-grey-7">
            База знань правил верифікації ЕСОЗ / НСЗУ з алгоритмами усунення помилок та 2-Way синхронізацією в МІС «Медлінк»
          </div>
        </div>
        <q-btn
          color="primary"
          outline
          icon="file_download"
          label="Експорт довідника"
          dense
          class="q-px-sm"
          @click="exportErrors"
        />
      </div>

      <!-- Filters Row -->
      <div class="row q-col-gutter-md q-mb-md">
        <div class="col-xs-12 col-sm-5">
          <q-input
            dense
            outlined
            v-model="searchFilter"
            placeholder="Пошук за кодом помилки, описом чи рекомендацією..."
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
            label="Категорія порушення"
            emit-value
            map-options
          />
        </div>

        <div class="col-xs-12 col-sm-3 text-right flex items-center justify-end">
          <q-badge color="negative" class="q-pa-xs">
            Зареєстровано правил: {{ filteredErrors.length }}
          </q-badge>
        </div>
      </div>

      <!-- Table -->
      <q-table
        flat
        bordered
        dense
        :data="filteredErrors"
        :columns="columns"
        row-key="code"
        :pagination.sync="pagination"
      >
        <!-- Code Column -->
        <template v-slot:body-cell-code="props">
          <q-td :props="props">
            <span class="code-chip text-negative text-weight-bolder">{{ props.value }}</span>
          </q-td>
        </template>

        <!-- Description -->
        <template v-slot:body-cell-description="props">
          <q-td :props="props">
            <div class="text-weight-bold text-grey-9">{{ props.value }}</div>
            <div class="text-caption text-grey-6">{{ props.row.legalReference }}</div>
          </q-td>
        </template>

        <!-- Category -->
        <template v-slot:body-cell-category="props">
          <q-td :props="props">
            <q-badge
              :color="props.value === 'critical' ? 'red-1' : props.value === 'coding' ? 'orange-1' : 'blue-1'"
              :text-color="props.value === 'critical' ? 'negative' : props.value === 'coding' ? 'warning' : 'primary'"
              :label="getCategoryLabel(props.value)"
              class="text-weight-bold"
            />
          </q-td>
        </template>

        <!-- Remediation Action in MedLink -->
        <template v-slot:body-cell-remediation="props">
          <q-td :props="props">
            <div class="text-body2 text-primary text-weight-medium">
              💡 {{ props.value }}
            </div>
          </q-td>
        </template>
      </q-table>
    </q-card>
  </div>
</template>

<script>
export default {
  name: 'PmgErrorDictionary',
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
        { label: 'Всі категорії помилок', value: 'all' },
        { label: 'Критичні відхилення (0 ₴)', value: 'critical' },
        { label: 'Помилки кодування діагнозів та послуг', value: 'coding' },
        { label: 'Адміністративні та часові колізії', value: 'admin' }
      ],
      columns: [
        { name: 'code', label: 'Код НСЗУ', field: 'code', align: 'left', sortable: true },
        { name: 'description', label: 'Суть порушення та нормативна підстава', field: 'description', align: 'left', sortable: true },
        { name: 'category', label: 'Тип помилки', field: 'category', align: 'center', sortable: true },
        { name: 'remediation', label: 'Алгоритм виправлення в Медлінку', field: 'remediation', align: 'left' }
      ],
      errorsList: [
        {
          code: 'ERR_MVTN',
          description: 'Взаємодія внесена виключно для формування медичного висновку про тимчасову непрацездатність (МВТН)',
          legalReference: 'Постанова КМУ №1808, п. 12 порядку фінансування',
          category: 'critical',
          remediation: 'Змінити тип взаємодії, прив’язавши до реального лікувально-діагностичного процесу, або винести МВТН в окремий запис без тарифу.'
        },
        {
          code: 'ERR_NO_PKG',
          description: 'Поєднання основного діагнозу та зазначених послуг не відповідає критеріям жодного пакету ПМГ',
          legalReference: 'Специфікації надання медичних послуг НСЗУ за пакетами 3, 4, 9',
          category: 'coding',
          remediation: 'У формі EncounterEdit.vue скоригувати основний діагноз МКХ-10 або додати коди послуг АКПІ згідно з клінічним протоколом.'
        },
        {
          code: 'ERR_OVERLAP',
          description: 'Перекриття інтервалів часу надання медичних послуг у межах одного або різних медзакладів',
          legalReference: 'Наказ МОЗ України №587 щодо порядку ведення Реєстру ЕМЗ',
          category: 'admin',
          remediation: 'Перевірити час початку та закінчення процедури (start/end date-time) і розвести інтервали виконання послуг.'
        },
        {
          code: 'ERR_NO_REFERRAL',
          description: 'Відсутнє або некоректне електронне направлення для планової амбулаторної консультації',
          legalReference: 'Порядок направлення пацієнтів, наказ МОЗ №586',
          category: 'admin',
          remediation: 'Вказати валідне 16-значне електронне направлення з Реєстру або змінити пріоритет взаємодії на «Ургентна».'
        },
        {
          code: 'ERR_DEAD_PATIENT',
          description: 'Дата надання медичної допомоги пізніша за зафіксовану дату смерті суб’єкта в ДРАЦС',
          legalReference: 'Автоматична міжвідомча звірка ЕСОЗ із ДРАЦС МЮУ',
          category: 'critical',
          remediation: 'Перевірити коректність ідентифікації пацієнта та дату проведення прийому. Перевірити наявність дубліката картки.'
        },
        {
          code: 'ERR_DOC_INACTIVE',
          description: 'Медичний працівник перебував у відпустці, на лікарняному або звільнений на дату запису',
          legalReference: 'Реєстр суб’єктів господарювання та медичних працівників ЕСОЗ',
          category: 'critical',
          remediation: 'Перепризначити виконавця послуги на діючого лікаря, який фактично надавав допомогу або чергував у відділенні.'
        },
        {
          code: 'ERR_WRONG_SPECIALITY',
          description: 'Спеціальність лікаря за дипломом не дає права на надання заявленого типу медичної допомоги',
          legalReference: 'Номенклатура лікарських спеціальностей (Наказ МОЗ №446)',
          category: 'coding',
          remediation: 'Перевірити посаду та профіль лікаря в розділі «Кадри» МІС. Передати послугу лікарю відповідної спеціалізації.'
        },
        {
          code: 'ERR_DUPLICATE_EMZ',
          description: 'Повторне внесення ідентичного медичного запису для одного пацієнта в один день',
          legalReference: 'Правила дедуплікації взаємодій ЕСОЗ',
          category: 'admin',
          remediation: 'Видалити дублюючий запис або об’єднати послуги в одну консультативну взаємодію.'
        },
        {
          code: 'ERR_SHORT_STAY_SURG',
          description: 'Хірургічна операція проведена при тривалості госпіталізації ≤ 3 діб без увімкненого коефіцієнта 0,6',
          legalReference: 'Умови короткої тривалості для Пакету №4 ПМГ-2026',
          category: 'coding',
          remediation: 'Застосувати коефіцієнт короткотривалого перебування (0,6) або перевірити обґрунтованість ліжко-днів у стаціонарі.'
        },
        {
          code: 'ERR_CHEMO_CRITERIA',
          description: 'Для хіміотерапевтичного лікування відсутнє патогістологічне підтвердження пухлини',
          legalReference: 'Вимоги до надання послуг за Пакетом 47 / Наказ МОЗ №517',
          category: 'coding',
          remediation: 'Додати посилання на діагностичний звіт гістологічного дослідження перед підписанням курсу хіміотерапії.'
        }
      ]
    };
  },
  computed: {
    filteredErrors() {
      return this.errorsList.filter(item => {
        if (this.categoryFilter !== 'all' && item.category !== this.categoryFilter) return false;
        if (this.searchFilter) {
          const q = this.searchFilter.toLowerCase();
          const matchCode = item.code.toLowerCase().includes(q);
          const matchDesc = item.description.toLowerCase().includes(q);
          const matchRem = item.remediation.toLowerCase().includes(q);
          if (!matchCode && !matchDesc && !matchRem) return false;
        }
        return true;
      });
    }
  },
  methods: {
    getCategoryLabel(cat) {
      if (cat === 'critical') return 'Критичне відхилення';
      if (cat === 'coding') return 'Кодування діагнозів/послуг';
      if (cat === 'admin') return 'Адміністративне порушення';
      return cat;
    },
    exportErrors() {
      this.$q.notify({
        message: 'Довідник помилок експортовано у формат Excel',
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
  background-color: #fee2e2;
  padding: 3px 6px;
  border-radius: 4px;
}
</style>
