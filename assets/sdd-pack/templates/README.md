# Templates

This folder stores templates only. Do not place real work artifacts here.

## Layout

- `overlays/`
  - optional overlay manifests and active overlay snapshots
- `tasks/`
  - `TASK-template.md`
  - `SUBTASK-template.md`
- `adr/`
  - `ADR-000-template.md`
- `evidence/`
  - `EVIDENCE-000-template.md`

## Rules

- create real artifacts through `SDD/scripts/`
- keep concrete tasks, ADRs, and evidence outside this folder
- when templates change, prefer upgrading through the skill
- use overlays only for supported template kinds; do not break required headings or checkbox fields
