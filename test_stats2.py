import sys, re
sys.stdout.reconfigure(encoding="utf-8")

with open(r"C:\Users\ASDCF\.qclaw\workspace\silkroad-trade_v7_silk_poster.html", encoding="utf-8") as f:
    html = f.read()

# Find all HTML <section> tags
for m in re.finditer(r'<section\s+([^>]*)>', html):
    attr = m.group(1)
    if 'stats' in attr or 'stat' in attr:
        print(f"STATS section: <section {attr}>")
    if 'banner' in attr:
        print(f"BANNER section: <section {attr}>")
