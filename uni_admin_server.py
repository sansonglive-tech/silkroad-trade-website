#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
丝路山海通 · 统一后台 v3 (服务端渲染)
端口 8083 | 显示现有内容可直接修改 | 不动原文件
"""

import os, json, secrets, traceback, subprocess, re
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from datetime import datetime

WORKSPACE = os.path.expanduser("~/.qclaw/workspace")
V7_FILE = os.path.join(WORKSPACE, "silkroad-trade_v7_silk_poster.html")
CONFIG_FILE = os.path.join(WORKSPACE, "site_config.json")
BOOKING_DATA = os.path.join(WORKSPACE, "booking_data.json")
ADMIN_USER = "jackleework"
ADMIN_PASS = "jackleework"
SESSIONS = {}
PORT = 8083

def load_cfg():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"company":{}, "slides":[], "services":[], "policies":[], "countries":[], "process":[], "stats":[], "testimonials":[]}

def save_cfg(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def read_v7():
    if os.path.isfile(V7_FILE):
        with open(V7_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return None

def load_bookings():
    if os.path.isfile(BOOKING_DATA):
        with open(BOOKING_DATA, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_bookings(data):
    with open(BOOKING_DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def esc(s):
    if s is None: return ""
    s = str(s)
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;").replace("'","&#39;")

def fv(val):
    return val if val else ""


def generate_admin_page(cfg):
    """服务端生成完整 admin HTML — 不用 f-string，防 Python 转义问题"""
    
    C = cfg.get("company", {})
    bg = C.get("backgrounds", {})
    sl = cfg.get("slides", [])
    sv = cfg.get("services", [])
    po = cfg.get("policies", [])
    ct = cfg.get("countries", [])
    pr = cfg.get("process", [])
    st = cfg.get("stats", [])
    te = cfg.get("testimonials", [])
    cta = cfg.get("cta", {})
    dc = cfg.get("detailContent", {})  # 提前定义，供政策分析等板块使用

    def img_block(label, key, url, w, h, hint=""):
        sz = ' <span class="sz">推荐 %d\u00d7%d</span>' % (w, h) if w and h else ""
        prev = '<img class="pv" src="%s" onerror="this.style.display=\'none\'">' % esc(url) if url else '<span class="np">暂无图片</span>'
        hh = '<div class="ht">%s</div>' % hint if hint else ""
        return '<div class="fg"><label>%s%s</label><input name="%s" value="%s" placeholder="粘贴图床链接">%s%s</div>' % (
            label, sz, esc(key), esc(url), prev, hh)

    def txt(label, key, val, ph=""):
        return '<div class="fg"><label>%s</label><input name="%s" value="%s" placeholder="%s"></div>' % (
            label, esc(key), esc(fv(val)), esc(ph))

    def ta(label, key, val, rows=2):
        return '<div class="fg"><label>%s</label><textarea name="%s" rows="%d">%s</textarea></div>' % (
            label, esc(key), rows, esc(fv(val)))

    # === 构建各板块 HTML ===
    sections = {}
    
    # 01 导航栏
    sections["nav"] = '''<div class="cd"><div class="ch"><h3>01 · 导航栏</h3></div>
<div class="ht">Logo 为 SVG 固化，公司名称/标语可修改</div>
<div class="ug2">%s%s</div></div>''' % (
        txt("公司名称", "company.name", C.get("name")),
        txt("标语(英文)", "company.slogan", C.get("slogan")))

    # 02 轮播幻灯片
    sl_html = '''<div class="cd"><div class="ch"><h3>02 · 轮播幻灯片 <span class="bd">%d张</span></h3><button class="ab" onclick="addSl()">+ 添加</button></div>''' % len(sl)
    if not sl:
        sl_html += '<p class="em">暂无轮播图，点击添加</p>'
    for i, s in enumerate(sl):
        sl_html += '''<div class="ib"><div class="ih"><strong>幻灯片 #%d: %s</strong><button class="ab" onclick="delSl(%d)">删除</button></div>
%s<div class="ug3">%s%s%s</div>%s</div>''' % (
            i+1, esc(s.get("title","")), i,
            img_block("主图", "slides[%d].img"%i, s.get("img"), 1920, 850, "宽图效果最佳"),
            txt("标题", "slides[%d].title"%i, s.get("title")),
            txt("副标题", "slides[%d].subtitle"%i, s.get("subtitle")),
            txt("详情页ID", "slides[%d].detailId"%i, s.get("detailId")),
            ta("描述", "slides[%d].desc"%i, s.get("desc")))
    sl_html += '</div>'
    sections["sl"] = sl_html

    # 03 关于我们
    sections["ab"] = '''<div class="cd"><div class="ch"><h3>03 · 关于我们</h3></div>
%s%s%s%s</div>''' % (
        img_block("右侧展示图", "company.backgrounds.aboutBg", bg.get("aboutBg"), 1200, 800, "商务/团队场景"),
        txt("品牌标题", "aboutTitle", cfg.get("aboutTitle","让中国企业出海不难")),
        ta("正文内容", "aboutText", cfg.get("aboutText","丝路山海通积极响应国家「一带一路」倡议…"), 3),
        ta("引用语", "aboutQuote", cfg.get("aboutQuote","让企业出海不再难")))

    # 04 核心服务
    sv_html = '''<div class="cd"><div class="ch"><h3>04 · 核心服务 <span class="bd">%d项</span></h3><button class="ab" onclick="addSv()">+ 添加</button></div>''' % len(sv)
    if not sv:
        sv_html += '<p class="em">暂无服务</p>'
    for i, s in enumerate(sv):
        sv_html += '''<div class="ib"><div class="ih"><strong>%s %s</strong><button class="ab" onclick="delSv(%d)">删除</button></div>
%s<div class="ug3">%s%s%s</div>%s</div>''' % (
            esc(s.get("icon","")), esc(s.get("title","")), i,
            img_block("展示图", "services[%d].img"%i, s.get("img"), 400, 300),
            txt("图标(emoji)", "services[%d].icon"%i, s.get("icon")),
            txt("标题", "services[%d].title"%i, s.get("title")),
            txt("副标题", "services[%d].sub"%i, s.get("sub")),
            ta("描述", "services[%d].desc"%i, s.get("desc")))
    sv_html += '</div>'
    sections["sv"] = sv_html

    # 05 政策分析
    po_html = '''<div class="cd"><div class="ch"><h3>05 · 政策分析 <span class="bd">%d项</span></h3><button class="ab" onclick="addPo()">+ 添加</button></div>''' % len(po)
    if not po:
        po_html += '<p class="em">暂无政策</p>'
    # Policy title to detailContent key mapping
    policy_detail_map = {
        "政策研究与解读": "policy-research",
        "政府与商会对接": "policy-network",
        "产业园区落地": "policy-park",
        "投融资对接": "policy-finance"
    }
    for i, p in enumerate(po):
        # Auto-map policy to detailContent based on title
        detail_id = policy_detail_map.get(p.get("title", ""), "")
        hero_img = ""
        if detail_id and dc.get(detail_id):
            m = __import__('re').search(r'<img[^>]+src="([^"]+)"', dc[detail_id].get("content", ""))
            if m:
                hero_img = m.group(1)
        po_html += '''<div class="ib"><div class="ih"><strong>%s %s</strong><button class="ab" onclick="delPo(%d)">删除</button></div>
<div class="ug3">%s%s</div>%s<div class="ug2">%s%s</div></div>''' % (
            esc(p.get("num","")), esc(p.get("title","")), i,
            txt("编号", "policies[%d].num"%i, p.get("num")),
            txt("标题", "policies[%d].title"%i, p.get("title")),
            ta("描述", "policies[%d].desc"%i, p.get("desc")),
            img_block("弹窗图片", "detailContent.%s.heroImg" % detail_id, hero_img, 800, 400, "点击政策卡片后弹窗顶部大图"),
            ta("详情页HTML", "detailContent.%s.content" % detail_id, dc.get(detail_id, {}).get("content",""), 6))
    po_html += '</div>'
    sections["po"] = po_html

    # 06 国家区域（含国家详情弹窗编辑）
    def country_editor(ri, ci, co):
        """每个国家的编辑区域"""
        sv_html = ''
        for si in range(len(co.get('services',[]))):
            v = esc(co['services'][si])
            sv_html += '<input class="csvi" name="countries[%d].countryList[%d].services[%d]" value="%s" placeholder="服务项">' % (ri, ci, si, v)
        sv_html += '<button class="ab sm" onclick="addCsv(%d,%d)">+</button>' % (ri, ci)
        hid = 'cd' + str(ri) + 'c' + str(ci)
        return '''<div class="ci" id="ci-%d-%d"><div class="cih" data-hid="%s" data-ri="%d" data-ci="%d"><strong>%s</strong> <span class="g">%s</span> <button class="ab sm" onclick="delCountry(%d,%d)">删除</button></div>
<div id="%s" class="cib" style="display:none">
<div class="ug2">%s%s</div>%s%s%s</div></div>''' % (
            ri, ci, hid, ri, ci,
            esc(co.get('name','')), esc(co.get('enName','')), ri, ci,
            hid,
            img_block('图片', 'countries[%d].countryList[%d].img'%(ri,ci), co.get('img'), 800, 500),
            txt('中文名', 'countries[%d].countryList[%d].name'%(ri,ci), co.get('name')),
            txt('英文名', 'countries[%d].countryList[%d].enName'%(ri,ci), co.get('enName')),
            ta('描述', 'countries[%d].countryList[%d].desc'%(ri,ci), co.get('desc'), 3),
            '<div class="fg"><label>服务列表</label><div class="csv">' + sv_html + '</div></div>')

    ct_html = '''<div class="cd"><div class="ch"><h3>06 · 国家区域 <span class="bd">%d个区域 / %d国</span></h3><button class="ab" onclick="addCt()">+ 添加区域</button></div>''' % (len(ct), sum(len(c.get('countryList',[])+c.get('countries',[])) for c in ct))
    if not ct:
        ct_html += '<p class="em">暂无区域，点击添加</p>'
    for i, c in enumerate(ct):
        # 基本信息
        ct_html += '''<div class="ib"><div class="ih"><strong>%s</strong><button class="ab" onclick="delCt(%d)">删除</button></div>
<div class="ug3">%s%s%s</div><div class="ug2">%s%s</div><div class="ciwrap">''' % (
            esc(c.get("name","区域")), i,
            txt("区域名称", "countries[%d].name"%i, c.get("name")),
            txt("英文名", "countries[%d].enName"%i, c.get("enName") or c.get("en")),
            txt("覆盖数", "countries[%d].count"%i, c.get("count") or c.get("num")),
            txt("旗帜/图标", "countries[%d].flag"%i, c.get("flag") or c.get("icon")),
            ta("区域描述", "countries[%d].desc"%i, c.get("desc"), 2))
        # 国家详情编辑
        cl = c.get('countryList', [])
        ct_html += '<div class="ch2">国家详情 <button class="ab sm" onclick="addCountry(%d)">+ 添加国家</button></div>' % i
        if cl:
            for j, co in enumerate(cl):
                ct_html += country_editor(i, j, co)
        ct_html += '</div></div>'
    ct_html += '</div>'
    sections["ct"] = ct_html

    # 07 服务流程
    pr_html = '''<div class="cd"><div class="ch"><h3>07 · 服务流程 <span class="bd">%d步</span></h3><button class="ab" onclick="addPr()">+ 添加</button></div>''' % len(pr)
    if not pr:
        pr_html += '<p class="em">暂无流程</p>'
    for i, p in enumerate(pr):
        pr_html += '''<div class="ib"><div class="ih"><strong>%s %s</strong><button class="ab" onclick="delPr(%d)">删除</button></div>
<div class="ug3">%s%s%s</div>%s</div>''' % (
            esc(p.get("num","")), esc(p.get("title","")), i,
            txt("编号", "process[%d].num"%i, p.get("num")),
            txt("步骤标题", "process[%d].title"%i, p.get("title")),
            txt("详情页ID", "process[%d].detailId"%i, p.get("detailId")),
            ta("描述", "process[%d].desc"%i, p.get("desc")))
    pr_html += '</div>'
    sections["pr"] = pr_html

    # 08 数据统计
    st_html = '''<div class="cd"><div class="ch"><h3>08 · 数据统计 <span class="bd">%d项</span></h3><button class="ab" onclick="addSt()">+ 添加</button></div>''' % len(st)
    if not st:
        st_html += '<p class="em">暂无数据</p>'
    for i, s in enumerate(st):
        st_html += '''<div class="ib"><div class="ih"><strong>%s %s</strong><button class="ab" onclick="delSt(%d)">删除</button></div>
<div class="ug2">%s%s</div></div>''' % (
            esc(s.get("num","")), esc(s.get("label","")), i,
            txt("数字", "stats[%d].num"%i, s.get("num")),
            txt("标签", "stats[%d].label"%i, s.get("label")))
    st_html += '</div>'
    sections["st"] = st_html

    # 09 客户评价
    te_html = '''<div class="cd"><div class="ch"><h3>09 · 客户评价 <span class="bd">%d条</span></h3><button class="ab" onclick="addTe()">+ 添加</button></div>''' % len(te)
    if not te:
        te_html += '<p class="em">暂无评价</p>'
    for i, t in enumerate(te):
        te_html += '''<div class="ib"><div class="ih"><strong>%s · %s</strong><button class="ab" onclick="delTe(%d)">删除</button></div>
%s<div class="ug2">%s%s</div>%s</div>''' % (
            esc(t.get("name","")), esc(t.get("role","")), i,
            img_block("头像照片", "testimonials[%d].avatarImg"%i, t.get("avatarImg"), 200, 200, "真人头像或Logo"),
            txt("客户名称", "testimonials[%d].name"%i, t.get("name")),
            txt("职位/公司", "testimonials[%d].role"%i, t.get("role")),
            ta("评价内容", "testimonials[%d].text"%i, t.get("text")))
    te_html += '</div>'
    
    # 客户案例弹窗（独立板块，但放在客户评价后面）
    # dc 已在函数开头定义
    dc_cases = {k: v for k, v in dc.items() if k.startswith("case-")}
    if dc_cases:
        dc_html = '''<div class="cd"><div class="ch"><h3>09b · 客户案例弹窗 <span class="bd">%d个</span></h3></div>''' % len(dc_cases)
        for key, item in dc_cases.items():
            hero_img = ""
            m = __import__('re').search(r'<img[^>]+src="([^"]+)"', item.get("content", ""))
            if m:
                hero_img = m.group(1)
            dc_html += '''<div class="ib" id="dc-%s"><div class="ih"><strong>%s</strong></div>
%s<div class="ug2">%s%s</div>%s</div>''' % (
                key,
                esc(item.get("title", "")),
                img_block("Hero图片", "detailContent.%s.heroImg" % key, hero_img, 800, 400, "弹窗顶部大图"),
                txt("标题", "detailContent.%s.title" % key, item.get("title")),
                txt("副标题", "detailContent.%s.subtitle" % key, item.get("subtitle")),
                ta("内容HTML", "detailContent.%s.content" % key, item.get("content"), 5))
        dc_html += '</div>'
        te_html += dc_html
    
    sections["te"] = te_html

    # 10 CTA
    sections["cta"] = '''<div class="cd"><div class="ch"><h3>10 · 预约召唤（CTA）</h3></div>
%s<div class="ug2">%s%s</div>%s</div>''' % (
        img_block("背景图", "company.backgrounds.ctaBg", bg.get("ctaBg"), 1920, 600, "全宽深色/渐变图"),
        txt("主标题", "cta.heading", cta.get("heading","乘「一带一路」东风")),
        txt("副标题", "cta.subheading", cta.get("subheading","让您的企业 出海无忧")),
        ta("描述", "cta.desc", cta.get("desc","与丝路山海通携手，开启全球化新篇章。")))

    # 11 页脚
    sections["ft"] = '''<div class="cd"><div class="ch"><h3>11 · 页脚信息</h3></div>
%s<div class="ug2">%s%s</div><div class="ug2">%s%s</div>%s</div>''' % (
        img_block("微信二维码", "company.wechatQR", C.get("wechatQR"), 300, 300, "正方形二维码"),
        txt("公司名称", "company.name", C.get("name")),
        txt("邮箱", "company.email", C.get("email")),
        txt("电话", "company.phone", C.get("phone")),
        txt("微信号", "company.wechatId", C.get("wechatId")),
        txt("备案号", "company.icp", C.get("icp")))

    # === 组装完整页面 ===
    page = PAGE_TEMPLATE
    for key in ["nav","sl","ab","sv","po","ct","pr","st","te","cta","ft"]:
        page = page.replace("{{%s}}" % key, sections.get(key, ""))

    return page


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>统一后台 · 丝路山海通</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif}
body{background:#f5f2ef;display:flex;min-height:100vh;color:#302824;font-size:14px}
.side{width:200px;background:#302824;padding:1rem 0;flex-shrink:0;position:sticky;top:0;height:100vh;overflow-y:auto}
.side h2{padding:0 1rem;font-size:.78rem;font-weight:700;color:#d4c8bc;margin-bottom:.5rem}
.side a{display:flex;align-items:center;gap:.3rem;padding:.4rem .6rem .4rem 1rem;color:#a89e96;text-decoration:none;font-size:.7rem;transition:.2s;border-left:3px solid transparent;line-height:1.3;cursor:pointer}
.side a:hover{color:#f0ece6;background:rgba(255,255,255,.05)}
.side a.on{color:#f0ece6;background:rgba(255,255,255,.08);border-left-color:#c44536;font-weight:600}
.side .idx{color:#6b625c;font-size:.55rem;width:12px;flex-shrink:0}
.main{flex:1;padding:1rem 1.5rem;max-width:1100px}
.main h1{font-size:.95rem;font-weight:700}
.main .sub{font-size:.65rem;color:#a89e96;margin-bottom:.5rem}
.msg{display:none;padding:.35rem .6rem;border-radius:4px;margin-bottom:.5rem;font-size:.7rem}
.msg.ok{display:block;background:#e8f5e9;color:#2e7d32;border:1px solid #a5d6a7}
.msg.er{display:block;background:#fce4ec;color:#c62828;border:1px solid #ef9a9a}
.tb{display:flex;gap:.35rem;margin-bottom:.5rem;flex-wrap:wrap}
.btn{padding:.3rem .8rem;border-radius:4px;font-size:.7rem;font-weight:600;cursor:pointer;border:none;transition:.2s}
.btn-g{background:#2d8a4e;color:#fff}.btn-g:hover{background:#1e6b37}
.btn-o{background:transparent;color:#6b625c;border:1px solid #c8c0b8}.btn-o:hover{border-color:#c44536;color:#c44536}
.tp{display:none}.tp.on{display:block}
.cd{background:#fff;border-radius:8px;padding:.7rem .9rem;margin-bottom:.6rem;box-shadow:0 1px 4px rgba(48,40,36,.08)}
.ch{display:flex;align-items:center;justify-content:space-between;margin-bottom:.4rem;flex-wrap:wrap;gap:.2rem}
.ch h3{font-size:.75rem;font-weight:600;display:flex;align-items:center;gap:.3rem}
.bd{font-size:.55rem;padding:.05rem .25rem;border-radius:3px;font-weight:400;background:#e3f2fd;color:#1565c0}
.ab{background:none;border:none;color:#c44536;font-size:.65rem;cursor:pointer;padding:.1rem .25rem;font-weight:600;white-space:nowrap}
.ab:hover{text-decoration:underline}
.fg{margin-bottom:.35rem}
.fg label{display:block;font-size:.62rem;font-weight:600;color:#6b625c;margin-bottom:.08rem}
.fg input,.fg textarea,.fg select{width:100%;padding:.28rem .38rem;border:1px solid #c8c0b8;border-radius:4px;font-size:.72rem;font-family:inherit;background:#fff}
.fg textarea{min-height:34px;resize:vertical}
.fg input:focus,.fg textarea:focus{outline:none;border-color:#c44536;box-shadow:0 0 0 2px rgba(196,69,54,.1)}
.ht{font-size:.58rem;color:#a89e96;margin-top:.08rem;line-height:1.3}
.pv{max-width:100px;max-height:70px;border-radius:4px;margin-top:.1rem;display:block;border:1px solid #f0eae4}
.ib{background:#faf8f6;border-radius:6px;padding:.4rem .6rem;margin-bottom:.35rem;border:1px solid #f0eae4}
.ih{display:flex;align-items:center;justify-content:space-between;margin-bottom:.2rem;flex-wrap:wrap;gap:.1rem}
.ih strong{font-size:.72rem;color:#302824}
.em{font-size:.68rem;color:#a89e96;padding:.3rem 0}
.fo{font-size:.6rem;color:#a89e96;margin-top:.8rem;text-align:center}
.ug2{display:grid;grid-template-columns:1fr 1fr;gap:.35rem}
.ug3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.35rem}
.sz{font-size:.55rem;color:#a89e96;background:#f5f2ef;display:inline-block;padding:.08rem .25rem;border-radius:3px;margin-left:.25rem}
.np{font-size:.58rem;color:#ccc;font-style:italic}

/* 国家详情编辑器 */
.ciwrap{border-top:1px dashed #ddd;margin-top:.35rem;padding-top:.35rem}
.ch2{font-size:.72rem;font-weight:600;color:#6b625c;margin-bottom:.2rem;padding:.15rem .25rem;background:#f8f5f2;border-radius:4px}
.ci{border:1px solid #eee;border-radius:6px;margin-bottom:.15rem;overflow:hidden}
.cih{padding:.2rem .35rem;background:#fcfaf8;cursor:pointer;display:flex;align-items:center;gap:.35rem;font-size:.72rem}
.cih .g{color:#a89e96;font-size:.65rem}
.cih .ar{color:#c8c0b8;margin-left:auto;font-size:.55rem}
.cib{padding:.3rem;border-top:1px solid #eee;display:none}
.cib .fg{margin-top:.15rem}
.cib .fg label{font-size:.62rem;color:#a89e96}
.csv{display:flex;flex-wrap:wrap;gap:.15rem}
.csvi{flex:1;min-width:120px;padding:.2rem .3rem;border:1px solid #d8d0c8;border-radius:4px;font-size:.65rem}
.sm{font-size:.6rem;padding:.08rem .25rem;background:#28a745;color:#fff;border:none;border-radius:3px;cursor:pointer}</style>
</head>
<body>
<div class="side">
  <h2>丝路山海通</h2>
  <a onclick="return sw(this,'nav')" class="on"><span class="idx">01</span>导航栏</a>
  <a onclick="return sw(this,'sl')"><span class="idx">02</span>轮播幻灯片</a>
  <a onclick="return sw(this,'ab')"><span class="idx">03</span>关于我们</a>
  <a onclick="return sw(this,'sv')"><span class="idx">04</span>核心服务</a>
  <a onclick="return sw(this,'po')"><span class="idx">05</span>政策分析</a>
  <a onclick="return sw(this,'ct')"><span class="idx">06</span>国家区域</a>
  <a onclick="return sw(this,'pr')"><span class="idx">07</span>服务流程</a>
  <a onclick="return sw(this,'st')"><span class="idx">08</span>数据统计</a>
  <a onclick="return sw(this,'te')"><span class="idx">09</span>客户评价</a>
  <a onclick="return sw(this,'cta')"><span class="idx">10</span>预约召唤</a>
  <a onclick="return sw(this,'ft')"><span class="idx">11</span>页脚信息</a>
  <a onclick="return sw(this,'bk')" style="margin-top:.5rem;border-left-color:#c44536;color:#c44536">📋 预约记录</a>
</div>
<div class="main">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.05rem">
    <h1>统一后台 · 菜单直接显示现有内容</h1>
    <span style="font-size:.62rem;color:#a89e96">不修改源文件</span>
  </div>
  <div class="sub">所有数据已填入输入框，改完点"保存全部"即可</div>
  <div id="msg" class="msg"></div>
  <div class="tb">
    <button class="btn btn-g" onclick="svAll()">💾 保存全部</button>
    <button class="btn btn-o" onclick="window.open('/preview','_blank')">👁 预览网站</button>
    <button class="btn btn-o" onclick="pubGH()" id="pubBtn" style="background:#24292e;color:#fff;border-color:#24292e">🚀 发布 GitHub</button>
  </div>
  <div class="tp on" id="tp_nav">{{nav}}</div>
  <div class="tp" id="tp_sl">{{sl}}</div>
  <div class="tp" id="tp_ab">{{ab}}</div>
  <div class="tp" id="tp_sv">{{sv}}</div>
  <div class="tp" id="tp_po">{{po}}</div>
  <div class="tp" id="tp_ct">{{ct}}</div>
  <div class="tp" id="tp_pr">{{pr}}</div>
  <div class="tp" id="tp_st">{{st}}</div>
  <div class="tp" id="tp_te">{{te}}</div>
  <div class="tp" id="tp_cta">{{cta}}</div>
  <div class="tp" id="tp_ft">{{ft}}</div>
  <div class="tp" id="tp_bk"></div>
  <div class="fo"><a href="/preview">localhost:8083/preview</a></div>
</div>

<script>
var D = {};
function $(id) { return document.getElementById(id); }
function msg(t,c){ var e=$('msg'); e.textContent=t; e.className='msg '+c; e.style.display='block'; }
function es(s){ if(!s) return ''; return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

var cur = 'nav';
function sw(el,id){
  document.querySelectorAll('.side a').forEach(function(a){ a.classList.remove('on'); });
  el.classList.add('on');
  document.querySelectorAll('.tp').forEach(function(t){ t.classList.remove('on'); });
  $(id==='bk'?'tp_bk':'tp_'+id).classList.add('on');
  cur = id;
  if(id==='bk') loadBk();
  return false;
}

function collect(){
  var inputs = document.querySelectorAll('.fg input[name], .fg textarea[name], .csvi');
  var data = {};
  inputs.forEach(function(inp){
    var name = inp.getAttribute('name');
    if(!name) return;
    var val = inp.value;
    var path = name.split(/[\[\].]+/).filter(Boolean);
    // Simple top-level key: set directly
    if(path.length <= 2 && /^[a-zA-Z_]\w*$/.test(name)) {
      data[name] = val;
      return;
    }
    // Walk nested path to set val at leaf
    var cur = data;
    for(var i=0; i<path.length; i++){
      var k = path[i];
      var n = parseInt(k);
      var isNum = !isNaN(n) && String(n)===k;
      var last = (i === path.length-1);
      if(last){
        cur[k] = val;
      } else {
        var nk = path[i+1];
        var nn = parseInt(nk);
        var nIsNum = !isNaN(nn) && String(nn)===nk;
        if(isNum) {
          if(!cur[n] || cur[n]===null) cur[n] = nIsNum ? [] : {};
          cur = cur[n];
        } else {
          if(!cur[k] || cur[k]===null) cur[k] = nIsNum ? [] : {};
          cur = cur[k];
        }
      }
    }
  });
  return data;
}
function svAll(){
  msg('保存中...','ok');
  var x = new XMLHttpRequest();
  x.open('POST','/api/save_all',true);
  x.setRequestHeader('Content-Type','application/json');
  x.onload=function(){
    if(x.status===200){ var r=JSON.parse(x.responseText); msg(r.message||'保存成功','ok'); }
    else msg('保存失败: '+x.status,'er');
  };
  x.onerror=function(){ msg('网络错误','er'); };
  x.send(JSON.stringify(collect()));
}

function pubGH(){
  var btn=$('pubBtn'); btn.textContent='⏳ 发布中'; btn.disabled=true;
  var x=new XMLHttpRequest();
  x.open('POST','/api/publish',true);
  x.onload=function(){
    btn.disabled=false;
    if(x.status===200){ var r=JSON.parse(x.responseText);
      if(r.success){ msg(r.message,'ok'); btn.textContent='已发布'; }
      else { msg(r.message,'er'); btn.textContent='发布 GitHub'; }
    } else { msg('发布失败','er'); btn.textContent='发布 GitHub'; }
    setTimeout(function(){ btn.textContent='发布 GitHub'; },3000);
  };
  x.onerror=function(){ msg('网络错误','er'); btn.textContent='发布 GitHub'; };
  x.send();
}

function loadBk(){
  var x=new XMLHttpRequest();
  x.open('GET','/api/bookings',true);
  x.onload=function(){
    if(x.status===200) renderBk(JSON.parse(x.responseText));
  };
  x.send();
}
function addCsv(ri,ci){
  var container = document.querySelector('[name^="countries['+ri+'].countryList['+ci+'].services[0]"]').parentNode;
  var count = container.querySelectorAll('.csvi').length;
  var inp = document.createElement('input');
  inp.className = 'csvi';
  inp.name = 'countries['+ri+'].countryList['+ci+'].services['+count+']';
  inp.placeholder = '服务项';
  var addBtn = container.querySelector('.sm');
  container.insertBefore(inp, addBtn);
}
function toggle(btn, id){
  var el = document.getElementById(id);
  if(el) el.style.display = el.style.display==='none'?'block':'none';
}
function addCountry(ri){
  var wrap = document.querySelector('[name="countries['+ri+'].name"]').closest('.ib').querySelector('.ciwrap');
  var cnt = wrap.querySelectorAll('.ci').length;
  var hid = 'cd'+ri+'c'+cnt;
  var div = document.createElement('div'); div.className = 'ci';
  var cih = document.createElement('div'); cih.className='cih'; cih.innerHTML='<strong>新国家</strong> <span class="g">new country</span> <span class="ar">▼</span>';
  cih.onclick = function(){ toggle(this, hid); };
  var cib = document.createElement('div'); cib.id=hid; cib.className='cib'; cib.style.display='none';
  cib.innerHTML = '<div class="ug2">'+
    '<div class="fg"><label>图片URL</label><input name="countries['+ri+'].countryList['+cnt+'].img" value="" placeholder="https://..."></div>'+
    '<div class="fg"><label>英文名</label><input name="countries['+ri+'].countryList['+cnt+'].enName" value="" placeholder="english name"></div></div>'+
    '<div class="fg"><label>中文名</label><input name="countries['+ri+'].countryList['+cnt+'].name" value="" placeholder="国家中文名"></div>'+
    '<div class="fg"><label>描述</label><textarea name="countries['+ri+'].countryList['+cnt+'].desc" rows="3" placeholder="国家描述"></textarea></div>'+
    '<div class="fg"><label>服务列表</label><div class="csv">'+
    '<input class="csvi" name="countries['+ri+'].countryList['+cnt+'].services[0]" value="" placeholder="服务项">'+
    '<input class="csvi" name="countries['+ri+'].countryList['+cnt+'].services[1]" value="" placeholder="服务项">'+
    '<button class="ab sm" onclick="addCsv('+ri+','+cnt+')">+</button></div></div>';
  div.appendChild(cih); div.appendChild(cib);
  wrap.appendChild(div);
}function delCountry(ri,ci){
  if(!confirm('确认删除该国家?')) return;
  var el = document.getElementById('ci-'+ri+'-'+ci);
  if(el) el.remove();
}// Bind country header clicks
document.addEventListener('DOMContentLoaded', function(){
  document.querySelectorAll('.cih').forEach(function(el){
    el.addEventListener('click', function(e){
      if(e.target.tagName === 'BUTTON') return; // Don't toggle if delete clicked
      var hid = this.getAttribute('data-hid');
      var cib = document.getElementById(hid);
      if(cib) cib.style.display = cib.style.display === 'none' ? 'block' : 'none';
    });
  });
});function renderBk(data){
  var total=data.length, today=new Date().toISOString().slice(0,10);
  var tc=data.filter(function(b){return b.created_at&&b.created_at.slice(0,10)===today;}).length;
  var pd=data.filter(function(b){return b.status!=='done';}).length;
  var h='<div class="cd"><div class="ch"><h3>预约记录 <span class="bd">'+total+'条</span></h3><span style="font-size:.58rem;color:#a89e96">30秒自动刷新</span></div>';
  h+='<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(80px,1fr));gap:.3rem;margin-bottom:.4rem">';
  h+='<div style="text-align:center;padding:.3rem;background:#faf8f6;border-radius:6px"><div style="font-weight:700;font-size:.95rem;color:#c44536">'+total+'</div><div style="font-size:.55rem;color:#a89e96">全部</div></div>';
  h+='<div style="text-align:center;padding:.3rem;background:#faf8f6;border-radius:6px"><div style="font-weight:700;font-size:.95rem;color:#c44536">'+tc+'</div><div style="font-size:.55rem;color:#a89e96">今日</div></div>';
  h+='<div style="text-align:center;padding:.3rem;background:#faf8f6;border-radius:6px"><div style="font-weight:700;font-size:.95rem;color:#c44536">'+pd+'</div><div style="font-size:.55rem;color:#a89e96">待处理</div></div></div>';
  h+='<input class="srch" id="bkQ" placeholder="搜索..." oninput="bkF()" style="width:100%;padding:.28rem .38rem;border:1px solid #c8c0b8;border-radius:4px;font-size:.7rem;margin-bottom:.35rem">';
  h+='<div style="display:grid;grid-template-columns:auto 1fr auto auto auto;gap:.3rem;align-items:center;padding:.25rem .35rem;border-bottom:1px solid #f0eae4;font-size:.7rem">';
  h+='<span style="font-weight:600;color:#6b625c;font-size:.62rem">姓名</span><span style="font-weight:600;color:#6b625c;font-size:.62rem">手机</span><span style="font-weight:600;color:#6b625c;font-size:.62rem">国家</span><span style="font-weight:600;color:#6b625c;font-size:.62rem">时间</span><span style="font-weight:600;color:#6b625c;font-size:.62rem">状态</span><span style="font-weight:600;color:#6b625c;font-size:.62rem">操作</span></div><div id="bkL">';
  for(var i=0;i<data.length;i++){
    var b=data[i];
    h+='<div class="bk-r" style="display:grid;grid-template-columns:auto 1fr auto auto auto;gap:.3rem;align-items:center;padding:.25rem .35rem;border-bottom:1px solid #f0eae4;font-size:.7rem" data-n="'+es(b.name)+'" data-p="'+es(b.phone)+'" data-c="'+es(b.country)+'">';
    h+='<span>'+es(b.name||'-')+'</span><span style="font-size:.65rem">'+es(b.phone||'-')+'</span><span>'+es(b.country||'-')+'</span>';
    h+='<span style="font-size:.62rem;color:#a89e96">'+(b.created_at||'')+'</span>';
    h+='<span><span style="font-size:.55rem;padding:.05rem .2rem;border-radius:3px;background:'+(b.status==='done'?'#e8f5e9;color:#2e7d32':'#fce4ec;color:#c62828')+'">'+(b.status==='done'?'已处理':'待处理')+'</span></span>';
    h+='<span>'; if(b.status!=='done') h+='<button class="ab" onclick="bkDone('+b.id+')">标记</button>'; h+='<button class="ab" onclick="bkDel('+b.id+')" style="color:#999">删除</button></span></div>';
  }
  h+='</div></div>';
  $('tp_bk').innerHTML=h;
}
function bkF(){
  var q=$('bkQ').value.toLowerCase();
  document.querySelectorAll('.bk-r').forEach(function(r){
    r.style.display=(r.dataset.n.indexOf(q)>-1||r.dataset.p.indexOf(q)>-1||r.dataset.c.indexOf(q)>-1)?'':'none';
  });
}
function bkDone(id){
  var x=new XMLHttpRequest();
  x.open('POST','/api/booking/update',true);
  x.setRequestHeader('Content-Type','application/json');
  x.onload=function(){ if(x.status===200) loadBk(); };
  x.send(JSON.stringify({id:id,status:'done'}));
}
function bkDel(id){
  if(!confirm('确认删除?')) return;
  var x=new XMLHttpRequest();
  x.open('POST','/api/booking/del',true);
  x.setRequestHeader('Content-Type','application/json');
  x.onload=function(){ if(x.status===200) loadBk(); };
  x.send(JSON.stringify({id:id}));
}
setInterval(function(){ if(cur==='bk') loadBk(); },30000);
</script>
</body></html>"""


