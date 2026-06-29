# -*- coding: utf-8 -*-
"""Convert document to PDF with beautiful, modern layout."""

import os, sys, platform
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    KeepTogether, HRFlowable, Table, TableStyle,
    PageTemplate, Frame, BaseDocTemplate, NextPageTemplate,
    Flowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

# ═══════════════════════════════════════════════════
# Color Palette
# ═══════════════════════════════════════════════════
C_PRIMARY    = HexColor('#1B3A5C')  # Deep navy
C_ACCENT     = HexColor('#C9A84C')  # Gold accent (丝路 vibe)
C_ACCENT2    = HexColor('#E8D5A3')  # Light gold
C_DARK       = HexColor('#0F2440')  # Darker navy
C_LIGHT_BG   = HexColor('#F7F5F0')  # Warm off-white
C_WHITE      = white
C_TEXT       = HexColor('#2C2C2C')
C_TEXT_LIGHT = HexColor('#6B6B6B')
C_TABLE_HEAD = HexColor('#1B3A5C')
C_TABLE_ALT  = HexColor('#F0ECE3')
C_TABLE_BORDER = HexColor('#D4CFC4')
C_SECTION_BG = HexColor('#ECE8DC')
C_SUBTITLE   = HexColor('#8B7D62')

# ═══════════════════════════════════════════════════
# Register Chinese Font
# ═══════════════════════════════════════════════════
system = platform.system()
cn_font = None
cn_bold = None

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
        ]:
            fp = os.path.join(d, fname)
            if os.path.exists(fp):
                try:
                    pdfmetrics.registerFont(TTFont(name, fp, subfontIndex=idx))
                    if 'Bold' in name:
                        cn_bold = name
                    else:
                        cn_font = name
                except:
                    continue
    if cn_bold is None and cn_font:
        cn_bold = cn_font
elif system == 'Darwin':
    for fp, name, idx in [
        ('/System/Library/Fonts/STHeiti Medium.ttc', 'STHeitiMedium', 0),
        ('/System/Library/Fonts/STHeiti Light.ttc', 'STHeitiLight', 0),
    ]:
        if os.path.exists(fp):
            pdfmetrics.registerFont(TTFont(name, fp, subfontIndex=idx))
            if cn_font is None:
                cn_font = name
            cn_bold = cn_bold or name
else:
    for fp, name, idx in [
        ('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 'NotoSansCJKBold', 0),
        ('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 'NotoSansCJK', 0),
    ]:
        if os.path.exists(fp):
            pdfmetrics.registerFont(TTFont(name, fp, subfontIndex=idx))
            if 'Bold' in name:
                cn_bold = name
            else:
                cn_font = name

if cn_font is None:
    raise RuntimeError(f"No CJK font found on {system}")
if cn_bold is None:
    cn_bold = cn_font

print(f"Font: {cn_font}, Bold: {cn_bold}")

# ═══════════════════════════════════════════════════
# Style Definitions
# ═══════════════════════════════════════════════════
def make_styles():
    s = {}
    
    # Base text
    s['body'] = ParagraphStyle('Body', fontName=cn_font, fontSize=10, leading=17,
                                spaceAfter=5, alignment=TA_JUSTIFY, textColor=C_TEXT)
    s['body_small'] = ParagraphStyle('BodySmall', fontName=cn_font, fontSize=8.5, leading=13,
                                      spaceAfter=3, textColor=C_TEXT_LIGHT)
    s['bullet'] = ParagraphStyle('Bullet', parent=s['body'], leftIndent=18,
                                  firstLineIndent=0, spaceAfter=3, leading=16)
    s['code'] = ParagraphStyle('Code', fontName=cn_font, fontSize=7.2, leading=10.5,
                                leftIndent=8, spaceAfter=1.5, spaceBefore=1.5,
                                textColor=HexColor('#3A3A3A'))
    
    # Hierarchical headings
    s['h1'] = ParagraphStyle('H1', fontName=cn_bold, fontSize=18, leading=26,
                              spaceBefore=20, spaceAfter=10,
                              textColor=C_PRIMARY)
    s['h2'] = ParagraphStyle('H2', fontName=cn_bold, fontSize=14, leading=20,
                              spaceBefore=14, spaceAfter=6,
                              textColor=C_PRIMARY)
    s['h3'] = ParagraphStyle('H3', fontName=cn_bold, fontSize=11.5, leading=17,
                              spaceBefore=10, spaceAfter=4,
                              textColor=HexColor('#2C5F8A'))
    
    # Table styles
    s['th'] = ParagraphStyle('TH', fontName=cn_bold, fontSize=8.5, leading=13,
                              alignment=TA_CENTER, textColor=C_WHITE)
    s['tc'] = ParagraphStyle('TC', fontName=cn_font, fontSize=8.5, leading=13,
                              alignment=TA_CENTER, textColor=C_TEXT)
    s['tl'] = ParagraphStyle('TL', fontName=cn_font, fontSize=8.5, leading=13,
                              textColor=C_TEXT)
    
    # Special
    s['subtitle'] = ParagraphStyle('Subtitle', fontName=cn_font, fontSize=12, leading=18,
                                    alignment=TA_CENTER, spaceAfter=6, textColor=C_SUBTITLE)
    s['tagline'] = ParagraphStyle('Tagline', fontName=cn_font, fontSize=11, leading=16,
                                   alignment=TA_CENTER, spaceAfter=30, textColor=C_TEXT_LIGHT)
    s['cover_quote'] = ParagraphStyle('CoverQuote', fontName=cn_font, fontSize=14, leading=22,
                                       alignment=TA_CENTER, spaceAfter=8, textColor=C_ACCENT)
    return s

S = make_styles()

# ═══════════════════════════════════════════════════
# Helper functions
# ═══════════════════════════════════════════════════
def P(text, style=S['body']):
    return Paragraph(text, style)

def escape(text):
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

def bullet(text):
    return P(f'<bullet>&bull;</bullet> {escape(text)}', S['bullet'])

def code(text):
    return P(escape(text), S['code'])

def colored_hr(color=C_ACCENT, thickness=0.8, vspace=8):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                       spaceBefore=vspace, spaceAfter=vspace)

def make_table(headers, rows, col_widths=None, first_col_center=False):
    """Create a styled table with alternating rows.
    Args:
        headers: list of header strings
        rows: list of rows, each row is a list of cell strings (or Paragraph objects)
        col_widths: list of column widths
        first_col_center: if True, center the first column
    Returns:
        Table flowable
    """
    all_rows = [[P(h, S['th']) for h in headers]]
    for i, row in enumerate(rows):
        row_paras = []
        for j, cell in enumerate(row):
            if isinstance(cell, Paragraph):
                row_paras.append(cell)
            elif j == 0 and first_col_center:
                row_paras.append(P(cell, S['tc']))
            else:
                row_paras.append(P(cell, S['tl']))
        all_rows.append(row_paras)
    
    if col_widths is None:
        n = len(headers)
        avail = 440  # usable width
        col_widths = [avail // n] * n
    
    t = Table(all_rows, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), C_TABLE_HEAD),
        ('TEXTCOLOR', (0, 0), (-1, 0), C_WHITE),
        ('GRID', (0, 0), (-1, -1), 0.4, C_TABLE_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    # Alternating row colors
    for i in range(1, len(all_rows)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), C_TABLE_ALT))
    t.setStyle(TableStyle(style_cmds))
    return t


