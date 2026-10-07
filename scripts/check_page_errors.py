import asyncio
import subprocess
import time
import urllib.request
import json
import websockets
import sys

async def check():
    sys.stdout.reconfigure(encoding='utf-8')
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    proc = subprocess.Popen([chrome_path, '--headless', '--remote-debugging-port=9227', '--disable-gpu', 'http://localhost:8085/prototype_medlink/index.html'])
    await asyncio.sleep(2.5)

    try:
        tabs = json.loads(urllib.request.urlopen('http://localhost:9227/json').read())
        ws_url = tabs[0]['webSocketDebuggerUrl']
        async with websockets.connect(ws_url, max_size=10*1024*1024) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Log.enable'}))
            await ws.send(json.dumps({'id': 2, 'method': 'Console.enable'}))
            await ws.send(json.dumps({'id': 3, 'method': 'Network.enable'}))

            # Evaluate state
            eval_req = {
                'id': 10,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': """
                    JSON.stringify({
                        title: document.title,
                        vueMounted: !!document.querySelector('#q-app').__vue__,
                        currentView: document.querySelector('#q-app').__vue__ ? document.querySelector('#q-app').__vue__.currentView : null,
                        packagesCount: document.querySelector('#q-app').__vue__ ? (document.querySelector('#q-app').__vue__.allPackages || []).length : 0,
                        errors: window.__errors || []
                    })
                    """
                }
            }
            await ws.send(json.dumps(eval_req))

            for _ in range(10):
                msg = json.loads(await ws.recv())
                if msg.get('id') == 10:
                    print("Vue App Status:", msg.get('result', {}).get('result', {}).get('value'))
                if msg.get('method') == 'Console.messageAdded':
                    print("Console msg:", msg.get('params', {}).get('message', {}).get('text'))
                if msg.get('method') == 'Network.loadingFailed':
                    print("Network FAIL:", msg.get('params'))

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(check())
