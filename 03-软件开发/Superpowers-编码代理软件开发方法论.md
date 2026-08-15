---
type: ingest-note
source: https://github.com/obra/superpowers
date: 2025-08-01
---
# Superpowers：编码代理的软件开发方法论

Superpowers 是一套完整的、面向编码代理（coding agents）的软件开发方法论，构建于一组可组合的技能（skills）和初始指令之上，能让代理自动使用这些技能。它支持 Claude Code、Antigravity、Codex App、Codex CLI、Cursor、Factory Droid、Gemini CLI、GitHub Copilot CLI、Kimi Code、OpenCode、Pi 等多种工具。

## 工作原理

当编码代理启动时，Superpowers 会阻止其直接跳入写代码的流程，而是先退一步，询问用户真正想做的事情。代理会从对话中提取出规范（spec），并以足够短的、可阅读的块展示给用户。在用户确认设计后，代理会制定一个清晰、足够详细的实现计划，让一个热情但缺乏判断力和测试意识的新手初级工程师也能遵循。它强调真正的红/绿 TDD、YAGNI 和 DRY 原则。

随后，用户说“开始”后，代理会启动一个子代理驱动的开发（subagent-driven development）过程，让代理逐个完成工程任务，检查并审查工作，然后继续推进。代理通常可以自主工作数小时而不偏离既定计划。

## 商业服务

Superpowers 还提供企业级商业支持、额外工具和托管费用等服务，联系邮箱为 sales@primeradiant.com。

## 安装方式

Superpowers 已发布到各平台的官方插件市场或通过 Git 仓库安装：

- **Claude Code**：可通过 Anthropic 官方插件市场执行 `/plugin install superpowers@claude-plugins-official`，或通过 Superpowers 市场安装。
- **Antigravity**：执行 `agy plugin install https://github.com/obra/superpowers`。
- **Codex App**：在插件商店中找到 Superpowers 并点击 + 安装。
- **Codex CLI**：在 `/plugins` 中搜索 `superpowers` 并安装。
- **Cursor**：在 Agent 聊天中执行 `/add-plugin superpowers`。
- **Factory Droid**：注册市场后安装。
- **Gemini CLI**：执行 `gemini extensions install https://github.com/obra/superpowers`。
- **GitHub Copilot CLI**：注册市场后安装。

每个工具都需要单独安装。

## 项目结构

仓库包含 `.agents/`、`.claude-plugin`、`.codex-plugin`、`.cursor-plugin`、`.kimi-plugin`、`.opencode`、`.pi/`、`plugins`、`skills`、`hooks`、`scripts` 等目录，以及针对不同代理的说明文件（如 `CLAUDE.md`、`GEMINI.md` 等）。

## 总结

Superpowers 通过将需求分析、计划制定、TDD 和子代理协作等过程封装为自动化技能，显著提升编码代理的自主性和代码质量，是 AI 辅助软件开发领域的重要开源项目。
