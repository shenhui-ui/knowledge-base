---
type: ingest-note
source: Hugging Face Model Hub
date: 2026-08
---

# Qwen3.8-27B 模型发布

本文基于 Hugging Face 上的模型卡信息，介绍 Qwen3.8-27B 的 FP8 量化版本及其核心特性。

## 概述

Qwen3.8 是 Qwen 开源模型家族中最强的一代，基于 Qwen3.5 的架构，在编码、专业工作、研究和长周期 Agentic 任务上取得了显著进步。Qwen3.8-27B 是一个紧凑、易于部署的稠密模型，原生支持图像和视频理解，并具备灵活的思维控制能力。

本仓库提供 FP8 量化权重和配置文件，格式为 Hugging Face Transformers，兼容 Transformers、vLLM、SGLang、TokenSpeed 等框架。量化方法为细粒度 FP8，块大小 128，性能与原始模型几乎一致。

## 主要特性

- **核心能力**：编码、专业工作、研究、长周期 Agentic 任务全面改进。
- **Agent 执行**：更强的自主规划能力，更好地处理环境反馈，端到端任务完成更可靠。
- **下游兼容性**：支持更多主流 harness 和开发工具，易于集成。
- **灵活思维控制**：默认开启思维模式，可按请求关闭；可通过 `reasoning_effort` 调节推理深度；通过 `preserve_thinking` 保留历史消息中的推理上下文。
- **视觉-语言理解**：原生支持图像和视频理解，涵盖 STEM 图表、文档乃至小时级视频。

## 模型架构

- 类型：带视觉编码器的因果语言模型
- 训练阶段：预训练 + 后训练
- 参数量：27B
- 隐含维度：5120
- Token 嵌入：248,320（填充后）
- 层数：64
- 隐藏布局：16 × (3 × (Gated DeltaNet → FFN) → 1 × (Gated Attention → FFN))
- Gated DeltaNet：线性注意力头 48（V）和 16（QK），头维度 128
- Gated Attention：注意力头 24（Q）和 4（KV），头维度 256
- 旋转位置嵌入维度：64
- 前馈网络中间维度：17,408
- LM 输出：248,320（填充后）
- MTP（多 Token 预测）：多步训练
- 上下文长度：原生 262,144，可扩展至 1,000,000 tokens

## 基准测试结果

### 文本性能

| 任务 | Qwen3.8-27B | Qwen3.6-27B | Qwen3.7-Plus | Muse Glimmer-30B | Opus4.6 Max |
|---|---|---|---|---|---|
| Agentic 终端编码 Terminal Bench 2.1 (Terminus) | 73.0 | 63.4 | 64.0 | 51.7 | 78.2 |
| Agentic 编码 SWE-bench Pro | 61.7 | 53.5 | 57.6 | 51.2 | 53.4 |
| 仓库级代码生成 NL2Repo-Bench | 42.3 | 36.2 | 41.1 | -- | 47.6 |
| Agentic 编码 DeepSWE 1.1 | 42.2 | 13.3 | 14.2 | -- | -- |
| 软件工程 QwenSWEBench | 79.0 | 49.3 | 59.2 | -- | 63.8 |
| 长周期办公 CoWorkBench | 70.7 | 61.0 | 65.1 | -- | 68.2 |
| 专业任务 JobBench | 33.4 | 21.8 | 27.6 | -- | -- |
| 前沿 Agentic 任务 Agents' Last Exam | Pass@1 20.4, Score 42.9 | Pass@1 10.6, Score 27.3 | Pass@1 13.2, Score 33.6 | -- | -- |
| 指令遵循 IFBench | 79.5 | 69.1 | 79.1 | 77.0 | 62.5 |
| 科学推理 GPQA Diamond | 89.2 | 87.8 | 90.3 | 83.5 | 91.3 |
| 多学科推理 HLE | 30.8 | 24.0 | 34.7 | 22.0 | 40.0 |
| 竞技编码 LiveCodeBench v6 | 90.3 | 83.9 | 89.6 | -- | 88.8 |

**评测说明**：
- SWE-bench Pro：除 Opus4.6 Max 使用官方报告值外，所有模型均使用 Claude Code harness 在 temp=1.0, top_p=0.95, 256K 上下文下评测。已修正问题任务，并重新评估基线模型。
- NL2Repo-Bench：使用 Claude Code harness 评测，禁用访问特定仓库的 Bash 命令以防止奖励攻击。
- DeepSWE 1.1：使用 Claude Code harness，temp=1.0, top_p=0.95, 256K 上下文。
- QwenSWEBench：内部基准，使用 Claude Code harness，avg@3，8 小时超时，max_tokens=32,768，temp=1.0，256K 上下文。
- CoWorkBench：内部基准，覆盖计算机科学、金融、法律、医学等领域的长周期任务。
- HLE：由 GPT-4o 评判。
- 每行最佳结果以粗体显示，-- 表示未报告。

## 可用性

模型权重可在 Hugging Face 仓库获取，FP8 量化版本兼容主流推理框架。官方 Qwen API 服务由 Qwen Cloud 提供，Qwen3.8-27B 托管版将默认支持 1M 上下文和官方内置工具，服务即将推出。
