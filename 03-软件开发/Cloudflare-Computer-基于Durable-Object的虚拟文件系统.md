---
type: ingest-note
source: https://github.com/cloudflare/computer
date: 2026-08-09
---
# Cloudflare Computer：基于 Durable Object 的虚拟文件系统与执行环境

> Cloudflare Computer 是一个位于 Durable Object 内部的虚拟文件系统，提供多种代码执行后端，支持容器、Shell 和 JavaScript 运行环境，适合实验与原型开发。

## 核心架构

- **虚拟文件系统**：运行在 Durable Object 中，通过 SQLite 保存权威状态。
- **统一执行入口**：`workspace.runtime.exec(source, { backend })` 是唯一执行入口，后端决定 source 是 Shell 命令还是 ECMAScript 模块。
- **可插拔后端**：支持 Container、Isolate Shell、Isolate JavaScript 三种后端，可在 Workspace 中按稳定 ID 注册。

## 后端类型

- **Container（容器）**：将 SQLite 状态投影为沙箱容器中的真实 FUSE 挂载，通过 `computerd` 守护进程同步，提供完整 Linux 用户态、真实二进制和网络。
- **Isolate Shell**：在 Dynamic Worker 中运行 bash，通过 Workers RPC 访问权威 Workspace，无二次存储和同步往返。
- **Isolate JavaScript**：在全新 Dynamic Worker 中运行 ECMAScript 模块，支持结构化输入/结果、持久相对导入、`node:fs/promises` 以及 `ws:git` 和 `ws:artifacts` 模块。

## 状态与适用场景

- **预览版**：仅用于反馈收集，API 不稳定，设计可能变更，适合实验、探索和原型，不适合生产。
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
- Date: 2025-08-02
