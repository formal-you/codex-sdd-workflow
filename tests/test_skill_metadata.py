from test_utils import *


class SkillMetadataTests(BootstrapWorkflowTestCase):
    def test_skill_description_covers_bootstrap_upgrade_and_profiles(self) -> None:
        frontmatter = self.load_skill_frontmatter()
        description = frontmatter["description"]

        self.assertIn("existing repository", description)
        self.assertIn("initialize or refresh", description)
        self.assertIn("durable docs", description)
        self.assertIn("task graphs", description)
        self.assertIn("branch/task hot-state notes", description)
        self.assertIn("context checkpoints", description)
        self.assertIn("template overlays", description)
        self.assertIn("lite or full", description)
        self.assertIn("connector hooks", description)
        self.assertIn("CI/CD-oriented workflow structure", description)

    def test_skill_documents_next_step_and_checkbox_rules(self) -> None:
        content = SKILL_MD.read_text(encoding="utf-8")

        self.assertIn("## Next-Step Discipline", content)
        self.assertIn("Before marking a task or subtask done", content)
        self.assertIn("[ ]` means unfinished", content)
        self.assertIn("[x]` means completed", content)
        self.assertIn("## Git Completion Closure", content)
        self.assertIn("TASK_COMPLETION_GIT_MODE", content)
        self.assertIn("Subagents never own the final commit", content)
        self.assertIn("## Session Decay And Checkpoint Rules", content)
        self.assertIn("context meter", content)
        self.assertIn("29%", content)
        self.assertIn("compact the context or switch to a new session", content)

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
        self.assertIn("checkpoint", interface["default_prompt"])
        self.assertIn("workflow", interface["short_description"].lower())
        self.assertIn("checkpointed session recovery", interface["short_description"])
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
        self.assertIn("Git 完成闭环", readme)
        self.assertIn("${CODEX_HOME:-$HOME/.codex}/skills", readme)
        self.assertIn("快速上手", readme)
        self.assertIn("先预览将要写入的内容", readme)
        self.assertIn("默认使用更轻量的", readme)
        self.assertIn("(Beta)", readme)
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
