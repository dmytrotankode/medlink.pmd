with open("c:/__MEDLINK___/PMG/downloaded_js/js_nszu-analyzer-compiled.js", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

idx = text.find('blobUrl')
print(text[max(0, idx-100):min(len(text), idx+1000)])
