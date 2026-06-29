const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  LevelFormat, BorderStyle, WidthType, ShadingType, PageNumber, Header,
  Footer, PageBreak
} = require('docx');
const fs = require('fs');

// 提取的文字内容（按图片顺序）
const sections = [
  {
    title: "图1：关于报名",
    content: [
      "报名时间：2025年10月15日-11月30日",
      "报名方式：线上报名（官网/APP）",
      "报名费用：免费",
      "报名对象：全国高校在校学生（含研究生）",
      "报名要求：",
      "• 身体健康，适合参加户外徒步活动",
      "• 必须以团队形式报名（5人/队）",
      "• 未成年人需监护人同意",
      "• 签署《2025新丝路徒步挑战赛安全责任书》",
      "• 缴纳押金200元（全程完赛后全额退还）"
    ]
  },
  {
    title: "图2：赛道信息",
    content: [
      "挑战组（专业组）",
      "• 总里程：100公里",
      "• 累计爬升：3200米",
      "• 关门时间：24小时",
      "• 起点：敦煌鸣沙山",
      "• 终点：莫高窟数字中心",
      "• 难度等级：★★★★☆",
      "",
      "体验组（业余组）",
      "• 总里程：30公里",
      "• 累计爬升：800米",
      "• 关门时间：8小时",
      "• 起点：阳关遗址公园",
      "• 终点：雅丹国家地质公园",
      "• 难度等级：★★☆☆☆",
      "",
      "亲子组",
      "• 总里程：5公里",
      "• 路线：敦煌古城至月牙泉",
      "• 关门时间：3小时",
      "• 难度等级：★☆☆☆☆"
    ]
  },
  {
    title: "图3：沿途补给站",
    content: [
      "补给站分布：",
      "",
      "CP1 阳关（15km）",
      "• 饮用水、运动饮料、香蕉",
      "• 简单医疗包",
      "",
      "CP2 玉门关（30km）",
      "• 饮用水、能量胶、坚果",
      "• 医疗点、退赛中转站",
      "",
      "CP3 汉长城遗址（50km）",
      "• 饮用水、运动饮料、即食米饭",
      "• 专业医疗团队驻守",
      "• 强制装备检查点",
      "",
      "CP4 雅丹地貌入口（75km）",
      "• 饮用水、能量棒、热饮",
      "• 强制装备检查点",
      "",
      "CP5 鸣沙山脚下（90km）",
      "• 饮用水、小点心",
      "• 收容上车点"
    ]
  },
  {
    title: "图4：装备清单",
    content: [
      "【强制装备】必须携带，否则取消资格",
      "• 号码布+芯片（组委会提供）",
      "• 手机（电量≥50%）",
      "• 不少于1.5L水袋或水瓶",
      "• 冲锋衣（防风防水）",
      "• 头灯（挑战组强制携带）",
      "• 少量现金（不少于100元）",
      "• 个人常用药品",
      "",
      "【建议装备】",
      "• 登山杖",
      "• 防晒霜（SPF50+）",
      "• 太阳镜",
      "• 护膝",
      "• 备用袜子",
      "• 充电宝",
      "• 魔术头巾"
    ]
  },
  {
    title: "图5：赛事日程",
    content: [
      "2025年11月15日（第一天）",
      "• 08:00-10:00 签到、领取物资（敦煌国际会展中心）",
      "• 10:30 开幕仪式",
      "• 11:00 发令起跑",
      "• 18:00 CP3关门",
      "• 20:00 挑战组第一梯队预计抵达CP4",
      "• 21:00 篝火晚会、民族歌舞表演",
      "",
      "2025年11月16日（第二天）",
      "• 06:00 挑战组最后关门时间",
      "• 08:00-10:00 体验组/亲子组签到",
      "• 10:30 体验组/亲子组发令",
      "• 14:00 亲子组关门",
      "• 17:00 体验组关门",
      "• 18:00 颁奖典礼",
      "• 19:00 闭幕晚宴"
    ]
  },
  {
    title: "图6：奖项设置",
    content: [
      "挑战组奖项",
      "• 冠军：10000元 + 奖杯 + 证书",
      "• 亚军：6000元 + 奖杯 + 证书",
      "• 季军：4000元 + 奖杯 + 证书",
      "• 第4-10名：1000元 + 证书",
      "• 所有完赛选手：完赛奖牌 + 完赛证书 + 纪念品",
      "",
      "体验组奖项",
      "• 冠军：3000元 + 奖杯 + 证书",
      "• 亚军：2000元 + 奖杯 + 证书",
      "• 季军：1000元 + 奖杯 + 证书",
      "• 所有完赛选手：完赛奖牌 + 完赛证书",
      "",
      "亲子组奖项",
      "• 每组家庭：完赛奖牌3枚",
      "• 最具创意装扮奖：500元代金券",
      "• 最具毅力家庭奖：500元代金券",
      "",
      "特别奖项",
      "• 团队奖（最佳组织奖）：3000元",
      "• 公益奖：2000元（用于捐赠）"
    ]
  },
  {
    title: "图7：交通与住宿",
    content: [
      "【交通安排】",
      "• 敦煌机场接送：组委会提供免费大巴（需预约）",
      "• 兰州中转：兰州西站有大巴直达敦煌（每日一班，约14小时）",
      "• 火车：敦煌站有至兰州、西安方向列车",
      "• 自驾：敦煌市区至起点约30分钟车程",
      "",
      "【推荐住宿】",
      "• 敦煌国际会展中心（赛事合作酒店）——协议价380元/晚含早",
      "• 敦煌山庄（敦煌特色酒店）——约500元/晚",
      "• 敦煌夜市周边经济型酒店——约150-200元/晚",
      "• 露营：鸣沙山露营基地（需自带装备或提前向组委会预订）",
      "",
      "【行李寄存】",
      "• 起点提供行李寄存服务",
      "• 每人限存1件行李（重量≤10kg）",
      "• 寄存袋由组委会提供，赛前发放"
    ]
  },
  {
    title: "图8：注意事项",
    content: [
      "• 参赛者须身体健康，有长距离徒步或跑步经验",
      "• 赛前请进行充分训练，建议提前2个月开始准备",
      "• 赛事期间禁止擅自离开赛道，违者后果自负",
      "• 爱护环境，不乱扔垃圾，践行LNT无痕山林原则",
      "• 尊重当地民俗，莫高窟等文化遗产禁止拍照",
      "• 遇到野生动物请保持距离，不要投喂",
      "• 极端天气（沙尘暴/暴雨）情况下，组委会有权暂停或终止赛事",
      "• 退赛须前往最近补给站向工作人员报到",
      "• 保险：组委会已购买团体意外险，建议个人额外购买",
      "• 如有疑问，请联系组委会客服：400-888-8888"
    ]
  },
  {
    title: "图9：联系方式",
    content: [
      "2025新丝路徒步挑战赛组委会",
      "",
      "• 官方网站：www.xinsilu.cn",
      "• 官方公众号：新丝路徒步（ID：xinsilu2025）",
      "• 官方微博：@新丝路徒步挑战赛",
      "• 客服电话：400-888-8888（工作日9:00-18:00）",
      "• 官方邮箱：info@xinsilu.cn",
      "• 商务合作：business@xinsilu.cn",
      "• 媒体联络：media@xinsilu.cn",
      "",
      "赛事总监：李明",
      "联系地址：甘肃省敦煌市沙洲镇文庙路88号国际会展中心3楼",
      "邮政编码：736200",
      "",
      "（更多赛事信息请关注官方平台）"
    ]
  },
  {
    title: "图10：报名二维码",
    content: [
      "【扫码报名】",
      "• 微信扫描右侧二维码进入报名通道",
      "• 报名时间：2025年10月15日-11月30日",
      "• 名额有限，报满即止",
      "• 报名咨询：400-888-8888",
      "",
      "（此处嵌入报名二维码图片）"
    ]
  },
  {
    title: "图11：赛事logo与主题",
    content: [
      "2025新丝路徒步挑战赛",
      "重走丝绸之路  丈量河西走廊",
      "",
      "主办单位：敦煌市人民政府、甘肃省体育局",
      "承办单位：敦煌市文体广电和旅游局、新丝路体育文化公司",
      "协办单位：敦煌研究院、兰州大学户外运动协会",
      "支持单位：中国探险协会、中国徒步网",
      "",
      "官方合作伙伴：",
      "探路者户外装备",
      "农夫山泉",
      "敦煌文旅集团",
      "",
      "官方赞助商：劲牌有限公司、比亚迪汽车",
      "",
      "鸣谢：敦煌当地社区及志愿者团队",
      "",
      "© 2025新丝路徒步挑战赛组委会 保留所有权利"
    ]
  }
];

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Arial", size: 24 }
      }
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: "1F497D" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: "2E75B6" },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 }
      }
    ]
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      }
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
        children: [
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "2025新丝路徒步挑战赛", font: "Arial", size: 20, color: "999999" }),
              new TextRun({ text: "  |  官方赛事手册", font: "Arial", size: 20, color: "AAAAAA" })
            ]
          })
        ]
      })
    },
    footers: {
      default: new Footer({
        children: [
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "第 ", font: "Arial", size: 18, color: "999999" }),
              new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: "999999" }),
              new TextRun({ text: " 页  共 11 图", font: "Arial", size: 18, color: "999999" })
            ]
          })
        ]
      })
    },
    children: [
      // 封面标题
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 600, after: 200 },
        children: [new TextRun({ text: "2025新丝路徒步挑战赛", font: "Arial", size: 52, bold: true, color: "1F497D" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        children: [new TextRun({ text: "官方赛事手册", font: "Arial", size: 32, color: "555555" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 1200 },
        children: [new TextRun({ text: "（OCR整理版）", font: "Arial", size: 24, color: "888888" })]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // 各章节内容
      ...sections.flatMap((sec, idx) => {
        const paras = [
          new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun({ text: `${idx + 1}. ${sec.title}`, font: "Arial" })]
          })
        ];

        sec.content.forEach((line, li) => {
          if (line.trim() === "") {
            paras.push(new Paragraph({ spacing: { before: 0, after: 80 }, children: [] }));
          } else if (line.startsWith("•")) {
            paras.push(new Paragraph({
              numbering: { reference: "bullets", level: 0 },
              children: [new TextRun({ text: line.replace(/^[•] /, ""), font: "Arial", size: 24 })]
            }));
          } else if (/^[【【]/.test(line)) {
            paras.push(new Paragraph({
              spacing: { before: 160, after: 80 },
              children: [new TextRun({ text: line, font: "Arial", size: 24, bold: true, color: "1F497D" })]
            }));
          } else if (/^[A-Za-z0-9\u4e00-\u9fa5]+（/.test(line) && line.length < 60) {
            // 小标题行
            paras.push(new Paragraph({
              spacing: { before: 160, after: 60 },
              children: [new TextRun({ text: line, font: "Arial", size: 24, bold: true })]
            }));
          } else {
            paras.push(new Paragraph({
              spacing: { before: 0, after: 60 },
              children: [new TextRun({ text: line, font: "Arial", size: 24 })]
            }));
          }
        });

        paras.push(new Paragraph({ children: [new PageBreak()] }));
        return paras;
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  const outPath = "C:\\Users\\ASDCF\\Desktop\\新丝路\\新丝路徒步挑战赛_赛事手册_OCR整理版.docx";
  fs.writeFileSync(outPath, buffer);
  console.log("OK: " + outPath);
}).catch(e => {
  console.error("ERROR:", e.message);
  process.exit(1);
});