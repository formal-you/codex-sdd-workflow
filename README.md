# 🚀 Codex SDD Workflow

> **让 Codex 不再"失忆"——一条命令，把可恢复、可审计、可持续迭代的工程工作流注入你的代码仓库。**

---

你是否遇到过这些困境？

- Codex 每次重新进入仓库，都像"第一次来"，完全忘记上次做到哪了？
- 多人协作时，任务没留下决策记录、验证证据或下一步方向？
- Session 意外断开，之前的进度、风险、分析全部丢失？

**Codex SDD Workflow** 就是为了解决这些问题而生的。它在你的仓库内建立一套 **持久化工作区**，让 Codex 每次回来都能立即接续上下文——有任务图、有交接文档、有验证脚本、有完整的执行规范。不靠聊天记忆，靠仓库里的文件。

---

## ✨ 一分钟了解核心能力

| 能力 | 做了什么 | 为什么重要 |
|:---|:---|:---|
| **SDD 持久工作区** | 在仓库中生成 `SDD/` 目录，承载项目简介、架构记录、流程摘要、进度状态 | Codex 每次进入仓库都有稳定的起点，不会"从零开始" |
| **Agent 工作契约** | 自动生成根目录 `AGENTS.md` 和 `README.md` shim | 明确 Codex 的启动顺序、执行边界和行为规范 |
| **结构化任务图** | Parent task → Subtask 的分层任务系统，含验收标准、验证命令、scope 界定 | 复杂工程不会变成"一锅粥"，每步可追踪、可验证 |
| **Session 生存 & 交接** | `session-brief` 脚本 + `handoff` 模板 + `progress.md` 持久状态 | 断连不丢活，换人不丢线——跨 session 无缝恢复 |
| **验证 & 审计链** | 内置 `validate-sdd`、evidence 模板、workflow audit 模板 | 确保流程"真的被执行了"，而非停留在纸面 |
| **下一步指引** | 任务结束前必须留下 next-step 记录 | 每个 session 结束都指向"接下来该做什么"，不会断档 |
| **Git 完成闭环** | 按 `TASK_COMPLETION_GIT_MODE` 管理 commit 状态和推荐 message | 不会静默 commit，也不会忘记记录"为什么没提交" |
| **双 Profile 灵活选择** | `lite` 精准开发 / `full` 敏捷交付 scaffolding | 按需选择，从轻量协作到完整 sprint 管理一步切换 |
| **跨平台支持** | Shell (Linux/macOS/WSL) 为主，PowerShell 完整支持 | Windows、Mac、Linux 团队无缝协作 |

---

## 🎯 谁应该使用它？

- **需要 Codex 长期参与项目演进的开发者** —— 不再每次从头解释背景
- **跨 session 持续推进复杂工程的团队** —— 断连不再是灾难
- **多人 + Codex 混合协作的场景** —— 任务、交接、证据链全部留在仓库里
- **关注工程纪律和可审计性的技术负责人** —— 每一步都有据可查

---

## 📦 安装

### Linux / macOS / WSL

```sh
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone <repo-url> "${CODEX_HOME:-$HOME/.codex}/skills/codex-sdd-workflow"
```

### Windows PowerShell

```powershell
$env:CODEX_HOME = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { "$HOME\.codex" }
git clone <repo-url> "$env:CODEX_HOME\skills\codex-sdd-workflow"
```

安装完成后，**重启 Codex** 让 skill 列表刷新即可。

---

## 🚀 快速上手

安装重启后，用自然语言告诉 Codex 你想做什么——它会自动识别 skill，选择合适的 profile，执行安全预览，然后引导你进入生成的 repo-local workflow。

### 试试这些提示词

```
"请使用 codex-sdd-workflow 给当前仓库初始化一套 SDD workflow，先预览将要写入的内容。"
```
```
"这个仓库已经有旧版 SDD workflow，请帮我安全升级，不要覆盖根目录已有的 README 和 AGENTS。"
```
```
"我不确定该用 lite 还是 full，请先帮我判断，再接入 workflow。"
```
```
"请为这个多人协作项目接入完整 agile delivery scaffolding。"
```

