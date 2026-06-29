import sys, re
sys.stdout.reconfigure(encoding="utf-8")
with open("C:/Users/ASDCF/.qclaw/workspace/silkroad-trade_v7_silk_poster.html", "r", encoding="utf-8") as f:
    html = f.read()
m = re.search(r"<section\s+class=\"stats-banner\"[^>]*>(.*?)</section>", html, re.DOTALL)
if m:
    print("stats found")
    im = re.search(r"<div\s+class=\"stats-inner\">(.*?)</div>", m.group(1), re.DOTALL)
    if im: print("stats inner found:", len(im.group(1)))
    else: print("stats inner MISS")
else:
    print("stats MISSING")
