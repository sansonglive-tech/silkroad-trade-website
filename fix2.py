# -*- coding: utf-8 -*-
import sys

REPL = '\ufffd'  # U+FFFD replacement character

with open('C:\\Users\\ASDCF\\.qclaw\\workspace\\silkroad-trade.html', 'rb') as f:
    raw = f.read()
print(f'Size: {len(raw)}')
text = raw.decode('utf-8', errors='replace')
print(f'U+FFFD count: {text.count(REPL)}')

# The file previously had GBK mojibake (UTF-8 decoded as GBK, then re-encoded as UTF-8)
# The GBK reversion couldn't map some characters -> U+FFFD
# These characters should have been single Chinese chars. Let me see what's still U+FFFD
# and figure out the correct replacements

# Find all unique contexts of U+FFFD to build the replacement map
import re
contexts = set()
for m in re.finditer(REPL, text):
    start = max(0, m.start() - 5)
    end = min(len(text), m.end() + 10)
    ctx = text[start:end].replace('\n', '\\n').replace('\r', '')
    contexts.add(ctx)

for ctx in sorted(contexts):
    print(f'  {ctx}')

print(f'\nTotal unique U+FFFD contexts: {len(contexts)}')
