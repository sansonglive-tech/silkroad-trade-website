#!/usr/bin/env python3
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/ASDCF/.qclaw/workspace/silkroad-trade_v7_silk_poster.html','r',encoding='utf-8') as f:
    h = f.read()

# Find all <section tags to see what ids they use
for m in re.finditer(r'<section\s+[^>]*>', h):
    tag = m.group()
    if 'id=' in tag:
        # extract id
        idm = re.search(r'id="([^"]+)"', tag)
        if idm:
            print(f'  SECTION id="{idm.group(1)}" at {m.start()}')
