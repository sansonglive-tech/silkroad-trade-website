#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/ASDCF/.qclaw/workspace/silkroad-trade_v7_silk_poster.html','r',encoding='utf-8') as f:
    h = f.read()

# Print each section's opening and close pattern
sections = {
    'services': 'services-grid',
    'stats': 'stats-inner',
    'policies': 'policy-grid',
    'testimonials': 'testimonials-grid',
    'process': 'process-grid',
}

for name, marker in sections.items():
    idx = h.find(marker)
    if idx >= 0:
        print(f"\n=== {name} (at {idx}) ===")
        print(h[idx:idx+80])

# Also print the cards/items structure
# Services: look at first card
print("\n\n=== First service card HTML ===")
m = re.search(r'<div class="services-grid">(.*?)</section>', h, re.DOTALL)
if m:
    inner = m.group(1)
    # Look at structure
    cards = re.findall(r'<div class="service-card', inner)
    print(f"Found {len(cards)} 'service-card' occurrences")
    # Get the first card - it starts with <div class="service-card" and ends before the next one
    parts = re.split(r'(?=<div class="service-card)', inner)
    for i, p in enumerate(parts):
        if p.strip():
            print(f"Part {i}: {p[:150]}...")
            if i >= 2: break

print("\n\n=== Policy cards ===")
m = re.search(r'<div class="policy-grid">(.*?)</div>\s*</div>\s*</div>', h, re.DOTALL)
if m:
    print(f"Found, inner len: {len(m.group(1))}")
    count = m.group(1).count('policy-card')
    print(f"policy-card count: {count}")

# Testimonials
print("\n\n=== Testimonials ===")
m = re.search(r'testimonials-grid">(.*?)</section>', h, re.DOTALL)
if m:
    inner = m.group(1)
    print(f"Inner len: {len(inner)}")
    print(f"t-card count: {inner.count('t-card')}")
    # Find closing </section> position
    start = h.find('testimonials-grid')
    sec_close = h.find('</section>', start)
    print(f"grid starts at {start}, section close at {sec_close}")
    print(f"Content between: {h[start:sec_close+10][:200]}...")
