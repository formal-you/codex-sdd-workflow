# CI/CD

当 workflow 使用 `full` profile 时，请维护本文件。

## 目标

- 让 task 图谱和流水线现实保持一致
- 在本地 workflow 中记录合并前和发布前的检查项
- 把自动化 scaffolding 放进 repo，而不是散落在聊天记录里

## 基线

- 自动化说明放在 `../automation/`
- GitHub Actions 示例放在 `../automation/github-actions/ci.yml.example`
- release 卡片应明确链接需要通过的检查
- connector hook 可以引入外部 issue 上下文，但流水线 ownership 仍然归团队现有系统

## 合并前

1. 分支检查通过
2. task 验收标准满足
3. release 或 sprint 卡片已经记录延后风险

## 发布前

1. release 检查单是最新的
2. 回滚负责人和回滚命令是明确的
3. 如果变更影响用户，evidence 已经补齐

## External Source Boundary

- 使用 `../workflow-config.env` 中的 `EXTERNAL_ISSUE_SOURCE` 与 `CONNECTOR_MODE` 标记当前 repo 是否正在镜像外部规划系统
- 默认 connector 行为是 `pull-only`
- 一旦团队已经有正式交付平台，不要把 repo-local 的 backlog 或 release 记录误当成唯一真源
