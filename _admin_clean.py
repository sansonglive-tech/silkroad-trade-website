#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 涓濊矾灞辨捣閫?鍙鍖栧悗鍙?v3 鈥?鐙珛杩愯锛屼笉鏀?v7
import json, os, re, shutil, traceback, sys, secrets
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

WORKSPACE = os.path.dirname(os.path.abspath(__file__))

# 鐧诲綍閰嶇疆
ADMIN_USER = "jackleework"
ADMIN_PASS = "999999"
SESSIONS = {}  # token -> username
V7_FILE = os.path.join(WORKSPACE, "silkroad-trade_v7_silk_poster.html")
V6_FILE = os.path.join(WORKSPACE, "silkroad-trade_v6_silk_poster.html")
CFG_FILE = os.path.join(WORKSPACE, "site_config.json")
PORT = 8080

DEFAULT = {
    "company": {
        "name": "涓濊矾灞辨捣閫?,
        "slogan": "涓€甯︿竴璺紒涓氬嚭娴蜂竴绔欏紡鏈嶅姟",
        "email": "outlook@silkroad-trade.com",
        "phone": "400-xxx-xxxx",
        "icp": "绮CP澶嘪XXXXXXX鍙?,
        "wechatId": "SilkRoadTrade",
        "wechatQR": ""
    },
    "slides": [
        {"id":"slide-1","title":"涔樹笣璺暱椋庨€氳揪鍏ㄧ悆","subtitle":"涓€甯︿竴璺紒涓氬嚭娴蜂竴绔欏紡鏈嶅姟","desc":"涓濊矾灞辨捣閫?鈥?鍝嶅簲鍥藉涓€甯︿竴璺€¤锛屼负浼佷笟鍑烘捣鎻愪緵鍏徃娉ㄥ唽銆佽储绋庢敮鎸併€佷骇鍝佸噯鍏ャ€佹湰鍦板寲杩愯惀绛変竴绔欏紡钀藉湴鏈嶅姟銆?,"img":"https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&q=80","detailId":"company-advantage"},
        {"id":"slide-2","title":"鍏徃娉ㄥ唽璧勮川鍔炵悊","subtitle":"鏈€蹇?涓伐浣滄棩瀹屾垚娴峰鍏徃璁剧珛","desc":"澧冨唴澧冨鍏徃娉ㄥ唽銆佽惀涓氭墽鐓ф縺娲汇€佽涓氳祫璐ㄨ瘉鐓у姙鐞嗭紝璁╂偍鐨勪紒涓氬揩閫熷悎娉曡惤鍦版捣澶栥€?,"img":"https://images.unsplash.com/photo-1560179707-f14e90ef3623?w=800&q=80","detailId":"company-reg"}
    ],
    "services": [
        {"id":"company-reg","title":"鍏徃娉ㄥ唽涓庤祫璐?,"sub":"incorporation & licensing","desc":"澧冨鍏徃娉ㄥ唽銆佽惀涓氭墽鐓ф縺娲汇€佽涓氳祫璐ㄨ瘉鐓у姙鐞?,"icon":"\U0001f3e2","detailId":"company-reg"},
        {"id":"product-cert","title":"浜у搧鍑嗗叆涓庤璇?,"sub":"product certification","desc":"SNI/BPOM/娓呯湡璁よ瘉涓€绔欏紡鍔炵悊","icon":"\u2705","detailId":"certification"},
        {"id":"tax-legal","title":"璐㈢◣浜轰簨涓庢硶鍔?,"sub":"tax, hr & legal","desc":"璐㈢◣绛瑰垝銆佷唬鐞嗚璐︺€佹硶鍔″挩璇竴绔欏紡","icon":"\U0001f4ca","detailId":"tax-legal"},
        {"id":"local-ops","title":"鏈湴鍖栬繍钀ユ敮鎸?,"sub":"local operation","desc":"琛屾斂鍔炲叕銆佹湰鍦版嫑鑱樸€佹斂搴滃叧绯汇€佽祫婧愬鎺?,"icon":"\U0001f310","detailId":"local-ops"},
        {"id":"visa","title":"绛捐瘉鑰冨療涓庡嚭琛?,"sub":"visa & business travel","desc":"鍟嗗姟绛捐瘉銆佸伐浣滅璇併€佸伐鍘傝€冨療涓€绔欏紡","icon":"\u2708\ufe0f","detailId":"visa"},
        {"id":"factory","title":"寤哄巶宸ョ▼涓庢姇浜?,"sub":"factory & construction","desc":"娴峰寤哄巶閫夊潃銆佸伐绋嬭鍙€佺幆澧冨悎瑙?,"icon":"\U0001f3ed","detailId":"factory"}
    ],
    "stats": [
        {"num":"60+","label":"涓€甯︿竴璺鐩栧浗瀹?},
        {"num":"1,600+","label":"鏈嶅姟鍑烘捣浼佷笟"},
        {"num":"400+","label":"娴峰鏈湴鍛樺伐"},
        {"num":"5+","label":"鍖哄煙鏈嶅姟缃戠粶"}
    ],
    "policies": [
        {"num":"01","title":"鏀跨瓥鐮旂┒涓庤В璇?,"desc":"60+鍥藉鏀跨瓥鏁版嵁搴擄紝涓撲笟鍥㈤槦瀹炴椂杩借釜鏀跨瓥鍔ㄦ€?},
        {"num":"02","title":"鏀垮簻涓庡晢浼氬鎺?,"desc":"娣辫€曟湰鍦版斂鍟嗗叧绯伙紝鎼缓浼佷笟涓庡綋鍦版斂搴滄矡閫氭ˉ姊?},
        {"num":"03","title":"浜т笟鍥尯钀藉湴","desc":"瀵规帴涓€甯︿竴璺部绾块噸鐐逛骇涓氬洯鍖猴紝浜紭鎯犳斂绛?},
        {"num":"04","title":"鎶曡瀺璧勫鎺?,"desc":"涓茶仈鏀跨瓥鎬ч噾铻嶆満鏋勪笌鍟嗕笟璧勬湰锛屽璺緞铻嶈祫閫氶亾"}
    ],
    "testimonials": [
        {"name":"寮犲畯浼?,"role":"鏂拌兘婧愭苯杞?鍗板凹宸ュ巶璐熻矗浜?,"text":"甯垜浠湪闆呭姞杈惧畬鎴愪簡鍏徃娉ㄥ唽鍜屽伐鍘傞€夊潃锛屼粠鑰冨療鍒拌惤鍦板彧鐢ㄤ簡2涓湀銆?,"avatar":"寮?},
        {"name":"鏉庨洩宄?,"role":"宸ョ▼鏈烘 涓簹浜嬩笟閮ㄦ€荤粡鐞?,"text":"鍝嶅簲涓€甯︿竴璺紑鎷撲腑浜氬競鍦猴紝浠庢硶寰嬪悎瑙勫埌鏀垮簻鍏崇郴涓€璺姢鑸€?,"avatar":"鏉?},
        {"name":"鐜嬬惓","role":"椋熷搧楗枡 娴峰鎷撳睍鎬荤洃","text":"鍗板凹鐨凷NI璁よ瘉鍜屾竻鐪熻璇佷竴绔欏紡鍖呭姙锛屼骇鍝佸噯鍏ュ懆鏈熺缉鐭簡60%銆?,"avatar":"鐜?}
    ],
    "process": [
        {"num":"01","title":"闇€姹傝瘖鏂?,"desc":"娣卞叆浜嗚В浼佷笟鍑烘捣鐩爣涓庨渶姹傦紝瀹氬埗鍖栧嚭娴锋柟妗堛€?},
        {"num":"02","title":"灏借亴璋冪爺","desc":"甯傚満璋冪爺銆佹硶寰嬭瘎浼般€佽储绋庡垎鏋愶紝瑙勯伩椋庨櫓鍓嶇疆銆?},
        {"num":"03","title":"钀藉湴鎵ц","desc":"鍏徃娉ㄥ唽銆佽祫璐ㄥ姙鐞嗐€佸洟闃熸惌寤猴紝鍏ㄧ▼闄即鎺ㄨ繘銆?},
        {"num":"04","title":"鎸佺画杩愯惀","desc":"璐㈢◣浠ｈ处銆佹硶鍔℃敮鎸併€佹斂搴滅淮鎶わ紝闀挎湡杩愯惀淇濋殰銆?}
    ]
}

# ========== 杩借釜鏃ュ織绯荤粺 ==========
TRACE_LOG = []
TRACE_MAX = 200

def trace(msg, data=None):
    """杈撳嚭杩借釜淇℃伅鍒版帶鍒跺彴骞剁紦瀛樺埌 TRACE_LOG"""
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
    """杈撳嚭鍒嗘鏍囬"""
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
<title>涓濊矾灞辨捣閫?路 鍚庡彴绠＄悊</title>
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
<h2>鍚庡彴绠＄悊鍣?/h2>
<a class="on" onclick="sw('cp',this)">鍏徃淇℃伅</a>
<a onclick="sw('sl',this)">杞挱鍥?/a>
<a onclick="sw('sv',this)">鏈嶅姟鍗＄墖</a>
<a onclick="sw('st',this)">缁熻鏁板瓧</a>
<a onclick="sw('po',this)">鏀跨瓥鍗＄墖</a>
<a onclick="sw('te',this)">瀹㈡埛妗堜緥</a>
<a onclick="sw('pr',this)">鏈嶅姟娴佺▼</a>
<a onclick="sw('di',this)" style="margin-top:1rem;border-left-color:#2d8a4e;color:#a8c8a0">璇婃柇宸ュ叿</a>
</div>
<div class="main">
<h1>涓濊矾灞辨捣閫?路 鍚庡彴绠＄悊</h1>
<div class="sub">涓嶆敼 v7 浠ｇ爜 | 濉ソ鍐呭鐐逛繚瀛?| 棰勮椤电湅鏁堟灉</div>
<div id="msg" class="msg"></div>
<div class="toolbar">
<button class="btn btn-g" onclick="svAll()" id="sb">淇濆瓨鍏ㄩ儴</button>
<button class="btn btn-o" onclick="window.open('/preview','_blank')">棰勮</button>
<button class="btn btn-o" onclick="publishToGitHub()" id="pubBtn" style="background:#24292e;color:#fff;border-color:#24292e">馃摛 鍙戝竷鍒?GitHub</button>
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
    <div class="card-h"><h3>馃攳 璇婃柇宸ュ叿</h3></div>
    <p style="font-size:.82rem;color:#6b625c;margin-bottom:1rem">妫€鏌?v7 鏂囦欢缁撴瀯瀹屾暣鎬э紝鏌ョ湅 CONFIG 鍧楀拰鍚勪釜鏉垮潡鏄惁鑳借姝ｅ父璇嗗埆銆?/p>
    <div style="display:flex;gap:.5rem;flex-wrap:wrap">
      <button class="btn btn-g" onclick="runDiag()">杩愯璇婃柇</button>
      <button class="btn btn-o" onclick="viewTrace()">鏌ョ湅杩借釜鏃ュ織</button>
      <button class="btn btn-o" onclick="clearTrace()">娓呯┖鏃ュ織</button>
    </div>
    <div id="diagResult" style="margin-top:1rem;font-size:.82rem"></div>
    <div id="traceResult" style="margin-top:1rem;font-size:.78rem;display:none">
      <div class="card-h"><h3>馃搵 杩借釜鏃ュ織</h3><button class="ab" onclick="document.getElementById('traceResult').style.display='none'">鍏抽棴</button></div>
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
var LB={'name':'鍏徃鍚嶇О','slogan':'鍓爣棰?鏍囪','email':'鑱旂郴閭','phone':'鑱旂郴鐢佃瘽','icp':'澶囨鍙?,'wechatId':'寰俊鍙?};
function fIn(k,p,v){return '<div class="fg"><label>'+LB[p||k]+'</label><input value="'+es(v)+'" onchange="sp(\''+k+'\',this.value)"></div>';}
function fImg(k,v){return '<div class="fg"><label>浜岀淮鐮侀摼鎺?/label><input value="'+es(v)+'" onchange="sp(\''+k+'\',this.value)">'+ip(v)+'<div class="ht">浜岀淮鐮佷笂浼犲浘搴婂悗绮樿创閾炬帴</div></div>';}

window.onload=function(){
  msg('鍔犺浇涓?..','ok');
  var x=new XMLHttpRequest();
  x.open('GET','/api/config',true);
  x.onload=function(){
    if(x.status==200){D=JSON.parse(x.responseText);rAll();mhide();}
    else msg('鍔犺浇澶辫触: '+x.status,'er');
  };
  x.onerror=function(){msg('缃戠粶閿欒','er');};
  x.send();
};

function rAll(){rCp();rSl();rSv();rSt();rPo();rTe();rPr();}

function rCp(){
  var c=D.company||{},h='<div class="card">';
  h+=fIn('company.name','鍏徃鍚嶇О',c.name);
  h+=fIn('company.slogan','鍓爣棰?鏍囪',c.slogan);
  h+=fIn('company.email','鑱旂郴閭',c.email);
  h+=fIn('company.phone','鑱旂郴鐢佃瘽',c.phone);
  h+=fIn('company.icp','澶囨鍙?,c.icp);
  h+=fIn('company.wechatId','寰俊鍙?,c.wechatId);
  h+=fImg('company.wechatQR',c.wechatQR);
  h+='</div>';
  g('tp_cp').innerHTML=h;
}

function rSl(){
  var a=D.slides||[],h='<div class="card"><div class="card-h"><h3>杞挱鍥?('+a.length+'寮?</h3><button class="ab" onclick="arrAdd(\'slides\',{title:\'\',subtitle:\'\',desc:\'\',img:\'\',detailId:\'\'});rSl()">+娣诲姞</button></div>';
  for(var i=0;i<a.length;i++){
    h+='<div class="ib"><div class="ib-h"><strong>'+(i+1)+'</strong><button class="ab" onclick="arrDel(\'slides\','+i+');rSl()">鍒犻櫎</button></div>';
    h+='<div class="fg"><label>鏍囬</label><input value="'+es(a[i].title)+'" onchange="D.slides['+i+'].title=this.value"></div>';
    h+='<div class="fg"><label>鍓爣棰?/label><input value="'+es(a[i].subtitle)+'" onchange="D.slides['+i+'].subtitle=this.value"></div>';
    h+='<div class="fg"><label>鎻忚堪</label><textarea rows="2" onchange="D.slides['+i+'].desc=this.value">'+es(a[i].desc)+'</textarea></div>';
    h+='<div class="fg"><label>鍥剧墖閾炬帴</label><input value="'+es(a[i].img)+'" onchange="D.slides['+i+'].img=this.value">'+ip(a[i].img)+'</div></div>';
  }
  if(!a.length)h+='<div class="em">鏆傛棤</div>';
  g('tp_sl').innerHTML=h+'</div>';
}

function rSv(){
  var a=D.services||[],h='<div class="card"><div class="card-h"><h3>鏈嶅姟鍗＄墖 ('+a.length+'椤?</h3></div>';
  for(var i=0;i<a.length;i++){
    h+='<div class="ib"><div class="ib-h"><strong>'+(i+1)+': '+es(a[i].title)+'</strong></div>';
    h+='<div class="fg"><label>鏍囬</label><input value="'+es(a[i].title)+'" onchange="D.services['+i+'].title=this.value"></div>';
    h+='<div class="fg"><label>鍓爣棰?/label><input value="'+es(a[i].sub)+'" onchange="D.services['+i+'].sub=this.value"></div>';
    h+='<div class="fg"><label>鎻忚堪</label><textarea rows="2" onchange="D.services['+i+'].desc=this.value">'+es(a[i].desc)+'</textarea></div>';
    h+='<div class="fg"><label>鍥炬爣(emoji)</label><input value="'+es(a[i].icon)+'" onchange="D.services['+i+'].icon=this.value"></div></div>';
  }
  g('tp_sv').innerHTML=h+'</div>';
}

function rSt(){
  var a=D.stats||[],h='<div class="card"><div class="card-h"><h3>缁熻鏁板瓧</h3><button class="ab" onclick="arrAdd(\'stats\',{num:\'\',label:\'\'});rSt()">+娣诲姞</button></div>';
  for(var i=0;i<a.length;i++){
    h+='<div class="il"><input value="'+es(a[i].num)+'" placeholder="鏁板瓧" style="width:80px" onchange="D.stats['+i+'].num=this.value">';
    h+='<input value="'+es(a[i].label)+'" placeholder="鏍囩" style="flex:1" onchange="D.stats['+i+'].label=this.value">';
    h+='<button class="ab" onclick="arrDel(\'stats\','+i+');rSt()">鍒犻櫎</button></div>';
  }
  if(!a.length)h+='<div class="em">鏆傛棤</div>';
  g('tp_st').innerHTML=h+'</div>';
}

function rPo(){
  var a=D.policies||[],h='<div class="card"><div class="card-h"><h3>鏀跨瓥鍗＄墖</h3><button class="ab" onclick="arrAdd(\'policies\',{num:\'\',title:\'\',desc:\'\'});rPo()">+娣诲姞</button></div>';
  for(var i=0;i<a.length;i++){
    h+='<div class="ib"><div class="ib-h"><strong>'+(i+1)+'</strong><button class="ab" onclick="arrDel(\'policies\','+i+');rPo()">鍒犻櫎</button></div>';
    h+='<div class="fg"><label>缂栧彿</label><input value="'+es(a[i].num)+'" onchange="D.policies['+i+'].num=this.value"></div>';
    h+='<div class="fg"><label>鏍囬</label><input value="'+es(a[i].title)+'" onchange="D.policies['+i+'].title=this.value"></div>';
    h+='<div class="fg"><label>鎻忚堪</label><textarea rows="2" onchange="D.policies['+i+'].desc=this.value">'+es(a[i].desc)+'</textarea></div></div>';
  }
  g('tp_po').innerHTML=h+'</div>';
}

function rTe(){
  var a=D.testimonials||[],h='<div class="card"><div class="card-h"><h3>瀹㈡埛妗堜緥</h3><button class="ab" onclick="arrAdd(\'testimonials\',{name:\'\',role:\'\',text:\'\'});rTe()">+娣诲姞</button></div>';
  for(var i=0;i<a.length;i++){
    h+='<div class="ib"><div class="ib-h"><strong>'+(i+1)+': '+es(a[i].name)+'</strong><button class="ab" onclick="arrDel(\'testimonials\','+i+');rTe()">鍒犻櫎</button></div>';
    h+='<div class="fg"><label>濮撳悕</label><input value="'+es(a[i].name)+'" onchange="D.testimonials['+i+'].name=this.value"></div>';
    h+='<div class="fg"><label>鑱屼綅</label><input value="'+es(a[i].role)+'" onchange="D.testimonials['+i+'].role=this.value"></div>';
    h+='<div class="fg"><label>瀹㈡埛鍘熻瘽</label><textarea rows="2" onchange="D.testimonials['+i+'].text=this.value">'+es(a[i].text)+'</textarea></div></div>';
  }
  g('tp_te').innerHTML=h+'</div>';
}

function rPr(){
  var a=D.process||[],h='<div class="card"><div class="card-h"><h3>鏈嶅姟娴佺▼</h3><button class="ab" onclick="arrAdd(\'process\',{num:\'\',title:\'\',desc:\'\'});rPr()">+娣诲姞</button></div>';
  for(var i=0;i<a.length;i++){
    h+='<div class="ib"><div class="ib-h"><strong>'+(i+1)+'</strong><button class="ab" onclick="arrDel(\'process\','+i+');rPr()">鍒犻櫎</button></div>';
    h+='<div class="fg"><label>缂栧彿</label><input value="'+es(a[i].num)+'" onchange="D.process['+i+'].num=this.value"></div>';
    h+='<div class="fg"><label>鏍囬</label><input value="'+es(a[i].title)+'" onchange="D.process['+i+'].title=this.value"></div>';
    h+='<div class="fg"><label>鎻忚堪</label><textarea rows="2" onchange="D.process['+i+'].desc=this.value">'+es(a[i].desc)+'</textarea></div></div>';
  }
  g('tp_pr').innerHTML=h+'</div>';
}

// ========== 璇婃柇宸ュ叿 ==========
function runDiag(){
  var r=g('diagResult');r.innerHTML='<div style="color:#6b625c">鈴?璇婃柇涓?..</div>';
  var x=new XMLHttpRequest();
  x.open('GET','/api/diagnose',true);
  x.onload=function(){
    if(x.status!=200){r.innerHTML='<div class="msg er" style="display:block">璇婃柇澶辫触: '+x.status+'</div>';return;}
    var d=JSON.parse(x.responseText);
    var h='<div class="card-h" style="margin-top:.5rem"><h3>馃搳 璇婃柇缁撴灉 '+(d.status=='ok'?'鉁?:'鈿狅笍')+'</h3></div>';
    h+='<table style="width:100%;border-collapse:collapse;font-size:.78rem">';
    for(var i=0;i<d.checks.length;i++){
      var c=d.checks[i];
      h+='<tr><td style="padding:.4rem .6rem;border-bottom:1px solid #eee">'+(c.passed?'鉁?:'鉂?)+'</td>';
      h+='<td style="padding:.4rem .6rem;border-bottom:1px solid #eee;font-weight:600">'+es(c.name)+'</td>';
      h+='<td style="padding:.4rem .6rem;border-bottom:1px solid #eee;color:#6b625c">'+es(c.detail)+'</td></tr>';
    }
    h+='</table>';
    if(d.files){
      h+='<div style="margin-top:.8rem;font-size:.72rem;color:#6b625c">馃搧 鏂囦欢: ';
      h+='v7='+(d.files.v7.exists ? d.files.v7.size.toLocaleString()+' bytes 鉁? : '鉂?涓嶅瓨鍦?)+', ';
      h+='v6='+(d.files.v6.exists ? d.files.v6.size.toLocaleString()+' bytes 鉁? : '鉂?涓嶅瓨鍦?);
      h+='</div>';
    }
    if(d.warnings&&d.warnings.length)h+='<div style="margin-top:.5rem;padding:.4rem .6rem;background:#fff3cd;border-radius:4px;font-size:.75rem">鈿狅笍 '+es(d.warnings.join('; '))+'</div>';
    r.innerHTML=h;
  };
  x.onerror=function(){r.innerHTML='<div class="msg er" style="display:block">缃戠粶閿欒</div>';};
  x.send();
}

function viewTrace(){
  var t=g('traceResult');t.style.display='block';
  var c=g('traceContent');c.textContent='鈴?鍔犺浇涓?..';
  var x=new XMLHttpRequest();
  x.open('GET','/api/trace',true);
  x.onload=function(){
    if(x.status!=200){c.textContent='鍔犺浇澶辫触: '+x.status;return;}
    var d=JSON.parse(x.responseText);
    c.textContent=d.traces.length ? d.traces.join('\n') : '鏆傛棤杩借釜鏃ュ織';
  };
  x.onerror=function(){c.textContent='缃戠粶閿欒';};
  x.send();
}

function clearTrace(){
  var x=new XMLHttpRequest();
  x.open('GET','/api/trace_clear',true);
  x.onload=function(){document.getElementById('traceResult').style.display='none';msg('杩借釜鏃ュ織宸叉竻绌?,'ok');setTimeout(mhide,2000);};
  x.send();
}

function svAll(){
  var b=g('sb');b.textContent='淇濆瓨涓?..';b.disabled=true;msg('淇濆瓨涓?..','ok');
  var x=new XMLHttpRequest();
  x.open('POST','/api/save_all',true);
  x.setRequestHeader('Content-Type','application/json');
  x.onload=function(){
    var d=JSON.parse(x.responseText);
    if(d.success){msg('淇濆瓨鎴愬姛!','ok');}else{msg('淇濆瓨澶辫触: '+d.message,'er');}
    b.textContent='淇濆瓨鍏ㄩ儴';b.disabled=false;setTimeout(mhide,3000);
  };
  x.onerror=function(){msg('缃戠粶閿欒','er');b.textContent='淇濆瓨鍏ㄩ儴';b.disabled=false;};
  x.send(JSON.stringify(D));
}

// ========== 鍙戝竷鍒?GitHub ==========
function publishToGitHub(){
  var b=g('pubBtn');b.textContent='鍙戝竷涓?..';b.disabled=true;msg('姝ｅ湪鐢熸垚鍙戝竷鏂囦欢骞舵帹閫佸埌 GitHub...','ok');
  var x=new XMLHttpRequest();
  x.open('POST','/api/publish',true);
  x.setRequestHeader('Content-Type','application/json');
  x.onload=function(){
    var d=JSON.parse(x.responseText);
    if(d.success){
      msg('鉁?鍙戝竷鎴愬姛! GitHub Pages 灏嗗湪 1-2 鍒嗛挓鍚庢洿鏂?,'ok');
      if(d.url){
        setTimeout(function(){
          if(confirm('鍙戝竷鎴愬姛! 鏄惁鎵撳紑 GitHub 鏌ョ湅?')){
            window.open(d.url,'_blank');
          }
        },500);
      }
    }else{
      msg('鉂?鍙戝竷澶辫触: '+d.message,'er');
    }
    b.textContent='馃摛 鍙戝竷鍒?GitHub';b.disabled=false;setTimeout(mhide,5000);
  };
  x.onerror=function(){msg('缃戠粶閿欒','er');b.textContent='馃摛 鍙戝竷鍒?GitHub';b.disabled=false;};
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
if(pg && c.policies && c.policies.length > 0) {
  pg.innerHTML = c.policies.map(function(p, i){
    var n = String(i + 1).padStart(2, '0');
    return '<div class="policy-card" onclick="openDetail(\\'' + (p.detailId || p.id) + '\\')">' +
      '<div class="pn">' + n + '</div><div>' +
      '<h3>' + p.title + '</h3><p>' + (p.desc || '') + '</p></div></div>';
  }).join('');
}

// --- Render testimonials from CONFIG ---
var tg = document.querySelector(".testimonials-grid");
if(tg && c.testimonials && c.testimonials.length > 0) {
  tg.innerHTML = c.testimonials.map(function(t, i){
    var av = t.avatar || (t.name ? t.name.charAt(0) : "\\ud83d\\udc64");
    return '<div class="t-card" onclick="openDetail(\\'' + (t.detailId || ("case-" + i)) + '\\')">' +
      '<div class="tq">&ldquo;</div><p class="t-text">' + (t.text || '') + '</p>' +
      '<div class="t-author"><div class="t-av">' + av + '</div><div>' +
      '<div class="t-name">' + (t.name || '') + '</div><div class="t-role">' + (t.role || '') + '</div></div></div></div>';
  }).join('');
}

// --- Render process from CONFIG ---
var pr = document.querySelector(".process-grid");
if(pr && c.process && c.process.length > 0) {
  pr.innerHTML = c.process.map(function(p){
    return '<div class="pstep" onclick="openDetail(\\'' + (p.detailId || ("process-step" + p.num)) + '\\')">' +
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
<title>绠＄悊鍚庡彴鐧诲綍 路 涓濊矾灞辨捣閫?/title>
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
<h1>涓濊矾灞辨捣閫?/h1>
<p>绠＄悊鍚庡彴鐧诲綍</p>
<div id="msg" class="msg"></div>
<div class="fg"><label>鐢ㄦ埛鍚?/label><input id="user" type="text" autocomplete="username" autofocus></div>
<div class="fg"><label>瀵嗙爜</label><input id="pass" type="password" autocomplete="current-password"></div>
<button class="btn btn-g" onclick="login()">鐧?褰?/button>
<div class="fo">鍚庡彴绠＄悊绯荤粺</div>
</div>
<script>
function login(){
  var u=document.getElementById('user'),p=document.getElementById('pass'),m=document.getElementById('msg');
  u.classList.remove('err');p.classList.remove('err');m.style.display='none';
  if(!u.value){u.classList.add('err');u.focus();m.textContent='璇疯緭鍏ョ敤鎴峰悕';m.className='msg er';return;}
  if(!p.value){p.classList.add('err');p.focus();m.textContent='璇疯緭鍏ュ瘑鐮?;m.className='msg er';return;}
  var x=new XMLHttpRequest();
  x.open('POST','/api/login',true);
  x.setRequestHeader('Content-Type','application/json');
  x.onload=function(){
    if(x.status==200){window.location.href='/admin';}
    else{var r=JSON.parse(x.responseText);m.textContent=r.message||'鐧诲綍澶辫触';m.className='msg er';}
  };
  x.onerror=function(){m.textContent='缃戠粶閿欒';m.className='msg er';};
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
            # 鍏紑璺敱锛氶瑙堥〉鏃犻渶鐧诲綍
            if p == "/preview":
                html = self.read_v7()
                if html and html != "<h1>v7 not found</h1>":
                    html = self.inject_config(html)
                self.rhtml(html)
                return
            # 鐧诲綍椤靛強鐧诲綍椤佃祫婧愶紙鍏紑锛?            if p == "/login":
                self.rhtml(LOGIN_PAGE)
                return
            if p == "/login_bg.jpg":
                self.rstatic(p)
                return
            # 浠ヤ笅璺敱闇€瑕佺櫥褰?            tok = self.get_session()
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
                    self.rjson({"success": False, "message": "鐢ㄦ埛鍚嶆垨瀵嗙爜閿欒"})
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
            # 浠ヤ笅 API 闇€瑕佺櫥褰?            tok = self.get_session()
            if not tok:
                self.rjson({"success": False, "message": "鏈櫥褰?})
                return
            if p == "/api/save_all":
                n = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(n).decode("utf-8"))
                save_cfg(data)
                self.rjson({"success": True, "message": "閰嶇疆宸蹭繚瀛?})
            elif p == "/api/publish":
                result = self.publish_to_github()
                self.rjson(result)
            else:
                self.rjson({"success": False, "message": "unknown"})
        except Exception as e:
            self.rjson({"success": False, "message": str(e)})

    def read_v7(self):
        trace_section("read_v7: 璇诲彇 HTML")
        if not os.path.isfile(V7_FILE) or os.path.getsize(V7_FILE) < 100:
            trace(f"v7 涓嶅瓨鍦ㄦ垨澶皬, 灏濊瘯浠?v6 澶嶅埗")
            if os.path.isfile(V6_FILE):
                trace(f"浠?v6 澶嶅埗鍒?v7: {os.path.getsize(V6_FILE)} bytes")
                shutil.copy2(V6_FILE, V7_FILE)
                trace("澶嶅埗瀹屾垚")
        if os.path.isfile(V7_FILE):
            size = os.path.getsize(V7_FILE)
            with open(V7_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            trace(f"v7 HTML 璇诲彇鎴愬姛: {size:,} bytes, {len(content):,} 瀛楃")
            return content
        trace("鉂?v7 鏂囦欢涓嶅瓨鍦?)
        return None

    def to_js(self, val, indent=2):
        return json.dumps(val, ensure_ascii=False, indent=indent)

    def inject_config(self, html):
        trace_section("inject_config: 娉ㄥ叆閰嶇疆")
        cfg = load_cfg()
        trace(f"閰嶇疆鍔犺浇: {len(cfg.get('slides',[]))} 寮犺疆鎾? {len(cfg.get('services',[]))} 椤规湇鍔? {len(cfg.get('stats',[]))} 椤圭粺璁?)
        js_config = self.to_js(cfg)
        trace(f"JS 閰嶇疆搴忓垪鍖? {len(js_config):,} 瀛楃")
        
        # 鐢ㄨ姳鎷彿鍖归厤鎵?CONFIG 鍧楋紝鑰岄潪绠€鍗曟鍒?        marker = "const CONFIG = "
        idx = html.find(marker)
        if idx == -1:
            trace("鈿狅笍 鏈湪 v7 HTML 涓壘鍒?'const CONFIG = ' 鏍囪锛?)
            return html
        
        brace_idx = html.find("{", idx)
        if brace_idx == -1:
            trace("鈿狅笍 鎵惧埌鏍囪浣嗘壘涓嶅埌 '{'")
            return html
        
        # 鑺辨嫭鍙锋繁搴﹁鏁帮紝鎵惧埌鍖归厤鐨?};
        depth = 0
        end = brace_idx
        for i in range(brace_idx, len(html)):
            if html[i] == "{":
                depth += 1
            elif html[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    # 璺宠繃鍙兘鐨勫垎鍙?                    while end < len(html) and html[end] in " \t\n\r":
                        end += 1
                    if end < len(html) and html[end] == ";":
                        end += 1
                    break
        
        if depth != 0:
            trace("鈿狅笍 鑺辨嫭鍙蜂笉鍖归厤锛屾棤娉曟壘鍒?CONFIG 缁撴潫")
            return html
        
        # 鏇挎崲 CONFIG 鍧?        new_html = html[:idx] + f"const CONFIG = {js_config};" + html[end:]
        old_len = end - idx
        trace(f"鉁?CONFIG 鍧楁浛鎹㈡垚鍔? 鏃?{old_len}瀛楃 鈫?鏂?{len(js_config)+len('const CONFIG = ;')}瀛楃")
        
        new_html = new_html.replace("</body>", INJECT_SCRIPT + "</body>")
        trace("鉁?INJECT_SCRIPT 娉ㄥ叆鎴愬姛")
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
        """鐢熸垚 index.html 骞舵帹閫佸埌 GitHub"""
        import subprocess
        from datetime import datetime
        
        trace_section("PUBLISH: 鍙戝竷鍒?GitHub")
        
        try:
            # 1. 璇诲彇 v7 HTML
            html = self.read_v7()
            if not html or html == "<h1>v7 not found</h1>":
                return {"success": False, "message": "v7 HTML 鏂囦欢涓嶅瓨鍦?}
            
            # 2. 娉ㄥ叆鏈€鏂伴厤缃紙鐢熸垚闈欐€?HTML锛?            trace("娉ㄥ叆鏈€鏂伴厤缃埌 HTML...")
            publish_html = self.inject_config(html)
            
            # 3. 淇濆瓨涓?index.html锛圙itHub Pages 榛樿鍏ュ彛锛?            index_path = os.path.join(WORKSPACE, "index.html")
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(publish_html)
            trace(f"鉁?index.html 鐢熸垚鎴愬姛: {len(publish_html):,} 瀛楃")
            
            # 4. 鎵ц git 鍛戒护鎺ㄩ€?            trace("鎵ц git 鎺ㄩ€?..")
            git_exe = r"E:\鑵捐榫欒櫨\QClaw\v0.2.29.592\resources\git\cmd\git.exe"
            trace(f"浣跨敤 git: {git_exe}")
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
                trace(f"鈿狅笍 git add 璀﹀憡: {result.stderr}")
            
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
                # 鍙兘鏄病鏈夊彉鍖?                if "nothing to commit" in result.stdout.lower() or "nothing to commit" in result.stderr.lower():
                    trace("娌℃湁鍙樺寲闇€瑕佹彁浜?)
                else:
                    trace(f"鈿狅笍 git commit 璀﹀憡: {result.stderr}")
            else:
                trace(f"鉁?git commit: {commit_msg}")
            
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
                trace(f"鉂?git push 澶辫触: {error_msg[:200]}")
                if "Could not connect" in error_msg or "Failed to connect" in error_msg:
                    return {"success": False, "message": f"鏃犳硶杩炴帴鍒?GitHub锛岃妫€鏌?VPN/浠ｇ悊鏄惁寮€鍚€俓n寤鸿: 寮€鍚?VPN 鍚庡啀灏濊瘯鍙戝竷锛屾垨纭缃戠粶鑳借闂?github.com"}
                if "could not read" in error_msg.lower() or "prompt" in error_msg.lower():
                    return {"success": False, "message": f"GitHub Token 璁よ瘉澶辫触锛岄渶瑕侀噸鏂伴厤缃繙绋嬩粨搴撹璇?}
                return {"success": False, "message": f"鎺ㄩ€佸埌 GitHub 澶辫触: {error_msg[:200]}"}
            
            trace("鉁?git push 鎴愬姛")
            
            # 5. 杩斿洖鎴愬姛淇℃伅
            repo_url = "https://github.com/sansonglive-tech/silkroad-trade-website"
            pages_url = "https://sansonglive-tech.github.io/silkroad-trade-website"
            
            return {
                "success": True,
                "message": "鍙戝竷鎴愬姛锛丟itHub Pages 灏嗗湪 1-2 鍒嗛挓鍚庢洿鏂?,
                "url": repo_url,
                "pages_url": pages_url,
                "timestamp": timestamp
            }
            
        except Exception as e:
            trace(f"鉂?鍙戝竷澶辫触: {str(e)}")
            print(traceback.format_exc())
            return {"success": False, "message": f"鍙戝竷澶辫触: {str(e)}"}

    def diagnose(self):
        """璇婃柇 v7 鏂囦欢缁撴瀯"""
        trace_section("DIAGNOSE: 杩愯璇婃柇")
        result = {"status": "ok", "checks": [], "warnings": []}
        
        v7_exists = os.path.isfile(V7_FILE)
        v6_exists = os.path.isfile(V6_FILE)
        result["files"] = {
            "v7": {"exists": v7_exists, "size": os.path.getsize(V7_FILE) if v7_exists else 0},
            "v6": {"exists": v6_exists, "size": os.path.getsize(V6_FILE) if v6_exists else 0},
            "cfg": {"exists": os.path.isfile(CFG_FILE), "size": os.path.getsize(CFG_FILE) if os.path.isfile(CFG_FILE) else 0}
        }
        trace(f"鏂囦欢妫€鏌? v7={v7_exists}(size={result['files']['v7']['size']:,}), v6={v6_exists}")
        
        html = self.read_v7()
        if not html:
            return {"status": "error", "message": "鏃犳硶璇诲彇 v7 HTML"}
        
        has_config = "const CONFIG =" in html
        result["checks"].append({"name": "CONFIG 鍧?, "passed": has_config,
                                "detail": "const CONFIG = {...}" if has_config else "鏈壘鍒?})
        
        checks = [
            ("services-grid", "service-card", "鏈嶅姟缃戞牸"),
            ("stats-inner", "stat-item", "缁熻鏁版嵁"),
            ("policy-grid", "policy-card", "鏀跨瓥鍗＄墖"),
            ("testimonials-grid", "t-card", "瀹㈡埛妗堜緥"),
            ("process-grid", "pstep", "鏈嶅姟娴佺▼"),
            ("countries-grid", "region-card", "鍥藉鍖哄煙"),
        ]
        for container, item, label in checks:
            has_c = container in html
            has_i = item in html
            cnt = html.count(item) if has_i else 0
            result["checks"].append({"name": label, "passed": has_c and has_i,
                                    "detail": f"瀹瑰櫒={'鉁? if has_c else '鉂?}, 鏉＄洰鏁?{cnt}"})
            trace(f"  {label}: container={'鉁? if has_c else '鉂?}, items={cnt}")
        
        all_passed = all(c["passed"] for c in result["checks"])
        result["status"] = "ok" if all_passed else "warning"
        if not all_passed:
            msg = "寮傚父: " + ", ".join(c["name"] for c in result["checks"] if not c["passed"])
            result["warnings"].append(msg)
            trace(f"鈿狅笍 {msg}")
        else:
            trace("鉁?鎵€鏈夋娴嬮€氳繃锛?)
        return result


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not os.path.isfile(CFG_FILE):
        save_cfg(DEFAULT)
    v7_ok = os.path.isfile(V7_FILE) and os.path.getsize(V7_FILE) >= 1000
    v6_ok = os.path.isfile(V6_FILE) and os.path.getsize(V6_FILE) >= 1000
    trace_section("鏈嶅姟鍚姩")
    print(f"\n  === 涓濊矾灞辨捣閫?鍚庡彴 ===")
    print(f"  鍚庡彴: http://localhost:{PORT}/admin")
    print(f"  棰勮: http://localhost:{PORT}/preview")
    print(f"  璇婃柇: http://localhost:{PORT}/api/diagnose")
    print(f"  杩借釜: http://localhost:{PORT}/api/trace")
    print('  v7 鐘舵€? ' + ('鉁? if v7_ok else '鉂?))
    print('  v6 鐘舵€? ' + ('鉁? if v6_ok else '鉂?))
    print(f"  鈿狅笍 涓嶆敼 v7 浠ｇ爜锛岄厤缃瓨鍦?site_config.json\n")
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n鍋滄")
        server.server_close()
