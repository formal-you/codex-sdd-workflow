from __future__ import annotations

import argparse

from bootstrap_sdd_settings import BootstrapSettings


def parse_args(settings: BootstrapSettings) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap the Codex SDD workflow pack into a target repository.")
    parser.add_argument("--target", required=True, help="Path to the target repository root.")
    parser.add_argument("--sdd-dir", default="SDD", help="Directory name to create inside the target repo. Default: SDD")
    parser.add_argument("--lang", choices=settings.lang_choices, default="zh-cn", help="Language used for generated workflow docs and script output.")
    parser.add_argument("--stack", choices=settings.stack_choices, default="generic", help="Project stack profile used for template defaults.")
    parser.add_argument("--workflow-profile", choices=settings.workflow_profile_choices, default="lite", help="Workflow profile. lite keeps the pack minimal; full adds backlog, sprint, release, and automation scaffolding.")
    parser.add_argument("--git-mode", choices=settings.git_mode_choices, default="auto", help="Git repo bootstrap mode. auto initializes a repo only when the target is not already inside one.")
    parser.add_argument(
        "--template-overlay",
        help="Optional path to a template overlay directory. Supported overlays may replace specific task, subtask, evidence, or release templates while preserving the parser contract.",
    )
    parser.add_argument("--force", action="store_true", help="Replace an existing workflow directory in the target repo.")
    parser.add_argument("--force-root-shims", action="store_true", help="Also overwrite root README.md and AGENTS.md when they already exist.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing files.")
    parser.add_argument("--no-root-shims", action="store_true", help="Do not create root README.md and AGENTS.md shims.")
    return parser.parse_args()
