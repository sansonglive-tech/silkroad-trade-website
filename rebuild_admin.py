#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""读取当前混乱的 admin_server.py，修复中文编码问题"""
import ast, os

WORKSPACE = r'C:\Users\ASDCF\.qclaw\workspace'
path = os.path.join(WORKSPACE, 'admin_server.py')

# 以二进制方式读取
with open(path, 'rb') as f:
    raw = f.read()

# 尝试用 UTF-8 解码，用替换模式处理乱码
content = raw.decode('utf-8', errors='replace')

# 现在 content 里的中文可能是乱码字符，也可能是正确的
# 从 git 初始版本提取正确的 DEFAULT 和 LB 等

import subprocess
git_exe = r'E:\腾讯龙虾\QClaw\v0.2.29.592\resources\git\cmd\git.exe'
result = subprocess.run([git_exe, 'show', 'eaa054d:admin_server.py'], capture_output=True, cwd=WORKSPACE)
clean_raw = result.stdout
clean_content = clean_raw.decode('utf-8')

# 从干净版本提取部分内容
# 提取 DEFAULT 部分
def extract_between(text, start_marker, end_marker):
    s = text.find(start_marker)
    if s < 0: return None
    e = text.find(end_marker, s + len(start_marker))
    if e < 0: return None
    return text[s:e+len(end_marker)]

# 替换损坏的部分
fixes = {}

# DEFAULT 部分 - 从干净版本取
default_clean = extract_between(clean_content, 'DEFAULT = {', "def load_cfg")
if default_clean:
    default_bad = extract_between(content, 'DEFAULT = {', "def load_cfg")
    if default_bad:
        fixes[default_bad] = default_clean

# LB 定义
lb_clean = extract_between(clean_content, "var LB={", "};")
if lb_clean:
    lb_clean = "var LB=" + lb_clean + "};"
    # 在当前内容里找 LB
    lb_bad_idx = content.find("var LB={")
    if lb_bad_idx >= 0:
        lb_bad_end = content.find(";", lb_bad_idx)
        if lb_bad_end >= 0:
            lb_bad = content[lb_bad_idx:lb_bad_end+1]
            fixes[lb_bad] = lb_clean

# 应用替换
for old, new in fixes.items():
    if old in content:
        content = content.replace(old, new)
        print(f'替换成功: {old[:30]}... -> {new[:30]}...')
    else:
        print(f'没找到: {old[:40]}...')

# 检查 LAN 和公司名称等中文在 Python 字符串中的情况
# 替换 remaining garbled Chinese in comments and strings
# 在默认 DEFAULT 之后的键名中文应该是好的了（因为替换了 DEFAULT 块）
# 但注释里的中文可能还是坏的
# 替换注释中的乱码
garbled_fixes = {
    '丝路山海通?': '丝路山海通 ',
    '?路 鍚庡彴绠＄悊': ' · 后台管理',
    '?鍚庡彴': ' · 后台',
    '?鍚庡彴绠＄悊鍣?': '后台管理器',
    '?路 鍚庡彴绠＄悊': ' · 后台管理',
    '?鍙鍖栧悗鍙?': ' 可视化后台',
    '?鍚庡彴': ' 后台',
}

# 更通用的方法：把 content 中所有被 replacement char 污染的地方修掉
# 用 ast 检查语法
try:
    ast.parse(content)
    print('✅ 语法通过')
except SyntaxError as e:
    print(f'❌ 语法错误: {e}')
    # 打印错误行
    lines = content.split('\n')
    err_line = e.lineno
    if err_line:
        for i in range(max(0,err_line-3), min(len(lines),err_line+2)):
            marker = '>>>' if i+1 == err_line else '   '
            print(f'{marker} {i+1}: {lines[i]}')

# 写入
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\n写入完成: {len(content)} 字符')
