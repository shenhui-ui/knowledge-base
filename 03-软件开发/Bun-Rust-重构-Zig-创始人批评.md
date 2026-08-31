---
type: ingest-note
source: https://www.theregister.com/devops/2026/07/14/zig-creator-calls-buns-claude-rust-rewrite-unreviewed-slop/5270743
date: 2026-08-14
title: "Bun-Rust-重构-Zig-创始人批评"
---

# Bun 用 Claude 生成 Rust 重构版，Zig 创始人称其为“没人把关的烂代码”

Bun 的创建者 Jarred Sumner 宣布，利用并行运行的 Claude 智能体，在 11 天内将 Bun 从 Zig 移植到 Rust，生成超过 100 万行 Rust 代码，花费约 16.5 万美元（按 API 定价）。但 Zig 语言创始人 Andrew Kelley 公开批评这一做法，认为项目背后是糟糕的编程实践和缺乏对 AI 生成代码的工程监督。

## 事件背景

- Bun 是 JavaScript 工具集，包含运行时、包管理器、打包工具和测试运行器，使用 WebKit JavaScriptCore 引擎和 Zig 语言以实现高性能。
- Anthropic 于 2025 年 12 月收购了 Bun，并基于其构建核心状态机。
- 收购前已有名为 RoboBun 的 Claude Bot 在代码库中承担大量维护工作，合并 PR 数量最多。
- 用户群扩大后漏洞增多，包括因 Bun 的 Bundler 漏洞导致 Anthropic 代码泄露事件（即使被禁止仍生成源映射文件）。

## 迁移细节

- 约 50 个动态 Claude Code 工作流并行运行，峰值时每分钟约生成 1300 行代码。
- 最终通过 Bun 自带的超过 100 万条断言的测试套件，所有平台 100% 通过，未跳过或删除测试。
- Sumner 称，手动重写需要小型工程师团队一年时间，而 AI 让这一任务变得可行。

## Zig 创始人的批评

- Andrew Kelley 在博文中指出，早在 AI 辅助之前，Bun 的代码质量就已堪忧，存在激进发布新功能、错误处理拙劣、技术债务堆积等问题。
- Kelley 认为，Bun 团队在获得 LLM 访问权限之前就已经写出“一团糟糕的代码”，并推测其面临商业目标压力。
- 他直言 Bun 与 Zig 分道扬镳是好事，因为 Bun 已不再适合作为 Zig 的典范。
- Zig 项目曾拒绝 Bun 团队基于 AI 辅助开发的分支贡献，理由是“不接受基于 AI 的贡献”。
- 核心质疑：如果测试套件连原有 Zig 代码的 Bug 都无法完全发现，又怎能保证 100 万行未经审核的 Rust 代码没有问题？

## 意义与争议

该事件展示了 AI 辅助大规模代码重写的可行性，但也引发了关于 AI 生成代码质量、工程监督和软件价值观的讨论。支持者如 HashiCorp 联合创始人 Mitchell Hashimoto 认为，AI 的速度远超人类工程师；批评者则强调，缺乏人类审核的代码可能隐藏大量隐患。

来源：The Register（InfoQ 转载）