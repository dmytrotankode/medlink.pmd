with open(r"C:\Projects\MedProfit\fMain.pas", "r", encoding="windows-1251", errors="ignore") as f:
    lines = f.readlines()

print("--- LINES 2040 to 2200 ---")
for i in range(2040, min(2200, len(lines))):
    print(f"L{i+1}: {lines[i].rstrip()}")

print("\n--- LINES 2580 to 2694 ---")
for i in range(2580, len(lines)):
    print(f"L{i+1}: {lines[i].rstrip()}")
