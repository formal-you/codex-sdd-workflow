import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from pathlib import PureWindowsPath

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = REPO_ROOT / "scripts" / "bootstrap_sdd_pack.py"
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from bootstrap_sdd_settings import load_settings
from skill_validation_utils import find_quick_validate, validate_skill_locally

SKILL_MD = REPO_ROOT / "SKILL.md"
OPENAI_YAML = REPO_ROOT / "agents" / "openai.yaml"
FORWARD_TESTING_MD = REPO_ROOT / "references" / "forward-testing.md"
SKILL_VALIDATION_SCRIPT = REPO_ROOT / "scripts" / "run_skill_validation.py"
NOISE_AUDIT_ZH = REPO_ROOT / "references" / "noise-audit-zh-cn.md"
REPORT_TEMPLATE = REPO_ROOT / "scripts" / "skill_validation_report_template.md.tmpl"
SCRIPTS_README = REPO_ROOT / "scripts" / "README.md"
LATEST_VALIDATION_REPORT = REPO_ROOT / "reports" / "skill-validation.md"
ROOT_GITIGNORE = REPO_ROOT / ".gitignore"
ROOT_README = REPO_ROOT / "README.md"
LICENSE = REPO_ROOT / "LICENSE"
CONTRIBUTING = REPO_ROOT / "CONTRIBUTING.md"
SECURITY = REPO_ROOT / "SECURITY.md"
CHANGELOG = REPO_ROOT / "CHANGELOG.md"
CI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"


def powershell_executable() -> str | None:
    return shutil.which("pwsh") or shutil.which("powershell")


def bash_executable() -> str | None:
    return shutil.which("bash")


def shell_script_path(path: Path) -> str:
    resolved = path.resolve()
    if os.name == "nt":
        pure = PureWindowsPath(resolved)
        drive = pure.drive.rstrip(":").lower()
        tail = "/".join(pure.parts[1:])
        return f"/mnt/{drive}/{tail}"
    return resolved.as_posix()


