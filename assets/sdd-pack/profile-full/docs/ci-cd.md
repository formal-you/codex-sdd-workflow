# CI/CD

Use this file when the workflow runs in the `full` profile.

## Intent

- keep the task graph aligned with pipeline reality
- record the required checks before merge or deploy
- keep automation examples local to the repo instead of hidden in chat

## Baseline

- automation notes live under `../automation/`
- the starter GitHub Actions example lives at `../automation/github-actions/ci.yml.example`
- release plans should point at the checks that must pass

## Before Merge

1. branch checks are green
2. task acceptance criteria are satisfied
3. the release or sprint card records any deferred risk

## Before Deploy

1. release checklist is current
2. rollback owner and rollback command are known
3. evidence links are attached when the deployment changes user-facing behavior
