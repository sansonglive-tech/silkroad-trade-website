const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, VerticalAlign, PageNumber, PageBreak, LevelFormat,
  TableOfContents, ExternalHyperlink, ImageRun
} = require('C:\\Users\\ASDCF\\AppData\\Roaming\\npm\\node_modules\\docx');
const fs = require('fs');

// Color palette
const COLORS = {
  primary: "C0392B",
  secondary: "2C3E50",
  accent: "E74C3C",
  lightBg: "FDF2F2",
  headerBg: "C0392B",
  altRow: "F9F9F9",
  border: "CCCCCC",
  white: "FFFFFF",
  black: "000000",
  gray: "666666",
};

// All screenshots: 14cm wide x 8cm tall at 150 DPI = 827 x 472 px
// They were pre-processed to fit this size consistently
const screenshotDir = "C:\\Users\\ASDCF\\.qclaw\\media\\browser\\resized\\";

function loadImage(filename) {
  const path = screenshotDir + filename;
  if (fs.existsSync(path)) {
    return fs.readFileSync(path);
  }
  console.warn("Image not found:", path);
  return null;
}

// All final images are 827x472px (14cm x 8cm at 150 DPI)
const img_mainPage    = loadImage("final_main.png");
const img_onboarding  = loadImage("final_onboarding.png");
const img_loyalty     = loadImage("final_loyalty.png");
const img_proWB       = loadImage("final_proWB.png");
const img_helpCenter  = loadImage("final_help.png");
const img_fbs         = loadImage("final_fbs.png");

function makeBorder(color = COLORS.border) {
  const b = { style: BorderStyle.SINGLE, size: 1, color };
  return { top: b, bottom: b, left: b, right: b };
}

function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 200 },
    children: [new TextRun({ text, bold: true, font: "Arial", size: 36, color: COLORS.primary })]
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 160 },
    children: [new TextRun({ text, bold: true, font: "Arial", size: 28, color: COLORS.secondary })]
  });
}

function heading3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 120 },
    children: [new TextRun({ text, bold: true, font: "Arial", size: 24, color: COLORS.secondary })]
  });
}

function paragraph(text, opts = {}) {
  return new Paragraph({
    spacing: { before: 80, after: 120 },
    children: [new TextRun({ text, font: "Arial", size: 22, color: COLORS.black, ...opts })]
  });
}

function bullet(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text, font: "Arial", size: 22, color: COLORS.black })]
  });
}

function coloredBox(title, contentLines, fillColor = COLORS.lightBg) {
  const rows = [];
  if (title) {
    rows.push(new TableRow({
      children: [new TableCell({
        borders: makeBorder(COLORS.accent),
        shading: { fill: COLORS.accent, type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 160, right: 160 },
        children: [new Paragraph({
          children: [new TextRun({ text: title, bold: true, font: "Arial", size: 22, color: COLORS.white })]
        })]
      })]
    }));
  }
  const cellChildren = contentLines.map(line => new Paragraph({
    spacing: { before: 40, after: 40 },
    children: [new TextRun({ text: line, font: "Arial", size: 22, color: COLORS.black })]
  }));
  rows.push(new TableRow({
    children: [new TableCell({
      borders: makeBorder(COLORS.accent),
      shading: { fill: fillColor, type: ShadingType.CLEAR },
      margins: { top: 100, bottom: 100, left: 160, right: 160 },
      children: cellChildren
    })]
  }));
  return new Table({
    width: { size: 9026, type: WidthType.DXA },
    columnWidths: [9026],
    rows
  });
}

function spacer() { return new Paragraph({ spacing: { before: 80, after: 80 }, children: [new TextRun("")] }); }
function pageBreak() { return new Paragraph({ children: [new PageBreak()] }); }

function importantBox(text) {
  return new Table({
    width: { size: 9026, type: WidthType.DXA },
    columnWidths: [9026],
    rows: [
      new TableRow({
        children: [new TableCell({
          borders: makeBorder("E74C3C"),
          shading: { fill: "FEF9E7", type: ShadingType.CLEAR },
          margins: { top: 120, bottom: 120, left: 200, right: 200 },
          children: [new Paragraph({
            children: [
              new TextRun({ text: "⚠ 重要提醒：", bold: true, font: "Arial", size: 22, color: "C0392B" }),
              new TextRun({ text, font: "Arial", size: 22, color: COLORS.black })
            ]
          })]
        })]
      })
    ]
  });
}

