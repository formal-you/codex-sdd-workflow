# 模板库

本目录只存放模板，不存放真实 workflow artifacts。

## 目录结构

- `overlays/`
  - 当前 overlay manifest 与活动 overlay 快照
- `tasks/`
  - `TASK-template.md`
  - `SUBTASK-template.md`
- `adr/`
  - `ADR-000-template.md`
- `evidence/`
  - `EVIDENCE-000-template.md`

## 规则

- 新 task/subtask/ADR/evidence 一律通过 `SDD/scripts/` 生成
- 真实 artifact 不要回写到 `templates/`
- 如果模板升级，优先通过 skill 升级，再评估是否同步现有仓库
- overlay 只能覆盖受支持的模板种类，且不能破坏必须存在的标题和 checkbox 字段
