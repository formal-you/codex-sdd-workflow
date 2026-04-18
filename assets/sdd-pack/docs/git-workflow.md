# Git Workflow

## Branch Naming

If the repo was freshly bootstrapped with `codex-sdd-workflow`:

1. bootstrap initializes a local Git repository when the target root is not already inside one
2. bootstrap preserves parent-repo boundaries by default instead of silently creating nested repos
3. bootstrap writes a stack-aware `.gitignore` when the target root does not already have one

That keeps the workflow usable for both standalone repos and existing repo directories.

Use short branches with an explicit intent prefix:

- `feat/<scope>-<slug>`
- `fix/<scope>-<slug>`
- `chore/<scope>-<slug>`

Examples:

- `feat/auth-refresh-token`
- `fix/orders-timeout`
- `chore/sdd-refresh`

## Commit Messages

Use Conventional Commits:

- `feat: add retry backoff for import worker`
- `fix(api): handle empty tenant id`
- `docs(sdd): record workflow audit findings`
- `chore: refresh generated workflow helpers`

Keep the summary line imperative and under about 72 characters when possible.

## Task Completion Git Closure

Read `TASK_COMPLETION_GIT_MODE` from `workflow-config.env`.

- `manual`: do not commit by default. When a task is complete, record `commit status: not committed`, the uncommitted reason, and a recommended commit message.
- `auto`: the main agent may commit only after tests pass, git scope is clear, and unrelated user changes are not included.

Subagents must not create final commits. When subtasks were used, the main agent owns integration and the final Git closure.

## Pull Request Checklist

Before opening or handing off a PR, confirm:

1. the task and any subtasks reflect the implemented scope
2. targeted tests or checks are recorded
3. risks, follow-ups, and docs updates are called out
4. the task records whether the work was committed or why it remains uncommitted
5. the branch and commits are ready for review
6. the main agent summarized how subtask work was integrated

## Agent Expectations

- inspect `git status --short` at the start and before finishing
- do not rewrite unrelated user changes
- keep integration commits with the main agent whenever subtasks were delegated
