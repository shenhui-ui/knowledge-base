---
type: ingest-note
source: Netlify Blog
date: 2026-08-01
---

# Netlify携手OpenRouter扩展AI Gateway与Agent Runners模型选择

Netlify宣布与OpenRouter达成合作，为用户带来两项新能力：

- **AI Gateway 支持任意模型**：项目可通过 AI Gateway 调用 OpenRouter 上的任意模型，终端用户在使用基于 AI 推理功能时拥有更广泛的模型选择。
- **Agent Runners 扩展前沿编码模型**：Agent Runners（Netlify 内置的聊天式代理）新增对 Kimi K3、GLM 5.2、DeepSeek V4 等近期热门开源模型的支持，所有模型均以完整编码代理运行，而非简化版本。

Agent Runners 之前支持 Claude Agent、OpenAI Codex、Gemini CLI，现新增开源 OpenCode 作为代理选项。代理具备额外技能和项目上下文意识，能自动决定何时使用 Netlify Database、AI Gateway、Identity 等能力。

Netlify 内部使用开源的 AXIS 工具自动评估模型。评估聚焦生成网站的功能正确性（如是否正确使用数据库、是否过度设计），而非视觉设计。未达标的模型不会在 Agent Runners 中提供；若技能应用失败则优先优化技能。

文章还披露了对三种实际用例的对比测试：本地咖啡店网站、多用户共享待办清单应用、以及基于 AI Gateway 的“能做什么菜”菜谱推荐应用，并比较了各模型的信用点消耗。当前默认将 GPT 5.6 Sol 设置为 low effort，提供比 Opus 更经济的替代选择，且效果不错。后续将分篇深入各场景。

（本则素材为系列文章第一篇，原文截断于咖啡店场景。）