#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描 v7 的板块结构"""
import re

with open("C:/Users/ASDCF/.qclaw/workspace/silkroad-trade_v7_silk_poster.html", "r", encoding="utf-8") as f:
    h = f.read()

# 1. 公司信息
for k in ["name", "slogan", "email", "icp", "wechatId", "wechatQR"]:
    m = re.search(r"wechatId:\s*'([^']*)'", h)
    if k == "wechatId":
        m = re.search(r"wechatId:\s*'([^']*)'", h)
    elif k == "wechatQR":
        m = re.search(r"wechatQR:\s*'([^']*)'", h)
    elif k == "name":
        m = re.search(r"name:\s*'([^']*)'", h)
    elif k == "slogan":
        m = re.search(r"slogan:\s*'([^']*)'", h)
    elif k == "email":
        m = re.search(r"email:\s*'([^']*)'", h)
    elif k == "icp":
        m = re.search(r"icp:\s*'([^']*)'", h)
print(f"公司: {m.group(1) if m else '?'}" if "name" in dir() else "?")

# 2. 服务卡片
m = re.search(r'<div class="services-grid">(.*?)</div>\s*</section>', h, re.DOTALL)
if m:
    cards = re.findall(r'<div class="service-card"[^>]*>(.*?)</div>\s*</div>', m.group(1), re.DOTALL)
    print(f"\n=== 服务卡片 ({len(cards)}) ===")
    for i, c in enumerate(cards):
        t = re.search(r'<h3>(.*?)</h3>', c)
        s = re.search(r'<div class=\"sc-sub\">(.*?)<', c)
        p = re.search(r'<p>(.*?)</p>', c)
        sp = re.search(r'<span[^>]*>(.*?)<', c)
        print(f"  [{i}] {t.group(1) if t else '?'} | {s.group(1) if s else '?'}")

# 3. 统计数字
m = re.search(r'class="stats-inner">(.*?)</div>', h, re.DOTALL)
if m:
    nums = re.findall(r'num">([^<]+)<', m.group(1))
    labels = re.findall(r'label">([^<]+)<', m.group(1))
    print(f"\n=== 统计数字 ({len(nums)}) ===")
    for n, l in zip(nums, labels):
        print(f"  {n} → {l}")

# 4. 轮播图
m = re.search(r'const SLIDE_CONFIG\s*=\s*\[(.*?)\];', h, re.DOTALL)
if m:
    slides = re.findall(r"title:'([^']*)'", m.group(1))
    print(f"\n=== 轮播图 ({len(slides)}) ===")
    for i, t in enumerate(slides):
        clean = re.sub(r'<[^>]+>', '', t)
        print(f"  [{i}] {clean[:30]}")

# 5. 政策卡片
m = re.search(r'<div class="policy-grid">(.*?)</div>\s*</div>\s*</section>', h, re.DOTALL)
if m:
    items = re.findall(r'<div class="policy-card"[^>]*>(.*?)</div>', m.group(1), re.DOTALL)
    print(f"\n=== 政策卡片 ({len(items)}) ===")
    for i, c in enumerate(items):
        pn = re.search(r'pn">([^<]+)', c)
        t = re.search(r'<h3>(.*?)</h3>', c)
        p = re.search(r'<p>(.*?)</p>', c)
        print(f"  [{i}] {pn.group(1) if pn else '?'} {t.group(1) if t else '?'}")

# 6. 客户案例
m = re.search(r'class="testimonials-grid">(.*?)</div>\s*</section>', h, re.DOTALL)
if m:
    cards = re.findall(r'<div class="t-card"[^>]*>(.*?)</div>\s*</div>', m.group(1), re.DOTALL)
    print(f"\n=== 客户案例 ({len(cards)}) ===")
    for i, c in enumerate(cards):
        n = re.search(r't-name">([^<]+)', c)
        r = re.search(r't-role">([^<]+)', c)
        t = re.search(r't-text">([^<]+)', c)
        print(f"  [{i}] {n.group(1) if n else '?'}: {r.group(1) if r else '?'}")

# 7. 流程
m = re.search(r'class="process-grid">(.*?)</div>\s*</section>', h, re.DOTALL)
if m:
    steps = re.findall(r'<div class="pstep"[^>]*>(.*?)</div>', m.group(1), re.DOTALL)
    print(f"\n=== 服务流程 ({len(steps)}) ===")
    for i, s in enumerate(steps):
        n = re.search(r'n">([^<]+)', s)
        t = re.search(r'<h3>(.*?)</h3>', s)
        p = re.search(r'<p>(.*?)</p>', s)
        print(f"  [{i}] {n.group(1) if n else '?'} {t.group(1) if t else '?'}")

# 8. 区域/国家
m = re.search(r'class="countries-grid">(.*?)</section>', h, re.DOTALL)
if m:
    regions = re.findall(r'<div class="region-card"[^>]*>', m.group(1))
    print(f"\n=== 区域 ({len(regions)}) ===")
    for i in range(len(regions)):
        titles = re.findall(r'<h3>(.*?)</h3>', m.group(1))
        subs = re.findall(r'rsub">(.*?)<', m.group(1))
        if i < len(titles):
            sub = subs[i] if i < len(subs) else ''
            print(f"  [{i}] {titles[i]} ({sub})")

# 9. 关于
m = re.search(r'about-text\s+(.*?)(?:</div>\s*){2}', h, re.DOTALL)
if m:
    t = re.search(r'<h2>(.*?)</h2>', m.group(1))
    p = re.search(r'<p>(.*?)</p>', m.group(1))
    print(f"\n=== 关于我们 ===")
    if t: print(f"  标题: {t.group(1)}")
    if p: print(f"  描述: {p.group(1)[:50]}...")

# 10. hero 轮播底部 CTA
m = re.search(r'<section id="contact"[^>]*>(.*?)</section>', h, re.DOTALL)
if m:
    t = re.findall(r'<h2>(.*?)</h2>', m.group(1))
    p = re.search(r'<p>(.*?)</p>', m.group(1))
    print(f"\n=== CTA ===") 
    for ti in t:
        clean = re.sub(r'<[^>]+>', '', ti)
        print(f"  标题: {clean}")

print("\n✅ 扫描完成")
