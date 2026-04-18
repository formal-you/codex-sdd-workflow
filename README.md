# Codex SDD Workflow

`codex-sdd-workflow` 是一个面向 Codex 的 workflow skill，用于在 existing repo 中 bootstrap 或升级一套 repo-local、可恢复、可审计的工程执行工作区。

它会把 task graph、handoff 文档、验证脚本、next-step discipline、Git completion handoff discipline，以及可选的 agile delivery scaffolding 写入目标 repo，让日常状态留在 repo 内，而不是散落在聊天上下文里。

## 功能概览

- 在 existing repo 中生成 `SDD/` workflow 工作区
- 生成根 `AGENTS.md` 和 `README.md` shim，除非显式禁用
- 支持 parent task、subtask、handoff、ADR、evidence 和验证脚本
- 支持 `lite` 与 `full` 两种 profile
- 支持 Linux/macOS/WSL shell，并保留 PowerShell 脚本
- 提供 next-step handoff 和 Git handoff 纪律，方便跨 session 继续推进

## 安装

把本 repo clone 到 Codex skills 目录：

```sh
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone <repo-url> "${CODEX_HOME:-$HOME/.codex}/skills/codex-sdd-workflow"
```

然后重启 Codex，让 skill 列表重新加载。

Windows PowerShell 用户也可以安装到：

```powershell
$env:CODEX_HOME = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { "$HOME\.codex" }
git clone <repo-url> "$env:CODEX_HOME\skills\codex-sdd-workflow"
```

## 快速开始

进入本 skill 目录后，先对目标 repo 做 dry run：

```sh
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --dry-run
```

确认输出后，使用默认推荐的 lightweight profile：

```sh
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --workflow-profile lite
```

bootstrap 完成后，在目标 repo 中从生成的 workflow 入口开始：

```sh
cd /path/to/repo
./SDD/scripts/session-brief.sh
./SDD/scripts/validate-sdd.sh --strict
./SDD/scripts/new-task.sh "Describe the next change"
```

PowerShell 用户使用 `SDD/scripts/` 下对应的 `.ps1` 脚本：

```powershell
./SDD/scripts/session-brief.ps1
./SDD/scripts/validate-sdd.ps1 -Strict
./SDD/scripts/new-task.ps1 "Describe the next change"
```

## Profile 选择

- `lite` 是公开推荐默认值，适合准确开发、session recovery、task card、handoff、验证和主 agent + subagent 执行纪律。
- `full` 是 beta scaffolding，在 `lite` 基础上增加 backlog、sprint、release 和 CI/CD-oriented 目录与模板。

`full` 不是完整的 agile management 平台，也不是 CI/CD orchestration 平台。它提供 repo-local scaffolding，真正的 issue tracker、PR 审批、release 环境和流水线仍需要接入你自己的团队系统。

## 常用命令

```sh
# 预览写入内容
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --dry-run

# 生成 lite profile
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --workflow-profile lite

# 生成 full profile
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --workflow-profile full

# 只刷新生成的 workflow 目录
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --force

# 保留目标 repo 原有根 README.md / AGENTS.md
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --no-root-shims
```

只有在你明确希望重建目标 repo 根目录 `README.md` 和 `AGENTS.md` 时，才使用 `--force-root-shims`。

## 验证

安装测试依赖并运行回归：

```sh
python -m pip install PyYAML
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/run_skill_validation.py --skip-tests
```

需要更新本地验证报告时运行：

```sh
python scripts/run_skill_validation.py --print-forward-prompts --report reports/skill-validation.md
```

验证脚本会优先使用本机 `skill-creator` 的 `quick_validate.py`；在干净的开源 CI 环境中，如果没有 system skill，会自动使用本地 fallback validator。

## Repo 结构

- `SKILL.md`：Codex 触发和导航层，保持精简
- `assets/`：bootstrap 到目标 repo 的 workflow pack
- `scripts/`：bootstrap、配置加载、文件写入、Git 和 skill validation 脚本
- `references/`：按需读取的 skill 参考文档、审计稿和 forward-testing prompt
- `tests/`：bootstrap、metadata、跨 shell、validation、release hygiene 和中文术语策略测试
- `reports/`：显式保留的验证报告

## 设计边界

这个 skill 会向 `--target` 指定的 repo 写入 workflow assets。建议先用 `--dry-run` 预览，再执行真实 bootstrap。

安全默认值：

- 默认不覆盖已有 workflow 目录
- 默认不替换目标 repo 根 `README.md` / `AGENTS.md`
- 默认 `TASK_COMPLETION_GIT_MODE=manual`，不会自动替用户提交 Git 历史
- subagent 不负责最终 commit，最终集成和 Git handoff 由主 agent 负责

不要在 issue、PR、测试 fixture、验证报告或示例中提交 API key、credential、私有 repo 路径、客户数据或本机私有路径。

## 贡献

欢迎提交 issue 和 PR。贡献前请阅读 [`CONTRIBUTING.md`](./CONTRIBUTING.md)。

最低验证要求：

```sh
python -m pip install PyYAML
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/run_skill_validation.py --skip-tests
```

涉及 skill 触发语义、profile 行为、bootstrap 输出或验证报告时，请同时更新 `reports/skill-validation.md`。

## 安全

安全问题请先私下报告维护者，不要直接公开可利用细节。更多说明见 [`SECURITY.md`](./SECURITY.md)。

## License

MIT License. See [`LICENSE`](./LICENSE).