# ═══════════════════════════════════════════════════
# Custom flowables
# ═══════════════════════════════════════════════════

class SectionHeader(Flowable):
    """A decorative section header with gold bar."""
    def __init__(self, number, title, width=440):
        Flowable.__init__(self)
        self.number = number
        self.title = title
        self.avail_width = width
        self.padding = 4
        
    def draw(self):
        c = self.canv
        c.saveState()
        y = 0
        
        # Draw gold bar on the left
        bar_w = 4
        bar_h = 22
        c.setFillColor(C_ACCENT)
        c.roundRect(0, y, bar_w, bar_h, 1.5, fill=1, stroke=0)
        
        # Draw number circle
        circle_x = bar_w + 8
        circle_r = 9
        c.setFillColor(C_PRIMARY)
        c.circle(circle_x + circle_r, y + bar_h/2, circle_r, fill=1, stroke=0)
        c.setFillColor(C_WHITE)
        c.setFont(cn_bold, 10)
        c.drawCentredString(circle_x + circle_r, y + bar_h/2 - 4, self.number)
        
        # Draw title text
        text_x = circle_x + circle_r * 2 + 8
        c.setFillColor(C_PRIMARY)
        c.setFont(cn_bold, 16)
        c.drawString(text_x, y + bar_h/2 - 6, self.title)
        
        # Draw gold underline
        underline_y = y - 3
        c.setStrokeColor(C_ACCENT2)
        c.setLineWidth(1.5)
        c.line(0, underline_y, self.avail_width, underline_y)
        
        self.width = self.avail_width
        self.height = bar_h + 6
        c.restoreState()


class CoverPage(Flowable):
    """Full-page cover design."""
    def __init__(self, width, height):
        Flowable.__init__(self)
        self.avail_width = width
        self.avail_height = height
        
    def draw(self):
        c = self.canv
        c.saveState()
        w = self.avail_width
        h = self.avail_height
        
        # Background
        c.setFillColor(C_LIGHT_BG)
        c.rect(0, 0, w, h, fill=1, stroke=0)
        
        # Top decorative band
        c.setFillColor(C_PRIMARY)
        c.rect(0, h - 120, w, 120, fill=1, stroke=0)
        
        # Gold accent line under band
        c.setStrokeColor(C_ACCENT)
        c.setLineWidth(3)
        c.line(0, h - 120, w, h - 120)
        
        # Gold thin line
        c.setStrokeColor(C_ACCENT2)
        c.setLineWidth(0.8)
        c.line(0, h - 124, w, h - 124)
        
        # Decorative element in dark band - circles
        for i in range(5):
            cx = 60 + i * 90
            alpha = 0.15 + i * 0.04
            c.setFillColor(Color(1, 1, 1, alpha=alpha))
            c.circle(cx, h - 60, 25 - i * 2, fill=1, stroke=0)
        
        # Title in dark band
        c.setFillColor(C_WHITE)
        c.setFont(cn_bold, 26)
        c.drawCentredString(w/2, h - 70, "新丝路·供应链矩阵计划")
        
        # Subtitle below band
        c.setFillColor(C_SUBTITLE)
        c.setFont(cn_font, 13)
        c.drawCentredString(w/2, h - 155, "以供应链为根基 · 以个体为触角 · 以陪跑为纽带的出海新生态")
        
        # Decorative gold divider
        div_y = h - 175
        c.setStrokeColor(C_ACCENT)
        c.setLineWidth(1.5)
        c.line(w/2 - 60, div_y, w/2 + 60, div_y)
        
        # Three key points
        points = [
            "供应端 · 深度     整合优质制造企业，打造出海供应链联盟",
            "个体端 · 广度     赋能3.2亿灵活就业人群，人人出海",
            "平台端 · 枢纽     连接器+赋能器，全链路服务生态",
        ]
        start_y = h - 215
        for i, pt in enumerate(points):
            c.setFillColor(C_TEXT)
            c.setFont(cn_font, 10.5)
            c.drawString(70, start_y - i * 28, pt)
            
            # Gold dot
            c.setFillColor(C_ACCENT)
            c.circle(55, start_y - i * 28 + 4, 3, fill=1, stroke=0)
        
        # Bottom decorative bar
        c.setFillColor(C_PRIMARY)
        c.rect(0, 0, w, 50, fill=1, stroke=0)
        c.setFillColor(C_ACCENT)
        c.setFont(cn_font, 9)
        c.drawCentredString(w/2, 18, "新丝路 · 让供应链做深度，让个体做广度，让中国制造走得更远")
        
        # Side gold line
        c.setStrokeColor(C_ACCENT)
        c.setLineWidth(2)
        c.line(30, 70, 30, h - 135)
        
        self.width = w
        self.height = h
        c.restoreState()


