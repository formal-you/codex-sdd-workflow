# Testing Guide

## Principles

- Start with the smallest test that can fail for the change.
- Prefer targeted verification before broad suite runs.
- Record commands that actually work in this repo.

## Fast Checks

- workflow structure:
  - `./SDD/scripts/validate-sdd.ps1 -Strict`
  - `./SDD/scripts/validate-sdd.sh --strict`
- task startup:
  - `./SDD/scripts/session-brief.ps1`
  - `./SDD/scripts/session-brief.sh`

## Project-Specific Checks

- lint:
- typecheck:
- unit tests:
- integration tests:

## Quality Gates

Before claiming a task is done:

1. targeted tests pass
2. no new diagnostics remain in changed files
3. behavior, task state, and risks are documented
4. Git closure is documented: committed, or not committed with reason and recommended commit message
5. branch, commit, and PR readiness match `docs/git-workflow.md`
