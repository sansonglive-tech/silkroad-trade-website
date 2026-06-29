# Codex CLI + CCX Desktop + DeepSeek API 修复记录

**时间**: 2026-06-16 11:53-12:05  
**问题**: Codex CLI 无法与 AI 对话

## 环境结构

用户通过 **CCX Desktop**（`C:\Program Files\CCX\CCX Desktop`）管理 API key，并跑一个本地代理（`ccx-go`），架构如下：

```
Codex CLI → http://127.0.0.1:3000/v1 (CCX 代理) → https://api.deepseek.com
```

## 发现的问题及修复

### 问题 1: CCX 代理未运行
`ccx-go` 进程没启动，端口 3000 没有服务。
- **修复**: 手动启动 `ccx-go.exe`，指向正确的配置路径。

### 问题 2: config.toml 端口错误
`openai_base_url` 写的是 `http://127.0.0.1:3688/v1`，但实际 CCX 代理监听的是 **3000 端口**。
- **修复**: 改为 `http://127.0.0.1:3000/v1`。

### 问题 3: auth.json 中 key 不对
`auth.json` 直接放了 DeepSeek API key，但 Codex 应该用 CCX 代理的 access key (`ccx-6cabb9e416265703`) 来认证到代理。
- **修复**: auth.json 改为 `{"OPENAI_API_KEY": "ccx-6cabb9e416265703"}`。

### 问题 4 (遗留): DeepSeek 余额不足
CCX 配置中先后出现 3 个 key：
- `sk-5bf2a...c0cb` → 无效（authentication_error）
- `sk-e351f...78e8b` → 无效
- `sk-19240...ba38c` → 有效但 **余额不足**（Insufficient Balance）

## 当前状态

- ✅ CCX 代理在 3000 端口正常运行
- ✅ config.toml 配置正确
- ✅ auth.json 配置正确
- ✅ CCX 内 DeepSeek key 有效但余额不足
