# Docs Index

Use this folder as the durable memory layer for the repository.

## Reading Order

1. `../../AGENTS.md`
2. `../workflow.md`
3. `process.md`
4. `project-brief.md`
5. `architecture.md`
6. `testing.md`
7. `git-workflow.md`
8. `progress.md`
9. the relevant file in `../tasks/active/`
10. any relevant file in `../adr/records/`

## File Roles

- `project-brief.md`: product, users, goals, constraints
- `process.md`: long-lived process summary, current task pointer, archive digest
- `architecture.md`: module map, ownership, risky areas
- `testing.md`: commands and quality gates
- `git-workflow.md`: branch naming, commit conventions, PR readiness
- `progress.md`: current implementation state and handoff
- `workflow-audit.md`: scorecard and findings from validating the workflow itself

## Full Profile Additions

When the workflow is generated with `--workflow-profile full`, this folder also includes:

- `agile-delivery.md`: backlog, sprint, and release cadence
- `ci-cd.md`: pipeline expectations and deployment gates
