import sys, re
sys.stdout.reconfigure(encoding="utf-8")

with open(r"C:\Users\ASDCF\.qclaw\workspace\silkroad-trade_v7_silk_poster.html", encoding="utf-8") as f:
    html = f.read()

# Find all section tags and their classes
for m in re.finditer(r'<section\s+([^>]*)>', html):
    attr = m.group(1)
    if 'stats' in attr:
        print(f"stats section: <section {attr}>")
        break
else:
    print("No stats section tag found")
    
# Find stats class in HTML (not CSS)
idx = html.find('stats-banner')
if idx >= 0:
    # Look backwards for <section
    before = html[max(0,idx-50):idx]
    print(f"Before stats-banner: {repr(before)}")
    
# Find actual HTML around stats
idx2 = html.find('stats-inner')
if idx2 >= 0:
    after = html[idx2:idx2+200]
    before = html[max(0,idx2-100):idx2]
    print(f"Before stats-inner: {repr(before)}")
    print(f"After stats-inner: {repr(after[:100])}")
