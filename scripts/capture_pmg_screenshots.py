import asyncio
import subprocess
import time
import urllib.request
import json
import os
import base64
import websockets
import sys

SCREENSHOT_DIR = r"c:\__MEDLINK___\PMG\screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

VIEWS_TO_CAPTURE = [
    {
        "name": "01_import_and_file_parsing",
        "action": """
            var vm = document.querySelector('#q-app').__vue__;
            vm.currentView = 'openxml-import';
            vm.currentViewTitle = 'Потоковий імпорт та аналіз звітів НСЗУ (OpenXML & SAX)';
        """,
        "desc": "Потоковий імпорт OpenXML без OutOfMemory: реальний розбір звітів (5 490 ЕМЗ ОЦО та 4 394 ЕМЗ ДКЛ Святої Зінаїди) за 5 стадіями"
    },
    {
        "name": "02_audit_dashboard_45_columns",
        "action": """
            var vm = document.querySelector('#q-app').__vue__;
            vm.currentView = 'audit';
            vm.currentViewTitle = 'Аудит 45 колонок звіту НСЗУ та автономний розрахунок тарифів';
        """,
        "desc": "Аудит офіційного вивантаження НСЗУ (45 колонок): автономний розрахунок тарифів за Постановою № 1808 (8 735 ₴ × Wg × 0.55/0.60)"
    },
    {
        "name": "03_two_way_reconciliation",
        "action": """
            var vm = document.querySelector('#q-app').__vue__;
            vm.currentView = 'reconciliation';
            vm.currentViewTitle = 'Двостороння 2-Way звірка з ЕМЗ МІС Медлінк';
        """,
        "desc": "Двостороння 2-Way звірка за Encounter.EhealthId: автоматичне виявлення «Прихованої дефектури» (відхилення в eHealth зі статусом 0 ₴)"
    },
    {
        "name": "04_discrepancies_and_lost_revenue",
        "action": """
            var vm = document.querySelector('#q-app').__vue__;
            vm.currentView = 'discrepancies';
            vm.currentViewTitle = 'Журнал відхилених записів та втраченого доходу (Lost Revenue)';
        """,
        "desc": "Журнал відхилених записів: 714 помилок дефектури, калькулятор втраченого доходу (4 974 842 ₴) та швидкий перехід до 2-Way виправлення"
    },
    {
        "name": "05_doctors_and_departments_report",
        "action": """
            var vm = document.querySelector('#q-app').__vue__;
            vm.currentView = 'doctors';
            vm.currentViewTitle = 'Зведений звіт за лікарями та відділеннями (Аналог аркуша «Звіт»)';
        """,
        "desc": "Зведений звіт за відділеннями та персоналом (аркуш «Звіт»): рейтинг лікарів за сумою підтверджених виплат та часткою дефектури"
    },
    {
        "name": "06_doctor_prebilling_assistant",
        "action": """
            var vm = document.querySelector('#q-app').__vue__;
            vm.currentView = 'prebilling';
            vm.currentViewTitle = 'АРМ Лікаря — Пре-білінг та захист від дефектури (Anti-Defektura)';
        """,
        "desc": "АРМ лікаря у Медлінку: пре-білінг симулятор у картці взаємодії лікаря, онлайн-валідація ДСГ та блокування дефектури (Anti-Defektura)"
    },
    {
        "name": "07_all_46_packages_catalog",
        "action": """
            var vm = document.querySelector('#q-app').__vue__;
            vm.currentView = 'catalog-packages';
            vm.currentViewTitle = 'Класифікатор усіх 46 медичних пакетів ПМГ-2026 (Постанова № 1808)';
        """,
        "desc": "Вичерпний реєстр усіх 46 пакетів ПМГ-2026: 12 клініко-економічних кластерів, базові ставки, формули та прямий доступ до нормативних досьє"
    },
    {
        "name": "08_normative_dossier_modal",
        "action": """
            var vm = document.querySelector('#q-app').__vue__;
            vm.currentView = 'catalog-packages';
            vm.openNormativeDossier(vm.allPmgPackages[3]);
        """,
        "desc": "Автономне нормативне досьє пакета ПМГ: юридичні статті Постанови № 1808, вагові коефіцієнти ДСГ, критерії входу та eHealth валідації"
    },
    {
        "name": "09_service_catalog_norms_matrix",
        "action": """
            var vm = document.querySelector('#q-app').__vue__;
            vm.packageDossierDialog = false;
            vm.currentView = 'catalog-services';
            vm.currentViewTitle = 'Справочник послуг (АКПІ) та клінічні норми';
        """,
        "desc": "Справочник послуг АКПІ: 12 клінічних груп, норми часу, типи анестезії, межі ліжко-днів, вікові та кваліфікаційні вимоги до лікаря"
    },
    {
        "name": "10_service_combination_validator",
        "action": """
            var vm = document.querySelector('#q-app').__vue__;
            vm.openServiceCard('32003-00');
            vm.activeServiceTab = 'tab-combinations';
        """,
        "desc": "Матриця комбінацій та валідатор (Delphi re-engineering): підвищувальний коефіцієнт мультихірургії 1.30, обов'язкові супутні коди та еталони myAddLib"
    },
    {
        "name": "11_patient_drilldown_45_modal",
        "action": """
            var vm = document.querySelector('#q-app').__vue__;
            vm.detailedServiceCardDialog = false;
            vm.currentView = 'audit';
            vm.openDetails45(vm.statementLines[0]);
        """,
        "desc": "Інспектор 45 колонок аркуша «Розшифровка»: наскрізний drill-down до реального ЕМЗ пацієнта з клінічними датами, посадами та конфліктами"
    },
    {
        "name": "12_correction_modal_2way",
        "action": """
            var vm = document.querySelector('#q-app').__vue__;
            vm.details45Dialog = false;
            vm.currentView = 'discrepancies';
            vm.openCorrectionModal(vm.rejectedLines[0]);
        """,
        "desc": "2-Way AI Асистент виправлення: підказка причини відхилення, підбір правильного АКПІ/МКХ-10 в 1 клік та розрахунок відновленого фінансування (+24 357 ₴)"
    }
]

