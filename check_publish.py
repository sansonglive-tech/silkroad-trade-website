#!/usr/bin/env python3
# 检查发布流程的问题
import json
import os

WORKSPACE = r"C:\Users\ASDCF\.qclaw\workspace"

# 1. 读取 site_config.json（发布时用的是这个）
with open(os.path.join(WORKSPACE, 'site_config.json'), 'r', encoding='utf-8') as f:
    cfg = json.load(f)
print("=== site_config.json（发布时读的数据）===")
print(f"邮箱: {cfg['company']['email']}")
print(f"ICP: {cfg['company']['icp']}")
print(f"政策数: {len(cfg['policies'])}")

# 2. 检查生成的 index.html 内容
with open(os.path.join(WORKSPACE, 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

print("\n=== index.html（发布到 GitHub 的文件）===")
if 'look@silkroad-trade.com' in html:
    print("邮箱: look@silkroad-trade.com OK")
if '粤ICP备010101010号' in html:
    print("ICP: 粤ICP备010101010号 OK")

# 3. 检查 CONFIG 块是否完整
marker = 'const CONFIG = '
idx = html.find(marker)
if idx > 0:
    # 提取 CONFIG 并解析
    brace = html.find('{', idx)
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
        cfg_in_html = json.loads(config_str)
        print(f"\nindex.html 中 CONFIG 的 ICP: {cfg_in_html['company']['icp']}")
        print(f"index.html 中 CONFIG 的 邮箱: {cfg_in_html['company']['email']}")
    except:
        print("无法解析 index.html 中的 CONFIG")
