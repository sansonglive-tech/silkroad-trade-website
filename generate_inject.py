import re

# Read the current admin_server.py
with open("C:/Users/ASDCF/.qclaw/workspace/admin_server.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find the current inject_script within inject_config
start_marker = "inject_script = '''"
idx = content.find(start_marker)
end_idx = content.find("</script>'''", idx)

if idx < 0:
    print("ERROR: inject_script not found!")
else:
    end_j = end_idx + len("</script>'''")
    print(f"Found inject_script at {idx}-{end_j}")

# Build the comprehensive injection script
inject = """
<script>
// Config-driven DOM update - injected by admin server
(function(){
var c = CONFIG;
if(!c) return;

// --- Update title ---
var titleEl = document.querySelector('title');
if(titleEl) titleEl.textContent = c.company.name + ' - ' + c.company.slogan;

// --- Update footer ---
var footerEls = document.querySelectorAll('.footer-bottom span');
footerEls.forEach(function(el){
  if(el.textContent.indexOf('\\u00a9') >= 0 || el.textContent.indexOf('(c)') >= 0 || el.textContent.indexOf('All rights') >= 0) {
    el.textContent = '\\u00a9 ' + new Date().getFullYear() + ' ' + c.company.name + '. All rights reserved.';
  }
  if(el.textContent.indexOf('ICP') >= 0 || el.textContent.indexOf('\\u7ca4') >= 0) {
    if(c.company.icp) el.textContent = c.company.icp;
  }
});

// --- Update email links ---
document.querySelectorAll('a[href^="mailto:"]').forEach(function(el){
  if(c.company.email) el.href = 'mailto:' + c.company.email;
});

// --- Render services from CONFIG ---
var servicesGrid = document.querySelector('.services-grid');
if(servicesGrid && c.services && c.services.length > 0) {
  var colors = [
    'linear-gradient(135deg,#C44536,#8B2D1E)',
    'linear-gradient(135deg,#C8923E,#8B6914)',
    'linear-gradient(135deg,#1A1512,#302824)',
    'linear-gradient(135deg,#6B625C,#A89E96)',
    'linear-gradient(135deg,#C44536,#C8923E)',
    'linear-gradient(135deg,#302824,#6B625C)'
  ];
  var emojis = ['\\ud83c\\udfed','\\ud83d\\udccb','\\u2696\\ufe0f','\\ud83d\\udee1\\ufe0f','\\ud83c\\udf10','\\ud83d\\udee2\\ufe0f'];
  servicesGrid.innerHTML = c.services.map(function(s, i){
    var bg = colors[i % colors.length];
    var emoji = emojis[i % emojis.length];
    var sub = s.sub || '';
    return '<div class="service-card" onclick="openDetail(\\'' + (s.detailId || s.id) + '\\')">' +
      '<div class="sc-img"><div class="sc-img-bg" style="background:' + bg + '"></div><span>' + emoji + '</span></div>' +
      '<h3>' + s.title + '</h3>' +
      (sub ? '<div class="sc-sub">' + sub + '</div>' : '') +
      '<p>' + s.desc + '</p></div>';
  }).join('');
}

// --- Render stats from CONFIG ---
var statsInner = document.querySelector('.stats-inner');
if(statsInner && c.stats && c.stats.length > 0) {
  statsInner.innerHTML = c.stats.map(function(s){
    return '<div class="stat-item"><div class="num">' + (s.num || '') + '</div><div class="label">' + (s.label || '') + '</div></div>';
  }).join('');
}

// --- Render policies from CONFIG ---
var policyGrid = document.querySelector('.policy-grid');
if(policyGrid && c.policies && c.policies.length > 0) {
  policyGrid.innerHTML = c.policies.map(function(p, i){
    var n = String(i + 1).padStart(2, '0');
    return '<div class="policy-card" onclick="openDetail(\\'' + (p.detailId || p.id) + '\\')">' +
      '<div class="pn">' + n + '</div>' +
      '<div><h3>' + p.title + '</h3><p>' + (p.desc || '') + '</p></div></div>';
  }).join('');
}

// --- Render testimonials from CONFIG ---
var testGrid = document.querySelector('.testimonials-grid');
if(testGrid && c.testimonials && c.testimonials.length > 0) {
  testGrid.innerHTML = c.testimonials.map(function(t, i){
    var name = t.name || '';
    var role = t.role || '';
    var text = t.text || '';
    var avatar = t.avatar || (name ? name.charAt(0) : '\\ud83d\\udc64');
    return '<div class="t-card" onclick="openDetail(\\'' + (t.detailId || ('case-' + i)) + '\\')">' +
      '<div class="tq">&ldquo;</div>' +
      '<p class="t-text">' + text + '</p>' +
      '<div class="t-author"><div class="t-av">' + avatar + '</div>' +
      '<div><div class="t-name">' + name + '</div><div class="t-role">' + role + '</div></div></div></div>';
  }).join('');
}

// --- Render process from CONFIG ---
var processGrid = document.querySelector('.process-grid');
if(processGrid && c.process && c.process.length > 0) {
  processGrid.innerHTML = c.process.map(function(p){
    return '<div class="pstep" onclick="openDetail(\\'' + (p.detailId || ('process-step' + p.num)) + '\\')">' +
      '<div class="ring"><div class="n">' + (p.num || '') + '</div></div>' +
      '<h3>' + (p.title || '') + '</h3><p>' + (p.desc || '') + '</p></div>';
  }).join('');
}

// --- Update SLIDE_CONFIG from CONFIG.slides ---
if(c.slides && c.slides.length > 0) {
  // Override the global SLIDE_CONFIG
  var newSlides = c.slides.map(function(s, i){
    var titleHtml = s.title;
    // Ensure gold spans are preserved
    if(titleHtml && titleHtml.indexOf('<span') < 0) {
      // Auto-wrap last 4 chars in gold if no html tags
      var parts = titleHtml.split(/(\\S+)/);
      if(parts.length > 1) {
        var lastWord = parts[parts.length - 1] || titleHtml;
        titleHtml = titleHtml.slice(0, -lastWord.length) + '<span class="gold">' + lastWord + '</span>';
      }
    }
    return {
      id: s.id || ('slide-' + (i+1)),
      title: titleHtml || '',
      subtitle: s.subtitle || '',
      desc: s.desc || '',
      img: s.img || '',
      detailId: s.detailId || ''
    };
  });
  // Replace SLIDE_CONFIG globally
  window.SLIDE_CONFIG = newSlides;
  // Re-render slide 0 if updateSlide function exists
  if(typeof updateSlide === 'function') {
    currentSlide = 0;
    updateSlide();
  }
}

// --- Update logo text ---
var logoNames = document.querySelectorAll('.logo-text strong');
logoNames.forEach(function(el){
  if(c.company.name) el.textContent = c.company.name;
});
var logoSlogans = document.querySelectorAll('.logo-text span');
logoSlogans.forEach(function(el){
  if(c.company.slogan && (!el.textContent || el.textContent.indexOf('SILK') >= 0)) {
    el.textContent = c.company.slogan;
  }
});

{% raw %}console.log('[Config Inject] Applied CONFIG to DOM');{% endraw %}
})();
</script>"""

print(f"New script length: {len(inject)} chars")
print(f"Inject script contains backticks: {'`' in inject}")
print(f"Inject script contains template literals: {'${' in inject}")

# Also check if there are any issues with quotes
backslash_issues = inject.count("\\'")
print(f"Escaped single quotes: {backslash_issues}")
