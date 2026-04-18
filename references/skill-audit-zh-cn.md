# 当前 Skill 正式审计稿

本文档评审的是当前仓库里的 `codex-sdd-workflow` skill 本身，而不是将来 bootstrap 到用户仓库中的 `workflow-audit.md` 模板。

## 审计元信息

- 日期：2026-04-18
- 审计人：Codex
- 目标版本或分支：当前工作区快照（审计收口时位于 `main` 分支）
- 目标对象：`codex-sdd-workflow` skill 当前实现
- 最近验证结果：
  - `reports/skill-validation.md`
- 目标受众：
  - `lite`: public release
  - `full`: beta users
- 已检查的 evidence：
  - commands：
    - `python scripts/bootstrap_sdd_pack.py --target <temp> --lang zh-cn --workflow-profile lite`
    - `python scripts/bootstrap_sdd_pack.py --target <temp> --lang zh-cn --workflow-profile full`
    - `python -m unittest discover -s tests -p "test_*.py" -v`
  - generated repos：
    - `lite` 与 `full` profile 均已实际 bootstrap 到临时目录，验证生成结构与 `workflow-config.env`
  - manual flows：
    - 检查 bootstrap 输出的 next steps
    - 检查 `full` profile 下 backlog、sprint、release、automation 目录和脚本是否实际生成
    - 审阅 `agile-delivery.md`、`ci-cd.md`、各 profile README 的操作约束
  - automated tests：
    - 当前完整 unittest 套件已通过，结果以 `reports/skill-validation.md` 的最近记录为准
    - 已覆盖 `--force`、`--force-root-shims`、`--sdd-dir`、`--no-root-shims`、`lite/full` profile、跨 shell handoff、validator 约束、skill metadata、references 路由、分发路径污染与报告模板

## 通用基线

| 维度 | 分数 | 备注 |
| --- | --- | --- |
| 跨 session 恢复 | 9.2 | 根 `AGENTS.md`、`docs/process.md`、task/subtask、handoff 模板与 session-brief 组成了稳定恢复面。 |
| 委派质量 | 8.9 | parent task 先行、subtask 显式化、主 agent 集成责任清晰，适合主 agent + 多 subagent。 |
| 多 subagent 就绪度 | 8.8 | workflow 契约已经把并行拆分条件、owned scope、集成责任写清楚，但仍停留在流程约束层。 |
| 跨 shell 可靠性 | 8.8 | PowerShell 与 shell 脚本均存在，且已有测试覆盖 handoff 与 validator；CRLF 解析问题已修复。 |
| Evidence 与可审计性 | 8.9 | task、ADR、evidence、audit、handoff、validate 形成了可回放链路。 |
| Git 协作基线 | 8.5 | git 上下文探测、`.gitignore` 初始化、repo-root handoff 范围已经稳固，但仍未打通 PR/审批系统。 |
| Token 效率潜力 | 9.1 | 通过本地 durable docs、task 图谱和脚本化入口，明显降低对聊天记忆的依赖。 |
| 自验证能力 | 8.9 | `validate-sdd`、`session-brief`、bootstrap 测试都比较成体系。 |
| Bootstrap 清晰度 | 8.7 | 引导命令、语言/stack/profile 选择清楚，且开始支持 `lite/full` 分流。 |
| 通用基线总体 | 8.9 | 作为“准确开发 + 主/多 SubAgent”工程执行 workflow，已经达到优秀档。 |

## Lite Profile 评审

### Lite 适配度

- 最适合的仓库类型：
  - 单服务仓库、工具仓库、脚手架仓库、SDK、小中型应用仓库
- 最适合的团队规模：
  - 1 到 3 人最佳；纪律较好的 4 到 5 人小团队也可用
- 什么情况下已经足够：
  - 目标是稳定执行、精确交付、主 agent + 多 subagent 协同，而不是完整项目管理平台
  - 变更以工程任务推进为主，release 节奏和 backlog 管理还不复杂
- 什么情况下开始显得不够：
  - 需要正式 backlog 分层、sprint 节奏、release 检查单、跨角色协作、上线前后操作基线时

### Lite 评分表

| 维度 | 分数 | 备注 |
| --- | --- | --- |
| 准确执行型 workflow | 9.4 | 这是当前实现最强的一档能力，任务驱动、验证驱动、handoff 驱动都很清楚。 |
| parent task / subtask 纪律 | 9.2 | 对拆分前置、subtask 链接、主 agent 集成都有明确约束。 |
| 低噪音与快速启动 | 9.5 | profile 轻，默认资产克制，适合直接进开发。 |
| 单人或小团队协作 | 8.5 | 共享 task/handoff/process 文档后，小团队协作已比较顺手。 |
| 项目渐进演化 | 8.6 | 通过 durable docs、ADR、history 归档支持长期演进，但还缺升级迁移工具。 |
| handoff 质量 | 8.9 | 已修复为 repo 级变更视角，handoff 价值明显提升。 |
| 轻量敏捷支持 | 7.4 | 有任务流和进度流，但没有 backlog/sprint/release 层。 |
| 对外采用准备度 | 8.5 | 对公共 skill 用户已经可用，行为边界也较可解释。 |
| Lite 总体 | 8.8 | 已可作为公开默认 profile。 |

### Lite 做得好的地方

1. 已经很好地支持“准确开发”与“主 agent + 多 subagent”工作模式，且职责边界清楚。
2. 本地 durable workflow artifacts 齐全，能显著降低 session 丢失、上下文飘移和口头约定失真。
3. 已开始把 branch/task 级热状态从共享 `progress.md` 中拆出，降低了多人或多分支协作时的共享热点。
4. 结构轻、启动快、约束明确，适合作为多数仓库的默认工程执行 workflow。

