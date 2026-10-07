with open("c:/__MEDLINK___/PMG/downloaded_js/js_nszu-analyzer-compiled.js", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

idx = text.find('analyzeWithProgress(')
while idx != -1:
    print(text[max(0, idx-50):min(len(text), idx+1000)])
    print("=" * 60)
    idx = text.find('analyzeWithProgress(', idx+1)
