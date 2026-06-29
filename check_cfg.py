import sys, re
sys.stdout.reconfigure(encoding="utf-8")
with open(r"C:\Users\ASDCF\.qclaw\workspace\silkroad-trade_v7_silk_poster.html", "r", encoding="utf-8") as f:
    html = f.read()

m = re.search(r"const\s+CONFIG\s*=\s*(\{[^;]+\});", html, re.DOTALL)
if m:
    cfg = m.group(1)
    print(f"CONFIG found, len={len(cfg)}")
    print("==START==")
    print(cfg[:400])
    print("==...==")
    print(cfg[-400:])
else:
    print("CONFIG not found, trying other searches")
    for p in ["companyName", "company", "name:"]:
        i = html.find(p)
        if i >= 0:
            print(f"'{p}' at {i}: {html[max(0,i-20):i+80]}")
