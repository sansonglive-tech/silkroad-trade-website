const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat,
  HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak
} = require('docx');

// Chinese smart quotes as constants to avoid JS string issues
const LQ = '\u201C'; // left curly double quote
const RQ = '\u201D'; // right curly double quote
const LS = '\u2018'; // left single curly
const RS = '\u2019'; // right single curly

const A4_W = 11906, A4_H = 16838;
const M = { top: 1440, right: 1440, bottom: 1440, left: 1440 };
const FONT = 'Microsoft YaHei';

const border = { style: BorderStyle.SINGLE, size: 1, color: '999999' };
const borders = { top: border, bottom: border, left: border, right: border };
const headerShading = { fill: '1F4E79', type: ShadingType.CLEAR };
const altShading = { fill: 'F2F7FB', type: ShadingType.CLEAR };
const cellMargins = { top: 60, bottom: 60, left: 100, right: 100 };

function tr(text, opts = {}) {
  const t = typeof text === 'string' ? text : '';
  const bold = opts.bold || false;
  const color = opts.color || '000000';
  return new TextRun({ text: t, font: FONT, size: opts.size || 22, bold, color, ...opts.runOpts });
}

function p(items, opts = {}) {
  const runs = [];
  if (typeof items === 'string') {
    runs.push(tr(items, opts));
  } else if (Array.isArray(items)) {
    for (const item of items) {
      if (typeof item === 'string') {
        runs.push(tr(item, opts));
      } else {
        runs.push(tr(item.text || '', { ...opts, ...item }));
      }
    }
  }
  return new Paragraph({
    spacing: { before: opts.before || 60, after: opts.after || 60, line: opts.line || 360 },
    alignment: opts.align || AlignmentType.LEFT,
    indent: opts.indent,
    ...opts.paraOpts,
    children: runs,
  });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 300, after: 120 },
    children: [new TextRun({ text, font: FONT, bold: true, size: 36, color: '1F4E79' })],
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 200, after: 120 },
    children: [new TextRun({ text, font: FONT, bold: true, size: 30, color: '2E75B6' })],
  });
}

function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 160, after: 80 },
    children: [new TextRun({ text, font: FONT, bold: true, size: 26, color: '2E75B6' })],
  });
}

function cell(textItems, opts = {}) {
  const runs = [];
  const items = Array.isArray(textItems) ? textItems : [textItems];
  for (const item of items) {
    if (typeof item === 'string') {
      runs.push(new TextRun({ text: item, font: FONT, size: opts.size || 20, bold: opts.bold, color: opts.color || '000000' }));
    } else {
      runs.push(new TextRun({ text: item.text || '', font: FONT, size: item.size || opts.size || 20, bold: item.bold || opts.bold, color: item.color || opts.color || '000000' }));
    }
  }
  return new TableCell({
    borders,
    width: { size: opts.w || 3000, type: WidthType.DXA },
    shading: opts.shading || undefined,
    margins: cellMargins,
    verticalAlign: opts.valign || 'center',
    children: [new Paragraph({
      spacing: { before: 20, after: 20, line: 300 },
      alignment: opts.align || AlignmentType.LEFT,
      children: runs,
    })],
  });
}

function hdrCell(text, w) {
  return cell(text, { w, bold: true, shading: headerShading, color: 'FFFFFF', size: 20 });
}

function datCell(text, w, alt) {
  return cell(text, { w, shading: alt ? altShading : undefined, size: 20 });
}

function makeTable(headers, rows, colWidths) {
  const totalW = colWidths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: totalW, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [
      new TableRow({ children: headers.map((h, i) => hdrCell(h, colWidths[i])) }),
      ...rows.map((r, i) => new TableRow({ children: r.map((c, j) => datCell(c, colWidths[j], i % 2 === 1)) })),
    ],
  });
}

function emptyLine(h = 40) {
  return new Paragraph({ spacing: { before: h, after: h }, children: [new TextRun({ text: '', font: FONT, size: 22 })] });
}

function pb() {
  return new Paragraph({ children: [new PageBreak()] });
}

// ========== Content ==========
const children = [];

// Title page
children.push(new Paragraph({ spacing: { before: 3000 }, children: [] }));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 200 },
  children: [new TextRun({ text: `新丝路跨境${LQ}实战${RQ}出海`, font: FONT, size: 56, bold: true, color: '1F4E79' })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 400 },
  children: [new TextRun({ text: '第二套商业模式', font: FONT, size: 36, color: '2E75B6' })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 200 },
  children: [new TextRun({ text: '以交付为基石的企业出海全链路服务平台', font: FONT, size: 32, bold: true, color: '1F4E79' })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 100 },
  children: [new TextRun({ text: `\u2014\u2014${LQ}让每一次出海都有人陪跑到底${RQ}`, font: FONT, size: 26, color: '666666', italics: true })],
}));
children.push(pb());

// ===== 一 =====
children.push(h1('一、核心定位与品牌逻辑'));

