# Codex SDD Workflow

`codex-sdd-workflow` 是一个面向 Codex 的 SDD workflow skill。它把一套可恢复、可审计、可持续迭代的工程执行流程安装到已有代码仓库中，让 Codex 围绕仓库内的文档、任务和验证记录开展工作，而不是只依赖聊天上下文。

这套 workflow 会在目标 repo 内生成 `SDD/` 工作区，用于承载 project brief、architecture notes、task graph、handoff、evidence、validation scripts、next-step discipline、Git completion handoff discipline，以及可选的 agile delivery scaffolding。它适合希望让 Codex 长期参与项目演进、多人协作或跨 session 持续推进的代码仓库。

## 功能概览

- SDD 工作区：在已有代码仓库中生成 repo-local 的 `SDD/` 目录，保存项目简介、流程摘要、架构记录、测试说明、Git 约定和进度状态。
- Agent 工作契约：默认生成根 `AGENTS.md` 和 `README.md` shim，让 Codex 每次进入仓库时都有稳定的启动顺序和执行边界。
- Task graph：用 parent task 和 subtask 记录拆分决策、owned scope、验收标准、验证命令和最终 handoff。
- Handoff 与恢复：通过 `session-brief`、`handoff-template` 和 `progress.md` 保留跨 session 恢复所需的当前状态、风险、下一步建议和 Git 状态。
- 验证与审计：内置 `validate-sdd`、evidence 模板和 workflow audit 模板，帮助检查 workflow 是否真实被运行、是否还存在占位内容或结构缺口。
- 持续迭代纪律：要求任务结束前留下 next-step entry，并按 `TASK_COMPLETION_GIT_MODE` 记录 commit 状态、未提交原因和推荐 commit message。
- Profile 分层：`lite` 适合准确开发和轻量协作；`full` 增加 backlog、sprint、release 和 CI/CD-oriented scaffolding。
- 跨平台脚本：默认以 Linux/macOS/WSL shell 为主，同时保留 PowerShell 脚本。

## 安装

将本项目克隆到 Codex skills 目录：

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

进入本 skill 目录后，先对目标 repo 执行 dry run：

```sh
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --dry-run
```

确认输出后，使用默认推荐的 lightweight profile：

```sh
python scripts/bootstrap_sdd_pack.py --target /path/to/repo --workflow-profile lite
```

bootstrap 完成后，进入目标 repo，并从生成的 workflow 入口开始：

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

- `lite` 是公开场景下的默认推荐，适合准确开发、session recovery、task card、handoff、验证和主 agent + subagent 执行纪律。
- `full` is beta scaffolding：在 `lite` 基础上增加 backlog、sprint、release 和 CI/CD-oriented 目录与模板。

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

验证脚本会优先使用已安装的 `skill-creator` `quick_validate.py`；在干净的开源 CI 环境中，如果没有 system skill，会自动使用本地 fallback validator。

## Repo 结构

- `SKILL.md`：Codex 触发和导航层，保持精简
- `assets/`：bootstrap 到目标 repo 的 workflow pack
- `scripts/`：bootstrap、配置加载、文件写入、Git 和 skill validation 脚本
- `references/`：按需读取的 skill 参考文档、审计稿和 forward-testing prompt
- `tests/`：bootstrap、metadata、跨 shell、validation、release hygiene 和中文术语策略测试
- `reports/`：显式保留的验证报告

## 设计边界

这个 skill 会在 `--target` 指定的 repo 中生成 workflow assets。建议先用 `--dry-run` 预览，再执行真实 bootstrap。

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
