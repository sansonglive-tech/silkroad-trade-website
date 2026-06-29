import re

with open(r"C:\Users\ASDCF\.qclaw\workspace\silkroad-trade_v7_silk_poster.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find key sections
patterns = [
    ("统计数字(60+)", r"60\+.*一带一路覆盖"),
    ("服务流程", r"服务流程|pstep"),
    ("客户心声/评价", r"客户心声|testimonials"),
    ("政策解读", r"政策解读|policy"),
    ("CTA区", r"class=\"cta"),
]

for name, pat in patterns:
    m = re.search(pat, html)
    if m:
        start = max(0, m.start() - 60)
        end = min(len(html), m.start() + 300)
        ctx = html[start:end].replace("\n", " ")[:300]
        print(f"=== {name} at {m.start()} ===")
        print(f"  {ctx}...")
        print()
