#!/usr/bin/env python3
import sys

with open('C:/Users/ASDCF/.qclaw/workspace/silkroad-trade_v7_silk_poster.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find script tag
script_idx = content.find('<script>')
print(f'script at index: {script_idx}')

if script_idx >= 0:
    after = content[script_idx:script_idx+100]
    print(repr(after))
    
    # Find where CONFIG is
    config_idx = content.find('const CONFIG = {')
    print(f'CONFIG at: {config_idx}')
    
    # Where is the // DETAIL CONTENT that was supposed to be replaced?
    dc_idx = content.find('// DETAIL CONTENT')
    print(f'DETAIL CONTENT marker at: {dc_idx}')
    
    # Count script tags
    print(f'<script> count: {content.count("<script>")}')
    print(f'</script> count: {content.count("</script>")}')
    
    # Is there a broken script tag like just `>\n`?
    print(f'Has <script>\\n: {content.find("<script>\\n")}')
    print(f'Has <script>\\\\n: {content.find("<script>\\\\n")}')
    
    # Let's see what a few chars around the DETAIL CONTENT marker look like
    if dc_idx > 0:
        print('\nAround DETAIL CONTENT:')
        print(repr(content[dc_idx-20:dc_idx+40]))
else:
    print('NO <script> TAG FOUND!')
    
    # Find where CONFIG was inserted
    config_idx = content.find('const CONFIG = {')
    print(f'CONFIG at: {config_idx}')
    if config_idx > 0:
        print('Before CONFIG:')
        print(repr(content[config_idx-100:config_idx]))

