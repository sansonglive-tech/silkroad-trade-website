const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat,
  TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak
} = require("docx");

// ── Constants ──────────────────────────────────────────────
const PW = 11906, PH = 16838, MG = 1440, CW = PW - MG * 2; // 9026
const bdr = { style: BorderStyle.SINGLE, size: 1, color: "999999" };
const bdrs = { top: bdr, bottom: bdr, left: bdr, right: bdr };
const cm = { top: 60, bottom: 60, left: 100, right: 100 };

const FONT = "Microsoft YaHei";

// ── Utilities ──────────────────────────────────────────────
function h1(t) { return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [r(t, { size: 32, bold: true, color: "1F4E79" })] }); }
function h2(t) { return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [r(t, { size: 26, bold: true, color: "2E75B6" })] }); }
function h3(t) { return new Paragraph({ spacing: { before: 200, after: 120 }, children: [r(t, { size: 23, bold: true, color: "3B86C4" })] }); }

function r(text, opts = {}) { return new TextRun({ text, font: FONT, size: 21, ...opts }); }

function p(text, opts = {}) {
  const runs = typeof text === "string" ? [r(text)] : text.map(t => typeof t === "string" ? r(t) : r(t.text || "", t));
  return new Paragraph({ spacing: { after: 100, line: 340 }, ...opts, children: runs });
}

function pb(text, boldText) {
  return p([r(boldText, { bold: true }), r(text)]);
}

function sep() { return new Paragraph({ spacing: { before: 120, after: 120 }, alignment: AlignmentType.CENTER, children: [r("────────────────────────", { size: 16, color: "CCCCCC" })] }); }
function el() { return new Paragraph({ spacing: { after: 40 }, children: [] }); }

function bl(items) {
  return items.map(item => {
    const runs = (typeof item === "string" ? [{ text: item, opts: {} }] : item).map(t =>
      typeof t === "string" ? r(t) : r(t.text || "", t.opts || {})
    );
    return new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 50, line: 320 }, children: runs });
  });
}

function sbl(items) {
  return items.map(text =>
    new Paragraph({ numbering: { reference: "bullets", level: 1 }, spacing: { after: 40, line: 300 }, children: [r(text, { size: 20 })] })
  );
}

// Table helpers
function tCell(text, opts = {}) {
  const runs = [];
  if (typeof text === "string") {
    runs.push(r(text, { size: 17, ...opts }));
  } else {
    text.forEach(t => runs.push(typeof t === "string" ? r(t, { size: 17 }) : r(t.text || "", { size: 17, ...t })));
  }
  return new Paragraph({ spacing: { after: 30 }, children: runs });
}

function hdrCell(text, w) {
  return new TableCell({
    borders: bdrs, width: { size: w, type: WidthType.DXA }, shading: { fill: "1F4E79", type: ShadingType.CLEAR },
    margins: cm, verticalAlign: "center",
    children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [r(text, { bold: true, color: "FFFFFF", size: 18 })] })],
  });
}

function dCell(text, w, opts = {}) {
  let raw;
  if (typeof text === "string") {
    raw = [r(text, { size: 17 })];
  } else if (Array.isArray(text)) {
    raw = text.map(t => typeof t === "string" ? r(t, { size: 17 }) : r(t.text || "", { size: 17, ...t }));
  } else {
    raw = [text];
  }
  return new TableCell({
    borders: bdrs, width: { size: w, type: WidthType.DXA }, margins: cm,
    children: [new Paragraph({ spacing: { after: 30 }, children: raw })],
  });
}

function mkTable(cols, headers, rows) {
  const colW = cols.map(c => Math.round(c / cols.reduce((a, b) => a + b, 0) * CW));
  return new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: colW,
    rows: [
      new TableRow({ tableHeader: true, children: headers.map((h, i) => hdrCell(h, colW[i])) }),
      ...rows.map((row, ri) => new TableRow({
        children: row.map((c, ci) => dCell(c, colW[ci], ri % 2 === 1 ? { shading: { fill: "F5F8FC" } } : {})),
      })),
    ],
  });
}

// ── Numbering ──────────────────────────────────────────────
const numbering = {
  config: [{
    reference: "bullets", levels: [
      { level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
      { level: 1, format: LevelFormat.BULLET, text: "-", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1080, hanging: 360 } } } },
    ]
  }, {
    reference: "tasks", levels: [
      { level: 0, format: LevelFormat.BULLET, text: "\u2610", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
    ]
  }],
};

