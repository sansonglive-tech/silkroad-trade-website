#!/usr/bin/env python3
"""Fix embedded double quotes in JS file."""
import re

with open(r'C:\Users\ASDCF\.qclaw\workspace\create_profit_data_doc.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all lines with problematic embedded quotes
lines = content.split('\n')
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith('//'):
        continue
    # Count double quotes
    dq = stripped.count('"')
    if dq > 6:
        print(f"Line {i+1} ({dq} quotes): {stripped[:100]}")

print("---")

# Fix: replace Chinese content's internal " with \u201c and \u201d (smart quotes)
fixes = [
    ('课"带电脑现场干"的', '\u201c带电脑现场干\u201d的'),
    ('调"带电脑来现场干"', '\u201c带电脑来现场干\u201d'),
    ('需求不是"可能会买"，而是"必须要有"', '需求不是\u201c可能会买\u201d，而是\u201c必须要有\u201d'),
    ('"交付为王"差异化定位', '\u201c交付为王\u201d差异化定位'),
    ('属于"高信任度+高支付能力+高需求匹配"的三高用户', '属于\u201c高信任度+高支付能力+高需求匹配\u201d的三高用户'),
]

for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        print(f"Fixed: {old[:40]} -> {new[:40]}")
    else:
        print(f"Not found: {old[:40]}")

with open(r'C:\Users\ASDCF\.qclaw\workspace\create_profit_data_doc.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone. Saved.")
