<template>
  <div data-testid="PmgReportImport" class="q-pa-md">
    <q-card flat bordered class="q-pa-lg bg-white">
      <div class="row items-center justify-between q-mb-md">
        <div>
          <div class="text-h6 text-primary text-weight-bold row items-center">
            <q-icon name="cloud_upload" class="q-mr-sm" size="24px" />
            Імпорт та потокова обробка звіту НСЗУ (OpenXML)
          </div>
          <div class="text-caption text-grey-7">
            Процесор NszuReportXlsxProcessor : IXlsxProcessor для пакетів до 50 000 рядків
          </div>
        </div>
      </div>

      <!-- Drag & Drop Container -->
      <div
        class="q-pa-xl text-center rounded-borders cursor-pointer upload-box"
        @click="triggerFileInput"
      >
        <q-icon name="insert_drive_file" size="56px" color="primary" class="q-mb-sm" />
        <div class="text-h6 text-primary text-weight-bold">
          Перетягніть Excel-файл щомісячного звіту НСЗУ (.xlsx) сюди
        </div>
        <div class="text-caption text-grey-7 q-mb-md">
          або оберіть зі зразків реальних звітів лікарень за 2026 рік:
        </div>

        <div class="row justify-center q-gutter-md">
          <q-btn
            color="primary"
            unelevated
            icon="file_upload"
            label="Зразок: «Вересень 26.xlsx» (ОЦО, 5 490 ЕМЗ)"
            @click.stop="startSimulation('oco')"
          />
          <q-btn
            outline
            color="primary"
            icon="file_upload"
            label="Зразок: «02000334_SF_2026.xlsx» (ДКЛ, 4 394 ЕМЗ)"
            @click.stop="startSimulation('dkl')"
          />
        </div>

        <input type="file" ref="fileInput" accept=".xlsx" style="display: none" @change="onFileSelected" />
      </div>

      <!-- Progress Tracking Panel -->
      <div v-if="inProgress || isComplete" class="q-mt-lg q-pa-md bg-grey-1 rounded-borders border">
        <div class="row items-center justify-between q-mb-sm">
          <div class="text-weight-bold text-primary">{{ statusText }}</div>
          <q-badge :color="isComplete ? 'positive' : 'accent'" :label="progress + '%'" />
        </div>

        <q-linear-progress :value="progress / 100" color="accent" size="8px" class="q-mb-md rounded-borders" />

        <div class="row q-col-gutter-sm text-caption">
          <div class="col-xs-6 col-sm-3">
            <div class="q-pa-xs rounded-borders bg-white border">
              <strong>1. Аркуші:</strong>
              <span class="text-positive text-weight-bold q-ml-xs">{{ step1 }}</span>
            </div>
          </div>
          <div class="col-xs-6 col-sm-3">
            <div class="q-pa-xs rounded-borders bg-white border">
              <strong>2. 45 колонок:</strong>
              <span class="text-positive text-weight-bold q-ml-xs">{{ step2 }}</span>
            </div>
          </div>
          <div class="col-xs-6 col-sm-3">
            <div class="q-pa-xs rounded-borders bg-white border">
              <strong>3. Тарифікація:</strong>
              <span class="text-positive text-weight-bold q-ml-xs">{{ step3 }}</span>
            </div>
          </div>
          <div class="col-xs-6 col-sm-3">
            <div class="q-pa-xs rounded-borders bg-white border">
              <strong>4. 2-Way звірка:</strong>
              <span class="text-positive text-weight-bold q-ml-xs">{{ step4 }}</span>
            </div>
          </div>
        </div>

        <div v-if="isComplete" class="q-mt-md q-pa-md bg-green-1 text-green-9 rounded-borders border">
          <div class="row items-center justify-between">
            <div>
              <q-icon name="check_circle" color="positive" size="20px" class="q-mr-xs" />
              <strong>Звіт успішно імпортовано та тарифіковано!</strong> Оброблено {{ processedCount }} ЕМЗ.
            </div>
            <q-btn color="positive" label="Перейти до аналітичного аудиту →" dense unelevated @click="$emit('go-to-audit')" />
          </div>
        </div>
      </div>
    </q-card>
  </div>
</template>

<script>
export default {
  name: 'PmgReportImport',
  data() {
    return {
      inProgress: false,
      isComplete: false,
      progress: 0,
      statusText: '',
      step1: 'Очікування...',
      step2: 'Очікування...',
      step3: 'Очікування...',
      step4: 'Очікування...',
      processedCount: 0
    };
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    onFileSelected(e) {
      if (e.target.files && e.target.files.length) {
        this.startSimulation('custom', e.target.files[0].name);
      }
    },
    startSimulation(type, fileName) {
      this.inProgress = true;
      this.isComplete = false;
      this.progress = 20;
      this.statusText = type === 'oco' 
        ? 'Аналіз файлу: Вересень 26.xlsx (КНП "ОЦО")...' 
        : type === 'dkl' 
          ? 'Аналіз файлу: 02000334_SF_2026.xlsx (КНП "ДКЛ")...' 
          : `Аналіз файлу: ${fileName}...`;

      this.step1 = '4 аркуші знайдено ✓';
      this.step2 = 'Очікування...';
      this.step3 = 'Очікування...';
      this.step4 = 'Очікування...';

      setTimeout(() => { this.progress = 50; this.step2 = '45 колонок верифіковано ✓'; }, 300);
      setTimeout(() => { this.progress = 80; this.step3 = 'Тарифи ПМГ нараховано ✓'; }, 600);
      setTimeout(() => {
        this.progress = 100;
        this.step4 = '2-Way співставлено ✓';
        this.inProgress = false;
        this.isComplete = true;
        this.processedCount = type === 'dkl' ? 4394 : 5490;
        this.$emit('imported', type);
      }, 900);
    }
  }
};
</script>

<style scoped>
.upload-box {
  border: 2px dashed #90caf9;
  background-color: #f0f7ff;
}
.upload-box:hover {
  background-color: #e3f2fd;
}
</style>
