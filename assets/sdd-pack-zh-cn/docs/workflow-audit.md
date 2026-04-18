# Workflow 审计

当你在验证或迭代 workflow 本身时，使用本文件。

目标不只是给当前 pack 打分，还要明确：`lite` profile、`full` profile，或者两者，是否已经适合目标使用场景。

## 审计元信息

- 日期：
- 审计人：
- 目标版本或分支：
- 目标受众：
  - internal only / beta users / public release
- 本轮审计的 profile：
  - lite / full / both
- 已检查的 evidence：
  - commands：
  - generated repos：
  - manual flows：
  - automated tests：

## 通用基线

这里评估的是不论 profile 如何都应该成立的 workflow 能力。

| 维度 | 分数 | 备注 |
| --- | --- | --- |
| 跨 session 恢复 | | |
| 委派质量 | | |
| 多 subagent 就绪度 | | |
| 跨 shell 可靠性 | | |
| Evidence 与可审计性 | | |
| Git 协作基线 | | |
| Token 效率潜力 | | |
| 自验证能力 | | |
| Bootstrap 清晰度 | | |
| 通用基线总体 | | |

## Lite Profile 评审

当 workflow 使用 `--workflow-profile lite` 生成时，使用本节。

### Lite 适配度

- 最适合的仓库类型：
- 最适合的团队规模：
- 什么情况下已经足够：
- 什么情况下开始显得不够：

### Lite 评分表

| 维度 | 分数 | 备注 |
| --- | --- | --- |
| 准确执行型 workflow | | |
| parent task / subtask 纪律 | | |
| 低噪音与快速启动 | | |
| 单人或小团队协作 | | |
| 项目渐进演化 | | |
| handoff 质量 | | |
| 轻量敏捷支持 | | |
| 对外采用准备度 | | |
| Lite 总体 | | |

### Lite 做得好的地方

1.
2.
3.

### Lite 缺口

1.
2.
3.

## Full Profile 评审

当 workflow 使用 `--workflow-profile full` 生成时，使用本节。

### Full 适配度

- 最适合的仓库类型：
- 最适合的团队规模：
- 在什么情况下值得引入这套额外流程：
- 在什么情况下会显得过重：

### Full 评分表

| 维度 | 分数 | 备注 |
| --- | --- | --- |
| Backlog 管理支持 | | |
| Sprint 规划支持 | | |
| Release 管理支持 | | |
| CI/CD scaffolding 实用性 | | |
| 多角色协作支持 | | |
| 敏捷交付支持 | | |
| 从 lite 升级到 full 的平滑度 | | |
| 使用清晰度 | | |
| Full 总体 | | |

### Full 做得好的地方

1.
2.
3.

### Full 缺口

1.
2.
3.

## 本轮审计中做过的修改

- 修改：

## 按 Profile 列出风险

### Lite 风险

- 风险：

### Full 风险

- 风险：

## 发布建议

- lite：
  - ship / beta only / internal only / hold
  - 原因：
- full：
  - ship / beta only / internal only / hold
  - 原因：

## 下一步动作

1.
2.
3.
