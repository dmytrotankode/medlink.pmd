with open("c:/__MEDLINK___/PMG/downloaded_js/js_pkg54-compiled.js", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("showIframe")
while idx != -1:
    print(text[max(0, idx-200):min(len(text), idx+200)])
    print("-" * 50)
    idx = text.find("showIframe", idx+1)
