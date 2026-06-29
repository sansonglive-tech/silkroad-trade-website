#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查 v7 文件的问题"""
import re

with open('C:/Users/ASDCF/.qclaw/workspace/silkroad-trade_v7_silk_poster.html', 'r', encoding='utf-8') as f:
    h = f.read()

print(f"文件大小: {len(h)} 字节")

# 1. scroll-bg 区域
idx = h.find('scroll-bg')
if idx >= 0:
    print('\n=== scroll-bg 区域 ===')
    print(h[idx:idx+500])

# 2. 找到 scroll-bg 里引用的图片
bg_start = h.find('<div class="scroll-bg">')
bg_end = h.find('</div>', bg_start) + 6
print('\n=== 完整 scroll-bg 块 ===')
print(h[bg_start:bg_end])

# 3. 找所有非 http 的相对图片引用
for m in re.finditer(r'(?:src|href)\s*=\s*"([^"]+)"', h):
    url = m.group(1)
    if url.startswith('data:') or url.startswith('#') or url.startswith('http'):
        continue
    if any(url.endswith(ext) for ext in ['.jpg','.jpeg','.png','.gif','.webp','.svg','.ico']):
        print(f'相对引用: {url}')
    elif 'wechat' in url.lower():
        print(f'微信图片: {url}')
