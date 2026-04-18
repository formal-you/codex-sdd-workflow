# Template Overlays

Use this folder to record the active template overlay manifest, not to store day-to-day work artifacts.

## Rules

- the base templates remain the parser contract
- overlays may only replace supported template kinds
- overlays must preserve required headings, checkbox fields, and completion handoff markers
- when `workflow-config.env` says `TEMPLATE_OVERLAY=none`, this folder should only contain documentation
