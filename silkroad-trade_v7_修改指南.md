# 丝路山海通 v7 修改指南

## 文件：silkroad-trade_v7_silk_poster.html

---

## 如何修改内容

打开 HTML 文件后，**所有可修改内容都在 `<script>` 标签顶部的 `CONFIG` 配置区**，用 `// ==== ` 注释块包裹，一眼就能找到。

---

## 修改示例

### 1. 改公司名称

找到：
```js
companyName: "丝路山海通",
```
改成：
```js
companyName: "您的新公司名",
```

---

### 2. 换轮播图图片（7 张）

找到 `slides: [` 里面的 `img: '...'`，替换 URL 即可：

```js
{title:'乘丝路长风<span class="gold">通达全球</span>', subtitle: '...', img: 'https://新的图片链接.jpg', ...},
{title:'公司注册<span class="gold">资质办理</span>', img: 'https://新的图片链接.jpg', ...},
// ... 共 7 张
```

---

### 3. 换某个国家的地标图片

找到 `countries: {` 里的对应国家，改 `image` 值：

```js
'country-id': { name: '印度尼西亚', flag: '🇮🇩', image: 'https://新的链接', ... },
'country-sa': { name: '沙特阿拉伯', flag: '🇸🇦', image: 'https://新的链接', ... },
// ... 共 18 个国家
```

---

### 4. 改联系方式

```js
phone: '400-xxx-xxxx',       // 改成您的电话
email: 'contact@your-company.com',   // 改成您的邮箱
```

---

### 5. 换微信二维码

找到 `wechatQR: 'base64,...'`，替换成您自己的二维码图片（base64 或图片 URL）

---

## 不需要改动的部分

- `DETAIL_CONTENT` — 详情弹窗内容（会自动从 CONFIG 生成）
- 所有 CSS 样式
- 所有 JavaScript 功能（弹窗、轮播、滚动动画等）
- HTML 结构（导航、板块布局等）

这些都在"配置区下方"，标了 `// 下面代码不用动 🚫`

---

## 常见问题

**Q: 改了 CONFIG 但页面没变化？**
- 保存文件后刷新浏览器（F5）即可
- 注意不要删掉最后的 `}; // ← CONFIG 结束`

**Q: 图片不显示？**
- Unsplash 图片偶尔会失效，换个新的 Unsplash 链接即可
- 可去 unsplash.com 搜索关键词找合适的图片
