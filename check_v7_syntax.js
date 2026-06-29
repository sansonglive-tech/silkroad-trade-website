
// ================================================================
// >>>  🌟 配 置 区 — 在这里修改所有内容和图片  🌟 <<<
// ================================================================
// 修改以下内容即可更新网页，无需改动其他代码
// 注意：逗号分隔，最后一项后面不要加逗号
// ================================================================

const CONFIG = {

  // ─── 公司基本信息 ───
  company: {
    name: '丝路山海通',                    // ← 公司名
    slogan: '一带一路企业出海一站式服务',    // ← 副标题
    email: 'contact@silkroad-trade.com',   // ← 邮箱
    icp: '粤ICP备XXXXXXXX号',              // ← ICP备案号
    wechatId: 'SilkRoadTrade',             // ← 微信号
    // 微信二维码图片路径（相对路径或URL）
    wechatQR: 'wechat/二维码.jpg',          // ← 改这里换二维码
  },

  // ─── 统计数字 ───
  stats: [
    { num: '60+', label: '一带一路覆盖国家' },
    { num: '1,600+', label: '服务出海企业' },
    { num: '400+', label: '海外本地员工' },
    { num: '5+', label: '区域服务网络' },
  ],

  // ─── 轮播图（7张）───
  // 修改 title/desc/img 即可更换内容和图片
  slides: [
    {
      id: 'slide-1',
      title: '乘丝路长风<span class="gold">通达全球</span>',
      subtitle: '一带一路企业出海一站式服务',
      desc: '丝路山海通 — 响应国家一带一路倡议，为企业出海提供公司注册、财税支持、产品准入、本地化运营等一站式落地服务。',
      img: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&q=80&auto=format',
      detailId: 'company-advantage'
    },
    {
      id: 'slide-2',
      title: '公司注册<span class="gold">资质办理</span>',
      subtitle: '最快7个工作日完成海外公司设立',
      desc: '境内境外公司注册、营业执照激活、行业资质证照办理，让您的企业快速合法落地海外。',
      img: 'https://images.unsplash.com/photo-1560179707-f14e90ef3623?w=800&q=80&auto=format',
      detailId: 'company-reg'
    },
    {
      id: 'slide-3',
      title: '财税人事<span class="gold">法务合规</span>',
      subtitle: '本地化运营全方位保障',
      desc: '财税筹划、代理记账、人事雇佣、法务咨询、合规审计，专业团队为您保驾护航。',
      img: 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&q=80&auto=format',
      detailId: 'tax-legal'
    },
    {
      id: 'slide-4',
      title: '产品准入<span class="gold">认证通关</span>',
      subtitle: 'SNI/BPOM/清真认证一站式办理',
      desc: 'SNI认证、BPOM注册、清真认证、进出口许可证、海关备案等全套产品合规准入服务。',
      img: 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800&q=80&auto=format',
      detailId: 'certification'
    },
    {
      id: 'slide-5',
      title: '本地运营<span class="gold">长期陪伴</span>',
      subtitle: '真正扎根海外市场',
      desc: '行政办公、本地招聘、政府关系、行业资源对接、展会活动策划，让您出海无忧。',
      img: 'https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=800&q=80&auto=format',
      detailId: 'local-ops'
    },
    {
      id: 'slide-6',
      title: '签证考察<span class="gold">商务出行</span>',
      subtitle: '签证办理与商务考察一站式',
      desc: '商务签证、工作签证、工厂考察、市场调研、政府对接，一站式行程安排，助您轻松出海考察。',
      img: 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&q=80&auto=format',
      detailId: 'visa'
    },
    {
      id: 'slide-7',
      title: '建厂工程<span class="gold">落地投产</span>',
      subtitle: '海外建厂与基建全流程服务',
      desc: '海外选址建厂、建筑工程许可、环境合规、能源矿产、IT通讯等基建配套，让您的工厂快速落地。',
      img: 'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=800&q=80&auto=format',
      detailId: 'factory'
    },
  ],

  // ─── 服务卡片（6个）───
  services: [
    { id: 'company-reg', icon: '&#127963;', title: '公司注册与资质', subtitle: 'incorporation & licensing', color: '#C44536', desc: '境内境外公司注册、营业执照激活、行业资质证照办理，最快7个工作日完成海外公司设立。' },
    { id: 'tax-legal', icon: '&#128203;', title: '财税人事与法务', subtitle: 'tax, hr & legal', color: '#C8923E', desc: '财税筹划、代理记账、人事雇佣、法务咨询、合规审计，本地化运营全方位保障。' },
    { id: 'visa', icon: '&#128706;', title: '签证与商务考察', subtitle: 'visa & business trip', color: '#5A7D6B', desc: '商务签证、工作签证、工厂考察、市场调研、政府对接，一站式行程安排。' },
    { id: 'certification', icon: '&#128230;', title: '产品准入与认证', subtitle: 'product certification', color: '#6B4A3E', desc: 'SNI认证、BPOM注册、清真认证、进出口许可证、海关备案等全套产品合规准入服务。' },
    { id: 'factory', icon: '&#127959;', title: '建厂与工程服务', subtitle: 'factory & construction', color: '#3A5A78', desc: '海外选址建厂、建筑工程许可、环境合规、能源矿产、IT通讯等基建配套服务。' },
    { id: 'local-ops', icon: '&#129309;', title: '本地化运营支持', subtitle: 'local operation', color: '#C44536', desc: '行政办公、本地招聘、政府关系、行业资源对接、展会活动策划，真正扎根海外市场。' },
  ],

  // ─── 政策卡片（4个）───
  policies: [
    { id: 'policy-research', num: '01', title: '政策研究与解读', desc: '专业团队追踪分析沿线国家最新外资政策、税收优惠、产业扶持措施，为企业出海提供精准政策导航。' },
    { id: 'policy-network', num: '02', title: '政府与商会对接', desc: '深度链接当地政府、中国驻外使领馆、华人商会，为企业建立高层级政商关系网络。' },
    { id: 'policy-park', num: '03', title: '产业园区落地', desc: '对接沿线产业园区、经济特区，协助企业享受税收减免、土地优惠等政策红利。' },
    { id: 'policy-finance', num: '04', title: '投融资对接', desc: '对接丝路基金、亚投行、国开行等金融机构，协助企业获取出海项目资金支持。' },
  ],

  // ─── 国家/地区 ───
  // 修改 img 即可更换国家图片
  countries: {
    // 东南亚
    'country-id': { name: '印度尼西亚', code: 'IDN', cities: '雅加达 · 泗水 · 棉兰', img: 'https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800&q=80&auto=format', intro: '印尼是东南亚最大经济体，中国企业出海首选目的地之一。三大服务中心覆盖全境。' },
    'country-vn': { name: '越南', code: 'VNM', cities: '胡志明 · 河内', img: 'https://images.unsplash.com/photo-1528127269322-539801943592?w=800&q=80&auto=format', intro: '越南凭借优越地理位置和劳动力成本优势，已吸引大量制造业转移。胡志明与河内双中心覆盖南北经济走廊。' },
    'country-ph': { name: '菲律宾', code: 'PHL', cities: '马尼拉', img: 'https://images.unsplash.com/photo-1518509562904-e7ef99cdcc86?w=800&q=80&auto=format', intro: '菲律宾英语普及率高、劳动力充足，是全球BPO中心和新兴制造业基地。' },
    'country-th': { name: '泰国', code: 'THA', cities: '曼谷', img: 'https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=800&q=80&auto=format', intro: '泰国是东盟第二大经济体，汽车制造和食品加工产业领先。曼谷服务中心提供全方位出海落地服务。' },
    'country-sg': { name: '新加坡', code: 'SGP', cities: '东南亚总部', img: 'https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=800&q=80&auto=format', intro: '新加坡是全球金融中心和东南亚区域总部首选地，提供高端商务与跨境服务。' },
    // 中亚/俄语区
    'country-kz': { name: '哈萨克斯坦', code: 'KAZ', cities: '阿拉木图 · 阿斯塔纳', img: 'https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800&q=80&auto=format', intro: '哈萨克斯坦是中亚最大经济体，一带一路首倡之地。阿拉木图与阿斯塔纳双中心。' },
    'country-uz': { name: '乌兹别克斯坦', code: 'UZB', cities: '塔什干', img: 'https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800&q=80&auto=format', intro: '乌兹别克斯坦近年改革开放力度大，经济特区政策优惠，市场潜力可观。' },
    'country-kg': { name: '吉尔吉斯斯坦', code: 'KGZ', cities: '比什凯克', img: 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&q=80&auto=format', intro: '吉尔吉斯斯坦是欧亚经济联盟成员国，可作为进入俄白哈市场的桥头堡。' },
    'country-tj': { name: '塔吉克斯坦', code: 'TJK', cities: '杜尚别', img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=80&auto=format', intro: '塔吉克斯坦是中亚新兴市场，水电资源和矿产资源丰富。' },
    'country-ru': { name: '俄罗斯', code: 'RUS', cities: '莫斯科 · 圣彼得堡', img: 'https://images.unsplash.com/photo-1513326738677-b964603b136d?w=800&q=80&auto=format', intro: '俄罗斯是横跨欧亚的超级市场，莫斯科与圣彼得堡双中心提供全面的市场准入和本地运营服务。' },
    // 中东/非洲
    'country-ae': { name: '阿联酋', code: 'ARE', cities: '迪拜 · 阿布扎比', img: 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&q=80&auto=format', intro: '阿联酋是中东商贸枢纽和金融中心，自由区政策为中国企业提供了快速落地和中东市场辐射的绝佳平台。' },
    'country-sa': { name: '沙特阿拉伯', code: 'SAU', cities: '利雅得 · 吉达', img: 'https://images.unsplash.com/photo-1586724237569-f3d0c1dee8c6?w=800&q=80&auto=format', intro: '沙特2030愿景推动经济全面开放和多元化转型，带来大量投资机遇。' },
    'country-eg': { name: '埃及', code: 'EGY', cities: '开罗', img: 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800&q=80&auto=format', intro: '埃及是阿拉伯世界人口最多的国家，苏伊士运河经济带与一带一路交汇，战略位置极其重要。' },
    'country-ng': { name: '尼日利亚', code: 'NGA', cities: '拉各斯', img: 'https://images.unsplash.com/photo-1565099824688-e93eb20fe622?w=800&q=80&auto=format', intro: '尼日利亚是非洲最大经济体和人口最多的国家，拉各斯是西非商业中心。' },
    'country-ke': { name: '肯尼亚', code: 'KEN', cities: '内罗毕', img: 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800&q=80&auto=format', intro: '肯尼亚是东非经济龙头，作为东非共同体门户，辐射整个东非市场。' },
    // 欧洲
    'country-de': { name: '德国', code: 'DEU', cities: '柏林 · 汉堡', img: 'https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=800&q=80&auto=format', intro: '德国是欧洲最大经济体，制造业全球领先。柏林与汉堡双中心提供德国与欧盟市场准入全套服务。' },
    'country-nl': { name: '荷兰', code: 'NLD', cities: '阿姆斯特丹 · 鹿特丹', img: 'https://images.unsplash.com/photo-1534351590666-13e3e96b5017?w=800&q=80&auto=format', intro: '荷兰是欧洲门户，鹿特丹港是中国企业进入欧洲的重要桥头堡。' },
    'country-pl': { name: '波兰', code: 'POL', cities: '华沙', img: 'https://images.unsplash.com/photo-1519197924294-4ba991a11128?w=800&q=80&auto=format', intro: '波兰是中东欧最大经济体，也是中欧班列进入欧洲的第一站。' },
  },

  // ─── 客户案例（3个）───
  cases: [
    {
      id: 'case-zhang',
      name: '张宏伟',
      role: '新能源汽车 · 印尼工厂负责人',
      avatar: '张',
      quote: '帮我们在雅加达完成了公司注册和工厂选址，从考察到落地只用了2个月。当地团队专业靠谱，比我们自己跑效率高太多了。',
      img: 'https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800&q=80&auto=format',
      background: ['新能源汽车行业', '计划在印尼设立工厂', '对当地法规和市场不熟悉'],
      results: ['2个月完成公司注册和工厂选址', '雅加达、泗水、棉兰三地考察', '顺利完成SNI认证和工厂许可', '本地招聘团队50+人'],
      comments: ['"当地团队专业靠谱"', '"比我们自己跑效率高太多"', '"强烈推荐丝路山海通"'],
    },
    {
      id: 'case-li',
      name: '李雪峰',
      role: '工程机械 · 中亚事业部总经理',
      avatar: '李',
      quote: '响应一带一路开拓中亚市场，丝路山海通从法律合规到政府关系一路护航，节省了大量试错成本，强烈推荐。',
      img: 'https://images.unsplash.com/photo-1542259681-d4cd4e5b3c5f?w=800&q=80&auto=format',
      background: ['工程机械行业', '开拓哈萨克斯坦、乌兹别克斯坦市场', '需要EAC认证和本地代理'],
      results: ['完成哈萨克斯坦公司注册', 'EAC认证顺利通过', '对接当地政府和商会资源', '建立本地经销商网络'],
      comments: ['"从法律合规到政府关系一路护航"', '"节省了大量试错成本"', '"强烈推荐"'],
    },
    {
      id: 'case-wang',
      name: '王琳',
      role: '食品饮料 · 海外拓展总监',
      avatar: '王',
      quote: '印尼的SNI认证和清真认证一度让我们头疼，丝路山海通一站式包办，产品准入周期缩短了60%，效果超出预期。',
      img: 'https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800&q=80&auto=format',
      background: ['食品饮料行业', '计划进入印尼市场', '需要SNI认证和清真认证'],
      results: ['SNI认证3个月完成（常规需6-8个月）', '清真认证一站式办理', 'BPOM注册顺利通过', '产品准入周期缩短60%'],
      comments: ['"一站式包办，省心省力"', '"产品准入周期缩短了60%"', '"效果超出预期"'],
    },
  ],

}; // ← CONFIG 结束
// ================================================================
// >>>  配 置 区 结 束  —  下面代码不用动  <<<
// ================================================================

// Helper: Build SLIDE_CONFIG from CONFIG
const SLIDE_CONFIG = CONFIG.slides;

// DETAIL CONTENT
// SLIDE_CONFIG loaded from CONFIG.slides


// DETAIL CONTENT
const DETAIL_CONTENT={
  'company-advantage':{title:'公司优势',subtitle:'为什么选择丝路山海通',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">ADV</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">丝路山海通专注一带一路沿线国家，深耕东南亚、中亚、中东、非洲等新兴市场，为企业出海提供一站式落地服务。</div><div class="dh-heading">深耕一带一路</div><ul><li>覆盖60+一带一路沿线国家</li><li>400+海外本地员工</li><li>丰富的本地化经验和政商资源</li></ul><div class="dh-heading">专业本地团队</div><ul><li>熟悉当地法律、税务、文化</li><li>真正接地气的落地服务</li><li>7×24小时响应支持</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">立即咨询</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'company-reg':{title:'公司注册与资质',subtitle:'incorporation & licensing',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1560179707-f14e90ef3623?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">REG</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">协助企业在目标国家完成公司注册、营业执照激活、行业资质办理，最快7个工作日完成海外公司设立。</div><div class="dh-heading">境内公司注册</div><ul><li>名称核准、章程制定、股东登记</li><li>全套流程一站式服务</li></ul><div class="detail-grid"><div class="detail-item"><strong>7个工作日</strong><span>最快完成公司设立</span></div><div class="detail-item"><strong>60+国家</strong><span>覆盖一带一路沿线</span></div></div><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">预约办理</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'tax-legal':{title:'财税人事与法务',subtitle:'tax, hr & legal',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">TAX</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">根据当地税法为企业制定最优财税方案，提供代理记账、人事雇佣、法务咨询等全方位服务。</div><div class="dh-heading">财税筹划</div><ul><li>制定最优财税方案</li><li>合理避税，降低成本</li></ul><div class="dh-heading">代理记账</div><ul><li>记账、报税、年审</li><li>全套财务服务</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">预约咨询</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'certification':{title:'产品准入与认证',subtitle:'product certification',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">CERT</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">SNI认证、BPOM注册、清真认证、进出口许可证等全套产品合规准入服务。</div><div class="dh-heading">SNI认证（印尼）</div><ul><li>印尼国家标准认证</li><li>产品进入印尼市场必备</li></ul><div class="dh-heading">清真认证</div><ul><li>穆斯林市场必备资质</li><li>开拓东南亚、中东市场</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">办理认证</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'local-ops':{title:'本地化运营支持',subtitle:'local operation',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">OPS</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">行政办公、本地招聘、政府关系、行业资源对接，让企业真正扎根海外市场。</div><div class="dh-heading">行政办公</div><ul><li>办公室租赁</li><li>办公手续办理</li></ul><div class="dh-heading">本地招聘</div><ul><li>本地渠道招聘</li><li>薪酬体系制定</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">获取方案</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'visa':{title:'签证与商务考察',subtitle:'visa & business trip',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">VISA</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">商务签证、工作签证、工厂考察、市场调研，一站式行程安排。</div><div class="dh-heading">商务签证</div><ul><li>最快5个工作日出签</li><li>多次往返类型</li></ul><div class="detail-grid"><div class="detail-item"><strong>5个工作日</strong><span>最快出签</span></div><div class="detail-item"><strong>20+国家</strong><span>签证覆盖</span></div></div><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">预约考察</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'factory':{title:'建厂与工程服务',subtitle:'factory & construction',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">FACT</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">海外选址建厂、建筑工程许可、环境合规、能源矿产，全流程服务。</div><div class="dh-heading">海外选址建厂</div><ul><li>工业园区考察</li><li>土地谈判、环保评估</li></ul><div class="dh-heading">建筑工程许可</div><ul><li>建筑施工许可</li><li>消防审批</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">建厂咨询</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
    'policy-research':{title:'政策研究与解读',subtitle:'policy research',content:'<div class="dh-hero"><div class="dh-hero-code">POL-01</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">专业团队追踪分析沿线国家最新外资政策、税收优惠、产业扶持措施，为企业出海提供精准政策导航。</div><div class="dh-heading">服务内容</div><ul><li>外资准入政策动态追踪</li><li>税收优惠政策解读与应用</li><li>产业扶持措施匹配分析</li><li>政策风险评估与预警</li></ul><div class="dh-heading">服务优势</div><ul><li>覆盖60+一带一路沿线国家</li><li>实时政策数据库更新</li><li>资深政策分析师团队</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询政策研究</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'policy-network':{title:'政府与商会对接',subtitle:'government & chamber',content:'<div class="dh-hero"><div class="dh-hero-code">POL-02</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">深度链接当地政府、中国驻外使领馆、华人商会，为企业建立高层级政商关系网络。</div><div class="dh-heading">对接资源</div><ul><li>目标国政府投资促进机构</li><li>中国驻外使领馆商务处</li><li>当地华人商会与行业协会</li><li>产业园区管委会</li></ul><div class="dh-heading">服务价值</div><ul><li>快速建立本地政商人脉</li><li>获取一手政策信息</li><li>提升企业在当地影响力</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询对接服务</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'policy-park':{title:'产业园区落地',subtitle:'industrial park',content:'<div class="dh-hero"><div class="dh-hero-code">POL-03</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">对接沿线产业园区、经济特区，协助企业享受税收减免、土地优惠等政策红利。</div><div class="dh-heading">园区类型</div><ul><li>出口加工区（EPZ）</li><li>自由贸易区（FTZ）</li><li>经济特区（SEZ）</li><li>高新技术产业园区</li></ul><div class="dh-heading">优惠政策</div><ul><li>企业所得税减免（5-15年免税期）</li><li>进口设备关税豁免</li><li>土地租金优惠</li><li>简化行政审批流程</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询园区入驻</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'policy-finance':{title:'投融资对接',subtitle:'investment & financing',content:'<div class="dh-hero"><div class="dh-hero-code">POL-04</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">对接丝路基金、亚投行、国开行等金融机构，协助企业获取出海项目资金支持。</div><div class="dh-heading">对接机构</div><ul><li>丝路基金</li><li>亚洲基础设施投资银行（AIIB）</li><li>国家开发银行</li><li>进出口银行</li><li>当地商业银行</li></ul><div class="dh-heading">融资类型</div><ul><li>项目贷款</li><li>股权投资</li><li>出口信贷</li><li>贸易融资</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询融资对接</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},'policy-overview':{title:'政策与落地支持',subtitle:'policy & support',content:'<div class="dh-hero"><div class="dh-hero-code">BRI</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">专业团队追踪分析沿线国家最新外资政策、税收优惠、产业扶持措施，为企业出海提供精准政策导航。</div><div class="dh-heading">政策研究与解读</div><ul><li>追踪分析沿线国家外资政策</li><li>税收优惠、产业扶持措施</li><li>精准政策导航</li></ul><div class="dh-heading">政府与商会对接</div><ul><li>深度链接当地政府、使领馆</li><li>华人商会资源对接</li><li>建立高层级政商关系</li></ul><div class="dh-heading">产业园区落地</div><ul><li>对接产业园区、经济特区</li><li>税收减免、土地优惠</li><li>政策红利最大化</li></ul><div class="dh-heading">投融资对接</div><ul><li>对接丝路基金、亚投行</li><li>国开行等金融机构</li><li>出海项目资金支持</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询政策</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'process-step1':{title:'01 需求诊断',subtitle:'needs assessment',content:'<div class="dh-hero"><div class="dh-hero-code">STEP 01</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">深入了解企业出海目标与需求，定制化出海方案。这是出海成功的第一步，也是最关键的一步。</div><div class="dh-heading">诊断内容</div><ul><li>企业出海目标与战略规划</li><li>产品特点与市场定位分析</li><li>预算规模与资源评估</li><li>目标市场机会与风险分析</li></ul><div class="dh-heading">交付成果</div><ul><li>定制化出海方案</li><li>目标市场可行性报告</li><li>初步投资预算与时间表</li><li>风险评估与应对建议</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">开始诊断</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'process-step2':{title:'02 尽职调研',subtitle:'due diligence',content:'<div class="dh-hero"><div class="dh-hero-code">STEP 02</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">市场调研、法律评估、财税分析，规避风险前置。用数据和事实为出海决策提供支撑。</div><div class="dh-heading">调研内容</div><ul><li>目标市场规模与竞争格局</li><li>当地法律法规与政策环境</li><li>财税制度与合规要求</li><li>行业准入门槛与资质要求</li></ul><div class="dh-heading">交付成果</div><ul><li>详细市场调研报告</li><li>法律合规评估报告</li><li>财税筹划方案</li><li>风险清单与规避建议</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">预约调研</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'process-step3':{title:'03 落地执行',subtitle:'execution',content:'<div class="dh-hero"><div class="dh-hero-code">STEP 03</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">公司注册、资质办理、团队搭建，全程陪伴推进。将方案转化为实际行动，让企业在海外落地生根。</div><div class="dh-heading">执行内容</div><ul><li>公司注册与营业执照激活</li><li>行业资质与许可证办理</li><li>本地团队招聘与培训</li><li>办公场地与基础设施</li></ul><div class="dh-heading">交付成果</div><ul><li>合法运营的海外公司</li><li>完整的资质证照</li><li>本地运营团队</li><li>办公场地与设备</li></ul><div class="detail-grid"><div class="detail-item"><strong>7个工作日</strong><span>最快完成公司设立</span></div><div class="detail-item"><strong>全程陪伴</strong><span>专人跟进每一步</span></div></div><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">立即执行</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'process-step4':{title:'04 持续运营',subtitle:'ongoing support',content:'<div class="dh-hero"><div class="dh-hero-code">STEP 04</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">财税代账、法务支持、政府维护，长期运营保障。出海不是一锤子买卖，我们陪伴企业长期发展。</div><div class="dh-heading">运营支持</div><ul><li>财税代账与税务申报</li><li>法务咨询与合同审核</li><li>政府关系维护与更新</li><li>本地资源对接与拓展</li></ul><div class="dh-heading">增值服务</div><ul><li>年度合规审计</li><li>业务扩展支持</li><li>危机应对与处理</li><li>战略咨询与优化</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">获取支持</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'case-zhang':{title:'客户案例：张宏伟',subtitle:'新能源汽车 · 印尼工厂负责人',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">CASE</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">"帮我们在雅加达完成了公司注册和工厂选址，从考察到落地只用了2个月。当地团队专业靠谱，比我们自己跑效率高太多了。"</div><div class="dh-heading">客户背景</div><ul><li>新能源汽车行业</li><li>计划在印尼设立工厂</li><li>对当地法规和市场不熟悉</li></ul><div class="dh-heading">服务成果</div><ul><li>2个月完成公司注册和工厂选址</li><li>雅加达、泗水、棉兰三地考察</li><li>顺利完成SNI认证和工厂许可</li><li>本地招聘团队50+人</li></ul><div class="dh-heading">客户评价</div><ul><li>"当地团队专业靠谱"</li><li>"比我们自己跑效率高太多"</li><li>"强烈推荐丝路山海通"</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询印尼出海</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'case-li':{title:'客户案例：李雪峰',subtitle:'工程机械 · 中亚事业部总经理',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">CASE</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">"响应一带一路开拓中亚市场，丝路山海通从法律合规到政府关系一路护航，节省了大量试错成本，强烈推荐。"</div><div class="dh-heading">客户背景</div><ul><li>工程机械行业</li><li>开拓哈萨克斯坦、乌兹别克斯坦市场</li><li>需要EAC认证和本地代理</li></ul><div class="dh-heading">服务成果</div><ul><li>完成哈萨克斯坦公司注册</li><li>EAC认证顺利通过</li><li>对接当地政府和商会资源</li><li>建立本地经销商网络</li></ul><div class="dh-heading">客户评价</div><ul><li>"从法律合规到政府关系一路护航"</li><li>"节省了大量试错成本"</li><li>"强烈推荐"</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询中亚出海</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'case-wang':{title:'客户案例：王琳',subtitle:'食品饮料 · 海外拓展总监',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">CASE</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">"印尼的SNI认证和清真认证一度让我们头疼，丝路山海通一站式包办，产品准入周期缩短了60%，效果超出预期。"</div><div class="dh-heading">客户背景</div><ul><li>食品饮料行业</li><li>计划进入印尼市场</li><li>需要SNI认证和清真认证</li></ul><div class="dh-heading">服务成果</div><ul><li>SNI认证3个月完成（常规需6-8个月）</li><li>清真认证一站式办理</li><li>BPOM注册顺利通过</li><li>产品准入周期缩短60%</li></ul><div class="dh-heading">客户评价</div><ul><li>"一站式包办，省心省力"</li><li>"产品准入周期缩短了60%"</li><li>"效果超出预期"</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询产品认证</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'about':{title:'关于丝路山海通',subtitle:'silk road trade',content:'<div class="dh-hero"><div class="dh-hero-code">ABOUT</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">让企业出海不再难，促进中国与一带一路国家经贸交往，互利共赢。</div><div class="dh-heading">我们的使命</div><ul><li>让企业出海不再难</li><li>促进一带一路经贸交往</li><li>互利共赢</li></ul><div class="dh-heading">我们的愿景</div><ul><li>成为中国企业出海首选服务伙伴</li><li>陪伴更多中国企业走向世界</li></ul><div class="dh-heading">我们的价值观</div><ul><li>专业、诚信、高效、共赢</li><li>以客户需求为中心</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">联系我们</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'region-sea':{title:'东南亚区域',subtitle:'southeast asia',content:'<div class="dh-hero"><div class="dh-hero-code">SEA</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">覆盖印尼、越南、菲律宾、泰国、新加坡五大核心市场，是中国企业出海最成熟的区域。</div><div class="dh-heading">核心服务</div><ul><li>外商独资公司注册</li><li>海关与进出口资质</li><li>本地招聘与人事外包</li><li>税务与法务支持</li><li>产业园区入驻</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询东南亚</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'region-ru':{title:'俄语区/中亚区域',subtitle:'cis & central asia',content:'<div class="dh-hero"><div class="dh-hero-code">CIS</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">覆盖哈萨克斯坦、乌兹别克斯坦、吉尔吉斯斯坦、塔吉克斯坦、俄罗斯五国。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与经营许可</li><li>矿产资源投资合作</li><li>EAC/CUTR认证办理</li><li>工作签证与劳动配额</li><li>海关清关与物流</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询俄语区/中亚</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'region-me':{title:'中东/非洲区域',subtitle:'middle east & africa',content:'<div class="dh-hero"><div class="dh-hero-code">MEA</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">覆盖阿联酋、沙特、埃及、尼日利亚、肯尼亚。</div><div class="dh-heading">阿联酋·沙特</div><ul><li>自由区公司注册</li><li>MISA投资许可、SABER/SASO认证</li></ul><div class="dh-heading">非洲三国</div><ul><li>埃及、尼日利亚、肯尼亚</li><li>产品认证、政府关系、公司注册</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询中东非洲</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'region-eu':{title:'欧洲区域',subtitle:'europe',content:'<div class="dh-hero"><div class="dh-hero-code">EU</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">覆盖德国、荷兰、波兰，深耕制造业、IT外包、物流贸易领域。</div><div class="dh-heading">德国</div><ul><li>柏林与汉堡双中心</li><li>GmbH注册、VAT税务、CE认证</li></ul><div class="dh-heading">荷兰·波兰</div><ul><li>欧洲物流枢纽</li><li>BV/Sp. z o.o.注册、投资特区优惠</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询欧洲</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-id':{title:'印度尼西亚',subtitle:'indonesia',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">IDN</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">印尼是东南亚最大经济体，中国企业出海首选目的地之一。三大服务中心覆盖全境。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与营业执照激活</li><li>SNI认证、BPOM注册、清真认证</li><li>财税代账与法务支持</li><li>建厂许可与环境合规</li><li>本地招聘与人事管理</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询印尼</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-vn':{title:'越南',subtitle:'vietnam',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1528127269322-539801943592?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">VNM</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">越南凭借优越地理位置和劳动力成本优势，已吸引大量制造业转移。胡志明与河内双中心覆盖南北经济走廊。</div><div class="dh-heading">核心服务</div><ul><li>外商独资公司注册</li><li>进出口权办理</li><li>本地招聘与社保代缴</li><li>税务合规与代理记账</li><li>工厂选址与环境评估</li><li>投资许可证申请</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询越南</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-ph':{title:'菲律宾',subtitle:'philippines',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1518509562904-e7ef99cdcc86?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">PHL</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">菲律宾英语普及率高、劳动力充足，是全球BPO中心和新兴制造业基地。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与SEC备案</li><li>BPO企业设立</li><li>税务合规与财务服务</li><li>本地招聘与人事外包</li><li>BOI投资优惠申请</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询菲律宾</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-th':{title:'泰国',subtitle:'thailand',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">THA</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">泰国是东盟第二大经济体，汽车制造和食品加工产业领先。曼谷服务中心提供全方位出海落地服务。</div><div class="dh-heading">核心服务</div><ul><li>BOI投资促进申请</li><li>外商经营许可证</li><li>公司注册与工厂许可</li><li>工作签证办理</li><li>本地招聘与薪酬管理</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询泰国</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-sg':{title:'新加坡',subtitle:'singapore',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">SGP</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">新加坡是全球金融中心和东南亚区域总部首选地，提供高端商务与跨境服务。</div><div class="dh-heading">核心服务</div><ul><li>私人有限公司注册</li><li>税务筹划与IRAS合规</li><li>银行开户与融资对接</li><li>国际贸易合规</li><li>知识产权保护</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询新加坡</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-kz':{title:'哈萨克斯坦',subtitle:'kazakhstan',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">KAZ</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">哈萨克斯坦是中亚最大经济体，一带一路首倡之地。阿拉木图与阿斯塔纳双中心。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与营业执照</li><li>矿产资源投资许可</li><li>海关清关与贸易合规</li><li>工作许可与本地招聘</li><li>合资企业设立</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询哈萨克斯坦</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-uz':{title:'乌兹别克斯坦',subtitle:'uzbekistan',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">UZB</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">乌兹别克斯坦近年改革开放力度大，经济特区政策优惠，市场潜力可观。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与经营许可</li><li>经济特区入驻与优惠申请</li><li>税务登记与优惠政策对接</li><li>进出口权办理</li><li>本地代理和分销网络搭建</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询乌兹别克斯坦</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-kg':{title:'吉尔吉斯斯坦',subtitle:'kyrgyzstan',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">KGZ</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">吉尔吉斯斯坦是欧亚经济联盟成员国，可作为进入俄白哈市场的桥头堡。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与税务登记</li><li>EAC认证办理</li><li>海关清关与物流</li><li>劳动配额与工作许可</li><li>农业合作与投资</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询吉尔吉斯斯坦</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-tj':{title:'塔吉克斯坦',subtitle:'tajikistan',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">TJK</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">塔吉克斯坦是中亚新兴市场，水电资源和矿产资源丰富。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与经营许可</li><li>矿产资源合作协议支持</li><li>基建工程竞标支持</li><li>签证与工作许可办理</li><li>本地法律与税务咨询</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询塔吉克斯坦</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-ru':{title:'俄罗斯',subtitle:'russia',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1513326738677-b964603b136d?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">RUS</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">俄罗斯是横跨欧亚的超级市场，莫斯科与圣彼得堡双中心提供全面的市场准入和本地运营服务。</div><div class="dh-heading">核心服务</div><ul><li>公司注册（OOO/代表处）</li><li>EAC/CUTR认证办理</li><li>VAT税务登记与合规申报</li><li>海关清关与物流方案</li><li>商标注册与知识产权保护</li><li>本地招聘与法务支持</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询俄罗斯</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-ae':{title:'阿联酋',subtitle:'united arab emirates',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">ARE</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">阿联酋是中东商贸枢纽和金融中心，自由区政策为中国企业提供了快速落地和中东市场辐射的绝佳平台。</div><div class="dh-heading">核心服务</div><ul><li>自由区公司注册（FZE/FZCO）</li><li>离岸公司设立</li><li>营业执照与经营许可</li><li>银行开户与金融合规</li><li>VAT税务登记与申报</li><li>本地保人/代理服务</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询阿联酋</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-sa':{title:'沙特阿拉伯',subtitle:'saudi arabia',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1586724237569-f3d0c1dee8c6?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">SAU</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">沙特2030愿景推动经济全面开放和多元化转型，带来大量投资机遇。</div><div class="dh-heading">核心服务</div><ul><li>公司注册（LLC/Branch）</li><li>MISA投资许可证申请</li><li>SABER/SASO产品认证</li><li>本地代理/经销商协议</li><li>工作签证与居住许可</li><li>政府招标参与支持</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询沙特</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-eg':{title:'埃及',subtitle:'egypt',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">EGY</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">埃及是阿拉伯世界人口最多的国家，苏伊士运河经济带与一带一路交汇，战略位置极其重要。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与投资许可证</li><li>苏伊士运河经济特区入驻</li><li>税务登记与优惠政策申请</li><li>海关清关与贸易合规</li><li>本地劳工与社保办理</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询埃及</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-ng':{title:'尼日利亚',subtitle:'nigeria',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1565099824688-e93eb20fe622?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">NGA</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">尼日利亚是非洲最大经济体和人口最多的国家，拉各斯是西非商业中心。</div><div class="dh-heading">核心服务</div><ul><li>CAC公司注册</li><li>NAFDAC产品认证（食品、药品、化妆品）</li><li>NCC通信设备认证</li><li>进口商许可证办理</li><li>工作签证与居留许可</li><li>本地法务与税务合规</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询尼日利亚</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-ke':{title:'肯尼亚',subtitle:'kenya',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">KEN</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">肯尼亚是东非经济龙头，作为东非共同体门户，辐射整个东非市场。</div><div class="dh-heading">核心服务</div><ul><li>公司注册与执照</li><li>KEBS产品认证</li><li>税务登记与合规</li><li>海关清关与物流</li><li>本地招聘与人事管理</li><li>政府关系对接</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询肯尼亚</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-de':{title:'德国',subtitle:'germany',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">DEU</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">德国是欧洲最大经济体，制造业全球领先。柏林与汉堡双中心提供德国与欧盟市场准入全套服务。</div><div class="dh-heading">核心服务</div><ul><li>GmbH公司注册</li><li>VAT税务登记与申报</li><li>CE认证办理</li><li>商标注册</li><li>投资并购咨询</li><li>法律与税务合规</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询德国</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-nl':{title:'荷兰',subtitle:'netherlands',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1534351590666-13e3e96b5017?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">NLD</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">荷兰是欧洲门户，鹿特丹港是中国企业进入欧洲的重要桥头堡。</div><div class="dh-heading">核心服务</div><ul><li>BV公司注册</li><li>VAT税务登记</li><li>海关备案与物流</li><li>欧盟CE认证</li><li>知识产权与品牌保护</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询荷兰</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
  'country-pl':{title:'波兰',subtitle:'poland',content:'<div class="dh-hero"><img src="https://images.unsplash.com/photo-1519197924294-4ba991a11128?w=800&q=80&auto=format" alt=""><div class="dh-hero-code">POL</div><div class="dh-hero-overlay"></div></div><div class="dh-intro">波兰是中东欧最大经济体，也是中欧班列进入欧洲的第一站。</div><div class="dh-heading">核心服务</div><ul><li>公司注册（Sp. z o.o.）</li><li>VAT税务登记</li><li>工作许可与居留卡</li><li>投资特区优惠申请</li><li>本地招聘与人事外包</li></ul><div class="detail-cta-bar"><a href="#" class="btn-primary" onclick="event.preventDefault();closeDetail();openBook()">咨询波兰</a><a href="#" class="btn-outline" onclick="event.preventDefault();closeDetail()">返回</a></div>'},
};

// INIT
let currentSlide=0;
let slideInterval;

function init(){
  renderSlides();
  renderDots();
  startSlideShow();
  initScrollEffects();
  initNavScroll();
  
  document.getElementById('arrowPrev').addEventListener('click',()=>{prevSlide();resetSlideShow();});
  document.getElementById('arrowNext').addEventListener('click',()=>{nextSlide();resetSlideShow();});
  
  setTimeout(()=>{document.getElementById('preloader').classList.add('hide');},500);
}

function renderSlides(){
  const track=document.getElementById('heroTrack');
  track.innerHTML=SLIDE_CONFIG.map((slide,i)=>`
    <div class="hero-slide" data-index="${i}" >
      <div class="hero-text">
        <div class="ht-label"><div class="dot"></div><span>SLIDE 0${i+1}</span></div>
        <h1>${slide.title}</h1>
        <p>${slide.desc}</p>
        <a class="hero-link" onclick="event.stopPropagation();openDetail('${slide.detailId}')">了解更多 &#8594;</a>
      </div>
      <div class="hero-image-panel">
        <img src="${slide.img}" alt="${slide.subtitle}" loading="${i===0?'eager':'lazy'}">
        <div class="hip-overlay"></div>
        <div class="hip-frame"></div>
        <div class="hip-tag"><div class="dot"></div><span>${slide.subtitle}</span></div>
      </div>
    </div>
  `).join('');
  document.getElementById('slideTotal').textContent=String(SLIDE_CONFIG.length).padStart(2,'0');
}

function renderDots(){
  const dots=document.getElementById('heroDots');
  dots.innerHTML=SLIDE_CONFIG.map((_,i)=>`<button class="hero-dot ${i===0?'active':''}" data-index="${i}" onclick="goToSlide(${i});resetSlideShow();"></button>`).join('');
}

function updateSlide(){
  const track=document.getElementById('heroTrack');
  track.style.transform=`translateX(-${currentSlide*100}%)`;
  document.querySelectorAll('.hero-dot').forEach((d,i)=>d.classList.toggle('active',i===currentSlide));
  document.getElementById('slideCurrent').textContent=String(currentSlide+1).padStart(2,'0');
}

function nextSlide(){currentSlide=(currentSlide+1)%SLIDE_CONFIG.length;updateSlide();}
function prevSlide(){currentSlide=(currentSlide-1+SLIDE_CONFIG.length)%SLIDE_CONFIG.length;updateSlide();}
function goToSlide(index){currentSlide=index;updateSlide();}

function startSlideShow(){slideInterval=setInterval(nextSlide,5000);}
function resetSlideShow(){clearInterval(slideInterval);startSlideShow();}

// SLIDE INTERACTION - one click to open detail
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
});

// DETAIL OVERLAY
function openDetail(id){
  const content=DETAIL_CONTENT[id];
  if(!content)return;
  document.getElementById('detailTitle').textContent=content.title;
  document.getElementById('detailSubtitle').textContent=content.subtitle;
  document.getElementById('detailBody').innerHTML=content.content;
  document.getElementById('detailOverlay').classList.add('active');
  document.body.style.overflow='hidden';
}

function closeDetail(){
  document.getElementById('detailOverlay').classList.remove('active');
  document.body.style.overflow='';
}

function closeDetailOnBackground(event){if(event.target===event.currentTarget)closeDetail();}

// NAV SCROLL
function initNavScroll(){
  const nav=document.getElementById('navbar');
  window.addEventListener('scroll',()=>{
    if(window.scrollY>50)nav.classList.add('scrolled');
    else nav.classList.remove('scrolled');
  },{passive:true});
}

// SCROLL REVEAL
function initScrollEffects(){
  const reveals=document.querySelectorAll('.reveal');
  const observer=new IntersectionObserver((entries)=>{
    entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('active');observer.unobserve(e.target);}});
  },{threshold:0.1});
  reveals.forEach(r=>observer.observe(r));
}

// MOBILE MENU
function toggleMobileMenu(){
  const nav=document.querySelector('.nav-links');
  nav.style.display=nav.style.display==='flex'?'none':'flex';
}

// WECHAT / BOOKING
function openWechat(){
  document.getElementById('wechatModal').classList.add('active');
}
function closeWechat(){
  document.getElementById('wechatModal').classList.remove('active');
}
function openBook(){
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
}

// INIT
document.addEventListener('DOMContentLoaded',init);
