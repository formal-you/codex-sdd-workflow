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
- `state/`
  - `hot/` stores branch-aware or task-aware scratch notes, `history/` stores retired hot-state notes
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
- `docs/progress.md` is the aggregate hot-state summary for current work, recent findings, and shared session handoff
- detailed branch or task scratch notes belong in `state/hot/`
- use `[ ]` for unfinished, pending, or unconfirmed items and `[x]` for completed or confirmed items in workflow status docs
- when a task or subtask is done and no longer active, move it from `tasks/active/` into `tasks/history/`
- before archiving, leave one next-step entry: a `recommended next step` entry in `docs/progress.md`, or a backlog item in the full profile
- if no recommendation is possible, record the waiting user decision or terminal reason in `docs/progress.md`
- after archiving, refresh the short archive notes in `docs/process.md` and retire any task-local hot-state note that is no longer needed

## Session Decay And Checkpoints

- Do not keep the current goal, completed work, remaining work, next action, risks, changed files, or validation status only in chat memory.
- Before long or risky work continues, update the active task, `docs/progress.md`, or a relevant `state/hot/` note with a checkpoint.
- Create a checkpoint when task scope grows, the session is long, memory is fuzzy, critical implementation or commit work is next, subtasks are about to be delegated, or context compression/recovery has happened.
- A checkpoint must record: true goal, completed work, remaining work, next concrete action, risks or blockers, and latest validation status.
- If the UI exposes a context meter and it reaches or exceeds 29%, write the checkpoint first, then ask the user whether to compact context or switch to a new session.
- After compression or resume, use the summary only as navigation. Re-read `AGENTS.md`, `docs/progress.md`, the active task, relevant hot-state notes, and `git status --short` before continuing.

## Git Workflow

Follow [`docs/git-workflow.md`](./docs/git-workflow.md) for branch naming, Conventional Commits, and PR readiness. During bootstrap, the pack also fills in `.gitignore` and initializes a local repo when the target is clearly a standalone project.
When a task is complete, follow `TASK_COMPLETION_GIT_MODE` from `workflow-config.env`: commit only when allowed, otherwise record `commit status: not committed` and a recommended commit message in the task handoff.
