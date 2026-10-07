with open("c:/__MEDLINK___/PMG/prototype/prototype_data.json", "r", encoding="utf-8") as f:
    raw_json = f.read()

with open("c:/__MEDLINK___/PMG/prototype/data.js", "w", encoding="utf-8") as f:
    f.write("window.PROTOTYPE_DATA = " + raw_json + ";\n")

print("Created data.js with window.PROTOTYPE_DATA")
