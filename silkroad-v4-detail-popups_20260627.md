# 丝路山海通 v4 详情弹窗版

## 目标
基于 v3 页面（silkroad-trade_v3_silk_poster.html），创建 v4 版本：**v3 的外形完全不动**，仅为每个板块卡片添加点击弹出详情弹窗功能，弹窗样式参考 silkroad-trade.html 的设计风格。

## 关键决策
1. **不覆盖 v3** — v4 是独立新文件，v3 完整保留
2. **外层 CSS 完全照搬 v3** — 背景、导航、网格、卡片样式零修改
3. **弹窗样式** — 采用 silkroad-trade.html 的元素：
   - dh-hero（深色背景标题区）
   - dh-intro（左边框引言）
   - dh-heading（下划线标题）
   - ◆ 菱形列表符号
   - detail-cta-bar（底部按钮栏）
4. **每个板块/卡片独立详情** — 所有卡片点击都弹出对应专属内容

## 文件
- v3: `silkroad-trade_v3_silk_poster.html`
- v4: `silkroad-trade_v4_silk_poster.html`（本次产出）
