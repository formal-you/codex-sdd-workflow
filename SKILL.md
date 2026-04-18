---
name: codex-sdd-workflow
description: Bootstrap or upgrade a durable Codex workflow inside an existing repository, with task graphs, handoff docs, branch/task hot-state notes, local repo scripts, optional template overlays, and lite or full operating models. Use when Codex needs to initialize or refresh repo-local workflow scaffolding for session recovery, durable docs, parent tasks, subtasks, git collaboration rules, agile delivery scaffolding, connector hooks, or CI/CD-oriented workflow structure.
---

# Codex SDD Workflow

## Overview

Use this skill to install or refresh a repo-local workflow that survives session loss and keeps daily execution inside the repository.

Core working rules:

- treat the generated root `AGENTS.md` as the stable agent contract when root shims are enabled
- create a parent task before implementation
- evaluate decomposition before coding when multiple independent work units exist
- create subtasks before implementation when parallel work is justified
- keep templates separate from generated artifacts
- keep live work in `tasks/active/`, archive finished work in `tasks/history/`, and update `docs/process.md`
- keep shared recovery state in `docs/progress.md`, and keep branch-local or task-local scratch notes in `state/hot/`
- before finishing or archiving work, leave a next-step entry so the next session can continue with direction, not just state
- before closing completed work, follow the generated repo's Git completion mode and either commit or record why it is not committed

## Bootstrapping Rule

Run the bootstrap script from this skill directory:

```sh
python scripts/bootstrap_sdd_pack.py --target /path/to/repo
```

Safer first pass:

```sh
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --dry-run
```

Use POSIX-style paths in examples by default so the entrypoint reads naturally in Linux, macOS, or WSL shells. When guiding a Windows PowerShell user, replace `/path/to/repo` with the matching Windows path.

Use `--force` only when the user explicitly wants to replace an existing generated workflow directory. Add `--force-root-shims` only when they also explicitly want to replace root `README.md` and `AGENTS.md`.

Use `--no-root-shims` only when the repo should keep its own root contract. In that mode, startup begins from `SDD/workflow.md` and `SDD/docs/process.md`.

Do not explain every CLI variant inline here. Route detailed command choices to the references below.

Use `--template-overlay /path/to/overlay` only when the user explicitly wants organization-specific template customization. Overlays must preserve the generated workflow parser contract.

## Profile Choice Rule

Before bootstrapping, if the user has not already picked an operating model, ask them to choose one of:

- `lite`: focused engineering execution with durable docs, task cards, validation, and handoff
- `full`: adds backlog, sprint, release, connector hooks, and CI/CD scaffolding on top of the execution workflow

Default to `lite` when the user has not said they want broader agile or delivery management structure.

## Next-Step Discipline

Before marking a task or subtask done, or before archiving it, ensure one of these exists:

- a new active task under `tasks/active/`
- a `recommended next step` entry in `docs/progress.md`
- a backlog item when the generated workflow uses the `full` profile

If no recommendation is possible, record the waiting user decision, candidate options, and the recommended default in `docs/progress.md`.

Use Markdown checkbox semantics in generated workflow docs: `[ ]` means unfinished, pending, or unconfirmed; `[x]` means completed or confirmed.

## Hot-State Discipline

Keep `docs/progress.md` as the shared aggregate recovery note. Put high-frequency branch or task scratch notes under `state/hot/` so multi-branch work does not turn `progress.md` into a merge hotspot.

When archiving a task, retire or summarize any matching task-local hot-state note.

## Git Completion Closure

When a task is complete and verification passed, follow `TASK_COMPLETION_GIT_MODE` in the generated `workflow-config.env`:

- `manual`: do not commit by default; record the uncommitted reason and recommended commit message
- `auto`: the main agent may commit only after scope, tests, and user changes are clear

Subagents never own the final commit. When subtasks are used, the main agent owns integration and Git closure.

## Full Profile Boundary

Treat `full` as repo-local agile delivery scaffolding, not as the only source of truth for planning.

When a team already uses GitHub Issues, Jira, Linear, or another tracker, use the generated connector hooks as pull-first context entrypoints. Do not promise bidirectional synchronization unless a later implementation explicitly adds it.

## Reference Routing

Read the minimum reference needed for the job:

- `references/quickstart.md`
  - read for concise English bootstrap, upgrade, and command flow
- `references/zh-cn-guide.md`
  - read for the fuller Chinese guide, onboarding flow, and profile-selection explanation
- `references/skill-audit-zh-cn.md`
  - read when evaluating the current skill in Chinese
- `references/skill-audit.md`
  - read when evaluating the current skill in English

`references/README.md` and `scripts/README.md` are maintainer maps. Do not load them for ordinary bootstrap, refresh, or first-use tasks.

After bootstrapping, guide the user into the generated workflow instead of stopping at the installer:

1. read root `AGENTS.md` when root shims are enabled
2. read `SDD/docs/process.md`
3. read `SDD/workflow.md`
4. run `./SDD/scripts/session-brief.sh` in Linux or macOS shells, or `./SDD/scripts/session-brief.ps1` in PowerShell
5. run `./SDD/scripts/validate-sdd.sh --strict` in Linux or macOS shells, or `./SDD/scripts/validate-sdd.ps1 -Strict` in PowerShell
6. create a parent task before implementation