// Image with caption — uses actual screenshot dimensions (914px wide, tall portrait)
// Page usable width: 11906 - 2*1440 = 9026 twips = 6.27 inches
// Display width: 5.5 inches = 7920 twips
// EMU conversion: 1 inch = 914400 EMU, 1 twip = 635 EMU
// All final images: 827x472px (14cm x 8cm at 150 DPI)
const IMG_W = 827;
const IMG_H = 472;

function screenshot(imageData, caption) {
  if (!imageData) {
    return [
      new Paragraph({ spacing: { before: 160, after: 80 }, children: [new TextRun({ text: `[截图：${caption}]`, font: "Arial", size: 20, color: COLORS.gray, italics: true })] }),
      new Paragraph({ spacing: { before: 80, after: 200 }, border: { top: { style: BorderStyle.DASHED, size: 1, color: COLORS.border } }, children: [new TextRun({ text: "（截图待补充）", font: "Arial", size: 18, color: COLORS.gray })] })
    ];
  }
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 80, after: 60 }, children: [new ImageRun({ data: imageData, transformation: { width: IMG_W, height: IMG_H }, type: "png" })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60, after: 200 }, children: [new TextRun({ text: `▼ 图：${caption}`, font: "Arial", size: 20, color: COLORS.gray, italics: true })] })
  ];
}

function twoColTable(leftTitle, leftContent, rightTitle, rightContent) {
  const makeCell = (title, content, isHeader) => new TableCell({
    borders: makeBorder(),
    shading: { fill: isHeader ? COLORS.headerBg : COLORS.white, type: ShadingType.CLEAR },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({ children: [new TextRun({ text: title, bold: true, font: "Arial", size: 22, color: isHeader ? COLORS.white : COLORS.primary })] })]
  });
  const makeContentCell = (items) => new TableCell({
    borders: makeBorder(),
    shading: { fill: COLORS.white, type: ShadingType.CLEAR },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: items.map(item => new Paragraph({
      spacing: { before: 40, after: 40 },
      children: [new TextRun({ text: item, font: "Arial", size: 22, color: COLORS.black })]
    }))
  });
  return new Table({
    width: { size: 9026, type: WidthType.DXA },
    columnWidths: [4513, 4513],
    rows: [
      new TableRow({ children: [makeCell(leftTitle, null, true), makeCell(rightTitle, null, true)] }),
      new TableRow({ children: [makeContentCell(leftContent), makeContentCell(rightContent)] })
    ]
  });
}

function tierTable() {
  const headers = ["等级", "近30天GMV目标（人民币）", "佣金优惠比例", "说明"];
  const rows_data = [
    ["1级", "≥ 50,000 元", "5%", "新卖家起点"],
    ["2级", "≥ 80,000 元", "10%", ""],
    ["3级", "≥ 200,000 元", "15%", ""],
    ["4级", "≥ 500,000 元", "20%", ""],
    ["5级", "≥ 1,000,000 元", "25%", ""],
    ["6级", "≥ 3,000,000 元", "30%", ""],
    ["7级", "≥ 6,000,000 元", "35%", ""],
    ["8级", "≥ 1.92亿元/年", "40%", "年度考核，等级跨年延续"],
  ];
  const headerRow = new TableRow({
    children: headers.map(h => new TableCell({
      borders: makeBorder(COLORS.primary),
      shading: { fill: COLORS.headerBg, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: h, bold: true, font: "Arial", size: 22, color: COLORS.white })] })]
    }))
  });
  const dataRows = rows_data.map((row, idx) => new TableRow({
    children: row.map((cell, col) => new TableCell({
      borders: makeBorder(),
      shading: { fill: idx % 2 === 0 ? COLORS.white : COLORS.altRow, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      children: [new Paragraph({
        alignment: col === 0 || col === 2 ? AlignmentType.CENTER : AlignmentType.LEFT,
        children: [new TextRun({ text: cell, font: "Arial", size: 22, color: COLORS.black, bold: col === 0 || col === 2 })]
      })]
    }))
  }));
  return new Table({
    width: { size: 9026, type: WidthType.DXA },
    columnWidths: [1504, 2314, 1929, 3279],
    rows: [headerRow, ...dataRows]
  });
}

