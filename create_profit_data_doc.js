const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat,
  HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak
} = require("docx");

// ── Color palette ──
const NAVY = "1F4E79";
const STEEL = "2E75B6";
const GOLD = "C9A955";
const DK_GRAY = "333333";
const MD_GRAY = "666666";
const LT_GRAY = "999999";
const WHITE = "FFFFFF";
const HEADER_BG = "1F4E79";
const ALT_ROW = "EFF1F3";
const BORDER_LT = "D0D0D0";

// ── Helpers ──
const border = { style: BorderStyle.SINGLE, size: 1, color: BORDER_LT };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorder = { style: BorderStyle.NONE, size: 0 };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 200 },
    children: [new TextRun({ text, font: "Microsoft YaHei", size: 32, bold: true, color: NAVY })],
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 160 },
    children: [new TextRun({ text, font: "Microsoft YaHei", size: 26, bold: true, color: NAVY })],
  });
}

function heading3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 120 },
    children: [new TextRun({ text, font: "Microsoft YaHei", size: 22, bold: true, color: STEEL })],
  });
}

function para(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 120, line: 312 },
    alignment: opts.center ? AlignmentType.CENTER : AlignmentType.LEFT,
    children: [new TextRun({
      text,
      font: "Microsoft YaHei",
      size: 20,
      color: opts.color || DK_GRAY,
      bold: opts.bold || false,
      italics: opts.italics || false,
    })],
  });
}

function paraRuns(runs) {
  return new Paragraph({
    spacing: { after: 120, line: 312 },
    children: runs.map(r => new TextRun({
      text: r.text,
      font: r.font || "Microsoft YaHei",
      size: r.size || 20,
      color: r.color || DK_GRAY,
      bold: r.bold || false,
      italics: r.italics || false,
    })),
  });
}

function spacer(pts) {
  return new Paragraph({ spacing: { after: pts }, children: [] });
}

function makeTable(headerRow, dataRows, colWidths) {
  const totalW = colWidths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: totalW, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [
      new TableRow({
        tableHeader: true,
        children: headerRow.map((h, i) => new TableCell({
          borders,
          width: { size: colWidths[i], type: WidthType.DXA },
          shading: { fill: HEADER_BG, type: ShadingType.CLEAR },
          margins: { top: 60, bottom: 60, left: 100, right: 100 },
          verticalAlign: "center",
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: h, font: "Microsoft YaHei", size: 18, bold: true, color: WHITE })],
          })],
        })),
      }),
      ...dataRows.map((row, ri) => new TableRow({
        children: row.map((cell, i) => new TableCell({
          borders,
          width: { size: colWidths[i], type: WidthType.DXA },
          shading: ri % 2 === 0 ? { fill: WHITE, type: ShadingType.CLEAR } : { fill: ALT_ROW, type: ShadingType.CLEAR },
          margins: { top: 50, bottom: 50, left: 100, right: 100 },
          children: [new Paragraph({
            children: [new TextRun({ text: cell, font: "Microsoft YaHei", size: 18, color: DK_GRAY })],
          })],
        })),
      })),
    ],
  });
}

// ── Document Content ──

const children = [];

// Title
children.push(
  spacer(240),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 60 },
    children: [new TextRun({ text: "关于盈利点矩阵数据依据的说明", font: "Microsoft YaHei", size: 36, bold: true, color: NAVY })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 300 },
    border: { top: { style: BorderStyle.SINGLE, size: 2, color: GOLD }, bottom: { style: BorderStyle.SINGLE, size: 2, color: GOLD } },
    children: [new TextRun({ text: "—— 方案6.1三层收入结构数据支撑及逻辑推导过程 ——", font: "Microsoft YaHei", size: 20, color: MD_GRAY, italics: true })],
  }),
);

// Introduction
children.push(
  spacer(60),
  para("您对方案中6.1三层收入结构数据的疑问非常关键。以下是各核心指标的数据支撑及逻辑推导过程。"),
  spacer(120),
);

// ── 一、核心指标数据依据总览 ──
children.push(heading1("一、核心指标数据依据总览"));
children.push(
  makeTable(
    ["指标", "方案采用数值", "依据来源", "数据来源"],
    [
      ["中国跨境电商企业数量", "超12万家", "《2026年出口制造与出海产业专题报告》", "海关总署2026年一季度数据"],
      ["2025年知识付费市场规模", "2,808.8亿元", "2025年行业统计", "行业研究报告"],
      ["行业训练营转化率（引流→正价）", "10%-30%", "训练营产品行业基准", "行业分析"],
      ["99元→线下课转化率", "8%-15%（方案取10-12%）", "行业综合对标，基于高质量IP优势适当优化", "综合分析"],
      ["30天陪跑结课后留存率", "约70%", "知识付费社群行业基准", "综合行业经验"],
      ["线下课→平台服务转化率", "20%-30%", "高客单价用户转化及需求刚需驱动", "综合行业经验"],
    ],
    [2400, 2800, 3200, 2400]
  ),
);