children.push(h2('1.1 品牌定位'));
children.push(p([
  { text: '品牌名称', bold: true },
  { text: `：新丝路跨境${LQ}实战${RQ}出海（核心品牌）\u2014\u2014以下简称${LQ}新丝路跨境${RQ}` },
]));
children.push(p([
  { text: '品牌Slogan', bold: true },
  { text: `：实战出海，交付为王\u2014\u2014让每一次出海都有人陪跑到底。` },
]));
children.push(p([
  { text: '核心定位', bold: true },
  { text: `：以交付为基本前提、以结果为导向的外贸全链路服务平台。区别于市面上${LQ}割韭菜式${RQ}的知识付费，新丝路跨境的核心逻辑是：` },
  { text: `99元不是终点，而是信任的起点；3天线下不是表演，而是结果的开始；平台服务不是增值，而是交付的延续。`, bold: true },
]));

children.push(h2('1.2 品牌核心资产'));
children.push(p([
  { text: '雨哥IP', bold: true },
  { text: `：几十万粉丝的外贸实战专家，20年外贸全链路实战经验，人设锚定为${LQ}外贸老兵${RQ}${LQ}工厂主的出海导航员${RQ}` },
]));
children.push(p([
  { text: '专业壁垒', bold: true },
  { text: '：跨境电商全链路实操能力（LinkedIn/Sales Navigator/独立站/AI获客）+ 海外落地资源网络 + 产业带供应链整合能力' },
]));
children.push(p([
  { text: '信任资产', bold: true },
  { text: '：粉丝群体精准分层（企业主/外贸从业者/创业者），已建立长期的认知信任' },
]));

children.push(h2('1.3 品牌差异化逻辑'));
children.push(makeTable(
  ['维度', '市面上主流模式', '新丝路跨境模式'],
  [
    ['核心逻辑', `${LQ}卖完课走人${RQ}\u2014\u2014以课程销售为终点`, `${LQ}卖完课只是起点${RQ}\u2014\u2014以课程为入口，交付在课后`],
    ['交付方式', '线上录播+社群答疑（轻交付）', '线上工具流 + 线下3天实战全案落地 + 社群陪跑（重交付）'],
    ['课程设计', '理论堆砌、通用技巧', '可复制的SOP + 每一节课带出一个可执行动作 + 现场实操'],
    ['IP定位', `${LQ}知识博主${RQ}\u2014\u2014卖认知`, `${LQ}出海陪跑教练${RQ}\u2014\u2014卖结果`],
    ['服务链路', '止步于知识交付', '知识\u2192方案\u2192执行\u2192增长\u2192生态，全链路打通'],
  ],
  [1500, 3500, 4026]
));
children.push(emptyLine());

children.push(h2(`1.4 ${LQ}交付为王${RQ}的落地逻辑`));
children.push(p(`新丝路跨境的${LQ}交付${RQ}不是一句口号，而是从产品设计到服务流程全面贯彻的闭环：`));
children.push(p([
  { text: '1. 课程交付：每一节课解决一个具体问题', bold: true },
  { text: `\u2014\u2014不是讲宏观趋势，而是讲${LQ}今天回去能马上落地的事${RQ}` },
]));
children.push(p([
  { text: '2. 线下交付：3天不是听课，是"干出来"', bold: true },
  { text: '\u2014\u2014每位学员带着自己的产品或目标市场，现场搭建账号、现场写开发信、现场制定获客计划' },
]));
children.push(p([
  { text: '3. 陪跑交付：结课不是结束，是陪跑的开始', bold: true },
  { text: '\u2014\u201430天线上陪跑群 + 每周直播诊断 + 无限次问答' },
]));
children.push(p([
  { text: '4. 平台交付：知识跑通了，服务接着干', bold: true },
  { text: '\u2014\u2014合规、注册、物流、金融，一站配齐' },
]));

// ===== 二 =====
children.push(pb());
children.push(h1('二、商业模型总览'));
children.push(p('三层递进模型：以雨哥IP为信任前置，通过99元门票课建立流量蓄水池，以3天线下实战课为核心转化引擎，最终以出海全链路服务平台实现长期价值绑定。'));
children.push(emptyLine());

children.push(p([
  { text: '第一层：99元门票课（流量蓄水池）', bold: true, size: 24, color: '1F4E79' },
]));
children.push(p('\u2022 只讲一个完整技能（LinkedIn/AI开发信/LBS搜索）', { indent: { left: 360 } }));
children.push(p('\u2022 第7天直播答疑 + 课后作业批改 + 进阶邀约', { indent: { left: 360 } }));
children.push(p('\u2022 目标：让学员在7天内拿到一个可量化结果', { indent: { left: 360 } }));
children.push(p('\u2022 转化率：8-15%（99元门票课\u2192线下课）', { indent: { left: 360 } }));
children.push(emptyLine());

children.push(p([
  { text: '第二层：3天线下实战课（核心转化引擎）', bold: true, size: 24, color: '1F4E79' },
]));
children.push(p(`\u2022 每期一个主题，形式为${LQ}带电脑来，现场干${RQ}`, { indent: { left: 360 } }));
children.push(p('\u2022 内容：账号搭建 \u2192 AI获客 \u2192 独立站建设 \u2192 客户转化 \u2192 合规架构', { indent: { left: 360 } }));
children.push(p('\u2022 陪跑：结课后30天线上陪跑 + 每周直播诊断', { indent: { left: 360 } }));
children.push(p('\u2022 增值：结课后6个月内第一笔订单，平台抽佣', { indent: { left: 360 } }));
children.push(p('\u2022 转化率：20-30%（线下课\u2192平台服务）', { indent: { left: 360 } }));
children.push(emptyLine());