// ═══════════════════════════════════════════════════════════
// CONTENT
// ═══════════════════════════════════════════════════════════
const cc = [];

// ═══ 一、执行摘要 ═══
cc.push(h1("一、执行摘要"));
cc.push(p("新丝路·企业主会是一个以创始人20年外贸实战经验 + 几十万粉丝IP存量为核心资产，借鉴\"山海图\"深度本地化服务模式，为国内中小制造企业提供\"认知升级→技能培训→线下深交→一站式出海服务\"的全链路解决方案。"));
cc.push(p([r("核心商业模式：", { bold: true }), r("以99元引流课为信任钩子，通过线上内容矩阵（短视频/直播/白皮书）和私域分层运营，将粉丝精准转化为付费用户；再通过进阶课程、付费社群、线下会销（大课/私董会/峰会/海外考察）实现深度转化；最终以海外公司注册、财税合规、知识产权、供应链金融等平台服务完成长期价值绑定，形成\"前端让利获客、后端服务盈利\"的可持续生态。")]));
cc.push(p([r("差异化壁垒：", { bold: true })]));
cc.push(...bl([
  "IP信任前置（几十万粉丝已建立认知）",
  "20年跨国外贸实战经验（内容不可复制）",
  "山海图式本地化服务网络（轻资产合作+海外资源）",
  "99元引流课→高客单价服务的平滑阶梯",
]));
cc.push(p([r("3年成熟期营收目标：", { bold: true }), r("5,000万+，净利率20-25%。")]));

// ═══ 二、市场机遇与差异化定位 ═══
cc.push(new Paragraph({ children: [new PageBreak()] }));
cc.push(h1("二、市场机遇与差异化定位"));

cc.push(h2("2.1 行业背景"));
cc.push(...bl([
  "国内制造业内卷加剧，出海成为企业破局核心路径。",
  "跨境电商与外贸服务市场规模持续增长，2026年外贸培训类目预计达620亿元。",
  "国家政策支持（《对外贸易法》修订、跨境电商出口海外仓\"离境即退税\"等）。",
  "知识付费进入3.0时代，AI驱动内容生产，用户更看重\"结果导向\"的实战交付。",
]));

cc.push(h2("2.2 \"新丝路\"品牌内涵"));
cc.push(p("新丝路——传承千年丝绸之路的开拓精神，在新时代为中国制造搭建通往全球的桥梁。"));
cc.push(...bl([
  [r("新：", { bold: true }), r("新理念、新方法、AI新工具、全球新市场")],
  [r("丝路：", { bold: true }), r("联通、合作、信任、悠远的历史底蕴")],
]));
cc.push(p([r("品牌口号：", { bold: true }), r("新丝路——让中国制造走得更远。")]));

cc.push(h2("2.3 山海图模式借鉴"));
cc.push(mkTable([5,7], ["山海图成功要素", "新丝路本土化应用"], [
  ["深度本地化团队（8国14城）", "轻资产合作网络 + 海外驻地代表"],
  ["一站式服务（注册/财税/法务/准入）", "全链路复制，增加国内产业带前置服务"],
  ["行业峰会矩阵（年均百场）", "出海大课城市巡回 + 年度千人峰会"],
  ["创始人IP线下讲述", "已有几十万粉丝IP，信任前置"],
]));

cc.push(h2("2.4 新丝路差异化定位"));
cc.push(...bl([
  [r("客户定位：", { bold: true }), r("年营收500万-2亿元的国内制造企业主/工厂负责人")],
  [r("服务定位：", { bold: true }), r("比传统咨询更懂工厂，比普通服务平台更系统化")],
  [r("价值主张：", { bold: true }), r("用20年实战经验 + 全球本地化网络，帮助企业降低出海试错成本，缩短盈利周期")],
]));

// ═══ 三、商业模型总览 ═══
cc.push(new Paragraph({ children: [new PageBreak()] }));
cc.push(h1("三、商业模型总览（三层漏斗 + IP赋能）"));

cc.push(p([r("IP资产：", { bold: true }), r("几十万粉丝 + 20年外贸实战（信任前置，大幅缩短用户决策周期）")]));

