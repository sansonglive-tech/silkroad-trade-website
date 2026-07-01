#!/usr/bin/env python3

with open('admin_server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到并修改第476行
for i, line in enumerate(lines):
    if 'policy-card' in line and 'p.detailId' in line:
        print(f'Found at line {i+1}: {line}')
        # 替换这一行
        old = "    return '<div class=\"policy-card\" onclick=\"openDetail(\\\\\'" + "' + (p.detailId || p.id) + '" + "'\\\\\')\">' +"
        new = "    var detailId = ['policy-research', 'policy-network', 'policy-park', 'policy-finance'][i] || ('policy-' + i);\n    return '<div class=\"policy-card\" onclick=\"openDetail(\\\\\'" + "' + detailId + '" + "'\\\\\')\">' +"
        
        lines[i] = line.replace(
            "return '<div class=\"policy-card\" onclick=\"openDetail(\\\\\'" + "' + (p.detailId || p.id) + '" + "'\\\\\')\">' +",
            "var detailId = ['policy-research', 'policy-network', 'policy-park', 'policy-finance'][i] || ('policy-' + i);\n    return '<div class=\"policy-card\" onclick=\"openDetail(\\\\\'" + "' + detailId + '" + "'\\\\\')\">' +"
        )
        print('Replaced!')
        break

with open('admin_server.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Done')