children.push(p([
  { text: '第三层：出海全链路服务平台（终极价值闭环）', bold: true, size: 24, color: '1F4E79' },
]));
children.push(p('\u2022 海外公司注册 / 财税合规 / 知识产权 / 产品认证', { indent: { left: 360 } }));
children.push(p('\u2022 社媒代运营 / 独立站代建 / AI获客工具', { indent: { left: 360 } }));
children.push(p('\u2022 供应链金融 / 物流对接 / 海外仓储', { indent: { left: 360 } }));
children.push(emptyLine());
children.push(p([
  { text: '盈利闭环：', bold: true },
  { text: '99元建立信任 \u2192 线下课深度交付 \u2192 平台服务长期绑定（信任\u2192结果\u2192依赖，三阶递进，实现客户全生命周期服务）' },
]));

// ===== 三 =====
children.push(pb());
children.push(h1('三、第一层：99元门票课\u2014\u2014流量蓄水池'));

children.push(h2('3.1 产品设计原则'));
children.push(p('99元门票课的定位不是盈利，而是以极低门槛建立一个足够深的流量蓄水池。核心设计原则：'));
children.push(p([
  { text: '一个主题，一个完整技能', bold: true },
  { text: '：7天内只讲一个可落地的技能（如LinkedIn获客、AI开发信），不讲大而全' },
], { indent: { left: 360 } }));
children.push(p([
  { text: '可量化结果', bold: true },
  { text: '：学员必须在7天内产出一个可验证的结果（如发了多少开发信、获得了多少回复）' },
], { indent: { left: 360 } }));
children.push(p([
  { text: '超预期交付', bold: true },
  { text: '：99元的价格，交付的是999元的价值感（资料包、模板、AI提示词库等）' },
], { indent: { left: 360 } }));
children.push(p([
  { text: '激励进阶', bold: true },
  { text: '：第7天直播时，释放线下课的早鸟价，并展示往期学员的成果案例' },
], { indent: { left: 360 } }));

children.push(h2('3.2 课程体系设计'));

children.push(h3('课程1：《LinkedIn外贸7天实战训练营》'));
children.push(makeTable(
  ['天数', '内容'],
  [
    ['第1天', '账号定位\u2014\u2014Profile优化 + Headline黄金公式 + 视觉升级'],
    ['第2天', '精准建联\u2014\u2014搜索方法论 + 邀请语工程 + 决策链识别'],
    ['第3天', '内容破冰\u2014\u2014矩阵式内容设计 + 引发自然询盘的内容逻辑'],
    ['第4天', '获客触达\u2014\u20143-7-21法则 + 批量化管理技巧 + 挖掘决策人'],
    ['第5天', '成交路径\u2014\u2014跟进节奏把控 + 询盘转化 + 从公域到私域'],
    ['第6天', 'AI赋能获客\u2014\u2014智能化背调 + Prompt指令库 + 批量个性化生成'],
    ['第7天', '直播复盘 + 成果拆解 + 高阶课邀约'],
  ],
  [1200, 7826]
));
children.push(emptyLine());

children.push(h3('课程2：《AI驱动外贸开发信实战训练营》'));
children.push(makeTable(
  ['天数', '内容'],
  [
    ['第1天', '背调篇\u2014\u2014用AI快速分析目标公司官网、社媒、海关数据'],
    ['第2天', '指令篇\u2014\u2014构建外贸专属Prompt库，掌握有效提示词的底层逻辑'],
    ['第3天', '内容篇\u2014\u2014用AI生成多版本开发信，打造高回复率模板库'],
    ['第4天', '场景篇\u2014\u2014开发信/跟进信/邀约函/节日问候等场景全覆盖'],
    ['第5天', '优化篇\u2014\u2014基于回复数据迭代指令，持续优化邮件质量'],
    ['第6天', '进阶篇\u2014\u2014邮件自动化 + A/B测试 + 邮件送达优化'],
    ['第7天', '直播复盘 + 成果展示 + 线下课邀约'],
  ],
  [1200, 7826]
));
children.push(emptyLine());

children.push(h3('课程3：《外贸社媒矩阵获客训练营》'));
children.push(makeTable(
  ['天数', '内容'],
  [
    ['第1天', 'Facebook\u2014\u2014个人号搭建 + 专业形象打造 + 精准群组获客'],
    ['第2天', 'Instagram\u2014\u2014视觉化内容设计 + 产品展示技巧'],
    ['第3天', 'TikTok\u2014\u2014短视频内容策略 + 爆款逻辑 + B2B获客应用'],
    ['第4天', 'YouTube\u2014\u2014产品测评视频制作 + 关键词布局 + 吸引精准询盘'],
    ['第5天', 'WhatsApp\u2014\u2014跨国沟通礼仪 + 高效跟进 + 客户关系维护'],
    ['第6天', '全社媒联动\u2014\u2014各平台差异化定位 + 内容分发策略'],
    ['第7天', '直播复盘 + 成果展示 + 线下课邀约'],
  ],
  [1200, 7826]
));
children.push(emptyLine());

