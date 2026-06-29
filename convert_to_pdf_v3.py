# -*- coding: utf-8 -*-
"""Convert document to PDF — refined compact-but-elegant layout."""

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
    Flowable
)
from reportlab.pdfgen import canvas

# ═══════════════════════════════════════════════════
# Color palette — warm & elegant
# ═══════════════════════════════════════════════════
C_PRIMARY    = HexColor('#1a2b4c')
C_ACCENT     = HexColor('#b8975a')
C_ACCENT_LT  = HexColor('#dac292')
C_ACCENT_BG  = HexColor('#f5efe6')
C_LIGHT_BG   = HexColor('#fcfaf5')
C_WHITE      = white
C_TEXT        = HexColor('#2a2a2a')
C_TEXT_SUB    = HexColor('#6b6b6b')
C_TABLE_HDR  = HexColor('#1a2b4c')
C_TABLE_ALT  = HexColor('#f3efe8')
C_TABLE_BDR  = HexColor('#d6d0c4')
C_SECTION_BAR = HexColor('#c6a56a')

# ═══════════════════════════════════════════════════
# Chinese font
# ═══════════════════════════════════════════════════
system = platform.system()
cn_font = cn_bold = None
if system == 'Windows':
    windir = os.environ.get('WINDIR', 'C:\\Windows')
    for d in [os.path.join(windir, 'Fonts'),
              os.path.join(os.environ.get('LOCALAPPDATA',''), 'Microsoft','Windows','Fonts')]:
        for fname, name, idx in [
            ('msyh.ttc','MicrosoftYaHei',0),
            ('msyhbd.ttc','MicrosoftYaHeiBold',0),
        ]:
            fp = os.path.join(d,fname)
            if os.path.exists(fp):
                try:
                    pdfmetrics.registerFont(TTFont(name,fp,subfontIndex=idx))
                except: continue
                if 'Bold' in name: cn_bold = name
                else: cn_font = name
elif system == 'Darwin':
    for fp,name,idx in [('/System/Library/Fonts/STHeiti Medium.ttc','STHeitiM',0),
                        ('/System/Library/Fonts/STHeiti Light.ttc','STHeitiL',0)]:
        if os.path.exists(fp):
            pdfmetrics.registerFont(TTFont(name,fp,subfontIndex=idx))
            cn_font=cn_font or name; cn_bold=cn_bold or name
if cn_font is None: raise RuntimeError(f'No CJK font on {system}')
if cn_bold is None: cn_bold=cn_font

# ═══════════════════════════════════════════════════
# Styles — tight spacing, clean hierarchy
# ═══════════════════════════════════════════════════
S = {}
S['body']    = ParagraphStyle('body', fontName=cn_font, fontSize=9.5, leading=15,
                               spaceAfter=3, alignment=TA_JUSTIFY, textColor=C_TEXT)
S['body_sm'] = ParagraphStyle('body_sm', fontName=cn_font, fontSize=8, leading=11,
                               spaceAfter=2, textColor=C_TEXT_SUB)
S['bullet']  = ParagraphStyle('bullet', fontName=cn_font, fontSize=9.5, leading=14,
                               leftIndent=16, spaceAfter=2, textColor=C_TEXT)
S['code']    = ParagraphStyle('code', fontName=cn_font, fontSize=7, leading=9.5,
                               leftIndent=6, spaceAfter=1, spaceBefore=1,
                               textColor=HexColor('#3a3a3a'))
S['h1']      = ParagraphStyle('h1', fontName=cn_bold, fontSize=16, leading=21,
                               spaceBefore=6, spaceAfter=5, textColor=C_PRIMARY)
S['h2']      = ParagraphStyle('h2', fontName=cn_bold, fontSize=12.5, leading=17,
                               spaceBefore=4, spaceAfter=3, textColor=C_PRIMARY)
S['h3']      = ParagraphStyle('h3', fontName=cn_bold, fontSize=10.5, leading=15,
                               spaceBefore=3, spaceAfter=2, textColor=HexColor('#2a5a80'))
S['th']      = ParagraphStyle('th', fontName=cn_bold, fontSize=8, leading=11,
                               alignment=TA_CENTER, textColor=C_WHITE)
S['tc']      = ParagraphStyle('tc', fontName=cn_font, fontSize=8, leading=11,
                               alignment=TA_CENTER, textColor=C_TEXT)
S['tl']      = ParagraphStyle('tl', fontName=cn_font, fontSize=8, leading=11, textColor=C_TEXT)
S['sub']     = ParagraphStyle('sub', fontName=cn_font, fontSize=11, leading=16,
                               alignment=TA_CENTER, spaceAfter=2, textColor=HexColor('#8a7a60'))