# ═══════════════════════════════════════════════════
# Page template
# ═══════════════════════════════════════════════════

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
    
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        canvas.Canvas.showPage(self)
    
    def save(self):
        num_pages = len(self._saved_page_states)
        for i, state in enumerate(self._saved_page_states):
            self.__dict__.update(state)
            self.draw_footer(i + 1, num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
    
    def draw_footer(self, page_num, num_pages):
        w, h = A4
        # Footer line
        self.setStrokeColor(C_ACCENT2)
        self.setLineWidth(0.5)
        self.line(22*mm, 15*mm, w - 22*mm, 15*mm)
        # Footer text
        self.setFillColor(C_TEXT_LIGHT)
        self.setFont(cn_font, 7.5)
        self.drawCentredString(w/2, 10*mm, f"— {page_num} / {num_pages} —")
        # Left text
        self.drawString(22*mm, 10*mm, "新丝路·供应链矩阵计划 | 内部文件")

# ═══════════════════════════════════════════════════
# Build Document Story
# ═══════════════════════════════════════════════════

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           '新丝路·供应链矩阵计划.pdf')

doc = SimpleDocTemplate(
    output_path, pagesize=A4,
    topMargin=22*mm, bottomMargin=22*mm,
    leftMargin=22*mm, rightMargin=22*mm,
    title='新丝路·供应链矩阵计划',
    author='新丝路'
)

W = 440  # usable width
story = []

# ═══════ COVER PAGE ═══════
story.append(Spacer(1, 5))
story.append(CoverPage(W, 730))
story.append(PageBreak())

# ═══════ SECTION 1 ═══════
story.append(SectionHeader("一", "核心定位与时代背景"))
story.append(Spacer(1, 6))

story.append(P(escape('计划名称：新丝路·供应链矩阵计划（以下简称"矩阵计划"）'), S['h2']))

story.append(P(escape('核心逻辑：'), S['body']))
story.append(P(escape('供应链是出海的"炮弹"，个体是出海的"炮兵"。传统的出海模式是"工厂自己当炮兵"——既要做产品，又要跑运营，两头不靠岸。矩阵计划颠覆这一逻辑：<b>供应链做深度，个体做广度。</b>'), S['body']))

story.append(P('供应端（深度）', S['bullet']))
story.append(P(escape('新丝路整合国内优质制造企业，形成"出海供应链联盟"，提供产品库、代发履约、合规认证、海外仓储等基础设施'), S['bullet']))
story.append(P('个体端（广度）', S['bullet']))
story.append(P(escape('赋能中国3.2亿灵活就业人群中的一部分，让他们以"一件代发""短视频带货""TikTok直播"等形式成为供应链的触角，实现"人人出海、万品出海"'), S['bullet']))
story.append(P('新丝路平台（枢纽）', S['bullet']))
story.append(P(escape('作为中间的"连接器+赋能器"，提供培训赋能、选品中心、代发系统、合规保障、收益分账等全链路服务'), S['bullet']))

story.append(P('时代背景：三大结构性红利', S['h2']))

# 红利一
story.append(P('红利一：灵活就业已成为中国劳动力市场的"新常态"', S['h3']))
t1 = make_table(
    ['时间节点', '灵活就业人数', '占就业人口比例', '年均增长'],
    [
        ['2021年', '约2.0亿', '约28%', '—'],
        ['2024年底', '2.4亿', '超33%', '约1,300万/年'],
        ['2025年', '2.8亿', '约39%', '约4,000万/年'],
        ['2026年（预计）', '3.2亿', '约44%', '约4,000万/年'],
    ],
    [85, 85, 95, 95]
)
story.append(t1)
story.append(Spacer(1, 4))
story.append(P(escape('数据来源：中国新就业形态研究中心、暨南大学经济与社会研究院与智联招聘联合发布的《2026年中国灵活就业市场发展报告》。2025年灵活就业人员规模已达2.8亿，预计2026年将增至3.2亿，占全国7.25亿总就业人口的44%以上，正式从就业市场的"补充形式"转变为"重要支柱"。其中，依托互联网平台的新型灵活就业群体约8,400万人。'), S['body_small']))
story.append(Spacer(1, 3))
story.append(P(escape('这意味着：超过3亿人正在或即将寻找灵活的收入来源——他们中绝大多数拥有时间、设备和基本的数字素养，但缺乏创业的方向、技能和供应链支持。'), S['body']))

# 红利二
story.append(P('红利二：跨境电商成为政策驱动的"新引擎"', S['h3']))
story.append(P(escape('国家层面持续推动跨境电商高质量发展，TikTok Shop等平台入驻门槛逐年优化，2026年东南亚市场支持个体工商户和部分个人身份入驻'), S['bullet']))
story.append(P(escape('"一带一路"倡议深入推进，海关通关便利化、海外仓建设等基础设施不断完善'), S['bullet']))
story.append(P(escape('新丝路品牌名自带"政策亲近度"，更容易获得政府、商会、产业园区的资源倾斜'), S['bullet']))

# 红利三
story.append(P('红利三：供应链整合已出现"可复制的成功经验"', S['h3']))
story.append(P(escape('SHEIN模式：通过"小单快反"柔性供应链，首单仅以100-200件小批量测试市场，根据实时销售数据敏捷返单，将行业平均库存率降至个位数'), S['bullet']))
story.append(P(escape('1688一件代发模式：2026年完善的电商生态为个人卖家提供了无需囤货的"零风险"起步路径，启动资金可低至2,000元左右'), S['bullet']))
story.append(P(escape('"自主品牌+平台"双引擎模式：SHEIN已形成"自主品牌+平台"双引擎，通过数字化柔性供应链支撑小单快反模式'), S['bullet']))

# ═══════ SECTION 2 ═══════
story.append(PageBreak())
story.append(SectionHeader("二", "商业模型总览"))
story.append(Spacer(1, 4))

story.append(P('供应链矩阵模型', S['h2']))

