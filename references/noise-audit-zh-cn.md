# 用户视角噪音审计

本文档评估的是：普通使用者在使用 `codex-sdd-workflow` 时，当前 skill 是否会带来不必要的信息噪音。

这里的“噪音”不是指仓库里存在多少维护文档，而是指：在 skill 被触发和执行时，是否会把与当前任务无关的内容推入模型主上下文，或者让使用者看到过多与当前任务无关的说明。

## 结论

当前结论：**噪音可控，且相比前几轮已经下降。**

判断理由：

1. 总是进入触发面的只有 `SKILL.md` frontmatter
2. `SKILL.md` 正文已经收紧为触发与导航层
3. `references/` 已经按职责拆分，不需要默认全部读取
4. `scripts/README.md`、`reports/`、审计稿、forward-testing 用例集都属于维护者资产，不是普通使用者默认读取面

## 当前最小加载面

当 skill 被正确触发时，最小加载面大致是：

1. `SKILL.md` frontmatter
   - 用于判断是否触发 skill
2. `SKILL.md` body
   - 用于确定 bootstrap 主路径、`lite/full` 选择规则、reference 路由
3. 按需读取 1 份 reference
   - 英文短路径通常是 `references/quickstart.md`
   - 中文完整解释通常是 `references/zh-cn-guide.md`

默认情况下，**不会**自动把下面这些都塞进主上下文：

- `references/skill-audit-zh-cn.md`
- `references/skill-audit.md`
- `references/forward-testing.md`
- `scripts/README.md`
- `reports/skill-validation.md`

## 低噪音做得好的地方

1. `SKILL.md` 不再承担完整用户手册角色
2. references 已经按“英文快速路径 / 中文完整指南 / 审计 / 验证”分工
3. bootstrap 细节、开发者说明、验证留痕都被压到了维护层
4. 过期 `examples` 能力已经移除，避免了无效说明进入文档面

## 仍然存在的噪音风险

### 风险 1：`zh-cn-guide.md` 仍然偏长

它现在是“中文完整使用指南”，这是合理的，但如果未来继续往里面叠：

- 维护者说明
- 审计结论
- 版本演进记录

那它就会重新变成一个高噪音大文件。

### 风险 2：`references/README.md` 可能被当成默认入口读太多次

它本来应该只是索引。如果以后往里面塞太多判断逻辑或冗长说明，就会变成次级 `SKILL.md`，造成重复导航。

### 风险 3：审计与验证材料继续增长

当前这些材料没有默认进主上下文，这是对的。但如果以后把审计结论又回塞进 `SKILL.md` 或 guide，就会重新产生噪音。

## 约束建议

为了保持当前低噪音状态，建议继续遵守：

1. `SKILL.md` 只保留触发、主规则、reference 路由
2. `quickstart.md` 保持英文短路径，不扩成完整手册
3. `zh-cn-guide.md` 只承担中文完整使用指南，不吸收维护者材料
4. 审计稿、forward-testing、validation report 只留在维护层
5. 新增 reference 时，先判断它是“用户执行面”还是“维护验证面”

## 审计结论等级

- 触发层噪音：低
- 执行层噪音：低
- references 导航噪音：中低
- 维护层噪音：中，但当前未泄漏到普通使用者路径

总体评价：**当前结构对普通使用者是低噪音的，对维护者则是中等信息量但可接受。**
