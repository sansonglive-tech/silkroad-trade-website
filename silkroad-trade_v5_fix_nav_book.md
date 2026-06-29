# 丝路山海通 v5 — 导航按钮点击修复

## 修复内容
- 导航栏「立即预约」按钮 onclick 中 `\(` 乱码已修复为正常 `event.preventDefault();openBook();`
- 轮播图幻灯片点击弹出详情功能重写，从 `handleSlideClick` 改为基于 `mousedown/mouseup` 全局监听，解决点击一次不弹出详情、需要两次点击的问题

## 文件
`silkroad-trade_v5_silk_poster.html` — 未覆盖 v3
