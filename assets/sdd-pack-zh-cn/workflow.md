# Workflow 指南

本 `SDD/` 目录是 repo-local 的 durable workflow 工作区。

仓库级的工作契约位于根目录 [`AGENTS.md`](../AGENTS.md)。本文件负责说明 workflow 机制、目录职责和辅助命令。

## 从这里开始

```sh
./SDD/scripts/session-brief.sh
./SDD/scripts/validate-sdd.sh --strict
./SDD/scripts/new-task.sh "描述下一项变更"
```

```powershell
./SDD/scripts/session-brief.ps1
./SDD/scripts/validate-sdd.ps1 -Strict
./SDD/scripts/new-task.ps1 "描述下一项变更"
```

## 目录说明

- `docs/`
  - durable docs、流程摘要、测试指引、Git workflow 与 audit 记录
- `tasks/`
  - `active/` 存放当前 active task 与 subtask，`history/` 存放已归档任务
- `state/`
  - `hot/` 存放 branch-aware 或 task-aware 的热状态便签，`history/` 存放已退役的热状态记录
- `templates/`
  - workflow 模板库；模板与真实 artifact 分离
- `adr/`
  - `records/` 存放真实 ADR；模板位于 `templates/adr/`
- `evidence/`
  - `records/` 存放真实 evidence；模板位于 `templates/evidence/`
- `scripts/`
  - 当前仓库的本地日常 workflow 命令

## 主 Agent 模型

- 读取根 `AGENTS.md`、`docs/process.md`、当前 `progress.md`、active task 与关联 subtasks
- 决定工作是保持本地、串行拆分，还是并行拆分
- 对多任务或天然可拆任务，先在 parent task 中记录拆分判断
- 如果适合并行，优先先创建 subtasks，再进入实现
- 只有在 owned scope 可分离，且当前会话允许时才委派
- 定期评估 `tasks/active/` 中已完成的 task，把旧 task 归档到 `tasks/history/`
- 负责集成改动、运行最终验证、更新文档，并准备 Git handoff

## Subagent 模型

- 拥有一个 narrow-scope task 或 subtask
- 保持在分配的 scope 内工作
- 返回改动文件、测试结果与剩余风险
- 不接管最终集成职责

## 并行工作规则

- 当用户给出多个任务，或者一个任务可以自然拆成多个独立可验收的工作单元时，优先评估 parallel subtasks
- 只有在文件 ownership 可以保持分离时才使用 parallel subtasks
- 如果 workflow 期望委派，但会话策略不允许 `spawn_agent`，主 agent 仍要记录“已评估并行，但受会话策略限制未委派”
- parent task card 必须记录拆分决策，并链接所有 subtasks
- 最终集成 ownership 始终保留给主 agent

## 进度与归档规则

- `docs/process.md` 是长期项目视角，记录 milestone、归档规则、近期历史和目录指针
- `docs/progress.md` 是聚合热状态摘要与 Session Handoff，不承担 task board 或完整项目历史
- branch/task 级细节便签请维护在 `state/hot/`
- workflow 状态文档里，用 `[ ]` 表示未完成、待推进或待确认，用 `[x]` 表示已完成或已确认
- 当某个 task 或 subtask 已完成且不再活跃时，把它从 `tasks/active/` 移入 `tasks/history/`
- 归档前，必须留下一个 next-step entry：`docs/progress.md` 中的“推荐的下一步明确动作”，或 full profile 下的 backlog 条目
- 如果暂时无法推荐下一步，在 `docs/progress.md` 写清楚等待用户决策或终态原因
- 归档后，在 `docs/process.md` 中更新近期归档摘要，并退役不再需要的 task 级热状态记录

## Git Workflow

请遵循 [`docs/git-workflow.md`](./docs/git-workflow.md) 中的分支命名、Conventional Commits 与 PR 准备规则。初始化 workflow 时，pack 会在安全场景下自动补齐 `.gitignore`，并在目标目录本身尚未处于 Git 仓库中时初始化本地仓库。
任务完成后，遵循 `workflow-config.env` 中的 `TASK_COMPLETION_GIT_MODE`：只有策略允许时才提交，否则在 task handoff 中记录未提交原因和推荐 commit message。
