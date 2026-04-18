# Changelog

All notable changes to this project will be documented here.

## Unreleased

- Added open-source project metadata, including README, MIT license, contributing guide, security policy, and CI workflow.
- Added local fallback skill validation so clean CI environments do not require a private `.system/skill-creator` installation.
- Documented `lite` as the public default profile and `full` as beta scaffolding.
- Added branch-aware hot-state scaffolding under `SDD/state/`, keeping `progress.md` as the shared aggregate recovery surface.
- Added connector-first configuration and stub entrypoints for `full`, with `EXTERNAL_ISSUE_SOURCE=none` and `CONNECTOR_MODE=pull-only` as the safe default.
- Added supported template overlay loading plus overlay manifest recording for controlled task, subtask, evidence, and release template customization.

## Current Baseline

- `lite` profile: public-ready default for durable engineering execution, task cards, validation, and handoff.
- `full` profile: beta scaffolding for backlog, sprint, release, and CI/CD-oriented workflow structure.
- Validation baseline: `quick_validate` or local fallback plus the unittest suite.
