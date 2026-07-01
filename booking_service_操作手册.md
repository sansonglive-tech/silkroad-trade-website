# 预约记录服务 -- 操作手册

## 新建文件清单（全独立，不碰任何原文件）

| 文件 | 作用 |
|------|------|
| `booking_server.py` | 预约记录服务（端口8081） |
| `booking_admin.html` | 预约管理后台页面 |
| `booking_data.json` | 预约数据存储（自动生成） |

## 如何使用

### 1. 启动预约服务

在 PowerShell 中运行：

```powershell
python3 booking_server.py
```

看到输出：
```
  +----------------------------------------+
  |   Silkroad Booking Service             |
  |   Independent - no files modified      |
  +----------------------------------------+

  >> Admin:   http://localhost:8081/admin
  >> Submit:  http://localhost:8081/api/booking
  >> Hook:    http://localhost:8081/booking_hook.js
```

### 2. 后台管理预约记录

在浏览器打开：**http://localhost:8081/admin**

功能：
- 查看所有预约记录（姓名/手机号/意向国家/提交时间）
- 搜索过滤（按姓名、手机号、国家搜索）
- 标记已处理 / 删除记录
- 自动每30秒刷新
- 统计卡片（总预约 / 今日新增 / 待处理）

### 3. 让前台网页的预约生效

当前 v7 网页已经有预约弹窗（姓名+手机号+意向国家），但 `submitBook()` 目前只是 `alert()` 不保存数据。

**让提交按钮指向预约服务的方法：**

#### 方法 A：在网页末尾加一行 script 引用

在网页的 `<script>` 标签最后，加上：

```html
<script src="http://localhost:8081/booking_hook.js"></script>
```

这会自动替换 `submitBook()` 函数，让提交的数据发到预约服务保存下来。

#### 方法 B：直接替换 submitBook 函数

把现有 `submitBook()` 函数中 `alert('预约已提交')` 的部分替换成 AJAX POST 发送即可。


### 4. 数据文件

所有预约数据保存在 `booking_data.json`，格式示例：

```json
[
  {
    "id": 1782874438604,
    "name": "张三",
    "phone": "13800138000",
    "country": "哈萨克斯坦",
    "created_at": "2026-07-01 10:53:58",
    "status": "new"
  }
]
```

### 5. API 接口

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/admin` | 预约管理后台 |
| GET | `/api/bookings` | 获取所有预约（最新在前） |
| POST | `/api/booking` | 提交预约 `{name, phone, country}` |
| POST | `/api/booking/update` | 更新状态 `{id, status}` |
| POST | `/api/booking/delete` | 删除 `{id}` |
| GET | `/booking_hook.js` | 前端Hook脚本 |

### 6. 同时运行两个服务

两个服务独立运行，不冲突：

```
终端1: python3 admin_server.py   # 原后台 :8080
终端2: python3 booking_server.py  # 预约服务 :8081
```

### 7. 回滚方法

如果出问题，所有原文件都在备份目录中：

```powershell
Copy-Item "backup_20260701_1044_完整备份\admin_server.py" "admin_server.py"
Copy-Item "backup_20260701_1044_完整备份\site_config.json" "site_config.json"
Copy-Item "backup_20260701_1044_完整备份\silkroad-trade_v7_silk_poster.html" "silkroad-trade_v7_silk_poster.html"
```

新建的预约文件删掉即可：
```powershell
Remove-Item booking_server.py, booking_admin.html, booking_data.json
```
