# Forward Testing Cases

Use this file when validating `codex-sdd-workflow` as a skill, not just validating the bootstrap script.

These prompts are intentionally written like real user requests. Keep validation low-leakage: give the subagent the skill path and the prompt, but do not provide the intended answer, suspected bug, or expected fix.

## Common Setup

- use a fresh thread or agent for each case
- invoke the skill explicitly as `$codex-sdd-workflow`
- pass only the skill path and the user-style request
- review whether the response routes to the right references and next steps

## Case 1: Existing Repo Bootstrap

### Prompt

```text
Use $codex-sdd-workflow at /path/to/codex-sdd-workflow to help with this request: I have an existing repository and want to bootstrap a durable Codex workflow into it. I have not said whether I want the lite or full profile yet. Tell me what you would do first and what repo-local workflow entrypoints I should use after bootstrap.
```

### Expected Behaviors

- asks or pauses on `lite` vs `full` instead of assuming silently
- recommends `lite` by default when no broader agile-management need is stated
- starts with a safe bootstrap path such as `--dry-run`
- routes the user into generated workflow entrypoints after bootstrap
- mentions root `AGENTS.md` when root shims are enabled
- mentions `SDD/workflow.md` and `SDD/docs/process.md`
- mentions `session-brief`, `validate-sdd`, and creating the first parent task

### Failure Signals

- jumps straight into `full` without justification
- stops at the installer and does not describe repo-local entrypoints
- answers only with generic workflow advice and misses the generated scripts

## Case 2: Existing Workflow Upgrade

### Prompt

```text
Use $codex-sdd-workflow at /path/to/codex-sdd-workflow to help with this request: My existing repo already has an older SDD workflow and I want to refresh or upgrade it without blindly replacing unrelated root files. Tell me the safest command path and what to read after upgrading.
```

### Expected Behaviors

- recognizes this as an upgrade or refresh path, not a first bootstrap path
- recommends `--dry-run` before replacement
- recommends `--force` only for the generated workflow directory
- avoids recommending `--force-root-shims` unless explicitly requested
- may suggest `--no-root-shims` when the repo should keep its own root contract
- routes the user to post-upgrade reading order:
  - `AGENTS.md` when root shims are enabled
  - `SDD/docs/process.md`
  - `SDD/workflow.md`
  - `session-brief`
  - `validate-sdd`

### Failure Signals

- recommends replacing root files by default
- ignores the distinction between refresh and first bootstrap
- fails to mention reading or validating the upgraded workflow

## Case 3: Lite vs Full Decision

### Prompt

```text
Use $codex-sdd-workflow at /path/to/codex-sdd-workflow to help with this request: I am not sure whether I need a lightweight engineering workflow or a fuller agile delivery setup with backlog, sprint, release, and CI/CD scaffolding. Help me choose and explain the practical difference.
```

### Expected Behaviors

- explains the practical tradeoff between `lite` and `full`
- defaults toward `lite` unless broader delivery-management needs are explicit
- frames `full` as backlog, sprint, release, and CI/CD scaffolding
- avoids overstating `full` as a complete CI/CD orchestration platform

### Failure Signals

- describes `full` as full automation or a complete delivery platform
- gives only abstract differences and no practical recommendation
- skips the default recommendation

## Review Checklist

For each case, check:

1. did the skill trigger on the right problem shape
2. did it ask or decide `lite/full` appropriately
3. did it route to the right reference depth instead of overloading `SKILL.md`
4. did it guide the user into generated workflow entrypoints
5. did it avoid unsafe upgrade advice

## Current Baseline

These three cases were forward-tested after the current skill-structure refactor and produced the expected high-level outcomes:

- bootstrap case: asked for or defaulted `lite/full`, then routed to repo-local entrypoints
- upgrade case: preferred preview and avoided replacing root files by default
- profile-choice case: defaulted toward `lite` and explained `full` as scaffolding, not a full platform
