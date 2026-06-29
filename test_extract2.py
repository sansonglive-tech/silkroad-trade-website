#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/ASDCF/.qclaw/workspace/silkroad-trade_v7_silk_poster.html','r',encoding='utf-8') as f:
    h = f.read()

m = re.search(r'<div class="services-grid">(.*?)</div>\s*</section>', h, re.DOTALL)
if m:
    inner = m.group(1)
    print(f"services-grid inner: {len(inner)} chars")
    print("First 500 chars:")
    print(inner[:500])
