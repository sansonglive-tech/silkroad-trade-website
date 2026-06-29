# 丝路山海通 v4 — 详情弹窗内容升级

## Objective
将 `silkroad-trade_v4_silk_poster.html` 中所有区块点击弹出的 DETAIL_CONTENT 从简单文字段落升级为富内容格式（含 Hero Banner、简介、分段列表+菱形符号、数据格子、CTA 操作栏），同时保持 v3 主页面外观不动。

## Key Changes

1. **DETAIL_CONTENT 数据重构** — 所有 28 个入口从 `{title, subtitle, content: '<h4>...<p>...'}` 改为 **dh-hero 头部 + dh-intro 简介 + dh-heading 分段标题 + ul列表 + 可选 detail-grid 数据卡 + detail-cta-bar 操作按钮**

2. **CSS 新增样式**：
   - `.dh-hero` / `.dh-hero-code` / `.dh-hero-overlay` — 弹窗顶部代码风 banner
   - `.dh-intro` — 简介段落
   - `.dh-heading` — 带❖符号的分段标题
   - `.detail-list` / `.detail-list li` — 菱形标记列表
   - `.detail-cta-bar` — 底部操作按钮栏
   - 响应式 `@media(max-width:768px)` 新增 `.dh-hero{height:140px}` 等覆盖

3. **文件大小**：v3 = 63KB → v4 = 83KB（内容大幅丰富）

## Coverage

| 入口类型 | 数量 | 入口 ID |
|---------|------|---------|
| 幻灯片服务 | 7 | company-advantage, company-reg, tax-legal, certification, local-ops, visa, factory |
| 服务卡片 | 1 | policy-overview（4 张卡片共享） |
| 服务流程 | 1 | service-process |
| 客户案例 | 1 | client-cases |
| 关于我们 | 1 | about |
| 区域概览 | 4 | region-sea, region-ru, region-me, region-eu |
| 国家详情 | 13 | country-id/vn/ph/th/sg/kz/uz/kg/tj/ru/ae/sa/eg/ng/ke/de/nl/pl |

## File
`silkroad-trade_v4_silk_poster.html` — 新文件，未覆盖 v3
