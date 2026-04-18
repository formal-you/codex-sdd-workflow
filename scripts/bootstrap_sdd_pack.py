from __future__ import annotations

from bootstrap_sdd_cli import parse_args
from bootstrap_sdd_core import run_bootstrap
from bootstrap_sdd_settings import load_settings


def main() -> None:
    settings = load_settings()
    args = parse_args(settings)
    run_bootstrap(args, settings)


if __name__ == "__main__":
    main()