children.push(h2('3.3 交付标准与陪跑机制'));
children.push(p([
  { text: '结业标准', bold: true },
  { text: '：学员必须提交作业（如LinkedIn Profile前后对比、发出的开发信截图），合格后方可获得线下课优惠资格' },
]));
children.push(p([
  { text: '社群陪跑', bold: true },
  { text: `：购买后立即入群，每个工作日有${LQ}雨哥助手${RQ}发布任务提醒，晚8点有值班导师答疑` },
]));
children.push(p([
  { text: '第7天直播闭环', bold: true },
  { text: '：集中答疑 + 优秀学员分享 + 1v1诊断邀约 + 线下课早鸟通道开放' },
]));

// ===== 四 =====
children.push(pb());
children.push(h1('四、第二层：3天线下实战课\u2014\u2014核心转化引擎'));

children.push(h2('4.1 课程定位与设计理念'));
children.push(p([
  { text: '定位', bold: true },
  { text: `：这不是一堂${LQ}课${RQ}，而是一套${LQ}3天带电脑来，现场把活干出来${RQ}的实战全案。每位学员带着自己的产品、行业和目标市场来，3天后带着一套完整的出海作战方案走。` },
]));
children.push(p([
  { text: '核心交付逻辑', bold: true },
  { text: '：3天 = 70%实操 + 30%方法论。不搞纯理论灌输，每听完一个模块，马上现场执行，雨哥和助教团队逐一点评指导。' },
]));
children.push(p([
  { text: '主题化运营', bold: true },
  { text: '：每期聚焦一个主题，精准吸引对应行业的企业主，形成主题社群效应。' },
]));

children.push(p([
  { text: '全年课程规划', bold: true, size: 24, color: '2E75B6' },
]));
children.push(makeTable(
  ['月份', '主题', '课程标题', '目标行业', '核心内容'],
  [
    ['1月', '年度复盘启动', '出海经营回顾与战略重启会', '全行业', '外贸年度数据复盘 + 2026趋势预判 + 企业主出海战略规划'],
    ['2月', 'LinkedIn获客', '领英外贸全案特训营', '工业品/机械设备/制造业', 'LinkedIn获客全流程 + 精准内容体系 + 社媒信任资产构建'],
    ['3月', 'AI获客', 'AI驱动外贸客户开发实战营', '全行业', 'AI开发信全流程 + Prompt工程 + 邮件自动化'],
    ['4月', '独立站建设', '外贸独立站从0到1建站营', 'B2B品牌/有新品的企业', '建站实操 + SEO基础 + 流量获取策略'],
    ['5月', '欧洲市场', '欧盟合规与VAT实战营', '消费品/电子产品/家电', 'CE认证 + VAT申报 + 欧盟市场准入全流程'],
    ['6月', '北美市场', '美国公司注册与品牌落地营', '计划做品牌出海的企业', '美国公司架构 + 产品责任险 + 分销渠道搭建'],
    ['7月', '东南亚市场', '东南亚掘金与合规落地营', '消费品/快消品/制造业', '东南亚市场机会分析 + 当地公司注册 + 文化适配 + 本地化运营'],
    ['8月', 'TikTok B2B', 'TikTok社媒获客特训营', '消费品/年轻人品牌/快消品', '短视频内容创作 + 直播引流 + B2B线索获取'],
    ['9月', '独立站运营', '独立站转化率提升实战营', '已有独立站的企业', 'SEO实战 + 广告投放 + 数据分析与优化'],
    ['10月', '供应链金融', '海外仓与供应链金融实战营', '有库存/有物流需求的企业', '海外仓选型 + FBA vs 海外仓对比 + 供应链金融方案'],
    ['11月', '知识产权', '海外商标与品牌保护实战营', '有自主品牌的企业', '全球商标布局 + 防侵权策略 + 侵权应对'],
    ['12月', '年度峰会', '2026出海年度复盘与展望大会', '全行业企业主', '年度出海数据发布 + 趋势展望 + 资源对接会 + 颁奖晚宴'],
  ],
  [600, 1200, 2800, 1800, 2626]
));
children.push(emptyLine());

children.push(h2('4.2 核心课程模块全景'));

children.push(h3('模块一：【雨哥起航】账号搭建与数字资产建设（2小时）'));
children.push(p('\u2022 外贸个人IP打造的底层逻辑与顶层设计', { indent: { left: 360 } }));
children.push(p('\u2022 LinkedIn Profile优化实战（头像/背景/Headline/About/精选推荐）', { indent: { left: 360 } }));
children.push(p('\u2022 多社媒平台协同运营方法论', { indent: { left: 360 } }));
children.push(p(`\u2022 数字名片\u2014\u2014让每一个页面都成为${LQ}信任资产${RQ}`, { indent: { left: 360 } }));
children.push(emptyLine());

