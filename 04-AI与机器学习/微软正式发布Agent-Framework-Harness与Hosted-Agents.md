---
title: 微软正式发布 Agent Framework Harness 与 Hosted Agents
type: ingest-note
source: https://www.infoq.com/news/2026/08/agent-framework-harness-ga/
date: 2026-08-10
---

# 微软正式发布 Agent Framework Harness 与 Hosted Agents

微软已将 Agent Framework 从 SDK 阶段推进至受支持的生产运行时。该框架于 2026 年 4 月 2 日发布 1.0 版本；在 Build 2026 大会上，Agent Harness、GitHub Copilot SDK 和 Claude Agent SDK 连接器以及多代理编排模式均已进入稳定发布阶段。此后，Harness 和 Foundry Hosted Agents 正式发布，为平台团队提供了运行和管理代理的途径，而不仅仅是一个用于构建代理的库。

## Harness 是什么？

Agent Harness 是一个运行时环境，作为单个二进制文件，可跨本地开发环境、容器环境和托管部署环境运行。核心思路在于：仅凭模型本身只能生成文本，需要将其封装在运行时环境中才能调用工具、处理多步骤任务并持续运行直至任务完成。Agent Framework 现已内置该运行时，团队无需重新构建。

内置能力默认开启且可单独禁用：

- 函数调用
- 每个历史调用记录的持久化
- 上下文压缩
- 带计划和执行模式的待办事项列表
- 文件记忆
- 技能
- 网络搜索
- 工具审批
- 内置 OpenTelemetry

Shell 工具、文件访问、后台子代理和自动循环仍为可选功能，启用时会发出警告。Foundry Hosted Agents（托管部署目标）按使用量计费。

示例代码（Python）：

```python
client = FoundryChatClient(credential=AzureCliCredential())

agent = create_harness_agent(
    client=client,
    agent_instructions="You are a research assistant. Plan your work, then execute it.",
    tools=[],  # add your own callable tools here
)

response = await agent.run("Research the outlook for renewable energy stocks.")
```

## Harness 占据系统的大部分

MBZUAI VILA 实验室对 Claude Code v2.1.88（泄露的 npm 包）分析后估算：代码库中约 98.4% 的代码属于 Harness 基础设施、权限管理、上下文管理、沙箱机制、工具路由及恢复机制，AI 决策逻辑仅占约 1.6%。类似结构也出现在 Codex CLI 和 Aider 中，表明这是问题约束而非设计选择。

微软自己的对比测试（由 Aqib Sherwani 执行）也得出结论：“推理相同，工程实现不同”——差异仅存在于运行时，关键差异在安全防护失控机制。Agent Framework 在 40 次往返后自行终止循环，而 Copilot SDK 在关闭主机端停止控制的情况下可持续运行至 300 次。

## 编码代理连接器与治理

Agent Framework 的编排功能可通过封装将编码代理与 Azure OpenAI、Anthropic 或自定义代理在同一个工作流中协同工作，无需自定义适配器。这些连接器严格遵循为代理集群设置的身份、内容安全以及可观测性策略。编码代理流量进入相同的 OpenTelemetry 跟踪和 Foundry 仪表板，而不是独立集成。治理核心问题从“代理能做什么”转变为“谁运行了它”“依据什么策略”“跟踪信息最终流向何处”。

## 编排模式与测试框架

编排模式（顺序管道、并行协作、Magentic 模式）与测试框架同步发布稳定版。Magentic-One 在 GAIA 基准测试中达到 38%，AssistantBench 为 27.7%，WebArena 为 32.8%，前两者与当前先进水平相当。这些模式共享一个 API，团队无需重写代理代码即可更改协调风格。

## 对平台团队的意义

此次发布的关键在于运行时而非 SDK：一个受支持的治理框架、按使用量计费的托管目标环境，以及将第三方编码代理视为集群中受管控成员的策略和可观测性模型。该框架、治理框架和连接器已在 GitHub 上发布 .NET 和 Python 版本。