def P(text,style=S['body']): return Paragraph(text,style)
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def bul(text): return P(f'<bullet>&bull;</bullet> {esc(text)}', S['bullet'])
def code(text): return P(esc(text), S['code'])
def thin_hr():
    return HRFlowable(width='100%', thickness=0.4, color=C_ACCENT_BG,
                       spaceBefore=2, spaceAfter=2)

# ═══════════════════════════════════════════════════
# Table helper
# ═══════════════════════════════════════════════════
def make_table(headers, rows, widths=None):
    all_rows = [[P(h,S['th']) for h in headers]]
    for row in rows:
        all_rows.append([P(c,S['tl']) for c in row])
    W = widths or [440//len(headers)]*len(headers)
    t = Table(all_rows, colWidths=W, repeatRows=1)
    cmds = [('BACKGROUND',(0,0),(-1,0),C_TABLE_HDR),
            ('TEXTCOLOR',(0,0),(-1,0),C_WHITE),
            ('GRID',(0,0),(-1,-1),0.35,C_TABLE_BDR),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('TOPPADDING',(0,0),(-1,-1),3),
            ('BOTTOMPADDING',(0,0),(-1,-1),3),
            ('LEFTPADDING',(0,0),(-1,-1),5),
            ('RIGHTPADDING',(0,0),(-1,-1),5)]
    for i in range(1,len(all_rows)):
        if i%2==0: cmds.append(('BACKGROUND',(0,i),(-1,i),C_TABLE_ALT))
    t.setStyle(TableStyle(cmds))
    return t

# ═══════════════════════════════════════════════════
# Section header flowable — compact gold bar
# ═══════════════════════════════════════════════════
class SecHdr(Flowable):
    def __init__(self, num, title, w=440):
        Flowable.__init__(self)
        self.num=num; self.title=title; self.avail=w
    def draw(self):
        c=self.canv; c.saveState()
        y=2
        # gold bar
        c.setFillColor(C_ACCENT); c.roundRect(0,y,3,18,1,fill=1,stroke=0)
        # number circle
        cx=3+10; r=8
        c.setFillColor(C_PRIMARY); c.circle(cx+r,y+9,r,fill=1,stroke=0)
        c.setFillColor(C_WHITE); c.setFont(cn_bold,9)
        c.drawCentredString(cx+r,y+9-4,self.num)
        # title
        tx=cx+r*2+6
        c.setFillColor(C_PRIMARY); c.setFont(cn_bold,14)
        c.drawString(tx,y+9-5.5,self.title)
        # underline
        uy=y-2
        c.setStrokeColor(C_ACCENT_LT); c.setLineWidth(1)
        c.line(0,uy,self.avail,uy)
        self.width=self.avail; self.height=22; c.restoreState()

# ═══════════════════════════════════════════════════
# Cover page
# ═══════════════════════════════════════════════════
class Cover(Flowable):
    def __init__(self,w,h):
        Flowable.__init__(self); self.w=w; self.h=h
    def draw(self):
        c=self.canv; c.saveState(); w=self.w; h=self.h
        # bg
        c.setFillColor(C_LIGHT_BG); c.rect(0,0,w,h,fill=1,stroke=0)
        # top band
        c.setFillColor(C_PRIMARY); c.rect(0,h-100,w,100,fill=1,stroke=0)
        c.setStrokeColor(C_ACCENT); c.setLineWidth(2); c.line(0,h-100,w,h-100)
        c.setStrokeColor(C_ACCENT_LT); c.setLineWidth(0.6); c.line(0,h-103,w,h-103)
        # dots
        for i in range(5):
            c.setFillColor(Color(1,1,1,0.12+i*0.04))
            c.circle(55+i*85,h-50,20-i*2,fill=1,stroke=0)
        # title
        c.setFillColor(C_WHITE); c.setFont(cn_bold,24); c.drawCentredString(w/2,h-58,"新丝路·供应链矩阵计划")
        # subtitle
        c.setFillColor(HexColor('#9a8a6a')); c.setFont(cn_font,11.5)
        c.drawCentredString(w/2,h-125,"以供应链为根基 · 以个体为触角 · 以陪跑为纽带的出海新生态")
        c.setStrokeColor(C_ACCENT); c.setLineWidth(1.2)
        c.line(w/2-50,h-140,w/2+50,h-140)
        # 3 points
        pts=["供应端 · 深度    整合优质制造企业，打造出海供应链联盟",
             "个体端 · 广度    赋能3.2亿灵活就业人群，人人出海",
             "平台端 · 枢纽    连接器+赋能器，全链路服务生态"]
        sy=h-170
        for i,pt in enumerate(pts):
            c.setFillColor(C_TEXT); c.setFont(cn_font,9.8)
            c.drawString(60,sy-i*24,pt)
            c.setFillColor(C_ACCENT); c.circle(50,sy-i*24+3,2.5,fill=1,stroke=0)
        # bottom bar
        c.setFillColor(C_PRIMARY); c.rect(0,0,w,40,fill=1,stroke=0)
        c.setFillColor(C_ACCENT); c.setFont(cn_font,8.5)
        c.drawCentredString(w/2,14,"新丝路 · 让供应链做深度，让个体做广度，让中国制造走得更远")
        # side line
        c.setStrokeColor(C_ACCENT); c.setLineWidth(1.5); c.line(25,55,25,h-115)
        self.width=w; self.height=h; c.restoreState()

# ═══════════════════════════════════════════════════
# Page numbering
# ═══════════════════════════════════════════════════
class NC(canvas.Canvas):
    def __init__(self,*a,**kw):
        canvas.Canvas.__init__(self,*a,**kw); self._saved=[]
    def showPage(self):
        self._saved.append(dict(self.__dict__))
        canvas.Canvas.showPage(self)
    def save(self):
        N=len(self._saved)
        for i,st in enumerate(self._saved):
            self.__dict__.update(st); self._footer(i+1,N); canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
    def _footer(self,p,n):
        w,h=A4
        self.setStrokeColor(C_ACCENT_LT); self.setLineWidth(0.4)
        self.line(22*mm,13*mm,w-22*mm,13*mm)
        self.setFillColor(C_TEXT_SUB); self.setFont(cn_font,7)
        self.drawCentredString(w/2,8*mm,f"— {p}/{n} —")

# ═══════════════════════════════════════════════════
# CONTENT
# ═══════════════════════════════════════════════════
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),'新丝路·供应链矩阵计划.pdf')
doc = SimpleDocTemplate(out, pagesize=A4,
    topMargin=18*mm, bottomMargin=18*mm, leftMargin=20*mm, rightMargin=20*mm,
    title='新丝路·供应链矩阵计划')
