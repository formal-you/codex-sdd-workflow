# 热状态目录

本目录用于存放 branch-aware 与 task-aware 的热状态便签。

## 结构

- `hot/`
  - 当前高频更新的局部便签
- `history/`
  - task 归档后仍值得保留的热状态记录

## 规则

- 共享恢复摘要写到 `../docs/progress.md`
- 长期项目视角写到 `../docs/process.md`
- branch/task 级细节写在这里，避免把 `progress.md` 重新写成共享热点
