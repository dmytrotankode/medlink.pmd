with open("c:/__MEDLINK___/PMG/downloaded_js/js_stac-compiled.js", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("App.modalManager.showIframe('/serve.php?f=info/'")
print(text[max(0, idx-300):min(len(text), idx+200)])