function statsTable() {
  return new Table({
    width: { size: 9026, type: WidthType.DXA },
    columnWidths: [3009, 3009, 3008],
    rows: [
      new TableRow({
        children: [
          new TableCell({ borders: makeBorder(), shading: { fill: COLORS.primary, type: ShadingType.CLEAR }, margins: { top: 120, bottom: 120, left: 160, right: 160 }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "7900万+", bold: true, font: "Arial", size: 36, color: COLORS.white })] }), new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "每日活跃买家", font: "Arial", size: 20, color: COLORS.white })] })] }),
          new TableCell({ borders: makeBorder(), shading: { fill: COLORS.secondary, type: ShadingType.CLEAR }, margins: { top: 120, bottom: 120, left: 160, right: 160 }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "80+", bold: true, font: "Arial", size: 36, color: COLORS.white })] }), new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "中国分拣中心", font: "Arial", size: 20, color: COLORS.white })] })] }),
          new TableCell({ borders: makeBorder(), shading: { fill: COLORS.accent, type: ShadingType.CLEAR }, margins: { top: 120, bottom: 120, left: 160, right: 160 }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "9万+", bold: true, font: "Arial", size: 36, color: COLORS.white })] }), new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "俄罗斯提货点", font: "Arial", size: 20, color: COLORS.white })] })] }),
        ]
      })
    ]
  });
}

function onboardingTable() {
  const steps = [
    { step: "第一步", title: "了解平台计费并设置权限", items: ["了解佣金比例、物流费用、仓储费用", "添加用户并分配权限"] },
    { step: "第二步", title: "创建商品卡，设置价格和折扣", items: ["确保商品不在禁售清单中", "以人民币为单位设置价格", "设置折扣和促销活动"] },
    { step: "第三步", title: "创建仓库及上传库存", items: ["创建卖家仓库", "添加退货自提点", "上传商品库存（门户或API）"] },
    { step: "第四步", title: "查看订单发货指南", items: ["从中国仓库或俄罗斯海外仓发货", "120小时备货并交付至WB仓库", "莫斯科时间17:00后生成每周财务报告"] },
    { step: "第五步", title: "了解如何推广商品", items: ["参与促销活动（查看促销日历）", "使用WB推广工具（搜索活动、自动推广）", "获得欢迎奖金30,000积分"] },
  ];
  const headerRow = new TableRow({
    children: ["步骤", "操作内容", "关键要点"].map((h, idx) => new TableCell({
      borders: makeBorder(), shading: { fill: COLORS.headerBg, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: h, bold: true, font: "Arial", size: 22, color: COLORS.white })] })]
    }))
  });
  const dataRows = steps.map((s, idx) => new TableRow({
    children: [
      new TableCell({ borders: makeBorder(), shading: { fill: COLORS.primary, type: ShadingType.CLEAR }, margins: { top: 80, bottom: 80, left: 120, right: 120 }, verticalAlign: VerticalAlign.CENTER, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: s.step, bold: true, font: "Arial", size: 22, color: COLORS.white })] })] }),
      new TableCell({ borders: makeBorder(), shading: { fill: idx % 2 === 0 ? COLORS.lightBg : COLORS.white, type: ShadingType.CLEAR }, margins: { top: 80, bottom: 80, left: 120, right: 120 }, verticalAlign: VerticalAlign.CENTER, children: [new Paragraph({ children: [new TextRun({ text: s.title, bold: true, font: "Arial", size: 22, color: COLORS.secondary })] })] }),
      new TableCell({ borders: makeBorder(), shading: { fill: idx % 2 === 0 ? COLORS.lightBg : COLORS.white, type: ShadingType.CLEAR }, margins: { top: 80, bottom: 80, left: 120, right: 120 }, children: s.items.map(item => new Paragraph({ spacing: { before: 40, after: 40 }, children: [new TextRun({ text: "• " + item, font: "Arial", size: 22, color: COLORS.black })] })) }),
    ]
  }));
  return new Table({
    width: { size: 9026, type: WidthType.DXA },
    columnWidths: [1350, 2893, 4783],
    rows: [headerRow, ...dataRows]
  });
}

