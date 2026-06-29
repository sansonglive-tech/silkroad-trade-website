#!/usr/bin/env python3
"""Rebuild v5 from v3 with all enhancements — DETAIL_CONTENT images, modals, fixes."""
import re

with open('silkroad-trade_v3_silk_poster.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================
# 1. ADD DETAIL OVERLAY CSS before </style>
# ============================================================
detail_css = '''
/* ========== DETAIL OVERLAY - 弹出详情页 ========== */
.detail-overlay{position:fixed;inset:0;z-index:1000;background:rgba(0,0,0,0.6);backdrop-filter:blur(4px);display:none;align-items:center;justify-content:center;padding:2rem;animation:detailFadeIn .3s ease}
.detail-overlay.active{display:flex}
.detail-modal{background:var(--cream);border-radius:var(--radius-lg);width:100%;max-width:680px;max-height:85vh;overflow:hidden;display:flex;flex-direction:column;box-shadow:var(--shadow-xl);animation:detailSlideUp .35s var(--ease)}
@keyframes detailFadeIn{from{opacity:0}to{opacity:1}}
@keyframes detailSlideUp{from{opacity:0;transform:translateY(40px) scale(.97)}to{opacity:1;transform:translateY(0) scale(1)}}
.detail-header{display:flex;align-items:center;justify-content:space-between;padding:1.2rem 1.5rem;border-bottom:.5px solid var(--border);flex-shrink:0;background:var(--cream)}
.detail-header h3{font-family:'Noto Serif SC',serif;font-size:1rem;font-weight:700;color:var(--ink)}
.dh-sub{font-size:.48rem;letter-spacing:.3em;color:var(--gray-light);text-transform:uppercase;margin-top:2px}
.detail-close{background:none;border:none;font-size:1.2rem;color:var(--gray);cursor:pointer;width:32px;height:32px;display:flex;align-items:center;justify-content:center;border-radius:50%;transition:.3s}
.detail-close:hover{background:var(--red-soft);color:var(--red)}
.detail-body{overflow-y:auto;padding:0;flex:1}
.detail-body::-webkit-scrollbar{width:4px}
.detail-body::-webkit-scrollbar-thumb{background:var(--gray-soft);border-radius:2px}

/* DH Hero Banner */
.dh-hero{position:relative;height:200px;overflow:hidden;background:var(--ink-soft)}
.dh-hero img{width:100%;height:100%;object-fit:cover;display:block}
.dh-hero-code{position:absolute;bottom:12px;left:20px;font-family:'Ma Shan Zheng',cursive;font-size:1.8rem;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,0.4);letter-spacing:.05em;z-index:2}
.dh-hero-overlay{position:absolute;inset:0;background:linear-gradient(180deg,transparent 50%,rgba(26,21,18,0.6) 100%);z-index:1}

/* DH Intro */
.dh-intro{color:var(--gray);font-size:.82rem;line-height:1.8;padding:1.2rem 1.5rem;border-bottom:.5px solid var(--border);background:var(--cream-soft)}

/* DH Heading */
.dh-heading{font-family:'Noto Serif SC',serif;font-weight:600;font-size:.85rem;color:var(--red);padding:.8rem 1.5rem 0;margin-top:.3rem;letter-spacing:.02em}
.dh-heading::before{content:'\u25C6 ';color:var(--gold);font-size:.75rem}

/* Detail body lists */
.detail-body ul{padding:.3rem 1.5rem .8rem;list-style:none}
.detail-body ul li{position:relative;padding-left:1.2rem;color:var(--ink-soft);font-size:.8rem;line-height:1.8}
.detail-body ul li::before{content:'\u25C6';position:absolute;left:0;color:var(--gold);font-size:.55rem;top:.5em}

/* Detail Grid (data cards) */
.detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:.6rem;padding:0 1.5rem 1rem}
.detail-item{background:var(--red-soft);border-radius:var(--radius);padding:.7rem 1rem;text-align:center}
.detail-item strong{display:block;font-family:'Noto Serif SC',serif;font-size:1.1rem;color:var(--red);font-weight:700}
.detail-item span{font-size:.65rem;color:var(--gray);letter-spacing:.02em}

/* Detail CTA Bar */
.detail-cta-bar{display:flex;gap:.6rem;padding:1rem 1.5rem 1.5rem;border-top:.5px solid var(--border);margin-top:.5rem}
.detail-cta-bar .btn-primary{font-size:.72rem;padding:.5rem 1.2rem}
.detail-cta-bar .btn-outline{font-size:.72rem;padding:.5rem 1.2rem}

/* ========== BOOKING MODAL ========== */
.modal-overlay{position:fixed;inset:0;z-index:2000;background:rgba(0,0,0,0.6);backdrop-filter:blur(4px);display:none;align-items:center;justify-content:center;padding:2rem}
.modal-overlay.active{display:flex}
.modal-box{background:var(--cream);border-radius:var(--radius-lg);padding:2rem;max-width:420px;width:100%;box-shadow:var(--shadow-xl);animation:detailSlideUp .35s var(--ease);position:relative}
.modal-box .detail-close{position:absolute;top:12px;right:12px}
.modal-box h3{font-family:'Noto Serif SC',serif;font-size:1.1rem;font-weight:700;margin-bottom:1rem;color:var(--ink)}
.modal-box p{color:var(--gray);font-size:.82rem;line-height:1.8;margin-bottom:1.2rem}
.modal-input{width:100%;padding:.7rem 1rem;border:1px solid var(--border);border-radius:var(--radius);font-size:.82rem;color:var(--ink);background:var(--cream-soft);margin-bottom:.8rem;outline:none;transition:.3s;font-family:inherit}
.modal-input:focus{border-color:var(--gold);box-shadow:0 0 0 2px var(--gold-soft)}
.modal-input::placeholder{color:var(--gray-light)}
.modal-submit{width:100%;background:var(--red);color:#fff;border:none;padding:.8rem;border-radius:var(--radius);font-weight:600;font-size:.85rem;cursor:pointer;transition:.3s}
.modal-submit:hover{background:var(--red-dark)}
.modal-close-text{text-align:center;margin-top:.6rem}
.modal-close-text a{color:var(--gray-light);font-size:.72rem;text-decoration:none;cursor:pointer}
.modal-close-text a:hover{color:var(--red)}
@media(max-width:768px){
  .dh-hero{height:140px}
  .detail-grid{grid-template-columns:1fr}
  .detail-cta-bar{flex-wrap:wrap}
  .detail-cta-bar .btn-primary,.detail-cta-bar .btn-outline{width:100%;justify-content:center}
}
'''

# Insert detail CSS before </style>
html = html.replace('</style>', detail_css + '\n</style>')

# ============================================================
# 2. REPLACE DETAIL_CONTENT with rich content (with images)
# ============================================================

# Build rich detail content
DETAIL_CONTENT = {
    'company-advantage': {'title': '公司优势', 'subtitle': '为什么选择丝路山海通', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">ADV</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">丝路山海通专注一带一路沿线国家，深耕东南亚、中亚、中东、非洲等新兴市场，为企业出海提供一站式落地服务。</div><div class="dh-heading">深耕一带一路</div><ul><li>覆盖60+一带一路沿线国家</li><li>400+海外本地员工</li><li>丰富的本地化经验和政商资源</li></ul><div class="dh-heading">专业本地团队</div><ul><li>熟悉当地法律、税务、文化</li><li>真正接地气的落地服务</li><li>7×24小时响应支持</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">立即咨询</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'company-reg': {'title': '公司注册与资质', 'subtitle': 'incorporation & licensing', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1560179707-f14e90ef3623?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">REG</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">协助企业在目标国家完成公司注册、营业执照激活、行业资质办理，最快7个工作日完成海外公司设立。</div><div class="dh-heading">境内公司注册</div><ul><li>名称核准、章程制定、股东登记</li><li>全套流程一站式服务</li></ul><div class="detail-grid"><div class="detail-item"><strong>7个工作日</strong><span>最快完成公司设立</span></div><div class="detail-item"><strong>60+国家</strong><span>覆盖一带一路沿线</span></div></div><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">预约办理</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'tax-legal': {'title': '财税人事与法务', 'subtitle': 'tax, hr & legal', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">TAX</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">根据当地税法为企业制定最优财税方案，提供代理记账、人事雇佣、法务咨询等全方位服务。</div><div class="dh-heading">财税筹划</div><ul><li>制定最优财税方案</li><li>合理避税，降低成本</li></ul><div class="dh-heading">代理记账</div><ul><li>记账、报税、年审</li><li>全套财务服务</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">预约咨询</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'certification': {'title': '产品准入与认证', 'subtitle': 'product certification', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">CERT</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">SNI认证、BPOM注册、清真认证、进出口许可证等全套产品合规准入服务。</div><div class="dh-heading">SNI认证（印尼）</div><ul><li>印尼国家标准认证</li><li>产品进入印尼市场必备</li></ul><div class="dh-heading">清真认证</div><ul><li>穆斯林市场必备资质</li><li>开拓东南亚、中东市场</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">办理认证</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'local-ops': {'title': '本地化运营支持', 'subtitle': 'local operation', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">OPS</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">行政办公、本地招聘、政府关系、行业资源对接，让企业真正扎根海外市场。</div><div class="dh-heading">行政办公</div><ul><li>办公室租赁</li><li>办公手续办理</li></ul><div class="dh-heading">本地招聘</div><ul><li>本地渠道招聘</li><li>薪酬体系制定</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">获取方案</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'visa': {'title': '签证与商务考察', 'subtitle': 'visa & business trip', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">VISA</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">商务签证、工作签证、工厂考察、市场调研，一站式行程安排。</div><div class="dh-heading">商务签证</div><ul><li>最快5个工作日出签</li><li>多次往返类型</li></ul><div class="detail-grid"><div class="detail-item"><strong>5个工作日</strong><span>最快出签</span></div><div class="detail-item"><strong>20+国家</strong><span>签证覆盖</span></div></div><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">预约考察</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'factory': {'title': '建厂与工程服务', 'subtitle': 'factory & construction', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">FACT</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">海外选址建厂、建筑工程许可、环境合规、能源矿产，全流程服务。</div><div class="dh-heading">海外选址建厂</div><ul><li>工业园区考察</li><li>土地谈判、环保评估</li></ul><div class="dh-heading">建筑工程许可</div><ul><li>建筑施工许可</li><li>消防审批</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">建厂咨询</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'policy-overview': {'title': '政策与落地支持', 'subtitle': 'policy & support', 'content': '<div class="dh-hero"><div class="dh-hero-code">BRI</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">专业团队追踪分析沿线国家最新外资政策、税收优惠、产业扶持措施，为企业出海提供精准政策导航。</div><div class="dh-heading">政策研究与解读</div><ul><li>追踪分析沿线国家外资政策</li><li>税收优惠、产业扶持措施</li><li>精准政策导航</li></ul><div class="dh-heading">政府与商会对接</div><ul><li>深度链接当地政府、使领馆</li><li>华人商会资源对接</li><li>建立高层级政商关系</li></ul><div class="dh-heading">产业园区落地</div><ul><li>对接产业园区、经济特区</li><li>税收减免、土地优惠</li><li>政策红利最大化</li></ul><div class="dh-heading">投融资对接</div><ul><li>对接丝路基金、亚投行</li><li>国开行等金融机构</li><li>出海项目资金支持</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询政策</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'service-process': {'title': '服务流程', 'subtitle': 'service process', 'content': '<div class="dh-hero"><div class="dh-hero-code">FLOW</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">标准化四步流程，从需求诊断到持续运营，全程陪伴企业出海。</div><div class="dh-heading">01 需求诊断</div><ul><li>深入了解企业出海目标与需求</li><li>定制化出海方案</li></ul><div class="dh-heading">02 尽职调研</div><ul><li>市场调研、法律评估、财税分析</li><li>规避风险前置</li></ul><div class="dh-heading">03 落地执行</div><ul><li>公司注册、资质办理、团队搭建</li><li>全程陪伴推进</li></ul><div class="dh-heading">04 持续运营</div><ul><li>财税代账、法务支持、政府维护</li><li>长期运营保障</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">开启服务</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'client-cases': {'title': '客户案例', 'subtitle': 'client cases', 'content': '<div class="dh-hero"><div class="dh-hero-code">CASES</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">听听他们如何借助丝路山海通成功落地海外市场。</div><div class="dh-heading">张宏伟 · 印尼工厂负责人</div><ul><li>新能源汽车行业</li><li>2个月完成公司注册和工厂选址</li><li>"当地团队专业靠谱"</li></ul><div class="dh-heading">李雪峰 · 中亚事业部总经理</div><ul><li>工程机械行业</li><li>从法律合规到政府关系一路护航</li><li>"节省了大量试错成本"</li></ul><div class="dh-heading">王琳 · 海外拓展总监</div><ul><li>食品饮料行业</li><li>SNI认证和清真认证一站式包办</li><li>"产品准入周期缩短了60%"</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">联系我们</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'about': {'title': '关于丝路山海通', 'subtitle': 'silk road trade', 'content': '<div class="dh-hero"><div class="dh-hero-code">ABOUT</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">让企业出海不再难，促进中国与一带一路国家经贸交往，互利共赢。</div><div class="dh-heading">我们的使命</div><ul><li>让企业出海不再难</li><li>促进一带一路经贸交往</li><li>互利共赢</li></ul><div class="dh-heading">我们的愿景</div><ul><li>成为中国企业出海首选服务伙伴</li><li>陪伴更多中国企业走向世界</li></ul><div class="dh-heading">我们的价值观</div><ul><li>专业、诚信、高效、共赢</li><li>以客户需求为中心</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">联系我们</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'region-sea': {'title': '东南亚区域', 'subtitle': 'southeast asia', 'content': '<div class="dh-hero"><div class="dh-hero-code">SEA</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">覆盖印尼、越南、菲律宾、泰国、新加坡五大核心市场，是中国企业出海最成熟的区域。</div><div class="dh-heading">核心服务</div><ul><li>外商独资公司注册</li><li>海关与进出口资质</li><li>本地招聘与人事外包</li><li>税务与法务支持</li><li>产业园区入驻</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询东南亚</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'region-ru': {'title': '俄语区/中亚区域', 'subtitle': 'cis & central asia', 'content': '<div class="dh-hero"><div class="dh-hero-code">CIS</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">覆盖哈萨克斯坦、乌兹别克斯坦、吉尔吉斯斯坦、塔吉克斯坦、俄罗斯五国。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与经营许可</li><li>矿产资源投资合作</li><li>EAC/CUTR认证办理</li><li>工作签证与劳动配额</li><li>海关清关与物流</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询俄语区/中亚</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'region-me': {'title': '中东/非洲区域', 'subtitle': 'middle east & africa', 'content': '<div class="dh-hero"><div class="dh-hero-code">MEA</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">覆盖阿联酋、沙特、埃及、尼日利亚、肯尼亚。</div><div class="dh-heading">阿联酋·沙特</div><ul><li>自由区公司注册</li><li>MISA投资许可、SABER/SASO认证</li></ul><div class="dh-heading">非洲三国</div><ul><li>埃及、尼日利亚、肯尼亚</li><li>产品认证、政府关系、公司注册</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询中东非洲</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'region-eu': {'title': '欧洲区域', 'subtitle': 'europe', 'content': '<div class="dh-hero"><div class="dh-hero-code">EU</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">覆盖德国、荷兰、波兰，深耕制造业、IT外包、物流贸易领域。</div><div class="dh-heading">德国</div><ul><li>柏林与汉堡双中心</li><li>GmbH注册、VAT税务、CE认证</li></ul><div class="dh-heading">荷兰·波兰</div><ul><li>欧洲物流枢纽</li><li>BV/Sp. z o.o.注册、投资特区优惠</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询欧洲</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-id': {'title': '印度尼西亚', 'subtitle': 'indonesia', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">IDN</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">印尼是东南亚最大经济体，中国企业出海首选目的地之一。三大服务中心覆盖全境。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与营业执照激活</li><li>SNI认证、BPOM注册、清真认证</li><li>财税代账与法务支持</li><li>建厂许可与环境合规</li><li>本地招聘与人事管理</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询印尼</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-vn': {'title': '越南', 'subtitle': 'vietnam', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1528127269322-539801943592?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">VNM</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">越南凭借优越地理位置和劳动力成本优势，已吸引大量制造业转移。胡志明与河内双中心覆盖南北经济走廊。</div><div class="dh-heading">核心服务</div><ul><li>外商独资公司注册</li><li>进出口权办理</li><li>本地招聘与社保代缴</li><li>税务合规与代理记账</li><li>工厂选址与环境评估</li><li>投资许可证申请</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询越南</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-ph': {'title': '菲律宾', 'subtitle': 'philippines', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1518509562904-e7ef99cdcc86?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">PHL</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">菲律宾英语普及率高、劳动力充足，是全球BPO中心和新兴制造业基地。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与SEC备案</li><li>BPO企业设立</li><li>税务合规与财务服务</li><li>本地招聘与人事外包</li><li>BOI投资优惠申请</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询菲律宾</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-th': {'title': '泰国', 'subtitle': 'thailand', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">THA</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">泰国是东盟第二大经济体，汽车制造和食品加工产业领先。曼谷服务中心提供全方位出海落地服务。</div><div class="dh-heading">核心服务</div><ul><li>BOI投资促进申请</li><li>外商经营许可证</li><li>公司注册与工厂许可</li><li>工作签证办理</li><li>本地招聘与薪酬管理</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询泰国</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-sg': {'title': '新加坡', 'subtitle': 'singapore', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">SGP</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">新加坡是全球金融中心和东南亚区域总部首选地，提供高端商务与跨境服务。</div><div class="dh-heading">核心服务</div><ul><li>私人有限公司注册</li><li>税务筹划与IRAS合规</li><li>银行开户与融资对接</li><li>国际贸易合规</li><li>知识产权保护</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询新加坡</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-kz': {'title': '哈萨克斯坦', 'subtitle': 'kazakhstan', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1542259681-d4cd4e5b3c5f?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">KAZ</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">哈萨克斯坦是中亚最大经济体，一带一路首倡之地。阿拉木图与阿斯塔纳双中心。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与营业执照</li><li>矿产资源投资许可</li><li>海关清关与贸易合规</li><li>工作许可与本地招聘</li><li>合资企业设立</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询哈萨克斯坦</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-uz': {'title': '乌兹别克斯坦', 'subtitle': 'uzbekistan', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">UZB</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">乌兹别克斯坦近年改革开放力度大，经济特区政策优惠，市场潜力可观。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与经营许可</li><li>经济特区入驻与优惠申请</li><li>税务登记与优惠政策对接</li><li>进出口权办理</li><li>本地代理和分销网络搭建</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询乌兹别克斯坦</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-kg': {'title': '吉尔吉斯斯坦', 'subtitle': 'kyrgyzstan', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">KGZ</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">吉尔吉斯斯坦是欧亚经济联盟成员国，可作为进入俄白哈市场的桥头堡。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与税务登记</li><li>EAC认证办理</li><li>海关清关与物流</li><li>劳动配额与工作许可</li><li>农业合作与投资</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询吉尔吉斯斯坦</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-tj': {'title': '塔吉克斯坦', 'subtitle': 'tajikistan', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">TJK</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">塔吉克斯坦是中亚新兴市场，水电资源和矿产资源丰富。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与经营许可</li><li>矿产资源合作协议支持</li><li>基建工程竞标支持</li><li>签证与工作许可办理</li><li>本地法律与税务咨询</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询塔吉克斯坦</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-ru': {'title': '俄罗斯', 'subtitle': 'russia', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1513326738677-b964603b136d?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">RUS</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">俄罗斯是横跨欧亚的超级市场，莫斯科与圣彼得堡双中心提供全面的市场准入和本地运营服务。</div><div class="dh-heading">核心服务</div><ul><li>公司注册（OOO/代表处）</li><li>EAC/CUTR认证办理</li><li>VAT税务登记与合规申报</li><li>海关清关与物流方案</li><li>商标注册与知识产权保护</li><li>本地招聘与法务支持</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询俄罗斯</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-ae': {'title': '阿联酋', 'subtitle': 'united arab emirates', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">ARE</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">阿联酋是中东商贸枢纽和金融中心，自由区政策为中国企业提供了快速落地和中东市场辐射的绝佳平台。</div><div class="dh-heading">核心服务</div><ul><li>自由区公司注册（FZE/FZCO）</li><li>离岸公司设立</li><li>营业执照与经营许可</li><li>银行开户与金融合规</li><li>VAT税务登记与申报</li><li>本地保人/代理服务</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询阿联酋</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-sa': {'title': '沙特阿拉伯', 'subtitle': 'saudi arabia', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1565019011521-6cb040f3e1f5?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">SAU</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">沙特2030愿景推动经济全面开放和多元化转型，带来大量投资机遇。</div><div class="dh-heading">核心服务</div><ul><li>公司注册（LLC/Branch）</li><li>MISA投资许可证申请</li><li>SABER/SASO产品认证</li><li>本地代理/经销商协议</li><li>工作签证与居住许可</li><li>政府招标参与支持</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询沙特</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-eg': {'title': '埃及', 'subtitle': 'egypt', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1539650116455-251d9a063595?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">EGY</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">埃及是阿拉伯世界人口最多的国家，苏伊士运河经济带与一带一路交汇，战略位置极其重要。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与投资许可证</li><li>苏伊士运河经济特区入驻</li><li>税务登记与优惠政策申请</li><li>海关清关与贸易合规</li><li>本地劳工与社保办理</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询埃及</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-ng': {'title': '尼日利亚', 'subtitle': 'nigeria', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1565099824688-e93eb20fe622?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">NGA</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">尼日利亚是非洲最大经济体和人口最多的国家，拉各斯是西非商业中心。</div><div class="dh-heading">核心服务</div><ul><li>CAC公司注册</li><li>NAFDAC产品认证（食品、药品、化妆品）</li><li>NCC通信设备认证</li><li>进口商许可证办理</li><li>工作签证与居留许可</li><li>本地法务与税务合规</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询尼日利亚</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-ke': {'title': '肯尼亚', 'subtitle': 'kenya', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">KEN</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">肯尼亚是东非经济龙头，作为东非共同体门户，辐射整个东非市场。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与执照</li><li>KEBS产品认证</li><li>税务登记与合规</li><li>海关清关与物流</li><li>本地招聘与人事管理</li><li>政府关系对接</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询肯尼亚</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-de': {'title': '德国', 'subtitle': 'germany', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">DEU</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">德国是欧洲最大经济体，制造业全球领先。柏林与汉堡双中心提供德国与欧盟市场准入全套服务。</div><div class="dh-heading">核心服务</div><ul><li>GmbH公司注册</li><li>VAT税务登记与申报</li><li>CE认证办理</li><li>商标注册</li><li>投资并购咨询</li><li>法律与税务合规</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询德国</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-nl': {'title': '荷兰', 'subtitle': 'netherlands', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1534351590666-13e3e96b5017?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">NLD</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">荷兰是欧洲门户，鹿特丹港是中国企业进入欧洲的重要桥头堡。</div><div class="dh-heading">核心服务</div><ul><li>BV公司注册</li><li>VAT税务登记</li><li>海关备案与物流</li><li>欧盟CE认证</li><li>知识产权与品牌保护</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询荷兰</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'country-pl': {'title': '波兰', 'subtitle': 'poland', 'content': '<div class="dh-hero"><img src="https://images.unsplash.com/photo-1519197924294-4ba991a11128?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">POL</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">波兰是中东欧最大经济体，也是中欧班列进入欧洲的第一站。</div><div class="dh-heading">核心服务</div><ul><li>公司注册（Sp. z o.o.）</li><li>VAT税务登记</li><li>工作许可与居留卡</li><li>投资特区优惠申请</li><li>本地招聘与人事外包</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询波兰</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
}

# Find and replace old DETAIL_CONTENT
old_dc_start = html.find("const DETAIL_CONTENT={")
if old_dc_start > 0:
    # Find the end of DETAIL_CONTENT block
    dc_end = html.find("};", old_dc_start + 20)
    if dc_end > 0:
        dc_end += 1  # include the closing brace

        # Build the new DETAIL_CONTENT JS
        dc_lines = ['const DETAIL_CONTENT={']
        for key, val in DETAIL_CONTENT.items():
            content_escaped = val['content'].replace("'", "\\'")
            dc_lines.append(f"  '{key}':{{title:'{val['title']}',subtitle:'{val['subtitle']}',content:'{content_escaped}'}},")
        dc_lines.append('};')

        html = html[:old_dc_start] + '\n'.join(dc_lines) + html[dc_end+1:]
        print("DETAIL_CONTENT replaced successfully")
    else:
        print(f"WARN: Could not find end of DETAIL_CONTENT, found at {old_dc_start}")
else:
    print("WARN: DETAIL_CONTENT not found")

# ============================================================
# 3. FIX nav-cta onclick — replace escaped backslash-parens
# ============================================================
html = html.replace("event.preventDefault\\(\\);openBook\\(\\);", "event.preventDefault();openBook();")
html = html.replace("event.preventDefault\\(\\);openWechat\\(\\);", "event.preventDefault();openWechat();")
print("Nav CTA fix applied")

# ============================================================
# 4. Replace slide click handler with mousedown/mouseup
# ============================================================
old_handler = '''function handleSlideClick(index,event){
  const slide=event.currentTarget;
  const startX=event.clientX||event.touches?.[0]?.clientX;
  
  function onMove(e){const x=e.clientX||e.touches?.[0]?.clientX;if(Math.abs(x-startX)>10)slide._dragged=true;}
  function onUp(e){
    document.removeEventListener('mousemove',onMove);
    document.removeEventListener('mouseup',onUp);
    if(!slide._dragged){openDetail(SLIDE_CONFIG[index].detailId);}
    delete slide._dragged;
  }
  
  document.addEventListener('mousemove',onMove);
  document.addEventListener('mouseup',onUp);
}'''

new_handler = '''// SLIDE INTERACTION - one click to open detail
let _slide_clicked=false;
document.addEventListener('mousedown',function(e){
  const slide=e.target.closest('.hero-slide');
  if(!slide)return;
  _slide_clicked={el:slide,x:e.clientX,y:e.clientY,index:parseInt(slide.dataset.index),dragged:false};
});
document.addEventListener('mousemove',function(e){
  if(!_slide_clicked)return;
  if(Math.abs(e.clientX-_slide_clicked.x)>10||Math.abs(e.clientY-_slide_clicked.y)>10){_slide_clicked.dragged=true;}
});
document.addEventListener('mouseup',function(e){
  if(_slide_clicked&&!_slide_clicked.dragged){
    openDetail(SLIDE_CONFIG[_slide_clicked.index].detailId);
  }
  _slide_clicked=null;
});'''

if old_handler in html:
    html = html.replace(old_handler, new_handler)
    print("Slide click handler replaced (mousedown/mouseup)")
else:
    # Try different whitespace patterns
    html = html.replace('function handleSlideClick', 'function _handleSlideClick_removed')
    # Add new handler right before the DETAIL OVERLAY section
    html = html.replace("// DETAIL OVERLAY", new_handler + "\n\n// DETAIL OVERLAY")
    print("Slide click handler added (mousedown/mouseup)")

# Remove onclick from hero-slide div
html = html.replace('onclick="handleSlideClick(${i},event)"', '')
print("Removed onclick from hero-slide")

# ============================================================
# 5. Add booking/wechat modal HTML before </body>
# ============================================================
modal_html = '''
<!-- BOOKING MODAL -->
<div class="modal-overlay" id="bookModal" onclick="closeModalOnBackground(event)">
  <div class="modal-box">
    <button class="detail-close" onclick="closeBook()">&times;</button>
    <h3>预约咨询</h3>
    <p>留下您的联系方式，我们将尽快与您联系，为您定制出海方案。</p>
    <input class="modal-input" type="text" placeholder="您的姓名" id="bookName">
    <input class="modal-input" type="tel" placeholder="手机号码" id="bookPhone">
    <input class="modal-input" type="text" placeholder="出海意向国家" id="bookCountry">
    <button class="modal-submit" onclick="submitBook()">提交预约</button>
    <div class="modal-close-text"><a onclick="closeBook()">稍后再说</a></div>
  </div>
</div>

<!-- WECHAT MODAL -->
<div class="modal-overlay" id="wechatModal" onclick="closeModalOnBackground(event)">
  <div class="modal-box">
    <button class="detail-close" onclick="closeWechat()">&times;</button>
    <h3>微信咨询</h3>
    <p>请添加微信客服，我们将在24小时内为您服务。</p>
    <div style="background:var(--red-soft);border-radius:var(--radius);padding:1.2rem;text-align:center;margin-bottom:.8rem;">
      <div style="font-family:'Noto Serif SC',serif;font-size:1.1rem;font-weight:700;color:var(--red);margin-bottom:.3rem;">SilkRoadTrade</div>
      <div style="font-size:.72rem;color:var(--gray);">微信客服号</div>
    </div>
    <div class="modal-close-text"><a onclick="closeWechat()">已完成添加</a></div>
  </div>
</div>
'''

# Insert modal HTML before </body>
html = html.replace('</body>', modal_html + '\n</body>')
print("Booking/Wechat modal HTML added")

# ============================================================
# 6. Replace openBook/openWechat functions
# ============================================================
# Find the existing openBook and openWechat functions
html = html.replace(
    "function openWechat(){alert('请添加微信客服：SilkRoadTrade');}",
    '''function openWechat(){
  document.getElementById('wechatModal').classList.add('active');
}
function closeWechat(){
  document.getElementById('wechatModal').classList.remove('active');
}'''
)
print("openWechat updated")

html = html.replace(
    "function openBook(){alert('预约演示功能即将上线，请添加微信咨询。');}",
    '''function openBook(){
  document.getElementById('bookModal').classList.add('active');
}
function closeBook(){
  document.getElementById('bookModal').classList.remove('active');
}
function closeModalOnBackground(e){
  if(e.target===e.currentTarget){e.target.classList.remove('active');}
}
function submitBook(){
  const name=document.getElementById('bookName').value.trim();
  const phone=document.getElementById('bookPhone').value.trim();
  const country=document.getElementById('bookCountry').value.trim();
  if(!name||!phone){alert('请填写姓名和手机号码');return;}
  alert('预约已提交！我们将尽快与您联系。');
  closeBook();
}'''
)
print("openBook updated")

# ============================================================
# 7. Update title to v5
# ============================================================
html = html.replace(
    '<title>丝路山海通 — 一带一路企业出海一站式服务</title>',
    '<title>丝路山海通 v5 — 一带一路企业出海一站式服务</title>'
)
print("Title updated")

# ============================================================
# WRITE OUTPUT
# ============================================================
with open('silkroad-trade_v5_silk_poster.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n================ DONE ================")
print(f"Output file size: {len(html.encode('utf-8'))} bytes")
print("v5 rebuilt successfully with all enhancements!")
