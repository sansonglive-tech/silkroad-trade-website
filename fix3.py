# -*- coding: utf-8 -*-
import sys

with open('C:\\Users\\ASDCF\\.qclaw\\workspace\\silkroad-trade.html', 'rb') as f:
    raw = f.read()
print(f'Size: {len(raw)}')
text = raw.decode('utf-8', errors='replace')
print(f'U+FFFD count: {text.count(chr(0xFFFD))}')

# Fix literal '?' chars that GBK couldn't map
fixes = {
    # Title
    '丝路山海??一带一路': '丝路山海通 — 一带一路',
    # About section
    '关于丝路山海?': '关于丝路山海通',
    '丝路万里 · 山海相?': '丝路万里 · 山海相通',
    '让中国企?': '让中国企业',
    '落地海外?': '落地海外。',
    '互利共赢?': '互利共赢。',
    '商务合?': '商务合作',
    # Services section
    '全链路出海落?': '全链路出海落地',
    '覆盖出海全流程?': '覆盖出海全流程。',
    '注册与资?': '注册与资质',
    '最快个工作日': '最快7个工作日',
    '完成海外公司设立?': '完成海外公司设立。',
    '完成设立?': '完成设立。',
    '财税人事与法?': '财税人事与法务',
    '全方位保障?': '全方位保障。',
    '行程安排?': '行程安排。',
    '产品准入与认?': '产品准入与认证',
    '合规准入服务?': '合规准入服务。',
    '建厂与工程服?': '建厂与工程服务',
    '基建配套服务?': '基建配套服务。',
    '本地化运营支?': '本地化运营支持',
    '扎根海外市场?': '扎根海外市场。',
    # Policy section
    '一带一路政?': '一带一路政策',
    '政策研究与解?': '政策研究与解读',
    '精准政策导航?': '精准政策导航。',
    '政府与商会对?': '政府与商会对接',
    '政商关系网络?': '政商关系网络。',
    '政策红利?': '政策红利。',
    '投融资对?': '投融资对接',
    '项目资金支持?': '项目资金支持。',
    # Countries
    '服务所?': '服务所达',
    '印度尼西?': '印度尼西亚',
    '雅加?': '雅加达',
    '菲律?': '菲律宾',
    '马尼?': '马尼拉',
    '新加?': '新加坡',
    '哈萨克斯?': '哈萨克斯坦',
    '阿联?': '阿联酋',
    '肯尼?': '肯尼亚',
    '内罗?': '内罗毕',
    # Process
    '需求诊?': '需求诊断',
    '出海方案?': '出海方案。',
    '风险前置?': '风险前置。',
    '全程推进?': '全程推进。',
    '长期运营保障?': '长期运营保障。',
    # Stats
    '信赖之?': '信赖之选',
    '一带一路覆盖国?': '一带一路覆盖国家',
    # Testimonials
    '太多了?': '太多了。',
    '张宏?': '张宏伟',
    '新能源汽?': '新能源汽车',
    '工厂负责?': '工厂负责人',
    '强烈推荐?': '强烈推荐。',
    '李雪?': '李雪峰',
    '总经理?': '总经理',
    '效果超出预期?': '效果超出预期。',
    # CTA
    '让您的企?': '让您的企业',
    '新篇章?': '新篇章。',
    # Footer
    '有限公?': '有限公司',
    '丝路山海?': '丝路山海通',
    # Detail content
    '渲染?': '渲染',
    '动态渲?': '动态渲染',
    '???': '',
    '一张证书通市?': '一张证书通市场',
    '缩短60%?': '缩短60%/',
    '货运港口集装?': '货运港口集装箱',
    '更要扎?': '更要扎根',
    '出海问?': '出海问题',
    '规模与行?': '规模与行业',
    '出海痛?': '出海痛点',
    '出海需?': '出海需求',
    '行业准入限?': '行业准入限制',
    '规范申?': '规范申报',
    '合作伙?': '合作伙伴',
    '银行开?': '银行开户',
    '认证办?': '认证办理',
    '团队搭?': '团队搭建',
    '投资许可审?': '投资许可审批',
    '管理体?': '管理体系',
    '风险预警机?': '风险预警机制',
    '出海信赖之?': '出海信赖之选',
    '最大动力?': '最大动力。',
    '生产许?': '生产许可',
    '节省企?': '节省企业',
    '效率高太多了?': '效率高太多了。',
    '本地招?': '本地招聘',
    '试错成本?': '试错成本。',
    '全程代?': '全程代办',
    '周期缩?': '周期缩短',
    '个月完成所有认?': '个月完成所有认证',
    '包办，效果超出预期?': '包办，效果超出预期。',
    '华侨银?': '华侨银行',
    'IT通?': 'IT通讯',
    '政策风?': '政策风险',
    'list-style-type:"?"': 'list-style-type:"none"',
    'fill="#F0D68A">?': 'fill="#F0D68A">丝',
    'arrowPrev">?</': 'arrowPrev">←</',
    'arrowNext">?</': 'arrowNext">→</',
    '返回首页': '← 返回首页',
    '拓?': '拓展',
    '绩?': '绩效',
    '利?': '利？',
}

count = 0
for old, new in fixes.items():
    if old in text:
        text = text.replace(old, new)
        count += 1

print(f'Applied {count} fixes')

with open('C:\\Users\\ASDCF\\.qclaw\\workspace\\silkroad-trade.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)

print('File written')

# Verify
with open('C:\\Users\\ASDCF\\.qclaw\\workspace\\silkroad-trade.html', 'rb') as f:
    raw = f.read()
txt = raw.decode('utf-8', errors='replace')
print(f'Final size: {len(raw)}')
print(f'U+FFFD: {txt.count(chr(0xFFFD))}')
print(f'Title: {txt[txt.index("<title>")+7:txt.index("</title>")]}')
print(f'关于丝路山海通: {"FOUND" if "关于丝路山海通" in txt else "MISSING"}')

# Check for remaining '?' corruption in Chinese text
dubious = 0
for ch in txt:
    if ch == '?' and ord(ch) == 0x3F:
        dubious += 1
print(f'Total literal ? marks: {dubious}')