W=456
story=[]

# ─── Cover ───
story.append(Spacer(1,3))
story.append(Cover(W,745))
story.append(PageBreak())

# ═══ 一 ═══
story.append(SecHdr("一","核心定位与时代背景"))
story.append(P(esc('计划名称：新丝路·供应链矩阵计划（以下简称"矩阵计划"）'),S['h2']))
story.append(P(esc('核心逻辑：供应链是出海的"炮弹"，个体是出海的"炮兵"。传统的出海模式是"工厂自己当炮兵"——既要做产品又要跑运营，两头不靠岸。矩阵计划颠覆这一逻辑：<b>供应链做深度，个体做广度。</b>'),S['body']))
story.append(bul('供应端（深度）：新丝路整合国内优质制造企业，形成"出海供应链联盟"，提供产品库、代发履约、合规认证、海外仓储等基础设施'))
story.append(bul('个体端（广度）：赋能中国3.2亿灵活就业人群中的一部分，让他们以"一件代发""短视频带货""TikTok直播"等形式成为供应链的触角，实现"人人出海、万品出海"'))
story.append(bul('新丝路平台（枢纽）：作为中间的"连接器+赋能器"，提供培训赋能、选品中心、代发系统、合规保障、收益分账等全链路服务'))

story.append(P('时代背景：三大结构性红利',S['h2']))
story.append(P('红利一：灵活就业已成为中国劳动力市场的"新常态"',S['h3']))
t1=make_table(['时间节点','灵活就业人数','占就业人口比例','年均增长'],
    [['2021年','约2.0亿','约28%','—'],
     ['2024年底','2.4亿','超33%','约1,300万/年'],
     ['2025年','2.8亿','约39%','约4,000万/年'],
     ['2026年（预计）','3.2亿','约44%','约4,000万/年']],
    [88,88,98,98])
story.append(t1)
story.append(P(esc('数据来源：中国新就业形态研究中心、暨南大学经济与社会研究院与智联招聘联合发布的《2026年中国灵活就业市场发展报告》。2025年灵活就业人员规模已达2.8亿，预计2026年将增至3.2亿，占全国7.25亿总就业人口的44%以上，其中依托互联网平台的新型灵活就业群体约8,400万人。'),S['body_sm']))
story.append(P(esc('这意味着：超过3亿人正在或即将寻找灵活的收入来源——他们中绝大多数拥有时间、设备和基本的数字素养，但缺乏创业的方向、技能和供应链支持。'),S['body']))

