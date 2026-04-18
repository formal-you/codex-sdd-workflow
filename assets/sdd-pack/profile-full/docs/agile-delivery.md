# Agile Delivery

Use this file when the workflow runs in the `full` profile.

## Cadence

- backlog intake lives under `../backlog/items/`
- active sprint plans live under `../sprints/active/`
- completed sprint plans move to `../sprints/history/`
- release plans and checklists live under `../releases/records/`

## Working Loop

1. capture candidate work with `new-backlog-item`
2. decide what enters the next sprint
3. create a sprint card with `new-sprint`
4. link sprint work to task cards under `../tasks/active/`
5. close the sprint, archive the sprint card, and refresh `process.md`
6. prepare a release card when the sprint is release-bound

## Minimum Fields To Keep Fresh

- sprint goal
- committed backlog items
- carry-over work
- release target or deployment window
- CI or CD risks that block shipping
