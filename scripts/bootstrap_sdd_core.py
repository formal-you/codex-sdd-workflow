from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from bootstrap_sdd_content import print_next_steps, root_agents, root_readme, testing_guide, workflow_config_content
from bootstrap_sdd_fs import copy_file, copy_tree, merge_tree, rewrite_generated_tree_references, workflow_exists_message, write_text
from bootstrap_sdd_git import maybe_setup_git
from bootstrap_sdd_settings import BootstrapSettings


def create_sdd_tree(
    settings: BootstrapSettings,
    pack_root: Path,
    sdd_target: Path,
    sdd_dir: str,
    lang: str,
    workflow_profile: str,
    root_shims_enabled: bool,
    stack: str,
    force: bool,
    dry_run: bool,
) -> None:
    if sdd_target.exists():
        if not force:
            raise SystemExit(workflow_exists_message(sdd_target))
        print(f"[REMOVE] {sdd_target}")
        if not dry_run:
            shutil.rmtree(sdd_target)

    for directory in settings.core_directories:
        copy_tree(pack_root / directory, sdd_target / directory, dry_run)

    for filename in settings.root_files:
        copy_file(pack_root / filename, sdd_target / filename, dry_run)

    if workflow_profile == "full":
        profile_root = pack_root / settings.full_profile_dir
        if not profile_root.exists():
            raise SystemExit(f"Profile assets not found: {profile_root}")
        merge_tree(profile_root, sdd_target, dry_run)

    write_text(
        sdd_target / "workflow-config.env",
        workflow_config_content(sdd_dir, lang, workflow_profile, root_shims_enabled),
        dry_run,
    )
    write_text(sdd_target / "docs" / "testing.md", testing_guide(settings, stack, lang, sdd_dir), dry_run)

    rewrite_generated_tree_references(sdd_target, sdd_dir, dry_run, settings.text_rewrite_suffixes)


def maybe_write_root_shims(
    target_root: Path,
    sdd_dir: str,
    lang: str,
    overwrite_existing: bool,
    dry_run: bool,
) -> None:
    repo_name = target_root.name or "Repository"
    root_files = {
        target_root / "README.md": root_readme(repo_name, sdd_dir, lang),
        target_root / "AGENTS.md": root_agents(sdd_dir, lang),
    }

    for path, content in root_files.items():
        if path.exists() and not overwrite_existing:
            print(f"[SKIP] {path} already exists")
            continue
        write_text(path, content, dry_run)


def run_bootstrap(args: argparse.Namespace, settings: BootstrapSettings) -> None:
    target_root = Path(args.target).expanduser().resolve()
    sdd_target = target_root / args.sdd_dir
    pack_root = settings.pack_roots[args.lang]

    if not pack_root.exists():
        raise SystemExit(f"Pack assets not found: {pack_root}")
    if not target_root.exists():
        raise SystemExit(f"Target root does not exist: {target_root}")
    if not target_root.is_dir():
        raise SystemExit(f"Target root is not a directory: {target_root}")

    create_sdd_tree(
        settings,
        pack_root,
        sdd_target,
        sdd_dir=args.sdd_dir,
        lang=args.lang,
        workflow_profile=args.workflow_profile,
        root_shims_enabled=not args.no_root_shims,
        stack=args.stack,
        force=args.force,
        dry_run=args.dry_run,
    )

    if not args.no_root_shims:
        maybe_write_root_shims(
            target_root,
            args.sdd_dir,
            args.lang,
            overwrite_existing=args.force_root_shims,
            dry_run=args.dry_run,
        )

    maybe_setup_git(settings, target_root, args.stack, args.lang, args.git_mode, args.dry_run)

    print_next_steps(
        settings,
        target_root,
        args.sdd_dir,
        stack=args.stack,
        lang=args.lang,
        workflow_profile=args.workflow_profile,
        root_shims_enabled=not args.no_root_shims,
    )