story.append(P('红利二：跨境电商成为政策驱动的"新引擎"',S['h3']))
story.append(bul('国家层面持续推动跨境电商高质量发展，TikTok Shop等平台入驻门槛逐年优化，2026年东南亚市场支持个体工商户和部分个人身份入驻'))
story.append(bul('"一带一路"倡议深入推进，海关通关便利化、海外仓建设等基础设施不断完善'))
story.append(bul('新丝路品牌名自带"政策亲近度"，更容易获得政府、商会、产业园区的资源倾斜'))
story.append(P('红利三：供应链整合已出现"可复制的成功经验"',S['h3']))
story.append(bul('SHEIN模式：通过"小单快反"柔性供应链，首单仅以100-200件小批量测试市场，根据实时销售数据敏捷返单'))
story.append(bul('1688一件代发模式：2026年完善的电商生态为个人卖家提供了无需囤货的"零风险"起步路径，启动资金可低至2,000元左右'))
story.append(bul('"自主品牌+平台"双引擎模式：SHEIN已形成"自主品牌+平台"双引擎，通过数字化柔性供应链支撑小单快反模式'))

# ═══ 二 ═══
story.append(PageBreak())
story.append(SecHdr("二","商业模型总览"))
story.append(P('供应链矩阵模型',S['h2']))
art1=[
'┌─────────────────────────────────────────────────────────────────┐',
'│             新丝路 · 供应链矩阵计划总体架构                      │',
'├─────────────────────────────────────────────────────────────────┤',
'│ ◆ 顶层 · 供应链联盟（供给侧 · 深度）                            │',
'│   ├─ 制造企业入驻（5-6个产业带，100+优质供应商）                │',
'│   ├─ 产品库搭建（选品中心、数字化产品目录）                      │',
'│   ├─ 合规基础设施（海外认证、商标、合规文档标准化）              │',
'│   └─ 履约系统（一件代发+海外仓+物流网络）                       │',
'│                    ↓ 产品供给 + 履约支持                         │',
'│ ◆ 中层 · 新丝路平台（连接器 · 赋能器）                          │',
'│   ├─ 选品分发 · 陪跑赋能 · 分账系统 · 合规监管 · 数据驱动       │',
'│                    ↓ 赋能个体 + 分发产品                         │',
'│ ◆ 底层 · 个体出海矩阵（供给侧 · 广度）                          │',
'│   └─ 99元课学员→线下课学员→社会招募                              │',
'│     一件代发 · 短视频带货 · 直播引流                             │',
'│ ● 核心飞轮：供应端深度支撑 × 个体端广度扩展 = 生态规模化增长     │',
'└─────────────────────────────────────────────────────────────────┘']
for l in art1: story.append(code(l))

# ═══ 三 ═══
story.append(PageBreak())
story.append(SecHdr("三","供应链联盟"))
story.append(P('顶层 · 供给侧 · 深度',S['sub']))
story.append(P('联盟定位与目标',S['h2']))
story.append(P(esc('定位：成为中国制造企业出海的"产品中台"——企业只需专注生产和品质，出海获客和销售由新丝路及其个体矩阵网络完成。目标：第一年整合5-6个国内产业带，筛选100+优质制造商作为联盟初始核心供应商；第三年扩展至30+产业带，500+供应商。'),S['body']))
story.append(P('供应商筛选标准',S['h2']))
t2=make_table(['维度','标准要求','筛选方式'],
    [['产品品质',esc('具有出口资质，如有ISO/CE等相关认证优先'),esc('工厂实地考察+第三方验厂报告')],
     ['生产柔性',esc('支持"小单快反"，最少起订量≤500件'),esc('现场考察生产流程+历史订单数据')],
     ['合作意愿',esc('愿意接受代发模式、接受15%佣金分成'),'面谈+协议确认'],
     ['合规能力',esc('能配合完成海外认证、产品标签等合规文件'),esc('文件审核+法律团队支持')],
     ['供应链透明度',esc('接受新丝路定期抽查和品质监控'),'年度复检+飞行抽查']],
    [75,190,191])
story.append(t2)
story.append(P('供应链来源策略',S['h2']))
story.append(P(esc('第一阶段（0-6个月）：从雨哥IP粉丝中的企业主直接转化，利用20年外贸积累的工厂人脉资源，定向邀约。'),S['body']))
story.append(P(esc('第二阶段（6-12个月）：锁定5-6个重点产业带（小家电、家居用品、宠物用品、户外装备、3C配件、美妆工具），与地方政府/商协会合作获取推荐名录。'),S['body']))
story.append(P(esc('第三阶段（12个月+）：开放供应商入驻申请，实行月度/季度SKU销售排名，末位10%淘汰。'),S['body']))
story.append(P('联盟的核心价值',S['h2']))
t3=make_table(['价值点','具体内容'],
    [['销售渠道扩展',esc('通过个体矩阵触达海量C端用户，形成"渠道即矩阵"的规模效应')],
     ['市场测试窗口',esc('利用"小单快反"模式，以极小成本测试海外市场反应')],
     ['合规降本',esc('新丝路统一提供海外认证、商标注册集采服务，降低单企业成本')],
     ['数据反哺',esc('个体矩阵销售数据反馈供应链，指导产品迭代和爆款开发')],
     ['品牌出海',esc('优质供应商可进入"品牌出海扶持计划"，获得独立品牌曝光')]],
    [100,356])
