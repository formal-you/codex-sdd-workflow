# Codex SDD Workflow

This `SDD/` folder is the repository-local workflow workspace for Codex.

The root [`AGENTS.md`](../AGENTS.md) is the single operating contract for agents. This folder holds the durable state, docs, and helper commands that make the workflow resumable.

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

## Local Workflow Responsibilities

- `workflow.md`
  - workflow mechanics, folder roles, and delegation rules
- `docs/`
  - project brief, process summary, architecture, testing, git workflow, progress, audit
- `tasks/`
  - active tasks, archived history, and task index
- `templates/`
  - task, subtask, ADR, and evidence templates
- `adr/`
  - durable decisions
- `evidence/`
  - proof that the workflow was exercised
- `scripts/`
  - daily local workflow commands for this repo

## Suggested Flow

1. run `session-brief`
2. run `validate-sdd`
3. create or update a task card
4. for multi-part work, record the decomposition decision first; when parallel work is justified, create subtasks before implementation
5. archive completed work from `tasks/active/` into `tasks/history/`, then refresh `docs/process.md`
6. keep integration and final verification with the main agent
7. record evidence when validating the workflow itself

## Git Baseline

- bootstrap fills in a root `.gitignore` when one is missing
- for standalone projects, bootstrap initializes a local Git repository when it is safe to do so
- when the target lives inside a parent Git repository, bootstrap avoids silently creating a nested repo by default
