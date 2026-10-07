<template>
  <div data-testid="PmgOutpatientClasses" class="q-pa-md">
    <q-card flat bordered class="q-pa-md bg-white">
      <!-- Title Bar -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <div class="text-h6 text-primary text-weight-bold row items-center">
            <q-icon name="medical_services" class="q-mr-sm" size="24px" />
            Класифікатор амбулаторних медичних послуг (148 Класів — Пакет 9)
          </div>
          <div class="text-caption text-grey-7">
            Тарифікація амбулаторної спеціалізованої допомоги за Постановою КМУ №1808 • Базова ставка класу: 155,00 ₴
          </div>
        </div>
        <q-btn
          color="primary"
          outline
          icon="file_download"
          label="Експорт класифікатора"
          dense
          class="q-px-sm"
          @click="exportClasses"
        />
      </div>

      <!-- Filters -->
      <div class="row q-col-gutter-md q-mb-md">
        <div class="col-xs-12 col-sm-6">
          <q-input
            dense
            outlined
            v-model="searchFilter"
            placeholder="Пошук за номером класу, назвою або кодом послуги АКПІ..."
            clearable
          >
            <template v-slot:prepend><q-icon name="search" /></template>
          </q-input>
        </div>

        <div class="col-xs-12 col-sm-3">
          <q-select
            dense
            outlined
            v-model="typeFilter"
            :options="typeOptions"
            label="Тип втручання"
            emit-value
            map-options
          />
        </div>

        <div class="col-xs-12 col-sm-3 text-right flex items-center justify-end">
          <q-badge color="accent" class="q-pa-xs">
            Всього класів: {{ filteredClasses.length }}
          </q-badge>
        </div>
      </div>

      <!-- Table -->
      <q-table
        flat
        bordered
        dense
        :data="filteredClasses"
        :columns="columns"
        row-key="classNumber"
        :pagination.sync="pagination"
      >
        <!-- Class Number -->
        <template v-slot:body-cell-classNumber="props">
          <q-td :props="props">
            <span class="code-chip text-weight-bolder text-primary">Клас {{ props.value }}</span>
          </q-td>
        </template>

        <!-- Name & Typical Services -->
        <template v-slot:body-cell-name="props">
          <q-td :props="props">
            <div class="text-weight-bold text-grey-9">{{ props.value }}</div>
            <div class="text-caption text-grey-6">АКПІ: {{ props.row.servicesSample }}</div>
          </q-td>
        </template>

        <!-- Weight Coeff -->
        <template v-slot:body-cell-weight="props">
          <q-td :props="props" class="text-center">
            <q-badge color="blue-1" text-color="primary" class="text-weight-bold" :label="props.value.toFixed(2)" />
          </q-td>
        </template>

        <!-- Calculated Tariff -->
        <template v-slot:body-cell-tariff="props">
          <q-td :props="props" class="text-right text-positive text-weight-bolder">
            {{ (155.0 * props.row.weight).toLocaleString('uk-UA', { minimumFractionDigits: 2 }) }} ₴
          </q-td>
        </template>
      </q-table>
    </q-card>
  </div>
</template>

<script>
export default {
  name: 'PmgOutpatientClasses',
  data() {
    return {
      searchFilter: '',
      typeFilter: 'all',
      pagination: {
        rowsPerPage: 15,
        sortBy: 'classNumber',
        descending: false
      },
      typeOptions: [
        { label: 'Всі категорії', value: 'all' },
        { label: 'Консультативні прийоми', value: 'consult' },
        { label: 'Діагностичні процедури', value: 'diag' },
        { label: 'Амбулаторні операції', value: 'surgery' }
      ],
      columns: [
        { name: 'classNumber', label: 'Номер класу', field: 'classNumber', align: 'left', sortable: true },
        { name: 'name', label: 'Найменування медичного класу', field: 'name', align: 'left', sortable: true },
        { name: 'weight', label: 'Коефіцієнт (К)', field: 'weight', align: 'center', sortable: true },
        { name: 'tariff', label: 'Вартість випадку (155 ₴ × К)', field: 'weight', align: 'right', sortable: true }
      ],
      classesList: [
        { classNumber: 1, name: 'Консультація лікаря-спеціаліста загальна', type: 'consult', weight: 1.00, servicesSample: '11000-00, 11000-01' },
        { classNumber: 2, name: 'Консультація дитячого спеціаліста', type: 'consult', weight: 1.15, servicesSample: '11005-00, 11005-02' },
        { classNumber: 12, name: 'Ендоскопічне дослідження верхніх відділів ШКТ', type: 'diag', weight: 4.80, servicesSample: '30473-00, 30478-00' },
        { classNumber: 15, name: 'Колоноскопія діагностична амбулаторна', type: 'diag', weight: 6.20, servicesSample: '32090-00, 32090-01' },
        { classNumber: 21, name: 'Малі амбулаторні хірургічні втручання на шкірі', type: 'surgery', weight: 2.45, servicesSample: '30003-00, 30023-00' },
        { classNumber: 25, name: 'Офтальмологічні маніпуляції та лазерні процедури', type: 'surgery', weight: 3.10, servicesSample: '42702-00, 42740-00' },
        { classNumber: 30, name: 'Отоларингологічні амбулаторні процедури', type: 'surgery', weight: 2.20, servicesSample: '41653-00, 41656-00' },
        { classNumber: 42, name: 'Ультразвукова діагностика експертного класу', type: 'diag', weight: 1.85, servicesSample: '55036-00, 55048-00' },
        { classNumber: 55, name: 'Рентгенографічні дослідження кістково-суглобової системи', type: 'diag', weight: 1.60, servicesSample: '57700-00, 57706-00' },
        { classNumber: 68, name: 'Комп’ютерна томографія без внутрішньовенного контрастування', type: 'diag', weight: 5.50, servicesSample: '56001-00, 56007-00' },
        { classNumber: 70, name: 'Комп’ютерна томографія з контрастним підсиленням', type: 'diag', weight: 9.80, servicesSample: '56010-00, 56013-00' },
        { classNumber: 82, name: 'Магнітно-резонансна томографія одного анатомічного регіону', type: 'diag', weight: 8.90, servicesSample: '63328-00, 63334-00' },
        { classNumber: 95, name: 'Кардіологічні навантажувальні тести (тредміл, холтер)', type: 'diag', weight: 2.75, servicesSample: '11700-00, 11712-00' },
        { classNumber: 110, name: 'Цитологічні та патогістологічні біопсійні дослідження', type: 'diag', weight: 3.40, servicesSample: '73045-00, 73050-00' },
        { classNumber: 125, name: 'Амбулаторні фізіотерапевтичні та відновлювальні цикли', type: 'consult', weight: 1.45, servicesSample: '93000-00, 93005-00' },
        { classNumber: 148, name: 'Специфічні високоспеціалізовані діагностичні консиліуми', type: 'consult', weight: 4.10, servicesSample: '99000-00' }
      ]
    };
  },
  computed: {
    filteredClasses() {
      return this.classesList.filter(item => {
        if (this.typeFilter !== 'all' && item.type !== this.typeFilter) return false;
        if (this.searchFilter) {
          const q = this.searchFilter.toLowerCase();
          const matchNum = ('клас ' + item.classNumber).includes(q);
          const matchName = item.name.toLowerCase().includes(q);
          const matchSvc = item.servicesSample.toLowerCase().includes(q);
          if (!matchNum && !matchName && !matchSvc) return false;
        }
        return true;
      });
    }
  },
  methods: {
    exportClasses() {
      this.$q.notify({
        message: 'Класифікатор амбулаторних послуг експортовано в Excel',
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
