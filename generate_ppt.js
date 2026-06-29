const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const { 
  FaUserTie, FaStore, FaGlobe, FaShieldAlt, FaMoneyCheckAlt, 
  FaFileInvoiceDollar, FaUserPlus, FaFish, FaBalanceScale, FaListOl,
  FaLightbulb, FaHandshake, FaIdCard, FaCoins, FaShip, FaFileContract,
  FaExclamationTriangle, FaCheckCircle, FaRocket, FaClipboardList
} = require("react-icons/fa");

const ICON_SIZE = 256;

function renderIconSvg(IconComponent, color = "#FFFFFF", size = ICON_SIZE) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}

async function iconToBase64Png(IconComponent, color, size = ICON_SIZE) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}

// Color palette: Ocean Gradient
const C = {
  navy:    "065A82",
  teal:    "1C7293",
  mid:     "21295C",
  accent:  "02C39A",
  light:   "CADCFC",
  white:   "FFFFFF",
  offwhite:"F5F7FA",
  text:    "1E293B",
  subtext: "64748B",
  warn:    "F96167",
};

async function main() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.title = "外贸全链条培训记录";
  pres.author = "培训部";

  // Pre-render icons
  const icons = {
    userTie:    await iconToBase64Png(FaUserTie, C.white, 256),
    store:      await iconToBase64Png(FaStore, C.white, 256),
    globe:      await iconToBase64Png(FaGlobe, C.white, 256),
    shield:     await iconToBase64Png(FaShieldAlt, C.white, 256),
    money:      await iconToBase64Png(FaMoneyCheckAlt, C.white, 256),
    invoice:    await iconToBase64Png(FaFileInvoiceDollar, C.white, 256),
    userPlus:   await iconToBase64Png(FaUserPlus, C.white, 256),
    fish:       await iconToBase64Png(FaFish, C.white, 256),
    balance:    await iconToBase64Png(FaBalanceScale, C.white, 256),
    listOl:     await iconToBase64Png(FaListOl, C.white, 256),
    lightbulb:  await iconToBase64Png(FaLightbulb, C.white, 256),
    handshake:  await iconToBase64Png(FaHandshake, C.white, 256),
    idCard:     await iconToBase64Png(FaIdCard, C.white, 256),
    coins:      await iconToBase64Png(FaCoins, C.white, 256),
    ship:       await iconToBase64Png(FaShip, C.white, 256),
    fileContract:await iconToBase64Png(FaFileContract, C.white, 256),
    exclam:     await iconToBase64Png(FaExclamationTriangle, C.warn, 256),
    check:      await iconToBase64Png(FaCheckCircle, C.accent, 256),
    rocket:     await iconToBase64Png(FaRocket, C.white, 256),
    clipboard:  await iconToBase64Png(FaClipboardList, C.white, 256),
  };

  // Helper: add slide number
  function addSlideNumber(slide, num) {
    slide.addText(String(num), {
      x: 9.2, y: 5.2, w: 0.6, h: 0.3,
      fontSize: 10, color: C.subtext, align: "right", margin: 0,
    });
  }

  // Helper: section divider slide
  function addSectionSlide(pres, title, subtitle, iconData) {
    const slide = pres.addSlide();
    slide.background = { color: C.navy };
    // Left accent bar
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 0.12, h: 5.625,
      fill: { color: C.accent }, line: { color: C.accent },
    });
    // Icon circle
    slide.addShape(pres.shapes.OVAL, {
      x: 0.5, y: 1.8, w: 1.2, h: 1.2,
      fill: { color: C.teal }, line: { color: C.teal },
    });
    slide.addImage({ data: iconData, x: 0.65, y: 1.95, w: 0.9, h: 0.9 });
    // Title
    slide.addText(title, {
      x: 2.0, y: 1.5, w: 7.5, h: 1.0,
      fontSize: 32, bold: true, color: C.white,
      fontFace: "Microsoft YaHei", margin: 0,
    });
    slide.addText(subtitle || "", {
      x: 2.0, y: 2.7, w: 7.5, h: 0.6,
      fontSize: 16, color: C.light,
      fontFace: "Microsoft YaHei", margin: 0,
    });
    // Bottom bar
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 5.3, w: 10, h: 0.325,
      fill: { color: C.mid }, line: { color: C.mid },
    });
    return slide;
  }

  // Helper: content slide with left accent
  function addContentSlide(pres, title, slideNum) {
    const slide = pres.addSlide();
    slide.background = { color: C.offwhite };
    // Left accent
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 0.08, h: 5.625,
      fill: { color: C.teal }, line: { color: C.teal },
    });
    // Header bar
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.85,
      fill: { color: C.navy }, line: { color: C.navy },
    });
    slide.addText(title, {
      x: 0.3, y: 0.15, w: 9.5, h: 0.55,
      fontSize: 22, bold: true, color: C.white,
      fontFace: "Microsoft YaHei", margin: 0,
    });
    addSlideNumber(slide, slideNum);
    return slide;
  }

  // Helper: add bullet card (rounded rect with icon)
  function addBulletCard(slide, x, y, w, h, iconData, title, bullets, fillColor) {
    const fc = fillColor || C.white;
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y, w, h,
      fill: { color: fc },
      line: { color: "E2E8F0", width: 1 },
      shadow: { type: "outer", color: "000000", blur: 8, offset: 2, angle: 135, opacity: 0.08 },
    });
    // Icon circle
    slide.addShape(pres.shapes.OVAL, {
      x: x + 0.15, y: y + 0.15, w: 0.45, h: 0.45,
      fill: { color: C.teal }, line: { color: C.teal },
    });
    slide.addImage({ data: iconData, x: x + 0.22, y: y + 0.2, w: 0.3, h: 0.3 });
    // Title
    slide.addText(title, {
      x: x + 0.7, y: y + 0.15, w: w - 0.85, h: 0.35,
      fontSize: 13, bold: true, color: C.text,
      fontFace: "Microsoft YaHei", margin: 0,
    });
    // Bullets
    const bulletText = bullets.map((b, i) => ({
      text: b,
      options: { bullet: true, breakLine: i < bullets.length - 1, fontSize: 11, color: C.text, fontFace: "Microsoft YaHei" }
    }));
    slide.addText(bulletText, {
      x: x + 0.15, y: y + 0.6, w: w - 0.3, h: h - 0.7,
      fontSize: 11, color: C.text, fontFace: "Microsoft YaHei", margin: 0,
    });
  }

  // ─────────────────────────────────────────────
  // SLIDE 1: Title Slide
  // ─────────────────────────────────────────────
  {
    const slide = pres.addSlide();
    slide.background = { color: C.navy };
    // Accent bar right
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 9.88, y: 0, w: 0.12, h: 5.625,
      fill: { color: C.accent }, line: { color: C.accent },
    });
    // Decorative circle
    slide.addShape(pres.shapes.OVAL, {
      x: 7.5, y: -1.5, w: 4, h: 4,
      fill: { color: C.teal, transparency: 70 },
      line: { color: C.teal, transparency: 70 },
    });
    // Icons row
    slide.addImage({ data: icons.globe, x: 0.8, y: 0.7, w: 0.7, h: 0.7 });
    slide.addImage({ data: icons.balance, x: 1.7, y: 0.7, w: 0.7, h: 0.7 });
    slide.addImage({ data: icons.coins, x: 2.6, y: 0.7, w: 0.7, h: 0.7 });
    // Title
    slide.addText("外贸全链条培训记录", {
      x: 0.5, y: 1.6, w: 9, h: 1.0,
      fontSize: 38, bold: true, color: C.white,
      fontFace: "Microsoft YaHei", margin: 0,
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y: 2.7, w: 3.5, h: 0.06,
      fill: { color: C.accent }, line: { color: C.accent },
    });
    slide.addText("身份选择 · 外汇管理 · 海关报关 · 税务合规 · 品牌运营", {
      x: 0.5, y: 2.85, w: 9, h: 0.5,
      fontSize: 14, color: C.light,
      fontFace: "Microsoft YaHei", margin: 0,
    });
    // Info bar
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 4.9, w: 10, h: 0.725,
      fill: { color: C.mid }, line: { color: C.mid },
    });
    slide.addText("培训部门  |  2025年版  |  内部资料", {
      x: 0.5, y: 4.95, w: 9, h: 0.5,
      fontSize: 12, color: C.light,
      fontFace: "Microsoft YaHei", margin: 0,
    });
  }

  // ─────────────────────────────────────────────
  // SLIDE 2: 目录
  // ─────────────────────────────────────────────
  {
    const slide = pres.addSlide();
    slide.background = { color: C.offwhite };
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.85,
      fill: { color: C.navy }, line: { color: C.navy },
    });
    slide.addText("目录 / CONTENTS", {
      x: 0.3, y: 0.15, w: 9.5, h: 0.55,
      fontSize: 22, bold: true, color: C.white,
      fontFace: "Microsoft YaHei", margin: 0,
    });
    addSlideNumber(slide, 2);

    const items = [
      ["01", "外贸人才库与三大关键要素", C.teal],
      ["02", "做外贸的三种身份（上）：个人身份", C.teal],
      ["03", "做外贸的三种身份（下）：1039模式与公司", "1C7293"],
      ["04", "三部门监管框架", C.navy],
      ["05", "外汇管理与收结汇实务", "1C7293"],
      ["06", "海关报关全流程", C.navy],
      ["07", "税务合规与退税实务", C.teal],
      ["08", "品牌运营官：客户开发", "1C7293"],
      ["09", "人财物关系与思维转型", C.navy],
      ["10", "总结与30天行动清单", C.accent],
    ];

    items.forEach(([num, title, color], i) => {
      const x = i % 2 === 0 ? 0.4 : 5.2;
      const y = 1.1 + Math.floor(i / 2) * 0.95;
      const w = 4.4, h = 0.75;
      slide.addShape(pres.shapes.RECTANGLE, {
        x, y, w, h,
        fill: { color: C.white },
        line: { color: "E2E8F0", width: 1 },
        shadow: { type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.06 },
      });
      slide.addShape(pres.shapes.RECTANGLE, {
        x, y, w: 0.55, h,
        fill: { color }, line: { color },
      });
      slide.addText(num, {
        x, y, w: 0.55, h,
        fontSize: 16, bold: true, color: C.white, align: "center", valign: "middle",
        fontFace: "Arial Black", margin: 0,
      });
      slide.addText(title, {
        x: x + 0.65, y: y + 0.1, w: w - 0.75, h: h - 0.2,
        fontSize: 12, bold: true, color: C.text, valign: "middle",
        fontFace: "Microsoft YaHei", margin: 0,
      });
    });
  }

  // ─────────────────────────────────────────────
  // CHAPTER 1: 培训导论
  // ─────────────────────────────────────────────
  addSectionSlide(pres, "第1章", "外贸人才库与三大关键要素", icons.lightbulb);

  // Slide: 外贸人才库的战略地位
  {
    const slide = addContentSlide(pres, "第1章  外贸人才库的战略地位", 4);
    addBulletCard(slide, 0.3, 1.1, 4.3, 2.0, icons.exclam,
      "三大风险", [
        "财务流失：人才储备不足导致业务断层",
        "客户丢失：关键人员离职带走客户资源",
        "产品断供：供应链人才缺失影响交付",
      ], C.white);
    addBulletCard(slide, 5.2, 1.1, 4.3, 2.0, icons.check,
      "建设目标", [
        "建立系统化人才筛选机制",
        "从「懂一点」到「全链条可控」",
        "定期评估人才库健康度",
      ], C.white);
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.3, y: 3.3, w: 9.2, h: 1.8,
      fill: { color: "E8F4F8" },
      line: { color: C.teal, width: 1 },
    });
    slide.addText("💡  行动建议", {
      x: 0.5, y: 3.4, w: 9, h: 0.35,
      fontSize: 13, bold: true, color: C.teal, fontFace: "Microsoft YaHei", margin: 0,
    });
    slide.addText([
      { text: "对照自身业务，识别薄弱环节并制定改进计划", options: { bullet: true, breakLine: true } },
      { text: "每季度评估一次人才库，确保关键岗位有备份人选", options: { bullet: true } },
    ], {
      x: 0.5, y: 3.85, w: 8.8, h: 1.1,
      fontSize: 12, color: C.text, fontFace: "Microsoft YaHei", margin: 0,
    });
  }

  // ─────────────────────────────────────────────
  // CHAPTER 2: 个人身份
  // ─────────────────────────────────────────────
  addSectionSlide(pres, "第2章", "做外贸的三种身份（上）：个人身份", icons.userTie);

  {
    const slide = addContentSlide(pres, "第2章  个人身份：利弊与定位", 6);
    addBulletCard(slide, 0.3, 1.1, 4.5, 1.9, icons.userTie,
      "个人身份特征", [
        "不能直接收外汇，无独立采购主体",
        "无退税资质，收入依赖提成",
        "本质角色：业务中间人",
      ], C.white);
    addBulletCard(slide, 5.0, 1.1, 4.5, 1.9, icons.exclam,
      "核心风险", [
        "客户关系不受控 → 客户流失",
        "货源不受控 → 供应链断裂",
        "资金不受控 → 提成被克扣",
      ], C.white);
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.3, y: 3.2, w: 9.2, h: 1.9,
      fill: { color: "FFF4E6" },
      line: { color: "F59E0B", width: 1 },
    });
    slide.addText("⚠  适用场景与建议", {
      x: 0.5, y: 3.35, w: 9, h: 0.35,
      fontSize: 13, bold: true, color: "B45309", fontFace: "Microsoft YaHei", margin: 0,
    });
    slide.addText([
      { text: "适用：刚入行试水、学习行业经验阶段", options: { bullet: true, breakLine: true } },
      { text: "建议：尽快升级到个体户或公司身份，掌握主动权", options: { bullet: true, breakLine: true } },
      { text: "警惕：「黑心老板」克扣提成，客户被老板直接接管", options: { bullet: true } },
    ], {
      x: 0.5, y: 3.8, w: 8.8, h: 1.2,
      fontSize: 12, color: C.text, fontFace: "Microsoft YaHei", margin: 0,
    });
  }

  // ─────────────────────────────────────────────
  // CHAPTER 3: 1039模式 + 公司身份
  // ─────────────────────────────────────────────
  addSectionSlide(pres, "第3章", "做外贸的三种身份（下）：1039模式与公司", icons.store);

  // 1039模式
  {
    const slide = addContentSlide(pres, "第3章  1039市场采购贸易模式（义乌模式）", 8);
    addBulletCard(slide, 0.3, 1.1, 4.5, 2.0, icons.store,
      "核心特征", [
        "限定主体、限定区域、限定收款银行",
        "单票不超过15万美金",
        "无需退税，即买即走",
      ], C.white);
    addBulletCard(slide, 5.0, 1.1, 4.5, 2.0, icons.check,
      "优势与适用", [
        "不承担报关义务，多种灵活收款方式",
        "适用区域：义乌、白沟箱包、临沂等产业带",
        "适合：超能卷的产业带、农村作坊式生产",
      ], C.white);
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.3, y: 3.3, w: 9.2, h: 1.7,
      fill: { color: "E8F4F8" },
      line: { color: C.teal, width: 1 },
    });
    slide.addText("📦  代表性区域", {
      x: 0.5, y: 3.45, w: 9, h: 0.35,
      fontSize: 13, bold: true, color: C.teal, fontFace: "Microsoft YaHei", margin: 0,
    });
    slide.addText("义乌商贸城  ·  河北白沟箱包市场  ·  山东临沂产业带  ·  新疆阿拉山口/霍尔果斯边民互市", {
      x: 0.5, y: 3.9, w: 8.8, h: 0.9,
      fontSize: 13, color: C.text, fontFace: "Microsoft YaHei", margin: 0,
    });
  }

  // 公司身份
  {
    const slide = addContentSlide(pres, "第3章  公司身份：正规军路线", 9);
    addBulletCard(slide, 0.3, 1.1, 4.5, 2.1, icons.idCard,
      "公司身份要求", [
        "必须具备外贸资质并完成备案",
        "通过SWIFT系统收汇，拥有对公账户",
        "可享受出口退税（最高13%）",
      ], C.white);
    addBulletCard(slide, 5.0, 1.1, 4.5, 2.1, icons.coins,
      "核心优势", [
        "人财物全可控，客户关系稳固",
        "13%退税 = 纯利润（很多国内生意都没有）",
        "可规模化，适合长期发展",
      ], C.white);
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.3, y: 3.4, w: 9.2, h: 1.6,
      fill: { color: "ECFDF5" },
      line: { color: C.accent, width: 1 },
    });
    slide.addText("💰  退税价值计算", {
      x: 0.5, y: 3.55, w: 9, h: 0.35,
      fontSize: 13, bold: true, color: "065F46", fontFace: "Microsoft YaHei", margin: 0,
    });
    slide.addText("年出口额1000万 → 退税可达130万  |  这是正规外贸企业的重要利润来源", {
      x: 0.5, y: 4.0, w: 8.8, h: 0.8,
      fontSize: 13, bold: true, color: "065F46", fontFace: "Microsoft YaHei", margin: 0,
    });
  }

  // ─────────────────────────────────────────────
  // CHAPTER 4: 三部门监管框架
  // ─────────────────────────────────────────────
  addSectionSlide(pres, "第4章", "三部门监管框架", icons.shield);

  {
    const slide = addContentSlide(pres, "第4章  外贸监管体系全景图", 11);
    // Three department cards
    const depts = [
      { icon: icons.money, title: "外汇管理局", subtitle: "管钱", color: C.teal,
        points: ["SWIFT收汇审核", "结汇合规管理", "冻卡风险控制"] },
      { icon: icons.ship, title: "海关", subtitle: "管货", color: C.navy,
        points: ["报关单审核", "查验（抽检/必检）", "放行与边检"] },
      { icon: icons.fileContract, title: "税务/公安", subtitle: "管账与合规", color: C.mid,
        points: ["退税资质审核", "账务合规检查", "非法经营的打击"] },
    ];
    depts.forEach((d, i) => {
      const x = 0.3 + i * 3.25;
      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: 1.1, w: 3.0, h: 2.5,
        fill: { color: C.white },
        line: { color: "E2E8F0", width: 1 },
        shadow: { type: "outer", color: "000000", blur: 8, offset: 2, angle: 135, opacity: 0.08 },
      });
      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: 1.1, w: 3.0, h: 0.55,
        fill: { color: d.color }, line: { color: d.color },
      });
      slide.addImage({ data: d.icon, x: x + 0.1, y: 1.2, w: 0.35, h: 0.35 });
      slide.addText(d.title, {
        x: x + 0.55, y: 1.15, w: 2.3, h: 0.45,
        fontSize: 12, bold: true, color: C.white, fontFace: "Microsoft YaHei", margin: 0,
      });
      slide.addText(d.subtitle, {
        x: x + 0.55, y: 1.5, w: 2.3, h: 0.3,
        fontSize: 11, color: C.light, fontFace: "Microsoft YaHei", margin: 0,
      });
      const pt = d.points.map((p, j) => ({
        text: p,
        options: { bullet: true, breakLine: j < d.points.length - 1, fontSize: 11, color: C.text, fontFace: "Microsoft YaHei" }
      }));
      slide.addText(pt, {
        x: x + 0.15, y: 1.8, w: 2.8, h: 1.6,
        fontSize: 11, color: C.text, fontFace: "Microsoft YaHei", margin: 0,
      });
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.3, y: 3.8, w: 9.2, h: 1.4,
      fill: { color: "FEE2E2" },
      line: { color: C.warn, width: 1 },
    });
    slide.addImage({ data: icons.exclam, x: 0.45, y: 3.95, w: 0.4, h: 0.4 });
    slide.addText("监管红线", {
      x: 0.95, y: 3.9, w: 8.5, h: 0.35,
      fontSize: 13, bold: true, color: C.warn, fontFace: "Microsoft YaHei", margin: 0,
    });
    slide.addText([
      { text: "公安介入场景：洗钱、非法经营、冻卡", options: { bullet: true, breakLine: true } },
      { text: "冻卡高发原因：地下钱庄、买单出口——碰都不要碰", options: { bullet: true } },
    ], {
      x: 0.95, y: 4.35, w: 8.5, h: 0.75,
      fontSize: 12, color: C.text, fontFace: "Microsoft YaHei", margin: 0,
    });
  }

  // ─────────────────────────────────────────────
  // CHAPTER 5: 外汇管理
  // ─────────────────────────────────────────────
  addSectionSlide(pres, "第5章", "外汇管理与收结汇实务", icons.money);

  // SWIFT系统
  {
    const slide = addContentSlide(pres, "第5章  SWIFT国际结算系统", 13);
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.3, y: 1.1, w: 9.2, h: 1.4,
      fill: { color: "E8F4F8" },
      line: { color: C.teal, width: 1 },
    });
    slide.addText("SWIFT 流程：客户TT电汇  →  水单/报文  →  外汇管理局审核  →  结汇至国内账户", {
      x: 0.5, y: 1.25, w: 8.8, h: 0.5,
      fontSize: 13, bold: true, color: C.teal, fontFace: "Microsoft YaHei", margin: 0,
    });
    slide.addText("以美元为锚定货币，全球银行间标准化通信网络。每一笔外汇流入都有迹可循，合规记录至关重要。", {
      x: 0.5, y: 1.85, w: 8.8, h: 0.55,
      fontSize: 12, color: C.text, fontFace: "Microsoft YaHei", margin: 0,
    });
    // Bank comparison
    const banks = [
      { name: "招商银行", rating: "⭐⭐⭐⭐⭐ 最佳", color: C.accent, desc: "服务态度最好，效率最高，强烈推荐" },
      { name: "中信银行", rating: "⭐⭐⭐⭐ 优秀", color: "1C7293", desc: "服务良好，效率较高" },
      { name: "工商银行", rating: "⭐⭐⭐ 良好", color: C.teal, desc: "服务不错，效率中等" },
      { name: "中国银行", rating: "⭐⭐⭐ 良好", color: C.navy, desc: "传统外贸银行，经验丰富" },
      { name: "农业银行", rating: "⭐ 较差", color: C.warn, desc: "效率偏低，流程慢，需预留更多时间" },
    ];
    slide.addText("银行选择建议", {
      x: 0.3, y: 2.65, w: 9, h: 0.35,
      fontSize: 14, bold: true, color: C.text, fontFace: "Microsoft YaHei", margin: 0,
    });
    banks.forEach((b, i) => {
      const y = 3.1 + i * 0.38;
      slide.addShape(pres.shapes.RECTANGLE, {
        x: 0.3, y, w: 9.2, h: 0.34,
        fill: { color: i % 2 === 0 ? C.offwhite : C.white },
        line: { color: "E2E8F0", width: 0.5 },
      });
      slide.addShape(pres.shapes.RECTANGLE, {
        x: 0.3, y, w: 0.08, h: 0.34,
        fill: { color: b.color }, line: { color: b.color },
      });
      slide.addText(b.name, { x: 0.5, y: y + 0.02, w: 2.0, h: 0.3, fontSize: 12, bold: true, color: C.text, fontFace: "Microsoft YaHei", margin: 0 });
      slide.addText(b.rating, { x: 2.6, y: y + 0.02, w: 3.0, h: 0.3, fontSize: 11, color: b.color, fontFace: "Microsoft YaHei", margin: 0 });
      slide.addText(b.desc, { x: 5.7, y: y + 0.02, w: 3.8, h: 0.3, fontSize: 11, color: C.subtext, fontFace: "Microsoft YaHei", margin: 0 });
    });
  }

  // ─────────────────────────────────────────────
  // CHAPTER 6: 海关报关
  // ─────────────────────────────────────────────
  addSectionSlide(pres, "第6章", "海关报关全流程", icons.ship);

  {
    const slide = addContentSlide(pres, "第6章  海关报关全流程", 15);
    // Process flow
    const steps = [
      { n: "01", title: "如实申报", desc: "品名、规格、单价、总价、HS编码\n报关单信息必须真实准确" },
      { n: "02", title: "海关查验", desc: "随机抽查 + 必检品类\n（医药、食品等）" },
      { n: "03", title: "三流合一核对", desc: "货物流、资金流、单证流\n三者必须一致" },
      { n: "04", title: "放行 + 边检", desc: "放行单 + 边检查违禁品\n（毒品、走私物品）" },
      { n: "05", title: "目的国报关", desc: "产品认证、原产地签证\n符合目的国进口合规要求" },
    ];
    steps.forEach((s, i) => {
      const x = 0.3 + (i % 3) * 3.15;
      const y = i < 3 ? 1.1 : 3.15;
      const w = i < 3 ? 3.0 : 4.5;
      const thisX = i >= 3 ? 0.3 + (i - 3) * 4.7 : x;
      const thisW = i >= 3 ? 4.5 : w;
      const thisY = i >= 3 ? 3.15 : y;
      slide.addShape(pres.shapes.RECTANGLE, {
        x: thisX, y: thisY, w: thisW, h: 1.4,
        fill: { color: C.white },
        line: { color: "E2E8F0", width: 1 },
        shadow: { type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.06 },
      });
      slide.addShape(pres.shapes.OVAL, {
        x: thisX + 0.15, y: thisY + 0.15, w: 0.5, h: 0.5,
        fill: { color: C.teal }, line: { color: C.teal },
      });
      slide.addText(s.n, {
        x: thisX + 0.15, y: thisY + 0.15, w: 0.5, h: 0.5,
        fontSize: 14, bold: true, color: C.white, align: "center", valign: "middle",
        fontFace: "Arial Black", margin: 0,
      });
      slide.addText(s.title, {
        x: thisX + 0.75, y: thisY + 0.15, w: thisW - 0.9, h: 0.4,
        fontSize: 13, bold: true, color: C.text, fontFace: "Microsoft YaHei", margin: 0,
      });
      slide.addText(s.desc, {
        x: thisX + 0.15, y: thisY + 0.65, w: thisW - 0.3, h: 0.7,
        fontSize: 11, color: C.subtext, fontFace: "Microsoft YaHei", margin: 0,
      });
    });
  }

  // ─────────────────────────────────────────────
  // CHAPTER 7: 税务合规
  // ─────────────────────────────────────────────
  addSectionSlide(pres, "第7章", "税务合规与退税实务", icons.invoice);

  // 退税机制
  {
    const slide = addContentSlide(pres, "第7章  出口退税机制与合规红线", 17);
    addBulletCard(slide, 0.3, 1.1, 4.5, 2.0, icons.coins,
      "退税核心要点", [
        "出口退税最高可达13%，是重要利润来源",
        "前提：账务合规，发票、报关单、收汇凭证三者匹配",
        "「平汇、平账」原则：外汇金额与报关金额必须一致",
      ], C.white);
    addBulletCard(slide, 5.0, 1.1, 4.5, 2.0, icons.exclam,
      "常见陷阱（严禁！）", [
        "买单出口：短期省钱，实为冻卡和处罚埋雷",
        "地下钱庄结汇：直接触发公安打击",
        "涉黑资金出海：风险极大，坚决不碰",
      ], C.white);
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.3, y: 3.3, w: 9.2, h: 1.7,
      fill: { color: "ECFDF5" },
      line: { color: C.accent, width: 1 },
    });
    slide.addText("✅  行动建议", {
      x: 0.5, y: 3.45, w: 9, h: 0.35,
      fontSize: 13, bold: true, color: "065F46", fontFace: "Microsoft YaHei", margin: 0,
    });
    slide.addText([
      { text: "宁可合规成本高一些，也不要在税务和资金通道上走捷径", options: { bullet: true, breakLine: true } },
      { text: "定期自查三个维度（外汇/海关/税务）的合规状态", options: { bullet: true, breakLine: true } },
      { text: "建立风控清单，确保所有交易留痕可查", options: { bullet: true } },
    ], {
      x: 0.5, y: 3.9, w: 8.8, h: 1.0,
      fontSize: 12, color: C.text, fontFace: "Microsoft YaHei", margin: 0,
    });
  }

  // ─────────────────────────────────────────────
  // CHAPTER 8: 品牌运营官
  // ─────────────────────────────────────────────
  addSectionSlide(pres, "第8章", "品牌运营官：客户开发方法论", icons.handshake);

  // 列名单
  {
    const slide = addContentSlide(pres, "第8章  列名单：锁定精准目标客户", 19);
    addBulletCard(slide, 0.3, 1.1, 4.5, 2.0, icons.listOl,
      "核心动作", [
        "梳理并锁定20个目标客户",
        "客户画像：有需求、有预算、可触达、有决策权",
        "名单质量决定后续转化效率",
      ], C.white);
    addBulletCard(slide, 5.0, 1.1, 4.5, 2.0, icons.lightbulb,
      "客户筛选标准", [
        "是否适合做品牌运营官？",
        "是否做供应链/中医出海/外贸相关业务？",
        "是否有团队资源或商会资源？",
      ], C.white);
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.3, y: 3.3, w: 9.2, h: 1.7,
      fill: { color: "E8F4F8" },
      line: { color: C.teal, width: 1 },
    });
    slide.addText("📋  行动建议", {
      x: 0.5, y: 3.45, w: 9, h: 0.35,
      fontSize: 13, bold: true, color: C.teal, fontFace: "Microsoft YaHei", margin: 0,
    });
    slide.addText([
      { text: "每周更新名单，持续做分层和优先级排序", options: { bullet: true, breakLine: true } },
      { text: "通过中医出海、品牌运营官岗位认知来筛选目标", options: { bullet: true } },
    ], {
      x: 0.5, y: 3.9, w: 8.8, h: 0.9,
      fontSize: 12, color: C.text, fontFace: "Microsoft YaHei", margin: 0,
    });
  }

  // 扔钩子
  {
    const slide = addContentSlide(pres, "第8章  扔钩子：激发客户好奇心", 20);
    addBulletCard(slide, 0.3, 1.1, 4.5, 2.2, icons.fish,
      "钩子设计原则", [
        "制造信息差，引发客户主动询问",
        "不卖产品，卖「价值预期」和「合作想象」",
        "好钩子：案例故事、行业数据、政策红利",
      ], C.white);
    addBulletCard(slide, 5.0, 1.1, 4.5, 2.2, icons.handshake,
      "执行要点", [
        "为每个客户定制差异化沟通切入点",
        "先建立信任，再谈合作",
        "让客户主动问「怎么参与？」",
      ], C.white);
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.3, y: 3.5, w: 9.2, h: 1.5,
      fill: { color: "FFF4E6" },
      line: { color: "F59E0B", width: 1 },
    });
    slide.addText("🎣  钩子示例（中医出海场景）", {
      x: 0.5, y: 3.65, w: 9, h: 0.35,
      fontSize: 13, bold: true, color: "B45309", fontFace: "Microsoft YaHei", margin: 0,
    });
    slide.addText("「我们已经帮XX省的中医馆在东南亚落地了3家，单月营收破50万，您有兴趣了解具体模式吗？」", {
      x: 0.5, y: 4.1, w: 8.8, h: 0.75,
      fontSize: 12, italic: true, color: C.text, fontFace: "Microsoft YaHei", margin: 0,
    });
  }

  // ─────────────────────────────────────────────
  // CHAPTER 9: 人财物与思维转型
  // ─────────────────────────────────────────────
  addSectionSlide(pres, "第9章", "人财物关系与思维转型", icons.balance);

  {
    const slide = addContentSlide(pres, "第9章  身份决定人财物格局", 22);
    const items = [
      { icon: icons.userTie, letter: "人", desc: "你是谁？代表谁？\n决定了客户对你的信任基础" },
      { icon: icons.coins, letter: "财", desc: "钱走谁的账？\n决定了利润空间和合规要求" },
      { icon: icons.store, letter: "物", desc: "货从哪来？\n决定了供应链控制力和议价能力" },
    ];
    items.forEach((it, i) => {
      const x = 0.4 + i * 3.1;
      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: 1.1, w: 2.9, h: 2.6,
        fill: { color: C.white },
        line: { color: "E2E8F0", width: 1 },
        shadow: { type: "outer", color: "000000", blur: 8, offset: 2, angle: 135, opacity: 0.08 },
      });
      slide.addShape(pres.shapes.RECTANGLE, {
        x, y: 1.1, w: 2.9, h: 0.6,
        fill: { color: C.navy }, line: { color: C.navy },
      });
      slide.addText(it.letter, {
        x, y: 1.1, w: 2.9, h: 0.6,
        fontSize: 22, bold: true, color: C.white, align: "center", valign: "middle",
        fontFace: "Microsoft YaHei", margin: 0,
      });
      slide.addImage({ data: it.icon, x: x + 0.2, y: 1.85, w: 0.6, h: 0.6 });
      slide.addText(it.desc, {
        x: x + 0.15, y: 2.55, w: 2.7, h: 1.0,
        fontSize: 12, color: C.text, fontFace: "Microsoft YaHei", margin: 0,
      });
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.3, y: 3.85, w: 9.2, h: 1.3,
      fill: { color: "E8F4F8" },
      line: { color: C.teal, width: 1 },
    });
    slide.addText("内贸思维  vs  外贸思维", {
      x: 0.5, y: 4.0, w: 9, h: 0.35,
      fontSize: 13, bold: true, color: C.teal, fontFace: "Microsoft YaHei", margin: 0,
    });
    slide.addText("内贸：关系驱动，现货现款，灵活变通  →  外贸：合规驱动，信用证/TT结算，流程标准化  →  把「合规」视为竞争力，而非负担", {
      x: 0.5, y: 4.45, w: 8.8, h: 0.6,
      fontSize: 12, color: C.text, fontFace: "Microsoft YaHei", margin: 0,
    });
  }

  // ─────────────────────────────────────────────
  // CHAPTER 10: 总结与行动清单
  // ─────────────────────────────────────────────
  addSectionSlide(pres, "第10章", "总结与30天行动清单", icons.clipboard);

  // 核心要点回顾
  {
    const slide = addContentSlide(pres, "第10章  培训核心要点回顾", 24);
    const points = [
      "身份选择决定业务天花板：个人 < 1039个体户 < 公司（正规军）",
      "三部门监管（外汇/海关/税务）是外贸运营的硬骨架，缺一不可",
      "合规是底线，不是选择——冻卡、处罚的风险远大于合规成本",
      "品牌运营官的核心：列名单 + 扔钩子，系统化开发客户",
      "人财物关系清晰，才能在外贸业务中掌握主动权",
    ];
    points.forEach((p, i) => {
      const y = 1.1 + i * 0.72;
      slide.addShape(pres.shapes.RECTANGLE, {
        x: 0.3, y, w: 9.2, h: 0.62,
        fill: { color: i % 2 === 0 ? "E8F4F8" : C.white },
        line: { color: "E2E8F0", width: 0.5 },
      });
      slide.addImage({ data: icons.check, x: 0.45, y: y + 0.06, w: 0.35, h: 0.35 });
      slide.addText(p, {
        x: 0.9, y: y + 0.08, w: 8.4, h: 0.5,
        fontSize: 13, color: C.text, fontFace: "Microsoft YaHei", margin: 0,
      });
    });
  }

  // 30天行动清单
  {
    const slide = addContentSlide(pres, "第10章  30天行动清单", 25);
    const actions = [
      { icon: icons.idCard, text: "确认当前身份是否匹配业务规模，制定升级计划" },
      { icon: icons.money, text: "开立合规外汇账户（推荐：招商银行）" },
      { icon: icons.fileContract, text: "梳理报关单证模板，确保「三流合一」" },
      { icon: icons.listOl, text: "列出20个目标客户名单，设计差异化钩子" },
      { icon: icons.invoice, text: "完成税务自查，确认退税资质和流程通畅" },
      { icon: icons.balance, text: "建立「人财物」关系图谱，明确权责边界" },
    ];
    actions.forEach((a, i) => {
      const x = i < 3 ? 0.3 : 5.1;
      const y = 1.1 + (i % 3) * 1.3;
      slide.addShape(pres.shapes.RECTANGLE, {
        x, y, w: 4.6, h: 1.1,
        fill: { color: C.white },
        line: { color: "E2E8F0", width: 1 },
        shadow: { type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.06 },
      });
      slide.addShape(pres.shapes.OVAL, {
        x: x + 0.15, y: y + 0.3, w: 0.5, h: 0.5,
        fill: { color: C.teal }, line: { color: C.teal },
      });
      slide.addText(String(i + 1), {
        x: x + 0.15, y: y + 0.3, w: 0.5, h: 0.5,
        fontSize: 16, bold: true, color: C.white, align: "center", valign: "middle",
        fontFace: "Arial Black", margin: 0,
      });
      slide.addText(a.text, {
        x: x + 0.75, y: y + 0.15, w: 3.7, h: 0.85,
        fontSize: 12, color: C.text, fontFace: "Microsoft YaHei", margin: 0,
      });
    });
  }

  // ─────────────────────────────────────────────
  // 结束页
  // ─────────────────────────────────────────────
  {
    const slide = pres.addSlide();
    slide.background = { color: C.navy };
    slide.addShape(pres.shapes.OVAL, {
      x: 7.0, y: -1.0, w: 5, h: 5,
      fill: { color: C.teal, transparency: 75 },
      line: { color: C.teal, transparency: 75 },
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 0.12, h: 5.625,
      fill: { color: C.accent }, line: { color: C.accent },
    });
    slide.addImage({ data: icons.rocket, x: 4.0, y: 0.8, w: 2.0, h: 2.0 });
    slide.addText("谢谢聆听", {
      x: 1.0, y: 3.0, w: 8, h: 0.8,
      fontSize: 36, bold: true, color: C.white, align: "center",
      fontFace: "Microsoft YaHei", margin: 0,
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 2.5, y: 4.0, w: 5.0, h: 0.06,
      fill: { color: C.accent }, line: { color: C.accent },
    });
    slide.addText("合规为基  ·  客户为王  ·  执行致胜", {
      x: 1.0, y: 4.2, w: 8, h: 0.5,
      fontSize: 14, color: C.light, align: "center",
      fontFace: "Microsoft YaHei", margin: 0,
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 5.3, w: 10, h: 0.325,
      fill: { color: C.mid }, line: { color: C.mid },
    });
  }

  // Write file
  const outPath = "E:\\郑州录音\\外贸全链条培训记录.pptx";
  await pres.writeFile({ fileName: outPath });
  console.log("✅ PPT saved to: " + outPath);
}

main().catch(console.error);
