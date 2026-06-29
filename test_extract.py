#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/ASDCF/.qclaw/workspace/silkroad-trade_v7_silk_poster.html','r',encoding='utf-8') as f:
    h = f.read()

# 测试服务卡片提取
m = re.search(r'<div class="services-grid">(.*?)</div>\s*</section>', h, re.DOTALL)
if m:
    print('services-grid FOUND, inner:', len(m.group(1)))
    cards = re.findall(r'<div class="service-card" onclick="([^"]+)">(.*?)</div>\s*</div>', m.group(1), re.DOTALL)
    print('cards count:', len(cards))
    for i, (click, ch) in enumerate(cards[:3]):
        t = re.search(r'<h3>(.*?)</h3>', ch)
        print(f'  [{i}] onclick={click[:40]} title={t.group(1) if t else "?"}')
else:
    print('services-grid NOT FOUND')
    # search more broadly
    m2 = re.search(r'services-grid', h)
    if m2:
        print('but "services-grid" exists at', m2.start())
        print('around:', h[m2.start():m2.start()+200])
    else:
        print('"services-grid" REFERENCE NOT FOUND')
