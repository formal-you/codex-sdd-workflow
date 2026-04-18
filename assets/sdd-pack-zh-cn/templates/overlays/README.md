# Template Overlay

本目录用于记录当前 overlay manifest，不用于存放日常工作 artifact。

## 规则

- base template 仍然是 parser contract
- overlay 只能覆盖受支持的模板种类
- overlay 不能删除必须存在的标题、checkbox 字段或 Completion Handoff 标记
- 当 `workflow-config.env` 中的 `TEMPLATE_OVERLAY=none` 时，这里通常只保留说明文档