art1 = [
    '┌───────────────────────────────────────────────────────────────────────┐',
    '│                      新丝路 · 供应链矩阵计划总体架构                     │',
    '├───────────────────────────────────────────────────────────────────────┤',
    '│                                                                        │',
    '│  ◆ 顶层 · 供应链联盟（供给侧 · 深度）                                   │',
    '│    ├─ 制造企业入驻（5-6个产业带，100+优质供应商）                        │',
    '│    ├─ 产品库搭建（选品中心、数字化产品目录）                              │',
    '│    ├─ 合规基础设施（海外认证、商标、合规文档标准化）                      │',
    '│    └─ 履约系统（一件代发+海外仓+物流网络）                               │',
    '│                                                                        │',
    '│                          ↓ 产品供给 + 履约支持                           │',
    '│                                                                        │',
    '│  ◆ 中层 · 新丝路平台（连接器 · 赋能器）                                 │',
    '│    ├─ 选品分发（按主题/地区/品类推送给个体矩阵）                          │',
    '│    ├─ 陪跑赋能（99元→线下课→矩阵陪跑，全链路培训）                        │',
    '│    ├─ 分账系统（自动分润，供应链85%：个体15%）                            │',
    '│    ├─ 合规监管（供应商审核、产品质量抽检、售后仲裁）                      │',
    '│    └─ 数据驱动（热销品数据分析→反向指导供应链生产）                       │',
    '│                                                                        │',
    '│                          ↓ 赋能个体 + 分发产品                           │',
    '│                                                                        │',
    '│  ◆ 底层 · 个体出海矩阵（供给侧 · 广度）                                 │',
    '│    ├─ 个体来源：新丝路99元课学员、线下课学员、社会招募                    │',
    '│    ├─ 运营模式：以"一件代发""短视频带货""直播引流"为主                  │',
    '│    ├─ 收入结构：销售佣金 + 矩阵激励 + 新丝路分成回馈                     │',
    '│    └─ 成长路径：新手（月销0-20单）→ 达人（月销20-200单）→ 合伙人       │',
    '│                                                                        │',
    '│  ● 核心飞轮：供应端深度支撑 × 个体端广度扩展 = 生态规模化增长             │',
    '└───────────────────────────────────────────────────────────────────────┘',
]
for line in art1:
    story.append(code(line))

# ═══════ SECTION 3 ═══════
story.append(PageBreak())
story.append(SectionHeader("三", "供应链联盟"))
story.append(Spacer(1, 4))
story.append(P('顶层 · 供给侧 · 深度', S['subtitle']))
story.append(Spacer(1, 6))

story.append(P('联盟定位与目标', S['h2']))
story.append(P(escape('定位：成为中国制造企业出海的"产品中台"——企业只需专注生产和品质，出海获客和销售由新丝路及其个体矩阵网络完成。'), S['body']))
story.append(P(escape('目标：第一年整合5-6个国内产业带，筛选100+优质制造商作为联盟初始核心供应商；第三年扩展至30+产业带，500+供应商。'), S['body']))

story.append(P('供应商筛选标准', S['h2']))

rows = [
    ['产品品质', escape('具有出口资质（如有ISO、CE等相关认证优先）'), escape('工厂实地考察+第三方验厂报告')],
    ['生产柔性', escape('支持"小单快反"，最少起订量≤500件'), escape('现场考察生产流程+历史订单数据')],
    ['合作意愿', escape('愿意接受代发模式、接受15%佣金分成'), escape('面谈+协议确认')],
    ['合规能力', escape('能配合完成海外认证、产品标签等合规文件'), escape('文件审核+法律团队支持')],
    ['供应链透明度', escape('接受新丝路定期抽查和品质监控'), escape('年度复检+飞行抽查')],
]
t2 = make_table(['维度', '标准要求', '筛选方式'],
                rows, [80, 180, 180], first_col_center=True)
story.append(t2)

story.append(P('供应链来源策略', S['h2']))
story.append(P(escape('第一阶段（0-6个月）：挖掘现有资源池'), S['body']))
story.append(P(escape('从雨哥IP粉丝中的企业主直接转化——通过发布"供应链联盟招募"内容，吸引有意出海的制造企业主动联系'), S['bullet']))
story.append(P(escape('利用雨哥20年外贸积累的工厂人脉资源，定向邀约'), S['bullet']))
story.append(P(escape('第二阶段（6-12个月）：产业带深度合作'), S['body']))
story.append(P(escape('锁定5-6个重点产业带（小家电、家居用品、宠物用品、户外装备、3C配件、美妆工具）'), S['bullet']))
story.append(P(escape('与地方政府/商协会合作，获取产业带推荐名录，进行批量筛选'), S['bullet']))
story.append(P(escape('第三阶段（12个月+）：开放入驻+动态管理'), S['body']))
story.append(P(escape('面向全社会开放供应商入驻申请，定期筛选优质新供应商'), S['bullet']))
story.append(P(escape('实行月度/季度SKU销售排名，末位10%淘汰'), S['bullet']))

story.append(P('联盟的核心价值：为供应商带来的收益', S['h2']))
t3 = make_table(
    ['价值点', '具体内容'],
    [
        ['销售渠道扩展', escape('通过个体矩阵触达海量C端用户，形成"渠道即矩阵"的规模效应')],
        ['市场测试窗口', escape('利用"小单快反"模式，以极小成本测试海外市场反应')],
        ['合规降本', escape('新丝路统一为供应商提供海外认证、商标注册的集采服务，降低单企业成本')],
        ['数据反哺', escape('个体矩阵的销售数据反馈给供应链，指导产品迭代和爆款开发')],
        ['品牌出海', escape('优质供应商可进入新丝路"品牌出海扶持计划"，获得独立品牌曝光')],
    ],
    [100, 340]
)
story.append(t3)

