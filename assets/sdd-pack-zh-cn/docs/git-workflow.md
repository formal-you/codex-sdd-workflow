# Git Workflow

## 分支命名

如果当前 repo 由 `codex-sdd-workflow` bootstrap 或升级，请先确认 Git 边界：

1. 目标目录不在任何 Git repo 内时，bootstrap 默认会初始化本地 repo
2. 目标目录位于父级 Git repo 中时，bootstrap 默认沿用父 repo 边界，不静默创建 nested repo
3. 目标目录缺少 `.gitignore` 时，bootstrap 会根据 `--stack` 生成基础模板

这样可以同时覆盖新项目和 existing repo，避免把 workflow 安装到不符合 Git 边界的位置。

分支名应短小、可读，并带有明确的意图前缀：

- `feat/<scope>-<slug>`
- `fix/<scope>-<slug>`
- `chore/<scope>-<slug>`

示例：

- `feat/auth-refresh-token`
- `fix/orders-timeout`
- `chore/sdd-refresh`

## Commit Message

使用 Conventional Commits：

- `feat: add retry backoff for import worker`
- `fix(api): handle empty tenant id`
- `docs(sdd): record workflow audit findings`
- `chore: refresh generated workflow helpers`

摘要行建议使用祈使句；在不影响可读性的前提下，尽量控制在约 72 个字符以内。

## Task Completion Git Handoff

任务完成并通过验证后，先从 `workflow-config.env` 读取 `TASK_COMPLETION_GIT_MODE`，再决定是否提交。

- `manual`：默认不提交。任务完成时，记录 `commit status: 未提交` 与推荐 commit message。
- `auto`：只有在测试通过、git scope 清楚、且不会夹带无关用户改动时，主 agent 才可以提交。

Subagent 不负责最终提交。只要使用了 subtasks，最终集成和 Git handoff 都由主 agent 负责。

## PR Handoff Check

发起 PR 或 handoff 给 reviewer 前，请确认：

1. task card 和 subtasks 准确覆盖本次实现范围
2. 相关测试或检查结果已经记录
3. 风险、后续事项和文档更新已经说明
4. task card 已记录本次工作是否提交；如未提交，至少保留 `commit status: 未提交` 与推荐 commit message
5. 当前分支和提交历史已经达到可评审状态
6. 如果使用了 subtasks，主 agent 已说明这些结果如何合入主线

## Agent 执行要求

- 在开始和结束前都检查 `git status --short`
- 不要重写与当前任务无关的用户改动
- 只要用了 subtasks，最终集成提交必须由主 agent 负责
