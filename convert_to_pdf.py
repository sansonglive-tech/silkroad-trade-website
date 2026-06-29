# -*- coding: utf-8 -*-
"""Convert the 新丝路·供应链矩阵计划 document to PDF without changing content."""

import os, sys, platform
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    KeepTogether, HRFlowable, Table, TableStyle
)
from reportlab.lib import colors

# ── 1. Register CJK font ──
system = platform.system()
cn_font = None
if system == 'Windows':
    windir = os.environ.get('WINDIR', 'C:\\Windows')
    font_dirs = [os.path.join(windir, 'Fonts')]
    local = os.environ.get('LOCALAPPDATA', '')
    if local:
        font_dirs.append(os.path.join(local, 'Microsoft', 'Windows', 'Fonts'))
    for d in font_dirs:
        for fname, name, idx in [
            ('msyh.ttc', 'MicrosoftYaHei', 0),
            ('msyhbd.ttc', 'MicrosoftYaHeiBold', 0),
            ('simhei.ttf', 'SimHei', 0),
            ('simsun.ttc', 'SimSun', 0),
        ]:
            fp = os.path.join(d, fname)
            if os.path.exists(fp):
                try:
                    pdfmetrics.registerFont(TTFont(name, fp, subfontIndex=idx))
                    cn_font = name
                    break
                except Exception:
                    continue
        if cn_font:
            break
elif system == 'Darwin':
    for fp, name, idx in [
        ('/System/Library/Fonts/STHeiti Light.ttc', 'STHeiti', 0),
        ('/System/Library/Fonts/STHeiti Medium.ttc', 'STHeitiMedium', 0),
    ]:
        if os.path.exists(fp):
            pdfmetrics.registerFont(TTFont(name, fp, subfontIndex=idx))
            cn_font = name
            break