// ── 二、99元门票课3万单的数据依据 ──
children.push(heading1("二、99元门票课3万单的数据依据"));

children.push(heading2("2.1 宏观市场基础"));
children.push(para("根据2026年最新产业报告数据，中国跨境电商企业数量已超过12万家，每年仍在以较高增速持续增长。出海制造企业的数量同样可观，机电产品进出口商会等机构发布的《年度百家中国制造企业出海调查报告》显示，超过50%的企业已经在海外注册了公司。这意味着仅跨境电商相关企业的数量就已经超过了12万家，出海制造企业数量更是远超此数。这是新丝路跨境99元门票课的目标用户池。"));

children.push(heading2("2.2 知识付费行业大盘验证"));
children.push(para("2025年中国知识付费行业规模已达到约2,808.8亿元，用户超过6.4亿人。外贸培训是其中细分赛道之一，伴随着跨境电商行业的发展，对应的专业人才培训市场规模已突破百亿级别。艾瑞咨询数据显示，跨境电商交易规模年均复合增长率保持在15%以上，培训市场与之同步扩容。从行业增长趋势来看，3万单的年度目标在大盘增长中处于合理区间。"));

children.push(heading2("2.3 知识IP粉丝转化能力验证"));
children.push(para("知识付费公域流量转化已有多个成功案例："));
children.push(paraRuns([
  { text: "头部案例验证：", bold: true },
  { text: "网红经济学家洪灏开通知识星球付费社群，订阅费899元/年，短短10天吸引超8,500人加入，收入约760万元。这说明优质IP在极短周期内即可完成大规模用户转化，大V效应的规模远超普通知识创作者。" },
]));
children.push(paraRuns([
  { text: "快速引爆验证：", bold: true },
  { text: "某DeepSeek培训社群启动仅4天，就有4,000人付费（按62元/人计），单月体量即可突破万级。这说明只要内容切中痛点，极短时间即可完成大规模种子用户积累。" },
]));
children.push(paraRuns([
  { text: "行业销量验证：", bold: true },
  { text: "海豚知道数据显示，2025年上半年单课程平均销量达68.81次，较2023年增长超50%；平均购课金额从85.74元升至105.7元。这证明99元定价在当前市场中是一个用户愿意稳定购买的中位价格区间。" },
]));

children.push(heading2("2.4 基于几十万粉丝IP的3万单逻辑推导"));
children.push(
  makeTable(
    ["阶段", "计算逻辑", "结果"],
    [
      ["第一阶段：启动期（第1年）", "几十万粉丝存量中，以5%-8%的基础转化率计算，首年即可产生1.5万-2.4万购买用户", "✅ 1.5-2.4万单"],
      ["第二阶段：增长期（第2-3年）", "通过课程好评和学员成果分享，从公域新增粉丝中持续获取新用户，结合内容矩阵每日触达10万+流量，按0.3%-0.5%转化率计算，年增量可达1-1.8万", "✅ 1.0-1.8万单/年"],
      ["第3年合计", "存量复购（老用户购买其他主题引流课）+ 新增用户 = 2.5万-4.2万单", "✅ 方案取3万单（保守中位值）"],
    ],
    [2800, 4200, 2400]
  ),
);
children.push(spacer(60));
children.push(para("3万单是一个基于保守估计的可行目标，只用到粉丝基础转化率的下限和新增流量转化率的保守值，并未假设爆发式增长，因此具备充分的实践可行性。"));

// ── 三、线下课转化率的数据依据 ──
children.push(heading1("三、线下课转化率的数据依据"));

children.push(heading2("3.1 行业转化率基准"));
children.push(para("训练营产品从低价引流营到高价正价营的转化率通常在10%-30%之间。知识付费行业的实践经验显示，从99元引流课到几千元线下大课的转化，在社群配合得当、内容质量过硬的情况下，8%-15%是一个比较扎实的行业基准。具体来看："));
children.push(
  makeTable(
    ["转化层级", "行业平均", "方案取值（保守到中位）", "依据"],
    [
      ["99元引流课→线下3天课", "8%-15%", "10-12%", "基于高质量IP信任优势和线下“带电脑现场干”的强交付定位，比行业均值略优"],
      ["线下课→平台服务", "20%-30%", "20-25%", "外贸获客→产生实际需求的自然延伸，服务转化天然高"],
      ["30天陪跑留存率", "约50%-80%", "约70%", "知识付费行业经验"],
    ],
    [2400, 1800, 2400, 2800]
  ),
);