function jamToolsTable() {
  const tools = [
    { name: "置顶评论", desc: "置顶商品详情页中的评论，突出商品优势，提升买家信任" },
    { name: "图片标记", desc: "标记商品中相关的搭配商品，提升关联销售" },
    { name: "搜索查询报告", desc: "了解您的商品通过哪些搜索查询被找到和购买" },
    { name: "买家画像报告", desc: "展示目标受众画像：年龄、性别、地区、兴趣、平均客单价、活跃时段及购买频率" },
    { name: "视频自动播放", desc: "通过短视频展示商品优势，吸引买家注意" },
    { name: "虚拟试衣照相馆", desc: "节省拍摄成本，上传服装照片，WB人工智能模型即可将其\"穿\"在模特身上并添加背景" },
    { name: "60天免费试用", desc: "试用期内完成首单后续订可享30%折扣" },
  ];
  const headerRow = new TableRow({
    children: ["工具名称", "功能说明"].map(h => new TableCell({
      borders: makeBorder(), shading: { fill: COLORS.headerBg, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: h, bold: true, font: "Arial", size: 22, color: COLORS.white })] })]
    }))
  });
  const dataRows = tools.map((t, idx) => new TableRow({
    children: [
      new TableCell({ borders: makeBorder(), shading: { fill: idx % 2 === 0 ? COLORS.lightBg : COLORS.white, type: ShadingType.CLEAR }, margins: { top: 80, bottom: 80, left: 120, right: 120 }, verticalAlign: VerticalAlign.CENTER, children: [new Paragraph({ children: [new TextRun({ text: t.name, bold: true, font: "Arial", size: 22, color: COLORS.primary })] })] }),
      new TableCell({ borders: makeBorder(), shading: { fill: idx % 2 === 0 ? COLORS.lightBg : COLORS.white, type: ShadingType.CLEAR }, margins: { top: 80, bottom: 80, left: 120, right: 120 }, children: [new Paragraph({ children: [new TextRun({ text: t.desc, font: "Arial", size: 22, color: COLORS.black })] })] }),
    ]
  }));
  return new Table({
    width: { size: 9026, type: WidthType.DXA },
    columnWidths: [2411, 6615],
    rows: [headerRow, ...dataRows]
  });
}