> 💡 **Tip**: 如果你没有明确要求 backlog、sprint、release 或 CI/CD scaffolding，Codex 会默认使用更轻量的 `lite` profile。

### 安装后会发生什么？

**首次接入时**，Codex 会在目标仓库中生成完整的 `SDD/` 工作区、根目录 `AGENTS.md` 和 `README.md` shim，然后阅读它们并帮你创建第一个 parent task，直接进入工作状态。**已有旧版 workflow 时**，Codex 会安全升级现有结构，保留你的任务记录和进度文档，然后继续从上次中断的地方推进。

---

## 🔀 Profile 选择指南

### `lite` —— 精准、轻量、开箱即用 ⭐ 推荐

适用于 **大多数日常开发场景**。覆盖：

- ✅ 持久化开发工作区 & session 恢复
- ✅ 结构化任务卡片 (parent / subtask)  
- ✅ 验收标准 & 验证命令
- ✅ 交接文档 & 下一步指引
- ✅ 主 agent + subagent 协作规范

> 🏷️ **公开场景的默认推荐**。绝大多数仓库从 `lite` 开始就够用了。

### `full` —— 敏捷交付增强 (Beta)

在 `lite` 的基础上扩展，增加：

- 📋 Backlog 管理
- 🏃 Sprint 记录
- 📦 Release 追踪
- 🔄 CI/CD 导向的目录结构和模板

> ⚠️ **注意**：`full` 提供的是 repo-local 的 scaffolding，不是完整的项目管理平台或 CI/CD 编排系统。真正的 issue tracker、PR 审批、release 环境和流水线，仍需要接入你自己的团队系统。

---

## 📂 你的仓库会变成什么样？

以下是 **lite profile** 生成后的完整目录结构（`--no-root-shims` 模式下不会生成根目录的 `AGENTS.md` 和 `README.md`）：

```
your-repo/
├── AGENTS.md                       # 🤖 Codex 的行为契约（启动入口）
├── README.md                       # 📖 项目 shim（指向 SDD workflow）
└── SDD/
    ├── workflow.md                  # 📋 Workflow 总指南：启动流程、文件夹角色、脚本用法
    ├── workflow-config.env          # ⚙️ 运行时配置（Git 模式、profile 等）
    ├── docs/                        # 📝 持久化项目记忆
    │   ├── project-brief.md         #     项目简介与背景
    │   ├── process.md               #     流程摘要：当前焦点、活跃任务、归档历史
    │   ├── progress.md              #     进度状态 & 交接面：下一步、风险、建议
    │   ├── architecture.md          #     架构记录
    │   ├── testing.md               #     测试策略、质量门禁、验证命令参考
    │   ├── git-workflow.md          #     分支命名、Conventional Commits、PR 规范
    │   └── workflow-audit.md        #     Workflow 执行审计记录
    ├── tasks/                       # ✅ 任务管理
    │   ├── active/                  #     进行中的 task 和 subtask
    │   └── history/                 #     已完成并归档的任务
    ├── templates/                   # 📄 模板库（与真实文件物理分离）
    │   ├── tasks/                   #     任务卡片模板
    │   ├── evidence/                #     验证留痕模板（记录测了什么、结果如何）
    │   └── adr/                     #     架构决策记录模板
    ├── adr/records/                 # 🏛️ 架构决策记录（ADR）
    ├── evidence/records/            # 🔍 实际的验证记录存档（由模板生成）
    └── scripts/                     # 🛠️ 日常工作脚本
        ├── session-brief.sh / .ps1  #     Session 恢复摘要
        ├── validate-sdd.sh / .ps1   #     Workflow 合规检查
        ├── new-task.sh / .ps1       #     创建新任务
        ├── new-subtask.sh / .ps1    #     创建子任务
        ├── archive-task.sh / .ps1   #     归档已完成任务
        ├── new-adr.sh / .ps1        #     创建架构决策记录
        └── handoff-template.sh/.ps1 #     生成交接文档
```

