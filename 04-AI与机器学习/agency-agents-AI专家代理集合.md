---
type: ingest-note
source: https://github.com/msitarzewski/agency-agents
date: 2026-08-12
---
# Agency Agents - 可安装的AI专家代理集合

Agency Agents（仓库名 agency-agents）是一个开源的 AI 专家代理集合，源于 Reddit 讨论并持续迭代，提供一套可安装到多种 AI 编码工具中的专业 AI 代理角色。每个代理都具有领域专长、独特人格、可交付的工作流程和已验证的产出。

## 核心特点

- **专业化**：每个代理聚焦特定领域，而非通用提示词模板。
- **人格驱动**：拥有独特的语气、沟通风格和工作方式。
- **交付导向**：附带真实可用的代码、流程和可度量的业务成果。
- **生产就绪**：包含经过实战测试的工作流和成功指标。

## 快速开始

支持多种安装方式：

1. **桌面应用（推荐）**：提供 macOS / Linux / Windows 原生应用，可浏览全部代理并一键安装到 Claude Code、Cursor、Codex、Gemini、Osaurus 等工具，支持自动更新。可通过 `brew install --cask msitarzewski/agency-agents/agency-agents` 安装。
2. **Claude Code 脚本安装**：运行 `./scripts/install.sh --tool claude-code` 安装全部代理，或将某个分类的 `.md` 文件复制到 `~/.claude/agents/`。
3. **作为参考使用**：每个代理文件包含身份特性、核心任务、技术交付物、代码示例、成功指标和沟通风格。
4. **其他工具**：支持 GitHub Copilot、Antigravity、Gemini CLI、OpenCode、OpenClaw、Cursor、Aider、Windsurf、Kimi Code、Codex、Osaurus、Hermes、Mistral Vibe 等。使用 `./scripts/convert.sh` 生成集成文件，再通过 `./scripts/install.sh --tool <tool>` 交互式安装。

可以通过 `--division` 或 `--agent` 参数选择只安装特定团队或代理。注意 OpenCode 运行时目前仅注册约 119 个代理并静默丢弃其余部分（上游 bug），使用 `--division` 安装子集可避开该限制。

## 代理分类

仓库按部门组织，包括：

- engineering（工程）
- design（设计）
- marketing（营销）
- sales（销售）
- support（支持）
- security（安全）
- finance（财务）
- product（产品）
- project-management（项目管理）
- game-development（游戏开发）
- healthcare（医疗）
- gis（地理信息）
- spatial-computing（空间计算）
- academic（学术）
- strategy（战略）
- specialized（专门领域）
- paid-media（付费媒体）
- testing（测试）
- integrations（集成）
- examples（示例）
- scripts（脚本）

每个分类下包含多个专家代理定义，可直接复制或安装使用。

## 使用场景

- 在 Claude Code 中激活特定专家模式，例如“前端开发者模式”来构建 React 组件。
- 通过 Cursor 等编辑器获得领域专属 AI 助手。
- 作为团队模板，为不同项目快速配置所需的 AI 角色。

---

- source: https://github.com/msitarzewski/agency-agents
- date: 2026-08-01
