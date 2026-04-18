# References

这个目录存放 `codex-sdd-workflow` skill 自身的参考文档。本文档是维护者地图，不是普通使用者的默认入口。

普通 bootstrap、refresh、first-use 场景应从 `SKILL.md` 直接路由到 `quickstart.md` 或 `zh-cn-guide.md`。只有维护 references 职责边界、审计文档分层或新增参考文档时，才读取本文件。

## 文件职责地图

- `quickstart.md`
  - 英文快速路径
  - 用于最短 bootstrap / refresh / first-use 流程
- `zh-cn-guide.md`
  - 中文完整指南
  - 用于 onboarding、profile 选择、初始化后的操作解释
- `skill-audit-zh-cn.md`
  - 当前 skill 的中文审计稿
  - 只负责评审 skill 本身
- `skill-audit.md`
  - 当前 skill 的英文审计稿
  - 只负责评审 skill 本身
- `forward-testing.md`
  - 固定 forward-testing 用例集
  - 用于验证 skill 触发、`lite/full` 选择、upgrade 安全性与 references 路由
- `architectural-defects-zh-cn.md`
  - 面向维护者的架构批评与 Codex 回应
  - 用于讨论当前 skill 的结构性上限、边界问题与下一轮演进方向
- `noise-audit-zh-cn.md`
  - 用户视角噪音审计
  - 用于评估这个 skill 在真实触发时是否会带来不必要的信息噪音

## 推荐读取顺序

当你在执行普通 skill 任务：

1. 先由 `SKILL.md` 判断要不要触发这个 skill
2. 触发后，如果只需要最短命令流，读 `quickstart.md`
3. 如果需要完整中文解释，读 `zh-cn-guide.md`

当你在维护 skill 本身：

1. 如果是在评估 skill 自身质量，读 `skill-audit-zh-cn.md` 或 `skill-audit.md`
2. 如果是在做真实 skill 验证，读 `forward-testing.md`
3. 如果是在讨论结构性缺陷、适用边界或下一轮架构调整，读 `architectural-defects-zh-cn.md`
4. 如果是在评估普通使用者是否会被过多说明干扰，读 `noise-audit-zh-cn.md`

## 和 assets 的边界

- `references/`
  - skill 本身的说明、导航、评审材料
- `assets/`
  - 将被 bootstrap 到目标仓库里的模板、脚本和 workflow 资产

因此：

- `references/skill-audit-zh-cn.md` 是“当前 skill 的评审结论”
- `assets/sdd-pack-zh-cn/docs/workflow-audit.md` 是“生成给用户仓库后再填写的审计模板”