children.push(h3('模块二：【雨哥智获】AI精准获客与开发信体系（6小时）'));
children.push(p('\u2022 企业AI化方法：Prompt工程 + 外贸场景提示词库搭建', { indent: { left: 360 } }));
children.push(p('\u2022 用AI批量生成高质量开发信 + 打造企业专属开发信模板库', { indent: { left: 360 } }));
children.push(p('\u2022 客户背调自动化：AI辅助分析客户官网、社媒、海关数据', { indent: { left: 360 } }));
children.push(p('\u2022 邮件自动化 + A/B测试 + 回复率优化', { indent: { left: 360 } }));
children.push(p('\u2022 现场实操：每位学员带着自己的产品，现场写出一封高质量开发信', { indent: { left: 360 } }));
children.push(emptyLine());

children.push(h3('模块三：【雨哥聚力】LinkedIn深度获客全案（4小时）'));
children.push(p('\u2022 精准搜索：布尔运算符组合 + Sales Navigator深度使用', { indent: { left: 360 } }));
children.push(p('\u2022 决策链识别与突破策略 + 个性化连接请求模板库', { indent: { left: 360 } }));
children.push(p('\u2022 内容矩阵设计：打造行业影响力，让客户主动找上门', { indent: { left: 360 } }));
children.push(p('\u2022 3-7-21跟进法则 + 从连接到询盘的完整闭环', { indent: { left: 360 } }));
children.push(p('\u2022 现场实操：搜索目标客户名单、建联、撰写内容脚本', { indent: { left: 360 } }));
children.push(emptyLine());

children.push(h3('模块四：【雨哥建站】外贸独立站从0到1（4小时）'));
children.push(p('\u2022 Shopify vs WordPress vs 自研\u2014\u2014B2B/B2C如何选？', { indent: { left: 360 } }));
children.push(p('\u2022 SEO基础布局：关键词策略 + 元标签优化 + 内容规划', { indent: { left: 360 } }));
children.push(p('\u2022 转化率提升：表单设计 + 信任标识 + 案例展示', { indent: { left: 360 } }));
children.push(p('\u2022 Google Search Console + GA4数据分析入门', { indent: { left: 360 } }));
children.push(emptyLine());

children.push(h3('模块五：【雨哥合规】海外公司架构与合规落地（4小时）'));
children.push(p('\u2022 美国/欧洲/东南亚/香港/新加坡公司优劣势对比', { indent: { left: 360 } }));
children.push(p('\u2022 产品准入：CE/FCC/ROHS/REACH，什么必须做？', { indent: { left: 360 } }));
children.push(p('\u2022 海外商标注册：美国USPTO、欧盟EUIPO、马德里体系怎么选？', { indent: { left: 360 } }));
children.push(p('\u2022 VAT/销售税/所得税合规框架', { indent: { left: 360 } }));
children.push(emptyLine());

children.push(h3('模块六：【雨哥爆单】TikTok B2B社媒获客（4小时）'));
children.push(p('\u2022 B2B企业短视频内容规划与脚本创作', { indent: { left: 360 } }));
children.push(p('\u2022 TikTok算法逻辑与账号冷启动策略', { indent: { left: 360 } }));
children.push(p('\u2022 直播引流 + 询盘获取 + 私域转化', { indent: { left: 360 } }));
children.push(p('\u2022 真实案例拆解：如何用6秒产品视频获得200+询盘', { indent: { left: 360 } }));
children.push(emptyLine());

children.push(h3('模块七：【雨哥诊断】1v1企业出海诊断会（每期必做）'));
children.push(p(`\u2022 每位学员10分钟${LQ}问诊${RQ}\u2014\u2014抛出企业真实卡点`, { indent: { left: 360 } }));
children.push(p('\u2022 雨哥1v1点评 + 给出具体解决方案', { indent: { left: 360 } }));
children.push(p('\u2022 同学互评 + 群智共创', { indent: { left: 360 } }));
children.push(p('\u2022 现场输出《90天出海行动路线图》', { indent: { left: 360 } }));
children.push(emptyLine());

children.push(h3('模块八：【雨哥晚宴】私董交流 + 资源对接（每期必做）'));
children.push(p('\u2022 主题晚宴，轻松破冰，深度交流', { indent: { left: 360 } }));
children.push(p('\u2022 学员现场发布资源需求（找海外代理/找物流/找翻译）', { indent: { left: 360 } }));
children.push(p('\u2022 雨哥现场撮合匹配', { indent: { left: 360 } }));
children.push(p('\u2022 往期优秀学员经验分享', { indent: { left: 360 } }));
children.push(emptyLine());

children.push(h2(`4.3 每期线下课日程安排（以${LQ}LinkedIn+独立站${RQ}主题为例）`));
children.push(makeTable(
  ['时间', '内容', '形式', '交付物'],
  [
    ['Day 1 上午', '《雨哥起航》账号搭建\u2014\u2014LinkedIn Profile全面升级', '讲解+现场实操', '优化后的Profile、出海个人IP定位书'],
    ['Day 1 下午', '《雨哥智获》AI开发信体系\u2014\u2014Prompt工程+批量生成', '讲解+实操+1v1指导', '20+Prompt指令库、5版开发信模板'],
    ['Day 1 晚上', '雨哥晚宴+资源对接', '自由交流+匹配', '资源需求清单、至少3个有效资源对接'],
    ['Day 2 上午', '《雨哥聚力》LinkedIn深度获客\u2014\u2014搜索+建联+内容', '案例拆解+实操', '目标客户名单（50+）、已发出的连接请求'],
    ['Day 2 下午', '《雨哥建站》独立站从0到1\u2014\u2014搭建+SEO+转化', '实操+分组演练', '独立站框架方案、SEO关键词布局表'],
    ['Day 2 晚上', '分组复盘+作业完成+助教辅导', '小组讨论', '第一天和第二天的成果汇总'],
    ['Day 3 上午', '《雨哥合规》海外公司架构\u2014\u2014公司选择+商标+认证', '案例讲解+分组研讨', '企业出海架构方案初稿'],
    ['Day 3 下午', '雨哥诊断\u2014\u20141v1诊断+结营仪式+陪跑启动', '1v1+全体结营', '《90天行动路线图》、陪跑群入群'],
    ['课后30天', '线上陪跑+每周直播诊断', '微信群+直播', '每周成果复盘、下一个阶段的行动建议'],
  ],
  [1400, 3100, 1800, 2726]
));
children.push(emptyLine());

