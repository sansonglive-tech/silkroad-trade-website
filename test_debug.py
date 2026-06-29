import sys, re, traceback
sys.stdout.reconfigure(encoding="utf-8")

with open(r"C:\Users\ASDCF\.qclaw\workspace\silkroad-trade_v7_silk_poster.html", encoding="utf-8") as f:
    html = f.read()

try:
    idx = html.find("stats-banner")
    if idx >= 0:
        ctx = html[idx:idx+300]
        print(f"OK stats-banner at {idx}")
        print(repr(ctx))
    else:
        print("NOT FOUND")
except Exception as e:
    traceback.print_exc()
