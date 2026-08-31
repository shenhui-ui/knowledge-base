---
type: ingest-note
source: https://github.com/cordiverse/cordis
date: 2026-08-19
---

# Cordis：时空组合性元框架

Cordis 是一个面向 Node.js 的元框架，强调“时空组合性”（Spatiotemporal Composability）。它提供了一套插件化、事件驱动的基础设施，用于构建高度模块化和可组合的应用程序。

- GitHub：https://github.com/cordiverse/cordis
- 文档：https://deepseek-harness.github.io/deepseek-harness/reference/cordis-primer
- Paper: A Programming Paradigm for Spatiotemporal Composability
- 状态：积极开发中，API 尚不稳定
- 许可证：MIT
- Stars: 5.3k

## 关键特性

- **元框架**：不直接提供业务功能，而是定义组合规则与生命周期管理。
- **时空组合性**：在时间与空间上对组件进行编排，保证上下文一致性。
- **插件系统**：基于插件机制，支持动态加载、依赖注入和事件通信。
- **Node.js**：面向现代 JavaScript/TypeScript 生态。

## 相关技术

- 在该仓库的文档中，引用了 DeepSeek Harness 的 Cordis Primer，暗示其可能与 AI Agent 运行时有关联，但 Cordis 本身是通用框架。

## 适用场景

- 需要复杂事件驱动架构的服务器应用。
- 微前端/插拔式应用。
- 需要严格生命周期管理的库或服务。

注意：由于项目处于早期，API 可能变动，建议用于实验性项目或深入研究。
