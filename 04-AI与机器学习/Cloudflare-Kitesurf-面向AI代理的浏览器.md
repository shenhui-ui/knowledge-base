---
type: ingest-note
title: Cloudflare Kitesurf：面向AI代理的浏览器
date: 2025-07-31
source: https://blog.cloudflare.com/introducing-kitesurf
---

# Cloudflare Kitesurf：面向AI代理的浏览器

Cloudflare 宣布推出 Kitesurf，一个专为 AI 代理设计的浏览器，完全运行在 Workers 上，目前以 beta 形式在 Browser Run 中免费提供。这个想法的萌芽源于 Cloudflare 内部多年的反复讨论，随着 Workers 平台技术的成熟（Wasm 支持、Durable Objects、Worker-to-worker RPC 等）以及 AI 代理对浏览器的需求愈发强烈，12 周前团队终于决定动手。Kitesurf 的灵感来自 Rust 无头引擎 obscura，并通过 AI 辅助的方式移植到 Workers。相比 Chromium，它大幅降低了 CPU 和内存消耗，适用于截图、HTML 提取等常见代理任务。

## 为什么自研浏览器

- 浏览器是互联网操作系统，但构建新浏览器难度大。
- Workers 平台技术成熟（Wasm、Durable Objects、RPC 等），为复杂应用打开了大门。
- AI 代理需要浏览器，但 Chromium 开销过大，AI 不需要人类浏览器的功能（标签页、主题、扩展等）。
- 威胁模型不同：提示注入、工具安全是核心。

## 设计决策

- 测试驱动：利用 Web Platform Tests（WPT）作为 AI 代理的成功标准，为 AI 提供清晰的目标。
- 人类专注于架构和代码审查，AI 实现功能特性。
- WPT 仅验证标准一致性，还需要额外测试验证真实渲染和交互。
- 初始原型由 AI 代理移植 obscura，在给予详细计划和成功定义后取得了良好效果。

## 当前状态

Kitesurf 已在 Browser Run 中开放 beta，免费使用。