story.append(P('参考案例：SHEIN的"链式赋能"模式', S['h2']))
story.append(P(escape('SHEIN通过"自营+平台"双引擎模式，以"小单快反"的柔性供应链为核心，实现"以销定产"，首单仅以100-200件小批量测试市场，再根据实时销售数据敏捷返单，将行业平均库存率降至个位数。更关键的是，SHEIN不仅自己运用这套模式，还手把手教供应商如何盘点库存、精准下单备货，每月举办自主运营与库存管理培训。通过数字化系统对接全球消费趋势，SHEIN已成为推动产业数智化转型升级的关键引擎。'), S['body']))
story.append(P(escape('新丝路的差异化：SHEIN主要整合服装产业带，新丝路覆盖多品类（小家电、家居、宠物、户外等）；SHEIN主要服务自身平台，新丝路通过"供应链矩阵"模式，让矩阵内个体共同分销，形成"万品出海、万人分销"的生态。'), S['body']))

# ═══════ SECTION 4 ═══════
story.append(PageBreak())
story.append(SectionHeader("四", "个体出海矩阵"))
story.append(Spacer(1, 4))
story.append(P('底层 · 供给侧 · 广度', S['subtitle']))
story.append(Spacer(1, 6))

story.append(P('个体从哪里来？', S['h2']))

t4 = make_table(
    ['来源', '转化路径', '目标规模（第一年）'],
    [
        ['新丝路99元课学员', escape('完成课程→通过矩阵入驻考核→成为矩阵成员'), '1,500-2,000人'],
        ['新丝路线下3天课学员', escape('结课后邀请进入矩阵陪跑群→实战试单→正式加入'), '300-500人'],
        ['社会公开招募', escape('通过短视频、招聘平台、灵活就业平台招募'), '1,000-2,000人'],
    ],
    [110, 210, 120]
)
story.append(t4)
story.append(Spacer(1, 4))
story.append(P(escape('为什么个体愿意来？启动门槛极低：无需营业执照、无需囤货、无需自建物流，全套供应链支持+新丝路培训陪跑+平台背书，个体只需专注内容创作和流量获取，即可实现"一人一台电脑"的跨境创业。'), S['body']))

story.append(P('个体成长路径', S['h2']))

growth = [
    '┌────────────────────────────────────────────────────────────────────┐',
    '│  层级           准入门槛                         权益               │',
    '├────────────────────────────────────────────────────────────────────┤',
    '│  L1：新手个体    完成新丝路入门课+矩阵培训         基础选品库、佣金5%   │',
    '│                  注册跨境收款账户                                      │',
    '│                                                                       │',
    '│                   ↓ 月销突破20单                                      │',
    '│                                                                       │',
    '│  L2：成长个体    连续3个月月销≥20单              佣金提升至8%         │',
    '│                  完成进阶运营课                   专属选品推荐          │',
    '│                                                                       │',
    '│                   ↓ 月销突破100单                                     │',
    '│                                                                       │',
    '│  L3：资深个体    连续3个月月销≥100单             佣金提升至12%        │',
    '│                  通过考核评审                     参加海外考察团        │',
    '│                                                                       │',
    '│                   ↓ 月销突破500单+团队                                │',
    '│                                                                       │',
    '│  L4：矩阵合伙人  团队管理能力+推荐新成员          享受团队流水分成      │',
    '│                  与新丝路深度绑定                优先参与新业务         │',
    '└────────────────────────────────────────────────────────────────────┘',
]
for line in growth:
    story.append(code(line))

story.append(P('个体运营模式', S['h2']))
story.append(P(escape('矩阵内个体采用"一件代发"（Dropshipping）模式为主。其逻辑非常简单：个体负责在前端店铺上架商品、引流接单；客户下单后，个体再拿着订单信息去1688等国内供应商处下单，由供应商直接发货给海外客户。这种模式的核心优势是：无需囤货、无需压资金、启动资金可低至2,000元左右。'), S['body']))

story.append(P(escape('新丝路矩阵 vs 普通1688代发：'), S['body']))
t5 = make_table(
    ['维度', '普通1688代发', '新丝路矩阵代发'],
    [
        ['选品', '自己大海捞针', escape('新丝路精选爆款+主题选品库推送')],
        ['合规', '个体自行摸索', escape('新丝路统一提供合规文件+认证支持')],
        ['物流', '个体自己找货代', escape('集采物流+海外仓备货，成本更低')],
        ['收款', '个体自己开通', escape('指导开户+与新丝路合作银行通道')],
        ['培训', '无', escape('新丝路全链路陪跑（选品→开店→出单→发货→售后）')],
        ['售后', '个体自己处理', escape('供应链统一处理+平台仲裁机制')],
    ],
    [60, 170, 210]
)
story.append(t5)

story.append(P('个体佣金分成机制', S['h2']))
t6 = make_table(
    ['层级', '基础佣金', '达标奖励', '综合佣金'],
    [
        ['L1新手', '5%', '—', '5%'],
        ['L2成长', '8%', '—', '8%'],
        ['L3资深', '12%', '月销达标额外1%', '13%'],
        ['L4合伙人', '12%', '团队流水0.5%', '12.5%+'],
    ],
    [80, 80, 140, 80]
)
story.append(t6)
story.append(Spacer(1, 4))
story.append(P(escape('单笔销售分润示意：一单100美元的订单，供应链获得85美元，矩阵个体获得15美元（约合人民币105元）。如果个体一个月出100单，月收入超过1万元；出500单，月收入超过5万元。'), S['body']))

# ═══════ SECTION 5 ═══════
story.append(PageBreak())
story.append(SectionHeader("五", "平台的枢纽角色"))
story.append(Spacer(1, 6))

story.append(P(escape('新丝路平台在"供应链联盟 + 个体矩阵"之间扮演三层角色：'), S['body']))