children.push(h2('4.4 课后陪跑体系'));
children.push(p(`\u2022 30天陪跑群：结课后立即进入陪跑群，助教每日发布${LQ}今日任务${RQ}`, { indent: { left: 360 } }));
children.push(p('\u2022 每周直播诊断：雨哥每周一次线上直播，针对学员实际卡点实时诊断', { indent: { left: 360 } }));
children.push(p('\u2022 成果追踪系统：学员每两周提交一次成果进度，雨哥团队逐一反馈', { indent: { left: 360 } }));
children.push(p(`\u2022 成果承诺：结课后6个月内，学员通过课程内容获得的第一笔订单，平台抽取5%作为${LQ}成功佣金${RQ}（上限不超过课程费用）`, { indent: { left: 360 } }));

children.push(h2('4.5 定价策略与目标'));
children.push(makeTable(
  ['产品', '价格', '全年场次', '目标总人次', '年收入目标'],
  [
    ['线下3天实战课', '3,800-6,800元', '全年11期，每期40-80人', '600-800人次', '300-500万元'],
    ['年度出海复盘峰会', '980-2,980元', '1场（500+人）', '500+人次', '50-100万元'],
    ['定制企业内训', '2-5万元/企', '根据需求定制', '20-30家企业', '50-100万元'],
  ],
  [1800, 1600, 2500, 1400, 1726]
));

// ===== 五 =====
children.push(pb());
children.push(h1('五、第三层：出海全链路服务平台'));

children.push(h2('5.1 平台定位与逻辑'));
children.push(p([
  { text: '定位', bold: true },
  { text: `：让${LQ}出海的企业不再被琐碎合规问题困住${RQ}的一站式服务平台` },
]));
children.push(p([
  { text: '核心逻辑', bold: true },
  { text: `：当学员通过线下课跑通了获客、接到了询盘、确认了订单，他们自然会产生${LQ}落地${RQ}需求\u2014\u2014注册海外公司、合规认证、商标保护、物流仓储\u2026\u2026新丝路跨境平台的价值就是承接这些需求，实现从${LQ}知识的交付${RQ}到${LQ}服务的交付${RQ}的自然过渡。` },
]));

children.push(h2('5.2 平台服务体系'));
children.push(p([{ text: '核心服务模块：', bold: true }]));
children.push(p('\u2022 海外公司注册与架构设计：美国/英国/香港/新加坡/东南亚公司注册 + 银行远程开户 + 年审维护 + 架构设计', { indent: { left: 360 } }));
children.push(p('\u2022 财税合规：VAT注册与申报 + 企业所得税 + 全球税务筹划 + 常设机构(PE)风险防控', { indent: { left: 360 } }));
children.push(p('\u2022 产品准入与知识产权：商标注册 + CE/FCC/ROHS认证 + 专利申请 + 版权登记', { indent: { left: 360 } }));
children.push(p('\u2022 海外推广与获客工具：独立站代建与运营 + LinkedIn代运营 + AI获客工具授权 + 社媒内容代制作', { indent: { left: 360 } }));
children.push(p('\u2022 物流与仓储：FBA头程 + 海外仓对接 + 国际物流比价 + 供应链金融', { indent: { left: 360 } }));
children.push(emptyLine());
children.push(p([{ text: '合作模式：', bold: true }]));
children.push(p('\u2022 核心服务自营（海外公司注册+财税咨询）', { indent: { left: 360 } }));
children.push(p('\u2022 第三方服务商入驻平台，平台抽佣（10-20%）', { indent: { left: 360 } }));
children.push(p(`\u2022 企业可按需购买服务打包，或选择${LQ}年度出海保障套餐${RQ}（年费19,800-49,800元）`, { indent: { left: 360 } }));

children.push(h2('5.3 服务入口与转化路径'));
children.push(p([
  { text: '线下课 ', bold: true },
  { text: '\u2192 陪跑期 \u2192 产生服务需求 \u2192 平台服务入口 \u2192 签约 \u2192 ' },
  { text: '长期绑定', bold: true },
], { align: AlignmentType.CENTER }));

// ===== 六 =====
children.push(pb());
children.push(h1('六、盈利点矩阵'));

