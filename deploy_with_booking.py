#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
丝路山海通 · 带预约记录的部署脚本
====================================
不修改任何源文件，生成 index.html 并推送至 GitHub。
读取源文件为只读，输出到 index.html + git push。
"""

import json, os, re, subprocess, sys
from datetime import datetime

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
V7_FILE = os.path.join(WORKSPACE, "silkroad-trade_v7_silk_poster.html")
CFG_FILE = os.path.join(WORKSPACE, "site_config.json")
GIT_EXE = r"E:\腾讯龙虾\QClaw\v0.2.30.594\resources\git\cmd\git.exe"
GIT_REPO = "https://github.com/sansonglive-tech/silkroad-trade-website"
PAGES_URL = "https://sansonglive-tech.github.io/silkroad-trade-website"

HOOK_SCRIPT = r"""<script>
(function(){
var BS='https://qty-poetry-regulation-comics.trycloudflare.com';
window.submitBook=function(){
var n=(document.getElementById('bookName')||{}).value;
var p=(document.getElementById('bookPhone')||{}).value;
var c=(document.getElementById('bookCountry')||{}).value;
if(!n||!n.trim()||!p||!p.trim()){alert('\u8bf7\u586b\u5199\u59d3\u540d\u548c\u624b\u673a\u53f7\u7801');return;}
var x=new XMLHttpRequest();
x.open('POST',BS+'/api/booking',true);
x.setRequestHeader('Content-Type','application/json');
x.onload=function(){
if(x.status===200){alert('\u2705 \u9884\u7ea6\u63d0\u4ea4\u6210\u529f\uff01\u6211\u4eec\u5c06\u5c3d\u5feb\u4e0e\u60a8\u8054\u7cfb\u3002');
if(document.getElementById('bookName'))document.getElementById('bookName').value='';
if(document.getElementById('bookPhone'))document.getElementById('bookPhone').value='';
if(document.getElementById('bookCountry'))document.getElementById('bookCountry').value='';
if(typeof closeBook==='function')closeBook();
}else{alert('\u274c \u63d0\u4ea4\u5931\u8d25\uff0c\u8bf7\u7a0d\u540e\u91cd\u8bd5');}
};
x.onerror=function(){alert('\u274c \u7f51\u7edc\u9519\u8bef\uff0c\u8bf7\u7a0d\u540e\u91cd\u8bd5\u6216\u8054\u7cfb\u5ba2\u670d');};
x.send(JSON.stringify({name:n.trim(),phone:p.trim(),country:(c||'').trim()}));
};
console.log('[BookingHook] enabled');
})();
</script>"""


def log(msg, data=None):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"  [{ts}] {msg}")
    if data:
        print(f"    -> {str(data)[:200]}")


def read_v7():
    if not os.path.isfile(V7_FILE):
        log("v7 文件不存在!", V7_FILE)
        return None
    with open(V7_FILE, "r", encoding="utf-8") as f:
        html = f.read()
    log(f"v7 已读取: {len(html):,} 字符")
    return html


def load_config():
    if not os.path.isfile(CFG_FILE):
        log("配置文件不存在", CFG_FILE)
        return None
    with open(CFG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    log(f"配置已加载: {len(json.dumps(cfg)):,} 字符")
    return cfg


def inject_config(html, cfg):
    """注入配置到 HTML（同 admin_server.py 的逻辑精简版）"""
    # 公司信息
    html = html.replace("__COMPANY_NAME__", cfg.get("company", {}).get("name", ""))
    html = html.replace("__COMPANY_SLOGAN__", cfg.get("company", {}).get("slogan", ""))
    html = html.replace("__COMPANY_EMAIL__", cfg.get("company", {}).get("email", ""))
    html = html.replace("__COMPANY_PHONE__", cfg.get("company", {}).get("phone", ""))
    html = html.replace("__ICP__", cfg.get("company", {}).get("icp", ""))
    html = html.replace("__WECHAT_ID__", cfg.get("company", {}).get("wechatId", ""))
    html = html.replace("__WECHAT_QR__", cfg.get("company", {}).get("wechatQR", ""))
    
    # Slides
    slides = cfg.get("slides", [])
    slides_html = ""
    for i, s in enumerate(slides):
        active = " active" if i == 0 else ""
        slides_html += f"""<div class="carousel-item{active}" id="{s.get('detailId','')}">
            <div class="carousel-bg" style="background-image:url('{s.get('img','')}')"></div>
            <div class="carousel-overlay"></div>
            <div class="carousel-content">
                <p class="carousel-subtitle">{s.get('subtitle','')}</p>
                <h2 class="carousel-title">{s.get('title','')}</h2>
                <p class="carousel-desc">{s.get('desc','')}</p>
                <a href="#services" class="btn-primary">了解服务</a>
                <a href="#contact" class="btn-outline">立即咨询</a>
            </div>
        </div>"""
    html = html.replace("<!-- AUTO_SLIDES -->", slides_html)
    
    # 服务项
    services = cfg.get("services", [])
    services_html = ""
    for s in services:
        services_html += f"""<div class="service-card" id="{s.get('detailId','')}">
            <div class="service-icon">{s.get('icon','')}</div>
            <h3>{s.get('title','')}</h3>
            <p class="service-sub">{s.get('sub','')}</p>
            <p class="service-desc">{s.get('desc','')}</p>
        </div>"""
    html = html.replace("<!-- AUTO_SERVICES -->", services_html)
    
    # 统计数据
    stats = cfg.get("stats", [])
    stats_html = ""
    for s in stats:
        stats_html += f"""<div class="stat-item">
            <div class="stat-num">{s.get('num','')}</div>
            <div class="stat-label">{s.get('label','')}</div>
        </div>"""
    html = html.replace("<!-- AUTO_STATS -->", stats_html)
    
    # 政策模块
    policies = cfg.get("policies", [])
    policies_html = ""
    for p in policies:
        policies_html += f"""<div class="policy-card">
            <div class="policy-num">{p.get('num','')}</div>
            <h3>{p.get('title','')}</h3>
            <p>{p.get('desc','')}</p>
        </div>"""
    html = html.replace("<!-- AUTO_POLICIES -->", policies_html)
    
    # 案例模块
    testimonials = cfg.get("testimonials", [])
    test_html = ""
    for t in testimonials:
        test_html += f"""<div class="test-card">
            <div class="test-avatar">{t.get('avatar','')}</div>
            <div class="test-text">"{t.get('text','')}"</div>
            <div class="test-name">{t.get('name','')}</div>
            <div class="test-role">{t.get('role','')}</div>
        </div>"""
    html = html.replace("<!-- AUTO_TESTIMONIALS -->", test_html)
    
    # 流程模块
    process = cfg.get("process", [])
    process_html = ""
    for p in process:
        process_html += f"""<div class="step-card">
            <div class="step-num">{p.get('num','')}</div>
            <h3>{p.get('title','')}</h3>
            <p>{p.get('desc','')}</p>
        </div>"""
    html = html.replace("<!-- AUTO_PROCESS -->", process_html)
    
    # 联系方式
    html = html.replace("__CONTACT_EMAIL__", cfg.get("company", {}).get("email", ""))
    html = html.replace("__CONTACT_PHONE__", cfg.get("company", {}).get("phone", ""))
    html = html.replace("__CONTACT_WECHAT__", cfg.get("company", {}).get("wechatId", ""))
    
    return html


def inject_booking_hook(html):
    """在 </body> 前注入预约 Hook 脚本"""
    if HOOK_SCRIPT in html:
        log("预约 Hook 已存在，跳过注入")
        return html
    
    html = html.replace("</body>", HOOK_SCRIPT + "\n</body>")
    log("预约 Hook 已注入到 HTML")
    return html


def git_publish(index_html):
    """执行 git add/commit/push"""
    env = os.environ.copy()
    env["GIT_ASKPASS"] = "echo"
    env["GIT_TERMINAL_PROMPT"] = "0"
    
    # 写入 index.html
    index_path = os.path.join(WORKSPACE, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    log(f"index.html 已生成: {len(index_html):,} 字符")
    
    # git add
    log("git add ...")
    r = subprocess.run([GIT_EXE, "add", "index.html", "site_config.json"],
                       cwd=WORKSPACE, capture_output=True, text=True, encoding="utf-8", env=env)
    if r.returncode != 0:
        log(f"git add 警告: {r.stderr.strip()[:100]}")
    
    # git commit
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"Update website + booking hook - {ts}"
    r = subprocess.run([GIT_EXE, "commit", "-m", msg],
                       cwd=WORKSPACE, capture_output=True, text=True, encoding="utf-8", env=env)
    if r.returncode == 0:
        log(f"git commit: {msg}")
    elif "nothing to commit" in (r.stdout + r.stderr).lower():
        log("无变化需要提交")
    else:
        log(f"commit 警告: {r.stderr.strip()[:100]}")
    
    # git pull
    log("git pull --rebase ...")
    r = subprocess.run([GIT_EXE, "pull", "origin", "main", "--rebase"],
                       cwd=WORKSPACE, capture_output=True, text=True, encoding="utf-8", env=env)
    if r.returncode == 0:
        log("git pull 成功")
    else:
        log(f"pull 警告: {r.stderr.strip()[:100]}")
    
    # git push
    log("git push ...")
    r = subprocess.run([GIT_EXE, "push", "origin", "main"],
                       cwd=WORKSPACE, capture_output=True, text=True, encoding="utf-8", env=env)
    if r.returncode == 0:
        log("git push 成功!")
        return True
    else:
        err = r.stderr or r.stdout
        log(f"git push 失败: {err.strip()[:200]}")
        return False


def main():
    print()
    print("  +----------------------------------------+")
    print("  |   丝路山海通 · 带预约记录部署          |")
    print("  |   Silent Reading 只读源文件             |")
    print("  +----------------------------------------+")
    print()
    
    # Step 1: 读取源文件
    log("Step 1: 读取 v7 源文件...")
    html = read_v7()
    if not html:
        print("\n  ERROR: v7 文件不存在\n")
        sys.exit(1)
    
    # Step 2: 加载配置
    log("Step 2: 加载配置...")
    cfg = load_config()
    if not cfg:
        print("\n  ERROR: 配置文件不存在\n")
        sys.exit(1)
    
    # Step 3: 注入配置
    log("Step 3: 注入配置...")
    html = inject_config(html, cfg)
    
    # Step 4: 注入预约 Hook
    log("Step 4: 注入预约 Hook...")
    html = inject_booking_hook(html)
    
    # Step 5: 推送 GitHub
    log("Step 5: 推送 GitHub...")
    success = git_publish(html)
    
    print()
    if success:
        print("  ✅ 部署成功！")
        print(f"  🌐 {PAGES_URL}")
        print(f"  ⏳ GitHub Pages 1-2 分钟后更新")
        print(f"  📋 预约服务: http://localhost:8081/admin")
    else:
        print("  ❌ 部署失败，请检查 git 错误信息")
    
    print()


if __name__ == "__main__":
    main()
