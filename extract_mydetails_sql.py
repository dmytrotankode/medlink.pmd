with open(r"C:\Projects\MedProfit\fMain.dfm", "r", encoding="windows-1251", errors="ignore") as f:
    text = f.read()

pos = text.find('object myDetails:')
if pos != -1:
    sql_pos = text.find('SQL.Strings = (', pos)
    end_pos = text.find(')', sql_pos)
    print("=== myDetails SQL ===")
    print(text[sql_pos:end_pos+1][:2000])

pos2 = text.find('object myPatients:')
if pos2 != -1:
    sql_pos2 = text.find('SQL.Strings = (', pos2)
    end_pos2 = text.find(')', sql_pos2)
    print("=== myPatients SQL ===")
    print(text[sql_pos2:end_pos2+1][:2000])