cc.push(h3("第一层：99元引流课 + 全域内容矩阵"));
cc.push(...bl([
  "短视频/直播/白皮书（免费）→ 日均触达10万+",
  "99元系列课（AI获客/LinkedIn/7天训练营）",
  "私域分层运营（企业主群/从业者群/小白群）",
  [r("↓ 转化率8-15%（行业基准）", { italics: true, color: "666666" })],
]));
cc.push(h3("第二层：进阶课程 + 付费社群"));
cc.push(...bl([
  "进阶线上课（499-1,999元）",
  "\"新丝路研习社\"年度会员（1,980-9,800元）",
  [r("↓ 转化率10-20%", { italics: true, color: "666666" })],
]));
cc.push(h3("第三层：线下会销矩阵"));
cc.push(...bl([
  "出海大课城市巡回（3,800-5,800元/2天）",
  "新丝路私董会闭门（12,800-29,800元/期）",
  "新丝路年度出海峰会（980-2,980元/人 + 赞助）",
  "海外考察团（38,000-88,000元/人）",
  [r("↓ 转化率20-40%（私董会→平台服务）", { italics: true, color: "666666" })],
]));
cc.push(h3("第四层：出海一体化服务平台"));
cc.push(...bl([
  "海外公司注册（5,000-15,000元/单）",
  "年度财税/合规托管（6,000-30,000元/年）",
  "知识产权代理（3,000-20,000元/单）",
  "供应链金融/物流佣金（交易额2-5%）",
]));
cc.push(el());
cc.push(p([r("盈利闭环：", { bold: true, color: "1F4E79" }), r("99元让利获客 → 后端服务赚取长期价值（LTV 2,400元+）")]));

// ═══ 四、第一层 ═══
cc.push(new Paragraph({ children: [new PageBreak()] }));
cc.push(h1("四、第一层：99元引流课为核心的线上获客体系"));

cc.push(h2("4.1 产品设计"));
cc.push(p([r("设计原则：", { bold: true })]));
cc.push(...bl([
  [r("超值感：", { bold: true }), r("交付价值感远高于99元")],
  [r("低门槛：", { bold: true }), r("每节课15-20分钟，碎片化学习")],
  [r("即时反馈：", { bold: true }), r("第1节课即给可操作技巧")],
  [r("埋钩子：", { bold: true }), r("课程中预告进阶内容，引导转化")],
]));
cc.push(el());
cc.push(mkTable([7,10,3,2,8], ["课程名称", "内容", "课时", "定价", "附加价值"], [
  ["《外贸AI获客实战课》", "AI提示词生成开发信、客户画像、邮件自动化", "5节×15分钟", "99元", "AI提示词库+SOP模板"],
  ["《LinkedIn外贸7天训练营》", "账号搭建、内容策略、InMail技巧、人脉扩展", "7天打卡", "99元", "话术模板+每日任务"],
  ["《外贸开发信从0到1》", "标题、正文、跟进策略、A/B测试", "4节×20分钟", "99元", "20个高回复率模板"],
]));

cc.push(h2("4.2 运营转化SOP"));
cc.push(p("购买99元课 → 自动入群 → 7天训练营（每日解锁）"));
cc.push(p("↓"));
cc.push(p("第3天：直播答疑 + 进阶课5折券 + 会员体验周"));
cc.push(p("↓"));
cc.push(p("第7天：结营 + 1v1私信（免费诊断邀约 / 线下课名额）"));
cc.push(p([r("↓", { italics: true }), r(" 转化路径：进阶课（15-25%）→ 会员（5-10%）→ 线下（3-5%）", { italics: true, color: "666666" })]));

cc.push(h2("4.3 私域分层"));
cc.push(mkTable([5,8,7,5], ["标签", "特征", "内容策略", "转化目标"], [
  ["企业主群", "年营收500万+，决策者", "宏观趋势、市场分析、风险合规", "私董会、平台服务"],
  ["外贸从业者群", "打工/创业初期，执行层", "战术技巧、工具使用、案例拆解", "进阶课、会员"],
  ["小白群", "新手/学生，兴趣导向", "基础概念、职业发展", "99元课、入门课"],
]));

cc.push(h2("4.4 数据指标"));
cc.push(mkTable([5,5,10], ["指标", "目标", "说明"], [
  ["99元课月销量", "2,000-3,000单", "自然流量+适度投放"],
  ["购买-入群率", ">80%", "自动化流程"],
  ["完课率", ">40%", "短课时+社群督促"],
  ["进阶课转化率", "15-25%", "从99元到499+元"],
  ["线下邀约成功率", "5-10%", "从99元买家到线下参与者"],
]));

