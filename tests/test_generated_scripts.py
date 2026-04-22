from test_utils import *


class GeneratedScriptsTests(BootstrapWorkflowTestCase):
    def test_no_root_shims_mode_is_self_consistent(self) -> None:
        powershell = powershell_executable()
        if not powershell:
            self.skipTest("PowerShell is not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.run_bootstrap("--target", tmpdir, "--lang", "en", "--no-root-shims")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(Path(tmpdir, "README.md").exists())
            self.assertFalse(Path(tmpdir, "AGENTS.md").exists())

            config = Path(tmpdir, "SDD", "workflow-config.env").read_text(encoding="utf-8")
            self.assertIn("ROOT_SHIMS=disabled", config)
            self.assertIn("Root shims are disabled;", result.stdout)

            script_path = Path(tmpdir, "SDD", "scripts", "validate-sdd.ps1")
            validate = subprocess.run(
                [
                    powershell,
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    f"& '{script_path}' -Strict",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(validate.returncode, 0, validate.stdout + validate.stderr)
            self.assertIn("workflow-config.env", validate.stdout)

    def test_validator_requires_validate_scripts(self) -> None:
        bash = bash_executable()
        if not bash:
            self.skipTest("bash is not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            bootstrap = self.run_bootstrap("--target", tmpdir, "--lang", "en")
            self.assertEqual(bootstrap.returncode, 0, bootstrap.stderr)

            Path(tmpdir, "SDD", "scripts", "validate-sdd.ps1").unlink()
            script_path = shell_script_path(Path(tmpdir, "SDD", "scripts", "validate-sdd.sh"))

            result = subprocess.run(
                [
                    bash,
                    "-lc",
                    f"\"{script_path}\" --strict",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("[FAIL] scripts/validate-sdd.ps1", result.stdout)

    def test_powershell_handoff_reports_repo_scope_changes(self) -> None:
        powershell = powershell_executable()
        if not powershell:
            self.skipTest("PowerShell is not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            bootstrap = self.run_bootstrap("--target", tmpdir, "--lang", "en")
            self.assertEqual(bootstrap.returncode, 0, bootstrap.stderr)

            Path(tmpdir, "app.py").write_text("print('hi')\n", encoding="utf-8")
            script_path = Path(tmpdir, "SDD", "scripts", "handoff-template.ps1")

            result = subprocess.run(
                [
                    powershell,
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    f"& '{script_path}' -CurrentTask 'tasks/active/TASK-001-sample.md' -CommitStatus 'not committed' -UncommittedReason 'manual mode' -CommitMessage 'chore: test handoff'",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("?? app.py", result.stdout)
            self.assertIn("- [ ] recommended next step:", result.stdout)
            self.assertIn("- [ ] active task: tasks/active/TASK-001-sample.md", result.stdout)
            self.assertIn("- [ ] commit status: not committed", result.stdout)
            self.assertIn("- [ ] recommended commit message: chore: test handoff", result.stdout)
            self.assertIn("## Context Checkpoint", result.stdout)
            self.assertIn("- [ ] context action: continue / compact / new session", result.stdout)
            self.assertNotIn("backlog item:", result.stdout)

    def test_shell_handoff_reports_repo_scope_changes(self) -> None:
        bash = bash_executable()
        if not bash:
            self.skipTest("bash is not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            bootstrap = self.run_bootstrap("--target", tmpdir, "--lang", "en")
            self.assertEqual(bootstrap.returncode, 0, bootstrap.stderr)

            Path(tmpdir, "app.py").write_text("print('hi')\n", encoding="utf-8")
            script_path = shell_script_path(Path(tmpdir, "SDD", "scripts", "handoff-template.sh"))

            result = subprocess.run(
                [
                    bash,
                    "-lc",
                    f"\"{script_path}\" --task \"tasks/active/TASK-001-sample.md\" --commit-status \"not committed\" --uncommitted-reason \"manual mode\" --commit-message \"chore: test handoff\"",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("?? app.py", result.stdout)
            self.assertIn("- [ ] recommended next step:", result.stdout)
            self.assertIn("- [ ] active task: tasks/active/TASK-001-sample.md", result.stdout)
            self.assertIn("- [ ] commit status: not committed", result.stdout)
            self.assertIn("- [ ] recommended commit message: chore: test handoff", result.stdout)
            self.assertIn("## Context Checkpoint", result.stdout)
            self.assertIn("- [ ] context action: continue / compact / new session", result.stdout)
            self.assertNotIn("backlog item:", result.stdout)

    def test_session_brief_prefers_current_handoff_and_keeps_legacy_fallback(self) -> None:
        powershell = powershell_executable()
        if not powershell:
            self.skipTest("PowerShell is not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            bootstrap = self.run_bootstrap("--target", tmpdir, "--lang", "en")
            self.assertEqual(bootstrap.returncode, 0, bootstrap.stderr)

            progress = Path(tmpdir, "SDD", "docs", "progress.md")
            progress.write_text(
                "# Progress\n\n"
                "## Current\n\n"
                "- [ ] current phase: focused validation\n\n"
                "## Recent Findings\n\n"
                "- [ ] [2026-04-19] finding: reproduced the parser issue\n\n"
                "## Session Handoff\n\n"
                "- [ ] commit status: not committed\n"
                "- [ ] recommended next step: run the focused regression\n\n"
                "## Context Checkpoint\n\n"
                "- [ ] true goal: keep session recovery reliable\n"
                "- [ ] latest validation status: focused regression pending\n\n"
                "## Concurrency\n\n"
                "- [ ] integration status: single_task\n\n"
                "## Git Closure\n\n"
                "- [ ] commit status: legacy not committed\n\n"
                "## Next Options\n\n"
                "- [ ] recommended next step: legacy fallback\n\n"
                "## Next\n\n"
                "- [ ] next action 1: legacy fallback\n",
                encoding="utf-8",
            )
            script_path = Path(tmpdir, "SDD", "scripts", "session-brief.ps1")

            result = subprocess.run(
                [
                    powershell,
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    f"& '{script_path}'",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("task completion git mode: manual", result.stdout)
            self.assertIn("## Current", result.stdout)
            self.assertIn("current phase: focused validation", result.stdout)
            self.assertIn("## Session Handoff", result.stdout)
            self.assertIn("recommended next step: run the focused regression", result.stdout)
            self.assertIn("## Context Checkpoint", result.stdout)
            self.assertIn("true goal: keep session recovery reliable", result.stdout)
            self.assertIn("## Concurrency", result.stdout)
            self.assertIn("## Git Closure", result.stdout)
            self.assertIn("commit status: legacy not committed", result.stdout)
            self.assertIn("## Next Options", result.stdout)
            self.assertIn("recommended next step: legacy fallback", result.stdout)
            self.assertLess(result.stdout.index("## Session Handoff"), result.stdout.index("## Next Options"))

    def test_session_brief_reads_branch_and_task_hot_state(self) -> None:
        powershell = powershell_executable()
        if not powershell:
            self.skipTest("PowerShell is not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            bootstrap = self.run_bootstrap("--target", tmpdir, "--lang", "en")
            self.assertEqual(bootstrap.returncode, 0, bootstrap.stderr)

            progress = Path(tmpdir, "SDD", "docs", "progress.md")
            progress.write_text(
                "# Progress\n\n"
                "## Current\n\n"
                "- [ ] current phase: focused validation\n"
                "- [ ] active task: `tasks/active/TASK-001-hot-state.md`\n\n"
                "## Session Handoff\n\n"
                "- [ ] recommended next step: review the hot state summary\n",
                encoding="utf-8",
            )
            Path(tmpdir, "SDD", "tasks", "active", "TASK-001-hot-state.md").write_text("# TASK-001\n", encoding="utf-8")
            Path(tmpdir, "SDD", "state", "hot", "branches", "main.md").write_text("# Branch Hot State\n\n- [ ] branch note\n", encoding="utf-8")
            Path(tmpdir, "SDD", "state", "hot", "tasks", "TASK-001-hot-state.md").write_text("# Task Hot State\n\n- [ ] task note\n", encoding="utf-8")

            script_path = Path(tmpdir, "SDD", "scripts", "session-brief.ps1")
            result = subprocess.run(
                [
                    powershell,
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    f"& '{script_path}'",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("## Active Branch Hot State", result.stdout)
            self.assertIn("branch note", result.stdout)
            self.assertIn("## Active Task Hot State", result.stdout)
            self.assertIn("task note", result.stdout)

    def test_archive_task_prints_next_step_discipline_reminder(self) -> None:
        bash = bash_executable()
        if not bash:
            self.skipTest("bash is not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            bootstrap = self.run_bootstrap("--target", tmpdir, "--lang", "en")
            self.assertEqual(bootstrap.returncode, 0, bootstrap.stderr)

            task = Path(tmpdir, "SDD", "tasks", "active", "TASK-001-next-step.md")
            task.write_text("# TASK-001: Next step\n", encoding="utf-8")
            script_path = shell_script_path(Path(tmpdir, "SDD", "scripts", "archive-task.sh"))

            result = subprocess.run(
                [
                    bash,
                    "-lc",
                    f"\"{script_path}\" \"tasks/active/TASK-001-next-step.md\"",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("leave a next-step entry", result.stdout)
            self.assertTrue(Path(tmpdir, "SDD", "tasks", "history", "TASK-001-next-step.md").exists())

    def test_archive_task_retires_task_hot_state_note(self) -> None:
        bash = bash_executable()
        if not bash:
            self.skipTest("bash is not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            bootstrap = self.run_bootstrap("--target", tmpdir, "--lang", "en")
            self.assertEqual(bootstrap.returncode, 0, bootstrap.stderr)

            task = Path(tmpdir, "SDD", "tasks", "active", "TASK-001-hot-state.md")
            task.write_text("# TASK-001: Hot state\n", encoding="utf-8")
            hot_state = Path(tmpdir, "SDD", "state", "hot", "tasks", "TASK-001-hot-state.md")
            hot_state.write_text("# Hot State\n\n- [ ] scratch note\n", encoding="utf-8")
            script_path = shell_script_path(Path(tmpdir, "SDD", "scripts", "archive-task.sh"))

            result = subprocess.run(
                [
                    bash,
                    "-lc",
                    f"\"{script_path}\" \"tasks/active/TASK-001-hot-state.md\"",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Retired task hot state", result.stdout)
            self.assertTrue(Path(tmpdir, "SDD", "state", "history", "tasks", "TASK-001-hot-state.md").exists())
            self.assertFalse(hot_state.exists())

    def test_validate_warns_but_passes_when_next_step_signal_is_missing(self) -> None:
        bash = bash_executable()
        if not bash:
            self.skipTest("bash is not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            bootstrap = self.run_bootstrap("--target", tmpdir, "--lang", "en")
            self.assertEqual(bootstrap.returncode, 0, bootstrap.stderr)

            script_path = shell_script_path(Path(tmpdir, "SDD", "scripts", "validate-sdd.sh"))
            result = subprocess.run(
                [
                    bash,
                    "-lc",
                    f"\"{script_path}\" --strict",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("[WARN] docs/progress.md does not contain a concrete next-step signal", result.stdout)
            self.assertIn("Result: PASS", result.stdout)

            progress = Path(tmpdir, "SDD", "docs", "progress.md")
            progress.write_text(
                "# Progress\n\n"
                "## Session Handoff\n\n"
                "- [ ] recommended next step: create TASK-002 for rollout checks\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    bash,
                    "-lc",
                    f"\"{script_path}\" --strict",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("does not contain a concrete next-step signal", result.stdout)

    def test_validate_warns_but_passes_when_completed_task_lacks_git_closure(self) -> None:
        bash = bash_executable()
        if not bash:
            self.skipTest("bash is not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            bootstrap = self.run_bootstrap("--target", tmpdir, "--lang", "en")
            self.assertEqual(bootstrap.returncode, 0, bootstrap.stderr)

            progress = Path(tmpdir, "SDD", "docs", "progress.md")
            progress.write_text(
                "# Progress\n\n"
                "## Session Handoff\n\n"
                "- [ ] recommended next step: prepare release checks\n",
                encoding="utf-8",
            )
            task = Path(tmpdir, "SDD", "tasks", "active", "TASK-001-complete.md")
            task.write_text(
                "# TASK-001: Complete\n\n"
                "## Status\n\n"
                "- [x] done\n",
                encoding="utf-8",
            )
            script_path = shell_script_path(Path(tmpdir, "SDD", "scripts", "validate-sdd.sh"))

            result = subprocess.run(
                [
                    bash,
                    "-lc",
                    f"\"{script_path}\" --strict",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("does not record manual Git closure", result.stdout)
            self.assertIn("Result: PASS", result.stdout)

            task.write_text(
                "# TASK-001: Complete\n\n"
                "## Status\n\n"
                "- [x] done\n\n"
                "## Completion Handoff\n\n"
                "- [ ] commit status: not committed\n"
                "- [ ] recommended commit message: chore: record completed task\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    bash,
                    "-lc",
                    f"\"{script_path}\" --strict",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("does not record manual Git closure", result.stdout)

            config = Path(tmpdir, "SDD", "workflow-config.env")
            config.write_text(config.read_text(encoding="utf-8").replace("TASK_COMPLETION_GIT_MODE=manual", "TASK_COMPLETION_GIT_MODE=auto"), encoding="utf-8")
            task.write_text(
                "# TASK-001: Complete\n\n"
                "## Status\n\n"
                "- [x] done\n\n"
                "## Completion Handoff\n\n"
                "- [ ] commit status: committed\n"
                "- [ ] commit hash: abc1234\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    bash,
                    "-lc",
                    f"\"{script_path}\" --strict",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("does not record committed Git closure", result.stdout)

