from __future__ import annotations

import subprocess
from pathlib import Path

from bootstrap_sdd_fs import write_text
from bootstrap_sdd_settings import BootstrapSettings


def gitignore_content(settings: BootstrapSettings, stack: str, lang: str) -> str:
    language_spec = settings.gitignore_messages[lang]
    shared_lines = language_spec["shared"]
    stack_lines = language_spec["stacks"][stack]
    return "\n".join([*shared_lines, "", *stack_lines, ""])


def ensure_gitignore(settings: BootstrapSettings, target_root: Path, stack: str, lang: str, dry_run: bool) -> None:
    gitignore_path = target_root / ".gitignore"
    if gitignore_path.exists():
        print(f"[SKIP] {gitignore_path} already exists")
        return
    write_text(gitignore_path, gitignore_content(settings, stack, lang), dry_run)


def detect_git_context(target_root: Path) -> tuple[str, str | None]:
    if (target_root / ".git").exists():
        return "repo-root", str(target_root)

    result = subprocess.run(
        ["git", "-C", str(target_root), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return "no-repo", None

    top_level = result.stdout.strip()
    if not top_level:
        return "no-repo", None

    resolved_top_level = Path(top_level).resolve()
    if resolved_top_level == target_root.resolve():
        return "repo-root", top_level
    return "inside-parent", top_level


def init_git_repo(target_root: Path, dry_run: bool) -> None:
    print(f"[GIT INIT] {target_root}")
    if dry_run:
        return

    primary = subprocess.run(
        ["git", "-C", str(target_root), "init", "--initial-branch", "main"],
        capture_output=True,
        text=True,
        check=False,
    )
    if primary.returncode == 0:
        return

    fallback = subprocess.run(
        ["git", "-C", str(target_root), "init"],
        capture_output=True,
        text=True,
        check=False,
    )
    if fallback.returncode != 0:
        raise SystemExit(primary.stderr.strip() or fallback.stderr.strip() or "git init failed")


def maybe_setup_git(settings: BootstrapSettings, target_root: Path, stack: str, lang: str, git_mode: str, dry_run: bool) -> None:
    ensure_gitignore(settings, target_root, stack, lang, dry_run)

    state, location = detect_git_context(target_root)
    if state == "repo-root":
        print(f"[INFO] Git repository ready at {location}")
        return

    if git_mode == "skip":
        if lang == "zh-cn":
            print("[SKIP] 已跳过 Git 仓库初始化")
        else:
            print("[SKIP] Git repository initialization disabled")
        return

    if state == "inside-parent" and git_mode == "auto":
        if lang == "zh-cn":
            print(f"[INFO] 目标目录位于父 Git 仓库内：{location}")
            print("[INFO] 为避免默认创建嵌套仓库，本次未自动执行 git init；如需独立仓库，请显式使用 --git-mode init。")
        else:
            print(f"[INFO] Target sits inside a parent Git repository: {location}")
            print("[INFO] Skipped automatic git init to avoid creating a nested repo by default. Use --git-mode init when you want a standalone repo here.")
        return

    init_git_repo(target_root, dry_run)