cc.push(h2("4.5 【优化新增】完课率保障机制（针对SWOT分析W4转化断裂风险）"));
cc.push(p("为应对知识付费行业完课率不足15%的行业痛点，新丝路建立三层完课保障机制："));
cc.push(...bl([
  [r("打卡激励机制：", { bold: true }), r("设置\"完成全部课程+作业提交=获得线下课专属优惠券\"，将完课率与转化激励直接挂钩")],
  [r("数据监控漏斗：", { bold: true }), r("建立\"购买-入群-完课-转化\"四段式漏斗，每周监控各环节转化率，一旦发现异常立即调整")],
  [r("班主任陪跑：", { bold: true }), r("每期99元课配备1名班主任，每日在群内发布任务提醒、作业催交、答疑汇总，确保学员\"有人管、有人问\"")],
]));

cc.push(h2("4.6 【优化新增】透明化交付机制（针对SWOT分析T1行业信任危机）"));
cc.push(...bl([
  [r("购买前公示：", { bold: true }), r("课程详情页完整展示课程大纲、讲师背景、往期学员成果数据，让用户\"先验货再买单\"")],
  [r("7天无条件退款：", { bold: true }), r("开课后7天内无条件退款，以高信任门槛倒逼自身交付质量，与\"割韭菜\"型机构形成鲜明对比")],
  [r("学员成果报告：", { bold: true }), r("每期课程结束后发布《学员成果报告》，用真实数据证明课程价值")],
]));

// ═══ 五、第二层 ═══
cc.push(new Paragraph({ children: [new PageBreak()] }));
cc.push(h1("五、第二层：进阶课程与付费社群"));

cc.push(h2("5.1 进阶线上课"));
cc.push(mkTable([8,10,5,4], ["课程名称", "内容", "形式", "定价"], [
  ["《独立站+谷歌SEO全链路》", "建站、关键词、外链、转化率优化", "录播+4次直播答疑", "999元"],
  ["《跨境电商合规与海外公司架构》", "美国/欧洲/东南亚公司选择、VAT、商标", "录播+工具包", "1,499元"],
  ["《20年外贸老兵教你拿下大客户》", "客户开发、谈判、关系维护、案例库", "录播+社群陪跑", "1,999元"],
]));

cc.push(h2("5.2 付费社群"));
cc.push(mkTable([5,10,3,3], ["社群名称", "权益", "年费", "目标人数"], [
  ["新丝路研习社", "每月闭门分享、资源对接、课程8折、线下优先", "1,980元", "500人"],
  ["新丝路私董会（审核制）", "全年4次线下私享会、1v1顾问、海外考察优先、创始人群", "9,800元", "100人"],
]));
cc.push(p([r("私董会审核标准：", { bold: true })]));
cc.push(...bl([
  "企业年营收≥1,000万元",
  "已确定出海意向或有初步尝试",
  "创始人亲自参与",
]));

// ═══ 六、第三层 ═══
cc.push(new Paragraph({ children: [new PageBreak()] }));
cc.push(h1("六、第三层：线下会销矩阵"));

cc.push(h2("6.1 产品体系"));
cc.push(mkTable([5,7,4,5,4,5], ["产品", "形式", "规模", "定价", "频率", "目标"], [
  ["出海大课", "2天集中授课+案例拆解+晚宴", "100-300人", "3,800-5,800元", "每月1-2城", "批量转化进阶用户"],
  ["新丝路私董会", "闭门研讨+1v1诊断+圆桌", "10-20人", "12,800-29,800元/期", "每季度1期", "高净值客户深度绑定"],
  ["年度出海峰会", "主题演讲+圆桌+资源展+颁奖", "500-1,000人", "980-2,980元", "每年1次", "行业影响力+品牌IP"],
  ["海外考察团", "7-12天，参访+政府对接+市场调研", "15-30人", "38,000-88,000元", "每半年1次", "实地落地+高客单价"],
]));

cc.push(h2("6.2 城市巡回计划"));
cc.push(p([r("第一年覆盖城市：", { bold: true }), r("深圳、广州、宁波、苏州、青岛、成都、重庆、武汉（8城）")]));
cc.push(p([r("合作方：", { bold: true }), r("本地跨境电商协会、产业带商会、外贸综试区")]));

