<template>
  <div data-testid="PmgServicesCatalog" class="q-pa-md">
    <q-card flat bordered class="q-pa-md bg-white">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <div class="text-h6 text-teal-9 text-weight-bold row items-center">
            <q-icon name="miscellaneous_services" class="q-mr-sm" size="26px" />
            Справочник послуг (АКПІ): норми, методики та матриця всіх можливих комбінацій
          </div>
          <div class="text-caption text-grey-7">
            Реінжиніринг модуля послуг та правил комбінування MedProfit/Delphi (dct_mp_service_odk) для ПМГ-2026 (Постанова КМУ № 1808)
          </div>
        </div>
        <div class="row q-gutter-sm">
          <q-btn
            color="teal-8"
            outline
            icon="menu_book"
            label="Розділ 10 ТЗ (HTML)"
            dense
            class="q-px-sm"
            @click="openDocsChapter10"
          />
          <q-btn
            color="primary"
            icon="file_download"
            label="Експорт каталогу (CSV)"
            dense
            class="q-px-sm"
            @click="exportCsv"
          />
        </div>
      </div>

      <!-- Filters & Group Selector -->
      <div class="row q-col-gutter-md q-mb-md">
        <div class="col-xs-12 col-sm-4">
          <q-input
            dense
            outlined
            v-model="searchQuery"
            placeholder="Пошук послуги (код АКПІ, назва, протоколи)..."
            clearable
            @input="filterServices"
          >
            <template v-slot:prepend><q-icon name="search" /></template>
          </q-input>
        </div>

        <div class="col-xs-12 col-sm-5">
          <q-select
            dense
            outlined
            v-model="selectedGroup"
            :options="groupOptions"
            label="Клінічна група послуг (12 груп)"
            emit-value
            map-options
            @input="filterServices"
          />
        </div>

        <div class="col-xs-12 col-sm-3">
          <q-select
            dense
            outlined
            v-model="selectedCategory"
            :options="categoryOptions"
            label="Категорія втручання"
            emit-value
            map-options
            @input="filterServices"
          />
        </div>
      </div>

      <!-- Badges Bar -->
      <div class="row q-gutter-sm items-center q-mb-md text-caption text-grey-8">
        <span class="text-weight-bold">Відображено: {{ filteredServices.length }} з {{ services.length }} послуг</span>
        <q-badge color="primary">12 Клінічних груп</q-badge>
        <q-badge color="positive">Матриця комбінацій (Delphi dct_mp_service_odk)</q-badge>
        <q-badge color="accent">Норми хронометражу та стаціонару</q-badge>
        <q-badge color="purple">Мультихірургія (+30%, коеф. 1.30)</q-badge>
        <q-badge color="amber-9">Бібліотека еталонів (myAddLib)</q-badge>
      </div>

      <!-- Main Services Table -->
      <q-table
        flat
        bordered
        dense
        :data="filteredServices"
        :columns="serviceColumns"
        row-key="service_code"
        :loading="loading"
        :pagination.sync="pagination"
      >
        <template v-slot:body-cell-service_code="props">
          <q-td :props="props" class="text-center">
            <q-chip
              dense
              color="teal-8"
              text-color="white"
              class="text-weight-bold cursor-pointer"
              icon="medical_services"
              @click="openServiceCard(props.value)"
            >
              {{ props.value }}
              <q-tooltip>Відкрити паспорт, клінічні норми, формули та матрицю комбінацій</q-tooltip>
            </q-chip>
          </q-td>
        </template>

        <template v-slot:body-cell-name="props">
          <q-td :props="props">
            <div class="text-weight-bold cursor-pointer text-primary" @click="openServiceCard(props.row.service_code)">
              {{ props.value }}
            </div>
            <div class="text-caption text-grey-7" style="font-size: 11px;">
              {{ props.row.clinical_norm_notes || props.row.group_name }}
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-category="props">
          <q-td :props="props" class="text-center">
            <q-badge :color="getCategoryColor(props.value)">
              {{ props.value }}
            </q-badge>
          </q-td>
        </template>

        <template v-slot:body-cell-norms="props">
          <q-td :props="props" class="text-caption">
            <div>⏱ <strong>{{ props.row.base_norm_time_minutes }} хв</strong></div>
            <div>🛌 <strong>{{ props.row.min_stay_days }}-{{ props.row.max_stay_days }} діб</strong></div>
            <div v-if="props.row.anesthesia_required" class="text-negative font-weight-bold">💉 Анестезія: Так</div>
          </q-td>
        </template>

        <template v-slot:body-cell-base_tariff="props">
          <q-td :props="props" class="text-right">
            <div class="text-weight-bolder text-positive">
              {{ Number(props.value).toLocaleString('uk-UA', {minimumFractionDigits: 2}) }} ₴
            </div>
            <div class="text-caption text-grey-6" style="font-size: 10px;">
              Пакети: {{ props.row.package_ids }}
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-actions="props">
          <q-td :props="props" class="text-center">
            <q-btn-group rounded dense unelevated>
              <q-btn dense size="sm" color="teal" icon="badge" label="Паспорт & Норми" @click="openServiceCard(props.row.service_code, 'tab-passport')">
                <q-tooltip>Норми часу, анестезія, ліжко-дні та вікові обмеження</q-tooltip>
              </q-btn>
              <q-btn dense size="sm" color="purple" icon="schema" label="Комбінації" @click="openServiceCard(props.row.service_code, 'tab-combinations')">
                <q-tooltip>Матриця дозволених МКХ-10, супутніх послуг, посад лікарів та мультихірургії 1.3</q-tooltip>
              </q-btn>
              <q-btn dense size="sm" color="primary" icon="people" label="Drill-down ЕМЗ" @click="openServiceCard(props.row.service_code, 'tab-encounters')">
                <q-tooltip>Перехід до реальних випадків лікування та аудиту в 45 колонок</q-tooltip>
              </q-btn>
            </q-btn-group>
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- Maximized Multi-tab Service Detail Card Modal -->
    <q-dialog v-model="detailDialog" maximized transition-show="slide-up" transition-hide="slide-down">
      <q-card class="bg-grey-1 column full-height" v-if="selectedService">
        <!-- Toolbar -->
        <q-toolbar class="bg-teal-9 text-white">
          <q-icon name="miscellaneous_services" size="24px" class="q-mr-sm" />
          <q-toolbar-title class="text-subtitle1 text-weight-bold">
            Картка медичної послуги: [{{ selectedService.service.service_code }}] {{ selectedService.service.name }}
          </q-toolbar-title>
          <q-badge color="accent" class="q-mr-md text-weight-bold">Постанова КМУ №1808 • АКПІ 2026</q-badge>
          <q-btn flat round dense icon="close" v-close-popup />
        </q-toolbar>

        <!-- Tabs Header -->
        <q-tabs
          v-model="activeTab"
          dense
          class="bg-teal-8 text-white shadow-2"
          active-color="amber-3"
          indicator-color="amber-3"
          align="left"
          narrow-indicator
        >
          <q-tab name="tab-passport" icon="badge" label="1. Паспорт послуги та норми" />
          <q-tab name="tab-pricing" icon="calculate" label="2. Методика тарифікації та формули" />
          <q-tab name="tab-combinations" icon="schema" label="3. Матриця комбінацій та валідатор" />
          <q-tab name="tab-encounters" icon="people" label="4. Drill-down до пацієнтів / ЕМЗ" />
          <q-tab name="tab-defektura" icon="warning" label="5. Ризики дефектури (186 помилок)" />
        </q-tabs>

        <q-separator />

        <!-- Tab Contents -->
        <q-card-section class="col overflow-auto q-pa-md">
          <!-- TAB 1: ПАСПОРТ ТА НОРМИ -->
          <div v-if="activeTab === 'tab-passport'">
            <div class="row q-col-gutter-md">
              <div class="col-xs-12 col-md-7">
                <q-card flat bordered class="q-pa-md bg-white">
                  <div class="text-h6 text-primary text-weight-bold q-mb-sm row items-center">
                    <q-icon name="rule" class="q-mr-xs" size="22px" />
                    Клініко-технологічний паспорт та нормативи виконання
                  </div>

                  <div class="row q-col-gutter-sm q-mb-md">
                    <div class="col-6">
                      <div class="col-cell">
                        <span class="c-title">Код АКПІ (НК 026:2021):</span>
                        <span class="c-val text-primary text-weight-bolder" style="font-size: 16px;">{{ selectedService.service.service_code }}</span>
                      </div>
                    </div>
                    <div class="col-6">
                      <div class="col-cell">
                        <span class="c-title">Категорія втручання:</span>
                        <span class="c-val">{{ selectedService.service.category }}</span>
                      </div>
                    </div>
                    <div class="col-12">
                      <div class="col-cell">
                        <span class="c-title">Офіційне найменування:</span>
                        <span class="c-val">{{ selectedService.service.name }}</span>
                      </div>
                    </div>
                    <div class="col-12">
                      <div class="col-cell">
                        <span class="c-title">Клінічна група:</span>
                        <span class="c-val text-weight-bold">{{ selectedService.service.group_name }}</span>
                      </div>
                    </div>
                  </div>

                  <div class="text-subtitle2 text-weight-bold text-grey-8 q-mb-xs">Нормативні обмеження (Постанова № 1808):</div>
                  <div class="row q-col-gutter-sm">
                    <div class="col-4">
                      <div class="col-cell bg-blue-1">
                        <span class="c-title">⏱ Норма часу:</span>
                        <span class="c-val text-primary">{{ selectedService.service.base_norm_time_minutes }} хв</span>
                      </div>
                    </div>
                    <div class="col-4">
                      <div class="col-cell bg-purple-1">
                        <span class="c-title">💉 Анестезія:</span>
                        <span class="c-val text-purple-9">{{ selectedService.service.anesthesia_required ? 'Обов\'язкова' : 'Не потрібна' }}</span>
                      </div>
                    </div>
                    <div class="col-4">
                      <div class="col-cell bg-teal-1">
                        <span class="c-title">🛌 Ліжко-дні:</span>
                        <span class="c-val text-teal-9">{{ selectedService.service.min_stay_days }} — {{ selectedService.service.max_stay_days }} діб</span>
                      </div>
                    </div>
                    <div class="col-6">
                      <div class="col-cell">
                        <span class="c-title">👶 Вікові рамки:</span>
                        <span class="c-val">{{ selectedService.service.age_min }} — {{ selectedService.service.age_max }} років</span>
                      </div>
                    </div>
                    <div class="col-6">
                      <div class="col-cell">
                        <span class="c-title">⚧ Статеві обмеження:</span>
                        <span class="c-val">{{ selectedService.service.gender_restriction === 'ALL' ? 'Без обмежень' : selectedService.service.gender_restriction }}</span>
                      </div>
                    </div>
                  </div>

                  <div class="q-mt-md q-pa-sm bg-grey-2 rounded-borders">
                    <div class="text-weight-bold text-grey-8 text-caption">Клінічні рекомендації та примітки:</div>
                    <div class="text-caption text-grey-9 q-mt-xs">{{ selectedService.service.clinical_norm_notes }}</div>
                  </div>
                </q-card>
              </div>

              <div class="col-xs-12 col-md-5">
                <q-card flat bordered class="q-pa-md bg-white">
                  <div class="text-h6 text-teal text-weight-bold q-mb-sm row items-center">
                    <q-icon name="gavel" class="q-mr-xs" size="22px" />
                    Нормативно-ліцензійна база ПМГ-2026
                  </div>

                  <div class="col-cell q-mb-sm">
                    <span class="c-title">Дозволені пакети ПМГ:</span>
                    <span class="c-val text-weight-bold text-indigo">{{ selectedService.service.package_ids }}</span>
                  </div>

                  <div class="col-cell q-mb-sm">
                    <span class="c-title">ДСГ за Додатком 1:</span>
                    <span class="c-val text-weight-bold text-positive">{{ selectedService.service.dsg_codes }}</span>
                  </div>

                  <div class="col-cell q-mb-sm">
                    <span class="c-title">Базовий тариф:</span>
                    <span class="c-val text-weight-bolder text-positive" style="font-size: 16px;">
                      {{ Number(selectedService.service.base_tariff).toLocaleString('uk-UA', {minimumFractionDigits: 2}) }} ₴
                    </span>
                  </div>

                  <div class="text-subtitle2 text-weight-bold text-grey-8 q-mt-md q-mb-xs">Вимоги до посади лікаря (Наказ МОЗ № 410):</div>
                  <q-list dense bordered separator class="rounded-borders">
                    <q-item v-for="(rule, rIdx) in selectedService.doctorRules" :key="rIdx">
                      <q-item-section avatar>
                        <q-icon name="badge" color="primary" />
                      </q-item-section>
                      <q-item-section>
                        <q-item-label class="text-weight-bold text-primary">{{ rule.required_position_name }}</q-item-label>
                        <q-item-label caption>Код: <code>{{ rule.required_position_code }}</code> • {{ rule.legal_basis }}</q-item-label>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </q-card>
              </div>
            </div>
          </div>

          <!-- TAB 2: МЕТОДИКА ТАРИФІКАЦІЇ -->
          <div v-if="activeTab === 'tab-pricing'">
            <q-card flat bordered class="q-pa-md bg-white">
              <div class="text-h6 text-primary text-weight-bold q-mb-sm row items-center">
                <q-icon name="calculate" class="q-mr-xs" size="24px" />
                Методика фінансового розрахунку та коефіцієнти Постанови № 1808
              </div>

              <div class="q-pa-md bg-blue-1 rounded-borders border q-my-md">
                <div class="text-subtitle1 text-weight-bold text-primary q-mb-sm">
                  🧮 Симулятор тарифу послуги:
                </div>
                <div class="row q-col-gutter-md items-center">
                  <div class="col-xs-12 col-sm-3">
                    <q-select dense outlined bg-color="white" v-model="calcAdmission" :options="['Планова', 'Ургентна']" label="Госпіталізація" />
                  </div>
                  <div class="col-xs-12 col-sm-3">
                    <q-select dense outlined bg-color="white" v-model="calcModel" :options="[{label: 'Стаціонар (0.55)', value: 0.55}, {label: 'Хірургія 1-дня (0.60)', value: 0.60}]" emit-value map-options label="Модель" />
                  </div>
                  <div class="col-xs-12 col-sm-3">
                    <q-toggle v-model="calcMountain" label="Гірський (1.25)" color="primary" />
                  </div>
                  <div class="col-xs-12 col-sm-3">
                    <q-toggle v-model="calcMultiSurg" label="Мультихірургія (1.30)" color="purple" />
                  </div>
                </div>

                <q-separator class="q-my-md" />

                <div class="row items-center justify-between">
                  <div>
                    <div class="text-caption text-grey-8">Формула:</div>
                    <div class="text-body2 text-weight-bold font-mono">
                      8 735.00 × 2.766 × {{ calcModel }} × {{ calcAdmission === 'Планова' ? '0.80' : '1.00' }} × {{ calcMountain ? '1.25' : '1.00' }} × {{ calcMultiSurg ? '1.30' : '1.00' }}
                    </div>
                  </div>
                  <div class="text-right">
                    <div class="text-caption text-grey-8">Розрахована сума:</div>
                    <div class="text-h5 text-weight-bolder text-positive">
                      {{ (8735.0 * 2.766 * calcModel * (calcAdmission === 'Планова' ? 0.8 : 1.0) * (calcMountain ? 1.25 : 1.0) * (calcMultiSurg ? 1.3 : 1.0)).toLocaleString('uk-UA', {minimumFractionDigits: 2}) }} ₴
                    </div>
                  </div>
                </div>
              </div>
            </q-card>
          </div>

          <!-- TAB 3: МАТРИЦЯ КОМБІНАЦІЙ ТА ВАЛІДАТОР (DELPHI) -->
          <div v-if="activeTab === 'tab-combinations'">
            <div class="row q-col-gutter-md">
              <div class="col-xs-12 col-md-6">
                <q-card flat bordered class="q-pa-md bg-white">
                  <div class="text-h6 text-purple-9 text-weight-bold q-mb-sm row items-center">
                    <q-icon name="schema" class="q-mr-xs" size="22px" />
                    Матриця дозволених комбінацій (Delphi dct_mp_service_odk)
                  </div>

                  <div v-for="comb in selectedService.combinations" :key="comb.id" class="q-pa-sm bg-grey-1 rounded-borders border q-mb-sm">
                    <div class="row items-center justify-between q-mb-xs">
                      <span class="text-weight-bold text-primary">{{ comb.combination_name }}</span>
                      <q-badge :color="comb.is_library_standard ? 'positive' : 'grey-7'">
                        {{ comb.is_library_standard ? '⭐ Еталон myAddLib' : 'Користувацька' }}
                      </q-badge>
                    </div>

                    <div class="text-caption q-my-xs">
                      <strong>Сумісні МКХ-10:</strong>
                      <div class="row q-gutter-xs q-mt-xs">
                        <q-badge color="indigo-7" v-for="icd in (comb.compatible_icd_codes || [])" :key="icd.code">
                          {{ icd.code }}
                        </q-badge>
                      </div>
                    </div>

                    <div class="text-caption q-my-xs" v-if="comb.mandatory_companions && comb.mandatory_companions.length > 0">
                      <strong class="text-negative">Обов'язкові супутні АКПІ:</strong>
                      <div class="row q-gutter-xs q-mt-xs">
                        <q-badge color="red-8" v-for="m in comb.mandatory_companions" :key="m.code">
                          + {{ m.code }} ({{ m.name }})
                        </q-badge>
                      </div>
                    </div>

                    <div class="text-caption q-my-xs" v-if="comb.optional_multisurg_companions && comb.optional_multisurg_companions.length > 0">
                      <strong class="text-positive">Мультихірургія (+30%):</strong>
                      <div class="row q-gutter-xs q-mt-xs">
                        <q-badge color="green-8" v-for="ms in comb.optional_multisurg_companions" :key="ms.code">
                          ⭐ {{ ms.code }} ({{ ms.name }})
                        </q-badge>
                      </div>
                    </div>

                    <div class="row items-center justify-between q-mt-sm pt-xs border-top">
                      <span class="text-caption font-mono">ДСГ: <strong>{{ comb.expected_dsg_code }}</strong> (Wg = {{ comb.weight_coef }})</span>
                      <span class="text-weight-bold text-positive">{{ Number(comb.calculated_tariff).toLocaleString('uk-UA') }} ₴</span>
                    </div>
                  </div>
                </q-card>
              </div>

              <!-- Validator Box -->
              <div class="col-xs-12 col-md-6">
                <q-card flat bordered class="q-pa-md bg-white">
                  <div class="text-h6 text-primary text-weight-bold q-mb-sm row items-center">
                    <q-icon name="smart_toy" class="q-mr-xs" size="22px" />
                    Онлайн-валідатор комбінації (Rule Check)
                  </div>

                  <div class="q-gutter-sm">
                    <q-input dense outlined v-model="validatorIcd" label="МКХ-10 (C180, C18.0...)" />
                    <q-select
                      dense
                      outlined
                      v-model="validatorDocPos"
                      :options="[
                        { label: 'P157 — Лікар-хірург-онколог (Дозволено)', value: 'P157' },
                        { label: 'P158 — Лікар-хірург дитячий (Дозволено)', value: 'P158' },
                        { label: 'P58 — Лікар-хірург загальний (Дозволено)', value: 'P58' },
                        { label: 'P122 — Лікар-терапевт (ДЕФЕКТУРА 0 ₴)', value: 'P122' }
                      ]"
                      emit-value
                      map-options
                      label="Посада лікаря"
                    />

                    <div class="text-caption text-grey-8 text-weight-bold q-mt-sm">Супутні втручання:</div>
                    <q-option-group
                      v-model="validatorCompanions"
                      :options="[
                        { label: '30075-01 Біопсія та резекція лімфовузлів брижі (Обов\'язково)', value: '30075-01' },
                        { label: '30394-00 Дренування черевної порожнини (Обов\'язково)', value: '30394-00' },
                        { label: '30440-00 Симультанна холецистектомія (+30% Мультихірургія)', value: '30440-00' }
                      ]"
                      type="checkbox"
                      dense
                    />

                    <q-btn
                      unelevated
                      color="primary"
                      icon="verified"
                      label="Перевірити комбінацію за правилами НСЗУ"
                      class="full-width q-mt-md"
                      @click="validateCombination"
                    />
                  </div>

                  <!-- Result Box -->
                  <div v-if="validationResult" class="q-mt-md q-pa-md rounded-borders border" :class="validationResult.isValid ? 'bg-green-1 border-positive' : 'bg-red-1 border-negative'">
                    <div class="row items-center justify-between q-mb-sm">
                      <span class="text-subtitle2 text-weight-bold" :class="validationResult.isValid ? 'text-positive' : 'text-negative'">
                        {{ validationResult.isValid ? '✓ КОМБІНАЦІЮ СХВАЛЕНО' : '⛔ ДЕФЕКТУРА: ВІДХИЛЕННЯ НСЗУ (0 ₴)' }}
                      </span>
                      <q-badge :color="validationResult.isValid ? 'positive' : 'negative'">
                        {{ validationResult.status }}
                      </q-badge>
                    </div>

                    <div class="row justify-between text-body2 q-my-xs">
                      <span>Розрахований тариф:</span>
                      <strong class="text-h6 text-positive">{{ validationResult.calculatedTariffUah.toLocaleString('uk-UA', {minimumFractionDigits: 2}) }} ₴</strong>
                    </div>

                    <div v-if="validationResult.errors && validationResult.errors.length > 0" class="q-mb-sm">
                      <div class="text-caption text-negative text-weight-bold" v-for="(err, eIdx) in validationResult.errors" :key="eIdx">
                        ✕ {{ err }}
                      </div>
                    </div>
                    <div v-if="validationResult.warnings && validationResult.warnings.length > 0" class="q-mb-sm">
                      <div class="text-caption text-warning text-weight-bold" v-for="(wrn, wIdx) in validationResult.warnings" :key="wIdx">
                        ⚠ {{ wrn }}
                      </div>
                    </div>

                    <q-btn
                      flat
                      dense
                      color="primary"
                      icon="bookmark_add"
                      label="Зберегти в бібліотеку еталонів (myAddLib)"
                      class="q-mt-sm"
                      @click="saveToLibrary"
                    />
                  </div>
                </q-card>
              </div>
            </div>
          </div>

          <!-- TAB 4: DRILL-DOWN ДО ПАЦІЄНТІВ / ЕМЗ -->
          <div v-if="activeTab === 'tab-encounters'">
            <q-card flat bordered class="q-pa-md bg-white">
              <div class="row items-center justify-between q-mb-md">
                <div>
                  <div class="text-h6 text-primary text-weight-bold row items-center">
                    <q-icon name="people" class="q-mr-xs" size="24px" />
                    Реєстр реальних ЕМЗ з послугою [{{ selectedService.service.service_code }}]
                  </div>
                  <div class="text-caption text-grey-7">
                    Прямий перехід від послуги до конкретного пацієнта та його повного аудиту в 45 колонок
                  </div>
                </div>
                <q-badge color="primary">Знайдено: {{ selectedService.encounters.length }} випадків</q-badge>
              </div>

              <q-table
                flat
                bordered
                dense
                :data="selectedService.encounters"
                :columns="encounterColumns"
                row-key="id"
                :pagination="{ rowsPerPage: 10 }"
              >
                <template v-slot:body-cell-status="props">
                  <q-td :props="props" class="text-center">
                    <q-badge :color="props.row.is_accepted ? 'positive' : 'negative'">
                      {{ props.row.is_accepted ? '✓ Оплачено' : '✕ Відхилено' }}
                    </q-badge>
                  </q-td>
                </template>
                <template v-slot:body-cell-actions="props">
                  <q-td :props="props" class="text-center">
                    <q-btn
                      dense
                      size="sm"
                      color="primary"
                      icon="visibility"
                      label="45 колонок"
                      @click="$emit('open-encounter-45', props.row)"
                    />
                  </template>
                </q-table>
            </q-card>
          </div>

          <!-- TAB 5: РИЗИКИ ДЕФЕКТУРИ -->
          <div v-if="activeTab === 'tab-defektura'">
            <q-card flat bordered class="q-pa-md bg-white">
              <div class="text-h6 text-negative text-weight-bold q-mb-sm row items-center">
                <q-icon name="report_problem" class="q-mr-xs" size="24px" />
                Ризики дефектури та протокольні вимоги НСЗУ (186 причин відхилення)
              </div>

              <q-list bordered separator class="rounded-borders">
                <q-item v-for="(risk, idx) in selectedService.defekturaRisks" :key="idx" class="q-py-md">
                  <q-item-section avatar>
                    <q-avatar color="red-1" text-color="negative" icon="warning" />
                  </q-item-section>
                  <q-item-section>
                    <div class="row items-center q-gutter-sm">
                      <span class="code-chip text-negative text-weight-bold">{{ risk.error_code }}</span>
                      <span class="text-weight-bold text-grey-9">{{ risk.title }}</span>
                    </div>
                    <div class="text-caption text-grey-8 q-mt-xs">
                      <strong>Юридична підстава:</strong> {{ risk.legal_basis }}
                    </div>
                    <div class="text-caption text-primary q-mt-xs">
                      <strong>💡 Рекомендація:</strong> {{ risk.recommendation_action }}
                    </div>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-card>
          </div>
        </q-card-section>

        <q-separator />
        <q-card-actions align="right" class="bg-white q-px-lg">
          <q-btn flat label="Закрити" color="grey-8" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