### Lite 缺口

1. 对多人敏捷协作的支持仍偏弱，缺 backlog、sprint、release 三层节奏管理。
2. 缺少 workflow 自身升级/迁移机制，目前更像“重新 bootstrap”而不是“增量演进”。
3. 与真实团队协作系统尚未打通，例如 issue tracker、PR 状态、审批人、发布环境信息都没有沉淀入口。

## Full Profile 评审

### Full 适配度

- 最适合的仓库类型：
  - 持续演进中的产品仓库、多人协作的业务仓库、需要发布节奏和交付节奏的中小型项目
- 最适合的团队规模：
  - 3 到 8 人最佳；更大团队需要接入外部项目管理与 CI 平台
- 在什么情况下值得引入这套额外流程：
  - 已经出现 backlog 堆积、迭代节奏管理、release 复盘、CI/CD 检查单等需求
  - 希望从工程执行 workflow 升级到“轻量敏捷管理套件 + 自动化 scaffolding”
- 在什么情况下会显得过重：
  - 个人原型、一次性交付、小脚本仓库、没有固定迭代节奏的探索性工作

### Full 评分表

| 维度 | 分数 | 备注 |
| --- | --- | --- |
| Backlog 管理支持 | 8.3 | 已有 backlog 目录、模板、脚本与链接规则，足以支撑基础条目管理。 |
| Sprint 规划支持 | 8.1 | sprint 卡片与 active/history 结构清晰，但仍偏文档驱动。 |
| Release 管理支持 | 8.2 | release 模板和检查单思路已具备，适合小团队治理。 |
| CI/CD scaffolding 实用性 | 7.5 | 已有 `automation/` 与 GitHub Actions 示例，但仍是 scaffolding，不是可直接接管流水线的平台。 |
| 多角色协作支持 | 7.6 | 已开始支持产品/研发/发布等角色的信息落点，但缺 reviewer、approver、owner 机制。 |
| 敏捷交付支持 | 7.9 | 形成了 backlog-sprint-task-release 的基本链路，但尚未闭环到速度、容量、缺陷流转。 |
| 从 lite 升级到 full 的平滑度 | 8.7 | profile 设计与 bootstrap 落地都比较顺，概念上连续。 |
| 使用清晰度 | 8.2 | 文档职责和目录语义清楚，用户能看懂为什么要维护这些 artifacts。 |
| Full 总体 | 8.1 | 已达到优秀“beta”档，但还不应宣称为完整敏捷管理 + CI/CD 自动编排平台。 |

### Full 做得好的地方

1. 已经把 backlog、sprint、release、automation 的基本 scaffolding 真正落到仓库里，而不是只停留在口头建议。
2. 能从 `lite` 平滑抬升到更完整的项目交付模型，且不破坏原有 task/subtask 主线。
3. 已经开始为外部 issue 系统预留 connector-first 的配置位和 stub entrypoints，方向比单纯扩本地文本面板更稳。
4. 对项目演进与多人协作的支持明显强于纯工程执行流，已经具备中小团队试用价值。

### Full 缺口

1. 当前是“管理 scaffolding + 文档化自动化入口”，不是“自动任务编排 + 真正 CI/CD 集成系统”。
2. 没有与 GitHub Issues、Jira、PR review、CI 状态、部署环境、发布审批形成双向同步。
3. 缺少团队级度量，例如 velocity、WIP、carry-over 统计、缺陷分类、发布失败复盘模板联动。

## 发布建议

- lite：
  - ship
  - 原因：
    - 当前 `lite` 已经足够支持准确开发、主 agent + 多 subagent、单人/小团队协作和项目渐进演化。
- full：
  - beta only
  - 原因：
    - 当前 `full` 已具备明确价值，但本质仍是优秀 scaffolding，不应过度承诺为完整敏捷管理与自动编排平台。

## 下一步动作

1. 为 `full` profile 增加团队级字段与模板约束，例如 owner、reviewer、release approver、environment、rollback owner。
2. 增加 workflow 升级/迁移命令，让已有仓库可以增量升级，而不是主要依赖 `--force` 重建。
3. 继续补测试与示例，覆盖 `full` profile 的 backlog -> sprint -> task -> release 最小闭环，并增加 CI 示例的可执行文档。

---

## 本次审计期间文档架构升级 (2026-04-18)

在本次审计中，对本仓库的入口文档 `README.md` 进行了彻底的重构和升级：

1. **大幅提升了阅读体验和转化率**：将原先技术说明书式的陈述，改为“痛点提问 + 产品价值 (9 大核心能力) + 使用画像”的叙述结构。
2. **具象化了生成内容**：补充了完整的 `SDD/` 工作区目录树结构图，明确展示了 `.md` 文件与文件夹的作用，以及任务、证据、记录之间的联动生命周期。
3. **补充了 AI 原生日常使用路径**：README 不再把脚本命令当成普通用户的主入口，而是改成“自然语言驱动 Codex，脚本作为底层 API”的叙述结构，填补了使用者“装完后下一步怎么协作”的空白阶段，并清楚区分首次接入与安全升级。
4. **规范了专业术语**：将生硬的机器翻译感词汇（如“下一步纪律”）更迭为更具温度且符合工程直觉的词汇（如“下一步指引”、“执行规范”），同时保持当前 unittest 套件与文档口径一致。

**审计结论变更**：“Bootstrap 清晰度”和对使用者的“使用引导”已有显著提升，下一步可开始增加演示用 GIF 图和实际 task 填好后的示例模板以进一步降低接入门槛。
