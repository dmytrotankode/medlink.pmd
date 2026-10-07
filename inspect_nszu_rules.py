with open("c:/__MEDLINK___/PMG/downloaded_js/js_nszu-analyzer-compiled.js", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

print("--- Header & templates part of nszu analyzer ---")
print(text[:4000])

print("\n--- Additional Requirements logic ---")
idx = text.find('class AdditionalRequirements')
if idx != -1:
    print(text[idx:idx+3000])
else:
    idx2 = text.find('AdditionalRequirements')
    print(text[idx2:idx2+2000])
