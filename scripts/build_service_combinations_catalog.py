import sqlite3
import json
import uuid
import os

def build_service_catalog():
    db_path = r'c:\__MEDLINK___\PMG\pmg_database.sqlite'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("1. Creating tables for services, groups, and combinations...")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pmg_service_groups (
        id TEXT PRIMARY KEY,
        code TEXT NOT NULL,
        name TEXT NOT NULL,
        parent_id TEXT,
        level INTEGER DEFAULT 1,
        description TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pmg_service_catalog (
        service_code TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        group_id TEXT,
        group_name TEXT,
        category TEXT NOT NULL, -- 'Surgical', 'Diagnostic', 'Therapeutic', 'Rehabilitation'
        base_norm_time_minutes INTEGER DEFAULT 60,
        anesthesia_required INTEGER DEFAULT 0, -- 1=yes, 0=no
        min_stay_days INTEGER DEFAULT 0,
        max_stay_days INTEGER DEFAULT 14,
        age_min INTEGER DEFAULT 0,
        age_max INTEGER DEFAULT 120,
        gender_restriction TEXT DEFAULT 'ALL', -- 'ALL', 'MALE', 'FEMALE'
        package_ids TEXT, -- '3,4,47'
        dsg_codes TEXT, -- 'G01,G02'
        base_tariff REAL DEFAULT 8735.0,
        clinical_norm_notes TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pmg_service_combinations (
        id TEXT PRIMARY KEY,
        service_code TEXT NOT NULL,
        combination_name TEXT NOT NULL,
        compatible_icd_codes TEXT NOT NULL, -- JSON array of ICD codes and names
        mandatory_companions TEXT, -- JSON array of companion service codes
        optional_multisurg_companions TEXT, -- JSON array of services giving 1.3 multisurg coeff
        incompatible_services TEXT, -- JSON array of conflicting services
        allowed_doctor_positions TEXT NOT NULL, -- JSON array of doctor positions
        prohibited_doctor_positions TEXT NOT NULL,
        expected_package_number TEXT NOT NULL,
        expected_dsg_code TEXT NOT NULL,
        weight_coef REAL NOT NULL,
        calculated_tariff REAL NOT NULL,
        calculation_formula TEXT NOT NULL,
        rule_condition TEXT,
        is_library_standard INTEGER DEFAULT 1 -- 1=in standard lib (myDetailLib), 0=custom
    );
    """)

    # 2. Populate 12 Hierarchical Service Groups (Delphi service_groups reengineering)
    print("2. Populating Service Groups...")
    cur.execute("DELETE FROM pmg_service_groups;")
    groups = [
        ("grp-01", "SG-01", "Хірургія органів черевної порожнини та ШКТ", None, 1, "Абдомінальна хірургія: резекції кишечника, шлунка, холецистектомія, грижосічення"),
        ("grp-02", "SG-02", "Онкологічні хірургічні втручання", None, 1, "Розширені та комбіновані онкохірургічні резекції пухлин з лімфодисекцією"),
        ("grp-03", "SG-03", "Офтальмологічні операції та мікрохірургія ока", None, 1, "Хірургія катаракти, глаукоми, травм ока, кератопластика"),
        ("grp-04", "SG-04", "Кардіохірургія та інтервенційна кардіологія", None, 1, "Стентування коронарних артерій, шунтування, корекція вад серця"),
        ("grp-05", "SG-05", "Нейрохірургія та спінальна хірургія", None, 1, "Краніотомія, кліпування аневризм, декомпресія хребта, шунтування"),
        ("grp-06", "SG-06", "Травматологія, ортопедія та ендопротезування", None, 1, "Остеосинтез переломів, артроскопія, ендопротезування суглобів"),
        ("grp-07", "SG-07", "Ендоскопічні діагностичні та лікувальні процедури", None, 1, "Гастроскопія, колоноскопія, бронхоскопія, ендоскопічна поліпектомія"),
        ("grp-08", "SG-08", "Хіміотерапевтичне та фармакологічне введення", None, 1, "Внутрішньовенна хіміотерапія, таргетна та імунотерапія онкохворих"),
        ("grp-09", "SG-09", "Променева терапія та радіологія", None, 1, "Дистанційна променева терапія, брахітерапія на лінійних прискорювачах"),
        ("grp-10", "SG-10", "Реабілітаційні інтервенції та фізіотерапія", None, 1, "Кінезіотерапія, ерготерапія, психологічна реабілітація за матрицями АР1-АР4"),
        ("grp-11", "SG-11", "Інтенсивна терапія, реанімація та ЕКМО", None, 1, "ШВЛ >24 годин, екстракорпоральна мембранна оксигенація, плазмаферез"),
        ("grp-12", "SG-12", "Амбулаторні консультації та скринінги", None, 1, "Спеціалізовані консультації 148 амбулаторних класів та ранній скринінг")
    ]
    for g in groups:
        cur.execute("INSERT INTO pmg_service_groups (id, code, name, parent_id, level, description) VALUES (?, ?, ?, ?, ?, ?)", g)

    # 3. Populate Services Catalog with full norms & clinical profiles
    print("3. Populating Services Catalog with norms and methods...")
    cur.execute("DELETE FROM pmg_service_catalog;")
    services_data = [
        {
            "code": "32003-00",
            "name": "Правобічна геміколектомія з анастомозом",
            "group_id": "grp-01",
            "group_name": "Хірургія органів черевної порожнини та ШКТ",
            "category": "Surgical",
            "base_norm_time": 180,
            "anesthesia": 1,
            "min_stay": 4,
            "max_stay": 21,
            "age_min": 18,
            "age_max": 120,
            "gender": "ALL",
            "packages": "4, 3",
            "dsgs": "O0101, G01",
            "base_tariff": 8735.0,
            "notes": "Потребує передопераційного онкоскринінгу (колоноскопія 11600-00), обов'язкового гістологічного дослідження та посади хірурга P157. Мультихірургія дозволена з дренуванням."
        },
        {
            "code": "30061-02",
            "name": "Видалення поверхневого стороннього тіла з рогівки",
            "group_id": "grp-03",
            "group_name": "Офтальмологічні операції та мікрохірургія ока",
            "category": "Surgical",
            "base_norm_time": 30,
            "anesthesia": 0,
            "min_stay": 0,
            "max_stay": 1,
            "age_min": 0,
            "age_max": 120,
            "gender": "ALL",
            "packages": "47, 9, 3",
            "dsgs": "C01, ААС",
            "base_tariff": 8735.0,
            "notes": "Виконується в амбулаторних умовах або стаціонарі одного дня (Пакет 47). Заборонена госпіталізація >1 доби без ускладнень."
        },
        {
            "code": "30518-00",
            "name": "Часткова дистальна резекція шлунка з гастроентероанастомозом",
            "group_id": "grp-01",
            "group_name": "Хірургія органів черевної порожнини та ШКТ",
            "category": "Surgical",
            "base_norm_time": 210,
            "anesthesia": 1,
            "min_stay": 5,
            "max_stay": 25,
            "age_min": 18,
            "age_max": 120,
            "gender": "ALL",
            "packages": "4, 3",
            "dsgs": "G03, G01",
            "base_tariff": 8735.0,
            "notes": "Високоскладна операція. Потребує обов'язкової лімфодисекції D2 при раку шлунка (C16) та посади онкохірурга P157."
        },
        {
            "code": "42672-00",
            "name": "Розріз рогівки (кератотомія)",
            "group_id": "grp-03",
            "group_name": "Офтальмологічні операції та мікрохірургія ока",
            "category": "Surgical",
            "base_norm_time": 45,
            "anesthesia": 1,
            "min_stay": 0,
            "max_stay": 2,
            "age_min": 5,
            "age_max": 120,
            "gender": "ALL",
            "packages": "47, 3",
            "dsgs": "C02, ААС",
            "base_tariff": 8735.0,
            "notes": "Мікрохірургічне втручання. Оплата за Пакет 47 з коефіцієнтом 0.60 при виписці в день операції."
        },
        {
            "code": "96199-00",
            "name": "Внутрішньовенне введення протипухлинного хіміотерапевтичного агента",
            "group_id": "grp-08",
            "group_name": "Хіміотерапевтичне та фармакологічне введення",
            "category": "Therapeutic",
            "base_norm_time": 120,
            "anesthesia": 0,
            "min_stay": 0,
            "max_stay": 3,
            "age_min": 0,
            "age_max": 120,
            "gender": "ALL",
            "packages": "18, 9",
            "dsgs": "Пакет 18",
            "base_tariff": 17865.0,
            "notes": "Тарифікується за Пакетом 18 (17 865 ₴ для дорослих / 35 730 ₴ при інтенсивній терапії). Вимагає основного діагнозу Z51.1 та супутнього C00-C97."
        },
        {
            "code": "15269-00",
            "name": "Дистанційна променева терапія на лінійному прискорювачі (фотонна/електронна)",
            "group_id": "grp-09",
            "group_name": "Променева терапія та радіологія",
            "category": "Therapeutic",
            "base_norm_time": 40,
            "anesthesia": 0,
            "min_stay": 0,
            "max_stay": 30,
            "age_min": 0,
            "age_max": 120,
            "gender": "ALL",
            "packages": "19, 9",
            "dsgs": "Пакет 19",
            "base_tariff": 54089.0,
            "notes": "Тарифікується за Пакетом 19 (54 089 ₴ - гамма / 131 499 ₴ - модульована IMRT). Обов'язкова наявність дозиметричного плану."
        },
        {
            "code": "11600-00",
            "name": "Діагностична та лікувальна колоноскопія з біопсією",
            "group_id": "grp-07",
            "group_name": "Ендоскопічні діагностичні та лікувальні процедури",
            "category": "Diagnostic",
            "base_norm_time": 45,
            "anesthesia": 1,
            "min_stay": 0,
            "max_stay": 1,
            "age_min": 40,
            "age_max": 120,
            "gender": "ALL",
            "packages": "13, 9, 47",
            "dsgs": "Пакет 13, Клас 54",
            "base_tariff": 1180.0,
            "notes": "Пріоритетний скринінг (Пакет 13 - 1 180 ₴). При виявленні поліпів обов'язкова поліпектомія та гістологія. Посада лікаря-ендоскопіста P58."
        },
        {
            "code": "31548-00",
            "name": "Секторальна резекція грудної залози (мамектомія)",
            "group_id": "grp-02",
            "group_name": "Онкологічні хірургічні втручання",
            "category": "Surgical",
            "base_norm_time": 90,
            "anesthesia": 1,
            "min_stay": 1,
            "max_stay": 7,
            "age_min": 18,
            "age_max": 120,
            "gender": "FEMALE",
            "packages": "4, 47, 3",
            "dsgs": "J01, G01",
            "base_tariff": 8735.0,
            "notes": "Органозберігаюча операція при пухлинах молочної залози (C50, D24). Вимагає термінового інтраопераційного гістологічного дослідження."
        },
        {
            "code": "90225-01",
            "name": "Екстракорпоральна мембранна оксигенація (ЕКМО, вено-артеріальна/вено-венозна)",
            "group_id": "grp-11",
            "group_name": "Інтенсивна терапія, реанімація та ЕКМО",
            "category": "Therapeutic",
            "base_norm_time": 1440,
            "anesthesia": 1,
            "min_stay": 3,
            "max_stay": 60,
            "age_min": 0,
            "age_max": 120,
            "gender": "ALL",
            "packages": "3, 4",
            "dsgs": "A40",
            "base_tariff": 177538.88,
            "notes": "Найвищий коефіцієнт складності ДСГ (20.325). Базова вартість 177 538.88 ₴ (тариф 97 646.38 ₴ при K=0.55). Вимагає консиліуму реаніматологів."
        },
        {
            "code": "39600-00",
            "name": "Дренування внутрішньочерепної гематоми шляхом краніотомії",
            "group_id": "grp-05",
            "group_name": "Нейрохірургія та спінальна хірургія",
            "category": "Surgical",
            "base_norm_time": 150,
            "anesthesia": 1,
            "min_stay": 5,
            "max_stay": 30,
            "age_min": 0,
            "age_max": 120,
            "gender": "ALL",
            "packages": "4, 5, 3",
            "dsgs": "B02, B02A",
            "base_tariff": 8735.0,
            "notes": "Ургентна нейрохірургія (інсульт з крововиливом I61 або ЧМТ S06). Ваговий коефіцієнт B02A = 11.0813 (тариф 53 237.34 ₴). Посада нейрохірурга P155."
        },
        {
            "code": "38218-00",
            "name": "Коронарна ангіопластика зі стентуванням (1 стент з лікарським покриттям)",
            "group_id": "grp-04",
            "group_name": "Кардіохірургія та інтервенційна кардіологія",
            "category": "Surgical",
            "base_norm_time": 90,
            "anesthesia": 0,
            "min_stay": 2,
            "max_stay": 10,
            "age_min": 18,
            "age_max": 120,
            "gender": "ALL",
            "packages": "6, 4",
            "dsgs": "F03, Пакет 6",
            "base_tariff": 44400.0,
            "notes": "Тарифікується за пріоритетним Пакетом 6 (Гострий інфаркт міокарда, 44 400 - 55 200 ₴). Обов'язкова наявність ангіографа та катетеризаційної лабораторії."
        },
        {
            "code": "93125-00",
            "name": "Індивідуальне заняття з ерготерапії та відновлення побутових навичок",
            "group_id": "grp-10",
            "group_name": "Реабілітаційні інтервенції та фізіотерапія",
            "category": "Rehabilitation",
            "base_norm_time": 60,
            "anesthesia": 0,
            "min_stay": 0,
            "max_stay": 21,
            "age_min": 0,
            "age_max": 120,
            "gender": "ALL",
            "packages": "54, 53, 25",
            "dsgs": "Пакет 54",
            "base_tariff": 10820.0,
            "notes": "Обов'язкова інтервенція за Пакетом 54/53. Надається ерготерапевтом (P_ERGO) у складі мультидисциплінарної команди (не менше 14 днів циклу)."
        }
    ]

    for s in services_data:
        cur.execute("""
        INSERT INTO pmg_service_catalog (
            service_code, name, group_id, group_name, category,
            base_norm_time_minutes, anesthesia_required, min_stay_days, max_stay_days,
            age_min, age_max, gender_restriction, package_ids, dsg_codes,
            base_tariff, clinical_norm_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            s["code"], s["name"], s["group_id"], s["group_name"], s["category"],
            s["base_norm_time"], s["anesthesia"], s["min_stay"], s["max_stay"],
            s["age_min"], s["age_max"], s["gender"], s["packages"], s["dsgs"],
            s["base_tariff"], s["notes"]
        ))

    # 4. Populate Service Combinations Matrix (Delphi dct_mp_service_odk_rule reengineering)
    print("4. Populating Service Combinations Matrix...")
    cur.execute("DELETE FROM pmg_service_combinations;")
    combinations = [
        {
            "id": "comb-32003-opt",
            "service_code": "32003-00",
            "name": "Оптимальна онкохірургічна комбінація: Геміколектомія при раку ободової кишки",
            "icd_codes": json.dumps([
                {"code": "C18.0", "name": "Злоякісне новоутворення сліпої кишки", "type": "PRIMARY"},
                {"code": "C18.2", "name": "Злоякісне новоутворення висхідної ободової кишки", "type": "PRIMARY"},
                {"code": "C18.3", "name": "Злоякісне новоутворення печінкового вигину ободової кишки", "type": "PRIMARY"}
            ], ensure_ascii=False),
            "mandatory_companions": json.dumps([
                {"code": "30075-01", "name": "Біопсія та резекція лімфатичних вузлів брижі (лімфодисекція)"},
                {"code": "30394-00", "name": "Дренування черевної порожнини"}
            ], ensure_ascii=False),
            "optional_multisurg": json.dumps([
                {"code": "30440-00", "name": "Симультанна холецистектомія (+30% за мультихірургію)"}
            ], ensure_ascii=False),
            "incompatible": json.dumps([
                {"code": "32000-00", "name": "Обмежена резекція кишки без анастомозу (дублювання втручання)"}
            ], ensure_ascii=False),
            "allowed_pos": json.dumps(["P157", "P158", "P58"], ensure_ascii=False),
            "prohibited_pos": json.dumps(["P122", "P101", "P115"], ensure_ascii=False),
            "pkg": "4",
            "dsg": "O0101",
            "weight": 5.070,
            "tariff": 24357.55,
            "formula": "8 735.00 ₴ × 5.070 × 0.55 = 24 357.55 ₴",
            "condition": "Постанова № 1808, Додаток 1. Обов'язкова гістологічна верифікація та посада P157 (Хірург-онколог).",
            "is_standard": 1
        },
        {
            "id": "comb-30061-opt",
            "service_code": "30061-02",
            "name": "Офтальмологічна амбулаторна комбінація: Травма рогівки",
            "icd_codes": json.dumps([
                {"code": "S05.0", "name": "Травма кон'юнктиви та садно рогівки без згадки про стороннє тіло", "type": "PRIMARY"},
                {"code": "T15.0", "name": "Стороннє тіло в рогівці", "type": "PRIMARY"},
                {"code": "H16.0", "name": "Виразка рогівки після травматизації", "type": "PRIMARY"}
            ], ensure_ascii=False),
            "mandatory_companions": json.dumps([], ensure_ascii=False),
            "optional_multisurg": json.dumps([
                {"code": "42650-00", "name": "Деепіталізація та обробка рогівки"}
            ], ensure_ascii=False),
            "incompatible": json.dumps([
                {"code": "42653-00", "name": "Повна наскрізна трансплантація рогівки (конфлікт обсягу)"}
            ], ensure_ascii=False),
            "allowed_pos": json.dumps(["P145", "P146", "P58"], ensure_ascii=False),
            "prohibited_pos": json.dumps(["P122", "P101"], ensure_ascii=False),
            "pkg": "47",
            "dsg": "ААС",
            "weight": 0.60,
            "tariff": 3144.60,
            "formula": "8 735.00 ₴ × 0.60 × 0.60 = 3 144.60 ₴",
            "condition": "Постанова № 1808, Додаток 2 (Хірургія 1 дня). Заборонена необґрунтована госпіталізація.",
            "is_standard": 1
        },
        {
            "id": "comb-30518-opt",
            "service_code": "30518-00",
            "name": "Абдомінальна онкорезекція: Дистальна резекція шлунка",
            "icd_codes": json.dumps([
                {"code": "C16.1", "name": "Злоякісне новоутворення дна шлунка", "type": "PRIMARY"},
                {"code": "C16.3", "name": "Злоякісне новоутворення воротаря шлунка", "type": "PRIMARY"},
                {"code": "K25.0", "name": "Гостра виразка шлунка з кровотечею", "type": "PRIMARY"}
            ], ensure_ascii=False),
            "mandatory_companions": json.dumps([
                {"code": "30075-00", "name": "Регіонарна лімфодисекція D2"},
                {"code": "30394-02", "name": "Дренування підпечінкового простору"}
            ], ensure_ascii=False),
            "optional_multisurg": json.dumps([
                {"code": "30440-00", "name": "Холецистектомія"}
            ], ensure_ascii=False),
            "incompatible": json.dumps([], ensure_ascii=False),
            "allowed_pos": json.dumps(["P157", "P58"], ensure_ascii=False),
            "prohibited_pos": json.dumps(["P122", "P101"], ensure_ascii=False),
            "pkg": "4",
            "dsg": "G03",
            "weight": 4.937,
            "tariff": 23720.08,
            "formula": "8 735.00 ₴ × 4.937 × 0.55 = 23 720.08 ₴",
            "condition": "Постанова № 1808, Додаток 1. Наказ МОЗ № 410 п. 4.1.",
            "is_standard": 1
        },
        {
            "id": "comb-96199-opt",
            "service_code": "96199-00",
            "name": "Протипухлинний хіміотерапевтичний цикл: Рак молочної залози / ШКТ",
            "icd_codes": json.dumps([
                {"code": "Z51.1", "name": "Сеанс хіміотерапії з приводу новоутворення (Обов'язковий основний)", "type": "PRIMARY"},
                {"code": "C50.9", "name": "Злоякісне новоутворення молочної залози (Супутній)", "type": "SECONDARY"},
                {"code": "C18.9", "name": "Злоякісне новоутворення ободової кишки (Супутній)", "type": "SECONDARY"}
            ], ensure_ascii=False),
            "mandatory_companions": json.dumps([
                {"code": "A34009", "name": "Загальний аналіз крові розгорнутий (перед введенням хіміопрепарату)"}
            ], ensure_ascii=False),
            "optional_multisurg": json.dumps([], ensure_ascii=False),
            "incompatible": json.dumps([], ensure_ascii=False),
            "allowed_pos": json.dumps(["P156", "P157", "P58"], ensure_ascii=False),
            "prohibited_pos": json.dumps(["P101"], ensure_ascii=False),
            "pkg": "18",
            "dsg": "Пакет 18",
            "weight": 1.0,
            "tariff": 17865.0,
            "formula": "Фіксований тариф Пакета 18 = 17 865.00 ₴ за цикл",
            "condition": "Глава 18 Постанови № 1808. Обов'язкова комбінація діагнозу Z51.1 + C-код в ЕСОЗ.",
            "is_standard": 1
        },
        {
            "id": "comb-11600-opt",
            "service_code": "11600-00",
            "name": "Пріоритетний скринінг: Колоноскопія пацієнтам 40+ років",
            "icd_codes": json.dumps([
                {"code": "K63.5", "name": "Поліп ободової кишки", "type": "PRIMARY"},
                {"code": "K58.0", "name": "Синдром подразненого кишечника", "type": "PRIMARY"},
                {"code": "Z12.1", "name": "Спеціальне скринінгове обстеження з метою виявлення пухлин ШКТ", "type": "PRIMARY"}
            ], ensure_ascii=False),
            "mandatory_companions": json.dumps([
                {"code": "30071-00", "name": "Біопсія слизової оболонки при виявленні змін"}
            ], ensure_ascii=False),
            "optional_multisurg": json.dumps([
                {"code": "32075-00", "name": "Ендоскопічна поліпектомія"}
            ], ensure_ascii=False),
            "incompatible": json.dumps([], ensure_ascii=False),
            "allowed_pos": json.dumps(["P58", "P157"], ensure_ascii=False),
            "prohibited_pos": json.dumps(["P122", "P101"], ensure_ascii=False),
            "pkg": "13",
            "dsg": "Пакет 13",
            "weight": 1.0,
            "tariff": 1180.0,
            "formula": "Тариф скринінгового Пакета 13 = 1 180.00 ₴",
            "condition": "Глава 13 Постанови № 1808. Вік пацієнта >= 40 років. Наявність електронного направлення.",
            "is_standard": 1
        },
        {
            "id": "comb-90225-opt",
            "service_code": "90225-01",
            "name": "Критична реанімація: Екстракорпоральна мембранна оксигенація (ЕКМО)",
            "icd_codes": json.dumps([
                {"code": "J96.0", "name": "Гостра респіраторна недостатність важкого ступеня", "type": "PRIMARY"},
                {"code": "I50.9", "name": "Серцева недостатність, кардіогенний шок", "type": "PRIMARY"}
            ], ensure_ascii=False),
            "mandatory_companions": json.dumps([
                {"code": "13882-01", "name": "Безперервна допоміжна ШВЛ > 96 годин"},
                {"code": "13839-00", "name": "Катетеризація центральної вени та артерії"}
            ], ensure_ascii=False),
            "optional_multisurg": json.dumps([], ensure_ascii=False),
            "incompatible": json.dumps([], ensure_ascii=False),
            "allowed_pos": json.dumps(["P154", "P157"], ensure_ascii=False),
            "prohibited_pos": json.dumps(["P122", "P101"], ensure_ascii=False),
            "pkg": "3",
            "dsg": "A40",
            "weight": 20.325,
            "tariff": 97646.38,
            "formula": "8 735.00 ₴ × 20.325 × 0.55 = 97 646.38 ₴",
            "condition": "Додаток 1 до Постанови № 1808 (ДСГ A40). Максимальний коефіцієнт реанімації.",
            "is_standard": 1
        }
    ]

    for c in combinations:
        cur.execute("""
        INSERT INTO pmg_service_combinations (
            id, service_code, combination_name, compatible_icd_codes,
            mandatory_companions, optional_multisurg_companions, incompatible_services,
            allowed_doctor_positions, prohibited_doctor_positions,
            expected_package_number, expected_dsg_code, weight_coef, calculated_tariff,
            calculation_formula, rule_condition, is_library_standard
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["id"], c["service_code"], c["name"], c["icd_codes"],
            c["mandatory_companions"], c["optional_multisurg"], c["incompatible"],
            c["allowed_pos"], c["prohibited_pos"],
            c["pkg"], c["dsg"], c["weight"], c["tariff"],
            c["formula"], c["condition"], c["is_standard"]
        ))

    conn.commit()
    print("Catalog tables successfully populated in SQLite!")

    # 5. Export into SQL file sql/11_seed_service_combinations_and_groups.sql
    print("5. Generating sql/11_seed_service_combinations_and_groups.sql...")
    sql_path = r'c:\__MEDLINK___\PMG\sql\11_seed_service_combinations_and_groups.sql'
    with open(sql_path, 'w', encoding='utf-8') as f:
        f.write("-- =====================================================================\n")
        f.write("-- MEDLINK PMG 2026: SERVICE CATALOG, CLINICAL NORMS & COMBINATIONS MATRIX\n")
        f.write("-- Re-engineered from Delphi MedProfit Legacy System (service_groups, dct_rules)\n")
        f.write("-- =====================================================================\n\n")
        
        f.write("CREATE TABLE IF NOT EXISTS pmg_service_groups (\n")
        f.write("    id TEXT PRIMARY KEY,\n    code TEXT NOT NULL,\n    name TEXT NOT NULL,\n")
        f.write("    parent_id TEXT,\n    level INTEGER DEFAULT 1,\n    description TEXT\n);\n\n")

        f.write("CREATE TABLE IF NOT EXISTS pmg_service_catalog (\n")
        f.write("    service_code TEXT PRIMARY KEY,\n    name TEXT NOT NULL,\n    group_id TEXT,\n")
        f.write("    group_name TEXT,\n    category TEXT NOT NULL,\n    base_norm_time_minutes INTEGER DEFAULT 60,\n")
        f.write("    anesthesia_required INTEGER DEFAULT 0,\n    min_stay_days INTEGER DEFAULT 0,\n")
        f.write("    max_stay_days INTEGER DEFAULT 14,\n    age_min INTEGER DEFAULT 0,\n    age_max INTEGER DEFAULT 120,\n")
        f.write("    gender_restriction TEXT DEFAULT 'ALL',\n    package_ids TEXT,\n    dsg_codes TEXT,\n")
        f.write("    base_tariff REAL DEFAULT 8735.0,\n    clinical_norm_notes TEXT\n);\n\n")

        f.write("CREATE TABLE IF NOT EXISTS pmg_service_combinations (\n")
        f.write("    id TEXT PRIMARY KEY,\n    service_code TEXT NOT NULL,\n    combination_name TEXT NOT NULL,\n")
        f.write("    compatible_icd_codes TEXT NOT NULL,\n    mandatory_companions TEXT,\n")
        f.write("    optional_multisurg_companions TEXT,\n    incompatible_services TEXT,\n")
        f.write("    allowed_doctor_positions TEXT NOT NULL,\n    prohibited_doctor_positions TEXT NOT NULL,\n")
        f.write("    expected_package_number TEXT NOT NULL,\n    expected_dsg_code TEXT NOT NULL,\n")
        f.write("    weight_coef REAL NOT NULL,\n    calculated_tariff REAL NOT NULL,\n")
        f.write("    calculation_formula TEXT NOT NULL,\n    rule_condition TEXT,\n    is_library_standard INTEGER DEFAULT 1\n);\n\n")

        # Inserts for groups
        f.write("-- Seed 12 Service Groups\n")
        for g in groups:
            desc_esc = g[5].replace("'", "''")
            f.write(f"INSERT OR REPLACE INTO pmg_service_groups (id, code, name, parent_id, level, description) VALUES ('{g[0]}', '{g[1]}', '{g[2]}', NULL, {g[4]}, '{desc_esc}');\n")
        f.write("\n")

        # Inserts for services
        f.write("-- Seed Services Catalog with Norms\n")
        for s in services_data:
            name_esc = s["name"].replace("'", "''")
            notes_esc = s["notes"].replace("'", "''")
            f.write(f"INSERT OR REPLACE INTO pmg_service_catalog (service_code, name, group_id, group_name, category, base_norm_time_minutes, anesthesia_required, min_stay_days, max_stay_days, age_min, age_max, gender_restriction, package_ids, dsg_codes, base_tariff, clinical_norm_notes) VALUES ('{s['code']}', '{name_esc}', '{s['group_id']}', '{s['group_name']}', '{s['category']}', {s['base_norm_time']}, {s['anesthesia']}, {s['min_stay']}, {s['max_stay']}, {s['age_min']}, {s['age_max']}, '{s['gender']}', '{s['packages']}', '{s['dsgs']}', {s['base_tariff']}, '{notes_esc}');\n")
        f.write("\n")

        # Inserts for combinations
        f.write("-- Seed Service Combinations Matrix\n")
        for c in combinations:
            name_esc = c["name"].replace("'", "''")
            icd_esc = c["icd_codes"].replace("'", "''")
            mand_esc = c["mandatory_companions"].replace("'", "''")
            opt_esc = c["optional_multisurg"].replace("'", "''")
            inc_esc = c["incompatible"].replace("'", "''")
            pos_esc = c["allowed_pos"].replace("'", "''")
            proh_esc = c["prohibited_pos"].replace("'", "''")
            cond_esc = c["condition"].replace("'", "''")
            f.write(f"INSERT OR REPLACE INTO pmg_service_combinations (id, service_code, combination_name, compatible_icd_codes, mandatory_companions, optional_multisurg_companions, incompatible_services, allowed_doctor_positions, prohibited_doctor_positions, expected_package_number, expected_dsg_code, weight_coef, calculated_tariff, calculation_formula, rule_condition, is_library_standard) VALUES ('{c['id']}', '{c['service_code']}', '{name_esc}', '{icd_esc}', '{mand_esc}', '{opt_esc}', '{inc_esc}', '{pos_esc}', '{proh_esc}', '{c['pkg']}', '{c['dsg']}', {c['weight']}, {c['tariff']}, '{c['formula']}', '{cond_esc}', {c['is_standard']});\n")

    conn.close()
    print(f"File {sql_path} generated successfully!")

if __name__ == '__main__':
    build_service_catalog()