class BootstrapWorkflowTests(unittest.TestCase):
    maxDiff = None

    def run_bootstrap(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(BOOTSTRAP), *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def load_skill_frontmatter(self) -> dict[str, str]:
        content = SKILL_MD.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))
        _, frontmatter_text, _ = content.split("---", 2)
        parsed = yaml.safe_load(frontmatter_text)
        self.assertIsInstance(parsed, dict)
        return parsed

    def test_custom_sdd_dir_rewrites_generated_references(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.run_bootstrap(
                "--target",
                tmpdir,
                "--lang",
                "en",
                "--sdd-dir",
                "Workflow",
                "--workflow-profile",
                "full",
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            testing_doc = Path(tmpdir, "Workflow", "docs", "testing.md").read_text(encoding="utf-8")
            workflow_doc = Path(tmpdir, "Workflow", "workflow.md").read_text(encoding="utf-8")
            scripts_readme = Path(tmpdir, "Workflow", "scripts", "README.md").read_text(encoding="utf-8")
            shell_script = Path(tmpdir, "Workflow", "scripts", "new-task.sh").read_text(encoding="utf-8")
            automation_example = Path(tmpdir, "Workflow", "automation", "github-actions", "ci.yml.example").read_text(encoding="utf-8")

            self.assertIn("./Workflow/scripts/validate-sdd.ps1 -Strict", testing_doc)
            self.assertNotIn("./SDD/scripts/validate-sdd.ps1 -Strict", testing_doc)
            self.assertIn("This `Workflow/` folder", workflow_doc)
            self.assertIn("./Workflow/scripts/session-brief.ps1", scripts_readme)
            self.assertNotIn("./SDD/scripts/session-brief.ps1", scripts_readme)
            self.assertIn('[--root /path/to/Workflow]', shell_script)
            self.assertNotIn('[--root /path/to/SDD]', shell_script)
            self.assertIn("./Workflow/scripts/validate-sdd.sh --strict", automation_example)
            self.assertNotIn("./SDD/scripts/validate-sdd.sh --strict", automation_example)

    def test_settings_loads_testing_guide_defaults_from_messages_json(self) -> None:
        settings = load_settings()

        self.assertIn("en", settings.testing_guide_defaults)
        self.assertIn("node", settings.testing_guide_defaults["en"])
        self.assertEqual(settings.testing_guide_defaults["en"]["node"][0], "- lint: `npm run lint` or `pnpm lint`")
        self.assertEqual(settings.testing_guide_defaults["zh-cn"]["python"][2], "- unit tests：`pytest` 或 `python -m unittest`")

    def test_skill_description_covers_bootstrap_upgrade_and_profiles(self) -> None:
        frontmatter = self.load_skill_frontmatter()
        description = frontmatter["description"]

        self.assertIn("existing repository", description)
        self.assertIn("initialize or refresh", description)
        self.assertIn("durable docs", description)
        self.assertIn("task graphs", description)
        self.assertIn("lite or full", description)
        self.assertIn("CI/CD-oriented workflow structure", description)

    def test_force_does_not_overwrite_root_shims(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            self.assertEqual(self.run_bootstrap("--target", tmpdir, "--lang", "en").returncode, 0)

            readme_path = Path(tmpdir, "README.md")
            agents_path = Path(tmpdir, "AGENTS.md")
            readme_path.write_text("keep-readme", encoding="utf-8")
            agents_path.write_text("keep-agents", encoding="utf-8")

            result = self.run_bootstrap("--target", tmpdir, "--lang", "en", "--force")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(readme_path.read_text(encoding="utf-8"), "keep-readme")
            self.assertEqual(agents_path.read_text(encoding="utf-8"), "keep-agents")

    def test_force_root_shims_overwrites_root_files_only_when_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            self.assertEqual(self.run_bootstrap("--target", tmpdir, "--lang", "en").returncode, 0)

            readme_path = Path(tmpdir, "README.md")
            agents_path = Path(tmpdir, "AGENTS.md")
            readme_path.write_text("keep-readme", encoding="utf-8")
            agents_path.write_text("keep-agents", encoding="utf-8")

            result = self.run_bootstrap("--target", tmpdir, "--lang", "en", "--force", "--force-root-shims")
            self.assertEqual(result.returncode, 0, result.stderr)

            self.assertIn("This repository uses a Codex-oriented workflow", readme_path.read_text(encoding="utf-8"))
            self.assertIn("single stable operating contract", agents_path.read_text(encoding="utf-8"))

    def test_dry_run_requires_force_when_workflow_dir_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            self.assertEqual(self.run_bootstrap("--target", tmpdir, "--lang", "en").returncode, 0)

            result = self.run_bootstrap("--target", tmpdir, "--lang", "en", "--dry-run")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Use --force to replace it.", result.stderr)

    def test_lite_profile_omits_full_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.run_bootstrap("--target", tmpdir, "--lang", "en", "--workflow-profile", "lite")
            self.assertEqual(result.returncode, 0, result.stderr)

            config = Path(tmpdir, "SDD", "workflow-config.env").read_text(encoding="utf-8")
            self.assertIn("WORKFLOW_PROFILE=lite", config)
            self.assertIn("TASK_COMPLETION_GIT_MODE=manual", config)
            self.assertFalse(Path(tmpdir, "SDD", "docs", "agile-delivery.md").exists())
            self.assertFalse(Path(tmpdir, "SDD", "scripts", "new-sprint.sh").exists())

    def test_full_profile_generates_agile_and_automation_assets(self) -> None:
        bash = bash_executable()
        if not bash:
            self.skipTest("bash is not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.run_bootstrap("--target", tmpdir, "--lang", "en", "--workflow-profile", "full")
            self.assertEqual(result.returncode, 0, result.stderr)

            config = Path(tmpdir, "SDD", "workflow-config.env").read_text(encoding="utf-8")
            self.assertIn("WORKFLOW_PROFILE=full", config)
            self.assertIn("TASK_COMPLETION_GIT_MODE=manual", config)
            self.assertTrue(Path(tmpdir, "SDD", "docs", "agile-delivery.md").exists())
            self.assertTrue(Path(tmpdir, "SDD", "docs", "ci-cd.md").exists())
            self.assertTrue(Path(tmpdir, "SDD", "backlog", "items").exists())
            self.assertTrue(Path(tmpdir, "SDD", "sprints", "active").exists())
            self.assertTrue(Path(tmpdir, "SDD", "releases", "records").exists())
            self.assertTrue(Path(tmpdir, "SDD", "automation", "github-actions", "ci.yml.example").exists())
            self.assertTrue(Path(tmpdir, "SDD", "scripts", "new-backlog-item.sh").exists())
            self.assertTrue(Path(tmpdir, "SDD", "scripts", "new-sprint.sh").exists())
            self.assertTrue(Path(tmpdir, "SDD", "scripts", "new-release.sh").exists())

            script_path = shell_script_path(Path(tmpdir, "SDD", "scripts", "validate-sdd.sh"))
            validate = subprocess.run(
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

            self.assertEqual(validate.returncode, 0, validate.stdout + validate.stderr)
            self.assertIn("[PASS] docs/agile-delivery.md", validate.stdout)

    def test_bootstrap_uses_config_driven_gitignore_and_testing_guide_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.run_bootstrap("--target", tmpdir, "--lang", "en", "--stack", "node")
            self.assertEqual(result.returncode, 0, result.stderr)

            gitignore = Path(tmpdir, ".gitignore").read_text(encoding="utf-8")
            testing_doc = Path(tmpdir, "SDD", "docs", "testing.md").read_text(encoding="utf-8")

            self.assertIn("*.tsbuildinfo", gitignore)
            self.assertIn("- lint: `npm run lint` or `pnpm lint`", testing_doc)
            self.assertIn("- typecheck: `npm run typecheck` or `pnpm typecheck`", testing_doc)
            self.assertNotIn("record the real lint command used in this repo", testing_doc)

    def test_bootstrap_uses_config_driven_next_steps_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.run_bootstrap("--target", tmpdir, "--lang", "en")
            self.assertEqual(result.returncode, 0, result.stderr)

            self.assertIn("Create an ADR with", result.stdout)
            self.assertIn("Use ", result.stdout)
            self.assertIn("handoff-template.ps1", result.stdout)

    def test_bootstrap_generates_next_step_discipline_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            en_result = self.run_bootstrap("--target", tmpdir, "--lang", "en", "--workflow-profile", "full")
            self.assertEqual(en_result.returncode, 0, en_result.stderr)

            progress = Path(tmpdir, "SDD", "docs", "progress.md").read_text(encoding="utf-8")
            process = Path(tmpdir, "SDD", "docs", "process.md").read_text(encoding="utf-8")
            task_template = Path(tmpdir, "SDD", "templates", "tasks", "TASK-template.md").read_text(encoding="utf-8")
            subtask_template = Path(tmpdir, "SDD", "templates", "tasks", "SUBTASK-template.md").read_text(encoding="utf-8")
            backlog_template = Path(tmpdir, "SDD", "templates", "backlog", "BACKLOG-ITEM-template.md").read_text(encoding="utf-8")
            sprint_template = Path(tmpdir, "SDD", "templates", "sprints", "SPRINT-template.md").read_text(encoding="utf-8")
            release_template = Path(tmpdir, "SDD", "templates", "releases", "RELEASE-template.md").read_text(encoding="utf-8")
            git_workflow = Path(tmpdir, "SDD", "docs", "git-workflow.md").read_text(encoding="utf-8")
            testing_doc = Path(tmpdir, "SDD", "docs", "testing.md").read_text(encoding="utf-8")
            root_agents = Path(tmpdir, "AGENTS.md").read_text(encoding="utf-8")

            self.assertIn("Use `[ ]` for unfinished", progress)
            self.assertIn("## Next Options", progress)
            self.assertIn("- [ ] recommended next step:", progress)
            self.assertIn("- [ ] waiting on user decision:", progress)
            self.assertIn("## Git Closure", progress)
            self.assertIn("- [ ] commit status: not committed / committed", progress)
            self.assertIn("before archiving, leave a next-step entry", process)
            self.assertIn("## Completion Handoff", task_template)
            self.assertIn("- [ ] recommended next step:", task_template)
            self.assertIn("- [ ] commit mode: manual / auto", task_template)
            self.assertIn("- [ ] uncommitted reason:", task_template)
            self.assertIn("- [ ] recommended commit message:", task_template)
            self.assertIn("## Completion Handoff", subtask_template)
            self.assertIn("- [ ] commit status: not committed / committed", subtask_template)
            self.assertIn("- [ ] candidate next step:", backlog_template)
            self.assertIn("## Next Options", sprint_template)
            self.assertIn("## Next Options", release_template)
            self.assertIn("## Task Completion Git Closure", git_workflow)
            self.assertIn("TASK_COMPLETION_GIT_MODE", git_workflow)
            self.assertIn("Git closure is documented", testing_doc)
            self.assertIn("Git closure is recorded", root_agents)

        with tempfile.TemporaryDirectory() as tmpdir:
            zh_result = self.run_bootstrap("--target", tmpdir, "--lang", "zh-cn", "--workflow-profile", "full")
            self.assertEqual(zh_result.returncode, 0, zh_result.stderr)

            progress = Path(tmpdir, "SDD", "docs", "progress.md").read_text(encoding="utf-8")
            task_template = Path(tmpdir, "SDD", "templates", "tasks", "TASK-template.md").read_text(encoding="utf-8")
            backlog_template = Path(tmpdir, "SDD", "templates", "backlog", "BACKLOG-ITEM-template.md").read_text(encoding="utf-8")
            git_workflow = Path(tmpdir, "SDD", "docs", "git-workflow.md").read_text(encoding="utf-8")
            testing_doc = Path(tmpdir, "SDD", "docs", "testing.md").read_text(encoding="utf-8")
            root_agents = Path(tmpdir, "AGENTS.md").read_text(encoding="utf-8")

            self.assertIn("用 `[ ]` 标记", progress)
            self.assertIn("- [ ] 交付信心：", progress)
            self.assertIn("## 下一步选项", progress)
            self.assertIn("- [ ] 推荐下一步：", progress)
            self.assertIn("- [ ] 等待用户决策：", progress)
            self.assertIn("## Git handoff", progress)
            self.assertIn("## Blockers", progress)
            self.assertIn("- [ ] commit status：未提交 / 已提交", progress)
            self.assertIn("## Completion Handoff", task_template)
            self.assertIn("- [ ] 未提交原因：", task_template)
            self.assertIn("- [ ] 推荐 commit message：", task_template)
            self.assertIn("- [ ] 候选下一步：", backlog_template)
            self.assertIn("## Task Completion Git Handoff", git_workflow)
            self.assertIn("Git handoff 已记录", testing_doc)
            self.assertIn("Git handoff 已记录", root_agents)
            self.assertNotIn("Git " + "收" + "口", progress + git_workflow + testing_doc + root_agents)

    def test_skill_documents_next_step_and_checkbox_rules(self) -> None:
        content = SKILL_MD.read_text(encoding="utf-8")

        self.assertIn("## Next-Step Discipline", content)
        self.assertIn("Before marking a task or subtask done", content)
        self.assertIn("[ ]` means unfinished", content)
        self.assertIn("[x]` means completed", content)
        self.assertIn("## Git Completion Closure", content)
        self.assertIn("TASK_COMPLETION_GIT_MODE", content)
        self.assertIn("Subagents never own the final commit", content)

    def test_skill_references_route_to_expected_docs(self) -> None:
        content = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("references/quickstart.md", content)
        self.assertIn("references/zh-cn-guide.md", content)
        self.assertIn("references/skill-audit-zh-cn.md", content)
        self.assertIn("references/skill-audit.md", content)
        self.assertNotIn("- `references/README.md`", content)
        self.assertIn("maintainer maps", content)

    def test_skill_entry_docs_are_shell_first_and_cross_platform(self) -> None:
        skill_content = SKILL_MD.read_text(encoding="utf-8")
        quickstart_content = (REPO_ROOT / "references" / "quickstart.md").read_text(encoding="utf-8")
        zh_content = (REPO_ROOT / "references" / "zh-cn-guide.md").read_text(encoding="utf-8")

        self.assertIn("```sh", skill_content)
        self.assertIn("/path/to/repo", skill_content)
        self.assertIn("session-brief.sh", skill_content)
        self.assertIn("validate-sdd.sh --strict", skill_content)

        self.assertIn("/path/to/repo", quickstart_content)
        self.assertIn("Linux, macOS, or WSL", quickstart_content)
        self.assertIn("./SDD/scripts/session-brief.sh", quickstart_content)
        self.assertIn("PowerShell equivalents", quickstart_content)
        self.assertIn("TASK_COMPLETION_GIT_MODE", quickstart_content)
        self.assertIn("record `commit status: not committed`", quickstart_content)

        self.assertIn("/path/to/repo", zh_content)
        self.assertIn("Linux、macOS、WSL", zh_content)
        self.assertIn("./SDD/scripts/session-brief.sh", zh_content)
        self.assertIn("TASK_COMPLETION_GIT_MODE", zh_content)
        self.assertIn("commit status: 未提交", zh_content)
        self.assertNotIn("C:\\Users\\formal\\.codex\\skills\\codex-sdd-workflow", zh_content)

    def test_forward_testing_doc_exists_with_three_core_cases(self) -> None:
        content = FORWARD_TESTING_MD.read_text(encoding="utf-8")

        self.assertIn("## Case 1: Existing Repo Bootstrap", content)
        self.assertIn("## Case 2: Existing Workflow Upgrade", content)
        self.assertIn("## Case 3: Lite vs Full Decision", content)
        self.assertIn("Use $codex-sdd-workflow", content)
        self.assertIn("Failure Signals", content)

    def test_noise_audit_doc_exists_with_low_noise_conclusion(self) -> None:
        content = NOISE_AUDIT_ZH.read_text(encoding="utf-8")

        self.assertIn("# 用户视角噪音审计", content)
        self.assertIn("当前结论：**噪音可控", content)
        self.assertIn("当前最小加载面", content)
        self.assertIn("`SKILL.md` frontmatter", content)
        self.assertIn("普通使用者是低噪音的", content)

    def test_openai_yaml_is_aligned_with_skill_metadata(self) -> None:
        frontmatter = self.load_skill_frontmatter()
        config = yaml.safe_load(OPENAI_YAML.read_text(encoding="utf-8"))
        interface = config["interface"]

        self.assertEqual(interface["display_name"], "Codex SDD Workflow")
        self.assertIn("bootstrap or upgrade", interface["default_prompt"])
        self.assertIn("$codex-sdd-workflow", interface["default_prompt"])
        self.assertIn("lite or full", interface["default_prompt"])
        self.assertIn("existing repo", interface["default_prompt"])
        self.assertIn("workflow", interface["short_description"].lower())
        self.assertIn("durable", frontmatter["description"])

    def test_quick_validate_passes_for_current_skill(self) -> None:
        quick_validate = find_quick_validate(REPO_ROOT)
        if quick_validate is None:
            self.assertEqual(validate_skill_locally(REPO_ROOT), [])
            return

        result = subprocess.run(
            [sys.executable, str(quick_validate), str(REPO_ROOT)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Skill is valid!", result.stdout)

    def test_local_fallback_validator_passes_for_current_skill(self) -> None:
        self.assertEqual(validate_skill_locally(REPO_ROOT), [])

    def test_run_skill_validation_script_supports_static_mode(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SKILL_VALIDATION_SCRIPT), "--skip-tests", "--print-forward-prompts"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("== quick_validate ==", result.stdout)
        self.assertIn("Skill is valid!", result.stdout)
        self.assertIn("== Forward Testing Cases ==", result.stdout)
        self.assertIn("## Case 1: Existing Repo Bootstrap", result.stdout)

    def test_run_skill_validation_script_supports_forced_local_fallback(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SKILL_VALIDATION_SCRIPT), "--skip-tests", "--force-local-validation"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("== quick_validate ==", result.stdout)
        self.assertIn("Using local fallback validator.", result.stdout)
        self.assertIn("Skill is valid!", result.stdout)

    def test_run_skill_validation_script_can_write_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "skill-validation.md"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_VALIDATION_SCRIPT),
                    "--skip-tests",
                    "--print-forward-prompts",
                    "--report",
                    str(report_path),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(report_path.exists())
            report = report_path.read_text(encoding="utf-8")
            self.assertIn("# Skill Validation Report", report)
            self.assertIn("quick_validate: passed", report)
            self.assertIn("unit_tests: " + "skipped", report)
            self.assertIn("forward_testing_prompts: included", report)

    def test_skill_validation_report_template_exists(self) -> None:
        content = REPORT_TEMPLATE.read_text(encoding="utf-8")

        self.assertIn("# Skill Validation Report", content)
        self.assertIn("{generated_at_utc}", content)
        self.assertIn("{quick_validate_status}", content)
        self.assertIn("{unit_tests_status}", content)
        self.assertIn("python ../.system/skill-creator/scripts/quick_validate.py .", content)

    def test_latest_validation_report_records_full_unit_test_pass(self) -> None:
        content = LATEST_VALIDATION_REPORT.read_text(encoding="utf-8")

        self.assertIn("quick_validate: passed", content)
        self.assertIn("unit_tests: passed", content)

    def test_scripts_readme_uses_shell_first_validation_commands(self) -> None:
        content = SCRIPTS_README.read_text(encoding="utf-8")

        self.assertIn("不属于 `SKILL.md` 的默认加载路径", content)
        self.assertIn("```sh\npython -m unittest discover -s tests -p \"test_*.py\" -v", content)
        self.assertIn("```sh\npython scripts/run_skill_validation.py --print-forward-prompts", content)
        self.assertNotIn("```powershell\npython scripts/run_skill_validation.py", content)

    def test_root_gitignore_excludes_local_runtime_artifacts(self) -> None:
        content = ROOT_GITIGNORE.read_text(encoding="utf-8")

        self.assertIn("__pycache__/", content)
        self.assertIn("*.py[cod]", content)
        self.assertIn(".pytest_cache/", content)
        self.assertIn("htmlcov/", content)

    def test_distribution_tree_does_not_include_python_bytecode_caches(self) -> None:
        for cache_dir in [path for path in REPO_ROOT.rglob("__pycache__") if path.is_dir()]:
            shutil.rmtree(cache_dir)

        pycache_dirs = [path for path in REPO_ROOT.rglob("__pycache__") if path.is_dir()]
        pyc_files = list(REPO_ROOT.rglob("*.pyc"))

        self.assertEqual(pycache_dirs, [])
        self.assertEqual(pyc_files, [])

    def test_distribution_files_do_not_embed_personal_machine_paths(self) -> None:
        slash_form = "C:" + "/Users/formal/.codex"
        backslash_form = "C:" + "\\Users\\formal\\.codex"
        files = [
            ROOT_README,
            CONTRIBUTING,
            SECURITY,
            REPO_ROOT / "references" / "forward-testing.md",
            REPO_ROOT / "scripts" / "run_skill_validation.py",
            REPO_ROOT / "scripts" / "skill_validation_report_template.md.tmpl",
            REPO_ROOT / "reports" / "skill-validation.md",
        ]

        for path in files:
            content = path.read_text(encoding="utf-8")
            self.assertNotIn(slash_form, content, str(path))
            self.assertNotIn(backslash_form, content, str(path))

    def test_skill_audit_docs_reference_latest_validation_report(self) -> None:
        zh_content = (REPO_ROOT / "references" / "skill-audit-zh-cn.md").read_text(encoding="utf-8")
        en_content = (REPO_ROOT / "references" / "skill-audit.md").read_text(encoding="utf-8")

        self.assertIn("reports/skill-validation.md", zh_content)
        self.assertIn("reports/skill-validation.md", en_content)
        self.assertNotIn("10 项" + "单元测试", zh_content)
        self.assertNotIn("all 10 " + "unit tests", en_content)
        self.assertIn("当前完整 unittest 套件已通过", zh_content)
        self.assertIn("current full unittest suite passed", en_content)

    def test_root_oss_files_exist_with_release_ready_content(self) -> None:
        readme = ROOT_README.read_text(encoding="utf-8")
        license_text = LICENSE.read_text(encoding="utf-8")
        contributing = CONTRIBUTING.read_text(encoding="utf-8")
        security = SECURITY.read_text(encoding="utf-8")
        changelog = CHANGELOG.read_text(encoding="utf-8")

        self.assertIn("Codex SDD Workflow", readme)
        self.assertIn("Git completion handoff discipline", readme)
        self.assertIn("${CODEX_HOME:-$HOME/.codex}/skills", readme)
        self.assertIn("在 Codex 中使用", readme)
        self.assertIn("先预览将要写入的内容", readme)
        self.assertIn("默认使用 `lite`", readme)
        self.assertIn("full` is beta scaffolding", readme)
        self.assertNotIn("references/README.md", readme)

        self.assertIn("MIT License", license_text)
        self.assertIn("Codex SDD Workflow contributors", license_text)

        self.assertIn("python -m unittest discover", contributing)
        self.assertIn("Do not commit `__pycache__/`", contributing)
        self.assertIn("Reporting", security)
        self.assertIn("target path handling", security)
        self.assertIn("Unreleased", changelog)
        self.assertIn("full` profile: beta scaffolding", changelog)

    def test_ci_workflow_runs_public_validation_path(self) -> None:
        content = CI_WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("python-version", content)
        self.assertIn('"3.11"', content)
        self.assertIn('"3.12"', content)
        self.assertIn("python -m pip install PyYAML", content)
        self.assertIn("python -m unittest discover -s tests -p \"test_*.py\" -v", content)
        self.assertIn("python scripts/run_skill_validation.py --skip-tests --force-local-validation", content)

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
            self.assertIn("- [ ] uncommitted reason: manual mode", result.stdout)
            self.assertIn("- [ ] recommended commit message: chore: test handoff", result.stdout)

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
            self.assertIn("- [ ] uncommitted reason: manual mode", result.stdout)
            self.assertIn("- [ ] recommended commit message: chore: test handoff", result.stdout)

    def test_session_brief_prefers_next_options_section(self) -> None:
        powershell = powershell_executable()
        if not powershell:
            self.skipTest("PowerShell is not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            bootstrap = self.run_bootstrap("--target", tmpdir, "--lang", "en")
            self.assertEqual(bootstrap.returncode, 0, bootstrap.stderr)

            progress = Path(tmpdir, "SDD", "docs", "progress.md")
            progress.write_text(
                "# Progress\n\n"
                "## Git Closure\n\n"
                "- [ ] commit status: not committed\n\n"
                "## Next Options\n\n"
                "- [ ] recommended next step: run the focused regression\n\n"
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
            self.assertIn("## Git Closure", result.stdout)
            self.assertIn("commit status: not committed", result.stdout)
            self.assertIn("## Next Options", result.stdout)
            self.assertIn("recommended next step: run the focused regression", result.stdout)
            self.assertLess(result.stdout.index("## Next Options"), result.stdout.index("## Next\n"))

    def test_zh_session_brief_supports_git_handoff_and_legacy_heading(self) -> None:
        powershell = powershell_executable()
        if not powershell:
            self.skipTest("PowerShell is not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            bootstrap = self.run_bootstrap("--target", tmpdir, "--lang", "zh-cn")
            self.assertEqual(bootstrap.returncode, 0, bootstrap.stderr)

            progress = Path(tmpdir, "SDD", "docs", "progress.md")
            progress.write_text(
                "# 进度记录\n\n"
                "## Git handoff\n\n"
                "- [ ] commit status：未提交\n\n"
                "## 下一步选项\n\n"
                "- [ ] 推荐下一步：运行 targeted regression\n",
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
            self.assertIn("## Git handoff", result.stdout)
            self.assertIn("commit status：未提交", result.stdout)

            legacy_heading = "Git " + "收" + "口"
            progress.write_text(
                "# 进度记录\n\n"
                f"## {legacy_heading}\n\n"
                "- [ ] commit status：未提交\n",
                encoding="utf-8",
            )
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
            self.assertIn(f"## {legacy_heading}", result.stdout)
            self.assertIn("commit status：未提交", result.stdout)

    def test_zh_pack_uses_professional_term_policy(self) -> None:
        forbidden_terms = [
            "Git " + "收" + "口",
            "整体" + "信心",
            "阻塞" + "项",
            "临时绕过" + "方式",
            "质量" + "门槛",
            "流程" + "总览",
            "活跃" + "任务",
            "活跃 " + "task",
            "父" + "任务",
            "子" + "任务",
            "会话" + "交" + "接",
            "交" + "接",
            "骨" + "架",
            "运营" + "清晰度",
        ]
        scan_roots = [
            REPO_ROOT / "assets" / "sdd-pack-zh-cn",
            REPO_ROOT / "references",
            REPO_ROOT / "scripts" / "bootstrap_sdd_templates",
            REPO_ROOT / "scripts" / "bootstrap_sdd_messages.json",
        ]
        checked_files = []

        for root in scan_roots:
            paths = [root] if root.is_file() else list(root.rglob("*"))
            for path in paths:
                if path.suffix not in {".md", ".tmpl", ".json"}:
                    continue
                if path.name.endswith(".en.md.tmpl") or path.name in {"skill-audit.md", "quickstart.md"}:
                    continue
                checked_files.append(path)
                content = path.read_text(encoding="utf-8")
                for term in forbidden_terms:
                    self.assertNotIn(term, content, str(path))

        testing_doc = (REPO_ROOT / "assets" / "sdd-pack-zh-cn" / "docs" / "testing.md").read_text(encoding="utf-8")
        process_doc = (REPO_ROOT / "assets" / "sdd-pack-zh-cn" / "docs" / "process.md").read_text(encoding="utf-8")
        progress_doc = (REPO_ROOT / "assets" / "sdd-pack-zh-cn" / "docs" / "progress.md").read_text(encoding="utf-8")
        subtask_template = (REPO_ROOT / "assets" / "sdd-pack-zh-cn" / "templates" / "tasks" / "SUBTASK-template.md").read_text(encoding="utf-8")
        self.assertIn("# 测试指南", testing_doc)
        self.assertIn("## Quality Gate", testing_doc)
        self.assertIn("# Process Summary", process_doc)
        self.assertIn("active task", progress_doc)
        self.assertIn("parent task", subtask_template)
        self.assertIn("subtask", subtask_template)
        self.assertIn("## Session Handoff", progress_doc)
        self.assertNotIn("# Testing Guide", testing_doc)
        self.assertNotIn("Before claiming a task is done", testing_doc)
        self.assertGreater(len(checked_files), 0)

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
                "## Next Options\n\n"
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
                "## Next Options\n\n"
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
                "- [ ] uncommitted reason: default manual mode\n"
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


if __name__ == "__main__":
    unittest.main()
