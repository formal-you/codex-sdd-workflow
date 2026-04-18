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

## 合并前

1. 分支检查通过
2. task 验收标准满足
3. release 或 sprint 卡片已经记录延后风险

## 发布前

1. release 检查单是最新的
2. 回滚负责人和回滚命令是明确的
3. 如果变更影响用户，evidence 已经补齐
