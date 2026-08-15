---
type: ingest-note
source: https://arc-agi.com/leaderboard
date: 2026-07-31
tags: [AI, DeepSeek, ARC-AGI, benchmark]
---

# DeepSeek V4 Flash 0731 ARC-AGI评测

## 概述

DeepSeek 于 2026 年 7 月 31 日发布 V4 Flash 0731 模型，针对 ARC-AGI 基准进行评测。模型提供三种推理变体（Max、High、Low），并在 ARC-AGI-1/2 上取得显著成绩。

## 关键成绩

| 基准                     | Max   | High  | Low   |
| ---------------------- | ----- | ----- | ----- |
| ARC-AGI-1 Semi-Private | 89.0% | 87.0% | 84.0% |
| ARC-AGI-2 Semi-Private | 61.4% | 56.0% | 46.0% |

- ARC-AGI-1 测试成本：$0.02/任务
- ARC-AGI-2 测试成本：$0.04/任务

## 任务级表现（摘要）

在 ARC-AGI-1 Public 400 任务中，Max 变体仅极少数任务失败（如 `0d87d2a6`、`1acc24af`、`212895b5` 等），大多通过。在 ARC-AGI-2 Public 120 任务中，Max 变体通过率约 75%（基于素材逐项统计，90/120）。具体可通过官方 leaderboard 查看。

## 意义

该评测展示了 DeepSeek 在低成本高效推理上的进展，尤其在抽象推理基准上接近 90% 的 ARC-AGI-1 得分。

相关：[[DeepSeek-开源推理优化]]