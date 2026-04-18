from __future__ import annotations

import json
from pathlib import Path

from bootstrap_sdd_fs import merge_tree, write_text


OVERLAY_MANIFEST_PATH = Path("templates") / "overlays" / "active" / "manifest.json"


TEMPLATE_CONTRACTS: dict[str, dict[str, tuple[str, ...]]] = {
    "en": {
        "templates/tasks/TASK-template.md": (
            "# TASK-XXX:",
            "## Status",
            "## Acceptance Criteria",
            "## Completion Handoff",
            "- [ ] commit status:",
            "- [ ] recommended next step:",
        ),
        "templates/tasks/SUBTASK-template.md": (
            "# SUBTASK-XXX:",
            "## Parent Task",
            "## Acceptance Criteria",
            "## Completion Handoff",
            "- [ ] commit status:",
            "- [ ] recommended next step:",
        ),
        "templates/evidence/EVIDENCE-000-template.md": (
            "# EVIDENCE-XXX:",
            "## Goal",
            "## Execution",
            "## Results And Findings",
            "- [ ] expected result:",
            "- [ ] validation result: pass / fail / partial",
        ),
        "templates/releases/RELEASE-template.md": (
            "# RELEASE-XXX:",
            "## Checks",
            "## Next Options",
            "- [ ] CI checks:",
            "- [ ] recommended next step:",
        ),
    },
    "zh-cn": {
        "templates/tasks/TASK-template.md": (
            "# TASK-XXX:",
            "## 状态",
            "## 4. 验收标准 (Acceptance Criteria)",
            "## Completion Handoff",
            "- [ ] Git commit 状态：未提交 / 已提交",
            "- [ ] 推荐的下一步排期 (Next Task)：",
        ),
        "templates/tasks/SUBTASK-template.md": (
            "# SUBTASK-XXX:",
            "## Parent Task",
            "## 验收标准",
            "## Completion Handoff",
            "- [ ] commit status：未提交 / 已提交",
            "- [ ] 推荐下一步：",
        ),
        "templates/evidence/EVIDENCE-000-template.md": (
            "# EVIDENCE-XXX:",
            "## 目标",
            "## 执行",
            "## 结果与发现",
            "- [ ] 预期结果应该是：",
            "- [ ] 验证结论：pass / fail / partial",
        ),
        "templates/releases/RELEASE-template.md": (
            "# RELEASE-XXX:",
            "## Release Checks",
            "## 下一步选项",
            "- [ ] CI checks：",
            "- [ ] 推荐下一步：",
        ),
    },
}


def normalize_overlay_file_list(overlay_root: Path) -> list[str]:
    return sorted(path.relative_to(overlay_root).as_posix() for path in overlay_root.rglob("*") if path.is_file())


def validate_template_overlay(
    overlay_root: Path,
    *,
    lang: str,
    workflow_profile: str,
    supported_paths: tuple[str, ...],
) -> list[str]:
    if not overlay_root.exists():
        raise SystemExit(f"Template overlay path does not exist: {overlay_root}")
    if not overlay_root.is_dir():
        raise SystemExit(f"Template overlay path is not a directory: {overlay_root}")

    files = normalize_overlay_file_list(overlay_root)
    if not files:
        raise SystemExit(f"Template overlay is empty: {overlay_root}")

    allowed = set(supported_paths)
    if workflow_profile != "full":
        allowed.discard("templates/releases/RELEASE-template.md")

    unknown = [rel for rel in files if rel not in allowed]
    if unknown:
        raise SystemExit(
            "Template overlay contains unsupported files. Supported files are "
            + ", ".join(sorted(allowed))
            + f". Unsupported entries: {', '.join(unknown)}"
        )

    contracts = TEMPLATE_CONTRACTS[lang]
    for rel in files:
        required_markers = contracts.get(rel, ())
        content = (overlay_root / rel).read_text(encoding="utf-8")
        missing = [marker for marker in required_markers if marker not in content]
        if missing:
            raise SystemExit(
                f"Template overlay file {rel} breaks the parser contract for {lang}. "
                f"Missing markers: {', '.join(missing)}"
            )

    return files


def overlay_display_name(overlay_root: Path) -> str:
    return overlay_root.name


def apply_template_overlay(
    overlay_root: Path,
    *,
    sdd_target: Path,
    lang: str,
    workflow_profile: str,
    supported_paths: tuple[str, ...],
    dry_run: bool,
) -> str:
    files = validate_template_overlay(
        overlay_root,
        lang=lang,
        workflow_profile=workflow_profile,
        supported_paths=supported_paths,
    )
    merge_tree(overlay_root, sdd_target, dry_run)
    manifest = {
        "overlay_name": overlay_display_name(overlay_root),
        "files": files,
        "lang": lang,
        "workflow_profile": workflow_profile,
    }
    write_text(sdd_target / OVERLAY_MANIFEST_PATH, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", dry_run)
    return manifest["overlay_name"]