async def capture():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=== STARTING CHROMIUM HEADLESS CAPTURE ===")

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    port = 9225

    # Launch Chrome headless with remote debugging
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        f"--remote-debugging-port={port}",
        "--window-size=1600,1050",
        "http://localhost:8085/prototype_medlink/index.html"
    ]
    proc = subprocess.Popen(cmd)
    print(f"Launched Chrome (PID: {proc.pid}) on port {port}")
    await asyncio.sleep(3)

    try:
        # Discover debug websocket url
        url = f"http://localhost:{port}/json"
        req = urllib.request.urlopen(url)
        tabs = json.loads(req.read().decode('utf-8'))
        page_tab = next(t for t in tabs if "prototype_medlink" in t.get("url", ""))
        ws_url = page_tab["webSocketDebuggerUrl"]
        print(f"Connected to DevTools: {ws_url}")

        async with websockets.connect(ws_url, max_size=50*1024*1024) as ws:
            await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
            await ws.send(json.dumps({"id": 2, "method": "Page.enable"}))
            await ws.send(json.dumps({
                "id": 3,
                "method": "Emulation.setDeviceMetricsOverride",
                "params": {"width": 1600, "height": 1050, "deviceScaleFactor": 1, "mobile": False}
            }))
            await asyncio.sleep(2)

            msg_id = 10
            for idx, item in enumerate(VIEWS_TO_CAPTURE, start=1):
                msg_id += 1
                # Evaluate action script
                await ws.send(json.dumps({
                    "id": msg_id,
                    "method": "Runtime.evaluate",
                    "params": {"expression": item["action"]}
                }))
                await asyncio.sleep(1.2)

                # Capture screenshot
                msg_id += 1
                await ws.send(json.dumps({
                    "id": msg_id,
                    "method": "Page.captureScreenshot",
                    "params": {"format": "png"}
                }))

                # Wait for response
                while True:
                    resp = await ws.recv()
                    data = json.loads(resp)
                    if data.get("id") == msg_id:
                        img_bytes = base64.b64decode(data["result"]["data"])
                        out_path = os.path.join(SCREENSHOT_DIR, f"{item['name']}.png")
                        with open(out_path, "wb") as f:
                            f.write(img_bytes)
                        print(f"  [{idx}/12] Captured: {item['name']}.png ({len(img_bytes):,} bytes)")
                        break

    except Exception as e:
        print(f"Error during capture: {e}")
    finally:
        proc.terminate()
        print("Chrome process terminated. Capture finished.")

if __name__ == '__main__':
    asyncio.run(capture())