> **📎 关键文件联动关系**
>
> **任务生命周期链**：`tasks/active/` 中创建任务 → 开发完成 → 归档到 `tasks/history/` → 同步更新 `docs/process.md`（长期流程摘要）和 `docs/progress.md`（当前进度快照）
>
> **验证留痕链**：参考 `docs/testing.md` 的命令和门禁 → 执行验证 → 基于 `templates/evidence/` 模板填写记录 → 保存到 `evidence/records/` → `validate-sdd --strict` 自动检查是否有留痕
>
> 简单来说：`process.md` 是项目的"长期记忆"，`progress.md` 是当前迭代的"工作台"，`tasks/` 是具体的"待办清单"——三者共同构成 Codex 每次恢复上下文的信息来源。

使用 **full profile** 时，还会额外生成：

```
SDD/
├── backlog/                         # 📋 需求池 / Backlog 管理
├── sprints/                         # 🏃 Sprint 记录
├── releases/                        # 📦 Release 追踪
├── automation/                      # 🔄 CI/CD 自动化配置
└── docs/
    ├── agile-delivery.md            #     敏捷交付流程说明
    └── ci-cd.md                     #     CI/CD 集成指南
```

---

## 🧭 日常使用完全指南

### 1️⃣ 每次开始工作——恢复上下文

```sh
# 查看当前项目状态、活跃任务、上次进度
./SDD/scripts/session-brief.sh          # Linux / macOS / WSL
./SDD/scripts/session-brief.ps1         # Windows PowerShell
```

Codex 也会自动阅读 `AGENTS.md` → `SDD/docs/process.md` → `SDD/workflow.md`，快速回到工作状态。

### 2️⃣ 创建任务——动手之前先建卡

```sh
./SDD/scripts/new-task.sh "实现用户登录模块"
./SDD/scripts/new-subtask.sh "TASK-001" "编写登录 API 端点"
```

> 💡 **为什么要先建卡？** 任务卡片记录了 scope、验收标准和验证命令，防止开发漂移。Codex 在执行前会先检查是否有活跃任务。

### 3️⃣ 开发中——按 scope 推进

- Codex 会自动判断任务是独立完成还是拆分为 subtask 并行推进
- 文件变更、测试记录、风险标注都会随任务卡更新
- 如果一个任务自然拆成多个独立可验证的工作单元，Codex 会优先评估并行拆分

### 4️⃣ 完成任务——验证、记录、闭环

验证链路分三步：

1. **参考 `docs/testing.md`** —— 查看该跑哪些命令、质量门禁有哪些要求
2. **执行验证** —— Codex 按 testing 指南运行测试命令
3. **填写验证记录** —— 基于 `templates/evidence/EVIDENCE-000-template.md` 创建一份验证留痕，保存到 `evidence/records/`

```sh
# 运行 workflow 合规检查
./SDD/scripts/validate-sdd.sh --strict

# 归档已完成的任务
./SDD/scripts/archive-task.sh "TASK-001"
```

> 💡 `validate-sdd --strict` 会检查 `evidence/records/` 下是否有实际的验证记录。如果没有，会给出 warning——所以验证完别忘了留痕。

闭环三件事会自动确保：
1. **验证留痕** —— 基于 evidence 模板记录"测了什么、结果如何、有什么缺口"
2. **下一步指引** —— 指向后续任务或在 `progress.md` 留下推荐方向
3. **Git 状态记录** —— 按 `workflow-config.env` 中的模式处理 commit

### 5️⃣ 交接 / 换人 / 下次继续

```sh
./SDD/scripts/handoff-template.sh
```

生成的交接文档包含：当前状态、未完成项、风险点、推荐 commit message 和下一步建议——无论是自己下次回来还是交给同事，都能无缝衔接。

### 📌 关键文件速查

| 想做什么 | 看哪个文件 |
|:---|:---|
| 了解项目背景和目标 | `SDD/docs/project-brief.md` |
| 查看当前焦点和进度 | `SDD/docs/process.md` + `progress.md` |
| 查阅架构决策 | `SDD/adr/records/` |
| 查找历史任务和经验 | `SDD/tasks/history/` |
| 查看验证证据 | `SDD/evidence/records/` |
| 理解 Git 协作规范 | `SDD/docs/git-workflow.md` |
| 审计 workflow 执行质量 | `SDD/docs/workflow-audit.md` |

