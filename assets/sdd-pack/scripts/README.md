# SDD Scripts

These generated scripts are the local day-to-day workflow interface for the current repo. The skill installs or upgrades them; daily use happens here.

## Included Helpers

- `new-task.ps1` / `new-task.sh`
  - create the next numbered task card from `../templates/tasks/TASK-template.md` under `../tasks/active/`
- `new-subtask.ps1` / `new-subtask.sh`
  - create the next numbered subtask card from `../templates/tasks/SUBTASK-template.md` under `../tasks/active/`
- `new-adr.ps1` / `new-adr.sh`
  - create the next numbered ADR from `../templates/adr/ADR-000-template.md` under `../adr/records/`
- `archive-task.ps1` / `archive-task.sh`
  - move a completed task or subtask from `../tasks/active/` into `../tasks/history/`
- `session-brief.ps1` / `session-brief.sh`
  - print a compact startup brief with `process.md`, `progress.md`, git status, and active/history summaries
- `handoff-template.ps1` / `handoff-template.sh`
  - print a Markdown handoff block for `../docs/progress.md`
- `validate-sdd.ps1` / `validate-sdd.sh`
  - check the workflow pack for missing core files, stale placeholders, and incomplete parallel-task wiring

When the workflow is generated with `--workflow-profile full`, the scripts folder also includes:

- `new-backlog-item.ps1` / `new-backlog-item.sh`
- `new-sprint.ps1` / `new-sprint.sh`
- `new-release.ps1` / `new-release.sh`

## Example Usage

### shell

```sh
./SDD/scripts/session-brief.sh
./SDD/scripts/new-task.sh "Add retry handling for OCR import"
./SDD/scripts/new-subtask.sh "tasks/active/TASK-003-add-retry-handling.md" "Update retry policy in worker"
./SDD/scripts/new-adr.sh "Adopt gopls MCP for Go work"
./SDD/scripts/archive-task.sh "tasks/active/TASK-003-add-retry-handling.md"
./SDD/scripts/handoff-template.sh --task "tasks/active/TASK-003-add-retry-handling.md"
./SDD/scripts/validate-sdd.sh
```

### PowerShell

```powershell
./SDD/scripts/session-brief.ps1
./SDD/scripts/new-task.ps1 "Add retry handling for OCR import"
./SDD/scripts/new-subtask.ps1 "tasks/active/TASK-003-add-retry-handling.md" "Update retry policy in worker"
./SDD/scripts/new-adr.ps1 "Adopt gopls MCP for Go work"
./SDD/scripts/archive-task.ps1 "tasks/active/TASK-003-add-retry-handling.md"
./SDD/scripts/handoff-template.ps1 -CurrentTask "tasks/active/TASK-003-add-retry-handling.md"
./SDD/scripts/validate-sdd.ps1
```

## Design Notes

- The scripts write only inside the current repo's `SDD/` tree.
- Naming and numbering are deterministic.
- `new-task.*`, `new-subtask.*`, `new-adr.*`, and `archive-task.*` support dry runs.
- `handoff-template.*` prints output instead of editing docs automatically, so the agent can review before pasting.
- `validate-sdd.*` is intentionally conservative: hard failures for missing structure, warnings for likely stale content.
