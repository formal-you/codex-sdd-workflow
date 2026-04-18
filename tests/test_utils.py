import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from pathlib import PureWindowsPath

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = REPO_ROOT / "scripts" / "bootstrap_sdd_pack.py"
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from bootstrap_sdd_settings import load_settings
from skill_validation_utils import find_quick_validate, validate_skill_locally

SKILL_MD = REPO_ROOT / "SKILL.md"
OPENAI_YAML = REPO_ROOT / "agents" / "openai.yaml"
FORWARD_TESTING_MD = REPO_ROOT / "references" / "forward-testing.md"
SKILL_VALIDATION_SCRIPT = REPO_ROOT / "scripts" / "run_skill_validation.py"
NOISE_AUDIT_ZH = REPO_ROOT / "references" / "noise-audit-zh-cn.md"
REPORT_TEMPLATE = REPO_ROOT / "scripts" / "skill_validation_report_template.md.tmpl"
SCRIPTS_README = REPO_ROOT / "scripts" / "README.md"
LATEST_VALIDATION_REPORT = REPO_ROOT / "reports" / "skill-validation.md"
ROOT_GITIGNORE = REPO_ROOT / ".gitignore"
ROOT_README = REPO_ROOT / "README.md"
LICENSE = REPO_ROOT / "LICENSE"
CONTRIBUTING = REPO_ROOT / "CONTRIBUTING.md"
SECURITY = REPO_ROOT / "SECURITY.md"
CHANGELOG = REPO_ROOT / "CHANGELOG.md"
CI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"


def powershell_executable() -> str | None:
    return shutil.which("pwsh") or shutil.which("powershell")


def bash_executable() -> str | None:
    return shutil.which("bash")


def shell_script_path(path: Path) -> str:
    resolved = path.resolve()
    if os.name == "nt":
        pure = PureWindowsPath(resolved)
        drive = pure.drive.rstrip(":").lower()
        tail = "/".join(pure.parts[1:])
        return f"/mnt/{drive}/{tail}"
    return resolved.as_posix()



class BootstrapWorkflowTestCase(unittest.TestCase):
    maxDiff = None
    def run_bootstrap(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(BOOTSTRAP), *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def load_skill_frontmatter(self) -> dict[str, str]:
        content = SKILL_MD.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))
        _, frontmatter_text, _ = content.split("---", 2)
        parsed = yaml.safe_load(frontmatter_text)
        self.assertIsInstance(parsed, dict)
        return parsed
