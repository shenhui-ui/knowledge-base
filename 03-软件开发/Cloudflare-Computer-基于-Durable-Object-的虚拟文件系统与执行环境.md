---
type: ingest-note
source: https://www.infoq.com/news/2026/08/cloudflare-computer-agents/
date: 2026-08-15
---
# Cloudflare Computer：基于 Durable Object 的虚拟文件系统与执行环境

> Cloudflare Computer 是一个新的开源运行时，旨在为 AI 智能体提供更接近真实“计算机”的环境，而不只是临时容器。它利用 Cloudflare isolates 实现快速无服务器执行，使智能体成本更低、速度更快、更容易扩展。（InfoQ, 2026-08-15）

## 设计动机

- 依赖容器运行智能体无法扩展到“数亿乃至数十亿个并发智能体”，全球没有足够计算能力。
- 方案：由平台决定代码在 isolate、容器沙箱还是 Web 浏览器中运行。每个智能体获得一台计算机，运行时针对效率和可扩展性优化。
- 目标：只有不到 10% 的工作需要容器；编码、音视频处理、文档创建可由 isolates 完成。

## 核心架构

- **虚拟文件系统**：运行在 Durable Object 中，通过 SQLite 保存权威状态。
- **统一执行入口**：`workspace.runtime.exec(source, { backend })` 是唯一执行入口，后端决定 source 是 Shell 命令还是 ECMAScript 模块。
- **可插拔后端**：支持 Container、Isolate Shell、Isolate JavaScript 三种后端，可在 Workspace 中按稳定 ID 注册。
- **横向+纵向弹性扩展**：isolate（一个 Durable Object）中运行智能体运行框架，按需连接的容器作为工具调用，只在必要时使用更重量级的计算原语。
- **共享文件系统**：基于 SQLite，isolate 和容器均可访问，任务可在两者之间无缝转移；文件系统可与 Git 仓库、存储桶或任意文件配合，所有操作受控、审计、可观测。

## 后端类型

- **Container（容器）**：将 SQLite 状态投影为沙箱容器中的真实 FUSE 挂载，通过 `computerd` 守护进程同步，提供完整 Linux 用户态、真实二进制和网络。
- **Isolate Shell**：在 Dynamic Worker 中运行 bash，通过 Workers RPC 访问权威 Workspace，无二次存储和同步往返。
- **Isolate JavaScript**：在全新 Dynamic Worker 中运行 ECMAScript 模块，支持结构化输入/结果、持久相对导入、`node:fs/promises` 以及 `ws:git` 和 `ws:artifacts` 模块。

## 状态与适用场景

- **预览版**：仍处于早期预览阶段，仅适合实验、探索和原型开发，不适合生产。
- **API 不稳定**：设计可能变更。
- **文档前瞻**：`docs/` 规范是意图说明，并非当前代码描述。

## 典型示例

- `examples/container`：在容器内运行 computerd，通过 capnweb 与 Durable Object 通信。
- `examples/worker-shell`：无容器，在 Dynamic Worker 中运行 bash。
- `examples/worker-javascript`：在 Dynamic Worker 中执行 ECMAScript 模块。
- `examples/think`：将 Workspace 作为聊天代理的工作目录。
- `examples/tutorial`：从零构建一个代理，生成 markdown 食谱并在容器内通过 pandoc 转 PDF。
- `examples/artifacts`：生成 Worker 项目并发布到 Cloudflare Artifacts。
- `examples/assets`：用 Workers AI 将提示词转为图片并写入 Workspace。

## 仓库结构

- `packages/dofs`：Durable Object SQLite 虚拟文件系统与同步协议。
- `packages/rpc`：capnweb 线协议类型与服务端/客户端辅助。
- `packages/computerd`：沙箱容器内的 FUSE 挂载与 RPC 服务守护进程。
- `packages/computer`：顶层 Computer 包，供 Durable Object 使用。

## 相关链接

- Source: [cloudflare/computer (GitHub)](https://github.com/cloudflare/computer)
- InfoQ 报道: [Cloudflare Computer 发布：让 AI 智能体拥有持久化运行环境](https://www.infoq.com/news/2026/08/cloudflare-computer-agents/)
