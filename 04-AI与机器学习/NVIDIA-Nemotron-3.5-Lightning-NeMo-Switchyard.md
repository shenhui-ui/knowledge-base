---
type: ingest-note
source: https://blogs.nvidia.com/blog/nemotron-3-5-lightning/
date: 2025-08-01
---

# NVIDIA Nemotron 3.5 Lightning 与 NeMo Switchyard

NVIDIA 发布 Nemotron 3.5 Lightning——面向长时间运行 Agentic AI 工作负载的高效率开放模型，同时发布 NeMo Switchyard 开源模型路由库，帮助企业构建更智能、更高效的 AI Agent 应用。

## 背景：从聊天机器人到自主 Agent

随着 AI 从聊天机器人转向自主代理，开放模型正满足市场对部署位置、运行方式和演进方式的全面控制需求。现代 Agent 系统越来越像“模型集成”（model ensembles）：不同模型负责不同任务。例如，前沿推理模型负责规划与编排，而小型专用模型负责代码审查、工具调用、安全告警监控、账单问答等高频任务。

## Nemotron 3.5 Lightning 核心特性

- 300 亿参数混合专家（MoE）模型，专为多智能体系统内的专业化任务设计
- 开放且可自定义，支持使用 NVIDIA NeMo 在组织自有数据、工具和工作流上进行后训练，提升领域准确度
- 相比同类模型，输出速度最高提升 4 倍，Agentic 任务完成速度提升 30%
- PinchBench 基准显示，在同类模型中兼具前沿准确度和更快任务完成速度
- 支持本地部署：可在 NVIDIA RTX PC、DGX Spark、DGX Station、Jetson 等设备运行，也可扩展到边缘、工作站、数据中心和云端

## 行业验证与应用

已有多个 AI 头部企业基于 Nemotron 3.5 Lightning 进行定制：

- **CrowdStrike**：网络安全
- **Harvey（Trajectory）**：法律服务
- **CodeRabbit（Baseten）**：代码审查
- **Lila Sciences**：物理与生命科学领域的推理能力提升
- **Fastino Labs**：软件研发、金融和医疗健康工作负载取得领先准确度

## 开放与可追溯

NVIDIA 随发布公开训练数据与许可允许范围内的技术细节，支持可追溯性和审计。同时发布 **Nemotron-RL-Agentic-Terminal-Pivot**，一个用于后训练编码 Agent 能力的强化学习数据集。

## NeMo Switchyard：智能模型路由

不同模型分别在编码、推理、轻量任务和本地隐私场景各有优势。NeMo Switchyard 是一个开源模型路由库，能够根据规格自动将 Agent 工作流中每一步的提示路由到最合适、最高效的模型，避免单一默认模型带来的过度开支或质量损失，也无需开发者重写应用。它支持在开发者自己的开放、专有和 NVIDIA 模型组合中进行路由。

## 总结

Nemotron 3.5 Lightning 与 NeMo Switchyard 的组合，让企业更精细地控制 AI 的部署位置、运行方式和运行效率，覆盖 PC、工作站、数据中心和云端，为高频、专业化 Agent 工作负载提供高性价比基础。