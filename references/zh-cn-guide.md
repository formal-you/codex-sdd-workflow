# Codex SDD Workflow 中文指南

这份文档承担中文完整使用指南与 onboarding 角色。它面向“准备在 existing repo 里初始化或升级 `codex-sdd-workflow`”的使用者。

## 这是什么

`codex-sdd-workflow` 是一个给 Codex 使用的 workflow skill。它不是只给出一段说明，而是会把一套 repo-local 的 durable workflow 生成到目标仓库里。

默认生成的核心 artifacts 包括：

- 根 `AGENTS.md`
- 根 `README.md`
- `SDD/workflow.md`
- `SDD/workflow-config.env`
- `SDD/docs/`
- `SDD/tasks/`
- `SDD/templates/`
- `SDD/adr/`
- `SDD/evidence/`
- `SDD/state/`
- `SDD/scripts/`

如果使用 `--workflow-profile full`，还会额外生成：

- `SDD/backlog/`
- `SDD/sprints/`
- `SDD/releases/`
- `SDD/automation/`
- `SDD/docs/agile-delivery.md`
- `SDD/docs/ci-cd.md`

## 它解决什么问题

这套 skill 主要解决这些 repo 级 workflow 问题：

1. 会话中断后，状态容易丢失
2. 主 agent 和 subagent 的任务边界不稳定
3. 多任务时缺少可恢复的 parent task / subtask 图谱
4. 只有聊天上下文，没有 repo-local durable docs
5. 工程执行、handoff、验证、git 协作缺少统一入口

## 什么时候用 lite，什么时候用 full

如果用户还没说明 operating model，应该先问：

- `lite`
  - 更适合准确执行、单人或小团队协作、低噪音工程流
- `full`
  - 更适合已经需要 backlog、sprint、release、CI/CD scaffolding 的仓库

默认建议：

- 没有明确敏捷管理需求时，优先 `lite`
- 已经有迭代节奏、发布节奏、多人协作管理需求时，再用 `full`

## 如何初始化

对大多数使用者来说，**更推荐的入口不是手动敲命令，而是直接用自然语言让 Codex 执行这件事**。例如：

```text
请使用 codex-sdd-workflow 给当前仓库初始化一套 SDD workflow，先预览将要写入的内容。
```

```text
这个仓库已经有旧版 SDD workflow，请帮我安全升级，不要覆盖根目录已有的 README 和 AGENTS。
```

```text
我不确定该用 lite 还是 full，请先帮我判断，再接入 workflow。
```

下面这些命令主要给两类人使用：

- 维护这个 skill 的维护者
- 明确想自己在终端直接调用 bootstrap 脚本的高级使用者

如果你是普通使用者，把这些命令理解为 **Codex 在后台会调用的底层入口** 就够了。

最稳的命令：

```sh
python scripts/bootstrap_sdd_pack.py --target /path/to/repo
```

先预演：

```sh
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --dry-run
```

上面这组例子默认按 Linux、macOS、WSL shell 来写。前提是你已经在这个 skill 目录下执行命令。  
如果是 Windows PowerShell，命令不变，只把 `/path/to/repo` 换成类似 `C:\path\to\repo` 的路径即可。

常见变体：

```sh
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --workflow-profile lite
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --workflow-profile full
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --sdd-dir Workflow
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --lang en
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --git-mode auto
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --no-root-shims
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --template-overlay /path/to/overlay
```

覆盖策略：

- `--force`
  - 只替换生成出来的 workflow 目录
- `--force --force-root-shims`
  - 同时允许重建根 `README.md` 和根 `AGENTS.md`
- `--no-root-shims`
  - 不生成根 shim，保留仓库原有根入口

## 初始化后怎么开始

默认情况下，更自然的工作方式是直接对 Codex 说：

- “给我一份当前项目状态与进度简报”
- “先帮我建一个 parent task，再开始实现”
- “帮我做验证留痕，然后归档这个任务”
- “我要下线了，帮我生成 handoff”

也就是说，**日常协作优先走自然语言入口，脚本是 Codex 在仓库内调用的确定性 API**。

