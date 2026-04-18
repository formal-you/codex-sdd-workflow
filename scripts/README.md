# Bootstrap Developer Notes

这份 README 说明 `codex-sdd-workflow` 里 bootstrap 代码的内部结构，面向维护这个 skill 的开发者，而不是面向最终使用 bootstrap 的用户。

它不属于 `SKILL.md` 的默认加载路径。普通 bootstrap、refresh、first-use 场景不需要读取本文件；只有修改 bootstrap 内部模块、配置、模板或验证链时才读取。

## 目标

当前 bootstrap 代码按下面的原则组织：

- 保持外部 CLI 入口稳定
- 把可配置的数据尽量移出主逻辑
- 把文件系统、内容渲染、Git 初始化、CLI 参数解析分层
- 让新增语言、stack、profile 时，优先改配置或模板，而不是改一整个大脚本

## 模块职责

- `bootstrap_sdd_pack.py`
  - 轻量入口
  - 负责加载配置、解析参数、调用主流程
- `bootstrap_sdd_settings.py`
  - 负责读取 JSON 配置
  - 把原始配置整理成 `BootstrapSettings`
- `bootstrap_sdd_cli.py`
  - 定义 CLI 参数
  - 参数 choices 直接来自配置，而不是硬编码在入口脚本里
- `bootstrap_sdd_core.py`
  - 主流程编排
  - 负责校验目标目录、创建 workflow、写 root shims、调用 Git 初始化、打印 next steps
- `bootstrap_sdd_fs.py`
  - 文件系统操作
  - 包含 copy、merge、write、引用重写等通用能力
- `bootstrap_sdd_git.py`
  - Git 相关逻辑
  - 包括 `.gitignore` 生成、Git 上下文探测、`git init`、嵌套仓库保护
- `bootstrap_sdd_content.py`
  - 内容渲染层
  - 负责 root `README.md`、root `AGENTS.md`、`testing.md`、next steps 的模板与格式化
- `run_skill_validation.py`
  - 半自动 skill 验证入口
  - 负责运行 `quick_validate`、单元测试，并可打印 forward-testing prompt 集
- `skill_validation_report_template.md.tmpl`
  - skill 验证报告模板
  - 负责稳定化 `reports/skill-validation.md` 的输出结构

## 配置与模板

- `bootstrap_sdd_config.json`
  - 结构性配置
  - 包括语言列表、stack 列表、profile 列表、pack 根目录、核心目录等
- `bootstrap_sdd_messages.json`
  - 文案型配置
  - 包括 `.gitignore` 内容片段、next steps 文案、testing guide 默认条目
- `bootstrap_sdd_templates/`
  - Markdown 模板
  - 当前用于 root `README.md`、root `AGENTS.md`、`testing.md`

## 典型扩展方式

### 新增语言

1. 在 `assets/` 下补对应语言 pack
2. 在 `bootstrap_sdd_config.json` 里补 `pack_roots` 和 `lang_choices`
3. 在 `bootstrap_sdd_messages.json` 里补对应语言的 `gitignore` 与 `next_steps`
4. 在 `bootstrap_sdd_templates/` 里补对应语言模板
5. 运行测试并补充必要用例

### 新增 stack

1. 在 `bootstrap_sdd_config.json` 里补 `stack_choices`
2. 在 `bootstrap_sdd_messages.json` 里补该 stack 的 `.gitignore` 片段
3. 在 `bootstrap_sdd_messages.json` 里补该 stack 的 testing guide 默认条目
4. 运行测试并补充必要用例

### 新增 workflow profile

1. 在 `bootstrap_sdd_config.json` 里补 `workflow_profile_choices`
2. 在 `assets/...` 下补 profile 资产目录
3. 在 `bootstrap_sdd_core.py` 中补 profile 装配逻辑
4. 在 `bootstrap_sdd_messages.json` 里补 profile 相关 next steps 文案
5. 更新参考文档与测试

## 什么时候改配置，什么时候改 Python

优先改配置或模板：

- 新增语言
- 新增 stack 映射
- 调整 `.gitignore` 内容
- 调整 next steps 文案
- 调整 testing guide 默认条目
- 调整 root shim / testing guide 文案

需要改 Python：

- 新增新的执行分支
- 新增新的生成阶段
- 修改 profile 装配逻辑
- 修改 Git 检测或文件系统行为
- 修改 validator 依赖的生成契约

## 回归要求

每次改 bootstrap 行为后，至少运行：

```sh
python -m unittest discover -s tests -p "test_*.py" -v
```

如果改动涉及新 profile、新语言、新 stack，应该补对应测试，而不是只依赖手工验证。

当改动涉及 skill 触发语义、references 路由、`lite/full` 选择逻辑或 upgrade 建议时，还应复查：

- `references/forward-testing.md`

它记录了固定的前向验证 prompt、预期行为和失败信号，用来验证这个 skill 作为 skill 是否仍然成立。

如需一键执行当前这套半自动验证链，可运行：

```sh
python scripts/run_skill_validation.py --print-forward-prompts
```

如需留下本地验证记录，可追加：

```sh
python scripts/run_skill_validation.py --print-forward-prompts --report reports/skill-validation.md
```

PowerShell 用户使用相同命令即可；脚本自身会解析当前平台路径。
