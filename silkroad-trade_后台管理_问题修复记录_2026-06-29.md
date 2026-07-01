# 问题修复：后台修改后网页不同步

## 问题
后台管理页面修改内容 → 保存 → 发布后，网页（GitHub Pages）不更新。

## 根因
GitHub 仓库有两个分支：
- `master`（本地默认分支，后台推送的目标）
- `main`（GitHub Pages 部署的目标）

后台 `publish_to_github` 推送到 `origin master`，但 GitHub Pages 配置的是 `main` 分支，导致推送了但网页不更新。

## 修复
在推送时指定目标分支：`git push origin master:main`（使用 `--force` 确保覆盖）

## 后续建议
修改 `admin_server.py` 中的 `publish_to_github` 函数，将 git push 命令改为推送到 main 分支。
