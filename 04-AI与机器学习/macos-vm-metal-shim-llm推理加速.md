---
type: ingest-note
date: 2026-08-11
source: https://github.com/trycua/cua/blob/main/gpu-passthrough-macos-vms.md
---

# macOS虚拟机Metal能力垫片：llama.cpp推理加速11–16倍

## 概述

trycua/cua 发布了一项研究：在 Apple Silicon 的 macOS 虚拟机中，通过一个进程级的 Metal 能力垫片（compatibility shim），让 llama.cpp 等应用选择更新的 Metal 内核，从而将 LLM 推理速度提升 11–16 倍。该工作作为研究版本发布，源码与基准日志均公开，可复现。

## 背景

- Cua 的 macOS 虚拟机基于 Apple Virtualization.framework，guest 使用虚拟 GPU，实际由宿主 Apple GPU 执行。
- 默认的 Tahoe VM 中虚拟设备报告的 Metal 能力较保守（如 Apple 5 代 GPU 家族、最大 threadgroup 内存 32 KB、SIMD-group matrix 不可用），导致 llama.cpp 只能走较慢的 GPU 路径。
- 这属于半虚拟化（paravirtualization）架构，与 x86 Linux 上 VFIO/IOMMU 的真实 GPU passthrough 不同。

## 解决方案

- 实现一个小型的 Metal 能力垫片，插入到 guest 进程与 Metal API 之间，只改变该进程获得的能力查询结果。
- 通过返回测试过的 Apple GPU 家族和 threadgroup 内存值，llama.cpp 会选择更新的 Metal 内核路径。
- 仅作用于单个 guest 进程，不修改系统或影响其他应用。

## 性能结果

| 模型 | 提示处理加速 | 生成加速 | 接近裸金属 |
| --- | --- | --- | --- |
| TinyLlama 1.1B (M1 Ultra) | 11.08× | 16.36× | 提示 98% |
| Gemma 4 12B QAT Q4_0 | 7.20× | 14.54× | 提示 99.59%，生成 94.82% |
| Muse Glimmer 30B Q4_K-M (64 GiB guest) | 7.55× | 8.87× | — |

- 测试均通过 llama.cpp 纯文本完成，未使用 Ollama、多模态投影器或 drafter。

## 影响与意义

- 该能力差距同样存在于其他 Virtualization.framework 前端（如 Tart 的 “No GPU passthrough in macOS guest?” issue）。
- 表明 Apple 虚拟化栈中，GPU 能力上报是性能的关键瓶颈；应用遵循平台建议选择内核，反而限制了硬件潜力。
- 该垫片为本地 AI 工作负载（如 Cua Driver / Cua Cloud）提供了无需硬件直通即可接近裸金属性能的路径。
