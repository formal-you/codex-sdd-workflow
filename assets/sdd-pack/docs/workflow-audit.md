# Workflow Audit

Use this file when validating or iterating on the workflow itself.

The goal is not only to score the current pack, but also to make it clear whether the `lite` profile, the `full` profile, or both are ready for the intended audience.

## Audit Metadata

- date:
- auditor:
- target version or branch:
- intended audience:
  - internal only / beta users / public release
- audited profiles:
  - lite / full / both
- evidence reviewed:
  - commands:
  - generated repos:
  - manual flows:
  - automated tests:

## Common Baseline

Score the workflow behaviors that should hold regardless of profile.

| Dimension | Score | Notes |
| --- | --- | --- |
| Session recovery | | |
| Delegation quality | | |
| Multi-subagent readiness | | |
| Cross-shell reliability | | |
| Proof and auditability | | |
| Git collaboration baseline | | |
| Token efficiency potential | | |
| Self-validation | | |
| Bootstrap clarity | | |
| Overall common baseline | | |

## Lite Profile Review

Use this section when the workflow is generated with `--workflow-profile lite`.

### Lite Fit

- best-fit repo type:
- best-fit team size:
- when this profile is enough:
- when this profile becomes too small:

### Lite Scorecard

| Dimension | Score | Notes |
| --- | --- | --- |
| Accurate execution workflow | | |
| Parent task and subtask discipline | | |
| Fast startup and low-noise usage | | |
| Solo or small-team collaboration | | |
| Incremental project evolution | | |
| Handoff quality | | |
| Lightweight agile support | | |
| Public adoption readiness | | |
| Overall lite profile | | |

### Lite Strengths

1.
2.
3.

### Lite Gaps

1.
2.
3.

## Full Profile Review

Use this section when the workflow is generated with `--workflow-profile full`.

### Full Fit

- best-fit repo type:
- best-fit team size:
- when this profile is worth the extra ceremony:
- when this profile is too heavy:

### Full Scorecard

| Dimension | Score | Notes |
| --- | --- | --- |
| Backlog management support | | |
| Sprint planning support | | |
| Release management support | | |
| CI/CD scaffolding usefulness | | |
| Cross-role collaboration | | |
| Agile delivery support | | |
| Scale-up path from lite | | |
| Operational clarity | | |
| Overall full profile | | |

### Full Strengths

1.
2.
3.

### Full Gaps

1.
2.
3.

## Changes Made During The Audit

- change:

## Risks By Profile

### Lite Risks

- risk:

### Full Risks

- risk:

## Release Recommendation

- lite:
  - ship / beta only / internal only / hold
  - reason:
- full:
  - ship / beta only / internal only / hold
  - reason:

## Next Actions

1.
2.
3.
