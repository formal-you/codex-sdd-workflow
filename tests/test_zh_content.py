from test_utils import *


class ZhContentTests(BootstrapWorkflowTestCase):
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
                "## Current\n\n"
                "- [ ] 总体进度或阶段：focused validation\n\n"
                "## Recent Findings\n\n"
                "- [ ] [2026-04-19] 发现：reproduced the parser issue\n\n"
                "## Session Handoff\n\n"
                "- [ ] commit status：未提交\n"
                "- [ ] 推荐的下一步明确动作：运行 targeted regression\n\n"
                "## Context Checkpoint\n\n"
                "- [ ] 真实目标：保持恢复链稳定\n"
                "- [ ] 最近验证状态：等待 targeted regression\n\n"
                "## Concurrency\n\n"
                "- [ ] 集成状态：single_task\n\n"
                "## Git handoff\n\n"
                "- [ ] commit status：legacy 未提交\n\n"
                "## 下一步选项\n\n"
                "- [ ] 推荐下一步：legacy fallback\n",
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
            self.assertIn("## Current", result.stdout)
            self.assertIn("## Session Handoff", result.stdout)
            self.assertIn("推荐的下一步明确动作：运行 targeted regression", result.stdout)
            self.assertIn("## Context Checkpoint", result.stdout)
            self.assertIn("真实目标：保持恢复链稳定", result.stdout)
            self.assertIn("## Concurrency", result.stdout)
            self.assertIn("## Git handoff", result.stdout)
            self.assertIn("commit status：legacy 未提交", result.stdout)

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
        self.assertIn("# 流程摘要 (Process Summary)", process_doc)
        self.assertIn("Active Task", progress_doc)
        self.assertIn("parent task", subtask_template)
        self.assertIn("subtask", subtask_template)
        self.assertIn("## Session Handoff", progress_doc)
        self.assertIn("## Context Checkpoint", progress_doc)
        self.assertIn("开启压缩 / 切换新 session", progress_doc)
        self.assertIn("## Current", progress_doc)
        self.assertNotIn("## Subagent 输出格式", (REPO_ROOT / "assets" / "sdd-pack-zh-cn" / "templates" / "tasks" / "TASK-template.md").read_text(encoding="utf-8"))
        self.assertNotIn("## 输出格式", subtask_template)
        self.assertNotIn("# Testing Guide", testing_doc)
        self.assertNotIn("Before claiming a task is done", testing_doc)
        self.assertGreater(len(checked_files), 0)

    def test_zh_workflow_keeps_subagent_return_shape_in_workflow_not_task_templates(self) -> None:
        workflow_doc = (REPO_ROOT / "assets" / "sdd-pack-zh-cn" / "workflow.md").read_text(encoding="utf-8")
        task_template = (REPO_ROOT / "assets" / "sdd-pack-zh-cn" / "templates" / "tasks" / "TASK-template.md").read_text(encoding="utf-8")
        subtask_template = (REPO_ROOT / "assets" / "sdd-pack-zh-cn" / "templates" / "tasks" / "SUBTASK-template.md").read_text(encoding="utf-8")

        self.assertIn("统一遵循本 workflow 的返回格式", workflow_doc)
        self.assertNotIn("## Subagent 输出格式", task_template)
        self.assertNotIn("## 输出格式", subtask_template)
        self.assertNotIn("1. 修改的文件", task_template)
        self.assertNotIn("1. 修改的文件", subtask_template)