story.append(t3)
story.append(P('参考案例：SHEIN的"链式赋能"模式',S['h2']))
story.append(P(esc('SHEIN通过"自营+平台"双引擎，以"小单快反"柔性供应链实现"以销定产"，首单100-200件测试市场，再根据实时销售数据敏捷返单。新丝路差异化：SHEIN整合服装产业带，新丝路覆盖多品类（小家电、家居、宠物、户外等），通过矩阵模式让个体共同分销，形成"万品出海、万人分销"的生态。'),S['body']))

# ═══ 四 ═══
story.append(PageBreak())
story.append(SecHdr("四","个体出海矩阵"))
story.append(P('底层 · 供给侧 · 广度',S['sub']))
story.append(P('个体从哪里来？',S['h2']))
t4=make_table(['来源','转化路径','目标规模（第一年）'],
    [['新丝路99元课学员',esc('完成课程→通过矩阵入驻考核→成为矩阵成员'),'1,500-2,000人'],
     ['新丝路线下3天课学员',esc('结课后邀请进入矩阵陪跑群→实战试单→正式加入'),'300-500人'],
     ['社会公开招募',esc('通过短视频、招聘平台、灵活就业平台招募'),'1,000-2,000人']],
    [115,210,131])
story.append(t4)
story.append(P(esc('启动门槛极低：无需营业执照、无需囤货、无需自建物流，全套供应链支持+新丝路培训陪跑+平台背书，个体只需专注内容创作和流量获取，即可实现"一人一台电脑"的跨境创业。'),S['body']))
story.append(P('个体成长路径',S['h2']))
growth=[
'┌──────────────────────────────────────────────────────────────┐',
'│ L1：新手个体 → 完成入门课+矩阵培训 → 基础选品库、佣金5%      │',
'│        ↓ 月销突破20单                                        │',
'│ L2：成长个体 → 连续3个月月销≥20单 → 佣金提升至8%             │',
'│        ↓ 月销突破100单                                       │',
'│ L3：资深个体 → 连续3个月月销≥100单 → 佣金12%+海外考察团      │',
'│        ↓ 月销突破500单+团队                                  │',
'│ L4：矩阵合伙人 → 团队管理+推荐新成员 → 团队流水分成          │',
'└──────────────────────────────────────────────────────────────┘']
for l in growth: story.append(code(l))
story.append(P('个体运营模式',S['h2']))
story.append(P(esc('矩阵内个体采用"一件代发"（Dropshipping）模式。个体负责在前端店铺上架商品、引流接单；客户下单后个体拿着订单信息去供应商处下单，由供应商直接发货给海外客户。核心优势：无需囤货、无需压资金，启动资金可低至2,000元左右。'),S['body']))
t5=make_table(['维度','普通1688代发','新丝路矩阵代发'],
    [['选品','自己大海捞针',esc('新丝路精选爆款+主题选品库推送')],
     ['合规','个体自行摸索',esc('新丝路统一提供合规文件+认证支持')],
     ['物流','个体自己找货代',esc('集采物流+海外仓备货，成本更低')],
     ['收款','个体自己开通',esc('指导开户+合作银行通道')],
     ['培训','无',esc('全链路陪跑，选品→开店→出单→发货→售后')],
     ['售后','个体自己处理',esc('供应链统一处理+平台仲裁机制')]],
    [60,180,216])
story.append(t5)
story.append(P('个体佣金分成机制',S['h2']))
t6=make_table(['层级','基础佣金','达标奖励','综合佣金'],
    [['L1新手','5%','—','5%'],
     ['L2成长','8%','—','8%'],
     ['L3资深','12%','月销达标额外1%','13%'],
     ['L4合伙人','12%','团队流水0.5%','12.5%+']],
    [80,80,160,80])
story.append(t6)
story.append(P(esc('单笔销售分润示意：一单100美元的订单，供应链85美元，矩阵个体15美元（约合人民币105元）。个体月出100单则月收入超1万元；出500单超5万元。'),S['body']))

