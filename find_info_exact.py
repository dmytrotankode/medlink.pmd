with open("c:/__MEDLINK___/PMG/downloaded_js/js_stac-compiled.js", "r", encoding="utf-8") as f:
    text = f.read()

idx = 0
while True:
    idx = text.find('info/', idx)
    if idx == -1:
        break
    print("Match at", idx, ":", text[max(0, idx-50):min(len(text), idx+100)])
    idx += 5
