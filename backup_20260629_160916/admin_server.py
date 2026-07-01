#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 丝路山海通 可视化后台 v3 — 独立运行，不改 v7
import json, os, re, shutil, traceback, sys, secrets
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

WORKSPACE = os.path.dirname(os.path.abspath(__file__))

# 登录配置
ADMIN_USER = "jackleework"
ADMIN_PASS = "999999"
SESSIONS = {}  # token -> username
V7_FILE = os.path.join(WORKSPACE, "silkroad-trade_v7_silk_poster.html")
V6_FILE = os.path.join(WORKSPACE, "silkroad-trade_v6_silk_poster.html")
CFG_FILE = os.path.join(WORKSPACE, "site_config.json")
PORT = 8080

DEFAULT = {
    "company": {
        "name": "丝路山海通",
        "slogan": "一带一路企业出海一站式服务",
        "email": "outlook@silkroad-trade.com",
        "phone": "400-xxx-xxxx",
        "icp": "粤ICP备XXXXXXXX号",
        "wechatId": "SilkRoadTrade",
        "wechatQR": ""
    },
    "slides": [
        {"id":"slide-1","title":"乘丝路长风通达全球","subtitle":"一带一路企业出海一站式服务","desc":"丝路山海通 — 响应国家一带一路倡议，为企业出海提供公司注册、财税支持、产品准入、本地化运营等一站式落地服务。","img":"https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&q=80","detailId":"company-advantage"},
        {"id":"slide-2","title":"公司注册资质办理","subtitle":"最快7个工作日完成海外公司设立","desc":"境内境外公司注册、营业执照激活、行业资质证照办理，让您的企业快速合法落地海外。","img":"https://images.unsplash.com/photo-1560179707-f14e90ef3623?w=800&q=80","detailId":"company-reg"}
    ],
    "services": [
        {"id":"company-reg","title":"公司注册与资质","sub":"incorporation & licensing","desc":"境外公司注册、营业执照激活、行业资质证照办理","icon":"\U0001f3e2","detailId":"company-reg"},
        {"id":"product-cert","title":"产品准入与认证","sub":"product certification","desc":"SNI/BPOM/清真认证一站式办理","icon":"\u2705","detailId":"certification"},
        {"id":"tax-legal","title":"财税人事与法务","sub":"tax, hr & legal","desc":"财税筹划、代理记账、法务咨询一站式","icon":"\U0001f4ca","detailId":"tax-legal"},
        {"id":"local-ops","title":"本地化运营支持","sub":"local operation","desc":"行政办公、本地招聘、政府关系、资源对接","icon":"\U0001f310","detailId":"local-ops"},
        {"id":"visa","title":"签证考察与出行","sub":"visa & business travel","desc":"商务签证、工作签证、工厂考察一站式","icon":"\u2708\ufe0f","detailId":"visa"},
        {"id":"factory","title":"建厂工程与投产","sub":"factory & construction","desc":"海外建厂选址、工程许可、环境合规","icon":"\U0001f3ed","detailId":"factory"}
    ],
    "stats": [
        {"num":"60+","label":"一带一路覆盖国家"},
        {"num":"1,600+","label":"服务出海企业"},
        {"num":"400+","label":"海外本地员工"},
        {"num":"5+","label":"区域服务网络"}
    ],
    "policies": [
        {"num":"01","title":"政策研究与解读","desc":"60+国家政策数据库，专业团队实时追踪政策动态"},
        {"num":"02","title":"政府与商会对接","desc":"深耕本地政商关系，搭建企业与当地政府沟通桥梁"},
        {"num":"03","title":"产业园区落地","desc":"对接一带一路沿线重点产业园区，享优惠政策"},
        {"num":"04","title":"投融资对接","desc":"串联政策性金融机构与商业资本，多路径融资通道"}
    ],
    "testimonials": [
        {"name":"张宏伟","role":"新能源汽车 印尼工厂负责人","text":"帮我们在雅加达完成了公司注册和工厂选址，从考察到落地只用了2个月。","avatar":"张"},
        {"name":"李雪峰","role":"工程机械 中亚事业部总经理","text":"响应一带一路开拓中亚市场，从法律合规到政府关系一路护航。","avatar":"李"},
        {"name":"王琳","role":"食品饮料 海外拓展总监","text":"印尼的SNI认证和清真认证一站式包办，产品准入周期缩短了60%。","avatar":"王"}
    ],
    "process": [
        {"num":"01","title":"需求诊断","desc":"深入了解企业出海目标与需求，定制化出海方案。"},
        {"num":"02","title":"尽职调研","desc":"市场调研、法律评估、财税分析，规避风险前置。"},
        {"num":"03","title":"落地执行","desc":"公司注册、资质办理、团队搭建，全程陪伴推进。"},
        {"num":"04","title":"持续运营","desc":"财税代账、法务支持、政府维护，长期运营保障。"}
    ]
}

# ========== 追踪日志系统 ==========
TRACE_LOG = []
TRACE_MAX = 200

def trace(msg, data=None):
    """输出追踪信息到控制台并缓存到 TRACE_LOG"""
    import datetime
    ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    line = f"[{ts}] {msg}"
    if data is not None:
        if isinstance(data, str):
            line += f"\n  -> {data[:300]}"
        elif isinstance(data, (list, dict)):
            import json
            line += f"\n  -> {json.dumps(data, ensure_ascii=False)[:500]}"
    print(line)
    TRACE_LOG.append(line)
    if len(TRACE_LOG) > TRACE_MAX:
        TRACE_LOG[:50] = []