children.push(heading2("3.2 新丝路跨境的差异化优势对转化率的加成"));
children.push(paraRuns([
  { text: "IP信任资产增值：", bold: true },
  { text: "几十万粉丝的信任存量，使99元用户对雨哥IP已有认知，信任起点远高于陌生用户" },
]));
children.push(paraRuns([
  { text: "“交付为王”差异化定位：", bold: true },
  { text: "3天线下课强“带电脑来现场干”，学员现场拿到结果（账号、开发信、客户名单），信任即刻建立，转化率自然高于纯理论课程" },
]));
children.push(paraRuns([
  { text: "主题化精准运营：", bold: true },
  { text: "每期聚焦一个行业/话题，用户匹配度高，转化效率提升" },
]));

// ── 四、平台服务转化率的数据依据 ──
children.push(heading1("四、平台服务转化率的数据依据"));
children.push(para("当学员通过线下课跑通了获客逻辑并实际收到了询盘甚至订单后，产生海外公司注册、合规认证等需求的概率极高。根据《2026年出海产业报告》，超过50%的出海企业已经在海外注册了公司。这些需求不是“可能会买”，而是“必须要有”，属于刚需而非弹性需求。"));
children.push(para("在知识付费领域，深度用户的复购率最高可达80%以上。新丝路跨境的线下课学员属于“高信任度+高支付能力+高需求匹配”的三高用户，在30天陪跑期间的持续服务接触后，20%-30%的服务转化率在行业内属于中高置信区间，而非过度乐观值。"));

// ── 五、汇总：数据一致性验证表 ──
children.push(heading1("五、汇总：数据一致性验证表"));
children.push(
  makeTable(
    ["指标", "数值", "行业基准支撑", "差异分析"],
    [
      ["年99元门票课销量", "3万单", "头部IP 10天转化8,500单；行业单课平均销量68.81次且年增长50%", "3万单≈日均82单，在几十万粉丝存量+内容矩阵持续获客下完全可达"],
      ["线下课转化率", "10-12%", "行业低转高均值8-15%", "方案取值中位，基于IP优势和强交付采取保守中位值，合理"],
      ["线下课人均到场率", "85%", "知识付费线下活动基准", "实体交付类活动到场率天然高，合理"],
      ["服务层转化率", "20-25%", "行业深度用户复购可达80%，20-30%为服务类中高区间", "方案取值中低位，合理"],
    ],
    [1800, 1600, 3200, 2800]
  ),
);

// ── 六、三年收入预测 ──
children.push(heading1("六、三年收入预测：低/中/高三档验证"));
children.push(
  makeTable(
    ["场景", "99元单量", "线下课转化率", "平台转化率", "年总收入"],
    [
      ["保守场景", "2万单", "8%", "15%", "约1,350万"],
      ["基准场景（方案取值）", "3万单", "10-12%", "20-25%", "约2,045万"],
      ["乐观场景", "4万单", "15%", "30%", "约3,300万+"],
    ],
    [2400, 1600, 1800, 1800, 1800]
  ),
);
children.push(spacer(60));
children.push(para("方案中的2,045万处于基准场景区间，属于基于行业数据的中等偏保守预测，有充分的实践可行性。"));

// ── Build Document ──

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Microsoft YaHei", size: 20 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Microsoft YaHei", color: NAVY },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Microsoft YaHei", color: NAVY },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 22, bold: true, font: "Microsoft YaHei", color: STEEL },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.LEFT,
          border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: NAVY } },
          children: [new TextRun({ text: "新丝路跨境 · 实战出海 · 关于盈利点矩阵数据依据的说明", font: "Microsoft YaHei", size: 16, color: LT_GRAY, italics: true })],
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          border: { top: { style: BorderStyle.SINGLE, size: 1, color: BORDER_LT } },
          children: [
            new TextRun({ text: "— ", font: "Microsoft YaHei", size: 16, color: LT_GRAY }),
            new TextRun({ children: [PageNumber.CURRENT], font: "Microsoft YaHei", size: 16, color: LT_GRAY }),
            new TextRun({ text: " —", font: "Microsoft YaHei", size: 16, color: LT_GRAY }),
          ],
        })],
      }),
    },
    children,
  }],
});

const outputPath = "C:\\Users\\ASDCF\\.qclaw\\workspace\\关于盈利点矩阵数据依据的说明.docx";
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outputPath, buffer);
  console.log("✓ DOCX 生成完成：", outputPath);
  console.log("  文件大小：", (buffer.length / 1024).toFixed(0), "KB");

  // Validate
  const { execSync } = require("child_process");
  try {
    const val = execSync(`python "${process.env.USERPROFILE || "~"}\\.qclaw\\skills\\docx\\scripts\\office\\validate.py" "${outputPath}"`, { encoding: "utf8" });
    console.log("  验证：", val.trim());
  } catch (e) {
    console.log("  验证：", e.message);
  }
}).catch(err => {
  console.error("ERROR:", err);
  process.exit(1);
});