# Three roles as visual cards
role_data = [
    [P('连接器', ParagraphStyle('R', fontName=cn_bold, fontSize=12, leading=16,
          textColor=C_PRIMARY, spaceAfter=4)),
     P(escape('精选产品库，按品类/主题/目标市场推送推荐\n匹配制度：系统根据个体画像自动推荐适合的产品\n实现订单流、信息流、资金流三流合一'), S['body'])],
    [P('赋能器', ParagraphStyle('R2', fontName=cn_bold, fontSize=12, leading=16,
          textColor=C_PRIMARY, spaceAfter=4)),
     P(escape('培训赋能（99元课→线下课→矩阵陪跑营，全链路实操）\n工具赋能（AI工具、智能选品、自动化订单处理系统）\n合规赋能（统一认证、合规文档库、客服仲裁机制）'), S['body'])],
    [P('监管者', ParagraphStyle('R3', fontName=cn_bold, fontSize=12, leading=16,
          textColor=C_PRIMARY, spaceAfter=4)),
     P(escape('供应商定期质量审核\n个体行为规范管理\n订单售后争议仲裁机制\n防止恶意刷单、知识产权侵权等风险'), S['body'])],
]
role_table = Table(role_data, colWidths=[70, 370])
role_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), C_ACCENT2),
    ('BOX', (0, 0), (-1, -1), 0.5, C_ACCENT),
    ('INNERGRID', (0, 0), (-1, -1), 0.4, C_TABLE_BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
]))
story.append(role_table)
story.append(Spacer(1, 8))

story.append(P('平台的核心技术系统规划', S['h2']))
t7 = make_table(
    ['系统模块', '功能', '优先级'],
    [
        ['选品中心', '产品上架、分类展示、关键词搜索、数据分析', 'P0（首年）'],
        ['分销系统', '个体分销链接生成、订单跟踪、收益结算', 'P0（首年）'],
        ['培训系统', '课程上传、打卡、考试、矩阵准入', 'P1（首年）'],
        ['分账系统', '自动计算佣金、多级分成、月结功能', 'P0（首年）'],
        ['履约系统', '对接海外仓、物流追踪、一键代发', 'P1（次年）'],
        ['数据分析平台', '热销品趋势分析、个体画像分析、智能推荐', 'P2（次年）'],
    ],
    [80, 220, 80]
)
story.append(t7)

story.append(P('与新丝路现有业务的关系', S['h2']))
story.append(P(escape('从知识付费到供应链矩阵的转化路径：'), S['body']))
story.append(P(escape('新丝路99元课 → 个体兴趣（跨境电商兴趣培养）'), S['bullet']))
story.append(P(escape('新丝路线下3天实战课 → 个体实战（完成为期30天的陪跑试单）'), S['bullet']))
story.append(P(escape('新丝路矩阵准入考核 → 正式加入矩阵（月收入稳定在3000元以上）'), S['bullet']))
story.append(P(escape('个体孵化升级 → 合伙人/导师（带动新个体，享受团队分成）'), S['bullet']))
story.append(P(escape('这种"培训→实战→孵化的自然阶梯"，形成了新丝路矩阵的持续内生增长飞轮。'), S['body']))

# ═══════ SECTION 6 ═══════
story.append(PageBreak())
story.append(SectionHeader("六", "灵活就业数据支撑与社会价值"))
story.append(Spacer(1, 6))

story.append(P('为什么矩阵计划恰逢其时？', S['h2']))

story.append(P('3.2亿灵活就业人群的真实图景', S['h3']))
t8 = make_table(
    ['数据类型', '数据'],
    [
        ['2026年预计灵活就业总人数', '3.2亿人'],
        ['占全国总就业人口比例', '44%以上'],
        ['其中新就业形态劳动者', '约8,400万人'],
        ['年均新增灵活就业者', '约4,000万人'],
        ['制造业灵活用工人员', escape('4,000万人（占制造业从业人员31.12%）')],
    ],
    [180, 260]
)
story.append(t8)
story.append(Spacer(1, 4))
story.append(P(escape('数据来源：中国新就业形态研究中心发布的《2025中国蓝领群体就业研究报告》指出，2025年中国灵活就业从业人员达2.8亿人，预计2026年将增至3.2亿，占城镇就业的比例超过四成。其中约8,400万人依赖平台就业。制造业用工中灵活用工达4,000万人，占制造业从业人员31.12%，已形成"高新技术人员+灵活用工人员"的新型生产模式。'), S['body_small']))
story.append(Spacer(1, 3))
story.append(P(escape('这意味着：中国有3.2亿人正在主动或被动地从事灵活就业，其中8,400万人已经熟悉平台化工作模式。新丝路矩阵计划的核心价值在于：把这3.2亿灵活就业人群中的一部分，从"低附加值劳动力"（外卖、网约车）升级为"高附加值跨境创业者" ——用中国供应链+个体矩阵，为灵活就业者提供更高收入的可能。'), S['body']))

story.append(P('政策支持', S['h2']))
story.append(P(escape('2026年6月，李强主持召开国务院常务会议，审议通过《实施就业优先战略"十五五"规划》。会议明确要求：要健全就业促进机制，完善就业创业服务体系，拓展高校毕业生等青年就业成才渠道，加大重点群体就业支持力度，推动灵活就业、新就业形态健康发展，加强劳动者就业权益保障。'), S['body']))
story.append(P(escape('矩阵计划的推出，与新丝路"一带一路"丝路文化的品牌内涵形成了极具张力的共振：既响应了国家稳就业、促创业的宏观政策，又满足了3.2亿灵活就业人群的高质量就业需求。'), S['body']))

# ═══════ SECTION 7 ═══════
story.append(PageBreak())
story.append(SectionHeader("七", "完整的生态闭环"))
story.append(Spacer(1, 4))

eco = [
    '┌───────────────────────────────────────────────────────────────────────┐',
    '│                       新丝路 · 供应链矩阵生态闭环图                     │',
    '├───────────────────────────────────────────────────────────────────────┤',
    '│                                                                        │',
    '│   ① 供应端                                                              │',
    '│      制造企业 → 加入供应链联盟 → 提供产品                                │',
    '│                                                                        │',
    '│                       ↓                                                │',
    '│                                                                        │',
    '│   ② 平台侧                                                              │',
    '│      新丝路平台：选品中心 + 培训体系 + 订单分发 + 结算系统                │',
    '│                                                                        │',
    '│                       ↓                                                │',
    '│                                                                        │',
    '│   ③ 个体侧                                                              │',
    '│      个体矩阵通过培训成长 → 开店 → 分销产品 → 完成销售                    │',
    '│                                                                        │',
    '│                       ↓                                                │',
    '│                                                                        │',
    '│   ④ 数据回流                                                            │',
    '│      销售数据反哺 → 爆款识别 → 反向指导供应链开发新品                     │',
    '│                                                                        │',
    '│                       ↓                                                │',
    '│                                                                        │',
    '│   ⑤ 闭环升级                                                            │',
    '│      更多爆款产品 → 吸引更多个体 → 生态规模持续扩大 → 飞轮加速              │',
    '│                                                                        │',
    '└───────────────────────────────────────────────────────────────────────┘',
]
for line in eco:
    story.append(code(line))

