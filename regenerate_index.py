#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json, sys

WORKSPACE = r'C:\Users\ASDCF\.qclaw\workspace'
V7_FILE = os.path.join(WORKSPACE, "silkroad-trade_v7_silk_poster.html")
CFG_FILE = os.path.join(WORKSPACE, "site_config.json")
INDEX_FILE = os.path.join(WORKSPACE, "index.html")

# 读取 v7 文件
with open(V7_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# 读取配置
with open(CFG_FILE, 'r', encoding='utf-8') as f:
    cfg = json.load(f)

# 替换 CONFIG
js_config = json.dumps(cfg, ensure_ascii=False, indent=2)
marker = 'const CONFIG = '
idx = html.find(marker)
if idx >= 0:
    brace_idx = html.find('{', idx)
    depth = 0
    end = brace_idx
    for i in range(brace_idx, len(html)):
        if html[i] == '{': depth += 1
        elif html[i] == '}': depth -= 1
        if depth == 0: end = i + 1; break
    
    new_html = html[:idx] + f'const CONFIG = {js_config};' + html[end:]
    
    # 添加 INJECT_SCRIPT
    inject_script = '''
<script>
(function(){
  console.log('[Config Inject] Starting...');
  var c = (typeof CONFIG !== 'undefined') ? CONFIG : {};
  
  // --- Update company info ---
  if(c.company) {
    document.querySelectorAll('.logo-text strong').forEach(function(el){ if(c.company.name) el.textContent = c.company.name; });
    document.querySelectorAll('.logo-text span').forEach(function(el){ if(c.company.slogan) el.textContent = c.company.slogan.toUpperCase(); });
    document.querySelectorAll("a[href^='mailto:]").forEach(function(el){ if(c.company.email) { el.href = 'mailto:' + c.company.email; el.textContent = c.company.email; } });
  }
  
  // --- Render services from CONFIG ---
  if(c.services && c.services.length) {
    var sg = document.querySelector('.services-grid');
    if(sg) {
      sg.innerHTML = c.services.map(function(s) {
        return '<div class="service-card" onclick="openDetail(\'' + (s.detailId || s.id) + '\')">' +
          '<div class="service-icon">' + (s.icon || '') + '</div>' +
          '<h3>' + (s.title || '') + '</h3>' +
          '<div class="service-sub">' + (s.sub || '') + '</div>' +
          '<p>' + (s.desc || '') + '</p>' +
          '</div>';
      }).join('');
    }
  }
  
  // --- Render stats from CONFIG ---
  if(c.stats && c.stats.length) {
    var sb = document.querySelector('.stats-row');
    if(sb) {
      sb.innerHTML = c.stats.map(function(st) {
        return '<div class="stat-item"><div class="stat-num">' + (st.num || '') + '</div><div class="stat-label">' + (st.label || '') + '</div></div>';
      }).join('');
    }
  }
  
  // --- Render policies from CONFIG ---
  if(c.policies && c.policies.length) {
    var pg = document.querySelector('.policy-grid');
    if(pg) {
      pg.innerHTML = c.policies.map(function(p, i) {
        var detailIds = ['policy-research', 'policy-network', 'policy-park', 'policy-finance'];
        return '<div class="policy-card" onclick="openDetail(\'' + detailIds[i] + '\')">' +
          '<div class="pn">' + (p.num || '') + '</div>' +
          '<div><h3>' + (p.title || '') + '</h3><p>' + (p.desc || '') + '</p></div>' +
          '</div>';
      }).join('');
    }
  }
  
  // --- Render testimonials from CONFIG ---
  if(c.testimonials && c.testimonials.length) {
    var tg = document.querySelector('.testimonials-grid');
    if(tg) {
      tg.innerHTML = c.testimonials.map(function(t) {
        return '<div class="testimonial-card">' +
          '<div class="quote">' + (t.text || '') + '</div>' +
          '<div class="author"><div class="avatar">' + (t.avatar || '') + '</div><div><strong>' + (t.name || '') + '</strong><span>' + (t.role || '') + '</span></div></div>' +
          '</div>';
      }).join('');
    }
  }
  
  // --- Render process from CONFIG ---
  if(c.process && c.process.length) {
    var pr = document.querySelector('.process-steps');
    if(pr) {
      pr.innerHTML = c.process.map(function(p, i) {
        var detailIds = ['process-step1', 'process-step2', 'process-step3', 'process-step4'];
        return '<div class="pstep" onclick="openDetail(\'' + detailIds[i] + '\')">' +
          '<div class="ring"><div class="n">' + (p.num || '') + '</div></div>' +
          '<h4>' + (p.title || '') + '</h4>' +
          '<p>' + (p.desc || '') + '</p>' +
          '</div>';
      }).join('');
    }
  }
  
  console.log('[Config Inject] Applied CONFIG to DOM');
})();
</script>
'''
    new_html = new_html.replace('</body>', inject_script + '</body>')
    
    # 写入文件，使用 UTF-8 编码
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f'SUCCESS: index.html regenerated with UTF-8 encoding ({len(new_html):,} chars)')
else:
    print('ERROR: Could not find CONFIG marker')
