---
type: ingest-note
source: 未知（素材未附原文链接）
date: 2026-08-31
---

# HTML over WebSockets：无需JSON的SPA架构

构建单页应用（SPA）是一个复杂拼图：需要 JavaScript 框架绘制视图、API 提供 JSON，以及两个独立代码库通过契约相互理解。这是一种被广泛接受的工程实践，但并非唯一路径。另一种思路是 **HTML over WebSockets**：服务端直接发送已构建好的 HTML，客户端仅负责将其放置到对应位置。所有渲染逻辑留在后端，使用单一语言，无需契约或 API。

该模式属于 **hypermedia / HTML over the wire** 家庭，根据 HTML 传输方式分为三种变体：

- **HTTP**：逐请求往返，代表如 htmx、Unicorn。
- **SSE**：单向持续通道，服务端到客户端，代表如 Datastar。
- **WebSockets**：永久双向通道，代表如 Phoenix LiveView、Django LiveView。

通道类型决定了应用架构与通信模式，本文聚焦 WebSockets 变体——实时、双向，让你几乎不用手写 JavaScript 就能构建 SPA。

## 起源

Chris McCord（Phoenix 框架作者）在 ElixirConf 2019 上演示了 **LiveView**。他用 15 分钟构建了一个实时工作的 Twitter 克隆，没有添加任何渲染型 JavaScript 或流行框架（React、Angular、Vue 等）来管理视图，证明可以留在后端并保持高效。此后该方案迅速推广，衍生出其他语言的实现。

## 工作原理

客户端仍然使用 JavaScript，但职责不是渲染，而是建立一个 WebSocket 通信通道，并将收到的 HTML 放到正确位置，外加动画、事件处理等次要任务。

服务端收到请求后，查询数据库，用模板引擎渲染完整 HTML（含 CSS/JS），通过 WebSocket 推送。由于通道永久开放，服务端还能在客户端未请求时主动推送变更（广播）。

传统 SPA 流程 vs HTML over WebSockets 流程：

- 传统：HTTP 请求 → 服务端查库 → 构建 JSON → 返回 → 客户端解析 JSON → 前端引擎渲染 HTML。
- WebSockets：建立连接并认证 → 在通道上发送“我要 /article/2/” → 服务端查库 → 渲染 HTML → 推送已组装好的 HTML/CSS/JS → 客户端放置 HTML。

后者更简洁、快速，且无需关心客户端状态或渲染逻辑，一切都在后端。

## 优势

- 实时性与双向通信，适合协作、聊天、仪表盘等场景。
- 无 API 契约，避免双代码库同步问题。
- 单语言、单渲染引擎，降低技术栈复杂度。
- 服务端主动推送能力，天然支持广播更新。

HTML over WebSockets 并非银弹，但在需要实时交互且希望保持后端主导的场景下，它提供了一条值得考虑的现代路径。
