# Task Cards

Do not mix templates and real work items.

## Layout

- `active/`
  - live tasks and subtasks
- `history/`
  - archived tasks and subtasks
- `../templates/tasks/`
  - `TASK-template.md`
  - `SUBTASK-template.md`

Examples:

- `active/TASK-004-add-export-command.md`
- `active/SUBTASK-002-update-http-client.md`
- `history/TASK-001-fix-auth-timeout.md`

## Why These Exist

Task cards let work survive:

- session restarts
- model changes
- main-agent to subagent handoff
- partial implementation states

Use `TASK-*.md` for parent tasks and `SUBTASK-*.md` for delegated slices. Parent tasks should record the decomposition decision and link the active subtasks.

## Archive Rule

- keep in-progress work in `active/`
- move completed work into `history/`
- after archiving, refresh the recent history summary in `../docs/process.md`

## Full Profile Note

When the workflow uses the `full` profile, task cards should also link:

- promoted backlog items under `../backlog/items/`
- active sprint cards under `../sprints/active/`
- release cards under `../releases/records/` when the work is shipping