# ═══ 五 ═══
story.append(PageBreak())
story.append(SecHdr("五","平台的枢纽角色"))
story.append(P(esc('新丝路平台在"供应链联盟 + 个体矩阵"之间扮演三层角色：'),S['body']))
rc=[
    [P('连接器',ParagraphStyle('r',fontName=cn_bold,fontSize=11,leading=14,textColor=C_PRIMARY)),
     P(esc('精选产品库按品类/主题/目标市场推送推荐；系统根据个体画像自动推荐适合产品；实现订单流、信息流、资金流三流合一'),S['body'])],
    [P('赋能器',ParagraphStyle('r2',fontName=cn_bold,fontSize=11,leading=14,textColor=C_PRIMARY)),
     P(esc('培训赋能（99元课→线下课→矩阵陪跑营）；工具赋能（AI智能选品、自动化订单处理）；合规赋能（统一认证、文档库、仲裁机制）'),S['body'])],
    [P('监管者',ParagraphStyle('r3',fontName=cn_bold,fontSize=11,leading=14,textColor=C_PRIMARY)),
     P(esc('供应商定期质量审核；个体行为规范管理；订单售后争议仲裁；防止恶意刷单、知识产权侵权等风险'),S['body'])]]
rt=Table(rc,colWidths=[65,391])
rt.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),C_ACCENT_BG),
    ('BOX',(0,0),(-1,-1),0.4,C_ACCENT_LT),
    ('INNERGRID',(0,0),(-1,-1),0.3,C_TABLE_BDR),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6)]))
story.append(rt)
story.append(P('平台核心技术系统',S['h2']))
t7=make_table(['系统模块','功能','优先级'],
    [['选品中心','产品上架、分类展示、数据分析','P0'],
     ['分销系统','分销链接生成、订单跟踪、收益结算','P0'],
     ['培训系统','课程上传、打卡、考试、矩阵准入','P1'],
     ['分账系统','自动计算佣金、多级分成、月结功能','P0'],
     ['履约系统','对接海外仓、物流追踪、一键代发','P1'],
     ['数据分析','热销品趋势分析、个体画像、智能推荐','P2']],
    [80,250,60])
story.append(t7)
story.append(P('与新丝路现有业务的关系',S['h2']))
story.append(P(esc('99元课（兴趣）→线下3天课（实战）→矩阵准入考核（筛选）→个体矩阵孵化（出单）→平台服务（深度绑定）→供应链联盟（供应升级）。每一步都是自然的向上流动，形成"知识付费引流、供应链矩阵变现、全链路服务增值"的三轮驱动格局。'),S['body']))

# ═══ 六 ═══
story.append(PageBreak())
story.append(SecHdr("六","灵活就业数据支撑与社会价值"))
story.append(P('为什么矩阵计划恰逢其时？',S['h2']))
story.append(P('3.2亿灵活就业人群的真实图景',S['h3']))
t8=make_table(['数据类型','数据'],
    [['2026年预计灵活就业总人数','3.2亿人'],
     ['占全国总就业人口比例','44%以上'],
     ['其中新就业形态劳动者','约8,400万人'],
     ['年均新增灵活就业者','约4,000万人'],
     ['制造业灵活用工人员',esc('4,000万人，占制造业从业人员31.12%')]],
    [200,256])
story.append(t8)
story.append(P(esc('数据来源：中国新就业形态研究中心《2025中国蓝领群体就业研究报告》。2025年中国灵活就业从业人员达2.8亿人，预计2026年将增至3.2亿，其中约8,400万人依赖平台就业。'),S['body_sm']))
story.append(P(esc('核心价值：把3.2亿灵活就业人群中的一部分，从"低附加值劳动力"（外卖、网约车）升级为"高附加值跨境创业者"——用中国供应链+个体矩阵，为灵活就业者提供更高收入的可能。'),S['body']))
story.append(P('政策支持',S['h2']))
story.append(P(esc('2026年6月，国务院常务会议审议通过《实施就业优先战略"十五五"规划》，明确推动灵活就业、新就业形态健康发展，加强劳动者就业权益保障。矩阵计划既响应了国家稳就业、促创业的宏观政策，又满足了3.2亿灵活就业人群的高质量就业需求。'),S['body']))

# ═══ 七 ═══
story.append(PageBreak())
story.append(SecHdr("七","完整的生态闭环"))
eco=[
'┌─────────────────────────────────────────────────────────────────┐',
'│             新丝路 · 供应链矩阵生态闭环                          │',
'├─────────────────────────────────────────────────────────────────┤',
'│ ① 供应端：制造企业 → 加入供应链联盟 → 提供产品                  │',
'│                              ↓                                  │',
'│ ② 平台侧：选品中心 + 培训体系 + 订单分发 + 结算系统             │',
'│                              ↓                                  │',
'│ ③ 个体侧：个体矩阵通过培训成长 → 开店 → 分销产品 → 完成销售     │',
'│                              ↓                                  │',
'│ ④ 数据回流：销售数据反哺 → 爆款识别 → 反向指导供应链开发新品     │',
'│                              ↓                                  │',
'│ ⑤ 闭环升级：更多爆款产品 → 吸引更多个体 → 生态规模持续扩大      │',
'└─────────────────────────────────────────────────────────────────┘']
for l in eco: story.append(code(l))

