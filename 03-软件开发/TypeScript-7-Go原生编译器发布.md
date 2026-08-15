---
type: ingest-note
date: 2026-08-10
source: https://www.infoq.com/news/2026/08/typescript-7-released/
tags: [TypeScript, Go, 编译器]
---

# 微软发布TypeScript 7.0：原生Go编译器构建速度提升10倍

微软正式发布 TypeScript 7.0，这是该语言首个搭载研发已久的原生编译器的稳定版本。新编译器将 TypeScript 工具集移植到了 Go 语言，在完整构建过程中通常能带来 8 至 12 倍的速度提升。

## 背景

该项目最初作为实验性原生移植计划于 2025 年 3 月公布，此前一直以 `@typescript/native-preview` 包的形式向社区开放，每周下载量曾超过 850 万次。随着 7.0 发布，夜间构建版本已回归标准 TypeScript 包的 `next` 标签，新的 `tsc` 可执行文件可通过常规方式安装：

```bash
npm install -D typescript
```

## 性能表现

微软公布的实测数据（基于 VS Code 源码库）：

- 完整构建时间：从 125.7 秒缩短至 10.6 秒，提升约 11.9 倍
- 总内存占用量下降约 18%
- 编辑器场景（含错误文件）：打开耗时从 17.5 秒降至不到 1.3 秒

外部团队也报告了类似效果：Slack 的 CI 类型检查时间从约 7.5 分钟缩短至 1.25 分钟；Vanta 反馈称 tsgo 影响显著。

并行度可通过新增的 `--checkers` 和 `--builders` 标志调整，资源受限环境可使用 `--singleThreaded` 完全关闭并行处理。

## 兼容性与迁移

- 7.0 尚未包含稳定的可编程 API，预计 7.1 推出，因此 typescript-eslint 以及 Vue、Svelte、Astro、MDX、Angular 等框架工具暂时无法使用该功能。
- 使用 webpack 加载器的项目需要等待 7.1 的 API 支持。
- 微软提供了兼容包 `@typescript/typescript6`，包含 `tsc6` 二进制并重新导出 6.0 API，便于现有工具继续工作。
- 6.0 中已弃用的功能在 7.0 中转为硬性错误，且默认启用 `strict` 和 `esnext` 模式，建议先采用 TypeScript 6.0 平稳过渡。

与 esbuild、swc、Biome 等工具不同，TypeScript 7.0 在保持完整类型检查的同时大幅缩小了速度差距。后续开发节奏约为每三到四个月发布一个版本，7.1 将重点关注生态系统期待的 API。

TypeScript 是由微软开发和维护的开源编程语言，遵循 Apache 2.0 许可，在 JavaScript 基础上增加可选静态类型，便于早期发现错误并自信构建大规模应用。

原文链接：<https://www.infoq.com/news/2026/08/typescript-7-released/>