import re

def inspect():
    pas_path = r"C:\Projects\MedProfit\fMain.pas"
    dfm_path = r"C:\Projects\MedProfit\fMain.dfm"

    print("=== INSPECTING fMain.pas ===")
    with open(pas_path, "r", encoding="windows-1251", errors="ignore") as f:
        pas_content = f.read()
        pas_lines = pas_content.splitlines()

    print(f"Total lines in fMain.pas: {len(pas_lines)}")

    keywords = [
        "послуг", "услуг", "норм", "методик", "комбінац", "комбинац",
        "правил", "правило", "умови", "умова", "критер", "sprav",
        "картк", "карточк", "діагноз", "інтервенц", "перелік", "справочник",
        "posluga", "usluga", "method", "combination", "tree", "node", "detail"
    ]

    found_sections = []
    for i, line in enumerate(pas_lines):
        line_lower = line.lower()
        if any(k in line_lower for k in keywords):
            # check if it's procedure or significant code
            found_sections.append((i+1, line.strip()))

    print(f"Found {len(found_sections)} matching lines in fMain.pas.")
    print("\n--- SAMPLE PROCEDURES & CODE FRAGMENTS ---")
    proc_matches = [item for item in found_sections if item[1].lower().startswith(("procedure", "function", "type", "select", "sql", "//"))]
    for line_num, txt in proc_matches[:40]:
        print(f"L{line_num}: {txt}")

    print("\n=== INSPECTING fMain.dfm ===")
    with open(dfm_path, "r", encoding="windows-1251", errors="ignore") as f:
        dfm_content = f.read()
        dfm_lines = dfm_content.splitlines()

    print(f"Total lines in fMain.dfm: {len(dfm_lines)}")
    dfm_components = []
    for i, line in enumerate(dfm_lines):
        if any(k in line.lower() for k in ["object", "caption", "sql.strings", "itemname"]):
            if any(k in line.lower() for k in ["послуг", "услуг", "норм", "методик", "тариф", "дсг", "пакет", "правил", "довідн", "справочн"]):
                dfm_components.append((i+1, line.strip()))

    print(f"Found {len(dfm_components)} matching lines in fMain.dfm:")
    for line_num, txt in dfm_components[:40]:
        print(f"L{line_num}: {txt}")

if __name__ == "__main__":
    inspect()