else:
    for fp, name, idx in [
        ('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 'NotoSansCJK', 0),
        ('/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc', 'NotoSansCJK', 0),
    ]:
        if os.path.exists(fp):
            pdfmetrics.registerFont(TTFont(name, fp, subfontIndex=idx))
            cn_font = name
            break

if cn_font is None:
    raise RuntimeError(f"No CJK font found on {system}")

# Also try to register bold variant
cn_font_bold = cn_font
if system == 'Windows':
    windir = os.environ.get('WINDIR', 'C:\\Windows')
    bold_path = os.path.join(windir, 'Fonts', 'msyhbd.ttc')
    if os.path.exists(bold_path):
        try:
            pdfmetrics.registerFont(TTFont('MicrosoftYaHeiBold', bold_path, subfontIndex=0))
            cn_font_bold = 'MicrosoftYaHeiBold'
        except:
            pass

# ── 2. Build styles ──
s_body = ParagraphStyle('Body', fontName=cn_font, fontSize=10, leading=16,
                         spaceAfter=4, alignment=TA_JUSTIFY)
s_h1 = ParagraphStyle('H1', fontName=cn_font_bold, fontSize=16, leading=22,
                        spaceBefore=14, spaceAfter=6,
                        textColor=colors.HexColor('#1a1a2e'))
s_h2 = ParagraphStyle('H2', fontName=cn_font_bold, fontSize=13, leading=18,
                        spaceBefore=10, spaceAfter=4,
                        textColor=colors.HexColor('#16213e'))
s_h3 = ParagraphStyle('H3', fontName=cn_font_bold, fontSize=11, leading=16,
                        spaceBefore=8, spaceAfter=3,
                        textColor=colors.HexColor('#0f3460'))
s_title = ParagraphStyle('Title', fontName=cn_font_bold, fontSize=22, leading=30,
                          alignment=TA_CENTER, spaceAfter=4)
s_subtitle = ParagraphStyle('Subtitle', fontName=cn_font, fontSize=12, leading=16,
                             alignment=TA_CENTER, spaceAfter=18,
                             textColor=colors.HexColor('#666666'))
s_bullet = ParagraphStyle('Bullet', parent=s_body, leftIndent=16,
                           firstLineIndent=0, spaceAfter=2)
s_code = ParagraphStyle('Code', fontName=cn_font, fontSize=7.5, leading=10,
                         leftIndent=6, spaceAfter=2, spaceBefore=2)
s_small = ParagraphStyle('Small', fontName=cn_font, fontSize=8, leading=11,
                          spaceAfter=2)
s_table_header = ParagraphStyle('TH', fontName=cn_font_bold, fontSize=8.5, leading=13,
                                 alignment=TA_CENTER, textColor=colors.white)
s_table_cell = ParagraphStyle('TC', fontName=cn_font, fontSize=8.5, leading=13,
                               alignment=TA_CENTER)
s_table_body = ParagraphStyle('TBody', fontName=cn_font, fontSize=8.5, leading=13)

def P(text, style=s_body):
    """Helper to create a Paragraph."""
    return Paragraph(text, style)

def escape(text):
    """Escape XML special chars for reportlab Paragraph."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

def bullet(text):
    return P(f'&bull; {escape(text)}', s_bullet)

def code(text):
    return P(escape(text), s_code)

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cccccc'),
                       spaceBefore=6, spaceAfter=6)

# ── 3. Document content ──
# The full document text, parsed into sections

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           '新丝路·供应链矩阵计划.pdf')

doc = SimpleDocTemplate(
    output_path, pagesize=A4,
    topMargin=20*mm, bottomMargin=20*mm,
    leftMargin=22*mm, rightMargin=22*mm,
    title='新丝路·供应链矩阵计划',
    author='新丝路'
)

story = []

# ===== TITLE PAGE =====
story.append(Spacer(1, 40*mm))
story.append(P('新丝路·供应链矩阵计划', s_title))
story.append(P('以供应链为根基、以个体为触角、以陪跑为纽带的出海新生态', s_subtitle))
story.append(Spacer(1, 15*mm))

# ===== 一、核心定位与时代背景 =====
story.append(P('一、核心定位与时代背景', s_h1))

story.append(P('1.1 计划定位', s_h2))
story.append(P(escape('计划名称：新丝路·供应链矩阵计划（以下简称"矩阵计划"）'), s_body))
story.append(P(escape('核心逻辑：供应链是出海的"炮弹"，个体是出海的"炮兵"。传统的出海模式是"工厂自己当炮兵"——既要做产品，又要跑运营，两头不靠岸。矩阵计划颠覆这一逻辑：供应链做深度，个体做广度。'), s_body))
story.append(P(escape('供应端（深度）：新丝路整合国内优质制造企业，形成"出海供应链联盟"，提供产品库、代发履约、合规认证、海外仓储等基础设施'), s_bullet))
story.append(P(escape('个体端（广度）：赋能中国3.2亿灵活就业人群中的一部分，让他们以"一件代发""短视频带货""TikTok直播"等形式成为供应链的触角，实现"人人出海、万品出海"'), s_bullet))
story.append(P(escape('新丝路平台（枢纽）：作为中间的"连接器+赋能器"，提供培训赋能、选品中心、代发系统、合规保障、收益分账等全链路服务'), s_bullet))

story.append(P('1.2 时代背景：三大结构性红利', s_h2))

story.append(P('红利一：灵活就业已成为中国劳动力市场的"新常态"', s_h3))

# Table for 灵活就业 data
t1_data = [
    [P('时间节点', s_table_header), P('灵活就业人数', s_table_header),
     P('占就业人口比例', s_table_header), P('年均增长', s_table_header)],
    [P('2021年', s_table_cell), P('约2.0亿', s_table_cell),
     P('约28%', s_table_cell), P('—', s_table_cell)],
    [P('2024年底', s_table_cell), P('2.4亿', s_table_cell),
     P('超33%', s_table_cell), P('约1,300万/年', s_table_cell)],
    [P('2025年', s_table_cell), P('2.8亿', s_table_cell),
     P('约39%', s_table_cell), P('约4,000万/年', s_table_cell)],
    [P('2026年（预计）', s_table_cell), P('3.2亿', s_table_cell),
     P('约44%', s_table_cell), P('约4,000万/年', s_table_cell)],
]
t1 = Table(t1_data, colWidths=[80, 80, 90, 90])
t1.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E4057')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t1)
story.append(Spacer(1, 4))

story.append(P(escape('数据来源：中国新就业形态研究中心、暨南大学经济与社会研究院与智联招聘联合发布的《2026年中国灵活就业市场发展报告》。2025年灵活就业人员规模已达2.8亿，预计2026年将增至3.2亿，占全国7.25亿总就业人口的44%以上，正式从就业市场的"补充形式"转变为"重要支柱"。其中，依托互联网平台的新型灵活就业群体约8,400万人。'), s_small))
story.append(Spacer(1, 3))
story.append(P(escape('这意味着：超过3亿人正在或即将寻找灵活的收入来源——他们中绝大多数拥有时间、设备和基本的数字素养，但缺乏创业的方向、技能和供应链支持。'), s_body))

story.append(P('红利二：跨境电商成为政策驱动的"新引擎"', s_h3))
story.append(P(escape('国家层面持续推动跨境电商高质量发展，TikTok Shop等平台入驻门槛逐年优化，2026年东南亚市场支持个体工商户和部分个人身份入驻'), s_bullet))
story.append(P(escape('"一带一路"倡议深入推进，海关通关便利化、海外仓建设等基础设施不断完善'), s_bullet))
story.append(P(escape('新丝路品牌名自带"政策亲近度"，更容易获得政府、商会、产业园区的资源倾斜'), s_bullet))

story.append(P('红利三：供应链整合已出现"可复制的成功经验"', s_h3))
story.append(P(escape('SHEIN模式：通过"小单快反"柔性供应链，首单仅以100-200件小批量测试市场，根据实时销售数据敏捷返单，将行业平均库存率降至个位数'), s_bullet))
story.append(P(escape('1688一件代发模式：2026年完善的电商生态为个人卖家提供了无需囤货的"零风险"起步路径，启动资金可低至2,000元左右'), s_bullet))
story.append(P(escape('"自主品牌+平台"双引擎模式：SHEIN已形成"自主品牌+平台"双引擎，通过数字化柔性供应链支撑小单快反模式'), s_bullet))

# ===== 二、商业模型总览 =====
story.append(P('二、商业模型总览：供应链矩阵模型', s_h1))

# ASCII art as code block
art1_lines = [
    '┌─────────────────────────────────────────────────────────────────┐',
    '│ 新丝路·供应链矩阵计划总体架构                                      │',
    '├─────────────────────────────────────────────────────────────────┤',
    '│                                                                  │',
    '│ 顶层：供应链联盟（供给侧·深度）                                    │',
    '│ ├─ 制造企业入驻（5-6个产业带，100+优质供应商）                      │',
    '│ ├─ 产品库搭建（选品中心、数字化产品目录）                            │',
    '│ ├─ 合规基础设施（海外认证、商标、合规文档标准化）                    │',
    '│ └─ 履约系统（一件代发+海外仓+物流网络）                             │',
    '│        ↓ （产品供给 + 履约支持）                                   │',
    '│ 中层：新丝路平台（连接器·赋能器）                                   │',
    '│ ├─ 选品分发（按主题/地区/品类推送给个体矩阵）                        │',
    '│ ├─ 陪跑赋能（99元→线下课→矩阵陪跑，全链路培训）                      │',
    '│ ├─ 分账系统（自动分润，供应链85%：个体15%）                          │',
    '│ ├─ 合规监管（供应商审核、产品质量抽检、售后仲裁）                    │',
    '│ └─ 数据驱动（热销品数据分析→反向指导供应链生产）                     │',
    '│        ↓ （赋能个体 + 分发产品）                                    │',
    '│ 底层：个体出海矩阵（供给侧·广度）                                    │',
    '│ ├─ 个体来源：新丝路99元课学员、线下课学员、社会招募                  │',
    '│ ├─ 运营模式：以"一件代发""短视频带货""直播引流"为主                │',
    '│ ├─ 收入结构：销售佣金 + 矩阵激励 + 新丝路分成回馈                   │',
    '│ └─ 成长路径：新手（月销0-20单）→ 达人（月销20-200单）→ 合伙人     │',
    '│                                                                  │',
    '│ 核心飞轮：供应端深度支撑 × 个体端广度扩展 = 生态规模化增长           │',
    '└─────────────────────────────────────────────────────────────────┘',
]
for line in art1_lines:
    story.append(code(line))

# ===== 三、供应链联盟 =====
story.append(P('三、供应链联盟（顶层：供给侧·深度）', s_h1))

story.append(P('3.1 联盟定位与目标', s_h2))
story.append(P(escape('定位：成为中国制造企业出海的"产品中台"——企业只需专注生产和品质，出海获客和销售由新丝路及其个体矩阵网络完成。'), s_body))
story.append(P(escape('目标：第一年整合5-6个国内产业带，筛选100+优质制造商作为联盟初始核心供应商；第三年扩展至30+产业带，500+供应商。'), s_body))

story.append(P('3.2 供应商筛选标准', s_h2))
t2_data = [
    [P('维度', s_table_header), P('标准要求', s_table_header), P('筛选方式', s_table_header)],
    [P('产品品质', s_table_cell),
     P(escape('具有出口资质（如有ISO、CE等相关认证优先）'), s_table_body),
     P(escape('工厂实地考察+第三方验厂报告'), s_table_body)],
    [P('生产柔性', s_table_cell),
     P(escape('支持"小单快反"，最少起订量≤500件'), s_table_body),
     P(escape('现场考察生产流程+历史订单数据'), s_table_body)],
    [P('合作意愿', s_table_cell),
     P(escape('愿意接受代发模式、接受15%佣金分成'), s_table_body),
     P(escape('面谈+协议确认'), s_table_body)],
    [P('合规能力', s_table_cell),
     P(escape('能配合完成海外认证、产品标签等合规文件'), s_table_body),
     P(escape('文件审核+法律团队支持'), s_table_body)],
    [P('供应链透明度', s_table_cell),
     P(escape('接受新丝路定期抽查和品质监控'), s_table_body),
     P(escape('年度复检+飞行抽查'), s_table_body)],
]
t2 = Table(t2_data, colWidths=[80, 200, 160])
t2.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E4057')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t2)

story.append(P('3.3 供应链来源策略', s_h2))
story.append(P(escape('第一阶段（0-6个月）：挖掘现有资源池'), s_body))
story.append(P(escape('从雨哥IP粉丝中的企业主直接转化——通过发布"供应链联盟招募"内容，吸引有意出海的制造企业主动联系'), s_bullet))
story.append(P(escape('利用雨哥20年外贸积累的工厂人脉资源，定向邀约'), s_bullet))
story.append(P(escape('第二阶段（6-12个月）：产业带深度合作'), s_body))
story.append(P(escape('锁定5-6个重点产业带（小家电、家居用品、宠物用品、户外装备、3C配件、美妆工具）'), s_bullet))
story.append(P(escape('与地方政府/商协会合作，获取产业带推荐名录，进行批量筛选'), s_bullet))
story.append(P(escape('第三阶段（12个月+）：开放入驻+动态管理'), s_body))
story.append(P(escape('面向全社会开放供应商入驻申请，定期筛选优质新供应商'), s_bullet))
story.append(P(escape('实行月度/季度SKU销售排名，末位10%淘汰'), s_bullet))

story.append(P('3.4 联盟的核心价值：为供应商带来的收益', s_h2))
t3_data = [
    [P('价值点', s_table_header), P('具体内容', s_table_header)],
    [P('销售渠道扩展', s_table_cell), P(escape('通过个体矩阵触达海量C端用户，形成"渠道即矩阵"的规模效应'), s_table_body)],
    [P('市场测试窗口', s_table_cell), P(escape('利用"小单快反"模式，以极小成本测试海外市场反应'), s_table_body)],
    [P('合规降本', s_table_cell), P(escape('新丝路统一为供应商提供海外认证、商标注册的集采服务，降低单企业成本'), s_table_body)],
    [P('数据反哺', s_table_cell), P(escape('个体矩阵的销售数据反馈给供应链，指导产品迭代和爆款开发'), s_table_body)],
    [P('品牌出海', s_table_cell), P(escape('优质供应商可进入新丝路"品牌出海扶持计划"，获得独立品牌曝光'), s_table_body)],
]
t3 = Table(t3_data, colWidths=[100, 340])
t3.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E4057')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t3)

story.append(P('3.5 参考案例：SHEIN的"链式赋能"模式', s_h2))
story.append(P(escape('SHEIN通过"自营+平台"双引擎模式，以"小单快反"的柔性供应链为核心，实现"以销定产"，首单仅以100-200件小批量测试市场，再根据实时销售数据敏捷返单，将行业平均库存率降至个位数。更关键的是，SHEIN不仅自己运用这套模式，还手把手教供应商如何盘点库存、精准下单备货，每月举办自主运营与库存管理培训。通过数字化系统对接全球消费趋势，SHEIN已成为推动产业数智化转型升级的关键引擎。'), s_body))
story.append(P(escape('新丝路的差异化：SHEIN主要整合服装产业带，新丝路覆盖多品类（小家电、家居、宠物、户外等）；SHEIN主要服务自身平台，新丝路通过"供应链矩阵"模式，让矩阵内个体共同分销，形成"万品出海、万人分销"的生态。'), s_body))

# ===== 四、个体出海矩阵 =====
story.append(PageBreak())
story.append(P('四、个体出海矩阵（底层：供给侧·广度）', s_h1))

story.append(P('4.1 个体从哪里来？', s_h2))
story.append(P(escape('个体矩阵的三大来源渠道：'), s_body))

t4_data = [
    [P('来源', s_table_header), P('转化路径', s_table_header), P('目标规模（第一年）', s_table_header)],
    [P('新丝路99元课学员', s_table_cell),
     P(escape('完成课程→通过矩阵入驻考核→成为矩阵成员'), s_table_body),
     P('1,500-2,000人', s_table_cell)],
    [P('新丝路线下3天课学员', s_table_cell),
     P(escape('结课后邀请进入矩阵陪跑群→实战试单→正式加入'), s_table_body),
     P('300-500人', s_table_cell)],
    [P('社会公开招募', s_table_cell),
     P(escape('通过短视频、招聘平台、灵活就业平台招募'), s_table_body),
     P('1,000-2,000人', s_table_cell)],
]
t4 = Table(t4_data, colWidths=[110, 210, 120])
t4.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E4057')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t4)
story.append(Spacer(1, 4))
story.append(P(escape('为什么个体愿意来？启动门槛极低：无需营业执照、无需囤货、无需自建物流，全套供应链支持+新丝路培训陪跑+平台背书，个体只需专注内容创作和流量获取，即可实现"一人一台电脑"的跨境创业。'), s_body))

story.append(P('4.2 个体成长路径', s_h2))

growth_lines = [
    '┌─────────────────────────────────────────────────────────────────┐',
    '│ 层级          准入门槛                      权益                  │',
    '├─────────────────────────────────────────────────────────────────┤',
    '│                                                                  │',
    '│ L1：新手个体 → 完成新丝路入门课+矩阵培训       → 基础选品库、佣金5%   │',
    '│               → 注册跨境收款账户                                   │',
    '│                                                                  │',
    '│              ↓（月销突破20单）                                     │',
    '│                                                                  │',
    '│ L2：成长个体 → 连续3个月月销≥20单            → 佣金提升至8%        │',
    '│               → 完成进阶运营课               → 专属选品推荐         │',
    '│                                                                  │',
    '│              ↓（月销突破100单）                                    │',
    '│                                                                  │',
    '│ L3：资深个体 → 连续3个月月销≥100单           → 佣金提升至12%       │',
    '│               → 通过考核评审                 → 参加海外考察团       │',
    '│                                                                  │',
    '│              ↓（月销突破500单+团队）                               │',
    '│                                                                  │',
    '│ L4：矩阵合伙人 → 团队管理能力+推荐新成员      → 享受团队流水分成     │',
    '│                 → 与新丝路深度绑定            → 优先参与新业务      │',
    '│                                                                  │',
    '└─────────────────────────────────────────────────────────────────┘',
]
for line in growth_lines:
    story.append(code(line))

story.append(P('4.3 个体运营模式', s_h2))
story.append(P(escape('矩阵内个体采用"一件代发"（Dropshipping）模式为主。其逻辑非常简单：个体负责在前端店铺上架商品、引流接单；客户下单后，个体再拿着订单信息去1688等国内供应商处下单，由供应商直接发货给海外客户。这种模式的核心优势是：无需囤货、无需压资金、启动资金可低至2,000元左右。'), s_body))
story.append(P(escape('新丝路矩阵比普通1688代发更优的地方：'), s_body))

t5_data = [
    [P('维度', s_table_header), P('普通1688代发', s_table_header), P('新丝路矩阵代发', s_table_header)],
    [P('选品', s_table_cell), P('自己大海捞针', s_table_cell), P(escape('新丝路精选爆款+主题选品库推送'), s_table_cell)],
    [P('合规', s_table_cell), P('个体自行摸索', s_table_cell), P(escape('新丝路统一提供合规文件+认证支持'), s_table_cell)],
    [P('物流', s_table_cell), P('个体自己找货代', s_table_cell), P(escape('集采物流+海外仓备货，成本更低'), s_table_cell)],
    [P('收款', s_table_cell), P('个体自己开通', s_table_cell), P(escape('指导开户+与新丝路合作银行通道'), s_table_cell)],
    [P('培训', s_table_cell), P('无', s_table_cell), P(escape('新丝路全链路陪跑（选品→开店→出单→发货→售后）'), s_table_cell)],
    [P('售后', s_table_cell), P('个体自己处理', s_table_cell), P(escape('供应链统一处理+平台仲裁机制'), s_table_cell)],
]
t5 = Table(t5_data, colWidths=[60, 170, 210])
t5.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E4057')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t5)

story.append(P('4.4 个体佣金分成机制', s_h2))
t6_data = [
    [P('层级', s_table_header), P('基础佣金', s_table_header), P('达标奖励', s_table_header), P('综合佣金', s_table_header)],
    [P('L1新手', s_table_cell), P('5%', s_table_cell), P('—', s_table_cell), P('5%', s_table_cell)],
    [P('L2成长', s_table_cell), P('8%', s_table_cell), P('—', s_table_cell), P('8%', s_table_cell)],
    [P('L3资深', s_table_cell), P('12%', s_table_cell), P(escape('月销达标额外1%'), s_table_cell), P('13%', s_table_cell)],
    [P('L4合伙人', s_table_cell), P('12%', s_table_cell), P(escape('团队流水0.5%'), s_table_cell), P(escape('12.5%+'), s_table_cell)],
]
t6 = Table(t6_data, colWidths=[80, 80, 140, 80])
t6.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E4057')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t6)
story.append(Spacer(1, 4))
story.append(P(escape('单笔销售分润示意：一单100美元的订单，供应链获得85美元，矩阵个体获得15美元（约合人民币105元）。如果个体一个月出100单，月收入超过1万元；出500单，月收入超过5万元。'), s_body))

# ===== 五、平台的枢纽角色 =====
story.append(PageBreak())
story.append(P('五、平台的枢纽角色', s_h1))

story.append(P('5.1 平台的核心职能', s_h2))
story.append(P(escape('新丝路平台在"供应链联盟 + 个体矩阵"之间扮演三层角色：'), s_body))
story.append(P('角色一：连接器', s_h3))
story.append(P(escape('精选产品库，按品类/主题/目标市场推送推荐'), s_bullet))
story.append(P(escape('匹配制度：系统根据个体画像自动推荐适合的产品'), s_bullet))
story.append(P(escape('实现订单流、信息流、资金流三流合一'), s_bullet))
story.append(P('角色二：赋能器', s_h3))
story.append(P(escape('培训赋能（99元课→线下课→矩阵陪跑营，涵盖跨境电商从0到1全链路实操）'), s_bullet))
story.append(P(escape('工具赋能（AI工具、智能选品、自动化订单处理系统）'), s_bullet))
story.append(P(escape('合规赋能（统一认证、合规文档库、客服仲裁机制）'), s_bullet))
story.append(P('角色三：监管者', s_h3))
story.append(P(escape('供应商定期质量审核'), s_bullet))
story.append(P(escape('个体行为规范管理'), s_bullet))
story.append(P(escape('订单售后争议仲裁机制'), s_bullet))
story.append(P(escape('防止恶意刷单、知识产权侵权等风险'), s_bullet))

story.append(P('5.2 平台的核心技术系统规划', s_h2))
t7_data = [
    [P('系统模块', s_table_header), P('功能', s_table_header), P('优先级', s_table_header)],
    [P('选品中心', s_table_cell), P(escape('产品上架、分类展示、关键词搜索、数据分析'), s_table_body), P('P0（首年）', s_table_cell)],
    [P('分销系统', s_table_cell), P(escape('个体分销链接生成、订单跟踪、收益结算'), s_table_body), P('P0（首年）', s_table_cell)],
    [P('培训系统', s_table_cell), P(escape('课程上传、打卡、考试、矩阵准入'), s_table_body), P('P1（首年）', s_table_cell)],
    [P('分账系统', s_table_cell), P(escape('自动计算佣金、多级分成、月结功能'), s_table_body), P('P0（首年）', s_table_cell)],
    [P('履约系统', s_table_cell), P(escape('对接海外仓、物流追踪、一键代发'), s_table_body), P('P1（次年）', s_table_cell)],
    [P('数据分析平台', s_table_cell), P(escape('热销品趋势分析、个体画像分析、智能推荐'), s_table_body), P('P2（次年）', s_table_cell)],
]
t7 = Table(t7_data, colWidths=[80, 220, 80])
t7.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E4057')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t7)

story.append(P('5.3 与新丝路现有业务的关系', s_h2))
story.append(P(escape('从知识付费到供应链矩阵的转化路径：'), s_body))
story.append(P(escape('新丝路99元课 → 个体兴趣（跨境电商兴趣培养）'), s_bullet))
story.append(P(escape('新丝路线下3天实战课 → 个体实战（完成为期30天的陪跑试单）'), s_bullet))
story.append(P(escape('新丝路矩阵准入考核 → 正式加入矩阵（月收入稳定在3000元以上）'), s_bullet))
story.append(P(escape('个体孵化升级 → 合伙人/导师（带动新个体，享受团队分成）'), s_bullet))
story.append(P(escape('这种"培训→实战→孵化的自然阶梯"，形成了新丝路矩阵的持续内生增长飞轮。'), s_body))

# ===== 六、灵活就业数据支撑与社会价值 =====
story.append(P('六、灵活就业数据支撑与社会价值', s_h1))

story.append(P('6.1 为什么矩阵计划恰逢其时？', s_h2))
story.append(P(escape('3.2亿灵活就业人群的真实图景'), s_h3))

t8_data = [
    [P('数据类型', s_table_header), P('数据', s_table_header)],
    [P('2026年预计灵活就业总人数', s_table_cell), P('3.2亿人', s_table_cell)],
    [P('占全国总就业人口比例', s_table_cell), P('44%以上', s_table_cell)],
    [P('其中新就业形态劳动者', s_table_cell), P('约8,400万人', s_table_cell)],
    [P('年均新增灵活就业者', s_table_cell), P('约4,000万人', s_table_cell)],
    [P('制造业灵活用工人员', s_table_cell), P(escape('4,000万人（占制造业从业人员31.12%）'), s_table_cell)],
]
t8 = Table(t8_data, colWidths=[180, 250])
t8.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E4057')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t8)
story.append(Spacer(1, 4))

story.append(P(escape('数据来源：中国新就业形态研究中心发布的《2025中国蓝领群体就业研究报告》指出，2025年中国灵活就业从业人员达2.8亿人，预计2026年将增至3.2亿，占城镇就业的比例超过四成。其中约8,400万人依赖平台就业。制造业用工中灵活用工达4,000万人，占制造业从业人员31.12%，已形成"高新技术人员+灵活用工人员"的新型生产模式。'), s_small))
story.append(Spacer(1, 3))
story.append(P(escape('这意味着：中国有3.2亿人正在主动或被动地从事灵活就业，其中8,400万人已经熟悉平台化工作模式。新丝路矩阵计划的核心价值在于：把这3.2亿灵活就业人群中的一部分，从"低附加值劳动力"（外卖、网约车）升级为"高附加值跨境创业者" ——用中国供应链+个体矩阵，为灵活就业者提供更高收入的可能。'), s_body))

story.append(P('6.2 政策支持', s_h2))
story.append(P(escape('2026年6月，李强主持召开国务院常务会议，审议通过《实施就业优先战略"十五五"规划》。会议明确要求：要健全就业促进机制，完善就业创业服务体系，拓展高校毕业生等青年就业成才渠道，加大重点群体就业支持力度，推动灵活就业、新就业形态健康发展，加强劳动者就业权益保障。'), s_body))
story.append(P(escape('矩阵计划的推出，与新丝路"一带一路"丝路文化的品牌内涵形成了极具张力的共振：既响应了国家稳就业、促创业的宏观政策，又满足了3.2亿灵活就业人群的高质量就业需求。'), s_body))

# ===== 七、完整的生态闭环 =====
story.append(P('七、完整的生态闭环', s_h1))

eco_lines = [
    '┌─────────────────────────────────────────────────────────────────┐',
    '│ 新丝路·供应链矩阵生态闭环图                                        │',
    '├─────────────────────────────────────────────────────────────────┤',
    '│                                                                  │',
    '│ ① 供应端                                                         │',
    '│ 制造企业 → 加入供应链联盟 → 提供产品                                │',
    '│        ↓                                                        │',
    '│ ② 平台侧                                                         │',
    '│ 新丝路平台：选品中心+培训体系+订单分发+结算系统                      │',
    '│        ↓                                                        │',
    '│ ③ 个体侧                                                         │',
    '│ 个体矩阵通过培训成长→开店→分销产品→完成销售                          │',
    '│        ↓                                                        │',
    '│ ④ 数据回流                                                       │',
    '│ 销售数据反哺→爆款识别→反向指导供应链开发新品                         │',
    '│        ↓                                                        │',
    '│ ⑤ 闭环升级                                                       │',
    '│ 更多爆款产品 → 吸引更多个体 → 生态规模持续扩大 → 飞轮加速              │',
    '│                                                                  │',
    '└─────────────────────────────────────────────────────────────────┘',
]
for line in eco_lines:
    story.append(code(line))

# ===== 八、盈利模式 =====
story.append(PageBreak())
story.append(P('八、盈利模式', s_h1))

story.append(P('8.1 收入来源矩阵', s_h2))
t9_data = [
    [P('收入来源', s_table_header), P('模式', s_table_header),
     P('成熟期年收入', s_table_header), P('毛利率', s_table_header)],
    [P('供应链佣金', s_table_cell),
     P(escape('每笔销售抽取15%（供应链85%+平台管理费）——实际为供应链85%，平台直接从15%佣金中分成'), s_table_body),
     P('2,000-3,000万元', s_table_cell), P('100%', s_table_cell)],
    [P('个体会员费', s_table_cell),
     P(escape('月费29元/人，包含无限次选品库访问+基础培训'), s_table_body),
     P('200-300万元', s_table_cell), P('90%', s_table_cell)],
    [P('供应链入驻费', s_table_cell),
     P(escape('供应商年费3,000-10,000元/家'), s_table_body),
     P('50-100万元', s_table_cell), P('100%', s_table_cell)],
    [P('配套服务', s_table_cell),
     P(escape('物流/海外仓/收款/认证等配套增值服务佣金'), s_table_body),
     P('500-1,000万元', s_table_cell), P('50%', s_table_cell)],
    [P('培训费', s_table_cell),
     P(escape('新丝路99元引流课+线下课收入（与知识付费版块合并统计）'), s_table_body),
     P(escape('计入知识付费版块'), s_table_cell), P('50-60%', s_table_cell)],
    [P('生态衍生收入', s_table_cell),
     P(escape('供应链金融服务、广告投放、数据服务'), s_table_body),
     P('300-500万元', s_table_cell), P('80%', s_table_cell)],
]
t9 = Table(t9_data, colWidths=[75, 185, 100, 50])
t9.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E4057')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
story.append(t9)
story.append(Spacer(1, 4))
story.append(P(escape('成熟期合计（不含知识付费版块）：约3,000-5,000万元（不含知识付费收入）'), s_body))

story.append(P('8.2 成本结构', s_h2))
t10_data = [
    [P('成本项', s_table_header), P('占比', s_table_header), P('说明', s_table_header)],
    [P('平台开发与维护', s_table_cell), P('20%', s_table_cell), P(escape('选品中心、订单系统、分账系统建设'), s_table_body)],
    [P('运营与BD', s_table_cell), P('25%', s_table_cell), P(escape('供应链拓展、个体招募、日常运营'), s_table_body)],
    [P('培训与内容', s_table_cell), P('15%', s_table_cell), P(escape('课程开发、讲师费用、陪跑服务'), s_table_body)],
    [P('物流补贴', s_table_cell), P('10%', s_table_cell), P(escape('个体起步期的物流补贴'), s_table_body)],
    [P('推广与获客', s_table_cell), P('20%', s_table_cell), P(escape('个体招募、供应链品牌推广'), s_table_body)],
    [P('其他', s_table_cell), P('10%', s_table_cell), P(escape('办公、人员、合规咨询等'), s_table_body)],
]
t10 = Table(t10_data, colWidths=[100, 60, 270])
t10.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E4057')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t10)

# ===== 九、参考案例 =====
story.append(P('九、参考案例与成功借鉴', s_h1))

story.append(P('9.1 SHEIN："链式赋能"的供应链整合标杆', s_h2))
story.append(P(escape('SHEIN通过"小单快反"的柔性供应链模式创新，实现"以销定产"，革新了传统生产逻辑。所有产品首单以100-200件的极小规模测试市场，再根据实时销售数据敏捷返单。其"SHEIN链"串联起品牌与供应商，在链主企业的带动下，产业链从开发、生产、仓储、物流等各环节实现数字化升级。'), s_body))
story.append(P(escape('矩阵计划的借鉴：将SHEIN的"链式赋能"逻辑应用于多品类供应链，打造"新丝路链"。'), s_body))

story.append(P('9.2 苏宁易购："拎包出海"的一站式方案', s_h2))
story.append(P(escape('苏宁易购推出"一站式出海平台"，为中国商家提供"拎包出海"的全链路解决方案。商家可灵活选择"直邮模式""入仓模式"两种仓储服务履约模式，以及"全托管""半托管""供应链补充"三种运营模式，真正实现低门槛、低风险的全球化布局。'), s_body))
story.append(P(escape('矩阵计划的借鉴：为新丝路个体提供类似的"拎包出海"体验——个体无需思考任何供应链问题，只管内容创作和引流。'), s_body))

story.append(P('9.3 菜鸟&鲸芽："多渠道一盘货"的库存模式', s_h2))
story.append(P(escape('菜鸟联合鲸芽推出的"多渠道、一盘货"解决方案，帮助商家实现多平台库存共享与一键发货。'), s_body))
story.append(P(escape('矩阵计划的借鉴：新丝路矩阵可打造"多平台一盘货"——个体可在TikTok Shop、Shopee、独立站等多个渠道同时分销同一产品库。'), s_body))

story.append(P('9.4 三节课："内容+服务+平台"的赋能模式', s_h2))
story.append(P(escape('三节课作为中国领先的数字化人才战略服务商，面向企业和个人用户提供以"内容+服务+平台"为核心的数字化人才战略解决方案。'), s_body))
story.append(P(escape('矩阵计划的借鉴：新丝路矩阵的赋能体系同样遵循"内容+服务+平台"的框架——内容（99元课→线下课→矩阵进阶课程）、服务（陪跑、诊断、售后仲裁）、平台（选品中心、订单分发、佣金结算）。'), s_body))

# ===== 十、实施路线图 =====
story.append(PageBreak())
story.append(P('十、实施路线图', s_h1))

story.append(P('阶段一：基建与启动期（0-6个月）', s_h2))
t11_data = [
    [P('时间节点', s_table_header), P('关键任务', s_table_header)],
    [P('第1个月', s_table_cell), P(escape('供应链联盟供应商筛选标准确立、首批10-20家核心供应商洽谈'), s_table_body)],
    [P('第2-3个月', s_table_cell), P(escape('平台选品中心MVP开发、个体培训课程体系搭建'), s_table_body)],
    [P('第3-4个月', s_table_cell), P(escape('从新丝路99元课和线下课学员中招募首批200名种子个体'), s_table_body)],
    [P('第4-5个月', s_table_cell), P(escape('首批个体完成培训并通过考核，启动首批产品上线（200-300个SKU）'), s_table_body)],
    [P('第5-6个月', s_table_cell), P(escape('全链路跑通（选品→培训→分销→出单→结算），形成可复制SOP'), s_table_body)],
]
t11 = Table(t11_data, colWidths=[80, 350])
t11.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E4057')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t11)
story.append(Spacer(1, 2))
story.append(P(escape('里程碑：首批200名个体成功出单，月销售额破50万元。'), s_body))

story.append(P('阶段二：规模化扩展期（6-18个月）', s_h2))
t12_data = [
    [P('时间节点', s_table_header), P('关键任务', s_table_header)],
    [P('第6-9个月', s_table_cell), P(escape('供应链联盟扩至5-6个产业带，供应商达60-80家'), s_table_body)],
    [P('第9-12个月', s_table_cell), P(escape('个体矩阵扩至1,000人，平台SKU达1,000+'), s_table_body)],
    [P('第12-15个月', s_table_cell), P(escape('上线完整的分账系统和履约系统，引入物流集采'), s_table_body)],
    [P('第15-18个月', s_table_cell), P(escape('启动供应链金融服务，为成长个体提供资金周转支持'), s_table_body)],
]
t12 = Table(t12_data, colWidths=[80, 350])
t12.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E4057')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t12)
story.append(Spacer(1, 2))
story.append(P(escape('里程碑：矩阵月销售额破500万元，个体平均月收入达3,000元。'), s_body))

story.append(P('阶段三：生态成熟期（18-36个月）', s_h2))
t13_data = [
    [P('时间节点', s_table_header), P('关键任务', s_table_header)],
    [P('第18-24个月', s_table_cell), P(escape('覆盖30+产业带，供应商达300-500家'), s_table_body)],
    [P('第24-30个月', s_table_cell), P(escape('矩阵个体达5,000-10,000人，SKU达3,000+'), s_table_body)],
    [P('第30-36个月', s_table_cell), P(escape('拓展至多平台（独立站、Amazon、Temu等），形成多平台分销网络'), s_table_body)],
]
t13 = Table(t13_data, colWidths=[80, 350])
t13.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E4057')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t13)
story.append(Spacer(1, 2))
story.append(P(escape('里程碑：矩阵年销售额破亿元，培养出100+月入过万的个体从业者。'), s_body))

# ===== 十一、风险与应对 =====
story.append(P('十一、风险与应对', s_h1))

t14_data = [
    [P('风险类别', s_table_header), P('具体风险', s_table_header), P('应对策略', s_table_header)],
    [P('供应端风险', s_table_cell), P(escape('供应商产品质量不稳定、履约效率低'), s_table_body),
     P(escape('严格的供应商准入审核机制；每月匿名抽查批次；设立供应商黑名单制度'), s_table_body)],
    [P('个体端风险', s_table_cell), P(escape('个体违规操作（刷单、侵权、套利）'), s_table_body),
     P(escape('建立个体行为规范红线；设立违规积分累计扣分制；严重的直接清退并公示'), s_table_body)],
    [P('平台运营风险', s_table_cell), P(escape('订单纠纷处理不当，影响平台信誉'), s_table_body),
     P(escape('设立标准化售后仲裁流程；为订单购买商业保险；运营团队专人负责'), s_table_body)],
    [P('竞争风险', s_table_cell), P(escape('其他平台模仿"供应链+个体"模式'), s_table_body),
     P(escape('依托雨哥IP的信任壁垒+供应链独家合作+个体陪跑的深度护城河'), s_table_body)],
    [P('政策风险', s_table_cell), P(escape('跨境监管政策变化'), s_table_body),
     P(escape('密切跟踪目标国家的跨境电商政策变化；法律服务团队及时协助调整方案'), s_table_body)],
]
t14 = Table(t14_data, colWidths=[75, 160, 205])
t14.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E4057')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t14)

# ===== 十二、核心亮点总结 =====
story.append(P('十二、核心亮点总结', s_h1))
story.append(P(escape('时代刚需：3.2亿灵活就业人群 + 国家稳就业政策 + 跨境电商红利 = 巨大的市场窗口'), s_bullet))
story.append(P(escape('模式创新："供应链+个体"的双引擎模式，区别于单一的知识付费或单一的服务平台'), s_bullet))
story.append(P(escape('产业链协同：供应端（国内制造企业）+ 平台端（新丝路）+ 个体端（灵活就业群体）三方共赢——企业获得海外市场渠道，个体获得高收益机会，平台获得持续收入'), s_bullet))
story.append(P(escape('可持续飞轮：供应链提供优质产品→个体创业创造销量→数据反馈供应链优化→更多爆款产品吸引更多个体加入→飞轮效应持续加速'), s_bullet))
story.append(P(escape('社会价值：将低技能的外卖/网约车"时间换钱"型灵活就业，升级为通过中国供应链+跨境电商创业的高价值就业模式，切实助力国家稳就业战略'), s_bullet))
story.append(P(escape('IP护城河：依托雨哥20年外贸实战IP的信任资产，新丝路矩阵的获客成本和转化效率天然优于其他类似平台'), s_bullet))

# ===== 十三、矩阵计划与新丝路知识付费业务的融合 =====
story.append(PageBreak())
story.append(P('十三、矩阵计划与新丝路知识付费业务的融合', s_h1))

t15_data = [
    [P('业务版块', s_table_header), P('关系', s_table_header), P('协同逻辑', s_table_header)],
    [P(escape('知识付费（99元课）'), s_table_cell), P('流量入口', s_table_cell),
     P(escape('为矩阵计划筛选意向个体，形成人才储备'), s_table_body)],
    [P(escape('知识付费（3天线下课）'), s_table_cell), P('实战漏斗', s_table_cell),
     P(escape('为矩阵个体提供深度实战培训+30天陪跑'), s_table_body)],
    [P('供应链矩阵计划', s_table_cell), P('盈利闭环', s_table_cell),
     P(escape('个体通过矩阵获得持续收入，驱动知识付费业务复购和转介绍'), s_table_body)],
    [P('出海全链路服务平台', s_table_cell), P('后端延伸', s_table_cell),
     P(escape('成长个体/合伙人可升级为企业主，进入更高价值的平台服务层'), s_table_body)],
]
t15 = Table(t15_data, colWidths=[120, 70, 240])
t15.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E4057')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t15)
story.append(Spacer(1, 8))

story.append(P(escape('整体生态闭环：99元课（兴趣）→ 线下3天课（实战）→ 矩阵准入考核（筛选）→ 个体矩阵孵化（出单）→ 平台服务（深度绑定）→ 供应链联盟（供应升级）。每一步都是自然的向上流动，最终形成"知识付费引流、供应链矩阵变现、全链路服务增值"的三轮驱动格局。'), s_body))

story.append(Spacer(1, 15))
# Final line
story.append(hr())
story.append(P(escape('新丝路·供应链矩阵计划——让供应链做深度，让个体做广度，让中国制造走得更远。'), s_body))

# ── 4. Build PDF ──
doc.build(story)
print(f"PDF saved to: {output_path}")
