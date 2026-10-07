import re

with open(r"C:\Projects\MedProfit\fMain.dfm", "r", encoding="windows-1251", errors="ignore") as f:
    text = f.read()

# Find SQL.Strings blocks for myCost, myDetailAnalysis, myInstrDiagn, myConsultTreatm
target_queries = ['myCost', 'myDetailAnalysis', 'myInstrDiagnCost', 'myConsultTreatmCost', 'myProceduresCost']

for q in target_queries:
    pos = text.find(f'object {q}:')
    if pos != -1:
        sql_pos = text.find('SQL.Strings = (', pos)
        if sql_pos != -1 and sql_pos - pos < 500:
            end_pos = text.find(')', sql_pos)
            print(f"=== SQL for {q} ===")
            print(text[sql_pos:end_pos+1][:1500])
