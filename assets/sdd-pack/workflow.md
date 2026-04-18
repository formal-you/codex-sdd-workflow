# Workflow Guide

This `SDD/` folder is the durable workflow workspace for the repository.

The repository-level operating contract lives in the root [`AGENTS.md`](../AGENTS.md). Use this file for workflow mechanics, folder roles, and helper commands.

## Start Here

```sh
./SDD/scripts/session-brief.sh
./SDD/scripts/validate-sdd.sh --strict
./SDD/scripts/new-task.sh "Describe the next change"
```

```powershell
./SDD/scripts/session-brief.ps1
./SDD/scripts/validate-sdd.ps1 -Strict
./SDD/scripts/new-task.ps1 "Describe the next change"
```

## Folder Map

- `docs/`
  - durable project memory, process summary, testing guidance, git workflow, and audit notes
- `tasks/`
  - `active/` stores live tasks and subtasks, `history/` stores archived work
- `templates/`
  - the workflow template library; templates are physically separated from real artifacts
- `adr/`
  - `records/` stores real ADRs; templates live under `templates/adr/`
- `evidence/`
  - `records/` stores real evidence; templates live under `templates/evidence/`
- `scripts/`
  - local day-to-day workflow commands for this repo

## Main Agent Model

- read the root `AGENTS.md`, `docs/process.md`, current `progress.md`, active task, and linked subtasks
- decide whether work should stay local, split sequentially, or split in parallel
- record the decomposition decision in the parent task before implementation for multi-part work
- create subtasks before implementation when parallel work is justified
- delegate only when owned scopes are disjoint, integration stays local, and the active session permits subagents
- periodically archive completed work from `tasks/active/` into `tasks/history/`
- integrate changes, run final verification, update docs, and prepare git handoff

## Subagent Model

- own one narrow task or subtask
- stay inside the assigned scope
- report files changed, tests run, and remaining risks
- never take over final integration from the main agent

## Parallel Work Rules

- when the user gives multiple tasks, or one task naturally splits into multiple independently verifiable work units, evaluate parallel subtasks first
- use parallel subtasks only when file ownership can stay disjoint
- if the workflow expects delegation but session policy blocks `spawn_agent`, record that delegation was evaluated but not permitted
- keep a parent task card with the decomposition decision and links to each subtask
- keep integration ownership with the main agent

## Progress And Archiving

- `docs/process.md` is the long-lived process view for milestones, archiving rules, recent history, and key pointers
- `docs/progress.md` is the short-lived recovery note for current work, recent findings, and session handoff
- use `[ ]` for unfinished, pending, or unconfirmed items and `[x]` for completed or confirmed items in workflow status docs
- when a task or subtask is done and no longer active, move it from `tasks/active/` into `tasks/history/`
- before archiving, leave one next-step entry: a `recommended next step` entry in `docs/progress.md`, or a backlog item in the full profile
- if no recommendation is possible, record the waiting user decision or terminal reason in `docs/progress.md`
- after archiving, refresh the short archive notes in `docs/process.md`

## Git Workflow

Follow [`docs/git-workflow.md`](./docs/git-workflow.md) for branch naming, Conventional Commits, and PR readiness. During bootstrap, the pack also fills in `.gitignore` and initializes a local repo when the target is clearly a standalone project.
When a task is complete, follow `TASK_COMPLETION_GIT_MODE` from `workflow-config.env`: commit only when allowed, otherwise record the uncommitted reason and recommended commit message in the task handoff.
