---
type: ingest-note
source: https://github.com/unslothai/unsloth
date: 2026-08-02
---

# Unsloth：开源LLM训练与推理桌面应用

Unsloth 是一个开源桌面应用，用于在本地运行、训练和部署 AI 模型。项目仓库位于 [unslothai/unsloth](https://github.com/unslothai/unsloth)，目前已有超过 73k Star。它提供了跨平台桌面客户端（Windows / macOS / Linux），并支持多种硬件后端。

## 主要特性

- **运行与构建**：支持各类 LLM（如 Kimi K3、MiniMax-H3、Qwen3.8、Muse Glimmer、DeepSeek-V4、Gemma 4）、扩散模型、嵌入模型和音频模型。
- **Agent 与工具**：可与 Claude Code、Codex、MCP 等工具配合，支持函数调用和代码执行。
- **搜索与 RAG**：支持私有、无限的网页搜索、深度研究（Deep Research）和 RAG。
- **图像与视频**：可运行和训练图像 / 视频扩散或多模态模型。
- **音频**：支持语音相关模型。
- **硬件兼容**：支持 CPU、NVIDIA、AMD、Intel、macOS 以及多 GPU 配置。
- **远程访问**：通过安全的 Cloudflare HTTPS 远程访问本地模型。

## 训练与部署

- **微调**：在 70% 更少 VRAM 下实现 2× 更快的训练（LLM、扩散模型、TTS、嵌入模型），且无精度损失。
- **完整支持**：包括强化学习（RL）、LoRA、QLoRA、全量微调、预训练、GRPO、DPO、FP8 等。
- **导出与部署**：支持导出 GGUF、NVFP4、FP8 等格式。
- **数据集构建**：使用 Data Recipes 从 PDF、CSV、DOCX 等文件构建数据集。
- **OpenAI 兼容 API**：通过 OpenAI 兼容 API 提供服务，并可连接云服务商。

## 快速开始

### 安装

- **Desktop 应用**（推荐）：从官网或 GitHub Releases 下载安装包，无需配置。
- **命令行安装**：
  - macOS / Linux / WSL：`curl -fsSL https://unsloth.ai/install.sh | sh`
  - Windows：`irm https://unsloth.ai/install.ps1 | iex`

### 与 Agent 集成

Unsloth Start 可一键将 Claude Code、Codex 等 Agent 连接到本地模型：

```bash
unsloth start claude
```

支持多个 Agent，并可将本地模型作为子 Agent 使用：

```bash
unsloth start claude --as-subagent --model unsloth/model-GGUF:quant
```

## 使用方式

Unsloth 提供三种使用形态：

1. **Unsloth Desktop**：基于 Tauri 的桌面应用，安装即用。
2. **Unsloth Studio**：Web UI（Beta），支持 Windows / Linux / WSL / macOS，训练支持 RTX 30/40/50、DGX Spark 等，macOS 支持 MLX 与 GGUF 推理，AMD 在 Windows / WSL / Linux 上均可使用。
3. **Unsloth Core**：代码库版本，适合开发者集成。

GGUF 推理引擎可在设置中切换 CPU、CUDA、ROCm 或 Vulkan。

## 社区与技术栈

- 支持多 GPU，且正在重点升级。
- 社区活跃：Discord、X (Twitter)、Reddit。
- 仓库包含大量 notebooks、tests 和命令行工具，使用 Python/PyTorch 实现。

Unsloth 降低了本地 LLM 微调和推理的门槛，是 AI 开发者在私有环境中训练和部署模型的有力工具。

## 平台支持补充

- NVIDIA：RTX 30/40/50、Blackwell、DGX Spark 等训练支持
- AMD：训练、RL、聊天和部署支持（Windows / WSL / Linux 均可）
- Vulkan：支持 Intel GPU 的 GGUF 推理加速，但训练仍需 PyTorch 或 MLX 后端
- macOS：训练、MLX 与 GGUF 推理全部支持