# ═══ 八 ═══
story.append(PageBreak())
story.append(SecHdr("八","盈利模式"))
story.append(P('收入来源矩阵',S['h2']))
t9=make_table(['收入来源','模式','成熟期年收入','毛利率'],
    [['供应链佣金',esc('每笔销售抽取15%'),'2,000-3,000万元','100%'],
     ['个体会员费','月费29元/人','200-300万元','90%'],
     ['供应链入驻费','年费3,000-10,000元/家','50-100万元','100%'],
     ['配套服务',esc('物流/海外仓/收款/认证等佣金'),'500-1,000万元','50%'],
     ['培训费',esc('99元引流课+线下课，计入知识付费版块'),'计入知识付费','50-60%'],
     ['生态衍生收入',esc('供应链金融、广告投放、数据服务'),'300-500万元','80%']],
    [80,180,100,70])
story.append(t9)
story.append(P(esc('成熟期合计（不含知识付费版块）：约3,000-5,000万元'),S['body']))
story.append(P('成本结构',S['h2']))
t10=make_table(['成本项','占比','说明'],
    [['平台开发与维护','20%','选品中心、订单系统、分账系统建设'],
     ['运营与BD','25%','供应链拓展、个体招募、日常运营'],
     ['培训与内容','15%','课程开发、讲师费用、陪跑服务'],
     ['物流补贴','10%','个体起步期物流补贴'],
     ['推广与获客','20%','个体招募、供应链品牌推广'],
     ['其他','10%','办公、人员、合规咨询等']],
    [95,60,301])
story.append(t10)

# ═══ 九 ═══
story.append(PageBreak())
story.append(SecHdr("九","参考案例与成功借鉴"))
story.append(P('SHEIN："链式赋能"的供应链整合标杆',S['h2']))
story.append(P(esc('SHEIN通过"小单快反"柔性供应链实现"以销定产"，所有产品首单以100-200件测试市场，根据实时销售数据敏捷返单。"SHEIN链"串联起品牌与供应商，从开发、生产、仓储、物流各环节实现数字化升级。借鉴：将"链式赋能"逻辑应用于多品类供应链，打造"新丝路链"。'),S['body']))
story.append(P('苏宁易购："拎包出海"的一站式方案',S['h2']))
story.append(P(esc('苏宁易购"一站式出海平台"提供直邮模式、入仓模式两种仓储服务，以及全托管、半托管、供应链补充三种运营模式。借鉴：为新丝路个体提供类似的"拎包出海"体验——个体只管内容创作和引流，供应链问题全部交给平台。'),S['body']))
story.append(P('菜鸟&鲸芽："多渠道一盘货"的库存模式',S['h2']))
story.append(P(esc('菜鸟联合鲸芽推出"多渠道、一盘货"解决方案，实现多平台库存共享与一键发货。借鉴：新丝路矩阵可打造"多平台一盘货"——个体可在TikTok Shop、Shopee、独立站等多个渠道同时分销同一产品库。'),S['body']))
story.append(P('三节课："内容+服务+平台"的赋能模式',S['h2']))
story.append(P(esc('三节课以"内容+服务+平台"为核心提供数字化人才战略解决方案。借鉴：新丝路矩阵的赋能体系同样遵循这一框架——内容（课程体系）、服务（陪跑、诊断、仲裁）、平台（选品中心、订单分发、佣金结算）。'),S['body']))

# ═══ 十 ═══
story.append(PageBreak())
story.append(SecHdr("十","实施路线图"))
story.append(P('阶段一：基建与启动期（0-6个月）',S['h2']))
t11=make_table(['时间','关键任务'],
    [['第1个月','供应链联盟供应商筛选标准确立、首批10-20家核心供应商洽谈'],
     ['第2-3个月','平台选品中心MVP开发、个体培训课程体系搭建'],
     ['第3-4个月','从99元课和线下课学员中招募首批200名种子个体'],
     ['第4-5个月','首批个体完成培训考核，启动首批产品上线（200-300个SKU）'],
     ['第5-6个月','全链路跑通（选品→培训→分销→出单→结算），形成可复制SOP']],
    [75,381])
story.append(t11)
story.append(P(esc('里程碑：首批200名个体成功出单，月销售额破50万元。'),S['body']))
story.append(P('阶段二：规模化扩展期（6-18个月）',S['h2']))
t12=make_table(['时间','关键任务'],
    [['第6-9个月','供应链联盟扩至5-6个产业带，供应商达60-80家'],
     ['第9-12个月','个体矩阵扩至1,000人，平台SKU达1,000+'],
     ['第12-15个月','上线完整分账系统和履约系统，引入物流集采'],
     ['第15-18个月','启动供应链金融服务，为成长个体提供资金周转支持']],
    [75,381])
