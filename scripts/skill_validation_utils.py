from __future__ import annotations

import os
import shutil
from pathlib import Path

import yaml


def quick_validate_candidates(skill_root: Path) -> list[Path]:
    candidates: list[Path] = []
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        candidates.append(
            Path(codex_home).expanduser() / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
        )
    candidates.append(skill_root.parent / ".system" / "skill-creator" / "scripts" / "quick_validate.py")
    return candidates


def resolve_quick_validate(skill_root: Path) -> Path:
    for candidate in quick_validate_candidates(skill_root):
        if candidate.exists():
            return candidate.resolve()
    return quick_validate_candidates(skill_root)[-1]


def find_quick_validate(skill_root: Path) -> Path | None:
    for candidate in quick_validate_candidates(skill_root):
        if candidate.exists():
            return candidate.resolve()
    return None


def clean_runtime_caches(skill_root: Path) -> None:
    root = skill_root.resolve()
    for cache_dir in list(root.rglob("__pycache__")):
        resolved = cache_dir.resolve()
        if root not in resolved.parents and resolved != root:
            raise RuntimeError(f"refusing to remove cache outside skill root: {resolved}")
        shutil.rmtree(resolved)


def validate_skill_locally(skill_root: Path) -> list[str]:
    errors: list[str] = []
    clean_runtime_caches(skill_root)
    skill_md = skill_root / "SKILL.md"
    agents_yaml = skill_root / "agents" / "openai.yaml"

    if not skill_md.exists():
        return ["missing SKILL.md"]

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter")
        frontmatter: dict[str, object] = {}
    else:
        try:
            _, frontmatter_text, _ = content.split("---", 2)
            parsed = yaml.safe_load(frontmatter_text)
            frontmatter = parsed if isinstance(parsed, dict) else {}
        except ValueError:
            errors.append("SKILL.md frontmatter must be closed with ---")
            frontmatter = {}
        except yaml.YAMLError as exc:
            errors.append(f"SKILL.md frontmatter is invalid YAML: {exc}")
            frontmatter = {}

    if frontmatter.get("name") != "codex-sdd-workflow":
        errors.append("SKILL.md name must be codex-sdd-workflow")

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("SKILL.md description must be non-empty")
    else:
        required_terms = ["existing repository", "initialize or refresh", "lite or full"]
        for term in required_terms:
            if term not in description:
                errors.append(f"SKILL.md description must mention {term!r}")

    for relative_path in ["agents/openai.yaml", "assets", "references", "scripts"]:
        if not (skill_root / relative_path).exists():
            errors.append(f"missing required skill resource: {relative_path}")

    if agents_yaml.exists():
        try:
            config = yaml.safe_load(agents_yaml.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            errors.append(f"agents/openai.yaml is invalid YAML: {exc}")
            config = {}
        interface = config.get("interface") if isinstance(config, dict) else None
        if not isinstance(interface, dict):
            errors.append("agents/openai.yaml must contain interface mapping")
        else:
            default_prompt = str(interface.get("default_prompt", ""))
            short_description = str(interface.get("short_description", ""))
            if "$codex-sdd-workflow" not in default_prompt:
                errors.append("agents/openai.yaml default_prompt must mention $codex-sdd-workflow")
            if "lite or full" not in default_prompt:
                errors.append("agents/openai.yaml default_prompt must mention lite or full")
            if "workflow" not in short_description.lower():
                errors.append("agents/openai.yaml short_description must mention workflow")

    personal_path_markers = ["C:" + "/Users/formal", "C:" + "\\Users\\formal"]
    checked_suffixes = {".md", ".py", ".yaml", ".yml", ".json", ".tmpl"}
    for path in skill_root.rglob("*"):
        if path.is_dir() and path.name == "__pycache__":
            errors.append(f"runtime cache directory must not be distributed: {path.relative_to(skill_root)}")
        if path.is_file() and path.suffix == ".pyc":
            errors.append(f"compiled Python file must not be distributed: {path.relative_to(skill_root)}")
        if path.is_file() and path.suffix in checked_suffixes:
            text = path.read_text(encoding="utf-8")
            for marker in personal_path_markers:
                if marker in text:
                    errors.append(f"personal machine path leaked in {path.relative_to(skill_root)}")

    return errors
