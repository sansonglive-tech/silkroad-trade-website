#!/usr/bin/env python3
"""修复 admin_server.py 的编码问题"""
import subprocess, os, ast

WORKSPACE = r'C:\Users\ASDCF\.qclaw\workspace'
git_exe = r'E:\腾讯龙虾\QClaw\v0.2.29.592\resources\git\cmd\git.exe'
target = os.path.join(WORKSPACE, 'admin_server.py')

# 获取初始提交的版本
result = subprocess.run([git_exe, 'show', 'eaa054d:admin_server.py'], capture_output=True, cwd=WORKSPACE)
data = result.stdout

# 检查初始版本里中文是否正常
needle = '丝路山海通'.encode('utf-8')
print(f'初始版本大小: {len(data)} 字节')
print(f'初始版本含丝路山海通: {needle in data}')

if needle not in data:
    print('初始版本也乱码了，尝试用 github 上最后一次提交')
    result = subprocess.run([git_exe, 'show', 'HEAD:admin_server.py'], capture_output=True, cwd=WORKSPACE)
    data = result.stdout
    print(f'HEAD版本大小: {len(data)} 字节')
    print(f'HEAD版本含丝路山海通: {needle in data}')

# 直接写入
with open(target, 'wb') as f:
    f.write(data)

# 检查语法
try:
    with open(target, 'r', encoding='utf-8') as f:
        content = f.read()
    ast.parse(content)
    print('语法检查通过')
    
    # 检查 LB 中的中文
    idx = content.find('var LB=')
    if idx >= 0:
        end = content.index(';', idx)
        section = content[idx:end+1]
        print(f'LB定义: {section}')
        has_chinese = any('\u4e00' <= c <= '\u9fff' for c in section)
        print(f'LB含中文: {has_chinese}')
    
except SyntaxError as e:
    print(f'语法错误: {e}')

print('完成')
