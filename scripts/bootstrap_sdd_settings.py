from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_ROOT.parent
CONFIG_PATH = SCRIPT_ROOT / "bootstrap_sdd_config.json"
MESSAGES_PATH = SCRIPT_ROOT / "bootstrap_sdd_messages.json"


@dataclass(frozen=True)
class BootstrapSettings:
    skill_root: Path
    pack_roots: dict[str, Path]
    lang_choices: tuple[str, ...]
    stack_choices: tuple[str, ...]
    git_mode_choices: tuple[str, ...]
    workflow_profile_choices: tuple[str, ...]
    text_rewrite_suffixes: frozenset[str]
    core_directories: tuple[str, ...]
    root_files: tuple[str, ...]
    full_profile_dir: str
    supported_template_overlay_paths: tuple[str, ...]
    gitignore_messages: dict[str, dict[str, object]]
    next_steps_messages: dict[str, dict[str, object]]
    testing_guide_defaults: dict[str, dict[str, tuple[str, ...]]]


def load_settings(config_path: Path = CONFIG_PATH, messages_path: Path = MESSAGES_PATH) -> BootstrapSettings:
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    messages = json.loads(messages_path.read_text(encoding="utf-8"))

    return BootstrapSettings(
        skill_root=SKILL_ROOT,
        pack_roots={lang: SKILL_ROOT / relative for lang, relative in raw["pack_roots"].items()},
        lang_choices=tuple(raw["lang_choices"]),
        stack_choices=tuple(raw["stack_choices"]),
        git_mode_choices=tuple(raw["git_mode_choices"]),
        workflow_profile_choices=tuple(raw["workflow_profile_choices"]),
        text_rewrite_suffixes=frozenset(raw["text_rewrite_suffixes"]),
        core_directories=tuple(raw["core_directories"]),
        root_files=tuple(raw["root_files"]),
        full_profile_dir=raw["full_profile_dir"],
        supported_template_overlay_paths=tuple(raw["supported_template_overlay_paths"]),
        gitignore_messages=messages["gitignore"],
        next_steps_messages=messages["next_steps"],
        testing_guide_defaults={
            lang: {stack: tuple(lines) for stack, lines in stacks.items()}
            for lang, stacks in messages["testing_guide_defaults"].items()
        },
    )
