from __future__ import annotations

import argparse
from datetime import datetime, timezone
import subprocess
import sys
from pathlib import Path

from skill_validation_utils import find_quick_validate, quick_validate_candidates, validate_skill_locally


SCRIPT_ROOT = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_ROOT.parent
TESTS_ROOT = SKILL_ROOT / "tests"
FORWARD_TESTING_DOC = SKILL_ROOT / "references" / "forward-testing.md"
REPORT_TEMPLATE = SCRIPT_ROOT / "skill_validation_report_template.md.tmpl"


def run_command(label: str, command: list[str]) -> int:
    print(f"\n== {label} ==")
    result = subprocess.run(
        command,
        cwd=SKILL_ROOT,
        text=True,
        check=False,
    )
    return result.returncode


def run_static_validation(force_local: bool) -> int:
    print("\n== quick_validate ==")
    quick_validate = None if force_local else find_quick_validate(SKILL_ROOT)
    if quick_validate:
        result = subprocess.run(
            [sys.executable, str(quick_validate), str(SKILL_ROOT)],
            cwd=SKILL_ROOT,
            text=True,
            check=False,
        )
        return result.returncode

    print("Using local fallback validator.")
    errors = validate_skill_locally(SKILL_ROOT)
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Skill is valid!")
    return 0


def print_forward_prompts() -> None:
    content = FORWARD_TESTING_DOC.read_text(encoding="utf-8")
    print("\n== Forward Testing Cases ==")
    print(content)


def build_report(quick_validate_rc: int, tests_rc: int | None, included_forward_prompts: bool) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    unit_tests_status = "skipped" if tests_rc is None else ("passed" if tests_rc == 0 else "failed")
    quick_validate_status = "passed" if quick_validate_rc == 0 else "failed"
    forward_section = "included" if included_forward_prompts else "not included"
    template = REPORT_TEMPLATE.read_text(encoding="utf-8")
    return template.format(
        generated_at_utc=timestamp,
        skill_name="codex-sdd-workflow",
        quick_validate_status=quick_validate_status,
        unit_tests_status=unit_tests_status,
        forward_testing_status=forward_section,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run semi-automated validation for the codex-sdd-workflow skill."
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip the unittest suite and run only skill-level validation.",
    )
    parser.add_argument(
        "--print-forward-prompts",
        action="store_true",
        help="Print the forward-testing prompt set after static validation.",
    )
    parser.add_argument(
        "--report",
        help="Write a Markdown validation report to the given path.",
    )
    parser.add_argument(
        "--force-local-validation",
        action="store_true",
        help="Use the built-in fallback validator even when skill-creator quick_validate is available.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    exit_code = 0
    tests_rc: int | None = None

    if not args.force_local_validation and not find_quick_validate(SKILL_ROOT):
        print("quick_validate not found; using local fallback validator.")
        print("Checked:")
        for candidate in quick_validate_candidates(SKILL_ROOT):
            print(f"- {candidate}")

    quick_validate_rc = run_static_validation(args.force_local_validation)
    exit_code = max(exit_code, quick_validate_rc)

    if not args.skip_tests:
        tests_rc = run_command(
            "unit_tests",
            [sys.executable, "-m", "unittest", "discover", "-s", str(TESTS_ROOT), "-p", "test_*.py", "-v"],
        )
        exit_code = max(exit_code, tests_rc)

    if args.print_forward_prompts:
        print_forward_prompts()

    if args.report:
        report_path = Path(args.report).expanduser()
        if not report_path.is_absolute():
            report_path = SKILL_ROOT / report_path
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            build_report(
                quick_validate_rc=quick_validate_rc,
                tests_rc=tests_rc,
                included_forward_prompts=args.print_forward_prompts,
            ),
            encoding="utf-8",
        )
        print(f"\n== report_written ==\n{report_path}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
