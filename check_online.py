#!/usr/bin/env python3
import urllib.request
import json

r = urllib.request.urlopen('https://sansonglive-tech.github.io/silkroad-trade-website/', timeout=10)
html = r.read().decode('utf-8')

print("邮箱look@silkroad-trade.com:", 'yes' if 'look@silkroad-trade.com' in html else 'no')
print("粤ICP备:", 'yes' if '粤ICP备' in html else 'no')
print("HTML大小:", len(html))
print()

# CONFIG块
config_idx = html.find('const CONFIG =')
if config_idx > 0:
    brace = html.find('{', config_idx)
    depth = 0
    end = brace
    for i in range(brace, len(html)):
        if html[i] == '{': depth += 1
        elif html[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    config_str = html[brace:end]
    try:
        cfg = json.loads(config_str)
        print("CONFIG ICP:", cfg['company']['icp'])
        print("CONFIG 邮箱:", cfg['company']['email'])
    except:
        print("CONFIG解析失败")
else:
    print("没有CONFIG块")

print()
print("页面最后200字符:")
print(html[-200:])