// ============== DOCUMENT ==============
const doc = new Document({
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } }
      }]
    }]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 36, bold: true, font: "Arial", color: COLORS.primary }, paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0, border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: COLORS.primary } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 28, bold: true, font: "Arial", color: COLORS.secondary }, paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 24, bold: true, font: "Arial", color: COLORS.secondary }, paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: COLORS.border } },
          spacing: { after: 120 },
          children: [
            new TextRun({ text: "Wildberries 卖家运营培训手册", font: "Arial", size: 18, color: COLORS.gray }),
            new TextRun({ text: "  |  内部培训资料", font: "Arial", size: 18, color: COLORS.border }),
          ]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          border: { top: { style: BorderStyle.SINGLE, size: 1, color: COLORS.border } },
          spacing: { before: 120 },
          children: [
            new TextRun({ text: "第 ", font: "Arial", size: 18, color: COLORS.gray }),
            new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: COLORS.gray }),
            new TextRun({ text: " 页", font: "Arial", size: 18, color: COLORS.gray }),
          ]
        })]
      })
    },
    children: [

      // ========== COVER PAGE ==========
      new Paragraph({ spacing: { before: 2000, after: 0 }, children: [new TextRun("")] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 200 }, children: [new TextRun({ text: "Wildberries 卖家运营", bold: true, font: "Arial", size: 72, color: COLORS.primary })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 400 }, children: [new TextRun({ text: "员工培训手册", bold: true, font: "Arial", size: 72, color: COLORS.primary })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 800 }, children: [new TextRun({ text: "WB Seller Operations Training Manual（含操作截图）", font: "Arial", size: 28, color: COLORS.gray, italics: true })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 200 }, children: [new TextRun({ text: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━", font: "Arial", size: 22, color: COLORS.primary })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 100 }, children: [new TextRun({ text: "适用对象：跨境电商运营团队", font: "Arial", size: 24, color: COLORS.secondary })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 100 }, children: [new TextRun({ text: "文档版本：v2.0（含截图）  |  编制日期：2026年5月", font: "Arial", size: 22, color: COLORS.gray })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 100 }, children: [new TextRun({ text: "资料来源：Wildberries 官方卖家后台 & PRO培训平台", font: "Arial", size: 22, color: COLORS.gray })] }),

      // ========== TABLE OF CONTENTS ==========
      new Paragraph({ spacing: { before: 400, after: 0 }, children: [new TextRun("")] }),
      new Paragraph({ alignment: AlignmentType.CENTER, border: { top: { style: BorderStyle.SINGLE, size: 4, color: COLORS.primary } }, spacing: { before: 0, after: 200 }, children: [new TextRun("")] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 200 }, children: [new TextRun({ text: "目  录", bold: true, font: "Arial", size: 32, color: COLORS.primary })] }),
      new TableOfContents("目录", { hyperlink: true, headingStyleRange: "1-3" }),
      spacer(),

      // ========== CHAPTER 1 ==========
      pageBreak(),
      heading1("第一章  Wildberries 平台概述"),
      heading2("1.1  平台简介"),
      paragraph("Wildberries（野莓，简称WB）成立于2004年，是俄罗斯本土规模最大的电商平台之一，在俄语国家深度布局了自营物流网络。平台全面向中国卖家开放，致力于帮助中国卖家拓展海外市场，发展出口业务，并打造国际知名品牌。"),
      spacer(),
      statsTable(),
      spacer(),
      heading2("1.2  卖家后台主界面"),
      heading2("1.3  平台核心数据"),
      twoColTable("平台简介", ["Wildberries（野莓/WB）成立于2004年，是俄罗斯本土规模最大的电商平台之一", "全面向中国卖家开放", "自营物流网络覆盖俄语国家市场"], "核心优势", ["80+中国分拣中心，物流便捷", "9万+俄罗斯提货点，支持自提", "每日活跃买家7900万+", "中文界面及客服支持", "新卖家入驻费仅10,000元人民币"]),
      spacer(),
      twoColTable("支持国家", ["俄罗斯、白俄罗斯、哈萨克斯坦、吉尔吉斯斯坦、亚美尼亚等俄语国家"], "卖家支持", ["中文客服（support@wildberries.cn）", "PRO培训平台", "Jam数据分析工具"]),
      spacer(),

      // ========== CHAPTER 2 ==========
      heading1("第二章  卖家入驻流程"),
      heading2("2.1  入驻基本要求"),
      twoColTable("入驻材料", ["① 营业执照扫描件（无需翻译）", "② 绑定个人账户的手机号码（国内手机号即可）"], "入驻费用", ["入驻费：10,000元人民币（一次性）", "平台佣金：根据商品类目不同（3%~15%不等）", "仓储及物流费用：按实际使用量计算"]),
      spacer(),
      heading2("2.2  入驻三步流程"),
      bullet("第一步：确定商品——深入分析细分市场竞争对手，评估商品盈利潜力"),
      bullet("第二步：选择销售模式——了解FBS等多种销售模式，选择适合自身业务的模式"),
      bullet("第三步：注册并发布商品——准备营业执照扫描件，支付10,000元入驻费"),
      spacer(),
      heading2("2.3  卖家后台核心功能"),
      paragraph("注册成功后，卖家后台（seller.wildberries.ru）提供以下核心功能："),
      bullet("将商品添加到店铺，设置价格和折扣，处理订单"),
      bullet("跟踪商品配送、销售和退货情况"),
      bullet("查看店铺余额并将资金提现至账户"),
      bullet("使用推广工具并参与促销活动"),
      bullet("分析销售数据（内容分析模块）"),
      bullet("与买家及Wildberries客服团队沟通"),
      spacer(),
      importantBox("入驻前请完成以下准备：①制定商品品类规划 ②预测成本和利润 ③规划物流流程。未完成准备的卖家可能在运营初期遇到较大困难。"),
      spacer(),

      // ========== CHAPTER 3 ==========
      heading1("第三章  新手卖家入门指南（5步走）"),
      heading2("3.1  新手入门指南页面"),
      heading2("3.2  完整入驻流程图"),
      onboardingTable(),
      spacer(),
      heading2("3.3  第一步：了解平台计费并设置权限"),
      paragraph("卖家入驻后，应首先熟悉平台收费标准。平台主要费用包括："),
      bullet("平台佣金：根据商品类目不同，佣金比例有所差异（最低约3%，最高约15%）"),
      bullet("物流费用：从中国仓库发至WB分拣中心，或从俄罗斯海外仓发至买家"),
      bullet("仓储费用：商品在WB仓库存储产生的费用"),
      paragraph("同时，应在卖家设置中配置用户权限，确保团队成员拥有适当的操作权限。"),
      spacer(),
      heading2("3.4  第二步：创建商品卡，设置价格和折扣"),
      paragraph("创建商品卡前，请务必确认商品不在禁售清单中。创建流程包括："),
      bullet("准备商品信息（名称、描述、图片、视频）"),
      bullet("填写商品属性（品类、规格、颜色等）"),
      bullet("上传高质量商品图片（支持AI虚拟试衣功能）"),
      bullet("以人民币为单位设置商品价格（买家侧自动按WB内部汇率显示为卢布）"),
      spacer(),
      coloredBox("野莓内部汇率说明", [
        "卖家以人民币设置的价格，在买家网站上会根据Wildberries的内部汇率自动显示为卢布。",
        "内部汇率每天更新，该汇率不超过俄罗斯中央银行公布的人民币兑换卢布官方汇率的110%。",
        "卢布汇率的变化不会影响卖家的收款，订单金额在生成时以人民币固定，卖家以人民币收款。"
      ]),
      spacer(),
      heading2("3.5  第三步：创建仓库及上传库存"),
      paragraph("卖家仓库创建路径：FBS页面 → 我的仓库及通行证 → 卖家仓库 → 创建仓库"),
      bullet("上传库存有两种方式：通过卖家门户界面操作，或通过API接口上传"),
      bullet("如使用API，需在卖家设置中生成API令牌（仅账户所有者可操作）"),
      bullet("必须为从中国发货的订单和从俄罗斯仓库发货的订单分别选择退货自提点"),
      spacer(),
      heading2("3.6  第四步：查看订单发货指南"),
      paragraph("发货模式对比："),
      bullet("FBS（自发货）：卖家从中国仓库发货至WB中国/俄罗斯仓库，买家有120小时备货时间，库存可控，适合初期测试"),
      bullet("海外仓：从俄罗斯当地仓库发货，配送速度更快，客户体验好，但库存成本高"),
      bullet("混合模式：同时使用FBS和海外仓，灵活调配，优化成本"),
      spacer(),
      paragraph("重要时间节点：买家下单后，卖家有120小时的时间准备商品并将其交付给Wildberries在中国或俄罗斯的仓库。此时间无法调整或延长，请务必在规定时间内完成发货。"),
      spacer(),
      heading2("3.7  第五步：了解如何推广商品"),
      paragraph("WB提供多种推广渠道："),
      bullet("促销活动：可在促销日历中查看促销活动的时间表及参与条件"),
      bullet("欢迎奖金：新注册卖家将获得30,000积分（入职后3个月再送30,000积分，6个月后再送60,000积分）"),
      bullet("自动推广活动：让商品展示在用户当前搜索的位置，算法决定最佳展示位置"),
      bullet("搜索活动：根据买家特定搜索请求提升商品在搜索结果中的排名"),
      spacer(),

      // ========== CHAPTER 4 ==========
      heading1("第四章  财务管理与提款"),
      heading2("4.1  财务报告"),
      paragraph("WB每周一（莫斯科时间17:00后）生成上周的财务报告，这是包含所有商品交易信息及所有扣款和收入的主要财务报告。报告位于：财务报告 → 每周财务报告板块。"),
      spacer(),
      heading2("4.2  提款规则"),
      paragraph("上周销售的款项可在每周一（莫斯科时间17:00后）提现至绑定账户。卖家可以提现的金额基于每周财务报告生成。"),
      spacer(),
      heading2("4.3  支付系统连接"),
      paragraph("连接支付系统步骤：在设置中填写卖家信息选项卡中的所有字段，然后转到支付系统选项卡，连接可用的支付系统。"),
      spacer(),
      importantBox("严禁销售假冒伪劣商品。平台对侵权和售假行为有严格的处罚机制，一旦违规可能导致店铺被封禁及法律诉讼。"),
      spacer(),

      // ========== CHAPTER 5 ==========
      heading1("第五章  卖家忠诚度计划（8级佣金优惠）"),
      heading2("5.1  等级制度概述"),
      paragraph("WB卖家等级是根据店铺营业额将卖家划分为不同等级的系统。营业额越高，等级越高，享受的佣金优惠越大。等级制度的目的是激励卖家提高店铺月营业额，并帮助高营业额卖家保持商品价格的竞争力。"),
      spacer(),
      heading2("5.2  忠诚度计划官方页面"),
      heading2("5.3  等级详情与佣金优惠"),
      tierTable(),
      spacer(),
      heading2("5.4  GMV计入规则"),
      coloredBox("GMV计入规则", [
        "✓ 计入GMV：卖家以设定价格成交的订单金额（例如：商品定价1000元，完成交付即计入1000元GMV）",
        "✗ 不计入GMV：物流费用、罚款、平台佣金、平台折扣（如常客优惠和WB钱包折扣）",
        "✗ 从GMV中扣除：卖家自行提供的折扣金额、商品退货金额",
        "注意：下单后1小时内取消的订单不计入GMV；商品退货和买家拒收均不影响营业额统计"
      ]),
      spacer(),
      heading2("5.5  等级升降规则（1-7级）"),
      paragraph("• 等级每月重新计算：根据上个月的营业额，在下个月交付的订单享受相应等级的佣金优惠"),
      paragraph("• 降级触发条件：当月营业额低于目标GMV的80%，则在下个月降级至与当前营业额对应的等级"),
      paragraph("• 示例：2月销售额80,000元 → 3月等级为2级（10%优惠）→ 3月需完成80,000×80%=64,000元才能保持2级"),
      spacer(),
      heading2("5.6  8级特殊规则"),
      coloredBox("8级（最高等级）特殊说明", [
        "8级考核年度营业额（≥1.92亿元人民币/年），而非月度营业额",
        "达到8级后，该等级在当前自然年内有效，并完全延续到下一个自然年",
        "示例：2025年10月达到8级 → 等级延续至2026年全年，享40%佣金优惠",
        "要在2027年保持8级，需在2026年完成1.92亿元年度GMV"
      ]),
      spacer(),

      // ========== CHAPTER 6 ==========
      heading1("第六章  Jam 营销工具套件"),
      heading2("6.1  工具套件概述"),
      paragraph("Jam是Wildberries为卖家提供的业务增长工具组合，一份订阅可获得多种独家分析数据和优化工具，助力提升销售额。注册后享有60天免费试用期，试用期内完成首单后续订可享30%折扣。"),
      spacer(),
      heading2("6.2  核心工具清单"),
      jamToolsTable(),
      spacer(),

      // ========== CHAPTER 7 ==========
      heading1("第七章  PRO Wildberries 培训平台"),
      heading2("7.1  培训平台主界面"),
      heading2("7.2  平台数据（2025年）"),
      twoColTable("平台数据", ["76,000+ 人次观看直播", "22,000+ 人次参与论坛活动", "470,000+ 次文章阅读量", "40场论坛活动", "315个优秀毕业生案例", "4.8分平均活动评分"], "课程分类", ["新手卖家基础强化训练", "发展业务课程（商品、推广等主题）", "规模扩张课程（认证经理人库）", "定期直播与论坛活动"]),
      spacer(),
      heading2("7.3  核心培训资源"),
      bullet("新手卖家指南（中文版）- 5步入驻全流程"),
      bullet("卖家网络直播课程 - 实时互动学习"),
      bullet("WB Insight杂志 - 行业洞察与运营技巧"),
      bullet("优秀毕业生案例 - 实战经验分享"),
      spacer(),
      heading2("7.4  卖家支持渠道"),
      twoColTable("官方支持", ["中文客服邮箱：support@wildberries.cn", "帮助中心（seller.wildberries.ru/instructions）", "PRO WB直播课程", "微信/抖音/小红书官方账号"], "社交媒体", ["抖音：@wildberries", "快手：Wildberries官方", "小红书：WB官方", "微博：@wildberries_official"]),
      spacer(),

      // ========== CHAPTER 8 ==========
      heading1("第八章  后台操作指南（截图说明）"),
      heading2("8.1  帮助中心"),
      paragraph("WB卖家帮助中心提供全中文的操作指南，涵盖入驻、发货、商品管理、财务、推广等所有运营环节。建议运营团队在正式操作前先在帮助中心查阅相关教程。"),
      spacer(),
      heading2("8.2  商品发布操作要点"),
      bullet("登录 seller.wildberries.ru，进入「商品与价格」→「添加商品」"),
      bullet("上传商品图片（支持批量上传，建议每商品至少3张图片）"),
      bullet("填写商品名称（建议含俄语关键词以提升搜索排名）"),
      bullet("选择正确的商品类目，设置人民币价格"),
      bullet("提交后等待WB审核（通常1-3个工作日）"),
      spacer(),
      heading2("8.3  订单发货操作要点"),
      bullet("登录卖家后台，进入「FBS」→「我的订单」查看新订单"),
      bullet("点击「准备发货」，打印物流面单"),
      bullet("在120小时内将商品送至指定WB分拣中心"),
      bullet("莫斯科时间17:00后可在「财务报告」中查看上周财务明细"),
      spacer(),
      heading2("8.4  运营规范与注意事项"),
      bullet("商品信息须真实准确，不得有虚假宣传"),
      bullet("须在买家下单后120小时内将商品交付至WB仓库"),
      bullet("及时响应买家咨询，维护良好的客户评价"),
      bullet("定期查看促销日历，积极参与平台促销活动"),
      bullet("监控退货率，及时优化商品描述或改进产品质量"),
      spacer(),
      importantBox("Kdocs金山文档《WB罚款清单》和《WB禁售清单》包含详细完整的规定，建议运营团队全体成员认真学习。"),
      spacer(),

      // ========== CHAPTER 9 ==========
      heading1("第九章  数据分析与运营优化"),
      heading2("9.1  数据分析工具入口"),
      paragraph("WB提供内容分析模块（seller.wildberries.ru/content-analytics），卖家可以在此处查看店铺运营的所有主要分析数据，包括销售趋势、流量来源、转化率等关键指标。"),
      spacer(),
      heading2("9.2  核心数据指标"),
      twoColTable("销售数据", ["GMV（成交总额）", "订单数量", "客单价", "退货率", "拒收率"], "流量数据", ["浏览量（Impressions）", "点击量（Clicks）", "点击率（CTR）", "转化率", "搜索查询来源"]),
      spacer(),
      heading2("9.3  优化建议"),
      bullet("定期分析销售数据，识别爆款商品和滞销商品"),
      bullet("关注搜索查询报告，了解买家搜索习惯，优化商品标题和关键词"),
      bullet("利用买家画像报告，了解目标受众特征，制定精准营销策略"),
      bullet("关注退货率，及时优化商品描述或改进产品质量"),
      bullet("积极参与平台促销活动，提升曝光和销量"),
      spacer(),

      // ========== CHAPTER 10 ==========
      heading1("第十章  常见问题解答（FAQ）"),
      heading2("Q1：入驻WB需要准备哪些材料？"),
      paragraph("需要准备：①有效营业执照扫描件（无需翻译）②国内手机号码（用于绑定账户）③支付10,000元人民币入驻费。"),
      spacer(),
      heading2("Q2：平台佣金如何计算？"),
      paragraph("佣金根据商品类目不同有所差异（3%~15%不等），具体费率请在卖家后台「商品与价格 → 价格与折扣」中查看。佣金最终金额还受卖家等级优惠比例影响。"),
      spacer(),
      heading2("Q3：如何提升卖家等级？"),
      paragraph("卖家等级由近30天GMV决定，营业额越高等级越高，等级每月重新计算。维持当前等级需完成目标GMV的80%以上，否则将降级。8级为年度考核，需完成1.92亿元年度GMV。"),
      spacer(),
      heading2("Q4：订单发货时间是多少？"),
      paragraph("买家下单后，卖家有120小时（5天）的备货时间，须在此时间内将商品交付至WB中国或俄罗斯仓库。此时间不可延长。"),
      spacer(),
      heading2("Q5：货款如何结算和提现？"),
      paragraph("每周一（莫斯科时间17:00后）生成上周财务报告，上周销售款项可在周一之后申请提现至绑定账户。"),
      spacer(),
      heading2("Q6：汇率风险如何管理？"),
      paragraph("卖家以人民币设置价格，买家侧自动按WB内部汇率显示卢布。但订单金额在生成时以人民币固定，卖家以人民币收款，因此汇率波动对收款金额无影响。"),
      spacer(),
      heading2("Q7：遇到问题如何联系客服？"),
      paragraph("可通过seller.wildberries.ru页面右上角的问号图标联系中文客服，或发送邮件至support@wildberries.cn。PRO WB平台也提供直播答疑环节。"),
      spacer(),

      // ========== APPENDIX ==========
      heading1("附录  核心参考资料"),
      heading2("A.1  官方链接"),
      bullet("WB卖家后台：https://seller.wildberries.ru/"),
      bullet("WB PRO培训平台：https://pro.wildberries.cn/"),
      bullet("WB中文帮助中心：https://seller.wildberries.ru/instructions/ch/ch/categories"),
      bullet("新手卖家指南（PDF）：https://static-basket-02.wbbasket.ru/vol20/guides/fornewcommers.pdf"),
      spacer(),
      heading2("A.2  联系方式"),
      twoColTable("官方支持", ["邮箱：support@wildberries.cn", "PRO培训：pro.wildberries.cn", "官方合作伙伴计划"], "社交媒体", ["抖音：Wildberries官方", "快手：Wildberries官方", "小红书：WB官方", "微博：@wildberries_official"]),
      spacer(),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 400 }, children: [new TextRun({ text: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━", font: "Arial", size: 22, color: COLORS.border })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200 }, children: [new TextRun({ text: "— 文档结束 —", font: "Arial", size: 22, color: COLORS.gray, italics: true })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 100 }, children: [new TextRun({ text: "本手册内容基于Wildberries官方资料整理，截图摄于2026年5月，如有更新请以官网最新公告为准", font: "Arial", size: 18, color: COLORS.gray })] }),
    ]
  }]
});

const outputPath = "C:\\Users\\ASDCF\\Desktop\\WB卖家运营培训手册_纯文字版.docx";
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outputPath, buffer);
  console.log("文档更新成功：" + outputPath);
}).catch(err => {
  console.error("创建失败：", err);
  process.exit(1);
});
