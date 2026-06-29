    def inject_config(self, html):
        """Replace the hardcoded CONFIG in v7 with site_config.json data.
        Also append a JS block that updates the HTML body with CONFIG values."""
        cfg = load_cfg()
        js_config = self.to_js(cfg)

        # Inject JS to update page with config data
        inject_script = '''
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
  if(txt.indexOf("\u00a9") >= 0 || txt.indexOf("All rights") >= 0) {
    el.textContent = "\u00a9 " + new Date().getFullYear() + " " + c.company.name + ". All rights reserved.";
  }
  if(txt.indexOf("ICP") >= 0 || txt.indexOf("\u7ca4") >= 0) {
    if(c.company.icp) el.textContent = c.company.icp;
  }
});

// --- Update email ---
document.querySelectorAll("a[href^='mailto:']").forEach(function(el){
  if(c.company.email) el.href = "mailto:" + c.company.email;
});

// --- Render services from CONFIG ---
var sg = document.querySelector(".services-grid");
if(sg && c.services && c.services.length > 0) {
  var cols = ["linear-gradient(135deg,#C44536,#8B2D1E)","linear-gradient(135deg,#C8923E,#8B6914)","linear-gradient(135deg,#1A1512,#302824)","linear-gradient(135deg,#6B625C,#A89E96)","linear-gradient(135deg,#C44536,#C8923E)","linear-gradient(135deg,#302824,#6B625C)"];
  var ems = ["\ud83c\udfed","\ud83d\udccb","\u2696\ufe0f","\ud83d\udee1\ufe0f","\ud83c\udf10","\ud83d\udee2\ufe0f"];
  sg.innerHTML = c.services.map(function(s,i){
    return '<div class="service-card" onclick="openDetail(\'' + (s.detailId || s.id) + '\')">' +
      '<div class="sc-img"><div class="sc-img-bg" style="background:' + cols[i % cols.length] + '"></div><span>' + (ems[i % ems.length]) + '</span></div>' +
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
    return '<div class="policy-card" onclick="openDetail(\'' + (p.detailId || p.id) + '\')">' +
      '<div class="pn">' + n + '</div><div>' +
      '<h3>' + p.title + '</h3><p>' + (p.desc || '') + '</p></div></div>';
  }).join('');
}

// --- Render testimonials from CONFIG ---
var tg = document.querySelector(".testimonials-grid");
if(tg && c.testimonials && c.testimonials.length > 0) {
  tg.innerHTML = c.testimonials.map(function(t, i){
    var av = t.avatar || (t.name ? t.name.charAt(0) : "\ud83d\udc64");
    return '<div class="t-card" onclick="openDetail(\'' + (t.detailId || ('case-' + i)) + '\')">' +
      '<div class="tq">&ldquo;</div><p class="t-text">' + (t.text || '') + '</p>' +
      '<div class="t-author"><div class="t-av">' + av + '</div><div>' +
      '<div class="t-name">' + (t.name || '') + '</div><div class="t-role">' + (t.role || '') + '</div></div></div></div>';
  }).join('');
}

// --- Render process from CONFIG ---
var pr = document.querySelector(".process-grid");
if(pr && c.process && c.process.length > 0) {
  pr.innerHTML = c.process.map(function(p){
    return '<div class="pstep" onclick="openDetail(\'' + (p.detailId || ('process-step' + p.num)) + '\')">' +
      '<div class="ring"><div class="n">' + (p.num || '') + '</div></div>' +
      '<h3>' + (p.title || '') + '</h3><p>' + (p.desc || '') + '</p></div>';
  }).join('');
}

// --- Update SLIDE_CONFIG from CONFIG.slides ---
if(c.slides && c.slides.length > 0) {
  var newSlides = c.slides.map(function(s, i){
    return {
      id: s.id || ('slide-' + (i+1)),
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
</script>'''

        # Replace const CONFIG = {...};
        pattern = re.compile(r"const\s+CONFIG\s*=\s*\{[^;]+?\};", re.DOTALL)
        new_block = "const CONFIG = " + js_config + ";"
        result = pattern.sub(new_block, html)
        if result == html:
            print("[inject_config] WARNING: no CONFIG block found in v7")
        else:
            # Inject update script before </body>
            result = result.replace("</body>", inject_script + "</body>")
        return result
