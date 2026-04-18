# Security Policy

## Reporting

Please report security issues privately to the maintainers before publishing details. If this project is mirrored on a hosting platform, use that platform's private vulnerability reporting feature when available.

Include:

- affected files or scripts
- reproduction steps
- expected impact
- whether the issue affects the skill repository, generated workflow assets, or target repositories

## Scope

This skill can write workflow files into a target repository through `scripts/bootstrap_sdd_pack.py`. Security-sensitive areas include:

- target path handling
- root `README.md` and `AGENTS.md` shim replacement
- generated shell and PowerShell scripts
- Git initialization and `.gitignore` generation
- validation scripts and reports

Use `--dry-run` before replacing an existing workflow. Use `--force-root-shims` only when root files should be regenerated.

## Data Handling

Do not include API keys, credentials, private repository paths, customer data, or local machine identifiers in issues, pull requests, validation reports, or examples.