cc.push(h2("6.3 【优化新增】线下3天课的标准化交付体系（针对SWOT分析W2交付瓶颈）"));
cc.push(p("为应对线下课规模化过程中的交付质量风险，建立三级交付体系："));
cc.push(p([r("① 标准化SOP：", { bold: true }), r("将每一门线下课的实操环节拆解为\"步骤化清单\"，学员可按照清单自行完成60%的基础操作，助教只需在关键节点介入")]));
cc.push(p([r("② 助教分级制度：", { bold: true })]));
cc.push(mkTable([4,7,3], ["层级", "职责", "配比"], [
  ["主讲导师", "核心模块授课 + 关键诊断", "1人/场"],
  ["高级助教", "复杂问题诊断 + 方案审核", "1:15学员"],
  ["初级助教", "基础操作指导 + 作业批改", "1:8学员"],
]));
cc.push(p([r("③ 预训机制：", { bold: true }), r("线下课开课前2周，向学员发送\"课前预习包\"（含账号注册、工具安装等前置任务），确保线下时间全部用于高价值的实操和诊断")]));
cc.push(p([r("④ 规模控制：", { bold: true }), r("在模式验证期（前6个月）严格控制每期招生不超过40人，确保1:8的师生比，待SOP成熟后再逐步扩大")]));

// ═══ 七、第四层 ═══
cc.push(new Paragraph({ children: [new PageBreak()] }));
cc.push(h1("七、第四层：出海一体化服务平台"));

cc.push(h2("7.1 服务模块"));
cc.push(mkTable([5,10,5,5], ["模块", "具体内容", "收费模式", "合作方式"], [
  ["海外公司注册", "美国LLC、英国、新加坡、香港公司", "5,000-15,000元/单+年审", "自营+本地律所分成"],
  ["财税合规", "VAT注册申报、年度审计、税务筹划", "6,000-30,000元/年(托管)", "合作会计所"],
  ["知识产权", "美国/欧盟商标、专利申请", "3,000-20,000元/单", "合作知识产权代理"],
  ["银行开户", "远程开立海外公司账户", "2,000-5,000元/单", "合作金融机构"],
  ["产品准入", "CE/FCC/ROHS等认证咨询", "按项目报价", "合作实验室"],
  ["供应链金融", "出口信用保险、订单融资", "佣金2-5%", "合作银行/保理"],
  ["国际物流", "海运/空运/海外仓对接", "佣金3-8%", "合作物流平台"],
]));

cc.push(h2("7.2 平台化路径"));
cc.push(...bl([
  [r("阶段一（1-2年）：", { bold: true }), r("自营核心服务（注册+咨询）+ 渠道合作模式")],
  [r("阶段二（2-3年）：", { bold: true }), r("搭建数字化服务平台（客户自助下单、进度追踪）")],
  [r("阶段三（3-5年）：", { bold: true }), r("开放生态，接入更多第三方服务商，赚取平台佣金")],
]));

cc.push(h2("7.3 【优化新增】海外服务网络分阶段建设计划（针对SWOT分析W3）"));
cc.push(mkTable([4,4,4,7], ["阶段", "时间", "覆盖市场", "核心任务"], [
  ["第一阶段", "第1年", "美国、英国、新加坡", "跑通服务流程、建立合作方准入机制"],
  ["第二阶段", "第2年", "欧盟（德国/荷兰）、香港", "复制已验证模式、搭建数字化平台"],
  ["第三阶段", "第3年", "东南亚、中东", "覆盖全球主要市场的服务网络"],
]));
cc.push(p([r("合作方准入标准：", { bold: true })]));
cc.push(...bl([
  "在当地持牌经营5年以上",
  "有服务中国企业的成功案例",
  "签订明确的责任划分协议",
  "建立\"合作方准入→定期评估→淘汰\"机制",
]));

cc.push(h2("7.4 【优化新增】跨境合规风险防控体系（针对SWOT分析T5）"));
cc.push(...bl([
  [r("服务范围书面确认：", { bold: true }), r("在服务协议中明确新丝路的服务范围仅限于\"信息提供和渠道对接\"")],
  [r("合规保险：", { bold: true }), r("购买专业责任保险，覆盖因服务失误导致的赔偿风险")],
  [r("持续合规培训：", { bold: true }), r("定期对团队进行跨境合规培训")],
  [r("客户告知书：", { bold: true }), r("明确告知客户海外公司注册、财税申报等服务的风险边界，客户签字确认")],
]));

