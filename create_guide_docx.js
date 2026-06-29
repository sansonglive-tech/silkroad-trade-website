const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageNumber, PageBreak, LevelFormat } = require('docx');

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorders = {
  top: { style: BorderStyle.NONE, size: 0 },
  bottom: { style: BorderStyle.NONE, size: 0 },
  left: { style: BorderStyle.NONE, size: 0 },
  right: { style: BorderStyle.NONE, size: 0 }
};

function cell(text, opts = {}) {
  return new TableCell({
    borders: opts.noBorder ? noBorders : borders,
    width: { size: opts.width || 4680, type: WidthType.DXA },
    shading: opts.shading ? { fill: opts.shading, type: ShadingType.CLEAR } : undefined,
    margins: { top: 60, bottom: 60, left: 120, right: 120 },
    children: [new Paragraph({
      alignment: opts.align || AlignmentType.LEFT,
      spacing: { before: 0, after: 0 },
      children: [new TextRun({
        text: text,
        font: "Arial",
        size: opts.size || 20,
        bold: opts.bold || false,
        color: opts.color || "333333"
      })]
    })]
  });
}

function hcell(text, width) {
  return cell(text, { width, bold: true, shading: "D5E8F0", color: "1A1512", size: 20 });
}

function noteCell(text, width) {
  return cell(text, { width, size: 18, color: "888888" });
}