export default {
  name: 'PmgServicesCatalog',
  data() {
    return {
      searchQuery: '',
      selectedGroup: 'ALL',
      selectedCategory: 'ALL',
      loading: false,
      services: [],
      filteredServices: [],
      groupOptions: [{ label: 'Усі клінічні групи (12)', value: 'ALL' }],
      categoryOptions: [
        { label: 'Усі категорії', value: 'ALL' },
        { label: 'Хірургічні (Surgical)', value: 'Surgical' },
        { label: 'Діагностичні (Diagnostic)', value: 'Diagnostic' },
        { label: 'Терапевтичні (Therapeutic)', value: 'Therapeutic' },
        { label: 'Реабілітаційні (Rehabilitation)', value: 'Rehabilitation' }
      ],
      pagination: { rowsPerPage: 15 },
      serviceColumns: [
        { name: 'service_code', label: 'Код АКПІ', field: 'service_code', align: 'center', sortable: true },
        { name: 'name', label: 'Назва послуги та регламент', field: 'name', align: 'left', sortable: true },
        { name: 'group_name', label: 'Клінічна група', field: 'group_name', align: 'left', sortable: true },
        { name: 'category', label: 'Категорія', field: 'category', align: 'center', sortable: true },
        { name: 'norms', label: 'Норми часу & ліжка', field: 'base_norm_time_minutes', align: 'left' },
        { name: 'base_tariff', label: 'Базовий тариф ПМГ', field: 'base_tariff', align: 'right', sortable: true },
        { name: 'actions', label: 'Дії', field: 'service_code', align: 'center' }
      ],
      encounterColumns: [
        { name: 'line_number', label: '№ рядка', field: 'line_number', align: 'center', sortable: true },
        { name: 'encounter_ehealth_id', label: 'eHealth ID', field: r => r.encounter_ehealth_id ? r.encounter_ehealth_id.slice(0, 12) + '...' : '—', align: 'left' },
        { name: 'patient_full_name', label: 'Пацієнт', field: 'patient_full_name', align: 'left' },
        { name: 'doctor_full_name', label: 'Лікар', field: 'doctor_full_name', align: 'left' },
        { name: 'primary_icd10_code', label: 'МКХ-10', field: 'primary_icd10_code', align: 'center' },
        { name: 'dsg_code', label: 'ДСГ', field: 'dsg_code', align: 'center' },
        { name: 'nszu_amount', label: 'Виплата НСЗУ', field: r => Number(r.nszu_amount || 0).toLocaleString('uk-UA') + ' ₴', align: 'right' },
        { name: 'status', label: 'Статус', field: 'is_accepted', align: 'center' },
        { name: 'actions', label: '45 колонок', field: 'id', align: 'center' }
      ],
      detailDialog: false,
      activeTab: 'tab-passport',
      selectedService: null,
      calcAdmission: 'Планова',
      calcModel: 0.55,
      calcMountain: false,
      calcMultiSurg: false,
      validatorIcd: 'C180',
      validatorDocPos: 'P157',
      validatorCompanions: ['30075-01', '30394-00'],
      validationResult: null
    };
  },
  mounted() {
    this.fetchGroups();
    this.fetchServices();
  },
  methods: {
    getCategoryColor(cat) {
      if (cat === 'Surgical') return 'red-8';
      if (cat === 'Diagnostic') return 'blue-8';
      if (cat === 'Rehabilitation') return 'green-8';
      return 'purple-8';
    },
    fetchGroups() {
      fetch('/api/v1/pmg/dictionaries/service-groups')
        .then(res => res.json())
        .then(data => {
          if (Array.isArray(data)) {
            this.groupOptions = [{ label: 'Усі клінічні групи (12)', value: 'ALL' }].concat(
              data.map(g => ({ label: `${g.code} — ${g.name} (${g.service_count} посл.)`, value: g.id }))
            );
          }
        })
        .catch(err => console.warn('Groups fetch error:', err));
    },
    fetchServices() {
      this.loading = true;
      fetch('/api/v1/pmg/dictionaries/services')
        .then(res => res.json())
        .then(data => {
          this.loading = false;
          if (Array.isArray(data)) {
            this.services = data;
            this.filteredServices = data;
          }
        })
        .catch(err => {
          this.loading = false;
          console.warn('Services fetch error:', err);
        });
    },
    filterServices() {
      const q = (this.searchQuery || '').toLowerCase().trim();
      const grp = this.selectedGroup;
      const cat = this.selectedCategory;

      this.filteredServices = this.services.filter(s => {
        if (grp !== 'ALL' && s.group_id !== grp) return false;
        if (cat !== 'ALL' && s.category !== cat) return false;
        if (q) {
          const text = (s.service_code + ' ' + s.name + ' ' + (s.clinical_norm_notes || '')).toLowerCase();
          if (!text.includes(q)) return false;
        }
        return true;
      });
    },
    openServiceCard(serviceCode, tab) {
      const clean = String(serviceCode).trim().split(' ')[0];
      fetch('/api/v1/pmg/dictionaries/services/' + clean)
        .then(res => res.json())
        .then(data => {
          this.selectedService = data;
          this.activeTab = tab || 'tab-passport';
          this.validatorIcd = 'C180';
          this.validatorDocPos = 'P157';
          this.validatorCompanions = ['30075-01', '30394-00'];
          this.validationResult = null;
          this.detailDialog = true;
        })
        .catch(err => {
          this.$q.notify({ message: 'Помилка завантаження: ' + err.message, color: 'warning' });
        });
    },
    validateCombination() {
      if (!this.selectedService) return;
      const payload = {
        serviceCode: this.selectedService.service.service_code,
        icdCode: this.validatorIcd,
        doctorPosition: this.validatorDocPos,
        companionServices: this.validatorCompanions,
        admissionType: 'Планова',
        isMountain: false
      };
      fetch('/api/v1/pmg/combinations/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
        .then(res => res.json())
        .then(data => {
          this.validationResult = data;
          if (data.isValid) {
            this.$q.notify({ message: '✓ Комбінацію схвалено! Тариф: ' + data.calculatedTariffUah.toLocaleString('uk-UA') + ' ₴', color: 'positive' });
          } else {
            this.$q.notify({ message: '⛔ Дефектура НСЗУ: 0 ₴!', color: 'negative' });
          }
        });
    },
    saveToLibrary() {
      if (!this.validationResult) return;
      const combId = this.validationResult.matchedCombination ? this.validationResult.matchedCombination.id : 'comb-custom';
      fetch('/api/v1/pmg/combinations/library-save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ combinationId: combId, isStandard: true })
      })
        .then(res => res.json())
        .then(() => {
          this.$q.notify({ message: '⭐ Еталон збережено в myAddLib!', color: 'positive' });
        });
    },
    openDocsChapter10() {
      window.open('../docs_html/10_service_directory_norms_methodologies_combinations.html', '_blank');
    },
    exportCsv() {
      let csv = "\uFEFFКод АКПІ;Назва послуги;Група;Категорія;Норма часу (хв);Анестезія;Ліжко-дні;Базовий тариф\n";
      this.filteredServices.forEach(s => {
        csv += `"${s.service_code}";"${s.name}";"${s.group_name}";"${s.category}";"${s.base_norm_time_minutes}";"${s.anesthesia_required ? 'Так' : 'Ні'}";"${s.min_stay_days}-${s.max_stay_days}";"${s.base_tariff}"\n`;
      });
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = "pmg_services_catalog_norms_combinations.csv";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      this.$q.notify({ message: '📥 Файл pmg_services_catalog_norms_combinations.csv завантажено!', color: 'positive' });
    }
  }
};
</script>

<style scoped>
.col-cell {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 8px 10px;
  font-size: 13px;
}
.col-cell .c-title {
  font-size: 11px;
  font-weight: 700;
  color: #64748b;
  display: block;
  margin-bottom: 2px;
}
.col-cell .c-val {
  font-weight: 600;
  color: #0f172a;
  word-break: break-word;
}
.code-chip {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid #cbd5e1;
}
</style>