// ═══ 八、盈利点矩阵 ═══
cc.push(new Paragraph({ children: [new PageBreak()] }));
cc.push(h1("八、盈利点矩阵（99元锚点版完整测算）"));

cc.push(h2("8.1 三年收入预测"));
cc.push(mkTable([3,4,3,4,4,5], ["盈利层", "产品", "客单价", "第1年", "第2年", "第3年（成熟期）"], [
  ["L1引流课", "99元系列", "99元", "10,000单→99万", "20,000单→198万", "30,000单→297万"],
  ["L2进阶课", "499-1,999元", "均899元", "500人→45万", "1,500人→135万", "3,000人→270万"],
  ["L3付费社群", "会员/私董会", "均4,800元", "100人→48万", "300人→144万", "800人→384万"],
  ["L4线下会销", "大课+私董会+峰会+考察", "均15,000元", "100人次→150万", "300人次→450万", "600人次→900万"],
  ["L5平台服务", "注册/财税/IP等", "年均8,000元/企", "100家→80万", "500家→400万", "1,500家→1,200万"],
  ["L6 B端合作", "政府/商会内训", "均5万", "10单→50万", "30单→150万", "60单→300万"],
  ["L7生态衍生", "佣金/撮合/广告", "—", "50万", "300万", "2,000万+"],
]));
cc.push(el());
cc.push(p([r("合计", { bold: true, size: 21 }), r("：", { bold: true }), r("第1年522万 → 第2年1,777万 → 第3年5,351万+", { bold: true, color: "1F4E79", size: 21 })]));
cc.push(el());
cc.push(p([r("数据说明：", { bold: true }), r("99元课3万单的年销量目标，基于几十万粉丝存量中5%-8%的基础转化率（首年即可产生1.5万-2.4万购买用户），叠加内容矩阵日均触达10万+流量的持续新增。行业头部案例验证了优质IP在极短周期内即可完成大规模用户转化——网红经济学家洪灏的知识星球899元/年，10天吸引超8,500人加入。3万单属于基于保守估计的可行目标。", { size: 19, color: "555555" })]));

cc.push(h2("8.2 成本与利润结构（成熟期）"));
cc.push(mkTable([5,4,8], ["成本项", "占比", "金额（万元）"], [
  ["内容生产（AI辅助）", "5%", "268"],
  ["平台技术（SaaS+定制）", "8%", "428"],
  ["团队人力（15-20人）", "20%", "1,070"],
  ["营销获客（投放+渠道分润）", "15%", "803"],
  ["海外合作方成本", "20%", "1,070"],
  ["其他（办公/差旅/活动）", "10%", "535"],
  [new TextRun({ text: "总成本", bold: true, size: 17 }), new TextRun({ text: "78%", bold: true, size: 17 }), new TextRun({ text: "4,174", bold: true, size: 17 })],
  [new TextRun({ text: "毛利", bold: true, size: 17, color: "1F4E79" }), new TextRun({ text: "22%", bold: true, size: 17, color: "1F4E79" }), new TextRun({ text: "1,177", bold: true, size: 17, color: "1F4E79" })],
]));
cc.push(p([r("注：", { bold: true, size: 19, italics: true }), r("生态衍生收入（2,000万）成本极低，实际净利率可达30%以上。", { size: 19, italics: true, color: "666666" })]));

cc.push(h2("8.3 核心财务指标"));
cc.push(mkTable([2,7], ["指标", "数值"], [
  ["单个99元用户LTV", "约2,400元"],
  ["获客成本（CAC）", "可控在300元以内"],
  ["LTV/CAC", ">8（健康）"],
  ["整体毛利率", "30-35%"],
  ["净利率（成熟期）", "20-25%"],
  ["投资回收期", "12-18个月"],
]));

// ═══ 九、实施路线图 ═══
cc.push(new Paragraph({ children: [new PageBreak()] }));
cc.push(h1("九、实施路线图"));

cc.push(h2("阶段一：品牌奠基期（0-6个月）"));
cc.push(mkTable([4,16], ["时间", "关键任务"], [
  ["第1个月", "粉丝分层梳理、99元课大纲设计、AI内容工具搭建"],
  ["第2-3个月", "录制99元引流课、上线小鹅通/私域、发布首期白皮书；同步申请教育培训相关资质（ICP备案等）"],
  ["第4个月", "99元课正式推广，跑通\"购买-入群-训练营-转化\"全流程；建立四段式数据监控漏斗"],
  ["第5-6个月", "举办首场线下大课（控制在40人以下，验证1:8师生比模型）；启动海外合作渠道（首批聚焦美国、英国、新加坡）"],
]));
cc.push(p([r("里程碑：", { bold: true }), r("99元课累计销售3,000单；私域企业主粉丝新增5,000人；首场大课营收20万+。")]));

