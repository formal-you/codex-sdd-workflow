# Codex SDD Workflow

本 `SDD/` 目录是当前 repo 给 Codex 使用的 repo-local workflow 工作区。

根目录下的 [`AGENTS.md`](../AGENTS.md) 是唯一稳定的 agent contract。这里保存让 workflow 可恢复、可委派、可审计的状态、文档和本地脚本。

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

## 本地 Workflow 职责

- `workflow.md`
  - workflow 机制、目录职责和委派规则
- `docs/`
  - 项目简介、流程摘要、架构、测试、Git workflow、进度和 audit
- `tasks/`
  - active task、历史归档与任务索引
- `templates/`
  - task、subtask、ADR 和 evidence 的模板
- `adr/`
  - 已采用的持久化技术决策
- `evidence/`
  - workflow 被真实运行过的 evidence
- `scripts/`
  - 当前仓库的日常本地 workflow 命令

## 建议流程

1. 运行 `session-brief`
2. 运行 `validate-sdd`
3. 创建或更新 task card
4. 多任务或天然可拆任务先写拆分判断；如果适合并行，先创建 subtasks，再进入实现
5. 已完成的 task 从 `tasks/active/` 归档到 `tasks/history/`，并把长期摘要写入 `docs/process.md`
6. 保持最终集成和验证由主 agent 负责
7. 验证 workflow 本身时补 evidence

## Git 基线

- bootstrap 会优先补齐仓库根目录的 `.gitignore`
- 对独立项目，bootstrap 会在安全场景下初始化本地 Git 仓库
- 如果目录位于父 Git 仓库内部，默认不会静默创建嵌套仓库
