const fs = require('fs');

const filePath = 'C:\\Users\\ASDCF\\.qclaw\\workspace\\silkroad-trade_v4_silk_poster.html';
let html = fs.readFileSync(filePath, 'utf8');

// 1. 修改标题
html = html.replace('<title>丝路山海通 — 一带一路企业出海一站式服务</title>', '<title>丝路山海通 v4 — 一带一路企业出海一站式服务</title>');

// 2. 修改导航栏"预约演示"为"立即预约"
html = html.replace('<a href="#contact" class="nav-cta">预约演示</a>', '<a href="#" class="nav-cta" onclick="event.preventDefault();openBook();">立即预约</a>');

// 3. 修改底部CTA"预约演示"为"立即咨询"
html = html.replace(/预约演示/g, '立即咨询');

// 4. 修改客户案例卡片为独立入口
html = html.replace("openDetail('client-cases')">帮我们在雅加达", "openDetail('case-zhang')">帮我们在雅加达");
html = html.replace("openDetail('client-cases')">响应一带一路", "openDetail('case-li')">响应一带一路");
html = html.replace("openDetail('client-cases')">印尼的SNI", "openDetail('case-wang')">印尼的SNI");

// 5. 修改政策卡片为独立入口
html = html.replace(/openDetail\('policy-overview'\)/g, "openDetail('policy-research')");
html = html.replace(/openDetail\('policy-research'\)/, "openDetail('policy-research')");
html = html.replace(/openDetail\('policy-research'\)(.*?)02/, "openDetail('policy-network')$102");
html = html.replace(/openDetail\('policy-network'\)(.*?)03/, "openDetail('policy-park')$103");
html = html.replace(/openDetail\('policy-park'\)(.*?)04/, "openDetail('policy-finance')$104");

console.log('Basic replacements done');

fs.writeFileSync(filePath, html, 'utf8');
console.log('File saved');
