#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
"""修复 admin_server.py 编码并保留所有功能"""
import os, subprocess, ast

WORKSPACE = r'C:\Users\ASDCF\.qclaw\workspace'
git_exe = r'E:\腾讯龙虾\QClaw\v0.2.29.592\resources\git\cmd\git.exe'
path = os.path.join(WORKSPACE, 'admin_server.py')

# 1. 获取初始版本（编码正确）
result = subprocess.run([git_exe, 'show', 'eaa054d:admin_server.py'], capture_output=True, cwd=WORKSPACE)
base = result.stdout.decode('utf-8')

# 2. 获取当前混乱版本中的新功能代码（从 HEAD 取，因为 HEAD 有所有功能但编码坏了）
result = subprocess.run([git_exe, 'show', 'HEAD:admin_server.py'], capture_output=True, cwd=WORKSPACE)
head = result.stdout.decode('utf-8', errors='replace')

# 3. 从 HEAD 提取增量功能
# 找出初始版本和 HEAD 之间的差异行
base_lines = set(base.split('\n'))

# 从 HEAD 提取新增的内容
# 初始版本在 "def trace(*" 之前就结束了（没有登录/诊断功能）
# 所以直接取 HEAD 版本，然后修复编码就行

# 现在用原头版本（有所有功能），但修复编码
# 从原始 git 对象获取
result = subprocess.run([git_exe, 'cat-file', '-p', 'HEAD:admin_server.py'], capture_output=True, cwd=WORKSPACE)
raw_bytes = result.stdout

# 检查原始字节。如果是 UTF-8 但有 BOM，去掉
if raw_bytes[:3] == b'\xef\xbb\xbf':
    raw_bytes = raw_bytes[3:]

# 尝试 UTF-8 解码
content = raw_bytes.decode('utf-8', errors='replace')

# 检查"丝路山海通"是否正常
if '丝路山海通' in content:
    print('✅ HEAD 版本中文正常（UTF-8）')
else:
    # 可能是 GBK 编码被错误存储了，尝试逐个替换已知乱码
    print('⚠️  HEAD 版本中文乱码，需要修复')

    # 用替换表修复
    garbled_to_correct = {
        '涓濊矾灞辨捣閫?': '丝路山海通',
        '涓€甯︿竴璺紒涓氬嚭娴蜂竴绔欏紡鏈嶅姟': '一带一路企业出海一站式服务',
        '绮CP澶噚xxxxx鍙?': '粤ICP备XXXXXXXX号',
        '鍏徃鍚嶇О': '公司名称',
        '鍓爣棰?鏍囪': '副标题/标语',
        '鍓爣棰\xbf鏍囪': '副标题/标语',
        '鑱旂郴閭': '联系邮箱',
        '鑱旂郴閭\xae\xc7\xc6': '联系邮箱',
        '鑱旂郴鐢佃瘽': '联系电话',
        '澶囨鍙?': '备案号',
        '寰俊鍙?': '微信号',
        '澶嘪': '备',
        '鍚嶇О': '名称',
        '鏍囪': '标语',
        '鐢佃瘽': '电话',
        '浠ｇ爜': '代码',
        '鐧诲綍': '登录',
        '鐢ㄦ埛': '用户',
        '瀵嗙爜': '密码',
        '鏃ュ織': '日志',
        '杩借釜': '追踪',
        '璇婃柇': '诊断',
        '淇濆瓨': '保存',
        '鍙戝竷': '发布',
        '鏂囦欢': '文件',
        '缃戠粶': '网络',
        '閰嶇疆': '配置',
        '鏈嶅姟': '服务',
        '鍥剧墖': '图片',
        '鏍囬': '标题',
        '鎻忚堪': '描述',
        '缂栧彿': '编号',
        '鍔犺浇': '加载',
        '鎴愬姛': '成功',
        '澶辫触': '失败',
        '鍚庡彴': '后台',
        '璁剧疆': '设置',
        '鏁版嵁': '数据',
        '鍒犻櫎': '删除',
        '娣诲姞': '添加',
        '鏆傛棤': '暂无',
        '鍥炬爣': '图标',
        '鏁板瓧': '数字',
        '鏍囩': '标签',
        '濮撳悕': '姓名',
        '鑱屼綅': '职位',
        '鍘熻瘽': '原话',
        '宸ュ叿': '工具',
        '缁撴灉': '结果',
        '鎺ㄩ€?': '推送',
        '鍖洪棿': '区间',
        '绯荤粺': '系统',
        '澶囨': '备',
    }

    for garbled, correct in garbled_to_correct.items():
        content = content.replace(garbled, correct)

# 验证
print(f'包含丝路山海通: {"丝路山海通" in content}')
print(f'LB公司名称: {"公司名称" in content}')

# 检查语法
try:
    tree = ast.parse(content)
    print('✅ 语法检查通过')
    print(f'文件大小: {len(content)} 字符')
except SyntaxError as e:
    print(f'❌ 语法错误: {e}')
    lines = content.split('\n')
    el = e.lineno
    if el:
        for i in range(max(0,el-2), min(len(lines),el+2)):
            m = '>>>' if i+1 == el else '   '
            print(f'{m} {i+1}: {lines[i][:120]}')

# 写入
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# 再次验证
import ast
with open(path, 'r', encoding='utf-8') as f:
    verify = f.read()
try:
    ast.parse(verify)
    print('\n✅ 最终语法检查通过')
    print(f'包含登录: {"ADMIN_USER" in verify}')
    print(f'包含诊断: {"def diagnose" in verify}')
    print(f'包含发布: {"publish_to_github" in verify}')
except SyntaxError as e:
    print(f'\n❌ 最终语法错误: {e}')

print('\n完成!')
