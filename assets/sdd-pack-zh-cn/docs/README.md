# 文档索引

本目录是仓库的持久化记忆层。

## 阅读顺序

1. `../../AGENTS.md`
2. `../workflow.md`
3. `process.md`
4. `project-brief.md`
5. `architecture.md`
6. `testing.md`
7. `git-workflow.md`
8. `progress.md`
9. `../state/README.md`
10. `../tasks/active/` 中与当前任务相关的文件
11. `../adr/records/` 中相关的决策记录

## 文件职责

- `project-brief.md`：产品目标、用户、范围与约束
- `process.md`：长期项目视角、归档摘要与目录指针
- `architecture.md`：模块划分、ownership 与高风险区域
- `testing.md`：测试命令与 Quality Gate
- `git-workflow.md`：分支命名、提交规范与 PR 准备
- `progress.md`：聚合热状态摘要、Session Handoff 与 context checkpoint
- `workflow-audit.md`：验证 workflow 本身时的评分和结论
- `../state/`：branch-aware 与 task-aware 的热状态便签，避免把 `progress.md` 写成共享热点

## Full Profile 增量内容

如果 workflow 使用 `--workflow-profile full` 生成，本目录还会增加：

- `agile-delivery.md`：backlog、sprint、release 节奏
- `ci-cd.md`：流水线要求和部署门槛
