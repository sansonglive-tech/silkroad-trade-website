# 丝路山海通后台 → GitHub 发布修复

**时间**: 2026-06-29 16:23

## 问题
后台管理修改内容后，点击"发布到 GitHub"按钮推送到 `master` 分支，但 GitHub Pages 使用 `main` 分支部署，导致线上网站一直显示旧内容。

## 修复
1. **分支修正**: 将本地 `master` 分支内容强制推送到远程 `main` 分支
2. **代码修复**: 修改 `admin_server.py` 中的发布逻辑，从推送到 `master` 改为推送 `main`
3. **本地分支统一**: 创建本地 `main` 分支并跟踪远程 `origin/main`

## 当前状态
- 后台管理: `http://localhost:8080` | 用户名 `jackleework` | 密码 `999999`
- 预览: `http://localhost:8080/preview`
- 线上: `https://sansonglive-tech.github.io/silkroad-trade-website/`
- 备份: `C:\Users\ASDCF\.qclaw\workspace\backup_20260629_160916\`

## v7 源文件原则
- ✅ v6 源文件 `silkroad-trade_v6_silk_poster.html` 未做任何改动
- ✅ 所有修改通过后台 + INJECT_SCRIPT 动态注入实现