---

## ⚠️ 使用注意事项

### 首次接入

- 🔍 **先预览再执行**：首次推荐使用 `--dry-run` 预览生成内容，确认无误后再正式写入
- 📝 **第一时间填写 `project-brief.md`**：这是 Codex 理解你项目的起点，越早填写越好
- 🔀 **已有 README / AGENTS.md 不会被覆盖**：除非你明确使用 `--force-root-shims`

### 日常使用

- ✅ 用 `[ ]` 标记未完成项，`[x]` 标记已完成项——Codex 和脚本都依赖这个约定
- 📂 活跃任务放 `tasks/active/`，完成后及时归档到 `tasks/history/`，保持工作区整洁
- 🚫 **不要手动修改 `templates/` 目录中的模板**——它们是生成新卡片的源，修改会影响后续创建
- 🔄 `process.md` 是长期维护的流程摘要，`progress.md` 是当前迭代的进度快照——不要混淆

### Git 相关

- 默认 `TASK_COMPLETION_GIT_MODE=manual`：Codex **不会自动帮你 commit**
- 每个任务闭环时会记录：commit 状态、未提交原因、推荐 commit message
- Subagent 永远不会拥有 commit 权限——集成和 Git 闭环由主 agent 负责
- 如需自动提交，可在 `workflow-config.env` 中将模式改为 `auto`（请谨慎使用）

### 多人协作

- 每个 subtask 有明确的 scope 边界，文件所有权保持不相交
- 主 agent 负责集成和最终验证，subtask 只报告变更和风险
- 任务卡片和交接文档是协作的通信契约——**请认真填写**

---

## 🛡️ 安全设计哲学

我们在每一个可能造成破坏的环节都设置了 **安全默认值**：

| 行为 | 默认状态 | 说明 |
|:---|:---|:---|
| 覆盖已有 workflow 目录 | ❌ 不覆盖 | 使用 `--force` 明确选择才会覆盖 |
| 替换根目录 `README.md` / `AGENTS.md` | ❌ 不替换 | 需要 `--force-root-shims` 才会替换 |
| Git 自动提交 | ❌ 不自动 | 默认 `TASK_COMPLETION_GIT_MODE=manual` |
| Subagent 提交权限 | ❌ 仅记录 | 最终 commit 和集成始终由主 agent 负责 |

> 🔒 **承诺**：不会在 issue、PR、测试 fixture、验证报告或示例中提交 API key、credential、私有路径或客户数据。

---

## ✅ 验证 & 测试

### 运行完整测试套件

```sh
python -m pip install PyYAML
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/run_skill_validation.py --skip-tests
```

### 生成本地验证报告

```sh
python scripts/run_skill_validation.py --print-forward-prompts --report reports/skill-validation.md
```

> 验证脚本会优先使用已安装的 `skill-creator` 的 `quick_validate.py`；在干净的 CI 环境中，如果没有 system skill，会自动回退到本地 fallback validator——**开箱即用，无需额外依赖**。

---

## 🤝 参与贡献

欢迎提交 Issue 和 PR！贡献前请阅读 [`CONTRIBUTING.md`](./CONTRIBUTING.md)。

**最低验证要求**（PR 前必须通过）：

```sh
python -m pip install PyYAML
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/run_skill_validation.py --skip-tests
```

涉及 skill 触发语义、profile 行为、bootstrap 输出或验证报告的变更，请同时更新 `reports/skill-validation.md`。

---

## 🔐 安全问题

安全漏洞请 **私下联系维护者** 报告，不要公开可利用的细节。详见 [`SECURITY.md`](./SECURITY.md)。

---

## 📄 License

[MIT License](./LICENSE) — 自由使用、修改和分发。

---

<p align="center">
  <em>让每个 session 都从上一次结束的地方开始，而不是从零开始。</em><br/>
  <strong>Codex SDD Workflow</strong> · Built for durable AI-assisted engineering.
</p>
