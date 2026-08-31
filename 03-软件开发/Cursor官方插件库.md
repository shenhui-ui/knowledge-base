---
type: ingest-note
source: https://github.com/cursor/plugins
date: 2026-08-01
---

# Cursor 官方插件库

## 概述

Cursor 官方推出了一个插件库仓库，收纳了针对流行开发者工具、框架和 SaaS 产品的官方插件。每个插件以独立目录存在，并带有自己的 `.cursor-plugin/plugin.json` 清单文件。该仓库还包含一些实验性目录和第三方集成。

## 插件列表

### 开发者工具插件

| 插件名 | 作者 | 类别 | 描述 |
|--------|------|------|------|
| continual-learning | Cursor | Developer Tools | 基于转录的增量式记忆更新，仅使用高信号要点更新 AGENTS.md |
| cursor-team-kit | Cursor | Developer Tools | 针对 CI、代码评审、发布、本地自动化和验证的团队内部工作流 |
| thermos | Cursor | Developer Tools | 热核分支评审：深度安全/正确性审计、严格代码质量评分、并行子代理、编排、可选合并 PR 流程 |
| create-plugin | Cursor | Developer Tools | 脚手架并验证新的 agent 插件 |
| agent-compatibility | Cursor | Developer Tools | 基于 CLI 的仓库兼容性扫描及审计代理 |
| cli-for-agent | Cursor | Developer Tools | 面向编码代理可可靠运行的 CLI 设计模式，包括 flags、带示例的 help、管道、错误处理、幂等性和 dry-run 等模式 |
| pr-review-canvas | Cursor | Developer Tools | 将 PR diff 渲染为交互式画布，按重要性分组，分离样板与核心逻辑，并突出意外代码 |
| docs-canvas | Cursor | Developer Tools | 将文档（架构笔记、API 参考、运行手册、代码库导览）渲染为可导航画布，包含章节、目录、图表和交叉引用 |
| cursor-sdk | Cursor | Developer Tools | 基于 Cursor TypeScript SDK（@cursor/sdk）构建应用、脚本、CI 流水线、自动化，涵盖运行时选择、认证、流式、MCP、错误处理及可扩展集成模式 |
| orchestrate | Cursor | Developer Tools | 将大任务分派给并行云代理，包含规划者、工作员、验证者和结构化交接 |
| pstack | Lauren Tan | Developer Tools | 深入优先，写更少但更高质量的代码；可并行化的严格 agent 工作流 |

### 生产力与集成插件

通过远程 MCP 服务器连接各 SaaS 产品，可直接在 Cursor 中操作外部数据。

| 插件名 | 类别 | 描述 |
|--------|------|------|
| Gmail | Productivity | 通过 Google 远程 MCP 服务器连接 Gmail，搜索、读取、草拟、标记和管理电子邮件 |
| Google Drive | Productivity | 通过 Google 远程 MCP 服务器连接 Google Drive，搜索、读取、创建、分享和管理文件 |
| Google Calendar | Productivity | 通过 Google 远程 MCP 服务器连接 Google Calendar，列出日历、搜索事件、创建或更新会议 |
| Gong | Integrations | 面向收入智能的 Gong MCP 集成，提供账户摘要、交易洞察和通话简报 |
| Salesforce | Integrations | 通过 Salesforce Hosted MCP 连接 Salesforce，查询、搜索、创建、更新和遍历组织中的记录 |
| Apollo.io | Integrations | 通过 Apollo 官方远程 MCP 服务器连接 Apollo.io，进行潜在客户搜索、联系人和公司丰富、列表、序列和一次性邮件 |
| Ashby | Integrations | 通过 Ashby 官方远程 MCP 服务器连接 Ashby，搜索候选人和职位、面试准备、管理管道任务和招聘操作 |
| HubSpot | Integrations | 通过 HubSpot 官方远程 MCP 服务器连接 HubSpot CRM，搜索和更新联系人、公司、交易和工单；处理活动、对话和营销邮件 |
| Intercom | Integrations | 通过 Intercom 官方远程 MCP 服务器连接 Intercom，搜索对话和联系人、查找公司、管理帮助中心文章 |

## 目录结构

仓库根目录下除了各插件目录外，还包含：

- `.cursor-plugin/`：插件清单和 schema 相关文件
- `schemas/`：插件配置的 JSON Schema 定义
- `scripts/`：仓库维护脚本
- `third_party/`：第三方相关文件
- `ralph-loop/` 和 `teaching/`：仓库中的新目录（可能是实验性插件或工具）

## 亮点

- 插件采用独立目录 + `plugin.json` 的标准结构，便于扩展和分发。
- 覆盖从代码评审（thermos, pr-review-canvas）到知识管理（continual-learning, docs-canvas）再到云端编排（orchestrate）的完整工作流。
- 集成了多家主流 SaaS 的远程 MCP 服务器，可直接连接外部数据源。
- 针对 agent 工作流提供了 CLI 设计模式（cli-for-agent）和 SDK 集成模式（cursor-sdk），强化自动化可靠性。

## 相关链接

- 仓库地址：https://github.com/cursor/plugins