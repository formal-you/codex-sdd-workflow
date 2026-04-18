# Quickstart

Use this file for the shortest English path through bootstrap, refresh, and first-use flow.

## Bootstrap An Existing Repo

Run from this skill directory:

```sh
python scripts/bootstrap_sdd_pack.py --target /path/to/repo
```

Safer first pass:

```sh
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --dry-run
```

Choose the operating model explicitly when needed:

```sh
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --workflow-profile lite
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --workflow-profile full
```

- `lite` keeps the workflow centered on execution, validation, task cards, and handoff
- `full` adds backlog, sprint, release, and CI/CD scaffolding

Useful variants:

```sh
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --sdd-dir Workflow
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --lang en
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --git-mode auto
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --no-root-shims
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --template-overlay /path/to/overlay
```

These examples are written for Linux, macOS, or WSL shells. In Windows PowerShell, use the same CLI flags with a Windows path such as `C:\path\to\repo`.

## Refresh An Existing Workflow

Replace only the generated workflow directory:

```sh
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --force
```

Replace root shims only when the user explicitly wants that too:

```sh
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --force --force-root-shims
```

## First Commands In The Target Repo

When root shims are enabled:

1. read `AGENTS.md`
2. read `SDD/docs/process.md`
3. read `SDD/workflow.md`

Then run:

```sh
./SDD/scripts/session-brief.sh
./SDD/scripts/validate-sdd.sh --strict
./SDD/scripts/new-task.sh "Describe the next change"
```

PowerShell equivalents:

```powershell
./SDD/scripts/session-brief.ps1
./SDD/scripts/validate-sdd.ps1 -Strict
./SDD/scripts/new-task.ps1 "Describe the next change"
```

When `--no-root-shims` was used, start from `SDD/workflow.md` and `SDD/docs/process.md` instead.

## What To Maintain

Always fill these first:

- `SDD/docs/project-brief.md`
- `SDD/docs/process.md`
- `SDD/docs/progress.md`
- `SDD/state/README.md`
- the first real task card

Keep shared recovery state in `SDD/docs/progress.md`. Keep branch-local or task-local scratch notes under `SDD/state/hot/`.

Before finishing or archiving a task, leave one next-step signal:

- a `recommended next step` entry in `SDD/docs/progress.md`
- a backlog item when using `full`
- or a clear waiting user decision / terminal reason

Use `[ ]` for unfinished, pending, or unconfirmed items. Use `[x]` for completed or confirmed items.

Before closing a completed task, also close the Git loop:

- follow `TASK_COMPLETION_GIT_MODE` in `SDD/workflow-config.env`
- with the default `manual` mode, do not commit automatically
- record `commit status: not committed`, the uncommitted reason, and a recommended commit message
- only commit when the repo config and user intent allow it

When `full` is used, also maintain:

- `SDD/docs/agile-delivery.md`
- `SDD/docs/ci-cd.md`
- backlog, sprint, and release records
- connector boundary notes in `SDD/workflow-config.env` when external issue systems exist

## Read Next

- use `zh-cn-guide.md` for the fuller Chinese onboarding guide
- use `README.md` in this folder for the reference map
- use `skill-audit.md` when reviewing the current skill itself
