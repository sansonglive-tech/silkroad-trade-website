# 丝路山海通 v7 — 添加 CONFIG 配置区并修复

## Objective
给 `silkroad-trade_v7_silk_poster.html` 添加顶部的 CONFIG 配置区，让不会编码的用户能通过简单修改配置区域来更换内容（公司名、图片、联系方式等）。同时修复 `<script>` 标签被修复脚本吃掉的问题。

## Key Changes

1. **新增 CONFIG 配置区** — 在 `<script>` 顶部，用 `// >>> 配置区 <<<` 注释块包裹
   - 公司基本信息：`companyName`, `phone`, `email`, `wechatQR`
   - 轮播图数据 7 张：`slides: [{title, subtitle, desc, img, detailId}, ...]`
   - 国家数据 18 个：`countries: { country-id: {name, flag, image, cities, intro, services}, ... }`
   - 客户案例 3 个：`cases: [{id, name, role, company, text, image, comments}, ...]`
   - 服务覆盖（服务卡片、流程、政策等数据）

2. **SLIDE_CONFIG / DETAIL_CONTENT 从 CONFIG 加载**
   - `const SLIDE_CONFIG = CONFIG.slides;`
   - `const DETAIL_CONTENT = { ... }` 保留硬编码（因为内容复杂，不适合自动生成）

3. **修复 `<script>` 标签** — 修复脚本把 `<script>` 标签替换成了 `\n` 文字导致 JS 无法执行

4. **修复内容完整性** — 验证了所有国家 18 个、轮播 7 张、客户案例 3 个、流程 4 步、政策 5 项、区域 4 个、关于我们全部完整

## Verification
- JS 花括号平衡：open=139, close=139 ✅
- CONFIG 花括号平衡：open=45, close=45 ✅
- 所有 42 个 DETAIL_CONTENT 入口齐全 ✅
- 预约弹窗、微信弹窗功能正常 ✅
- 配套写了《修改指南.md》给小白用户

## File
`silkroad-trade_v7_silk_poster.html` — 新增 CONFIG 配置区版本
`silkroad-trade_v7_修改指南.md` — 面向编码小白的修改教程
