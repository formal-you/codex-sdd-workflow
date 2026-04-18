# Current Skill Audit

This document audits the current `codex-sdd-workflow` skill implementation itself, not the `workflow-audit.md` template that will later be bootstrapped into user repositories.

## Audit Metadata

- date: 2026-04-18
- auditor: Codex
- target version or branch: current workspace snapshot on `main`
- target under review: current `codex-sdd-workflow` implementation
- latest validation result:
  - `reports/skill-validation.md`
- intended audience:
  - `lite`: public release
  - `full`: beta users
- evidence reviewed:
  - commands:
    - `python scripts/bootstrap_sdd_pack.py --target <temp> --lang zh-cn --workflow-profile lite`
    - `python scripts/bootstrap_sdd_pack.py --target <temp> --lang zh-cn --workflow-profile full`
    - `python -m unittest discover -s tests -p "test_*.py" -v`
  - generated repos:
    - both `lite` and `full` profiles were bootstrapped into temporary directories and checked for generated structure and `workflow-config.env`
  - manual flows:
    - checked bootstrap next-step output
    - checked that `full` generates backlog, sprint, release, and automation assets and scripts
    - reviewed `agile-delivery.md`, `ci-cd.md`, and the profile README files for operating constraints
  - automated tests:
    - the current full unittest suite passed, with the latest run recorded in `reports/skill-validation.md`
    - coverage includes `--force`, `--force-root-shims`, `--sdd-dir`, `--no-root-shims`, `lite/full` profiles, cross-shell handoff, validator requirements, skill metadata, references routing, distribution-path hygiene, and the report template

## Common Baseline

| Dimension | Score | Notes |
| --- | --- | --- |
| Session recovery | 9.2 | Root `AGENTS.md`, `docs/process.md`, task or subtask cards, handoff templates, and session-brief form a stable recovery surface. |
| Delegation quality | 8.9 | Parent-task-first discipline, explicit subtasks, and clear main-agent integration ownership fit the main agent plus multi-subagent model well. |
| Multi-subagent readiness | 8.8 | Parallel decomposition rules, owned-scope language, and integration responsibility are clear, though still process-level rather than enforced orchestration. |
| Cross-shell reliability | 8.8 | PowerShell and shell variants exist with tests covering handoff and validator behavior; CRLF parsing issues were fixed. |
| Proof and auditability | 8.9 | Tasks, ADRs, evidence, audits, handoffs, and validation scripts create a good replay trail. |
| Git collaboration baseline | 8.5 | Git context detection, `.gitignore` bootstrapping, and repo-root handoff scope are solid, but there is still no PR or approval-system integration. |
| Token efficiency potential | 9.1 | Durable local workflow state clearly reduces dependence on chat memory. |
| Self-validation | 8.9 | `validate-sdd`, `session-brief`, and bootstrap tests form a strong validation baseline. |
| Bootstrap clarity | 8.7 | Commands, language or stack selection, and profile selection are clear, and `lite/full` branching is now explicit. |
| Overall common baseline | 8.9 | As an execution workflow for accurate development plus main agent and multi-subagent collaboration, it is now in the excellent tier. |

## Lite Profile Review

### Lite Fit

- best-fit repo type:
  - single-service repos, tooling repos, scaffolding repos, SDK repos, and small to medium product repos
- best-fit team size:
  - best at 1 to 3 people, and still workable for disciplined 4 to 5 person teams
- when this profile is enough:
  - when the goal is stable execution, precise delivery, and main agent plus multi-subagent coordination rather than a full project-management suite
  - when change moves mainly through engineering tasks and release or backlog overhead is still modest
- when this profile becomes too small:
  - when you need formal backlog intake, sprint rhythm, release checklists, cross-role coordination, or pre-release operating structure

### Lite Scorecard

| Dimension | Score | Notes |
| --- | --- | --- |
| Accurate execution workflow | 9.4 | This is the strongest part of the current implementation: task-driven, verification-driven, and handoff-driven execution is clear. |
| Parent task and subtask discipline | 9.2 | Decomposition gates, subtask linkage, and main-agent integration rules are explicit. |
| Fast startup and low-noise usage | 9.5 | The profile stays lean and gets teams into execution quickly. |
| Solo or small-team collaboration | 8.5 | Shared tasks, handoffs, and process docs make small-team collaboration practical. |
| Incremental project evolution | 8.6 | Durable docs, ADRs, and history support long-lived evolution, though migration tooling is still missing. |
| Handoff quality | 8.9 | Repo-scope handoff behavior is now much more useful for real collaboration. |
| Lightweight agile support | 7.4 | There is task flow and progress tracking, but no backlog, sprint, or release layer. |
| Public adoption readiness | 8.5 | It is now strong enough to serve as the public default profile. |
| Overall lite profile | 8.8 | Ready to ship as the default profile. |

