# 2026-06-27 14:00 — 页脚"关于我们"板块添加详情页

## 任务
用户截图显示页脚"关于我们"板块（公司介绍 / 联系咨询 / 加入我们）3 个链接点击后无反应。
要求：
1. 点击能跳转
2. 联系咨询显示联系方式：+8615701071176
3. 联系咨询显示地址：北京市东城区通正国际大厦615室
4. 其他内容先用模板

## 实施

### 1. 修改页脚链接（line 516）
把 3 个 `<a onclick="closeDetail()">` 改为触发 `openDetail()`：

```html
<div><h4>关于我们</h4>
  <a onclick="event.preventDefault();openDetail('about')">公司介绍</a>
  <a onclick="event.preventDefault();openDetail('about-contact')">联系咨询</a>
  <a onclick="event.preventDefault();openDetail('about-join')">加入我们</a>
</div>
```

### 2. 在 DETAIL_CONTENT 中新增 3 个条目（line 595-）

- **'about'** — 公司介绍
  - 定位：本地化服务集团、响应一带一路
  - 核心优势：400+ 海外员工、8+ 国家、14+ 服务中心、7 年经验
  - 服务网络：5 大区域（东南亚/中亚/中东/俄语区/欧洲）
  - 企业愿景：让企业出海不再难

- **'about-contact'** — 联系咨询
  - 联系方式：+86 157 0107 1176
  - 邮箱：service@silkroad-trade.com
  - 办公地址：北京市东城区通正国际大厦 615 室
  - 业务咨询：4 个业务部联系方式
  - 海外服务点：5 大区域站点

- **'about-join'** — 加入我们
  - 招聘岗位：6 个核心岗位
  - 岗位要求：5 项基础要求
  - 福利待遇：5 项福利
  - 投递方式：邮箱 hr@silkroad-trade.com + 电话 + 地址

## 验证
- ✅ JS 语法 OK
- ✅ 文件 82086 字节
- ✅ 3 个条目已插入 DETAIL_CONTENT
- ✅ 页脚 3 个链接已绑定 openDetail 调用

## 文件
- `C:\Users\ASDCF\.qclaw\workspace\silkroad-trade.html` (82086 bytes, modified)