# ═══════ SECTION 8 ═══════
story.append(PageBreak())
story.append(SectionHeader("八", "盈利模式"))
story.append(Spacer(1, 6))

story.append(P('收入来源矩阵', S['h2']))
t9 = make_table(
    ['收入来源', '模式', '成熟期年收入', '毛利率'],
    [
        ['供应链佣金', escape('每笔销售抽取15%（供应链85%+平台管理费）'), '2,000-3,000万元', '100%'],
        ['个体会员费', escape('月费29元/人，包含无限次选品库访问+基础培训'), '200-300万元', '90%'],
        ['供应链入驻费', escape('供应商年费3,000-10,000元/家'), '50-100万元', '100%'],
        ['配套服务', escape('物流/海外仓/收款/认证等配套增值服务佣金'), '500-1,000万元', '50%'],
        ['培训费', escape('新丝路99元引流课+线下课收入（与知识付费版块合并统计）'), '计入知识付费版块', '50-60%'],
        ['生态衍生收入', escape('供应链金融服务、广告投放、数据服务'), '300-500万元', '80%'],
    ],
    [80, 175, 105, 60]
)
story.append(t9)
story.append(Spacer(1, 4))
story.append(P(escape('成熟期合计（不含知识付费版块）：约3,000-5,000万元'), S['body']))

story.append(P('成本结构', S['h2']))
t10 = make_table(
    ['成本项', '占比', '说明'],
    [
        ['平台开发与维护', '20%', '选品中心、订单系统、分账系统建设'],
        ['运营与BD', '25%', '供应链拓展、个体招募、日常运营'],
        ['培训与内容', '15%', '课程开发、讲师费用、陪跑服务'],
        ['物流补贴', '10%', '个体起步期的物流补贴'],
        ['推广与获客', '20%', '个体招募、供应链品牌推广'],
        ['其他', '10%', '办公、人员、合规咨询等'],
    ],
    [100, 60, 280]
)
story.append(t10)

# ═══════ SECTION 9 ═══════
story.append(PageBreak())
story.append(SectionHeader("九", "参考案例与成功借鉴"))
story.append(Spacer(1, 6))

story.append(P('SHEIN："链式赋能"的供应链整合标杆', S['h2']))
story.append(P(escape('SHEIN通过"小单快反"的柔性供应链模式创新，实现"以销定产"，革新了传统生产逻辑。所有产品首单以100-200件的极小规模测试市场，再根据实时销售数据敏捷返单。其"SHEIN链"串联起品牌与供应商，在链主企业的带动下，产业链从开发、生产、仓储、物流等各环节实现数字化升级。'), S['body']))
story.append(P(escape('借鉴：将SHEIN的"链式赋能"逻辑应用于多品类供应链，打造"新丝路链"。'), S['bullet']))

story.append(P('苏宁易购："拎包出海"的一站式方案', S['h2']))
story.append(P(escape('苏宁易购推出"一站式出海平台"，为中国商家提供"拎包出海"的全链路解决方案。商家可灵活选择"直邮模式""入仓模式"两种仓储服务履约模式，以及"全托管""半托管""供应链补充"三种运营模式，真正实现低门槛、低风险的全球化布局。'), S['body']))
story.append(P(escape('借鉴：为新丝路个体提供类似的"拎包出海"体验——个体无需思考任何供应链问题，只管内容创作和引流。'), S['bullet']))

story.append(P('菜鸟&鲸芽："多渠道一盘货"的库存模式', S['h2']))
story.append(P(escape('菜鸟联合鲸芽推出的"多渠道、一盘货"解决方案，帮助商家实现多平台库存共享与一键发货。'), S['body']))
story.append(P(escape('借鉴：新丝路矩阵可打造"多平台一盘货"——个体可在TikTok Shop、Shopee、独立站等多个渠道同时分销同一产品库。'), S['bullet']))

story.append(P('三节课："内容+服务+平台"的赋能模式', S['h2']))
story.append(P(escape('三节课作为中国领先的数字化人才战略服务商，面向企业和个人用户提供以"内容+服务+平台"为核心的数字化人才战略解决方案。'), S['body']))
story.append(P(escape('借鉴：新丝路矩阵的赋能体系同样遵循"内容+服务+平台"的框架——内容（99元课→线下课→矩阵进阶课程）、服务（陪跑、诊断、售后仲裁）、平台（选品中心、订单分发、佣金结算）。'), S['bullet']))

# ═══════ SECTION 10 ═══════
story.append(PageBreak())
story.append(SectionHeader("十", "实施路线图"))
story.append(Spacer(1, 6))

story.append(P('阶段一：基建与启动期（0-6个月）', S['h2']))
t11 = make_table(
    ['时间节点', '关键任务'],
    [
        ['第1个月', '供应链联盟供应商筛选标准确立、首批10-20家核心供应商洽谈'],
        ['第2-3个月', '平台选品中心MVP开发、个体培训课程体系搭建'],
        ['第3-4个月', '从新丝路99元课和线下课学员中招募首批200名种子个体'],
        ['第4-5个月', '首批个体完成培训并通过考核，启动首批产品上线（200-300个SKU）'],
        ['第5-6个月', '全链路跑通（选品→培训→分销→出单→结算），形成可复制SOP'],
    ],
    [80, 360]
)
story.append(t11)
story.append(Spacer(1, 3))
story.append(P(escape('里程碑：首批200名个体成功出单，月销售额破50万元。'), S['body']))

