---
type: ingest-note
source: https://github.com/vllm-project/vllm/releases/tag/v0.28.0
date: 2026-08-31
---

## vLLM v0.28.0 版本要点

本版包含 584 个提交，来自 270 位贡献者（76 位新贡献者）。

## 主要新特性

- **Kimi-K3 性能专项优化**：Decode Context Parallel (DCP)、融合 FlashKDA 解码/预填充内核、GEMM-RS 序并行、组合 all-gathers 提速 1.5~3 倍、自适应投机 token 预算（DSpark TTFT 提升约 60%）、共享专家分片每 GPU 节省约 17 GiB 内存；新增 ROCm 支持
- **DeepSeek V4**：sparse MLA 端到端支持普通解码、MTP 与 DSpark 投机解码；AMD Quark NVFP4 支持、gfx11/gfx950 ROCm 使能
- **投机解码**：DFlash2（本地卷积 + 候选选择器）、DSpark 置信度调度验证、草稿模型自动启用异步调度
- **Model Runner V2**：E/P/D 分离部署、权重卸载、多层 MTP KV cache、编码器 CUDA graph、thinking_token_budget
- **分层 KV cache 卸载**：磁盘卸载、通过 module_path 的树外二级 tier 管理器、分层指标
- **Rust 前端与 gRPC**：独立渲染器、多模态图像推理、数据并行 rank 路由、RL 生命周期控制
- **新模型**：Muse Glimmer、Ling 3.0 Flash（BF16/MTP/FP8/MXFP4）、Dots3 NOTE 原生多模态

## 性能改进

- 新默认值：`max_num_batched_tokens` 8192 → 16384；Mamba 模型默认开启前缀缓存；Blackwell CUDA graph 捕获上限提升至 1024
- NVIDIA：SM12x FlashInfer XQA 解码、SM100 CuTeDSL 融合查询内核、GB10 融合 MoE FP8 调优
- AMD ROCm：torch 2.12 / triton 3.7 升级、GFX120x 启用 AITER 与 FP8
- CPU：MLA 后端使 DeepSeek-V2/V3 可在 CPU 运行；s390x 支持 GPTQ/AWQ；继续消除执行路径上的 GPU↔CPU 同步

## 重要修复与安全

- 修复通过伪造采样率绕过音频解码时长限制的 DoS 漏洞
- `_load_ov2_processor` 增加 resolve_trust_remote_code 防护；文档警告 `--api-key` 不保护所有端点
- 修复优先级调度静默跳过请求、DP 保留端口活锁、LoRA level-2 sleep/wake/reload
- 单节点 executor 改用 `file://` rendezvous 消除启动端口竞争

## 破坏性变更

- bitsandbytes 支持迁移为树外插件
- Transformers 升级至 5.15.0（huggingface-hub 1.27.0）
- 移除已弃用的 `calculate_kv_scales`、`override_attention_dtype`、MoE 遗留代码
- `reasoning_content` 输出移除；KV 卸载 tier 指标重命名（`..._block_...` → `..._chunk_...`）
- 运行时镜像升级至 Ubuntu 24.04

## See Also

- [[Unsloth-开源LLM训练与推理桌面应用]]
- [[多GPU本地LLM构建FAQ]]