children.push(h2('6.1 三层收入结构'));
children.push(makeTable(
  ['盈利层', '产品/服务', '客单价', '年收入目标（成熟期）', '毛利率'],
  [
    ['L1：引流层', '99元门票课', '99元', '30,000单\u2192297万', '60%'],
    ['L2：转化层', '线下3天实战课', '均价5,000元', '800人\u2192400万', '50%'],
    ['L2：转化层', '年度峰会', '均价1,500元', '600人\u219290万', '40%'],
    ['L2：转化层', '企业内训/定制', '均价3万', '30单\u219290万', '60%'],
    ['L3：平台层', '海外公司注册', '5,000-15,000元', '300单\u2192300万', '40%'],
    ['L3：平台层', '年度合规托管', '12,000-30,000元', '150家企业\u2192270万', '35%'],
    ['L3：平台层', '独立站代建/运营', '8,000-50,000元', '100单\u2192200万', '50%'],
    ['L3：平台层', '年度出海保障套餐', '19,800元', '100家\u2192198万', '50%'],
    ['L3：平台层', '第三方服务抽佣', '5,000-20,000元/单', '抽佣收入200万', '90%'],
  ],
  [1200, 2000, 1800, 2226, 1800]
));
children.push(emptyLine());

// Summary row
children.push(makeTable(
  ['', '', '', '', ''],
  [
    [{ text: '\u2014', bold: true }, { text: '\u2014', bold: true }, { text: '\u2014', bold: true }, { text: '约2,045万', bold: true }, { text: '整体约50%', bold: true }],
  ],
  [1200, 2000, 1800, 2226, 1800]
));
children.push(emptyLine());

children.push(h2('6.2 核心财务指标'));
children.push(makeTable(
  ['指标', '数值'],
  [
    ['单个99元用户LTV', '约2,500-3,500元（包含线下课+平台服务）'],
    ['线下课转化率（99元\u2192线下课）', '8-15%'],
    ['平台服务转化率（线下课\u2192平台）', '20-30%'],
    ['整体净利率（成熟期）', '25-30%'],
    ['获客成本（CAC）', '200-300元'],
    ['LTV/CAC', '>10（健康）'],
  ],
  [3000, 6026]
));

// ===== 七 =====
children.push(pb());
children.push(h1('七、行业数据支撑'));
const industryData = [
  `\u2022 全球职场用户超过10亿，其中超过6,500万为B2B决策者活跃在LinkedIn上，是外贸企业获取精准客户的黄金渠道`,
  `\u2022 LinkedIn账号的专业化改造是获客的第一步，个人资料需围绕${LQ}产品解决方案提供者${RQ}而非${LQ}销售${RQ}定位进行优化`,
  `\u2022 全球超过90%的B2B决策者活跃于此，可按行业、职能等维度精准定位目标客户，以打造专业品牌形象和深度展示企业实力`,
  `\u2022 LinkedIn本身的数据表明，它被招聘者、企业领导者和B2B买家平等信任，仍然是与职业相关的数字活动最常用的领域`,
  `\u2022 用AI重构外贸开发信流程，通过结构化提示词工程，回复率可从传统的0.5%提升至8%左右，提升16倍`,
  `\u2022 跨境邮件自动化使用AI生成专业B2B开发信已成为常态，核心原则是提供清晰背景信息 + 明确指令`,
  `\u2022 GoGlobal环瑀提供企业一站式出海服务，包括公司注册、全球薪酬管理、会计与税务合规、人力资源咨询等`,
  `\u2022 万企帮集团服务覆盖全球213个国家和地区，设立36个本地直营交付中心，累计服务184,071家全球性企业`,
  `\u2022 税无忧整合全球120+国家/地区的本地化资源，提供${LQ}全球公司注册+财税合规管理+ODI备案代办+多币种银行开户${RQ}的全链条服务`,
  `\u2022 2025年中国电动两轮车出口量突破2,670万辆，出口额达68.29亿美元，2026年Q1同比增长68.2%`,
  `\u2022 Wavytalk从事代工多年后借助跨境电商平台走出国门，在TikTok Shop美国市场3年累计营收超过2亿美元`,
  `\u2022 新国货品牌追觅通过设计美学和底层技术创新重新定义全球化产品，从${LQ}跟随经典设计${RQ}转向${LQ}提出新的产品审美${RQ}`,
  `\u2022 中国消费品出海正在从拼低价向做品牌转型，进入更大规模、更细分、更复杂的集体出海周期`,
];
industryData.forEach(d => children.push(p(d)));

// ===== 八 =====
children.push(pb());
children.push(h1('八、竞争优势总结'));

children.push(h2('8.1 与山海图的差异化对比'));
children.push(makeTable(
  ['维度', '山海图', '新丝路跨境'],
  [
    ['获客模式', '线下活动积累（5-10年）', 'IP存量信任前置 + 内容矩阵，1-2年见效'],
    ['核心优势', '重资产本地化团队（8国14城、400+人）', '轻资产合作网络 + 20年海外人脉 + 国内产业带深度理解'],
    ['内容策略', '以行业活动/报告为主', '全域内容矩阵 + AI内容生产 + IP故事线'],
    ['客户转化路径', '线下活动\u2192口碑\u2192重复获客', '99元门票\u21923天实战\u2192平台服务\u2192终生客户'],
    ['交付重心', '以本地化落地服务为核心', '以实战培训和持续陪跑为入口，服务为生态'],
    ['服务广度', '聚焦东南亚', '覆盖全球重点市场（欧美、东南亚、中东等）'],
  ],
  [1400, 3500, 4126]
));
children.push(emptyLine());

