# 测试指南

## 原则

- 从能暴露本次变更风险的最小测试开始。
- 先做 targeted verification，再决定是否跑完整 suite。
- 只记录本 repo 中真实可运行的命令。

## 快速检查

- workflow 结构：
  - `./SDD/scripts/validate-sdd.ps1 -Strict`
  - `./SDD/scripts/validate-sdd.sh --strict`
- task 启动：
  - `./SDD/scripts/session-brief.ps1`
  - `./SDD/scripts/session-brief.sh`

## 项目级检查

- lint:
- typecheck:
- unit tests:
- integration tests:

## Quality Gate

在声明 task 完成前：

1. targeted tests 已通过
2. 改动文件中没有新增 diagnostics
3. 行为变化、task 状态与风险已经记录
4. Git handoff 已记录：已提交，或未提交并说明原因和推荐 commit message
5. branch、commit 与 PR readiness 符合 `docs/git-workflow.md`
