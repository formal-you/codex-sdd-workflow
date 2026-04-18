from __future__ import annotations

import shutil
from pathlib import Path


def write_text(path: Path, content: str, dry_run: bool) -> None:
    print(f"[WRITE] {path}")
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_file(source: Path, destination: Path, dry_run: bool) -> None:
    print(f"[COPY] {source} -> {destination}")
    if dry_run:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def copy_tree(source: Path, destination: Path, dry_run: bool) -> None:
    print(f"[COPY] {source} -> {destination}")
    if dry_run:
        return
    shutil.copytree(source, destination)


def merge_tree(source: Path, destination: Path, dry_run: bool) -> None:
    print(f"[MERGE] {source} -> {destination}")
    if dry_run:
        return
    shutil.copytree(source, destination, dirs_exist_ok=True)


def workflow_exists_message(sdd_target: Path) -> str:
    return f"Target workflow directory already exists: {sdd_target}\nUse --force to replace it."


def rewrite_sdd_references(content: str, sdd_dir: str) -> str:
    if sdd_dir == "SDD":
        return content

    rewritten = content.replace("/path/to/SDD", f"/path/to/{sdd_dir}")
    rewritten = rewritten.replace("SDD/", f"{sdd_dir}/")
    return rewritten


def rewrite_generated_tree_references(
    sdd_target: Path,
    sdd_dir: str,
    dry_run: bool,
    text_rewrite_suffixes: frozenset[str],
) -> None:
    if sdd_dir == "SDD":
        return

    for path in sorted(sdd_target.rglob("*")):
        if not path.is_file() or path.suffix not in text_rewrite_suffixes:
            continue

        content = path.read_text(encoding="utf-8")
        rewritten = rewrite_sdd_references(content, sdd_dir)
        if rewritten == content:
            continue

        print(f"[REWRITE] {path}")
        if dry_run:
            continue
        path.write_text(rewritten, encoding="utf-8")