children.push(h2('8.2 新丝路跨境的核心竞争力（不可复制之处）'));
children.push(p([
  { text: '1. 雨哥IP + 20年实战经验', bold: true },
  { text: '：几十万粉丝的认知壁垒 + 20年外贸全链路经验，形成出海知识领域的信任护城河' },
]));
children.push(p([
  { text: `2. 99元\u2192线下课\u2192平台的平滑转化阶梯`, bold: true },
  { text: `：产品线设计科学，用户自然向上流动，从根本上杜绝${LQ}割韭菜${RQ}印象` },
]));
children.push(p([
  { text: `3. ${LQ}交付即品牌${RQ}的价值主张`, bold: true },
  { text: '：不是卖完课走人，而是用3天线下课 + 30天陪跑 + 长期服务，让学员真正拿到结果' },
]));
children.push(p([
  { text: '4. 主题化内容运营', bold: true },
  { text: '：每期不同主题，精准吸引细分行业企业主，形成主题圈层效应' },
]));
children.push(p([
  { text: '5. 结果导向的交付闭环', bold: true },
  { text: `：从${LQ}知识${RQ}到${LQ}方案${RQ}到${LQ}执行${RQ}到${LQ}增长${RQ}\u2014\u2014不仅仅是认知升级，更是可复制的执行SOP` },
]));

// ===== 九 =====
children.push(pb());
children.push(h1('九、风险与应对'));
children.push(makeTable(
  ['风险', '描述', '应对策略'],
  [
    ['线下课交付能力', '学员实战实操需要大量助教支持，交付门槛高', '建立助教培训体系，每期1:5师生比；提前录制标准SOP'],
    ['IP信任透支', '99元课\u2192线下课转化链条断裂', `在99元课即开始${LQ}结果驱动${RQ}，确保每期结营有真实成果展示`],
    ['平台服务落地', '海外服务交付能力跟不上销售速度', '前期合作模式 + 核心服务自营，控制接单节奏'],
    ['同质化竞争', '市场上出现类似模式', '壁垒在于雨哥IP+20年经验的差异化，持续强化内容输出'],
    ['主题热度波动', '某些主题可能报名人数不足', '提前调研行业热点，灵活调整主题排期；每期保证基础人数后再开放报名'],
    ['跨境合规', '涉及海外法律税务风险', '只与持牌机构合作，购买合规保险，客户告知书明确责任边界'],
  ],
  [1400, 3000, 4626]
));

// ===== 十 =====
children.push(pb());
children.push(h1('十、核心亮点总结'));
children.push(p([
  { text: '1. IP驱动', bold: true },
  { text: '：几十万粉丝是天然的流量蓄水池，99元门票课是低成本获客的利器' },
]));
children.push(p([
  { text: '2. 交付为王', bold: true },
  { text: `：每堂课必须${LQ}现场干出来${RQ}，结课后30天陪跑 + 每周直播诊断，确保学员真正拿到结果` },
]));
children.push(p([
  { text: '3. 主题化运营', bold: true },
  { text: '：每期聚焦一个行业/一个话题，精准吸引对应领域的企业主' },
]));
children.push(p([
  { text: '4. 山海图差异化', bold: true },
  { text: '：不拼重资产本地化，拼的是IP信任 + 国内产业带深耕 + 20年海外资源网络' },
]));
children.push(p([
  { text: '5. 可持续生态', bold: true },
  { text: '：99元\u2192线下课\u2192平台服务\u2192终生客户，每一层都是下一层的蓄水池，形成飞轮效应' },
]));
children.push(emptyLine());
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 200 },
  children: [new TextRun({ text: `新丝路跨境${LQ}实战${RQ}出海\u2014\u2014让每一次出海都有人陪跑到底。`, font: FONT, size: 28, bold: true, color: '1F4E79' })],
}));

// ========== Build ==========
const doc = new Document({
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 36, bold: true, font: FONT, color: '1F4E79' },
        paragraph: { spacing: { before: 300, after: 120 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 30, bold: true, font: FONT, color: '2E75B6' },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 26, bold: true, font: FONT, color: '2E75B6' },
        paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 2 } },
    ],
  },
  numbering: {
    config: [
      { reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '\u2022', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: A4_W, height: A4_H },
        margin: M,
      },
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: '新丝路跨境\u00B7实战出海 | 商业模式方案书', font: FONT, size: 18, color: '999999' })],
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: '- ', font: FONT, size: 18, color: '999999' }),
            new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18, color: '999999' }),
            new TextRun({ text: ' -', font: FONT, size: 18, color: '999999' }),
          ],
        })],
      }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then(buffer => {
  const outPath = 'C:\\Users\\ASDCF\\.qclaw\\workspace\\新丝路跨境_实战出海_商业模式方案书.docx';
  fs.writeFileSync(outPath, buffer);
  console.log('DONE: ' + outPath);
}).catch(err => console.error('FAILED:', err));
