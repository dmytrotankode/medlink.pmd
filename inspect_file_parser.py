import re

with open("c:/__MEDLINK___/PMG/downloaded_js/js_nszu-analyzer-compiled.js", "r", encoding="utf-8") as f:
    text = f.read()

# Let's see the occurrences of formData or analyze-nszu
for m in re.finditer(r'(formData|analyze-nszu|XLSX|readAsArrayBuffer|readAsBinaryString)', text, re.I):
    idx = m.start()
    print(f"\n--- Match '{m.group(0)}' at {idx} ---")
    print(text[max(0, idx-100):min(len(text), idx+300)])
