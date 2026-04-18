# Skill Validation Report

- generated_at_utc: 2026-04-18 14:35:04Z
- skill: codex-sdd-workflow
- quick_validate: passed
- unit_tests: passed
- forward_testing_prompts: included

## Summary

This report records the latest semi-automated validation run for the skill.

## Commands

```sh
python ../.system/skill-creator/scripts/quick_validate.py .
python scripts/run_skill_validation.py --print-forward-prompts
python -m unittest discover -s tests -p "test_*.py" -v
```

## Results

- quick_validate: passed
- unit_tests: passed
- forward_testing_prompts: included

## Forward Testing Source

- reference: `references/forward-testing.md`
- note: run the prompts there in fresh threads and record outcomes separately

## Next Manual Check

1. review the latest forward-testing prompt set
2. run those prompts in fresh threads when the skill’s trigger surface changes
3. compare this report with `references/skill-audit-zh-cn.md` or `references/skill-audit.md`
