#!/usr/bin/env python3
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/ASDCF/.qclaw/workspace/silkroad-trade_v7_silk_poster.html','r',encoding='utf-8') as f:
    h = f.read()

# HTML sections are: id="services", id="policies", id="testimonials", id="stats", id="process"
html_sections = ['services', 'policies', 'testimonials', 'stats', 'process']

for sid in html_sections:
    idx = h.find(f'id="{sid}"')
    if idx >= 0:
        section_end = h.find('</section>', idx)
        print(f'\n=== {sid} (section: {idx}..{section_end}) ===')
        section_html = h[idx:section_end]
        # Find grid div
        if sid == 'services':
            grid_class = 'services-grid'
        elif sid == 'policies':
            grid_class = 'policy-grid'
        elif sid == 'testimonials':
            grid_class = 'testimonials-grid'
        elif sid == 'stats':
            grid_class = 'stats-inner'
        elif sid == 'process':
            grid_class = 'process-grid'
        
        grid_m = re.search(rf'<div\s+class="{grid_class}">', section_html)
        if grid_m:
            grid_start = grid_m.end()
            # find the correct closing </div> - count open/close
            depth = 1
            i = grid_start
            while i < len(section_html) and depth > 0:
                o = section_html.find('<', i)
                if o < 0: break
                if section_html[o:o+2] == '</':
                    depth -= 1
                    i = section_html.index('>', o) + 1
                elif section_html[o:o+3] == '<!--':
                    ce = section_html.find('-->', o)
                    i = ce + 3 if ce >= 0 else o + 3
                elif section_html[o] == '<' and section_html[o+1] != '/' and section_html[o+1] != '!' and not section_html[o+1].isspace():
                    # check if self-closing
                    tag_end = section_html.index('>', o)
                    if section_html[tag_end-1] == '/':
                        i = tag_end + 1  # self-closing
                    else:
                        depth += 1
                        i = tag_end + 1
                else:
                    i = section_html.index('>', o) + 1
            inner = section_html[grid_start:i-1]
            print(f'  Grid inner: {len(inner)} chars')
            print(f'  First 200: {inner[:200]}')
        else:
            print(f'  Grid class "{grid_class}" NOT FOUND in section')
            # debug: find in whole html
            wh = h.find(grid_class)
            print(f'  But found in HTML at pos {wh}')
            if wh >= 0:
                print(f'  Context: {h[wh-40:wh+100]}')
    else:
        print(f'\n=== {sid}: NOT FOUND ===')

# Also check SLIDE_CONFIG
sc = re.search(r'const\s+SLIDE_CONFIG\s*=\s*\[(.*?)\];', h, re.DOTALL)
print(f'\n=== SLIDE_CONFIG ===')
if sc:
    objs = re.findall(r"\{([^}]+)\}", sc.group(1), re.DOTALL)
    print(f'Found {len(objs)} objects')
    for i, o in enumerate(objs[:2]):
        t = re.search(r"title:\s*'([^']*)'", o)
        print(f'  [{i}] title: {t.group(1) if t else "?"}')
else:
    print('NOT FOUND')

print('\nDONE')
