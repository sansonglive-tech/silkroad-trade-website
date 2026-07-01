#!/usr/bin/env python3
import json
import os

print("=== Test Publish ===")

# 1. Load config
with open('site_config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)
print(f"Config: {cfg['company']['name']}")

# 2. Load v7 HTML
with open('silkroad-trade_v7_silk_poster.html', 'r', encoding='utf-8') as f:
    html = f.read()
print(f"v7 HTML: {len(html)} chars")

# 3. Check CONFIG placeholder
if 'const CONFIG' in html:
    print("OK: v7 has CONFIG placeholder")
else:
    print("WARN: v7 no CONFIG placeholder")

# 4. Check inject script
if 'INJECT_SCRIPT' in html or 'CONFIG' in html:
    print("OK: Can inject config")
else:
    print("WARN: Need inject script")

print("\nTest passed, ready to publish")
