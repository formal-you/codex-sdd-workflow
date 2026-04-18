# SDD Scripts

这些生成出来的脚本是当前仓库的本地日常 workflow 入口。skill 负责安装和升级；真正的日常使用发生在这里。

## 已包含的辅助命令

- `new-task.ps1` / `new-task.sh`
  - 根据 `../templates/tasks/TASK-template.md` 在 `../tasks/active/` 创建下一个编号的 parent task
- `new-subtask.ps1` / `new-subtask.sh`
  - 根据 `../templates/tasks/SUBTASK-template.md` 在 `../tasks/active/` 创建下一个编号的 subtask
- `new-adr.ps1` / `new-adr.sh`
  - 根据 `../templates/adr/ADR-000-template.md` 在 `../adr/records/` 创建下一个编号的 ADR
- `archive-task.ps1` / `archive-task.sh`
  - 把已完成 task 或 subtask 从 `../tasks/active/` 归档到 `../tasks/history/`
- `session-brief.ps1` / `session-brief.sh`
  - 打印紧凑的启动摘要，包含 `process.md`、`progress.md`、git 状态与 active/history 摘要
- `handoff-template.ps1` / `handoff-template.sh`
  - 为 `../docs/progress.md` 打印 Markdown handoff 模板
- `validate-sdd.ps1` / `validate-sdd.sh`
  - 检查 workflow 的核心结构、占位内容和并行 task wiring 是否完整

如果 workflow 使用 `--workflow-profile full` 生成，scripts 目录还会包含：

- `new-backlog-item.ps1` / `new-backlog-item.sh`
- `new-sprint.ps1` / `new-sprint.sh`
- `new-release.ps1` / `new-release.sh`

## 示例

### shell

```sh
./SDD/scripts/session-brief.sh
./SDD/scripts/new-task.sh "为 OCR 导入增加重试"
./SDD/scripts/new-subtask.sh "tasks/active/TASK-003-add-retry-handling.md" "更新 worker 的重试策略"
./SDD/scripts/new-adr.sh "采用 gopls MCP 进行 Go 开发"
./SDD/scripts/archive-task.sh "tasks/active/TASK-003-add-retry-handling.md"
./SDD/scripts/handoff-template.sh --task "tasks/active/TASK-003-add-retry-handling.md"
./SDD/scripts/validate-sdd.sh
```

### PowerShell

```powershell
./SDD/scripts/session-brief.ps1
./SDD/scripts/new-task.ps1 "为 OCR 导入增加重试"
./SDD/scripts/new-subtask.ps1 "tasks/active/TASK-003-add-retry-handling.md" "更新 worker 的重试策略"
./SDD/scripts/new-adr.ps1 "采用 gopls MCP 进行 Go 开发"
./SDD/scripts/archive-task.ps1 "tasks/active/TASK-003-add-retry-handling.md"
./SDD/scripts/handoff-template.ps1 -CurrentTask "tasks/active/TASK-003-add-retry-handling.md"
./SDD/scripts/validate-sdd.ps1
```

## 设计说明

- 这些脚本只会写入当前仓库的 `SDD/` 目录。
- 命名和编号是确定性的。
- `new-task.*`、`new-subtask.*` 和 `new-adr.*` 支持 dry-run。
- `handoff-template.*` 只打印输出，不会自动改文档，便于 agent 审核后再贴进去。
- `validate-sdd.*` 采取保守策略：缺结构时硬失败，占位内容和 wiring 问题给警告。
