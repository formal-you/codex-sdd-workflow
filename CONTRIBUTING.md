# Contributing

Thanks for improving `codex-sdd-workflow`. Keep changes focused: this repository is a Codex skill, not a Python package or a general project-management platform.

## Development Flow

1. Read `SKILL.md` before changing trigger or routing behavior.
2. Change `assets/` for files copied into target repositories.
3. Change `scripts/` for bootstrap, rendering, Git, or validation behavior.
4. Change `references/` for optional skill guidance, audits, and forward-testing prompts.
5. Keep maintainer docs out of the default skill route unless `SKILL.md` explicitly needs them.

## Validation

Run these before opening a PR:

```sh
python -m pip install PyYAML
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/run_skill_validation.py --skip-tests
```

When trigger semantics, profile behavior, or validation reporting changes, also run:

```sh
python scripts/run_skill_validation.py --print-forward-prompts --report reports/skill-validation.md
```

## Contribution Rules

- Do not change the skill name, public CLI flags, or `lite/full` semantics without calling it out as a breaking change.
- Do not commit `__pycache__/`, `.pyc`, coverage output, local virtual environments, secrets, or private machine paths.
- Prefer configuration or templates over Python changes for language, stack, profile, `.gitignore`, next-step, and generated-doc content.
- Preserve shell-first documentation while keeping PowerShell equivalents supported.

