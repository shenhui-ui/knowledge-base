---
type: ingest-note
source: InfoQ
date: 2026-08-13
---

# TanStack Table V9 测试版：Tree-Shakable 特性、TanStack Store 状态与更低内存的使用

TanStack Table 是一个用于在各种 JavaScript 框架中构建表格和数据网格的 headless UI 库，近日发布了 V9 beta 版本。该版本重构了状态管理、内存使用、打包体积与可扩展性，同时保持开发者熟悉的核心表格逻辑。beta 版本于 2026 年 6 月 8 日通过 X 发布，支持 React、Preact、Angular、Solid、Vue、Svelte 和 Lit 等框架。

## 主要变化

- **Tree-shakable 特性**：特性改为按需注册。V8 中所有特性一起发布，V9 仅注册表格实际使用的部分，小表格可只有约 5 kb，企业级网格可按需引入排序、过滤、分页等功能。TypeScript 会强制执行，未注册的特性 API 不存在。
- **基于 TanStack Store 的状态管理**：`useReactTable` 变为 `useTable`，状态通过 `table.state`、`table.store` 及每个切片的 atoms 流动。新的 `table.Subscribe` 允许细粒度重渲染，如行选择变化只重新渲染显示计数的组件。
- **更低的内存占用**：大规模下内存占用明显降低。
- **清晰插件模型与重写的开发者工具**：回应了开发者对可扩展性的长期抱怨。

## 维护者说明

主维护者 Kevin Van Cott 表示设计直接借鉴自 TanStack Form 与 Store，并称 React Compiler 的稳定迫使重写，因 V8 模式已“开始出现问题”。他还承认发布“似乎花费了太长的时间”，一次性修复所有抱怨是“一个大错误”。

## 迁移与兼容

迁移设计为渐进式：`useLegacyTable` hook 在 V9 之上接受 V8 风格 API；导入 `stockFeatures` 可恢复旧的全量包行为（牺牲打包体积）。表的标记本身没有变化。

## 社区反馈

有开发者指出新的 atoms API 并非对受控状态的直接替代，在 Angular 与 React 应用中同样重要。另有开发者询问 per-table meta 缺失问题，Van Cott 已通过新功能和指南回应。V9 定位于未来发布的基础，目前处于测试阶段。

## 相关阅读

- 英文原文：TanStack Table V9 Beta: Tree-Shakable Features, TanStack Store State, and Lower Memory
- 迁移指南及文档见 TanStack 官方仓库