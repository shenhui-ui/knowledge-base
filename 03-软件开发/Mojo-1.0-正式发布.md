---
type: ingest-note
source: https://www.modular.com/blog/mojo-1-0-is-here
date: 2026-08-11
title: Mojo 1.0 正式发布
---

# Mojo 1.0 正式发布

## 概述
Mojo 语言于 2026 年 8 月 11 日正式发布 1.0 版本，标志着这一自 2023 年首次发布以来不断演进的通用编程语言进入稳定生产可用阶段。Modular 团队表示，Mojo 已成为其商业基础设施（MAX 与 Modular Cloud）的日常基础。

## 稳定基础与生态增长
- 1.0 的核心目标是提供稳定的语言基础，允许社区长期项目可持续维护。
- 未来 1.x 阶段的变更将以增量添加为主，破坏性变更将参照 C++ 等成熟语言的演变标准谨慎管理。
- 标准库开源以来，近 200 名贡献者合并了超过 1,100 个 PR，改动超过 20 万行代码；另有上千人提交 issue 影响语言设计。

## 26.5 版本关键改进
- 语言简化与清理：变量统一使用 var 声明，闭包语法统一，单一 Pointer 类型，一系列重命名让词法更精确一致。
- 新增 Python 风格 lambda 语法用于内联闭包。
- Mojo LSP 服务器稳定性大幅提升，改善 VS Code 等编辑器体验。
- Mojo AI Skills 达到 1.0 ready，覆盖新项目创建、GPU 编程、其他语言移植等。
- 诊断内存安全问题：例如 List.append 使引用失效时能给出提示。
- where 子句在标准库中更一致地使用，并支持描述性错误信息。

## 未来路线图
Mojo 1.0 是重要里程碑，未来将拓展为真正的通用系统编程语言，重点包括：
- 健壮的异步编程模型
- 模式匹配与联合类型
- 继续开源 Mojo 语言及 MAX 组件，编译器与工具链将在 2026 年内开源

## MAX 26.5 增强
- 安装更灵活：使用 max["serve"]、max["benchmark"] 或 max["all"] 按需安装，conda 对应 max-serve、max-benchmark。modular 包将在 26.6 退役。
- 新增 GLM-5.2 与 Nemotron-H 两族模型支持（均为混合 Mamba-2 架构）。
- Kimi 2.5 现支持 Module V3 模型创作路径。

## 来源
- 原文：Modular Blog (2026-08-11) — 🔥🔥 Mojo 1.0 is here!