## 任务背景
用户之前安装的Codex CLI无法连接DeepSeek API，需要排查修复。

## 执行过程
1. 检查Codex配置，发现openai_base_url指向本地3688端口
2. 发现用户通过CCX Desktop做代理中转
3. 发现CCX代理(ccx-go)未运行，实际监听3000端口
4. 修复config.toml端口错误和auth.json key配置
5. 验证DeepSeek key有效但余额不足

## 关键结果
- config.toml改为http://127.0.0.1:3000/v1
- auth.json改为CCX代理的access key
- CCX代理已在3000端口正常运行
- 问题：DeepSeek余额不足（Insufficient Balance）

## 结论建议
代理和配置已修复，但需要用户在DeepSeek平台充值后才能正常使用对话功能。