#!/usr/bin/env python3
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/ASDCF/.qclaw/workspace/silkroad-trade_v7_silk_poster.html','r',encoding='utf-8') as f:
    h = f.read()

# Find where "policies" and "stats" appear in HTML body (not CSS)
for term in ['policies', 'stats', 'policy-overview']:
    indices = [i for i in range(len(h)) if h.startswith(term, i)]
    print(f'\n=== "{term}" at positions: {indices[:5]} ===')
    for idx in indices[:2]:
        print(f'  Context: {h[idx-40:idx+80]}')

# Also search for "Policies" and "Stats" in heading tags
for m in re.finditer(r'class="label-tag"[^>]*>.*?<div class="txt">([^<]+)<', h, re.DOTALL):
    print(f'  Label tag: {m.group(1)}')
