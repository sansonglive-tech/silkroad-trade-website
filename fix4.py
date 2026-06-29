# -*- coding: utf-8 -*-
with open('C:\\Users\\ASDCF\\.qclaw\\workspace\\silkroad-trade.html', 'rb') as f:
    raw = f.read()
text = raw.decode('utf-8', errors='replace')

fixes = {
    '?/div>': '</div>',
    '?/span>': '</span>',
    '?/p>': '</p>',
    '?/h3>': '</h3>',
    '?/h4>': '</h4>',
    '?/a>': '</a>',
    '?/button>': '</button>',
    '?/strong>': '</strong>',
    '?/small>': '</small>',
    'arrowPrev">' + chr(0xFFFD): 'arrowPrev">←',
    'arrowNext">' + chr(0xFFFD): 'arrowNext">→',
}

count = 0
for old, new in fixes.items():
    if old in text:
        text = text.replace(old, new)
        count += 1
print(f'Applied {count} fixes')

# Handle specific remaining issues
# Find lines with problematic patterns
issues = 0
for line in text.split('\n'):
    if 'arrowPrev' in line or 'arrowNext' in line:
        if '←' not in line and '→' not in line:
            print(f'Arrow issue: {line.strip()}')
            issues += 1
    if '关于丝路山海通/' in line:
        print(f'Split tag issue: {line.strip()}')
        issues += 1

print(f'Remaining issues: {issues}')

# Direct fixes for the arrow buttons
text = text.replace('arrowPrev">←/button>', 'arrowPrev">←</button>')
text = text.replace('arrowNext">→/button>', 'arrowNext">→</button>')

# Fix the "合作>" to "合作">"
text = text.replace('国际化商务合作>', '国际化商务合作">')

# Fix remaining stray issues
text = text.replace('?-->', '-->')
text = text.replace('??', '')

with open('C:\\Users\\ASDCF\\.qclaw\\workspace\\silkroad-trade.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)
print('Written')

# Final verification
with open('C:\\Users\\ASDCF\\.qclaw\\workspace\\silkroad-trade.html', 'rb') as f:
    raw = f.read()
txt = raw.decode('utf-8', errors='replace')
print(f'Title: {txt[txt.index("<title>")+7:txt.index("</title>")]}')
print(f'U+FFFD: {txt.count(chr(0xFFFD))}')