story.append(P('阶段二：规模化扩展期（6-18个月）', S['h2']))
t12 = make_table(
    ['时间节点', '关键任务'],
    [
        ['第6-9个月', '供应链联盟扩至5-6个产业带，供应商达60-80家'],
        ['第9-12个月', '个体矩阵扩至1,000人，平台SKU达1,000+'],
        ['第12-15个月', '上线完整的分账系统和履约系统，引入物流集采'],
        ['第15-18个月', '启动供应链金融服务，为成长个体提供资金周转支持'],
    ],
    [80, 360]
)
story.append(t12)
story.append(Spacer(1, 3))
story.append(P(escape('里程碑：矩阵月销售额破500万元，个体平均月收入达3,000元。'), S['body']))

story.append(P('阶段三：生态成熟期（18-36个月）', S['h2']))
t13 = make_table(
    ['时间节点', '关键任务'],
    [
        ['第18-24个月', '覆盖30+产业带，供应商达300-500家'],
        ['第24-30个月', '矩阵个体达5,000-10,000人，SKU达3,000+'],
        ['第30-36个月', '拓展至多平台（独立站、Amazon、Temu等），形成多平台分销网络'],
    ],
    [80, 360]
)
story.append(t13)
story.append(Spacer(1, 3))
story.append(P(escape('里程碑：矩阵年销售额破亿元，培养出100+月入过万的个体从业者。'), S['body']))

# ═══════ SECTION 11 ═══════
story.append(PageBreak())
story.append(SectionHeader("十一", "风险与应对"))
story.append(Spacer(1, 6))

t14 = make_table(
    ['风险类别', '具体风险', '应对策略'],
    [
        ['供应端风险', '供应商产品质量不稳定、履约效率低', '严格的供应商准入审核机制；每月匿名抽查批次；设立供应商黑名单制度'],
        ['个体端风险', '个体违规操作（刷单、侵权、套利）', '建立个体行为规范红线；设立违规积分累计扣分制；严重的直接清退并公示'],
        ['平台运营风险', '订单纠纷处理不当，影响平台信誉', '设立标准化售后仲裁流程；为订单购买商业保险；运营团队专人负责'],
        ['竞争风险', '其他平台模仿"供应链+个体"模式', '依托雨哥IP的信任壁垒+供应链独家合作+个体陪跑的深度护城河'],
        ['政策风险', '跨境监管政策变化', '密切跟踪目标国家的跨境电商政策变化；法律服务团队及时协助调整方案'],
    ],
    [80, 165, 195]
)
story.append(t14)

# ═══════ SECTION 12 ═══════
story.append(SectionHeader("十二", "核心亮点总结"))
story.append(Spacer(1, 6))

highlights = [
    ('时代刚需', '3.2亿灵活就业人群 + 国家稳就业政策 + 跨境电商红利 = 巨大的市场窗口'),
    ('模式创新', '"供应链+个体"的双引擎模式，区别于单一的知识付费或单一的服务平台'),
    ('产业链协同', '供应端（国内制造企业）+ 平台端（新丝路）+ 个体端（灵活就业群体）三方共赢——企业获得海外市场渠道，个体获得高收益机会，平台获得持续收入'),
    ('可持续飞轮', '供应链提供优质产品→个体创业创造销量→数据反馈供应链优化→更多爆款产品吸引更多个体加入→飞轮效应持续加速'),
    ('社会价值', '将低技能的外卖/网约车"时间换钱"型灵活就业，升级为通过中国供应链+跨境电商创业的高价值就业模式，切实助力国家稳就业战略'),
    ('IP护城河', '依托雨哥20年外贸实战IP的信任资产，新丝路矩阵的获客成本和转化效率天然优于其他类似平台'),
]

highlight_data = []
for title, desc in highlights:
    highlight_data.append([
        Paragraph(escape(title), ParagraphStyle('HL', fontName=cn_bold, fontSize=10, leading=14,
                  textColor=C_PRIMARY, alignment=TA_CENTER)),
        P(escape(desc), S['body'])
    ])

ht = Table(highlight_data, colWidths=[80, 360])
ht.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), C_ACCENT2),
    ('BOX', (0, 0), (-1, -1), 0.5, C_ACCENT),
    ('INNERGRID', (0, 0), (-1, -1), 0.4, C_TABLE_BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
]))
story.append(ht)

# ═══════ SECTION 13 ═══════
story.append(PageBreak())
story.append(SectionHeader("十三", "矩阵计划与新丝路知识付费业务的融合"))
story.append(Spacer(1, 6))

t15 = make_table(
    ['业务版块', '关系', '协同逻辑'],
    [
        ['知识付费（99元课）', '流量入口', '为矩阵计划筛选意向个体，形成人才储备'],
        ['知识付费（3天线下课）', '实战漏斗', '为矩阵个体提供深度实战培训+30天陪跑'],
        ['供应链矩阵计划', '盈利闭环', '个体通过矩阵获得持续收入，驱动知识付费业务复购和转介绍'],
        ['出海全链路服务平台', '后端延伸', '成长个体/合伙人可升级为企业主，进入更高价值的平台服务层'],
    ],
    [120, 70, 250]
)
story.append(t15)
story.append(Spacer(1, 8))

story.append(P(escape('整体生态闭环：99元课（兴趣）→ 线下3天课（实战）→ 矩阵准入考核（筛选）→ 个体矩阵孵化（出单）→ 平台服务（深度绑定）→ 供应链联盟（供应升级）。每一步都是自然的向上流动，最终形成"知识付费引流、供应链矩阵变现、全链路服务增值"的三轮驱动格局。'), S['body']))

story.append(Spacer(1, 20))
colored_hr(C_ACCENT, 1.5, 12)

story.append(P(escape('新丝路·供应链矩阵计划——让供应链做深度，让个体做广度，让中国制造走得更远。'),
               ParagraphStyle('FinalQuote', fontName=cn_font, fontSize=11, leading=18,
                              alignment=TA_CENTER, textColor=C_SUBTITLE, spaceAfter=10)))

# ═══════ BUILD ═══════
doc.build(story, canvasmaker=NumberedCanvas)
print(f"PDF saved to: {output_path}")
