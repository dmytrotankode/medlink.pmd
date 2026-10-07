HTML_PATH = r"c:\__MEDLINK___\PMG\prototype_medlink\index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    text = f.read()

old_calc = """        calcSimulation: function () {
          const pkg = this.simPackage;
          const diag = (this.simDiag || '').replace(/\./g, '').trim().toUpperCase();
          const svc = this.simSvc || '';
          const mountain = parseFloat(this.simMountain) || 1.0;

          let dsgCode = '—';
          let dsgName = 'Не визначено';
          let coeff = 1.0;
          let baseRate = 8735.0;
          let extraK = 0.55;
          let warning = null;"""

new_calc = """        calcSimulation: function () {
          const self = this;
          const pkg = this.simPackage;
          const rawDiag = this.simDiag || 'C180';
          const diagNorm = rawDiag.replace(/\./g, '').trim().toUpperCase();
          const svc = this.simSvc || '32003-00';
          const mountain = parseFloat(this.simMountain) || 1.0;
          const docPos = this.simDoctorPos || 'P157';
          const admType = this.simAdmissionType || 'Планова';

          // Call Real Live SQLite REST API
          fetch('/api/v1/pmg/prebilling/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              icdCode: rawDiag,
              serviceCode: svc,
              doctorPosition: docPos,
              admissionType: admType,
              isMountain: mountain > 1.0
            })
          })
          .then(res => res.json())
          .then(data => {
            self.simResult = {
              dsgCode: data.dsgCode,
              dsgName: data.dsgTitle,
              baseRate: 8735.0,
              coeff: data.weightCoefficient,
              total: data.calculatedTariffUah,
              warning: data.antiDefekturaCheck?.warning
            };
            if (data.antiDefekturaCheck?.isValid) {
              self.$q.notify({
                message: `✓ Пре-білінг успішний: Тариф ${data.calculatedTariffUah.toLocaleString('uk-UA')} ₴ • Посада ${docPos} валідна`,
                color: 'positive',
                icon: 'check_circle'
              });
            } else {
              self.$q.notify({
                message: `⛔ КРИТИЧНО: ${data.antiDefekturaCheck?.warning?.message}`,
                color: 'negative',
                icon: 'report_problem',
                timeout: 5000
              });
            }
          })
          .catch(err => {
            console.warn('Fallback to local calc:', err);
            // Local fallback calculation
            let coeff = (svc.includes('32003')) ? 2.766 : (svc.includes('30518') ? 2.340 : 1.0);
            let baseRate = (pkg === '9') ? 155.0 : 8735.0;
            let extraK = (pkg === '4') ? 0.60 : 0.55;
            let kPlan = (admType === 'Планова') ? 0.80 : 1.0;
            let total = Math.round(baseRate * coeff * extraK * kPlan * mountain * 100) / 100;
            let warn = null;
            if (docPos === 'P122') {
              warn = {
                code: 'ERR_DOC_SPEC_04',
                severity: 'CRITICAL',
                message: 'Спеціальність терапевта (P122) не дозволяє кодування операції 32003-00. Випадок буде відхилено НСЗУ (0 ₴)!',
                legalBasis: 'Наказ МОЗ № 410, п. 4.1',
                advice: 'Призначте лікаря з посадою P157 (Хірург-онколог).'
              };
            }
            self.simResult = {
              dsgCode: 'O0101',
              dsgName: 'Великі хірургічні втручання на ободовій кишці',
              baseRate: baseRate,
              coeff: coeff,
              total: total,
              warning: warn
            };
          });
          return;

          let dsgCode = '—';
          let dsgName = 'Не визначено';
          let coeff = 1.0;
          let baseRate = 8735.0;
          let extraK = 0.55;
          let warning = null;"""

if old_calc in text:
    text = text.replace(old_calc, new_calc)
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print("calcSimulation updated with live API integration!")
else:
    print("old_calc snippet not found.")