## Full Profile Review

### Full Fit

- best-fit repo type:
  - ongoing product repos, multi-contributor business repos, and projects that need release rhythm and delivery rhythm
- best-fit team size:
  - strongest at 3 to 8 people; larger teams still need external project-management and CI platforms
- when this profile is worth the extra ceremony:
  - when backlog growth, iteration planning, release reviews, or CI/CD checklist needs have become real
  - when you want to scale from an execution workflow into a lightweight agile management suite plus automation scaffolding
- when this profile is too heavy:
  - for solo prototypes, one-off delivery work, small scripts, or exploratory repos without a stable cadence

### Full Scorecard

| Dimension | Score | Notes |
| --- | --- | --- |
| Backlog management support | 8.3 | Backlog folders, templates, scripts, and linkage rules are enough for basic intake and prioritization. |
| Sprint planning support | 8.1 | Sprint cards and active/history structure are clear, but still mostly document-driven. |
| Release management support | 8.2 | Release templates and checklist thinking are present and useful for small teams. |
| CI/CD scaffolding usefulness | 7.5 | `automation/` and a GitHub Actions example exist, but this is still scaffolding rather than a live pipeline platform. |
| Cross-role collaboration | 7.6 | Product, engineering, and release viewpoints now have landing spots, but reviewer, approver, and owner mechanics are still thin. |
| Agile delivery support | 7.9 | The backlog-sprint-task-release path exists, but it does not yet close the loop on velocity, capacity, or defect flow. |
| Scale-up path from lite | 8.7 | The conceptual path from `lite` to `full` is smooth and the bootstrap behavior supports that expansion well. |
| Operational clarity | 8.2 | Directory semantics and documentation responsibilities are easy to understand. |
| Overall full profile | 8.1 | Strong beta-quality scaffolding, but not yet a full agile-management and CI/CD orchestration platform. |

## Release Recommendation

- lite:
  - ship
  - reason:
    - the current `lite` profile is strong enough for accurate development, main agent plus multi-subagent collaboration, small-team work, and incremental project evolution
- full:
  - beta only
  - reason:
    - the current `full` profile has clear value, but it is still best described as strong scaffolding rather than a complete agile-management and orchestration platform

## Next Actions

1. Add team-scale fields and template requirements to `full`, such as owner, reviewer, release approver, environment, and rollback owner.
2. Add a workflow upgrade or migration command so existing repos can evolve incrementally instead of relying mostly on `--force`.
3. Expand tests and examples to cover the minimum `full` loop from backlog to sprint to task to release, and add execution guidance for the CI example.

---

## Documentation Architecture Upgrade (2026-04-18 Audit Addendum)

During this audit, the skill's primary entrypoint (`README.md`) was completely refactored and upgraded:

1. **Vastly Improved Readability & Engagement**: Transitioned from a dry, declarative format to a pain-point driven narrative, highlighting 9 core capabilities and specific user personas.
2. **Materialized Workflow Artifacts**: Added a full visual directory tree of the generated `SDD/` workspace. The roles of markdown files, folders, and the intertwined lifecycles of tasks, evidence, and records are now explicitly modeled.
3. **AI-Native Daily Guide**: Filled the "what to do after installation" gap with a natural-language-first workflow. The README now frames scripts as deterministic APIs for Codex rather than as the default surface ordinary users must type manually, while still clarifying first bootstrap versus safe upgrade behavior.
4. **Terminology Calibration**: Corrected stiff, machine-translated phrasing (for example, replacing "下一步纪律" with "下一步指引") while keeping the current unittest suite aligned with the documentation language.

**Audit Score Adjustment**: "Bootstrap clarity" and user on-boarding guidance are now fundamentally stronger. The next immediate step for documentation is to incorporate moving GIF demonstrations and fully filled-out example task templates to further lower the adoption barrier.