cc.push(h2("阶段二：规模化增长期（6-18个月）"));
cc.push(mkTable([4,16], ["时间", "关键任务"], [
  ["第7-9个月", "进阶课程上线、新丝路研习社会员启动；建立助教培养体系（首批培养3-5名核心助教）"],
  ["第10-12个月", "私董会首期举办、年度峰会筹备、平台服务V1.0上线；启动\"品牌IP化\"过渡"],
  ["第13-15个月", "城市巡回扩至8城、海外考察团首发；助教体系复制到各城市站点"],
  ["第16-18个月", "平台服务客户累计200+；私域企业主粉丝达5万+；完成从\"个人IP\"到\"新丝路品牌IP\"的初步过渡"],
]));
cc.push(p([r("里程碑：", { bold: true }), r("年营收突破1,000万；团队扩至15人。")]));

cc.push(h2("阶段三：生态成熟期（18-36个月）"));
cc.push(mkTable([4,16], ["时间", "关键任务"], [
  ["第19-24个月", "数字化服务平台上线、开放第三方服务商入驻；建立讲师矩阵（邀请行业专家、成功学员加入讲师团队）"],
  ["第25-30个月", "生态衍生收入规模化（佣金/金融/撮合）；海外服务网络扩展至欧盟市场"],
  ["第31-36个月", "打造出海生态\"智库\"，覆盖30+产业带城市；个人IP依赖度降低50%以上"],
]));
cc.push(p([r("里程碑：", { bold: true }), r("年营收突破5,000万；服务企业累计2,000+；成为出海服务领域头部品牌。")]));

// ═══ 十、风险与防范 ═══
cc.push(new Paragraph({ children: [new PageBreak()] }));
cc.push(h1("十、风险与防范（基于SWOT深度分析优化版）"));
cc.push(mkTable([4,8,10], ["风险类别", "风险描述", "防范措施"], [
  ["W1：IP依赖风险", "高度依赖创始人个人IP，个人风险可能传导至品牌", "①助教培养体系+SOP复制 ②个人IP→品牌IP升级 ③讲师矩阵"],
  ["W2：交付能力瓶颈", "线下3天课规模化需要大量助教支持", "①标准化SOP ②助教分级制度 ③预训机制 ④前6个月≤40人"],
  ["W3：海外网络建设周期长", "海外网络搭建慢，服务承诺可能无法兑现", "①分阶段推进 ②严选合作方 ③服务边界清晰"],
  ["W4：转化断裂", "行业完课率不足15%", "①打卡激励 ②四段式漏斗 ③班主任陪跑"],
  ["T1：行业信任危机", "\"割韭菜\"乱象频发", "①购买前公示 ②7天退款 ③学员成果报告"],
  ["T2：监管趋严", "教育培训行业监管收紧", "①资质合规前置 ②规范合同 ③法律顾问"],
  ["T3：竞品跟进", "山海图等向下延伸进培训", "①速度优先建认知 ②差异化欧美市场 ③IP温度壁垒"],
  ["T5：海外法律风险", "多国法律体系差异", "①服务范围书面确认 ②合规保险 ③持续培训 ④客户告知书"],
]));

// ═══ 十一、核心竞争力总结 ═══
cc.push(new Paragraph({ children: [new PageBreak()] }));
cc.push(h1("十一、核心竞争力总结"));
cc.push(p("新丝路·企业主会的不可复制壁垒："));
cc.push(...bl([
  [r("1. IP认知壁垒：", { bold: true }), r("几十万粉丝的信任 + 20年外贸实战 = 出海知识领域的第一KOL心智")],
  [r("2. 私域企业主社群：", { bold: true }), r("粉丝中沉淀了大量国内制造企业决策者，形成精准获客池")],
  [r("3. 海外本地化网络：", { bold: true }), r("20年积累的律师、会计师、物流、政府资源，快速搭建服务生态")],
  [r("4. 99元→高客单价平滑阶梯：", { bold: true }), r("产品线设计科学，用户自然向上流动，拒绝\"割韭菜\"")],
  [r("5. 结果导向的闭环：", { bold: true }), r("不只是卖课，而是真正帮助企业注册公司、合规运营、拿到订单")],
  [r("6. 丝路文化底蕴+政策高度：", { bold: true }), r("品牌名自带\"一带一路\"红利，更容易获得政府与商会资源支持")],
]));

