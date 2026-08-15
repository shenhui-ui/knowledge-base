---
type: ingest-note
source:
  - https://github.com/addyosmani/agent-skills
  - https://github.com/mattpocock/skills
date: 2025-07-31
---

# AI 编码代理工程技能：addyosmani/agent-skills 与 mattpocock/skills

## 概述

[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) 是一个开源仓库，提供「生产级工程技能」（Production-grade engineering skills）。它把资深工程师在构建软件时使用的工作流、质量门禁和最佳实践封装成 AI 编码代理可一致遵循的技能包，覆盖从想法到上线的完整开发阶段。

## 开发生命周期与命令

仓库将开发流程划分为 6 个阶段，并提供 8 个斜杠命令来映射整个生命周期：

- **Define**：/spec —— 先写规格再写代码
- **Plan**：/plan —— 小而原子的任务
- **Build**：/build —— 一次只做一个切片
- **Test**：/test —— 测试就是证明
- **Review**：/review —— 合并前先审查，提升代码健康度
- **Web 性能**：/webperf —— 先测量再优化
- **简化**：/code-simplify —— 清晰胜过聪明
- **Ship**：/ship —— 更快更安全地交付

其中 `/build` 可在规格已经存在时自动生成计划并实施所有任务，只需一次批准计划即可自主运行。它减少了人工步骤，但保留了验证：每个任务仍然以测试驱动的方式单独提交，遇到失败或风险步骤会暂停。

## 技能自动激活

除了斜杠命令，技能也会根据当前工作自动激活。例如设计 API 时触发 `api-and-interface-design`，构建 UI 时触发 `frontend-ui-engineering`。仓库共打包 24 个技能，可通过 CLI 安装到 70+ 种智能体（Claude Code、Cursor、Codex、Copilot、Cline 等）。

## 安装与集成

- **通用 CLI**：`npx skills add addyosmani/agent-skills` 安装全部 24 个技能；`--list` 可浏览后再安装；`--skill <name>` 可单独安装某个技能。
- **Claude Code（推荐）**：通过 `/plugin marketplace add` 和 `/plugin install` 安装，也支持本地开发方式。
- **Cursor**：将技能放到 `.cursor/skills/`，将简短策略放到 `.cursor/rules/*.mdc`，不要把完整技能粘贴进 rules。
- **Antigravity CLI**：支持技能、子代理和斜杠命令的原生插件。

### 注意事项

单独安装一个技能时，只复制 `skills/<name>/`，不会复制仓库级的 `references/` 目录。技能仍可工作，但指向补充共享检查清单的路径会失效。建议使用整个仓库集成、克隆仓库或将所需检查清单复制到已安装技能的 `references/` 目录中。

## 相关项目：mattpocock/skills

[mattpocock/skills](https://github.com/mattpocock/skills) 是另一个广受欢迎（210k stars）的 AI 编码代理技能集。它同样主张「为真正的工程师而开发，而不是 vibe coding」，但设计理念更偏向小而可组合、易于修改。

### 设计理念

与 addyosmani 的完整技能包不同，mattpocock/skills 刻意保持技能体积小、易适配、可组合，并声称适用于任何模型。它不试图拥有整个开发流程（不走 GSD、BMAD、Spec-Kit 等重流程路线），而是基于数十年工程经验的、可 hack 的技能集合。

### 安装方式

支持两条路径，选择其一即可：

- **Claude Code 插件**：`claude plugins install mattpocock-skills` 或会话内 `/plugin install mattpocock-skills`。作为 Claude Code 官方 marketplace 插件，更新自动到达，属于「订阅」模式。
- **可编辑文件**：`npx skills@latest add mattpocock/skills`，将技能以普通文件写入仓库，用户拥有并可自由编辑，之后通过 `npx skills update` 拉取更新。适用于 Codex 及其它代理。

安装后，运行 `/setup-matt-pocock-skills` 进行一次性配置：选择 issue 跟踪器（GitHub、Linear 或本地文件）、triage 标签、以及文档保存位置。

### 核心技能

仓库针对常见失败模式提供修复技能：

- `/grill-me`：在非代码改动前，让 Agent 对你进行详细「拷问」，以对齐需求，避免「Agent 没做我想要的事」。
- `/grill-with-docs`：同 `/grill-me`，但额外结合文档进行更深入的对齐。
- `/triage`：使用标签对 ticket 进行分类（配置阶段指定的标签）。
- `/setup-matt-pocock-skills`：初始化技能配置。

项目还提供 `CONTEXT.md` 等文档，帮助 Agent 解码项目术语，避免使用 20 个词表达 1 个词能说清的事。

### 与 addyosmani/agent-skills 的对比

| 维度 | addyosmani/agent-skills | mattpocock/skills |
| --- | --- | --- |
| 设计哲学 | 6 阶段生命周期 + 24 个标准化技能 | 小型、可组合、可 hack 的技能集 |
| 安装方式 | `npx skills add` + 各 IDE 集成 | Claude Code 插件或 npx 可编辑文件 |
| 核心命令 | /spec, /plan, /build, /test, /review, /ship 等 | /grill-me, /grill-with-docs, /triage, /setup |
| 更新模式 | 技能文件复制到项目 | 插件订阅自动更新或手动更新 |
| 适用模型 | 70+ 种智能体 | 任何模型 |

两者互为补充：addyosmani 侧重流程编排与质量门禁，mattpocock 侧重需求对齐与轻量适配。

## 知识库关联

该仓库为 AI 编码代理提供了可复用的「方法论层」，与知识库中已收录的 AI 编码实践类条目形成互补：

- [[企业AI编码工具成本管理实践]]：关注成本管理，本文关注质量与流程规范。
- [[Python工具调用Agent与MCP服务器集成]]：关注 Agent 工具集成，本文关注 Agent 自身的工程技能。
- [[prime-agent-自改进RLM编码与研究Agent]]：关注自主改进 Agent，本文关注标准化技能套件。

## 参考

- 来源：https://github.com/addyosmani/agent-skills
- 来源：https://github.com/mattpocock/skills