def trace_section(title):
    """输出分段标题"""
    bar = "=" * 50
    print(f"\n{bar}")
    print(f"  {title}")
    print(f"{bar}")
    TRACE_LOG.append(f"\n--- {title} ---")

def load_cfg():
    if os.path.isfile(CFG_FILE):
        with open(CFG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    save_cfg(DEFAULT)
    return dict(DEFAULT)

def save_cfg(data):
    with open(CFG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


ADMIN = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>丝路山海通 · 后台管理</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,"Segoe UI",sans-serif}
body{background:#f5f0ea;color:#1a1512;display:flex;min-height:100vh}
.side{width:200px;background:#302824;padding:1.5rem 0;flex-shrink:0;height:100vh;position:sticky;top:0;overflow-y:auto}
.side h2{color:#f0d68a;font-size:.85rem;padding:0 1.2rem;margin-bottom:1rem;letter-spacing:.05em}
.side a{display:block;padding:.6rem 1.2rem;color:#a89e96;text-decoration:none;font-size:.82rem;transition:.2s;border-left:3px solid transparent;cursor:pointer}
.side a:hover,.side a.on{color:#fff;background:rgba(255,255,255,.05);border-left-color:#c44536}
.main{flex:1;padding:2rem;max-width:1100px}
h1{font-size:1.4rem;color:#c44536;margin-bottom:.2rem}
.sub{color:#6b625c;font-size:.82rem;margin-bottom:1.5rem}
.toolbar{display:flex;gap:.5rem;margin-bottom:1rem;flex-wrap:wrap}
.btn{padding:.5rem 1.2rem;border-radius:4px;font-size:.82rem;font-weight:600;cursor:pointer;border:none;transition:.2s}
.btn-g{background:#2d8a4e;color:#fff}.btn-g:hover{background:#1e6b37}
.btn-o{background:transparent;border:1px solid #c8c0b8;color:#1a1512}.btn-o:hover{border-color:#c44536;color:#c44536}
.msg{padding:.6rem 1rem;border-radius:4px;margin-bottom:1rem;display:none;font-size:.85rem}
.msg.ok{display:block;background:#e8f5e9;color:#1e6b37;border:1px solid #a5d6a7}
.msg.er{display:block;background:#fce4ec;color:#c62828;border:1px solid #ef9a9a}
.card{border:1px solid #c8c0b8;border-radius:6px;padding:1rem;margin-bottom:.8rem;background:#fff}
.card-h{display:flex;justify-content:space-between;align-items:center;margin-bottom:.6rem;flex-wrap:wrap}
.card-h h3{font-size:.88rem}
.tp{display:none}.tp.on{display:block}
.fg{margin-bottom:.6rem}
.fg label{display:block;font-size:.78rem;font-weight:600;margin-bottom:.2rem;color:#6b625c}
.fg input,.fg textarea{width:100%;padding:.4rem .5rem;border:1px solid #c8c0b8;border-radius:4px;font-size:.82rem;background:#fff;font-family:inherit}
.fg textarea{min-height:40px;resize:vertical;font-size:.78rem}
.fg input:focus,.fg textarea:focus{outline:none;border-color:#c44536;box-shadow:0 0 0 2px rgba(196,69,54,.1)}
.p2{display:grid;grid-template-columns:1fr 1fr;gap:.3rem}
.ab{background:#eee;border:none;border-radius:4px;padding:.15rem .4rem;cursor:pointer;font-size:.7rem;color:#666}
.ab:hover{background:#c44536;color:#fff}
.ib{border:1px solid #eee;border-radius:4px;padding:.5rem;margin-bottom:.5rem}
.ib-h{display:flex;justify-content:space-between;margin-bottom:.3rem}
.ib-h strong{font-size:.82rem}
.ip{max-width:100px;max-height:60px;margin-top:.2rem;border-radius:4px;border:1px solid #eee;display:block}
.ht{font-size:.74rem;color:#a89e96;margin-top:.15rem}
.em{color:#999;font-size:.8rem;padding:.5rem 0}
.il{display:flex;gap:.3rem;margin-bottom:.3rem;align-items:center}
.fo{text-align:center;padding:2rem 0;color:#a89e96;font-size:.75rem;line-height:1.6}
@media(max-width:768px){.side{display:none}}
</style></head><body>
<div class="side">
<h2>后台管理器</h2>
<a class="on" onclick="sw('cp',this)">公司信息</a>
<a onclick="sw('sl',this)">轮播图</a>
<a onclick="sw('sv',this)">服务卡片</a>
<a onclick="sw('st',this)">统计数字</a>
<a onclick="sw('po',this)">政策卡片</a>
<a onclick="sw('te',this)">客户案例</a>
<a onclick="sw('pr',this)">服务流程</a>
<a onclick="sw('di',this)" style="margin-top:1rem;border-left-color:#2d8a4e;color:#a8c8a0">诊断工具</a>
</div>
<div class="main">
<h1>丝路山海通 · 后台管理</h1>
<div class="sub">不改 v7 代码 | 填好内容点保存 | 预览页看效果</div>
<div id="msg" class="msg"></div>
<div class="toolbar">
<button class="btn btn-g" onclick="svAll()" id="sb">保存全部</button>
<button class="btn btn-o" onclick="window.open('/preview','_blank')">预览</button>
<button class="btn btn-o" onclick="publishToGitHub()" id="pubBtn" style="background:#24292e;color:#fff;border-color:#24292e">📤 发布到 GitHub</button>
</div>
<div class="tp on" id="tp_cp"></div>
<div class="tp" id="tp_sl"></div>
<div class="tp" id="tp_sv"></div>
<div class="tp" id="tp_st"></div>
<div class="tp" id="tp_po"></div>
<div class="tp" id="tp_te"></div>
<div class="tp" id="tp_pr"></div>
<div class="tp" id="tp_di">
  <div class="card">
    <div class="card-h"><h3>🔍 诊断工具</h3></div>
    <p style="font-size:.82rem;color:#6b625c;margin-bottom:1rem">检查 v7 文件结构完整性，查看 CONFIG 块和各个板块是否能被正常识别。</p>
    <div style="display:flex;gap:.5rem;flex-wrap:wrap">
      <button class="btn btn-g" onclick="runDiag()">运行诊断</button>
      <button class="btn btn-o" onclick="viewTrace()">查看追踪日志</button>
      <button class="btn btn-o" onclick="clearTrace()">清空日志</button>
    </div>
    <div id="diagResult" style="margin-top:1rem;font-size:.82rem"></div>
    <div id="traceResult" style="margin-top:1rem;font-size:.78rem;display:none">
      <div class="card-h"><h3>📋 追踪日志</h3><button class="ab" onclick="document.getElementById('traceResult').style.display='none'">关闭</button></div>
      <pre id="traceContent" style="max-height:400px;overflow-y:auto;background:#f8f5f2;padding:.8rem;border-radius:4px;font-family:monospace;font-size:.72rem;line-height:1.6;white-space:pre-wrap"></pre>
    </div>
  </div>
</div>
<div class="fo"><a href="/preview" target="_blank">http://localhost:8080/preview</a></div>
</div>
<script>
var D={};
function g(id){return document.getElementById(id);}
function msg(t,c){var e=g('msg');e.textContent=t;e.className='msg '+c;e.style.display='block';}
function mhide(){g('msg').style.display='none';}
function es(s){if(!s)return '';return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function ip(u){return u?'<img class="ip" src="'+es(u)+'" onerror="this.style.display=\'none\'">':'';}
function sw(n,el){
  var as=document.querySelectorAll('.side a');
  for(var i=0;i<as.length;i++)as[i].classList.remove('on');
  var ts=document.querySelectorAll('.tp');
  for(var i=0;i<ts.length;i++)ts[i].classList.remove('on');
  el.classList.add('on');
  g('tp_'+n).classList.add('on');
}
function sp(k,v){
  var ks=k.split('.'),o=D;
  for(var i=0;i<ks.length-1;i++){if(!o[ks[i]])o[ks[i]]={};o=o[ks[i]];}
  o[ks[ks.length-1]]=v;
}
function arrAdd(k,obj){if(!D[k])D[k]=[];D[k].push(obj);}
function arrDel(k,i){D[k].splice(i,1);}
/* Label helpers */
var LB={'name':'公司名称','slogan':'副标题/标语','email':'联系邮箱','phone':'联系电话','icp':'备案号','wechatId':'微信号'};
function fIn(k,p,v){
  var label = LB[p] || p || k;
  if(label===k && k.indexOf('.')>0) label=k.split('.').pop();
  return '<div class="fg"><label>'+label+'</label><input value="'+es(v)+'" onchange="sp(\''+k+'\',this.value)"></div>';
}
function fImg(k,v){return '<div class="fg"><label>二维码链接</label><input value="'+es(v)+'" onchange="sp(\''+k+'\',this.value)">'+ip(v)+'<div class="ht">二维码上传图床后粘贴链接</div></div>';}

window.onload=function(){
  msg('加载中...','ok');
  var x=new XMLHttpRequest();
  x.open('GET','/api/config',true);
  x.onload=function(){
    if(x.status==200){D=JSON.parse(x.responseText);rAll();mhide();}
    else msg('加载失败: '+x.status,'er');
  };
  x.onerror=function(){msg('网络错误','er');};
  x.send();
};

function rAll(){rCp();rSl();rSv();rSt();rPo();rTe();rPr();}

function rCp(){
  var c=D.company||{},h='<div class="card">';
  h+=fIn('company.name','公司名称',c.name);
  h+=fIn('company.slogan','副标题/标语',c.slogan);
  h+=fIn('company.email','联系邮箱',c.email);
  h+=fIn('company.phone','联系电话',c.phone);
  h+=fIn('company.icp','备案号',c.icp);
  h+=fIn('company.wechatId','微信号',c.wechatId);
  h+=fImg('company.wechatQR',c.wechatQR);
  h+='</div>';
  g('tp_cp').innerHTML=h;
}

function rSl(){
  var a=D.slides||[],h='<div class="card"><div class="card-h"><h3>轮播图 ('+a.length+'张)</h3><button class="ab" onclick="arrAdd(\'slides\',{title:\'\',subtitle:\'\',desc:\'\',img:\'\',detailId:\'\'});rSl()">+添加</button></div>';
  for(var i=0;i<a.length;i++){
    h+='<div class="ib"><div class="ib-h"><strong>'+(i+1)+'</strong><button class="ab" onclick="arrDel(\'slides\','+i+');rSl()">删除</button></div>';
    h+='<div class="fg"><label>标题</label><input value="'+es(a[i].title)+'" onchange="D.slides['+i+'].title=this.value"></div>';
    h+='<div class="fg"><label>副标题</label><input value="'+es(a[i].subtitle)+'" onchange="D.slides['+i+'].subtitle=this.value"></div>';
    h+='<div class="fg"><label>描述</label><textarea rows="2" onchange="D.slides['+i+'].desc=this.value">'+es(a[i].desc)+'</textarea></div>';
    h+='<div class="fg"><label>图片链接</label><input value="'+es(a[i].img)+'" onchange="D.slides['+i+'].img=this.value">'+ip(a[i].img)+'</div></div>';
  }
  if(!a.length)h+='<div class="em">暂无</div>';
  g('tp_sl').innerHTML=h+'</div>';
}

function rSv(){
  var a=D.services||[],h='<div class="card"><div class="card-h"><h3>服务卡片 ('+a.length+'项)</h3></div>';
  for(var i=0;i<a.length;i++){
    h+='<div class="ib"><div class="ib-h"><strong>'+(i+1)+': '+es(a[i].title)+'</strong></div>';
    h+='<div class="fg"><label>标题</label><input value="'+es(a[i].title)+'" onchange="D.services['+i+'].title=this.value"></div>';
    h+='<div class="fg"><label>副标题</label><input value="'+es(a[i].sub)+'" onchange="D.services['+i+'].sub=this.value"></div>';
    h+='<div class="fg"><label>描述</label><textarea rows="2" onchange="D.services['+i+'].desc=this.value">'+es(a[i].desc)+'</textarea></div>';
    h+='<div class="fg"><label>图标(emoji)</label><input value="'+es(a[i].icon)+'" onchange="D.services['+i+'].icon=this.value"></div></div>';
  }
  g('tp_sv').innerHTML=h+'</div>';
}

function rSt(){
  var a=D.stats||[],h='<div class="card"><div class="card-h"><h3>统计数字</h3><button class="ab" onclick="arrAdd(\'stats\',{num:\'\',label:\'\'});rSt()">+添加</button></div>';
  for(var i=0;i<a.length;i++){
    h+='<div class="il"><input value="'+es(a[i].num)+'" placeholder="数字" style="width:80px" onchange="D.stats['+i+'].num=this.value">';
    h+='<input value="'+es(a[i].label)+'" placeholder="标签" style="flex:1" onchange="D.stats['+i+'].label=this.value">';
    h+='<button class="ab" onclick="arrDel(\'stats\','+i+');rSt()">删除</button></div>';
  }
  if(!a.length)h+='<div class="em">暂无</div>';
  g('tp_st').innerHTML=h+'</div>';
}

function rPo(){
  var a=D.policies||[],h='<div class="card"><div class="card-h"><h3>政策卡片</h3><button class="ab" onclick="arrAdd(\'policies\',{num:\'\',title:\'\',desc:\'\'});rPo()">+添加</button></div>';
  for(var i=0;i<a.length;i++){
    h+='<div class="ib"><div class="ib-h"><strong>'+(i+1)+'</strong><button class="ab" onclick="arrDel(\'policies\','+i+');rPo()">删除</button></div>';
    h+='<div class="fg"><label>编号</label><input value="'+es(a[i].num)+'" onchange="D.policies['+i+'].num=this.value"></div>';
    h+='<div class="fg"><label>标题</label><input value="'+es(a[i].title)+'" onchange="D.policies['+i+'].title=this.value"></div>';
    h+='<div class="fg"><label>描述</label><textarea rows="2" onchange="D.policies['+i+'].desc=this.value">'+es(a[i].desc)+'</textarea></div></div>';
  }
  g('tp_po').innerHTML=h+'</div>';
}

function rTe(){
  var a=D.testimonials||[],h='<div class="card"><div class="card-h"><h3>客户案例</h3><button class="ab" onclick="arrAdd(\'testimonials\',{name:\'\',role:\'\',text:\'\'});rTe()">+添加</button></div>';
  for(var i=0;i<a.length;i++){
    h+='<div class="ib"><div class="ib-h"><strong>'+(i+1)+': '+es(a[i].name)+'</strong><button class="ab" onclick="arrDel(\'testimonials\','+i+');rTe()">删除</button></div>';
    h+='<div class="fg"><label>姓名</label><input value="'+es(a[i].name)+'" onchange="D.testimonials['+i+'].name=this.value"></div>';
    h+='<div class="fg"><label>职位</label><input value="'+es(a[i].role)+'" onchange="D.testimonials['+i+'].role=this.value"></div>';
    h+='<div class="fg"><label>客户原话</label><textarea rows="2" onchange="D.testimonials['+i+'].text=this.value">'+es(a[i].text)+'</textarea></div></div>';
  }
  g('tp_te').innerHTML=h+'</div>';
}

function rPr(){
  var a=D.process||[],h='<div class="card"><div class="card-h"><h3>服务流程</h3><button class="ab" onclick="arrAdd(\'process\',{num:\'\',title:\'\',desc:\'\'});rPr()">+添加</button></div>';
  for(var i=0;i<a.length;i++){
    h+='<div class="ib"><div class="ib-h"><strong>'+(i+1)+'</strong><button class="ab" onclick="arrDel(\'process\','+i+');rPr()">删除</button></div>';
    h+='<div class="fg"><label>编号</label><input value="'+es(a[i].num)+'" onchange="D.process['+i+'].num=this.value"></div>';
    h+='<div class="fg"><label>标题</label><input value="'+es(a[i].title)+'" onchange="D.process['+i+'].title=this.value"></div>';
    h+='<div class="fg"><label>描述</label><textarea rows="2" onchange="D.process['+i+'].desc=this.value">'+es(a[i].desc)+'</textarea></div></div>';
  }
  g('tp_pr').innerHTML=h+'</div>';
}

// ========== 诊断工具 ==========
function runDiag(){
  var r=g('diagResult');r.innerHTML='<div style="color:#6b625c">⏳ 诊断中...</div>';
  var x=new XMLHttpRequest();
  x.open('GET','/api/diagnose',true);
  x.onload=function(){
    if(x.status!=200){r.innerHTML='<div class="msg er" style="display:block">诊断失败: '+x.status+'</div>';return;}
    var d=JSON.parse(x.responseText);
    var h='<div class="card-h" style="margin-top:.5rem"><h3>📊 诊断结果 '+(d.status=='ok'?'✅':'⚠️')+'</h3></div>';
    h+='<table style="width:100%;border-collapse:collapse;font-size:.78rem">';
    for(var i=0;i<d.checks.length;i++){
      var c=d.checks[i];
      h+='<tr><td style="padding:.4rem .6rem;border-bottom:1px solid #eee">'+(c.passed?'✅':'❌')+'</td>';
      h+='<td style="padding:.4rem .6rem;border-bottom:1px solid #eee;font-weight:600">'+es(c.name)+'</td>';
      h+='<td style="padding:.4rem .6rem;border-bottom:1px solid #eee;color:#6b625c">'+es(c.detail)+'</td></tr>';
    }
    h+='</table>';
    if(d.files){
      h+='<div style="margin-top:.8rem;font-size:.72rem;color:#6b625c">📁 文件: ';
      h+='v7='+(d.files.v7.exists ? d.files.v7.size.toLocaleString()+' bytes ✅' : '❌ 不存在')+', ';
      h+='v6='+(d.files.v6.exists ? d.files.v6.size.toLocaleString()+' bytes ✅' : '❌ 不存在');
      h+='</div>';
    }
    if(d.warnings&&d.warnings.length)h+='<div style="margin-top:.5rem;padding:.4rem .6rem;background:#fff3cd;border-radius:4px;font-size:.75rem">⚠️ '+es(d.warnings.join('; '))+'</div>';
    r.innerHTML=h;
  };
  x.onerror=function(){r.innerHTML='<div class="msg er" style="display:block">网络错误</div>';};
  x.send();
}

function viewTrace(){
  var t=g('traceResult');t.style.display='block';
  var c=g('traceContent');c.textContent='⏳ 加载中...';
  var x=new XMLHttpRequest();
  x.open('GET','/api/trace',true);
  x.onload=function(){
    if(x.status!=200){c.textContent='加载失败: '+x.status;return;}
    var d=JSON.parse(x.responseText);
    c.textContent=d.traces.length ? d.traces.join('\n') : '暂无追踪日志';
  };
  x.onerror=function(){c.textContent='网络错误';};
  x.send();
}

function clearTrace(){
  var x=new XMLHttpRequest();
  x.open('GET','/api/trace_clear',true);
  x.onload=function(){document.getElementById('traceResult').style.display='none';msg('追踪日志已清空','ok');setTimeout(mhide,2000);};
  x.send();
}

function svAll(){
  var b=g('sb');b.textContent='保存中...';b.disabled=true;msg('保存中...','ok');
  var x=new XMLHttpRequest();
  x.open('POST','/api/save_all',true);
  x.setRequestHeader('Content-Type','application/json');
  x.onload=function(){
    var d=JSON.parse(x.responseText);
    if(d.success){msg('保存成功!','ok');}else{msg('保存失败: '+d.message,'er');}
    b.textContent='保存全部';b.disabled=false;setTimeout(mhide,3000);
  };
  x.onerror=function(){msg('网络错误','er');b.textContent='保存全部';b.disabled=false;};
  x.send(JSON.stringify(D));
}

// ========== 发布到 GitHub ==========
function publishToGitHub(){
  var b=g('pubBtn');b.textContent='发布中...';b.disabled=true;msg('正在生成发布文件并推送到 GitHub...','ok');
  var x=new XMLHttpRequest();
  x.open('POST','/api/publish',true);
  x.setRequestHeader('Content-Type','application/json');
  x.onload=function(){
    var d=JSON.parse(x.responseText);
    if(d.success){
      msg('✅ 发布成功! GitHub Pages 将在 1-2 分钟后更新','ok');
      if(d.url){
        setTimeout(function(){
          if(confirm('发布成功! 是否打开 GitHub 查看?')){
            window.open(d.url,'_blank');
          }
        },500);
      }
    }else{
      msg('❌ 发布失败: '+d.message,'er');
    }
    b.textContent='📤 发布到 GitHub';b.disabled=false;setTimeout(mhide,5000);
  };
  x.onerror=function(){msg('网络错误','er');b.textContent='📤 发布到 GitHub';b.disabled=false;};
  x.send(JSON.stringify(D));
}
</script></body></html>"""

# The inject script used by inject_config() to update v7 preview with CONFIG data
INJECT_SCRIPT = """
<script>
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
  if(txt.indexOf("\\u00a9") >= 0 || txt.indexOf("All rights") >= 0) {
    el.textContent = "\\u00a9 " + new Date().getFullYear() + " " + c.company.name + ". All rights reserved.";
  }
  if(txt.indexOf("ICP") >= 0 || txt.indexOf("\\u7ca4") >= 0) {
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
  var ems = ["\\ud83c\\udfed","\\ud83d\\udccb","\\u2696\\ufe0f","\\ud83d\\udee1\\ufe0f","\\ud83c\\udf10","\\ud83d\\udee2\\ufe0f"];
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
    var av = t.avatar || (t.name ? t.name.charAt(0) : "\\ud83d\\udc64");
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

LOGIN_PAGE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>管理后台登录 · 丝路山海通</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,"Segoe UI",sans-serif}
body{background:url(/login_bg.jpg) center/cover no-repeat;display:flex;justify-content:center;align-items:center;min-height:100vh;position:relative}
body::before{content:"";position:fixed;inset:0;background:linear-gradient(135deg,rgba(245,240,234,.85) 0%,rgba(48,40,36,.4) 100%);z-index:0}
.l-box{position:relative;z-index:1;background:rgba(255,255,255,.95);backdrop-filter:blur(10px);border-radius:12px;padding:2.5rem;width:360px;box-shadow:0 8px 32px rgba(48,40,36,.15);text-align:center;border:1px solid rgba(255,255,255,.3)}
.l-box h1{font-size:1.2rem;color:#302824;margin-bottom:.3rem}
.l-box p{font-size:.8rem;color:#a89e96;margin-bottom:1.5rem}
.fg{margin-bottom:.8rem;text-align:left}
.fg label{display:block;font-size:.78rem;font-weight:600;margin-bottom:.2rem;color:#6b625c}
.fg input{width:100%;padding:.45rem .5rem;border:1px solid #c8c0b8;border-radius:4px;font-size:.85rem;background:#fff}
.fg input:focus{outline:none;border-color:#c44536;box-shadow:0 0 0 2px rgba(196,69,54,.1)}
.btn{padding:.5rem 1.2rem;border-radius:4px;font-size:.85rem;font-weight:600;cursor:pointer;border:none;transition:.2s;width:100%}
.btn-g{background:#2d8a4e;color:#fff}.btn-g:hover{background:#1e6b37}
.msg{padding:.5rem .8rem;border-radius:4px;margin-bottom:1rem;font-size:.8rem;display:none}
.msg.er{display:block;background:#fce4ec;color:#c62828;border:1px solid #ef9a9a}
.fo{font-size:.72rem;color:#a89e96;margin-top:1.5rem}
.err{border-color:#c62828!important}
</style>
</head><body>
<div class="l-box">
<h1>丝路山海通</h1>
<p>管理后台登录</p>
<div id="msg" class="msg"></div>
<div class="fg"><label>用户名</label><input id="user" type="text" autocomplete="username" autofocus></div>
<div class="fg"><label>密码</label><input id="pass" type="password" autocomplete="current-password"></div>
<button class="btn btn-g" onclick="login()">登 录</button>
<div class="fo">后台管理系统</div>
</div>
<script>
function login(){
  var u=document.getElementById('user'),p=document.getElementById('pass'),m=document.getElementById('msg');
  u.classList.remove('err');p.classList.remove('err');m.style.display='none';
  if(!u.value){u.classList.add('err');u.focus();m.textContent='请输入用户名';m.className='msg er';return;}
  if(!p.value){p.classList.add('err');p.focus();m.textContent='请输入密码';m.className='msg er';return;}
  var x=new XMLHttpRequest();
  x.open('POST','/api/login',true);
  x.setRequestHeader('Content-Type','application/json');
  x.onload=function(){
    if(x.status==200){window.location.href='/admin';}
    else{var r=JSON.parse(x.responseText);m.textContent=r.message||'登录失败';m.className='msg er';}
  };
  x.onerror=function(){m.textContent='网络错误';m.className='msg er';};
  x.send(JSON.stringify({username:u.value,password:p.value}));
}
document.getElementById('user').addEventListener('keydown',function(e){if(e.key=='Enter')document.getElementById('pass').focus();});
document.getElementById('pass').addEventListener('keydown',function(e){if(e.key=='Enter')login();});
</script>
</body></html>"""

class Handler(BaseHTTPRequestHandler):
    def get_session(self):
        c = self.headers.get("Cookie", "")
        for part in c.split(";"):
            part = part.strip()
            if part.startswith("admin_token="):
                tok = part[12:]
                if tok in SESSIONS:
                    return tok
        return None

    def set_session(self, tok):
        self.send_header("Set-Cookie", f"admin_token={tok}; Path=/; HttpOnly; SameSite=Lax")

    def clear_session(self):
        self.send_header("Set-Cookie", "admin_token=; Path=/; Max-Age=0; HttpOnly")

    def do_GET(self):
        p = urlparse(self.path).path
        try:
            # 公开路由：预览页无需登录
            if p == "/preview":
                html = self.read_v7()
                if html and html != "<h1>v7 not found</h1>":
                    html = self.inject_config(html)
                self.rhtml(html)
                return
            # 登录页及登录页资源（公开）
            if p == "/login":
                self.rhtml(LOGIN_PAGE)
                return
            if p == "/login_bg.jpg":
                self.rstatic(p)
                return
            # 以下路由需要登录
            tok = self.get_session()
            if not tok:
                self.redirect("/login")
                return
            if p == "/api/config":
                self.rjson(load_cfg())
            elif p == "/api/diagnose":
                self.rjson(self.diagnose())
            elif p == "/api/trace":
                self.rjson({"traces": list(TRACE_LOG)})
            elif p == "/api/trace_clear":
                TRACE_LOG.clear()
                self.rjson({"success": True})
            elif p in ("/admin", "/manager"):
                self.rhtml(ADMIN)
            elif p == "/" or p == "":
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
                u = data.get("username", "")
                pw = data.get("password", "")
                if u == ADMIN_USER and pw == ADMIN_PASS:
                    tok = secrets.token_hex(32)
                    SESSIONS[tok] = u
                    self.send_response(200)
                    self.set_session(tok)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
                else:
                    self.rjson({"success": False, "message": "用户名或密码错误"})
                return
            if p == "/api/logout":
                tok = self.get_session()
                if tok:
                    SESSIONS.pop(tok, None)
                self.send_response(200)
                self.clear_session()
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
                return
            # 以下 API 需要登录
            tok = self.get_session()
            if not tok:
                self.rjson({"success": False, "message": "未登录"})
                return
            if p == "/api/save_all":
                n = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(n).decode("utf-8"))
                save_cfg(data)
                self.rjson({"success": True, "message": "配置已保存"})
            elif p == "/api/publish":
                result = self.publish_to_github()
                self.rjson(result)
            else:
                self.rjson({"success": False, "message": "unknown"})
        except Exception as e:
            self.rjson({"success": False, "message": str(e)})

    def read_v7(self):
        trace_section("read_v7: 读取 HTML")
        if not os.path.isfile(V7_FILE) or os.path.getsize(V7_FILE) < 100:
            trace(f"v7 不存在或太小, 尝试从 v6 复制")
            if os.path.isfile(V6_FILE):
                trace(f"从 v6 复制到 v7: {os.path.getsize(V6_FILE)} bytes")
                shutil.copy2(V6_FILE, V7_FILE)
                trace("复制完成")
        if os.path.isfile(V7_FILE):
            size = os.path.getsize(V7_FILE)
            with open(V7_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            trace(f"v7 HTML 读取成功: {size:,} bytes, {len(content):,} 字符")
            return content
        trace("❌ v7 文件不存在")
        return None

    def to_js(self, val, indent=2):
        return json.dumps(val, ensure_ascii=False, indent=indent)

    def inject_config(self, html):
        trace_section("inject_config: 注入配置")
        cfg = load_cfg()
        trace(f"配置加载: {len(cfg.get('slides',[]))} 张轮播, {len(cfg.get('services',[]))} 项服务, {len(cfg.get('stats',[]))} 项统计")
        js_config = self.to_js(cfg)
        trace(f"JS 配置序列化: {len(js_config):,} 字符")
        
        # 用花括号匹配找 CONFIG 块，而非简单正则
        marker = "const CONFIG = "
        idx = html.find(marker)
        if idx == -1:
            trace("⚠️ 未在 v7 HTML 中找到 'const CONFIG = ' 标记！")
            return html
        
        brace_idx = html.find("{", idx)
        if brace_idx == -1:
            trace("⚠️ 找到标记但找不到 '{'")
            return html
        
        # 花括号深度计数，找到匹配的 };
        depth = 0
        end = brace_idx
        for i in range(brace_idx, len(html)):
            if html[i] == "{":
                depth += 1
            elif html[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    # 跳过可能的分号
                    while end < len(html) and html[end] in " \t\n\r":
                        end += 1
                    if end < len(html) and html[end] == ";":
                        end += 1
                    break
        
        if depth != 0:
            trace("⚠️ 花括号不匹配，无法找到 CONFIG 结束")
            return html
        
        # 替换 CONFIG 块
        new_html = html[:idx] + f"const CONFIG = {js_config};" + html[end:]
        old_len = end - idx
        trace(f"✅ CONFIG 块替换成功: 旧={old_len}字符 → 新={len(js_config)+len('const CONFIG = ;')}字符")
        
        new_html = new_html.replace("</body>", INJECT_SCRIPT + "</body>")
        trace("✅ INJECT_SCRIPT 注入成功")
        return new_html

    def rhtml(self, body):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.wfile.write(body)

    def rjson(self, d):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(d, ensure_ascii=False).encode("utf-8"))

    def redirect(self, loc):
        self.send_response(302)
        self.send_header("Location", loc)
        self.end_headers()

    def rerr(self, code, msg):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"Error {code}: {msg}".encode("utf-8"))

    def rstatic(self, p):
        local = os.path.join(WORKSPACE, p.lstrip("/"))
        if not os.path.isfile(local):
            return self.rerr(404, "Not found")
        ext = os.path.splitext(local)[1].lower()
        mt = {".png":"image/png",".jpg":"image/jpeg",".jpeg":"image/jpeg",".gif":"image/gif",".webp":"image/webp",".svg":"image/svg+xml"}
        ct = mt.get(ext, "application/octet-stream")
        with open(local, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ct)
        self.send_header("Cache-Control", "max-age=3600")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        print(f"[{args[0]}] {args[1]} {args[2]}")


    def publish_to_github(self):
        """生成 index.html 并推送到 GitHub"""
        import subprocess
        from datetime import datetime
        
        trace_section("PUBLISH: 发布到 GitHub")
        
        try:
            # 1. 读取 v7 HTML
            html = self.read_v7()
            if not html or html == "<h1>v7 not found</h1>":
                return {"success": False, "message": "v7 HTML 文件不存在"}
            
            # 2. 注入最新配置（生成静态 HTML）
            trace("注入最新配置到 HTML...")
            publish_html = self.inject_config(html)
            
            # 3. 保存为 index.html（GitHub Pages 默认入口）
            index_path = os.path.join(WORKSPACE, "index.html")
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(publish_html)
            trace(f"✅ index.html 生成成功: {len(publish_html):,} 字符")
            
            # 4. 执行 git 命令推送
            trace("执行 git 推送...")
            git_exe = r"E:\腾讯龙虾\QClaw\v0.2.29.592\resources\git\cmd\git.exe"
            trace(f"使用 git: {git_exe}")
            env = os.environ.copy()
            env["GIT_ASKPASS"] = "echo"
            env["GIT_TERMINAL_PROMPT"] = "0"
            
            # git add
            result = subprocess.run(
                [git_exe, "add", "index.html", "site_config.json"],
                cwd=WORKSPACE,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=env
            )
            if result.returncode != 0:
                trace(f"⚠️ git add 警告: {result.stderr}")
            
            # git commit
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_msg = f"Update website content - {timestamp}"
            result = subprocess.run(
                [git_exe, "commit", "-m", commit_msg],
                cwd=WORKSPACE,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=env
            )
            if result.returncode != 0:
                # 可能是没有变化
                if "nothing to commit" in result.stdout.lower() or "nothing to commit" in result.stderr.lower():
                    trace("没有变化需要提交")
                else:
                    trace(f"⚠️ git commit 警告: {result.stderr}")
            else:
                trace(f"✅ git commit: {commit_msg}")
            
            # git pull first (to avoid "fetch first" error)
            trace("先拉取远程最新代码...")
            result = subprocess.run(
                [git_exe, "pull", "origin", "master", "--rebase"],
                cwd=WORKSPACE,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=env
            )
            if result.returncode != 0:
                trace(f"⚠️ git pull 警告: {result.stderr[:100]}")
                # pull 失败不一定阻止 push，继续尝试
            else:
                trace("✅ git pull 成功")
            
            # git push
            result = subprocess.run(
                [git_exe, "push", "origin", "master"],
                cwd=WORKSPACE,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=env
            )
            if result.returncode != 0:
                error_msg = result.stderr or result.stdout
                trace(f"❌ git push 失败: {error_msg[:200]}")
                if "fetch first" in error_msg.lower() or "rejected" in error_msg.lower():
                    return {"success": False, "message": "推送到 GitHub 失败: 本地代码落后于远程。\n建议: 先在命令行运行 'git pull origin master' 后再试。"}
                if "Could not connect" in error_msg or "Failed to connect" in error_msg:
                    return {"success": False, "message": f"无法连接到 GitHub，请检查 VPN/代理是否开启。\n建议: 开启 VPN 后再尝试发布，或确认网络能访问 github.com"}
                if "could not read" in error_msg.lower() or "prompt" in error_msg.lower():
                    return {"success": False, "message": f"GitHub Token 认证失败，需要重新配置远程仓库认证"}
                return {"success": False, "message": f"推送到 GitHub 失败: {error_msg[:200]}"}
            
            trace("✅ git push 成功")
            
            # 5. 返回成功信息
            repo_url = "https://github.com/sansonglive-tech/silkroad-trade-website"
            pages_url = "https://sansonglive-tech.github.io/silkroad-trade-website"
            
            return {
                "success": True,
                "message": "发布成功！GitHub Pages 将在 1-2 分钟后更新",
                "url": repo_url,
                "pages_url": pages_url,
                "timestamp": timestamp
            }
            
        except Exception as e:
            trace(f"❌ 发布失败: {str(e)}")
            print(traceback.format_exc())
            return {"success": False, "message": f"发布失败: {str(e)}"}

    def diagnose(self):
        """诊断 v7 文件结构"""
        trace_section("DIAGNOSE: 运行诊断")
        result = {"status": "ok", "checks": [], "warnings": []}
        
        v7_exists = os.path.isfile(V7_FILE)
        v6_exists = os.path.isfile(V6_FILE)
        result["files"] = {
            "v7": {"exists": v7_exists, "size": os.path.getsize(V7_FILE) if v7_exists else 0},
            "v6": {"exists": v6_exists, "size": os.path.getsize(V6_FILE) if v6_exists else 0},
            "cfg": {"exists": os.path.isfile(CFG_FILE), "size": os.path.getsize(CFG_FILE) if os.path.isfile(CFG_FILE) else 0}
        }
        trace(f"文件检查: v7={v7_exists}(size={result['files']['v7']['size']:,}), v6={v6_exists}")
        
        html = self.read_v7()
        if not html:
            return {"status": "error", "message": "无法读取 v7 HTML"}
        
        has_config = "const CONFIG =" in html
        result["checks"].append({"name": "CONFIG 块", "passed": has_config,
                                "detail": "const CONFIG = {...}" if has_config else "未找到"})
        
        checks = [
            ("services-grid", "service-card", "服务网格"),
            ("stats-inner", "stat-item", "统计数据"),
            ("policy-grid", "policy-card", "政策卡片"),
            ("testimonials-grid", "t-card", "客户案例"),
            ("process-grid", "pstep", "服务流程"),
            ("countries-grid", "region-card", "国家区域"),
        ]
        for container, item, label in checks:
            has_c = container in html
            has_i = item in html
            cnt = html.count(item) if has_i else 0
            result["checks"].append({"name": label, "passed": has_c and has_i,
                                    "detail": f"容器={'✅' if has_c else '❌'}, 条目数={cnt}"})
            trace(f"  {label}: container={'✅' if has_c else '❌'}, items={cnt}")
        
        all_passed = all(c["passed"] for c in result["checks"])
        result["status"] = "ok" if all_passed else "warning"
        if not all_passed:
            msg = "异常: " + ", ".join(c["name"] for c in result["checks"] if not c["passed"])
            result["warnings"].append(msg)
            trace(f"⚠️ {msg}")
        else:
            trace("✅ 所有检测通过！")
        return result


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not os.path.isfile(CFG_FILE):
        save_cfg(DEFAULT)
    v7_ok = os.path.isfile(V7_FILE) and os.path.getsize(V7_FILE) >= 1000
    v6_ok = os.path.isfile(V6_FILE) and os.path.getsize(V6_FILE) >= 1000
    trace_section("服务启动")
    print(f"\n  === 丝路山海通 后台 ===")
    print(f"  后台: http://localhost:{PORT}/admin")
    print(f"  预览: http://localhost:{PORT}/preview")
    print(f"  诊断: http://localhost:{PORT}/api/diagnose")
    print(f"  追踪: http://localhost:{PORT}/api/trace")
    print('  v7 状态: ' + ('✅' if v7_ok else '❌'))
    print('  v6 状态: ' + ('✅' if v6_ok else '❌'))
    print(f"  ⚠️ 不改 v7 代码，配置存在 site_config.json\n")
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n停止")
        server.server_close()