LOGIN_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>统一后台登录 · 丝路山海通</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,"Segoe UI",sans-serif}
body{background:url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920') center/cover no-repeat;display:flex;justify-content:center;align-items:center;min-height:100vh}
.l-box{background:rgba(255,255,255,.95);border-radius:12px;padding:2.5rem;width:360px;box-shadow:0 8px 32px rgba(48,40,36,.15);text-align:center}
.l-box h1{font-size:1.2rem;color:#302824;margin-bottom:.3rem}
.l-box p{font-size:.8rem;color:#a89e96;margin-bottom:1.5rem}
.fg{margin-bottom:.8rem;text-align:left}
.fg label{display:block;font-size:.78rem;font-weight:600;margin-bottom:.2rem;color:#6b625c}
.fg input{width:100%;padding:.45rem .5rem;border:1px solid #c8c0b8;border-radius:4px;font-size:.85rem;background:#fff;outline:none}
.fg input:focus{border-color:#c44536;box-shadow:0 0 0 2px rgba(196,69,54,.1)}
.btn{padding:.5rem 1.2rem;border-radius:4px;font-size:.85rem;font-weight:600;cursor:pointer;border:none;transition:.2s;width:100%;background:#2d8a4e;color:#fff}
.btn:hover{background:#1e6b37}
.msg{padding:.5rem .8rem;border-radius:4px;margin-bottom:1rem;font-size:.8rem;display:none}
.msg.er{display:block;background:#fce4ec;color:#c62828;border:1px solid #ef9a9a}
</style></head><body>
<div class="l-box"><h1>丝路山海通</h1><p>统一后台管理</p><div id="msg" class="msg"></div>
<div class="fg"><label>用户名</label><input id="user" type="text" autocomplete="username" autofocus></div>
<div class="fg"><label>密码</label><input id="pass" type="password" autocomplete="current-password"></div>
<button class="btn" onclick="login()">登 录</button></div>
<script>
function login(){
  var u=document.getElementById('user'),p=document.getElementById('pass'),m=document.getElementById('msg');
  if(!u.value){m.textContent='请输入用户名';m.className='msg er';return;}
  if(!p.value){m.textContent='请输入密码';m.className='msg er';return;}
  var x=new XMLHttpRequest();
  x.open('POST','/api/login',true);x.setRequestHeader('Content-Type','application/json');
  x.onload=function(){ if(x.status===200) window.location.href='/admin'; else { var r=JSON.parse(x.responseText); m.textContent=r.message||'登录失败'; m.className='msg er'; } };
  x.onerror=function(){ m.textContent='网络错误'; m.className='msg er'; };
  x.send(JSON.stringify({username:u.value,password:p.value}));
}
</script></body></html>"""


INJECT_SCRIPT = """<script>
// Config-driven DOM update - injected by admin server
(function(){
var c = CONFIG;
if(!c || !c.company) return;
// --- Update title ---
var t = document.querySelector("title");
if(t) t.textContent = c.company.name + " - " + c.company.slogan;
// --- Update footer ---
document.querySelectorAll(".footer-bottom span").forEach(function(el){
  var txt = el.textContent;
  if(txt.indexOf("\u00a9") >= 0 || txt.indexOf("All rights") >= 0) {
    el.textContent = "\u00a9 " + new Date().getFullYear() + " " + c.company.name + ". All rights reserved.";
  }
  if(txt.indexOf("ICP") >= 0 || txt.indexOf("\u7ca4") >= 0) {
    if(c.company.icp) el.textContent = c.company.icp;
  }
});
// --- Update email ---
var mailtoLinks = document.querySelectorAll("a[href^='mailto:']");
console.log("[Config Inject] Found " + mailtoLinks.length + " mailto links");
mailtoLinks.forEach(function(el, i){
  if(c.company.email) {
    console.log("[Config Inject] Updating mailto link #" + i + ": " + el.href + " -> " + c.company.email);
    el.href = "mailto:" + c.company.email;
    el.textContent = c.company.email;
  }
});
// --- Render services from CONFIG ---
var sg = document.querySelector(".services-grid");
if(sg && c.services && c.services.length > 0) {
  var cols = ["linear-gradient(135deg,#C44536,#8B2D1E)","linear-gradient(135deg,#C8923E,#8B6914)","linear-gradient(135deg,#1A1512,#302824)","linear-gradient(135deg,#6B625C,#A89E96)","linear-gradient(135deg,#C44536,#C8923E)","linear-gradient(135deg,#302824,#6B625C)"];
  var ems = ["🏭t>
// Config-driven DOM update - injected by admin server
(function(){
var c = CONFIG;
if(!c || !c.company) return;
// --- Update title ---
var t = document.querySelector("title");
if(t) t.textContent = c.company.name + " - " + c.company.slogan;
// --- Update footer ---
document.querySelectorAll(".footer-bottom span").forEach(function(el){
  var txt = el.textContent;
  if(txt.indexOf("\u00a9") >= 0 || txt.indexOf("All rights") >= 0) {
    el.textContent = "\u00a9 " + new Date().getFullYear() + " " + c.company.name + ". All rights reserved.";
  }
  if(txt.indexOf("ICP") >= 0 || txt.indexOf("\u7ca4") >= 0) {
    if(c.company.icp) el.textContent = c.company.icp;
  }
});
// --- Update email ---
var mailtoLinks = document.querySelectorAll("a[href^='mailto:']");
console.log("[Config Inject] Found " + mailtoLinks.length + " mailto links");
mailtoLinks.forEach(function(el, i){
  if(c.company.email) {
    console.log("[Config Inject] Updating mailto link #" + i + ": " + el.href + " -> " + c.company.email);
    el.href = "mailto:" + c.company.email;
    el.textContent = c.company.email;
  }
});
// --- Render services from CONFIG ---
var sg = document.querySelector(".services-grid");
if(sg && c.services && c.services.length > 0) {
  var cols = ["linear-gradient(135deg,#C44536,#8B2D1E)","linear-gradient(135deg,#C8923E,#8B6914)","linear-gradient(135deg,#1A1512,#302824)","linear-gradient(135deg,#6B625C,#A89E96)","linear-gradient(135deg,#C44536,#C8923E)","linear-gradient(135deg,#302824,#6B625C)"];
  var ems = ["🏭","📋t>
// Config-driven DOM update - injected by admin server
(function(){
var c = CONFIG;
if(!c || !c.company) return;
// --- Update title ---
var t = document.querySelector("title");
if(t) t.textContent = c.company.name + " - " + c.company.slogan;
// --- Update footer ---
document.querySelectorAll(".footer-bottom span").forEach(function(el){
  var txt = el.textContent;
  if(txt.indexOf("\u00a9") >= 0 || txt.indexOf("All rights") >= 0) {
    el.textContent = "\u00a9 " + new Date().getFullYear() + " " + c.company.name + ". All rights reserved.";
  }
  if(txt.indexOf("ICP") >= 0 || txt.indexOf("\u7ca4") >= 0) {
    if(c.company.icp) el.textContent = c.company.icp;
  }
});
// --- Update email ---
var mailtoLinks = document.querySelectorAll("a[href^='mailto:']");
console.log("[Config Inject] Found " + mailtoLinks.length + " mailto links");
mailtoLinks.forEach(function(el, i){
  if(c.company.email) {
    console.log("[Config Inject] Updating mailto link #" + i + ": " + el.href + " -> " + c.company.email);
    el.href = "mailto:" + c.company.email;
    el.textContent = c.company.email;
  }
});
// --- Render services from CONFIG ---
var sg = document.querySelector(".services-grid");
if(sg && c.services && c.services.length > 0) {
  var cols = ["linear-gradient(135deg,#C44536,#8B2D1E)","linear-gradient(135deg,#C8923E,#8B6914)","linear-gradient(135deg,#1A1512,#302824)","linear-gradient(135deg,#6B625C,#A89E96)","linear-gradient(135deg,#C44536,#C8923E)","linear-gradient(135deg,#302824,#6B625C)"];
  var ems = ["🏭","📋","\u2696️","🛡t>
// Config-driven DOM update - injected by admin server
(function(){
var c = CONFIG;
if(!c || !c.company) return;
// --- Update title ---
var t = document.querySelector("title");
if(t) t.textContent = c.company.name + " - " + c.company.slogan;
// --- Update footer ---
document.querySelectorAll(".footer-bottom span").forEach(function(el){
  var txt = el.textContent;
  if(txt.indexOf("\u00a9") >= 0 || txt.indexOf("All rights") >= 0) {
    el.textContent = "\u00a9 " + new Date().getFullYear() + " " + c.company.name + ". All rights reserved.";
  }
  if(txt.indexOf("ICP") >= 0 || txt.indexOf("\u7ca4") >= 0) {
    if(c.company.icp) el.textContent = c.company.icp;
  }
});
// --- Update email ---
var mailtoLinks = document.querySelectorAll("a[href^='mailto:']");
console.log("[Config Inject] Found " + mailtoLinks.length + " mailto links");
mailtoLinks.forEach(function(el, i){
  if(c.company.email) {
    console.log("[Config Inject] Updating mailto link #" + i + ": " + el.href + " -> " + c.company.email);
    el.href = "mailto:" + c.company.email;
    el.textContent = c.company.email;
  }
});
// --- Render services from CONFIG ---
var sg = document.querySelector(".services-grid");
if(sg && c.services && c.services.length > 0) {
  var cols = ["linear-gradient(135deg,#C44536,#8B2D1E)","linear-gradient(135deg,#C8923E,#8B6914)","linear-gradient(135deg,#1A1512,#302824)","linear-gradient(135deg,#6B625C,#A89E96)","linear-gradient(135deg,#C44536,#C8923E)","linear-gradient(135deg,#302824,#6B625C)"];
  var ems = ["🏭","📋","\u2696️","\\ud83d\\udee1️","🌐t>
// Config-driven DOM update - injected by admin server
(function(){
var c = CONFIG;
if(!c || !c.company) return;
// --- Update title ---
var t = document.querySelector("title");
if(t) t.textContent = c.company.name + " - " + c.company.slogan;
// --- Update footer ---
document.querySelectorAll(".footer-bottom span").forEach(function(el){
  var txt = el.textContent;
  if(txt.indexOf("\u00a9") >= 0 || txt.indexOf("All rights") >= 0) {
    el.textContent = "\u00a9 " + new Date().getFullYear() + " " + c.company.name + ". All rights reserved.";
  }
  if(txt.indexOf("ICP") >= 0 || txt.indexOf("\u7ca4") >= 0) {
    if(c.company.icp) el.textContent = c.company.icp;
  }
});
// --- Update email ---
var mailtoLinks = document.querySelectorAll("a[href^='mailto:']");
console.log("[Config Inject] Found " + mailtoLinks.length + " mailto links");
mailtoLinks.forEach(function(el, i){
  if(c.company.email) {
    console.log("[Config Inject] Updating mailto link #" + i + ": " + el.href + " -> " + c.company.email);
    el.href = "mailto:" + c.company.email;
    el.textContent = c.company.email;
  }
});
// --- Render services from CONFIG ---
var sg = document.querySelector(".services-grid");
if(sg && c.services && c.services.length > 0) {
  var cols = ["linear-gradient(135deg,#C44536,#8B2D1E)","linear-gradient(135deg,#C8923E,#8B6914)","linear-gradient(135deg,#1A1512,#302824)","linear-gradient(135deg,#6B625C,#A89E96)","linear-gradient(135deg,#C44536,#C8923E)","linear-gradient(135deg,#302824,#6B625C)"];
  var ems = ["🏭","📋","\u2696️","\\ud83d\\udee1️","🌐","🛢t>
// Config-driven DOM update - injected by admin server
(function(){
var c = CONFIG;
if(!c || !c.company) return;
// --- Update title ---
var t = document.querySelector("title");
if(t) t.textContent = c.company.name + " - " + c.company.slogan;
// --- Update footer ---
document.querySelectorAll(".footer-bottom span").forEach(function(el){
  var txt = el.textContent;
  if(txt.indexOf("\u00a9") >= 0 || txt.indexOf("All rights") >= 0) {
    el.textContent = "\u00a9 " + new Date().getFullYear() + " " + c.company.name + ". All rights reserved.";
  }
  if(txt.indexOf("ICP") >= 0 || txt.indexOf("\u7ca4") >= 0) {
    if(c.company.icp) el.textContent = c.company.icp;
  }
});
// --- Update email ---
var mailtoLinks = document.querySelectorAll("a[href^='mailto:']");
console.log("[Config Inject] Found " + mailtoLinks.length + " mailto links");
mailtoLinks.forEach(function(el, i){
  if(c.company.email) {
    console.log("[Config Inject] Updating mailto link #" + i + ": " + el.href + " -> " + c.company.email);
    el.href = "mailto:" + c.company.email;
    el.textContent = c.company.email;
  }
});
// --- Render services from CONFIG ---
var sg = document.querySelector(".services-grid");
if(sg && c.services && c.services.length > 0) {
  var cols = ["linear-gradient(135deg,#C44536,#8B2D1E)","linear-gradient(135deg,#C8923E,#8B6914)","linear-gradient(135deg,#1A1512,#302824)","linear-gradient(135deg,#6B625C,#A89E96)","linear-gradient(135deg,#C44536,#C8923E)","linear-gradient(135deg,#302824,#6B625C)"];
  var ems = ["🏭","📋","\u2696️","\\ud83d\\udee1️","🌐","\\ud83d\\udee2️"];
  sg.innerHTML = c.services.map(function(s,i){
    return '<div class="service-card" onclick="openDetail(\\'' + (s.detailId || s.id) + '\\')">' +
      '<div class="sc-img"><div class="sc-img-bg" style="background:' + cols[i % cols.length] + '"></div><span>' + ems[i % ems.length] + '</span></div>' +
      '<h3>' + s.title + '</h3>' +
      (s.sub ? '<div class="sc-sub">' + s.sub + '</div>' : '') +
      '<p>' + (s.desc || '') + '</p></div>';
  }).join('');
}
// --- Render stats from CONFIG ---
var si = document.querySelector(".stats-inner");
if(si && c.stats && c.stats.length > 0) {
  si.innerHTML = c.stats.map(function(s){
    return '<div class="stat-item"><div class="num">' + (s.num || '') + '</div><div class="label">' + (s.label || '') + '</div></div>';
  }).join('');
}
// --- Render policies from CONFIG ---
var pg = document.querySelector(".policy-grid");
var policyIds = ['policy-research', 'policy-network', 'policy-park', 'policy-finance'];
if(pg && c.policies && c.policies.length > 0) {
  pg.innerHTML = c.policies.map(function(p, i){
    var n = String(i + 1).padStart(2, '0');
    var detailId = policyIds[i] || ('policy-' + i);
    return '<div class="policy-card" onclick="openDetail(\\'' + detailId + '\\')">' +
      '<div class="pn">' + n + '</div><div>' +
      '<h3>' + p.title + '</h3><p>' + (p.desc || '') + '</p></div></div>';
  }).join('');
}
// --- Render testimonials from CONFIG ---
var tg = document.querySelector(".testimonials-grid");
var caseIds = ['case-zhang', 'case-li', 'case-wang'];
if(tg && c.testimonials && c.testimonials.length > 0) {
  tg.innerHTML = c.testimonials.map(function(t, i){
    var av = t.avatar || (t.name ? t.name.charAt(0) : "👤t>
// Config-driven DOM update - injected by admin server
(function(){
var c = CONFIG;
if(!c || !c.company) return;
// --- Update title ---
var t = document.querySelector("title");
if(t) t.textContent = c.company.name + " - " + c.company.slogan;
// --- Update footer ---
document.querySelectorAll(".footer-bottom span").forEach(function(el){
  var txt = el.textContent;
  if(txt.indexOf("\u00a9") >= 0 || txt.indexOf("All rights") >= 0) {
    el.textContent = "\u00a9 " + new Date().getFullYear() + " " + c.company.name + ". All rights reserved.";
  }
  if(txt.indexOf("ICP") >= 0 || txt.indexOf("\u7ca4") >= 0) {
    if(c.company.icp) el.textContent = c.company.icp;
  }
});
// --- Update email ---
var mailtoLinks = document.querySelectorAll("a[href^='mailto:']");
console.log("[Config Inject] Found " + mailtoLinks.length + " mailto links");
mailtoLinks.forEach(function(el, i){
  if(c.company.email) {
    console.log("[Config Inject] Updating mailto link #" + i + ": " + el.href + " -> " + c.company.email);
    el.href = "mailto:" + c.company.email;
    el.textContent = c.company.email;
  }
});
// --- Render services from CONFIG ---
var sg = document.querySelector(".services-grid");
if(sg && c.services && c.services.length > 0) {
  var cols = ["linear-gradient(135deg,#C44536,#8B2D1E)","linear-gradient(135deg,#C8923E,#8B6914)","linear-gradient(135deg,#1A1512,#302824)","linear-gradient(135deg,#6B625C,#A89E96)","linear-gradient(135deg,#C44536,#C8923E)","linear-gradient(135deg,#302824,#6B625C)"];
  var ems = ["🏭","📋","\u2696️","\\ud83d\\udee1️","🌐","\\ud83d\\udee2️"];
  sg.innerHTML = c.services.map(function(s,i){
    return '<div class="service-card" onclick="openDetail(\\'' + (s.detailId || s.id) + '\\')">' +
      '<div class="sc-img"><div class="sc-img-bg" style="background:' + cols[i % cols.length] + '"></div><span>' + ems[i % ems.length] + '</span></div>' +
      '<h3>' + s.title + '</h3>' +
      (s.sub ? '<div class="sc-sub">' + s.sub + '</div>' : '') +
      '<p>' + (s.desc || '') + '</p></div>';
  }).join('');
}
// --- Render stats from CONFIG ---
var si = document.querySelector(".stats-inner");
if(si && c.stats && c.stats.length > 0) {
  si.innerHTML = c.stats.map(function(s){
    return '<div class="stat-item"><div class="num">' + (s.num || '') + '</div><div class="label">' + (s.label || '') + '</div></div>';
  }).join('');
}
// --- Render policies from CONFIG ---
var pg = document.querySelector(".policy-grid");
var policyIds = ['policy-research', 'policy-network', 'policy-park', 'policy-finance'];
if(pg && c.policies && c.policies.length > 0) {
  pg.innerHTML = c.policies.map(function(p, i){
    var n = String(i + 1).padStart(2, '0');
    var detailId = policyIds[i] || ('policy-' + i);
    return '<div class="policy-card" onclick="openDetail(\\'' + detailId + '\\')">' +
      '<div class="pn">' + n + '</div><div>' +
      '<h3>' + p.title + '</h3><p>' + (p.desc || '') + '</p></div></div>';
  }).join('');
}
// --- Render testimonials from CONFIG ---
var tg = document.querySelector(".testimonials-grid");
var caseIds = ['case-zhang', 'case-li', 'case-wang'];
if(tg && c.testimonials && c.testimonials.length > 0) {
  tg.innerHTML = c.testimonials.map(function(t, i){
    var av = t.avatar || (t.name ? t.name.charAt(0) : "👤");
    var detailId = t.detailId || caseIds[i] || ('case-' + i);
    return '<div class="t-card" onclick="openDetail(\\'' + detailId + '\\')">' +
      '<div class="tq">&ldquo;</div><p class="t-text">' + (t.text || '') + '</p>' +
      '<div class="t-author"><div class="t-av">' + av + '</div><div>' +
      '<div class="t-name">' + (t.name || '') + '</div><div class="t-role">' + (t.role || '') + '</div></div></div></div>';
  }).join('');
}
// --- Render process from CONFIG ---
var pr = document.querySelector(".process-grid");
var processIds = ['process-step1', 'process-step2', 'process-step3', 'process-step4'];
if(pr && c.process && c.process.length > 0) {
  pr.innerHTML = c.process.map(function(p, i){
    var detailId = p.detailId || processIds[i] || ('process-step' + (i+1));
    return '<div class="pstep" onclick="openDetail(\\'' + detailId + '\\')">' +
      '<div class="ring"><div class="n">' + (p.num || '') + '</div></div>' +
      '<h3>' + (p.title || '') + '</h3><p>' + (p.desc || '') + '</p></div>';
  }).join('');
}
// --- Update SLIDE_CONFIG from CONFIG.slides ---
if(c.slides && c.slides.length > 0) {
  var newSlides = c.slides.map(function(s, i){
    return {
      id: s.id || ("slide-" + (i+1)),
      title: s.title || '',
      subtitle: s.subtitle || '',
      desc: s.desc || '',
      img: s.img || '',
      detailId: s.detailId || ''
    };
  });
  window.SLIDE_CONFIG = newSlides;
  if(typeof window.updateSlide === 'function') {
    window.currentSlide = 0;
    window.updateSlide();
  }
}
// --- Update logo text ---
document.querySelectorAll(".logo-text strong").forEach(function(el){
  if(c.company.name) el.textContent = c.company.name;
});
document.querySelectorAll(".logo-text span").forEach(function(el){
  if(c.company.slogan) el.textContent = c.company.slogan.toUpperCase();
});
console.log("[Config Inject] Applied CONFIG to DOM");
})();
</script>"""


class Handler(BaseHTTPRequestHandler):
    def get_session(self):
        c = self.headers.get("Cookie", "")
        for part in c.split(";"):
            part = part.strip()
            if part.startswith("uni="):
                tok = part[4:]
                if tok in SESSIONS: return tok
        return None

    def set_session(self, tok):
        self.send_header("Set-Cookie", "uni=%s; Path=/; HttpOnly; SameSite=Lax" % tok)

    def do_GET(self):
        p = urlparse(self.path).path
        try:
            if p == "/preview":
                html = read_v7()
                if html: html = self.inject_config(html)
                self.rhtml(html or "<h1>v7 not found</h1>"); return
            if p == "/login":
                self.rhtml(LOGIN_HTML); return
            tok = self.get_session()
            if not tok: self.redirect("/login"); return
            if p == "/api/config":
                self.rjson(load_cfg())
            elif p == "/api/bookings":
                self.rjson(load_bookings())
            elif p == "/admin":
                cfg = load_cfg()
                self.rhtml(generate_admin_page(cfg))
            elif p == "/":
                self.redirect("/admin")
            else:
                self.rstatic(p)
        except Exception as e:
            print(traceback.format_exc())
            self.rerr(500, str(e))

    def do_POST(self):
        p = urlparse(self.path).path
        try:
            if p == "/api/login":
                n = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(n).decode("utf-8"))
                if data.get("username") == ADMIN_USER and data.get("password") == ADMIN_PASS:
                    tok = secrets.token_hex(32)
                    SESSIONS[tok] = data["username"]
                    self.send_response(200)
                    self.set_session(tok)
                    self.end_headers()
                    self.wfile.write(json.dumps({"success":True}).encode("utf-8"))
                else:
                    self.rjson({"success":False,"message":"用户名或密码错误"})
                return
            tok = self.get_session()
            if not tok: self.rjson({"success":False,"message":"未登录"}); return
            if p == "/api/save_all":
                n = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(n).decode("utf-8"))
                save_cfg(data)
                self.rjson({"success":True,"message":"保存成功"})
            elif p == "/api/booking/update":
                n = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(n).decode("utf-8"))
                bk = load_bookings()
                for b in bk:
                    if b.get("id") == data.get("id"):
                        b["status"] = data.get("status","done")
                        b["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        break
                save_bookings(bk)
                self.rjson({"success":True})
            elif p == "/api/booking/del":
                n = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(n).decode("utf-8"))
                save_bookings([b for b in load_bookings() if b.get("id") != data.get("id")])
                self.rjson({"success":True})
            elif p == "/api/publish":
                self.rjson(self.publish_to_github())
            else:
                self.rjson({"success":False,"message":"unknown"})
        except Exception as e:
            print(traceback.format_exc())
            self.rjson({"success":False,"message":str(e)})

    def inject_config(self, html):
        cfg = load_cfg()
        js = json.dumps(cfg, ensure_ascii=False, indent=2)
        marker = "const CONFIG = "
        idx = html.find(marker)
        if idx == -1: return html
        b = html.find("{", idx)
        if b == -1: return html
        d = 0; e = b
        for i in range(b, len(html)):
            if html[i] == "{": d += 1
            elif html[i] == "}": d -= 1
            if d == 0: e = i+1; break
        if d != 0: return html
        new_html = html[:idx] + "const CONFIG = %s;" % js + html[e:]

        # 替换 DETAIL_CONTENT（弹窗详情数据）
        dc = cfg.get("detailContent", {})
        if dc:
            dc_js = json.dumps(dc, ensure_ascii=False, indent=2)
            # v8 模板中的 marker 格式是 "const DETAIL_CONTENT={" (无空格)
            dc_marker = "const DETAIL_CONTENT={"
            dc_idx = new_html.find(dc_marker)
            if dc_idx < 0:
                dc_marker = "const DETAIL_CONTENT = "
                dc_idx = new_html.find(dc_marker)
            if dc_idx >= 0:
                dc_b = new_html.find("{", dc_idx)
                if dc_b >= 0:
                    dc_d = 0; dc_e = dc_b
                    for i in range(dc_b, len(new_html)):
                        if new_html[i] == "{": dc_d += 1
                        elif new_html[i] == "}": dc_d -= 1
                        if dc_d == 0: dc_e = i+1; break
                    if dc_d == 0:
                        new_html = new_html[:dc_idx] + "const DETAIL_CONTENT = %s;" % dc_js + new_html[dc_e:]

        new_html = new_html.replace("</body>", INJECT_SCRIPT + "</body>")
        
        # Replace hardcoded ICP text in HTML (footer display)
        icp_val = cfg.get("company", {}).get("icp", "")
        if icp_val:
            # Replace patterns like: <span>粤ICP备XXXXXXXX号</span> or 粤ICP备XXXXXXXX号
            new_html = re.sub(
                r'(<[^>]*>)?粤ICP备[^<\s]*号(</[^>]*>)?',
                lambda m: (m.group(1) or "") + icp_val + (m.group(2) or ""),
                new_html
            )
        
        # Replace process step titles and descriptions (hardcoded in v7 HTML)
        process_items = cfg.get("process", [])
        # v7 has 4 steps: 需求诊断, 尽职调研, 落地执行, 持续运营 (old titles)
        old_titles = ["需求诊断", "尽职调研", "落地执行", "持续运营"]
        for i, old_title in enumerate(old_titles):
            if i < len(process_items):
                new_title = process_items[i].get("title", old_title)
                if new_title and new_title != old_title:
                    # Replace in HTML - be careful to only replace in process section
                    # Use a simple string replace for now
                    new_html = new_html.replace(
                        '>%s<' % old_title,
                        '>%s<' % new_title
                    )
        
        return new_html

    def rhtml(self, b):
        self.send_response(200)
        self.send_header("Content-Type","text/html; charset=utf-8")
        self.end_headers()
        if isinstance(b, str): b = b.encode("utf-8")
        self.wfile.write(b)

    def rjson(self, d):
        self.send_response(200)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        self.wfile.write(json.dumps(d, ensure_ascii=False).encode("utf-8"))

    def redirect(self, l):
        self.send_response(302); self.send_header("Location",l); self.end_headers()

    def rerr(self, c, m):
        self.send_response(c); self.send_header("Content-Type","text/plain; charset=utf-8")
        self.end_headers(); self.wfile.write(("Error %d: %s" % (c,m)).encode("utf-8"))

    def rstatic(self, p):
        local = os.path.join(WORKSPACE, p.lstrip("/"))
        if not os.path.isfile(local): return self.rerr(404,"Not found")
        ext = os.path.splitext(local)[1].lower()
        mt = {".png":"image/png",".jpg":"image/jpeg",".jpeg":"image/jpeg",".gif":"image/gif",".webp":"image/webp",".svg":"image/svg+xml"}
        with open(local,"rb") as f: data=f.read()
        self.send_response(200)
        self.send_header("Content-Type",mt.get(ext,"application/octet-stream"))
        self.end_headers(); self.wfile.write(data)

    def log_message(self,*a): pass

    def publish_to_github(self):
        import subprocess, re as _re
        try:
            cfg = load_cfg()
            # 用当前cfg注入v8模板 → 生成最新index.html
            v8_path = os.path.join(WORKSPACE, "index_v8.html")
            if not os.path.isfile(v8_path):
                return {"success":False,"message":"v8模板不存在"}
            with open(v8_path, "r", encoding="utf-8") as f:
                html = f.read()
            
            js = json.dumps(cfg, ensure_ascii=False, indent=2)
            marker = "const CONFIG = "
            idx = html.find(marker)
            if idx >= 0:
                b = html.find("{", idx)
                if b >= 0:
                    d = 0; e = b
                    for i in range(b, len(html)):
                        if html[i] == "{": d += 1
                        elif html[i] == "}": d -= 1
                        if d == 0: e = i+1; break
                    if d == 0:
                        html = html[:idx] + "const CONFIG = %s;" % js + html[e:]
            
            dc = cfg.get("detailContent", {})
            if dc:
                # 自动注入 heroImg 到 content 顶部（如果不重复）
                for _k, _v in dc.items():
                    if not isinstance(_v, dict):
                        continue
                    _hero = (_v.get("heroImg") or "").strip()
                    if not _hero:
                        continue
                    _content = _v.get("content") or ""
                    # 检查 content 里是否已有这张图的 src
                    if _hero in _content:
                        continue
                    # 在 content 开头插入 heroImg 图（保留原内容）
                    _img_html = '<div class="detail-hero"><img src="%s" alt="%s" style="width:100%%;max-height:380px;object-fit:cover;display:block;"></div>' % (
                        _hero, (_v.get("title") or _k).replace('"', '&quot;')
                    )
                    _v["content"] = _img_html + _content
                dc_js = json.dumps(dc, ensure_ascii=False, indent=2)
                # v8 模板中的 marker 格式是 "const DETAIL_CONTENT={" (无空格)
                dc_marker = "const DETAIL_CONTENT={"
                dc_idx = html.find(dc_marker)
                if dc_idx < 0:
                    dc_marker = "const DETAIL_CONTENT = "
                    dc_idx = html.find(dc_marker)
                if dc_idx >= 0:
                    dc_b = html.find("{", dc_idx)
                    if dc_b >= 0:
                        dc_d = 0; dc_e = dc_b
                        for i in range(dc_b, len(html)):
                            if html[i] == "{": dc_d += 1
                            elif html[i] == "}": dc_d -= 1
                            if dc_d == 0: dc_e = i+1; break
                        if dc_d == 0:
                            html = html[:dc_idx] + "const DETAIL_CONTENT = %s;" % dc_js + html[dc_e:]
            
            icp_val = cfg.get("company", {}).get("icp", "")
            if icp_val:
                html = _re.sub(
                    r'(<[^>]*>)?粤ICP备[^<\s]*号(</[^>]*>)?',
                    lambda m: (m.group(1) or "") + icp_val + (m.group(2) or ""),
                    html
                )
            
            with open(os.path.join(WORKSPACE,"index.html"),"w",encoding="utf-8") as f:
                f.write(html)
            
            ge = r"E:\腾讯龙虾\QClaw\v0.2.30.594\resources\git\cmd\git.exe"
            if not os.path.isfile(ge): ge="git"
            e=os.environ.copy(); e["GIT_ASKPASS"]="echo"; e["GIT_TERMINAL_PROMPT"]="0"
            # 工作流：本地 master → fetch远程main → rebase → push master:main（Pages构建）→ push master:master（同步）
            subprocess.run([ge,"add","index.html","site_config.json"],cwd=WORKSPACE,capture_output=True,text=True,encoding="utf-8",env=e)
            subprocess.run([ge,"commit","-m","u-%s"%datetime.now().strftime("%H%M")],cwd=WORKSPACE,capture_output=True,text=True,encoding="utf-8",env=e)
            subprocess.run([ge,"fetch","origin"],cwd=WORKSPACE,capture_output=True,text=True,encoding="utf-8",env=e)
            pr=subprocess.run([ge,"rebase","origin/main"],cwd=WORKSPACE,capture_output=True,text=True,encoding="utf-8",env=e)
            r=subprocess.run([ge,"push","origin","master:main"],cwd=WORKSPACE,capture_output=True,text=True,encoding="utf-8",env=e)
            if r.returncode!=0:
                return {"success":False,"message":"push master:main 失败: %s"%r.stderr[:200]}
            subprocess.run([ge,"push","origin","master:master"],cwd=WORKSPACE,capture_output=True,text=True,encoding="utf-8",env=e)
            return {"success":True,"message":"已发布到 GitHub Pages"}
        except Exception as e: return {"success":False,"message":str(e)}


def main():
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()

if __name__ == "__main__":
    print("\n  统一后台 v3 | http://localhost:%d/admin | %s/%s\n" % (PORT, ADMIN_USER, ADMIN_PASS))
    main()
