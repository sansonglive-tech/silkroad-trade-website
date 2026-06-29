const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageNumber, LevelFormat
} = require("docx");

// Border helper
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

// Table cell helper
function makeCell(text, opts = {}) {
  const { bold, shading, width } = opts;
  const runs = [];
  if (bold || opts.isHeader) {
    runs.push(new TextRun({ text, bold: true, font: "Microsoft YaHei", size: 22 }));
  } else {
    runs.push(new TextRun({ text, font: "Microsoft YaHei", size: 22 }));
  }
  return new TableCell({
    borders,
    width: width ? { size: width, type: WidthType.DXA } : undefined,
    shading: shading ? { fill: shading, type: ShadingType.CLEAR } : undefined,
    margins: cellMargins,
    verticalAlign: "center",
    children: [new Paragraph({ children: runs, alignment: AlignmentType.LEFT })],
  });
}

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Microsoft YaHei", size: 22 } } },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Microsoft YaHei", color: "1F4E79" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 },
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Microsoft YaHei", color: "2E75B6" },
        paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 1 },
      },
      {
        id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Microsoft YaHei", color: "404040" },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 },
      },
    ],
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } },
        }],
      },
      {
        reference: "numbers",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } },
        }],
      },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 11906, height: 16838 }, // A4
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        },
      },
      headers: {
        default: new Header({
          children: [
            new Paragraph({
              alignment: AlignmentType.RIGHT,
              children: [
                new TextRun({ text: "2026 国际无人机应用及防控大会", font: "Microsoft YaHei", size: 18, color: "808080", italics: true }),
              ],
            }),
          ],
        }),
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [
                new TextRun({ text: "第 ", font: "Microsoft YaHei", size: 18, color: "808080" }),
                new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "808080" }),
                new TextRun({ text: " 页", font: "Microsoft YaHei", size: 18, color: "808080" }),
              ],
            }),
          ],
        }),
      },
      children: [
        // ========== Title ==========
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 100 },
          children: [
            new TextRun({ text: "2026 国际无人机应用及防控大会", font: "Microsoft YaHei", size: 44, bold: true, color: "1F4E79" }),
          ],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 },
          children: [
            new TextRun({ text: "第七届中国国际无人机及无人系统博览会", font: "Microsoft YaHei", size: 32, bold: true, color: "2E75B6" }),
          ],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 },
          children: [
            new TextRun({ text: "—— 参观购票指南", font: "Microsoft YaHei", size: 26, color: "808080" }),
          ],
        }),

        // ========== Section 1: 基本信息 ==========
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("一、展会基本信息")] }),

        new Table({
          width: { size: 9026, type: WidthType.DXA },
          columnWidths: [2400, 6626],
          rows: [
            new TableRow({
              children: [
                makeCell("展 会 名 称", { bold: true, shading: "D5E8F0", width: 2400 }),
                makeCell("2026 国际无人机应用及防控大会暨第七届中国国际无人机及无人系统博览会", { width: 6626 }),
              ],
            }),
            new TableRow({
              children: [
                makeCell("举 办 时 间", { bold: true, shading: "D5E8F0", width: 2400 }),
                makeCell("2026年6月25日（周四）— 6月27日（周日）", { width: 6626 }),
              ],
            }),
            new TableRow({
              children: [
                makeCell("举 办 地 点", { bold: true, shading: "D5E8F0", width: 2400 }),
                makeCell("北京国家会议中心", { width: 6626 }),
              ],
            }),
            new TableRow({
              children: [
                makeCell("展 馆 地 址", { bold: true, shading: "D5E8F0", width: 2400 }),
                makeCell("北京市朝阳区奥运村街道天辰东路7号", { width: 6626 }),
              ],
            }),
            new TableRow({
              children: [
                makeCell("展 会 规 模", { bold: true, shading: "D5E8F0", width: 2400 }),
                makeCell("展览面积 20,000 ㎡ / 参展商 500+ 家 / 观众 50,000+ 人", { width: 6626 }),
              ],
            }),
            new TableRow({
              children: [
                makeCell("主 办 单 位", { bold: true, shading: "D5E8F0", width: 2400 }),
                makeCell("中国光学工程学会、国际无人机从业者协会、欧洲无人机培训运营协会、意大利航空航天企业协会、首都会展（集团）有限公司、中国航空器拥有者及驾驶员协会（AOPA）", { width: 6626 }),
              ],
            }),
            new TableRow({
              children: [
                makeCell("承 办 单 位", { bold: true, shading: "D5E8F0", width: 2400 }),
                makeCell("中国光学工程学会无人机产业创新专业委员会、北京北辰领航商务会展有限公司等", { width: 6626 }),
              ],
            }),
          ],
        }),

        // ========== Section 2: 购票方式 ==========
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("二、购票方式")] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("方式一：大会官网预登记（推荐）")] }),
        new Paragraph({
          spacing: { after: 80 },
          children: [new TextRun({ text: "登录大会官方网站 ", font: "Microsoft YaHei", size: 22 }), new TextRun({ text: "https://www.uav-expo.cn/", font: "Microsoft YaHei", size: 22, bold: true, color: "0563C1" }), new TextRun({ text: "，点击导航栏「参观登记」进行线上预登记。", font: "Microsoft YaHei", size: 22 })],
        }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "中国观众：实名制绑定身份证信息", font: "Microsoft YaHei", size: 22 })] }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "港澳台观众：实名制绑定港澳台通行证", font: "Microsoft YaHei", size: 22 })] }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "国外观众：实名制绑定护照信息", font: "Microsoft YaHei", size: 22 })] }),
        new Paragraph({ spacing: { before: 80, after: 120 }, children: [new TextRun({ text: "现场凭电子门票二维码或刷身份证入场。", font: "Microsoft YaHei", size: 22 })] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("方式二：聚展网（折扣价购票）")] }),
        new Paragraph({
          spacing: { after: 80 },
          children: [
            new TextRun({ text: "通过聚展平台购票，可在官网价基础上享受折扣：", font: "Microsoft YaHei", size: 22 }),
          ],
        }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "标准票价：¥55", font: "Microsoft YaHei", size: 22 })] }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "折扣价：¥29", font: "Microsoft YaHei", size: 22, bold: true })] }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "购票网址：https://www.jufair.com/exhibition/3211.html", font: "Microsoft YaHei", size: 22, color: "0563C1" })] }),

        new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("方式三：学术/产业会议报名")] }),
        new Paragraph({
          spacing: { after: 80 },
          children: [new TextRun({ text: "参加同期举办的专题会议需通过以下专属入口报名：", font: "Microsoft YaHei", size: 22 })],
        }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "学术会场（智能无人系统及应用大会）：https://b2b.csoe.org.cn/meeting/UAV2026.html", font: "Microsoft YaHei", size: 22, color: "0563C1" })] }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "产业论坛（14场应用交流会）：https://t.eainfor.com/T/w/148T2", font: "Microsoft YaHei", size: 22, color: "0563C1" })] }),

        // ========== Section 3: 展会日程 ==========
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("三、展会日程安排")] }),

        new Table({
          width: { size: 9026, type: WidthType.DXA },
          columnWidths: [2400, 6626],
          rows: [
            new TableRow({
              children: [
                makeCell("6月24日（周三）下午", { bold: true, shading: "D5E8F0", width: 2400 }),
                makeCell("大会报到 / 布展", { width: 6626 }),
              ],
            }),
            new TableRow({
              children: [
                makeCell("6月25日（周四）上午", { bold: true, shading: "D5E8F0", width: 2400 }),
                makeCell("开幕式、主旨报告", { width: 6626 }),
              ],
            }),
            new TableRow({
              children: [
                makeCell("6月25日（周四）下午 — 27日（周日）全天", { bold: true, shading: "D5E8F0", width: 2400 }),
                makeCell("专题分会 / 博览会展览 / 全国无人机创新技能大赛", { width: 6626 }),
              ],
            }),
          ],
        }),

        // ========== Section 4: 展品范围 ==========
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("四、展品范围概览")] }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "无人机系统：多旋翼、固定翼、复合翼、无人直升机、FPV穿越机等", font: "Microsoft YaHei", size: 22 })] }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "核心部件：任务载荷、数据链路、5G网联设备、动力系统、导航设备等", font: "Microsoft YaHei", size: 22 })] }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "通航与低空经济：eVTOL、空管技术、运营服务平台、低空基础设施", font: "Microsoft YaHei", size: 22 })] }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "无人机防控技术及系统：探测、跟踪、识别与反制全链条解决方案", font: "Microsoft YaHei", size: 22 })] }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "无人系统技术及装备：地面机器人、机器狗、无人车、无人艇、水下潜航器", font: "Microsoft YaHei", size: 22 })] }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "应急智能装备：智能消防机器人、救援机器人、应急指挥调度平台", font: "Microsoft YaHei", size: 22 })] }),

        // ========== Section 5: 特色活动 ==========
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("五、同期特色活动")] }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "2026 全国无人机创新技能大赛（不收取参赛费用）", font: "Microsoft YaHei", size: 22 })] }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "14 场产业应用交流会（覆盖警用、测绘、植保、低空经济等方向）", font: "Microsoft YaHei", size: 22 })] }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "10 场学术专题会议（光电系统、反制技术、通信组网等前沿领域）", font: "Microsoft YaHei", size: 22 })] }),

        // ========== Section 6: 联系方式 ==========
        new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("六、组委会联系方式")] }),

        new Table({
          width: { size: 9026, type: WidthType.DXA },
          columnWidths: [4000, 5026],
          rows: [
            new TableRow({
              children: [
                makeCell("会议及赞助合作", { bold: true, shading: "D5E8F0", width: 4000 }),
                makeCell("鄂老师：13001030561", { width: 5026 }),
              ],
            }),
            new TableRow({
              children: [
                makeCell("展览展示及大赛咨询", { bold: true, shading: "D5E8F0", width: 4000 }),
                makeCell("王老师：13810630623", { width: 5026 }),
              ],
            }),
            new TableRow({
              children: [
                makeCell("大会官网", { bold: true, shading: "D5E8F0", width: 4000 }),
                makeCell("https://www.uav-expo.cn/", { width: 5026 }),
              ],
            }),
          ],
        }),

        // ========== Footer note ==========
        new Paragraph({
          spacing: { before: 480 },
          alignment: AlignmentType.RIGHT,
          children: [
            new TextRun({ text: "文档生成时间：2026 年 6 月 24 日", font: "Microsoft YaHei", size: 18, color: "808080", italics: true }),
          ],
        }),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  const outPath = "C:\\Users\\ASDCF\\.qclaw\\workspace\\2026无人机博览会参观购票指南.docx";
  fs.writeFileSync(outPath, buffer);
  console.log("Document created: " + outPath);
});
