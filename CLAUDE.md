# MedLink PMG-2026 — інструкції для агента (локальна робота)

Проєкт: модуль аналітики ПМГ-2026 / ДСГ / аудиту звітів НСЗУ для МІС «Медлінк» (evomis).
Автономний стенд на стеку Medlink: **.NET 8 Web API + EF Core 8 (SQLite, для перенесення в PostgreSQL evomis) + Quasar 1.15.3 / Vue 2**, без авторизації.

## Структура (що важливо)

| Шлях | Призначення |
|---|---|
| `src/MedLink.Pmg.Module/` | Готовий бекенд (.NET 8). `Models/` — CoreEntity, сутності Медлінка (org_*, mis_*), домен `dsg_*`, довідники `pmg_*`. `Services/` — тарифний движок, SAX OpenXML парсер, класифікатор помилок, 2-Way звірка + рекомендації, пре-білінг, комбінатор, коригування, workflow. `Controllers/` — REST API. `Data/DatabaseSeeder.cs` — сідинг з `seed/`. |
| `seed/*.json` | Компактні довідники (465 ДСГ + 285k зв'язків, 148 класів, реабілітація, 186 помилок, 1 257 посад, послуги/комбінації). Генерується `python tools/build_seed.py` з `extracted_data/` та `sql/`. |
| `Вересень 26.xlsx`, `02000334_SF_2026_08_20260910.xlsx` | Реальні звіти НСЗУ — імпортуються автоматично при першому старті. |
| `src/MedLink.Pmg.Web/` | **Ще не створено** — сюди треба покласти Quasar v1 / Vue 2 SPA (вендори можна взяти з `prototype_medlink/vendor/`, компоненти-зразки з `prototype_medlink/components/*.vue`). API віддає цю папку як статику з кореня `/`. |
| `docs/`, `docs_html/`, `TZ_*.html` | Попередні ТЗ та документація (Antigravity). |
| `prototype/`, `prototype_medlink/` | Старі прототипи з вбудованими даними (data.js) — залишені як референс дизайну MedLink. |

## Запуск

```powershell
cd src\MedLink.Pmg.Module
dotnet run            # http://localhost:8085  (Swagger: /swagger, фронтенд: /)
```
При першому старті: створення SQLite `App_Data/pmg_medlink.sqlite`, сідинг (~13 с), автоімпорт двох звітів (~15 с, фоново).
Повний скид транзакційних даних: `POST /api/v1/system/reset-transactional-data?confirm=true`. Перебудувати сіди: `python tools/build_seed.py`.

## Основні API (усе в Swagger)

- `POST /api/v1/nszu/statements/upload` (multipart `file`) · `GET /api/v1/nszu/statements` · `GET .../{id}/lines` (45 колонок, фільтри) · `GET .../{id}/summary` · `POST .../{id}/reconcile` · `GET .../{id}/doctors-summary`
- `GET /api/v1/pmg/analytics/discrepancies` · `POST .../apply-correction` · `POST .../discrepancies/{id}/status` · `GET/POST .../resync-queue` · `GET .../overview` · `GET .../workflows`
- `POST /api/v1/pmg/prebilling/evaluate` · `POST /api/v1/pmg/combinations/validate` · `POST /api/v1/pmg/combinations/library-save`
- `GET /api/v1/pmg/dictionaries/{packages|dsg|classes|rehab|errors|doctor-positions|lab-tests|rules|service-groups|services|icd10|achi}` + CRUD для `tariff-settings`, `package-rules`, `rule-configs`, `errors`, `library`
- CRUD + статуси: `/api/v1/medlink/{legal-entities|departments|employees|patients|encounters}`; `POST .../encounters/{id}/status` (Draft→Signed→Submitted→Accepted/Rejected→Corrected→Resubmitted; Signed блокується Anti-Defektura, `note:"force"` для примусового підпису)
- `GET /api/v1/system/info` — ролі (Doctor, Economist, ChiefPhysician, Admin) та процеси P1–P8 з мапінгом на API.

## Що залишилось зробити (пріоритет)

1. **ТЗ v4** `docs/TZ_MedLink_PMG_v4_Cloud.md` (+ HTML у стилі `TZ_MedLink_PMG_Master_Specification.html`): мета, задачі з аналізу, MoSCoW, процеси P1–P8 за ролями з життєвими циклами (`Workflows.cs`), модель даних (усі таблиці `Models/*.cs`), зв'язки з evomis, REST API, формули тарифів (`PmgTariffCalculatorService.cs`), план міграції SQLite→PostgreSQL, тест-план. Оновити `README.md`.
2. **Тести**: xUnit проєкт `src/MedLink.Pmg.Tests` (формули: G01 5.070×0.55 = 24 357.55; pkg47 4.937×0.60 = 25 874.82; pkg9 1.29 = 199.95; гірський 1.25; неонатальний 1.54; парсер на реальних файлах; 2-Way статуси; workflow переходи) + e2e-скрипт `tools/smoke_api.py` по всіх ендпоінтах і CRUD/статусах.
3. **Фронтенд** `src/MedLink.Pmg.Web/` (Quasar UMD + Vue 2, без збірки): перемикач ролі в шапці, екрани — дашборд/імпорт, аудит 45 колонок з інспектором, 2-Way звірка, журнал розбіжностей + модалка виправлення, звіт за лікарями, АРМ лікаря (картка ЕМЗ з CRUD + пре-білінг + статуси), комбінатор + myAddLib, довідники (46 пакетів, ДСГ, класи, реабілітація, помилки, послуги), адміністрування (тарифи, правила, сутності Медлінка). Усі дані — з API (без data.js).

## Домовленості

- Конвенції evomis: snake_case колонки, `CoreEntity` (id, record_state 2/4, caption, created_*/modified_*), м'яке видалення через `record_state = 4`.
- Тарифні константи — у таблицях `dsg_tariff_setting` та `dsg_package_tariff_rule` (не хардкодити). Частки: 0.55 (пакети 3/4), 0.60 (47), планова 0.80, гірський 1.25, мультихірургія 1.30, неонатальний 1.54.
- Великі бінарники (`*.sqlite`, `bin/`, `obj/`) не комітити.
