---
type: ingest-note
source: https://stolen-thoughts.com/
date: 2026-08-13
---
# LLM推理块泄露敏感信息研究

> Source: 待补充（素材未提供链接）
> Date: 待补充（素材未提供日期）

## 概述

一项研究发现，从 GitHub 和 Hugging Face 上收集的 6,708 条公开 AI Agent 轨迹中，可以恢复出被加密的“推理块”（reasoning blocks）中的敏感信息。这些轨迹由 Claude、GPT 和 Gemini 模型生成，仍包含加密的推理块。通过解码管道，研究团队恢复了 315,320 个推理块。

## 泄露规模

- Distinct leaked items: 351
- 技术标识符: 204
- PII: 126
- 凭证: 23

在排除了基准测试会话后，共恢复 704 个隐私工件，包括：

- 62 个 API 密钥
- 33 个密码
- 24 个访问令牌
- 30 个个人电子邮件地址
- 姓名、通信地址、内部 URL 等

其中 64 个工件仅出现在推理块中，而从未出现在可见会话里，说明推理内容本身成为秘密泄露的新渠道。

## 实例：Terminal-Bench 中的 sanitize-git-repo 任务

素材展示了一个来自 GPT-5.2 Codex 的推理示例：在 Terminal-Bench 的“sanitize-git-repo”任务中，模型被要求清除仓库中的 API 密钥。推理过程显示模型逐步用 grep 搜索 `API_KEY`、`apikey`、`secret`、`token` 等模式，最终在 `process.py`、`ray_cluster.yaml` 等文件中找到真实的 AWS Access Key、GitHub Token 和 HuggingFace Token，并计划替换为占位符。此例说明即使模型本身在努力脱敏，推理过程中也会暴露真实凭证，而这些推理块可能被第三方解码恢复。

## 启示

这一发现对 AI Agent 安全、LLM 隐私和密钥管理提出了挑战：模型在推理时可能“自言自语”地处理秘密，而加密的推理块并不等于安全。需要更严格地限制敏感信息进入推理上下文，或确保推理内容真正不可恢复。