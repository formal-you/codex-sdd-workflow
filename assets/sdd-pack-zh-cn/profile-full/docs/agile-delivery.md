# 敏捷交付

当 workflow 使用 `full` profile 时，请维护本文件。

## 节奏

- backlog 收入口在 `../backlog/items/`
- 当前 sprint 卡片放在 `../sprints/active/`
- 已完成 sprint 卡片归档到 `../sprints/history/`
- 发布计划与发布检查单放在 `../releases/records/`

## 工作循环

1. 用 `new-backlog-item` 记录候选工作
2. 决定哪些 backlog 条目进入下一轮 sprint
3. 用 `new-sprint` 创建 sprint 卡片
4. 把 sprint 里的工作链接到 `../tasks/active/` 下的 task
5. sprint 完成后归档 sprint 卡片，并刷新 `process.md`
6. 如果本轮需要发布，再创建 release 卡片

## 最低维护要求

- sprint goal
- 承诺交付的 backlog 条目
- carry-over 项
- 发布窗口或上线节奏
- 会阻塞交付的 CI/CD 风险
