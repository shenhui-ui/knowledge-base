---
type: ingest-note
tags:
  - AI
  - Harness
  - Agent
  - 开源
  - DeepSeek
source: InfoQ
date: 2026-08-14
---

# DeepSeek Harness 开源：模型、工具、Agent Loop 全是插件

2026 年 8 月 13 日，DeepSeek 发布 Harness 开发者预览版 v0.1，以 MIT 协议开源。可通过 `npx @deepseek-ai/dsh web` 启动 Web UI，源码位于 https://github.com/deepseek-ai/deepseek-harness 。

## 核心设计：一切皆插件

DeepSeek Harness 将整个运行时拆分为可替换插件：模型、工具、技能、会话、沙箱、存储、Agent Loop、调度和 UI 均由插件组成。工具调用拆成可扩展流水线，包含 Hook、审批、权限检查、沙箱、超时控制等环节，PTC 模式同样不能绕过安全机制。

## 四种运行模式

- 标准模式：完整工具组合，面向常规 Agent 任务
- PTC 模式：程序化工具调用，模型生成代码组合多轮工具调用
- 极简模式：仅 shell 和文件编辑两个工具，用于测试模型能力
- 创造模式：允许 Agent 检查运行时，在内存中试验插件并组合新运行模式

## 多 Agent 系统

内置多 Agent 系统，支持 Spawn（全新上下文）、Fork（继承会话）、workflow 工具（JavaScript 编写 parallel/pipeline）、Ralph 模式（多 Agent 轮次接力）。最接近层级式 Supervisor–Worker 编排，尚未突破范式，但将编排方式做成可配置插件，可接入 Claude Code、Codex 或支持 ACP 的外部 Agent。

## 统一事件流

所有运行轨迹汇入仅追加的会话日志，包括系统提示词、推理内容、工具调用结果、子 Agent 调度等。这解决了可观测性问题，并支持会话分叉、检索与回放。

## 评价与挑战

- 差异化押在架构开放上，但“什么都能换”不自动带来更好任务成功率
- 插件边界深，接口稳定性、依赖管理、性能开销和调试复杂度是挑战
- v0.1 阶段核心接口快速变化，开发者迁移成本高
- MIT 协议开放源码，目标超过封闭客户端，可能成为更多 Agent 产品的底层 Harness

## 参考

- 原文：InfoQ（2026-08-14）