cc.push(h2("【优化新增】从\"个人IP\"到\"品牌IP\"的过渡路径"));
cc.push(mkTable([4,7,10], ["阶段", "策略", "关键动作"], [
  ["0-6个月", "IP势能最大化", "创始人全力出镜，建立内容壁垒和信任基础"],
  ["6-18个月", "品牌化过渡", "培养助教团队、标准化SOP、\"新丝路方法论\"统一输出"],
  ["18个月+", "品牌IP独立化", "讲师矩阵成型、品牌认知超越个人、个人依赖度降低50%以上"],
]));

// ═══ 十二、启动行动清单 ═══
cc.push(new Paragraph({ children: [new PageBreak()] }));
cc.push(h1("十二、启动行动清单（第一个月）"));
cc.push(...bl([
  [r("第1周：", { bold: true }), r("梳理粉丝画像，统计企业主占比、行业分布、地域分布；整理20年外贸案例库")],
  [r("第2周：", { bold: true }), r("用AI辅助产出第一版99元课大纲和3节样片；注册\"新丝路\"品牌商标和公众号/视频号；启动ICP备案等资质申请")],
  [r("第3周：", { bold: true }), r("发布首条品牌宣发视频，私域预热99元课；联系3个地方商会洽谈合作")],
  [r("第4周：", { bold: true }), r("99元课正式上架小鹅通，启动第一轮推广（粉丝群+朋友圈+直播）；确定首场线下大城市（深圳）；建立四段式数据监控漏斗")],
]));

cc.push(el()); cc.push(el());
cc.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 300 },
  children: [r("新丝路——让中国制造走得更远。", { bold: true, size: 28, color: "1F4E79" })],
}));
cc.push(el());
cc.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 100 },
  children: [r("本商业模型为创始人20年经验与IP势能的系统化落地，经SWOT深度分析后优化，欢迎进一步探讨细节模块的深化设计。", { size: 18, italics: true, color: "888888" })],
}));

// ═══════════════════════════════════════════════════════════
// BUILD DOCUMENT
// ═══════════════════════════════════════════════════════════

// ── Cover Page ──
const cover = [
  el(), el(), el(), el(), el(),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 }, children: [r("新丝路·企业主会", { size: 52, bold: true, color: "1F4E79" })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 }, children: [r("基于IP存量的全链路出海服务平台", { size: 36, bold: true, color: "2E75B6" })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [r("商业模型", { size: 36, bold: true, color: "2E75B6" })] }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 200 },
    children: [r("（99元引流课锚点版·完整方案·经SWOT深度分析后优化）", { size: 22, color: "555555" })],
  }),
  sep(),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [r("2026年6月", { size: 22, color: "888888" })] }),
  el(), el(), el(), el(), el(), el(),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [r("新丝路——让中国制造走得更远", { size: 20, color: "1F4E79", italics: true })] }),
];

const doc = new Document({
  styles: {
    default: { document: { run: { font: FONT, size: 21 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: FONT, color: "1F4E79" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: FONT, color: "2E75B6" },
        paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 1 } },
    ],
  },
  numbering,
  sections: [
    { properties: { page: { size: { width: PW, height: PH }, margin: { top: MG, right: MG, bottom: MG, left: MG } } }, children: cover },
    {
      properties: { page: { size: { width: PW, height: PH }, margin: { top: MG, right: MG, bottom: MG, left: MG } } },
      headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [r("新丝路·企业主会 商业模型", { size: 16, color: "999999" })] })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [r("- ", { font: "Arial", size: 18, color: "999999" }), new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: "999999" }), r(" -", { font: "Arial", size: 18, color: "999999" })] })] }) },
      children: [new TableOfContents("目录", { hyperlink: true, headingStyleRange: "1-2" }), ...cc],
    },
  ],
});

const outPath = "C:\\Users\\ASDCF\\.qclaw\\workspace\\新丝路_企业主会商业模型.docx";
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outPath, buf);
  console.log("OK: " + outPath + " (" + (buf.length / 1024).toFixed(1) + " KB)");
}).catch(err => { console.error("ERROR:", err); process.exit(1); });
