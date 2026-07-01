#!/usr/bin/env python3
# 测试发布流程（不实际 push，只测试生成和 git 命令）
import json, os, subprocess, sys

git_exe = r"E:\腾讯龙虾\QClaw\v0.2.29.592\resources\git\cmd\git.exe"
work = r"C:\Users\ASDCF\.qclaw\workspace"

print("=== 1. 读取配置 ===")
with open(os.path.join(work, 'site_config.json'), 'r', encoding='utf-8') as f:
    cfg = json.load(f)
print(f"公司: {cfg['company']['name']}")
print(f"邮箱: {cfg['company']['email']}")

print("\n=== 2. 读取 v7 HTML ===")
with open(os.path.join(work, 'silkroad-trade_v7_silk_poster.html'), 'r', encoding='utf-8') as f:
    html = f.read()
print(f"大小: {len(html):,} 字符")

print("\n=== 3. 生成 index.html ===")
js_config = json.dumps(cfg, ensure_ascii=False, indent=2)

marker = "const CONFIG = "
idx = html.find(marker)
if idx == -1:
    print("FAIL: 未找到 CONFIG 标记")
    sys.exit(1)

brace_idx = html.find("{", idx)
depth = 0
end = brace_idx
for i in range(brace_idx, len(html)):
    if html[i] == "{":
        depth += 1
    elif html[i] == "}":
        depth -= 1
        if depth == 0:
            end = i + 1
            while end < len(html) and html[end] in " \t\n\r":
                end += 1
            if end < len(html) and html[end] == ";":
                end += 1
            break

publish_html = html[:idx] + f"const CONFIG = {js_config};" + html[end:]
print(f"生成成功: {len(publish_html):,} 字符")

print("\n=== 4. 检查弹框功能 ===")
# 检查政策卡片
if "onclick=\"openDetail('policy-research')\"" in publish_html or "openDetail" in publish_html:
    print("OK: 包含 openDetail 调用")
else:
    print("WARN: 无 openDetail")

# 检查 preloader
if "pointer-events:none" in publish_html:
    print("OK: preloader 已修复")
else:
    print("WARN: preloader 可能有问题")

print("\n=== 5. 测试 git 命令 ===")
# 测试 git status
result = subprocess.run(
    [git_exe, "status", "--short", "index.html", "site_config.json"],
    cwd=work, capture_output=True, text=True, timeout=10
)
print(f"git status: rc={result.returncode}")
print(result.stdout[:200] if result.stdout else "(no output)")

print("\n=== 测试完成 ===")