// Build warning table
const warningRows = [
  new TableRow({ children: [
    hcell("❌ 不要做", 4680),
    hcell("✅ 正确做法", 4680)
  ]}),
  new TableRow({ children: [
    cell("改配置区下面的代码", 4680, { size: 18 }),
    cell("只改 CONFIG 配置区（能看到 // >>> 标记的区域）", 4680, { size: 18 })
  ]}),
  new TableRow({ children: [
    cell("删掉逗号 , 或引号 \"", 4680, { size: 18 }),
    cell("符号原样保留，只改里面的中文或图片链接", 4680, { size: 18 })
  ]}),
  new TableRow({ children: [
    cell("把 // 开头的注释行删掉", 4680, { size: 18 }),
    cell("灰字注释只是提示，留着没关系", 4680, { size: 18 })
  ]}),
];

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: "1A1512" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: "C44536" },
        paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: "333333" },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } },
    ]
  },
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numsteps",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 }, // A4
        margin: { top: 1440, right: 1440, bottom: 1200, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: "丝路山海通 v7 — 小白修改指南", font: "Arial", size: 16, color: "999999", italics: true })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "第 ", font: "Arial", size: 16, color: "999999" }),
                     new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 16, color: "999999" }),
                     new TextRun({ text: " 页", font: "Arial", size: 16, color: "999999" })]
        })]
      })
    },
    children: [
      // ===== COVER =====
      new Paragraph({
        spacing: { before: 3600, after: 200 },
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "🦞 丝路山海通 v7", font: "Arial", size: 44, bold: true, color: "C44536" })]
      }),
      new Paragraph({
        spacing: { after: 200 },
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "修改指南（编码小白专用）", font: "Arial", size: 32, color: "333333" })]
      }),
      new Paragraph({
        spacing: { after: 600 },
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "文件：silkroad-trade_v7_silk_poster.html", font: "Arial", size: 20, color: "888888" })]
      }),
      new Paragraph({ children: [new PageBreak()] }),

      // ===== 1. 概述 =====
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("1. 这个文件是什么？")] }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "silkroad-trade_v7_silk_poster.html", font: "Arial", size: 22, bold: true }),
                   new TextRun({ text: " 是一个网页文件，双击就能在浏览器打开，不需要联网，不需要服务器。", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "整个文件的内容分为两部分：", font: "Arial", size: 22 })]
      }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "配置区（需要你改的部分）", font: "Arial", size: 22, bold: true }),
                   new TextRun({ text: " — 公司名称、图片链接、联系方式等，都在最顶部集中管理", font: "Arial", size: 22 })]
      }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "代码区（不需要动）", font: "Arial", size: 22, bold: true }),
                   new TextRun({ text: " — 样式、布局、弹窗等功能代码，碰都不要碰", font: "Arial", size: 22 })]
      }),

      // ===== 2. 四大步骤 =====
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("2. 修改只需 4 步")] }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun({ text: "你不需要懂任何编码，按下面步骤操作即可。", font: "Arial", size: 22 })]
      }),

      // Step 1
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("第一步：打开文件")] }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "找到电脑上的 silkroad-trade_v7_silk_poster.html 文件：", font: "Arial", size: 22 })]
      }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "鼠标右键点击文件 → 选择「打开方式」→ 选「记事本」", font: "Arial", size: 22 })]
      }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "也可以先打开记事本，再把文件拖进去", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        spacing: { before: 80, after: 80 },
        children: [new TextRun({ text: "💡 提示：", font: "Arial", size: 20, bold: true, color: "C8923E" }),
                   new TextRun({ text: "记事本里那些乱七八糟的英文字母你都不用管，后面只改一小块地方。", font: "Arial", size: 20, color: "888888" })]
      }),
      new Paragraph({ children: [new PageBreak()] }),

      // Step 2
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("第二步：找到修改区")] }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "在记事本里按 ", font: "Arial", size: 22 }),
                   new TextRun({ text: "Ctrl + F", font: "Arial", size: 22, bold: true }),
                   new TextRun({ text: " 打开搜索框", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "在搜索框输入：", font: "Arial", size: 22 }),
                   new TextRun({ text: " // >>> ", font: "Arial", size: 22, bold: true, color: "C44536" }),
                   new TextRun({ text: "（不含空格也行）", font: "Arial", size: 20, color: "888888" })]
      }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "按回车，光标会跳到这个位置：", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        spacing: { before: 120, after: 120 }, indent: { left: 720 },
        shading: { fill: "F5F0EA", type: ShadingType.CLEAR },
        children: [new TextRun({ text: "// >>>  🎯 配 置 区 — 在这里修改所有内容和图片  🎯 <<<", font: "Arial", size: 20, bold: true, color: "C44536" })]
      }),
      new Paragraph({
        spacing: { before: 120, after: 80 },
        shading: { fill: "FFF3DC", type: ShadingType.CLEAR },
        children: [new TextRun({ text: "⚠️ 重要提醒：", font: "Arial", size: 22, bold: true, color: "C44536" }),
                   new TextRun({ text: "只改这个黄色区域的里面的内容！下面的代码一个字都别动！", font: "Arial", size: 22, bold: true, color: "C44536" })]
      }),

      // Step 3
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("第三步：开始修改")] }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "下面举几个例子，你对着改就行：", font: "Arial", size: 22 })]
      }),

      // 3.1 Image URL Guide
      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("🖼️ 图片变成链接的方法（新手必看）")] }),
      new Paragraph({
        spacing: { after: 80 },
        children: [new TextRun({ text: "配置区里的图片都是「链接」形式，不是直接把图片文件贴进去。所以你要先把自己的图片上传到网上，拿到链接，再粘贴替换。", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        spacing: { after: 80 },
        children: [new TextRun({ text: "下面教你用免费图床（ImgKB）操作：", font: "Arial", size: 22 })]
      }),
      new Paragraph({ numbering: { reference: "numsteps", level: 0 },
        children: [new TextRun({ text: "打开浏览器，访问 ", font: "Arial", size: 22 }),
                   new TextRun({ text: "https://imgkb.com", font: "Arial", size: 22, bold: true, color: "C44536" }),
                   new TextRun({ text: "（免注册，纯免费，支持中文）", font: "Arial", size: 20, color: "888888" })]
      }),
      new Paragraph({ numbering: { reference: "numsteps", level: 0 },
        children: [new TextRun({ text: "点击页面中间的「Upload」或「选择文件」按钮", font: "Arial", size: 22 })]
      }),
      new Paragraph({ numbering: { reference: "numsteps", level: 0 },
        children: [new TextRun({ text: "选中电脑上的图片（支持 JPG、PNG 格式，单张不超过 5MB）", font: "Arial", size: 22 })]
      }),
      new Paragraph({ numbering: { reference: "numsteps", level: 0 },
        children: [new TextRun({ text: "上传成功后，页面会显示一个链接列表——找到 ", font: "Arial", size: 22 }),
                   new TextRun({ text: "URL 或 Link", font: "Arial", size: 22, bold: true }),
                   new TextRun({ text: " 那一行，点击右边的「复制」按钮", font: "Arial", size: 22 })]
      }),
      new Paragraph({ numbering: { reference: "numsteps", level: 0 },
        children: [new TextRun({ text: "回到记事本，找到要替换的图片链接，按 ", font: "Arial", size: 22 }),
                   new TextRun({ text: "Ctrl + V", font: "Arial", size: 22, bold: true }),
                   new TextRun({ text: " 粘贴覆盖掉原来的链接", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        spacing: { before: 80, after: 80 },
        shading: { fill: "FFF3DC", type: ShadingType.CLEAR },
        children: [new TextRun({ text: "📌 简单理解：", font: "Arial", size: 20, bold: true, color: "C8923E" }),
                   new TextRun({ text: "图片链接就像你家照片的网址，记事本里放的是网址，不是照片本身。所以换图片 = 换网址。", font: "Arial", size: 20, color: "666666" })]
      }),
      new Paragraph({
        spacing: { before: 60, after: 80 },
        children: [new TextRun({ text: "其他图床也可以：", font: "Arial", size: 20, bold: true }),
                   new TextRun({ text: "ImgKB、imgbb.com、路过图床 imgse.com 等都免费免注册。imgbb.com 支持上传 32MB，也很大方。", font: "Arial", size: 20, color: "888888" })]
      }),

      // 3.2 Company name
      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("🏢 改公司名称")] }),
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "找到这一行：", font: "Arial", size: 22 })] }),
      new Paragraph({
        spacing: { before: 60, after: 60 }, indent: { left: 720 },
        shading: { fill: "F0F0F0", type: ShadingType.CLEAR },
        children: [new TextRun({ text: 'companyName: "丝路山海通",', font: "Consolas", size: 20, color: "333333" })]
      }),
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "改成你的名字：", font: "Arial", size: 22 })] }),
      new Paragraph({
        spacing: { before: 60, after: 60 }, indent: { left: 720 },
        shading: { fill: "F0F0F0", type: ShadingType.CLEAR },
        children: [new TextRun({ text: 'companyName: "我的贸易公司",   ', font: "Consolas", size: 20, bold: true, color: "C44536" }),
                   new TextRun({ text: "← 只改双引号里的字", font: "Arial", size: 18, color: "888888" })]
      }),

      // 3.2 Slides
      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("🖼️ 换轮播图图片")] }),
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "在配置区找到 slides: [ 部分，每张图长这样：", font: "Arial", size: 22 })] }),
      new Paragraph({
        spacing: { before: 60, after: 60 }, indent: { left: 720 },
        shading: { fill: "F0F0F0", type: ShadingType.CLEAR },
        children: [new TextRun({ text: "img: 'https://images.unsplash.com/photo-xxxxx'", font: "Consolas", size: 18 })]
      }),
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "把 https://... 那段链接换掉就行。", font: "Arial", size: 22 })] }),
      new Paragraph({
        spacing: { before: 80, after: 80 },
        shading: { fill: "FFF3DC", type: ShadingType.CLEAR },
        children: [new TextRun({ text: "💡 哪里找图片？", font: "Arial", size: 20, bold: true, color: "C8923E" }),
                   new TextRun({ text: "去 unsplash.com 搜索关键词 → 点一张图 → 右键「复制图片链接」→ 粘贴替换", font: "Arial", size: 20, color: "666666" })]
      }),
      new Paragraph({ children: [new PageBreak()] }),

      // 3.3 Country image
      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("🌍 换国家地标图片")] }),
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "找到 countries: { 里的国家，比如：", font: "Arial", size: 22 })] }),
      new Paragraph({
        spacing: { before: 60, after: 60 }, indent: { left: 720 },
        shading: { fill: "F0F0F0", type: ShadingType.CLEAR },
        children: [new TextRun({ text: "'country-sa': { name: '沙特阿拉伯', flag: '🇸🇦', image: 'https://...' }", font: "Consolas", size: 18 })]
      }),
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "只改 ", font: "Arial", size: 22 }),
        new TextRun({ text: "image:", font: "Consolas", size: 22, bold: true }),
        new TextRun({ text: " 后面的链接即可。", font: "Arial", size: 22 })] }),

      // 3.4 Phone
      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("📞 改联系电话")] }),
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "找到：", font: "Arial", size: 22 })] }),
      new Paragraph({
        spacing: { before: 60, after: 60 }, indent: { left: 720 },
        shading: { fill: "F0F0F0", type: ShadingType.CLEAR },
        children: [new TextRun({ text: "phone: '400-xxx-xxxx',", font: "Consolas", size: 20 })]
      }),
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "改成你的号码。", font: "Arial", size: 22 })] }),

      // 3.5 QR code
      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("📱 换微信二维码")] }),
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "找到：", font: "Arial", size: 22 })] }),
      new Paragraph({
        spacing: { before: 60, after: 60 }, indent: { left: 720 },
        shading: { fill: "F0F0F0", type: ShadingType.CLEAR },
        children: [new TextRun({ text: "wechatQR: 'base64,/9j/...很长一串...'", font: "Consolas", size: 18 })]
      }),
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "最简单的办法：把二维码图片上传到网上（比如图床），然后把链接贴过来：", font: "Arial", size: 22 })] }),
      new Paragraph({
        spacing: { before: 60, after: 60 }, indent: { left: 720 },
        shading: { fill: "F0F0F0", type: ShadingType.CLEAR },
        children: [new TextRun({ text: "wechatQR: 'https://xxx.com/your-qrcode.png',", font: "Consolas", size: 18, color: "C44536" })]
      }),

      // Step 4
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("第四步：保存并查看效果")] }),
      new Paragraph({ numbering: { reference: "numsteps", level: 0 },
        children: [new TextRun({ text: "在记事本按 ", font: "Arial", size: 22 }),
                   new TextRun({ text: "Ctrl + S", font: "Arial", size: 22, bold: true }),
                   new TextRun({ text: " 保存", font: "Arial", size: 22 })]
      }),
      new Paragraph({ numbering: { reference: "numsteps", level: 0 },
        children: [new TextRun({ text: "双击 silkroad-trade_v7_silk_poster.html 在浏览器打开", font: "Arial", size: 22 })]
      }),
      new Paragraph({ numbering: { reference: "numsteps", level: 0 },
        children: [new TextRun({ text: "看到新内容，大功告成！🎉", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        spacing: { before: 120, after: 80 },
        shading: { fill: "FFF3DC", type: ShadingType.CLEAR },
        children: [new TextRun({ text: "如果没变？", font: "Arial", size: 20, bold: true, color: "C8923E" }),
                   new TextRun({ text: " 在浏览器按 F5 刷新一下", font: "Arial", size: 20, color: "666666" })]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // ===== 3. 注意事项 =====
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("3. 三个绝对不能犯的错")] }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun({ text: "记住这三条，就不会改坏文件：", font: "Arial", size: 22 })]
      }),
      new Table({
        width: { size: 9026, type: WidthType.DXA },
        columnWidths: [4513, 4513],
        rows: warningRows
      }),

      // ===== 4. 常见问题 =====
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("4. 遇到问题怎么办？")] }),
      
      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("页面打不开？")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "确认文件后缀是 .html，不是 .txt", font: "Arial", size: 22 })]
      }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun({ text: "双击就会用浏览器打开，如果变成乱码，记事本保存时选编码 → UTF-8", font: "Arial", size: 22 })]
      }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("改坏了怎么办？")] }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "别慌！我有所有版本的备份（v3/v5/v6/v7），随时找我要就行。", font: "Arial", size: 22 })]
      }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("不确定能不能改？")] }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "截图发给我，我帮你看。随时问！😄", font: "Arial", size: 22 })]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // ===== APPENDIX: Config Area Reference =====
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("附录：配置区完整速查表")] }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "下表中「查找关键词」是在记事本里用 Ctrl+F 搜的内容，「修改内容」告诉你要改哪个值。", font: "Arial", size: 20, color: "666666" })]
      }),

      // Config reference table
      new Table({
        width: { size: 9026, type: WidthType.DXA },
        columnWidths: [2500, 2500, 4026],
        rows: [
          new TableRow({ children: [
            hcell("要改什么", 2500),
            hcell("查找关键词", 2500),
            hcell("修改内容", 4026)
          ]}),
          new TableRow({ children: [
            cell("公司名称", 2500, { size: 18 }),
            cell("companyName", 2500, { size: 18 }),
            cell("改双引号里的中文", 4026, { size: 18 })
          ]}),
          new TableRow({ children: [
            cell("联系电话", 2500, { size: 18 }),
            cell("phone:", 2500, { size: 18 }),
            cell("改引号里的号码", 4026, { size: 18 })
          ]}),
          new TableRow({ children: [
            cell("邮箱", 2500, { size: 18 }),
            cell("email:", 2500, { size: 18 }),
            cell("改引号里的邮箱", 4026, { size: 18 })
          ]}),
          new TableRow({ children: [
            cell("微信二维码", 2500, { size: 18 }),
            cell("wechatQR:", 2500, { size: 18 }),
            cell("替换成新二维码链接", 4026, { size: 18 })
          ]}),
          new TableRow({ children: [
            cell("轮播图1~7", 2500, { size: 18 }),
            cell("slides: [", 2500, { size: 18 }),
            cell("改每张的 img: 链接", 4026, { size: 18 })
          ]}),
          new TableRow({ children: [
            cell("国家1~18", 2500, { size: 18 }),
            cell("countries: {", 2500, { size: 18 }),
            cell("改每个国家的 image: 链接", 4026, { size: 18 })
          ]}),
          new TableRow({ children: [
            cell("客户案例", 2500, { size: 18 }),
            cell("cases: [", 2500, { size: 18 }),
            cell("改 name/text/comments", 4026, { size: 18 })
          ]}),
        ]
      }),

      // ===== Footer Note =====
      new Paragraph({
        spacing: { before: 400 },
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "--- 有任何问题，直接找我！😄🦞 ---", font: "Arial", size: 20, color: "999999", italics: true })]
      }),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("C:\\Users\\ASDCF\\.qclaw\\workspace\\丝路山海通v7_小白修改指南.docx", buffer);
  console.log("✅ Word 文档生成成功！");
});