如果你需要手动检查或调试，默认情况下再按下面顺序进入：

1. 阅读根 `AGENTS.md`
2. 阅读 `SDD/docs/process.md`
3. 阅读 `SDD/workflow.md`
4. 在 Linux、macOS、WSL shell 中先运行：

```sh
./SDD/scripts/session-brief.sh
./SDD/scripts/validate-sdd.sh --strict
./SDD/scripts/new-task.sh "Describe the next change"
```

如果你在 Windows PowerShell 中工作，对应命令是：

```powershell
./SDD/scripts/session-brief.ps1
./SDD/scripts/validate-sdd.ps1 -Strict
./SDD/scripts/new-task.ps1 "Describe the next change"
```

如果使用了 `--no-root-shims`，起点改为：

- `SDD/workflow.md`
- `SDD/docs/process.md`
- `SDD/docs/progress.md`

当任务适合并行拆分时，再创建 subtask：

```sh
./SDD/scripts/new-subtask.sh "tasks/active/TASK-001-parent.md" "实现某个独立切片"
```

已完成任务归档：

```sh
./SDD/scripts/archive-task.sh "tasks/active/TASK-001-parent.md"
```

PowerShell 对应命令分别是 `new-subtask.ps1` 与 `archive-task.ps1`。但对普通使用者来说，仍然优先建议直接让 Codex 去调用这些脚本，而不是自己记忆命令。

从这轮开始，repo-local workflow 还会生成 `SDD/state/`：

- `SDD/docs/progress.md`
  - 只保留共享、聚合后的恢复信号
- `SDD/state/hot/branches/`
  - 适合写 branch-local 便签
- `SDD/state/hot/tasks/`
  - 适合写 task-local 便签
- `SDD/state/history/`
  - 归档后仍值得保留的热状态记录

也就是说：**`progress.md` 负责共享恢复，`state/hot/` 负责局部高频便签**。

任务结束或归档前，必须留下一个下一步信号：

- `SDD/docs/progress.md` 里的“推荐的下一步明确动作”
- 使用 `full` 时的 backlog 条目
- 或者明确写出等待用户决策 / 项目已经终态的原因

状态类文档统一使用 Markdown checkbox：`[ ]` 表示未完成、待推进或待确认，`[x]` 表示已完成或已确认。

任务完成时，还必须处理 Git handoff：

- 遵循 `SDD/workflow-config.env` 中的 `TASK_COMPLETION_GIT_MODE`
- 默认 `manual` 模式下不要自动提交
- 记录 `commit status: 未提交`、未提交原因，以及推荐 commit message
- 只有 repo 配置与用户意图都允许时，主 agent 才执行 commit

如果你在 `full` profile 下使用外部 issue 系统，这轮生成的 `workflow-config.env` 还会包含：

- `EXTERNAL_ISSUE_SOURCE`
- `CONNECTOR_MODE`

默认值分别是 `none` 和 `pull-only`。这代表当前 workflow 采用 **connector-first** 设计：先 pull 外部上下文，不做双向回写。

## 主 Agent / SubAgent 工作模型

这套 skill 的核心约束是：

- 从 parent task 开始，而不是只靠聊天记忆
- 多任务或可拆分任务，要先评估并行
- owned scope 可分离时，优先先建 subtask，再实现
- 主 agent 负责最终集成、验证、handoff
- 如果当前会话策略不允许 `spawn_agent`，也要明确记录“已评估并行，但受限制未委派”

## 第一次使用的正常现象

刚初始化时，这些文件仍然是模板态：

- `SDD/docs/project-brief.md`
- `SDD/docs/process.md`
- `SDD/docs/progress.md`
- 审计模板

所以一开始：

- `session-brief` 可以运行，但内容还会比较空
- `validate-sdd` 会提示 placeholder 警告

这是正常的。先把第一批真实内容填进去，workflow 才会真正“活起来”。

## 继续阅读

- 如果你只要最短英文操作流，读 `quickstart.md`
- 如果你想看这个 skill 当前做得怎么样，读 `skill-audit-zh-cn.md`
- 如果你需要知道 references 目录怎么分工，读 `README.md`
