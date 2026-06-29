#!/usr/bin/env python3
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/ASDCF/.qclaw/workspace/silkroad-trade_v7_silk_poster.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Test each extraction
tests = [
    ("services", 'id="services"', 'services-grid'),
    ("policy", 'id="policy"', 'policy-grid'),
    ("testimonials", 'id="testimonials"', 'testimonials-grid'),
    ("process", 'id="process"', 'process-grid'),
]

for name, id_marker, grid in tests:
    idx = h.find(id_marker)
    if idx < 0:
        print(f"[{name}] section id NOT found")
        continue
    sec_end = h.find('</section>', idx)
    sec = h[idx:sec_end]
    # grid pattern
    pat = rf'<div\s+class="{grid}">(.*?)</div>'
    m = re.search(pat, sec, re.DOTALL)
    if m:
        print(f"[{name}] FOUND: {len(m.group(1))} chars")
    else:
        print(f"[{name}] NOT FOUND in section")
        # try case-sensitive
        if grid in sec:
            print(f"[{name}] marker IS in section but regex didn't match")
            pos = sec.find(grid)
            print(f"    context: {sec[pos-20:pos+80]}")
        else:
            print(f"[{name}] marker NOT in section")

# Stats banner
m = re.search(r'class="stats-banner"[^>]*>(.*?)</section>', h, re.DOTALL)
if m:
    inner_m = re.search(r'<div\s+class="stats-inner">(.*?)</div>', m.group(1), re.DOTALL)
    if inner_m:
        nums = re.findall(r'<div class="num">([^<]+)<', inner_m.group(1))
        print(f"[stats] FOUND: {len(inner_m.group(1))} chars, {len(nums)} items")
    else:
        print("[stats] stats-inner NOT FOUND in banner section")
else:
    print("[stats] stats-banner NOT FOUND")
