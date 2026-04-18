# Task Cards

真实任务和模板不要混放。

## 目录结构

- `active/`
  - 当前 active task 与 subtask
- `history/`
  - 已完成或已归档的 task 与 subtask
- `../templates/tasks/`
  - `TASK-template.md`
  - `SUBTASK-template.md`

示例：

- `active/TASK-004-add-export-command.md`
- `active/SUBTASK-002-update-http-client.md`
- `history/TASK-001-fix-auth-timeout.md`

## 为什么需要这些文件

Task cards 让工作在以下场景中仍然可继续：

- session 重启
- 模型切换
- 主 agent 向 subagent handoff
- 实现到一半的中断状态

使用 `TASK-*.md` 表示 parent task，使用 `SUBTASK-*.md` 表示 delegated slice。parent task 需要记录拆分决策，并链接所有 active subtasks。

## 归档规则

- 仍在推进中的任务保留在 `active/`
- 已完成且不再作为当前焦点的任务移入 `history/`
- 归档后，把近期归档摘要更新到 `../docs/process.md`

## Full Profile 说明

当 workflow 使用 `full` profile 时，task card 还应链接：

- `../backlog/items/` 下的 backlog 条目
- `../sprints/active/` 下的 sprint 卡片
- 如果工作涉及发布，还应链接 `../releases/records/` 下的 release 卡片
