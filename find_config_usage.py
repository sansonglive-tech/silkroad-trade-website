import re
with open(r"C:\Users\ASDCF\.qclaw\workspace\silkroad-trade_v7_silk_poster.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "CONFIG." in line or "CONFIG[" in line or ("CONFIG" in line and "SLIDE_CONFIG" not in line and "const CONFIG" not in line):
        print(f"L{i+1}: {line.rstrip()[:250]}")