story.append(t12)
story.append(P(esc('里程碑：矩阵月销售额破500万元，个体平均月收入达3,000元。'),S['body']))
story.append(P('阶段三：生态成熟期（18-36个月）',S['h2']))
t13=make_table(['时间','关键任务'],
    [['第18-24个月','覆盖30+产业带，供应商达300-500家'],
     ['第24-30个月','矩阵个体达5,000-10,000人，SKU达3,000+'],
     ['第30-36个月',esc('拓展至多平台（独立站、Amazon、Temu等），形成多平台分销网络')]],
    [75,381])
story.append(t13)
story.append(P(esc('里程碑：矩阵年销售额破亿元，培养出100+月入过万的个体从业者。'),S['body']))

# ═══ 十一 ═══
story.append(PageBreak())
story.append(SecHdr("十一","风险与应对"))
t14=make_table(['风险类别','具体风险','应对策略'],
    [['供应端风险','供应商产品质量不稳定、履约效率低',esc('严格准入审核；每月匿名抽查；设立黑名单制度')],
     ['个体端风险','个体违规操作（刷单、侵权、套利）',esc('行为规范红线；违规积分累计扣分制；严重者清退公示')],
     ['平台运营风险','订单纠纷处理不当影响信誉',esc('标准化售后仲裁流程；商业保险；运营团队专人负责')],
     ['竞争风险','其他平台模仿模式',esc('雨哥IP信任壁垒+供应链独家合作+个体陪跑的深度护城河')],
     ['政策风险','跨境监管政策变化',esc('密切跟踪目标国政策变化；法律服务团队及时调整方案')]],
    [72,175,209])
story.append(t14)

# ═══ 十二 ═══
story.append(Spacer(1,2))
story.append(SecHdr("十二","核心亮点总结"))
hls=[
    ('时代刚需','3.2亿灵活就业人群 + 国家稳就业政策 + 跨境电商红利 = 巨大市场窗口'),
    ('模式创新','"供应链+个体"双引擎模式，区别于单一的知识付费或服务平台'),
    ('产业链协同',esc('供应端+平台端+个体端三方共赢——企业获渠道，个体获收益，平台获收入')),
    ('可持续飞轮','优质产品→个体创造销量→数据反馈优化→更多爆款吸引更多个体→飞轮加速'),
    ('社会价值',esc('将低技能"时间换钱"型灵活就业升级为高价值跨境电商创业，助力国家稳就业战略')),
    ('IP护城河',esc('依托雨哥20年外贸实战IP的信任资产，获客成本和转化效率天然优于同类平台'))]
hd=[]
for t,d in hls:
    hd.append([Paragraph(esc(t),ParagraphStyle('h',fontName=cn_bold,fontSize=9.5,leading=13,
                textColor=C_PRIMARY,alignment=TA_CENTER)),
               P(esc(d),S['body'])])
ht=Table(hd,colWidths=[75,381])
ht.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),C_ACCENT_BG),
    ('BOX',(0,0),(-1,-1),0.4,C_ACCENT_LT),
    ('INNERGRID',(0,0),(-1,-1),0.3,C_TABLE_BDR),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6)]))
story.append(ht)

# ═══ 十三 ═══
story.append(Spacer(1,2))
story.append(SecHdr("十三","与新丝路知识付费业务的融合"))
t15=make_table(['业务版块','关系','协同逻辑'],
    [['知识付费（99元课）','流量入口','为矩阵计划筛选意向个体，形成人才储备'],
     ['知识付费（3天线下课）','实战漏斗','为矩阵个体提供深度实战培训+30天陪跑'],
     ['供应链矩阵计划','盈利闭环','个体通过矩阵获得持续收入，驱动知识付费复购和转介绍'],
     ['出海全链路服务平台','后端延伸','成长个体/合伙人可升级为企业主，进入更高价值的平台服务层']],
    [125,70,261])
story.append(t15)

# ─── Final quote ───
story.append(Spacer(1,8))
thin_hr()
story.append(Spacer(1,4))
story.append(P(esc('新丝路·供应链矩阵计划——让供应链做深度，让个体做广度，让中国制造走得更远。'),
    ParagraphStyle('fq',fontName=cn_font,fontSize=10,leading=16,
                   alignment=TA_CENTER,textColor=HexColor('#8a7a60'))))

# ═══ BUILD ═══
doc.build(story,canvasmaker=NC)
print(f"PDF saved: {out}")
