from test_utils import *


class BootstrapCoreTests(BootstrapWorkflowTestCase):
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
            progress = Path(tmpdir, "SDD", "docs", "progress.md").read_text(encoding="utf-8")
            task_template = Path(tmpdir, "SDD", "templates", "tasks", "TASK-template.md").read_text(encoding="utf-8")
            subtask_template = Path(tmpdir, "SDD", "templates", "tasks", "SUBTASK-template.md").read_text(encoding="utf-8")
            handoff_script = Path(tmpdir, "SDD", "scripts", "handoff-template.sh").read_text(encoding="utf-8")
            self.assertIn("WORKFLOW_PROFILE=lite", config)
            self.assertIn("TASK_COMPLETION_GIT_MODE=manual", config)
            self.assertFalse(Path(tmpdir, "SDD", "docs", "agile-delivery.md").exists())
            self.assertFalse(Path(tmpdir, "SDD", "scripts", "new-sprint.sh").exists())
            self.assertNotIn("backlog item:", progress)
            self.assertNotIn("backlog item:", task_template)
            self.assertNotIn("backlog item:", subtask_template)
            self.assertNotIn("backlog item:", handoff_script)

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

    def test_bootstrap_generates_hot_state_layer_and_config_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.run_bootstrap("--target", tmpdir, "--lang", "en", "--workflow-profile", "lite")
            self.assertEqual(result.returncode, 0, result.stderr)

            config = Path(tmpdir, "SDD", "workflow-config.env").read_text(encoding="utf-8")
            progress = Path(tmpdir, "SDD", "docs", "progress.md").read_text(encoding="utf-8")
            state_root = Path(tmpdir, "SDD", "state")

            self.assertIn("HOT_STATE_MODE=branch-aware", config)
            self.assertIn("HOT_STATE_BRANCH_DIR=state/hot/branches", config)
            self.assertIn("HOT_STATE_TASK_DIR=state/hot/tasks", config)
            self.assertIn("HOT_STATE_HISTORY_DIR=state/history", config)
            self.assertIn("EXTERNAL_ISSUE_SOURCE=none", config)
            self.assertIn("CONNECTOR_MODE=pull-only", config)
            self.assertIn("TEMPLATE_OVERLAY=none", config)
            self.assertTrue((state_root / "README.md").exists())
            self.assertTrue((state_root / "hot" / "branches" / "README.md").exists())
            self.assertTrue((state_root / "hot" / "tasks" / "README.md").exists())
            self.assertTrue((state_root / "history" / "README.md").exists())
            self.assertIn("- [ ] active branch hot state:", progress)
            self.assertIn("- [ ] active task hot state:", progress)
            self.assertIn("- [ ] latest verified summary:", progress)
            self.assertIn("- [ ] branch-aware hot state checked:", progress)

    def test_task_templates_do_not_embed_static_subagent_output_instructions(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.run_bootstrap("--target", tmpdir, "--lang", "en", "--workflow-profile", "full")
            self.assertEqual(result.returncode, 0, result.stderr)

            task_template = Path(tmpdir, "SDD", "templates", "tasks", "TASK-template.md").read_text(encoding="utf-8")
            subtask_template = Path(tmpdir, "SDD", "templates", "tasks", "SUBTASK-template.md").read_text(encoding="utf-8")

            self.assertNotIn("## Output Format For Subagent", task_template)
            self.assertNotIn("## Output Format", subtask_template)
            self.assertNotIn("1. files changed", task_template)
            self.assertNotIn("1. files changed", subtask_template)

    def test_template_overlay_applies_supported_override_and_records_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir, tempfile.TemporaryDirectory() as overlay_tmpdir:
            overlay_root = Path(overlay_tmpdir)
            task_overlay_path = overlay_root / "templates" / "tasks" / "TASK-template.md"
            task_overlay_path.parent.mkdir(parents=True, exist_ok=True)

            base_task_template = (REPO_ROOT / "assets" / "sdd-pack" / "templates" / "tasks" / "TASK-template.md").read_text(encoding="utf-8")
            task_overlay_path.write_text(base_task_template + "\n- [ ] overlay marker: active\n", encoding="utf-8")

            result = self.run_bootstrap(
                "--target",
                tmpdir,
                "--lang",
                "en",
                "--template-overlay",
                str(overlay_root),
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            config = Path(tmpdir, "SDD", "workflow-config.env").read_text(encoding="utf-8")
            task_template = Path(tmpdir, "SDD", "templates", "tasks", "TASK-template.md").read_text(encoding="utf-8")
            manifest = Path(tmpdir, "SDD", "templates", "overlays", "active", "manifest.json").read_text(encoding="utf-8")

            self.assertIn(f"TEMPLATE_OVERLAY={overlay_root.name}", config)
            self.assertIn("overlay marker: active", task_template)
            self.assertIn(f"\"overlay_name\": \"{overlay_root.name}\"", manifest)
            self.assertIn("templates/tasks/TASK-template.md", manifest)

    def test_template_overlay_rejects_contract_breaking_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir, tempfile.TemporaryDirectory() as overlay_tmpdir:
            overlay_root = Path(overlay_tmpdir)
            task_overlay_path = overlay_root / "templates" / "tasks" / "TASK-template.md"
            task_overlay_path.parent.mkdir(parents=True, exist_ok=True)
            task_overlay_path.write_text("# TASK-XXX: broken\n\n## Notes\n\n- [ ] only notes\n", encoding="utf-8")

            result = self.run_bootstrap(
                "--target",
                tmpdir,
                "--lang",
                "en",
                "--template-overlay",
                str(overlay_root),
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("breaks the parser contract", result.stderr)

    def test_full_profile_includes_connector_hooks_and_boundary_docs(self) -> None:
        bash = bash_executable()
        if not bash:
            self.skipTest("bash is not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.run_bootstrap("--target", tmpdir, "--lang", "en", "--workflow-profile", "full")
            self.assertEqual(result.returncode, 0, result.stderr)

            config = Path(tmpdir, "SDD", "workflow-config.env").read_text(encoding="utf-8")
            agile_doc = Path(tmpdir, "SDD", "docs", "agile-delivery.md").read_text(encoding="utf-8")
            ci_cd_doc = Path(tmpdir, "SDD", "docs", "ci-cd.md").read_text(encoding="utf-8")
            backlog_readme = Path(tmpdir, "SDD", "backlog", "README.md").read_text(encoding="utf-8")
            sync_script = shell_script_path(Path(tmpdir, "SDD", "scripts", "sync-external-items.sh"))

            self.assertIn("EXTERNAL_ISSUE_SOURCE=none", config)
            self.assertIn("CONNECTOR_MODE=pull-only", config)
            self.assertIn("## External Source Boundary", agile_doc)
            self.assertIn("## External Source Boundary", ci_cd_doc)
            self.assertIn("execution mirrors", backlog_readme)

            sync = subprocess.run(
                [
                    bash,
                    "-lc",
                    f"\"{sync_script}\"",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(sync.returncode, 0, sync.stdout + sync.stderr)
            self.assertIn("connector hook", sync.stdout)
            self.assertIn("pull external planning context", sync.stdout)

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
            evidence_template = Path(tmpdir, "SDD", "templates", "evidence", "EVIDENCE-000-template.md").read_text(encoding="utf-8")
            adr_template = Path(tmpdir, "SDD", "templates", "adr", "ADR-000-template.md").read_text(encoding="utf-8")
            handoff_script = Path(tmpdir, "SDD", "scripts", "handoff-template.sh").read_text(encoding="utf-8")
            git_workflow = Path(tmpdir, "SDD", "docs", "git-workflow.md").read_text(encoding="utf-8")
            testing_doc = Path(tmpdir, "SDD", "docs", "testing.md").read_text(encoding="utf-8")
            root_agents = Path(tmpdir, "AGENTS.md").read_text(encoding="utf-8")

            self.assertIn("Use `[ ]` for unfinished", progress)
            self.assertIn("## Current", progress)
            self.assertIn("## Recent Findings", progress)
            self.assertIn("## Session Handoff", progress)
            self.assertIn("## Context Checkpoint", progress)
            self.assertIn("## Concurrency", progress)
            self.assertIn("- [ ] recommended next step:", progress)
            self.assertIn("- [ ] backlog item:", progress)
            self.assertIn("- [ ] waiting on user decision:", progress)
            self.assertIn("- [ ] commit status: not committed / committed", progress)
            self.assertIn("- [ ] true goal:", progress)
            self.assertIn("- [ ] context action: continue / compact / new session", progress)
            self.assertNotIn("## Current Context", progress)
            self.assertNotIn("## Next Options", progress)
            self.assertNotIn("## Active Task Cards", progress)
            self.assertIn("## Macro Focus", process)
            self.assertIn("## Rules of Archiving", process)
            self.assertIn("## Recent History", process)
            self.assertIn("## Pointers", process)
            self.assertNotIn("## Current Focus", process)
            self.assertIn("Before archiving work, leave a concrete handoff action", process)
            self.assertIn("- [ ] validation target:", evidence_template)
            self.assertIn("- [ ] command:", evidence_template)
            self.assertIn("- [ ] expected result:", evidence_template)
            self.assertIn("- [ ] finding:", evidence_template)
            self.assertIn("- [ ] change:", evidence_template)
            self.assertIn("- [ ] validation result: pass / fail / partial", evidence_template)
            self.assertIn("## Completion Handoff", task_template)
            self.assertIn("- [ ] recommended next step:", task_template)
            self.assertIn("- [ ] commit mode: manual / auto", task_template)
            self.assertIn("- [ ] uncommitted reason:", task_template)
            self.assertIn("- [ ] recommended commit message:", task_template)
            self.assertIn("- [ ] behavior passes:", task_template)
            self.assertIn("- [ ] regression protection passes:", task_template)
            self.assertIn("- [ ] backlog item:", task_template)
            self.assertNotIn("1. behavior:", task_template)
            self.assertIn("## Completion Handoff", subtask_template)
            self.assertIn("- [ ] commit status: not committed / committed", subtask_template)
            self.assertIn("- [ ] behavior passes:", subtask_template)
            self.assertIn("- [ ] backlog item:", subtask_template)
            self.assertNotIn("1. behavior:", subtask_template)
            self.assertIn("- [ ] candidate next step:", backlog_template)
            self.assertIn("- [ ] scope is understandable", backlog_template)
            self.assertNotIn("1. scope is understandable", backlog_template)
            self.assertIn("## Next Options", sprint_template)
            self.assertIn("## Next Options", release_template)
            self.assertIn("- [ ] CI checks:", release_template)
            self.assertNotIn("1. CI checks:", release_template)
            self.assertIn("- [ ] status: proposed / accepted / superseded / deprecated", adr_template)
            self.assertIn("- [ ] backlog item: ", handoff_script)
            self.assertIn("## Task Completion Git Closure", git_workflow)
            self.assertIn("TASK_COMPLETION_GIT_MODE", git_workflow)
            self.assertIn("Git closure is documented", testing_doc)
            self.assertIn("Git closure is recorded", root_agents)
            self.assertIn("## Session Decay And Checkpoint Rules", root_agents)
            self.assertIn("29%", root_agents)
            self.assertIn("compact context or switch to a new session", root_agents)

        with tempfile.TemporaryDirectory() as tmpdir:
            zh_result = self.run_bootstrap("--target", tmpdir, "--lang", "zh-cn", "--workflow-profile", "full")
            self.assertEqual(zh_result.returncode, 0, zh_result.stderr)

            progress = Path(tmpdir, "SDD", "docs", "progress.md").read_text(encoding="utf-8")
            process = Path(tmpdir, "SDD", "docs", "process.md").read_text(encoding="utf-8")
            task_template = Path(tmpdir, "SDD", "templates", "tasks", "TASK-template.md").read_text(encoding="utf-8")
            subtask_template = Path(tmpdir, "SDD", "templates", "tasks", "SUBTASK-template.md").read_text(encoding="utf-8")
            backlog_template = Path(tmpdir, "SDD", "templates", "backlog", "BACKLOG-ITEM-template.md").read_text(encoding="utf-8")
            evidence_template = Path(tmpdir, "SDD", "templates", "evidence", "EVIDENCE-000-template.md").read_text(encoding="utf-8")
            release_template = Path(tmpdir, "SDD", "templates", "releases", "RELEASE-template.md").read_text(encoding="utf-8")
            adr_template = Path(tmpdir, "SDD", "templates", "adr", "ADR-000-template.md").read_text(encoding="utf-8")
            handoff_script = Path(tmpdir, "SDD", "scripts", "handoff-template.sh").read_text(encoding="utf-8")
            git_workflow = Path(tmpdir, "SDD", "docs", "git-workflow.md").read_text(encoding="utf-8")
            testing_doc = Path(tmpdir, "SDD", "docs", "testing.md").read_text(encoding="utf-8")
            root_agents = Path(tmpdir, "AGENTS.md").read_text(encoding="utf-8")

            self.assertIn("用 `[ ]` 标记", progress)
            self.assertIn("## Current", progress)
            self.assertIn("## Recent Findings", progress)
            self.assertIn("## Session Handoff", progress)
            self.assertIn("## Context Checkpoint", progress)
            self.assertIn("## Concurrency", progress)
            self.assertIn("- [ ] 推荐的下一步明确动作：", progress)
            self.assertIn("- [ ] backlog 条目：", progress)
            self.assertIn("- [ ] 等待用户决策：", progress)
            self.assertIn("- [ ] commit status：未提交 / 已提交", progress)
            self.assertIn("- [ ] 真实目标：", progress)
            self.assertIn("- [ ] context 处理动作：继续 / 开启压缩 / 切换新 session", progress)
            self.assertNotIn("## 当前上下文", progress)
            self.assertNotIn("## 下一步选项", progress)
            self.assertNotIn("## 协作区", progress)
            self.assertIn("## Macro Focus", process)
            self.assertIn("## Rules of Archiving", process)
            self.assertIn("## Recent History", process)
            self.assertIn("## Pointers", process)
            self.assertNotIn("## Current Focus", process)
            self.assertIn("- [ ] 验证目标：", evidence_template)
            self.assertIn("- [ ] command：", evidence_template)
            self.assertIn("- [ ] 预期结果应该是：", evidence_template)
            self.assertIn("- [ ] 实际看到现象是 (Finding)：", evidence_template)
            self.assertIn("- [ ] 根据刚才的发现做出的代码补充 (Change)：", evidence_template)
            self.assertIn("- [ ] 验证结论：pass / fail / partial", evidence_template)
            self.assertIn("## Completion Handoff", task_template)
            self.assertIn("## 1. 目标与背景 (Context)", task_template)
            self.assertIn("## 2. 操作沙盒 (Owned Scope)", task_template)
            self.assertIn("## 3. 执行策略 (Execution Plan)", task_template)
            self.assertIn("## 4. 验收标准 (Acceptance Criteria)", task_template)
            self.assertIn("## 5. 验证记录 (Verification)", task_template)
            self.assertIn("- [ ] 行为指标：当 [执行某操作] 时，预期结果是 [产生某行为]", task_template)
            self.assertIn("- [ ] 架构合规：改动未违背 `AGENTS.md` 及全局规范", task_template)
            self.assertIn("- [ ] 回归防御：确保原有的 [某核心业务] 没有受到破坏", task_template)
            self.assertIn("- [ ] 未提交原因 (如果是 manual 模式)：", task_template)
            self.assertIn("- [ ] 推荐 commit message：", task_template)
            self.assertIn("- [ ] 推荐的下一步排期 (Next Task)：", task_template)
            self.assertIn("- [ ] 对应 evidence：", task_template)
            self.assertIn("- [ ] backlog 条目：", task_template)
            self.assertIn("- [ ] 行为通过：", subtask_template)
            self.assertIn("- [ ] backlog 条目：", subtask_template)
            self.assertNotIn("1. 行为：", subtask_template)
            self.assertIn("- [ ] 候选下一步：", backlog_template)
            self.assertIn("- [ ] scope 已经足够清楚", backlog_template)
            self.assertNotIn("1. scope 已经足够清楚", backlog_template)
            self.assertIn("- [ ] CI checks：", release_template)
            self.assertNotIn("1. CI checks：", release_template)
            self.assertIn("- [ ] status: proposed / accepted / superseded / deprecated", adr_template)
            self.assertIn("- [ ] backlog 条目：", handoff_script)
            self.assertIn("## Task Completion Git Handoff", git_workflow)
            self.assertIn("Git handoff 已记录", testing_doc)
            self.assertIn("Git handoff 已记录", root_agents)
            self.assertIn("## Session 衰减与 Checkpoint 规则", root_agents)
            self.assertIn("达到或超过 29%", root_agents)
            self.assertIn("开启压缩，还是切换到新的 session", root_agents)
            self.assertNotIn("Git " + "收" + "口", progress + git_workflow + testing_doc + root_agents)
