# 热状态 (Hot State)

本目录存放高频、局部、可并发的便签，避免所有会话都去改同一个 `../docs/progress.md`。

## 结构

- `branches/`
  - branch-aware 便签，通常每个 branch 一份
- `tasks/`
  - task-aware 便签，通常每个 active task 一份

## 约定

- 保持短、小、可快速恢复
- 共享结论再回写到 `../docs/progress.md`
- task 归档后，按需把旧便签移动到 `../history/`
- 当会话持续较久或 context 已经压缩/恢复时，写入 checkpoint：真实目标、已完成内容、剩余工作、下一步、风险、最近验证状态
