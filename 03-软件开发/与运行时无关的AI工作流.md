---
type: ingest-note
source: InfoQ中文
date: 2026-08-13
---

# 与运行时无关的AI工作流：兼顾生产环境稳定性与快速评估迭代

> 本文来自 InfoQ 中文，作者 Mateus Moury，编译平川。介绍一种将 AI 工作流编排逻辑与具体运行环境解耦的模式，源自 Brex 的 AI 工作流平台实践。

## 核心矛盾

AI 工作流是一系列调用 LLM 的步骤组合。生产环境要求：持久化执行、幂等重试、水平扩展。但 LLM 输出会随提示词或模型变化而漂移，必须通过评估验证——需要低成本、可快速重复的轻量循环。这两个需求相互矛盾：持久化需要重量级分布式运行时，评估需要进程内短暂循环。

## 现有框架的问题

- **LangGraph / Mastra**：编排逻辑直接写在框架 SDK 中，控制流变成图的节点/边，评估和部署都必须运行框架本身。
- **Temporal 类引擎**：允许通用语言编写，但强加确定性约束（不能直接 `Date.now()`、不能 I/O），编排代码必须遵循引擎规则。

简单粗暴的替代方案是在评估运行时中重新实现代理，但会导致两份代码漂移，评估与生产不一致。

## 模式：运行时无关的编排

核心是把编排写在一个“可移植内核”中，通过适配器对接不同运行时。编排本身是普通函数，只依赖类型化的 Steps 接口，不导入任何运行时相关库。

```ts
export interface ClassifyBusinessSteps {
  enrichWithWebData(website: string): Promise<string>;
  classify(businessName: string, webContext: string): Promise<string>;
}

export const classifyBusinessAgent = defineAgentHandle({
  name: 'classify_business',
  description: 'Classifies a business given its name and website.',
  orchestration: async (
    steps: ClassifyBusinessSteps,
    input: { businessName: string; website: string },
  ) => {
    const webContext = await steps.enrichWithWebData(input.website);
    return steps.classify(input.businessName, webContext);
  },
});
```

副作用（真实爬虫、LLM 客户端等）通过依赖注入到具体 Steps 实现中。生产环境注入真实服务，评估环境注入稳定测试数据。

## 目录结构

- `agents/`：代理创建者只写这里，每个代理一个文件夹，含编排 + 具体步骤。
- `platform/`：代理依赖的基元和运行时适配器。
- `bin/`：生产工作进程入口和评估循环入口。

新增代理无需改动 platform 层，两个运行时也不会感知新代理。

## 可移植性强制规则

1. 编排中不得存在隐蔽非确定性：不读墙钟时间、不产生随机值、不做直接 I/O（这些操作必须推到 Steps 实现中）。
2. 所有运行时相关依赖都通过注入进入 Steps 实现。

## 实践来源

Brex 的 AI 工作流平台，TypeScript 编写，5 人团队维护；生产环境运行在 Kubernetes + Temporal Cloud，LLM 访问经 Vercel AI SDK 路由到内部网关。该模式在保证生产稳定性的同时，让评估循环能够在本地快速反复运行。
