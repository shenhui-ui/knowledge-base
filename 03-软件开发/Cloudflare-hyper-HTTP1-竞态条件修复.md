---
type: ingest-note
date: 2026-08-12
source: InfoQ
---

# Cloudflare 发现并修复 hyper HTTP/1 实现中的竞态条件

## 概述

Cloudflare 在重构 Workers Images 绑定过程中，发现并修复了 Rust 常用 HTTP 库 hyper 中的一个罕见竞态条件漏洞。该漏洞可能导致大型 HTTP 响应在返回 HTTP 200 成功状态的情况下被悄然截断，问题已存在多年，仅在特定时序条件下触发。修复仅用四行代码，并已合并到 hyper 上游。

## 背景

- **hyper 库**：Rust 生态中实现 HTTP 协议的底层网络库，为许多高层 Web 框架和应用提供客户端与服务端核心功能，始于 2014 年，由 Sean McArthur 发起，MIT 许可。
- 漏洞发现于 Cloudflare Images 的 Workers Images 绑定重构上线后，部分大型图像转换请求间歇性返回被截断的数据，但响应报告为 HTTP 200，Content-Length 也符合预期。

## 定位过程

1. 客户报告图像截断，响应声称成功且长度正确，但实际传输数据量远小于预期（例如 200 KB 而非 3.3 MB）。
2. 构建可确定性复现用例，在不同 hyper 版本和环境中测试，逐服务埋点并使用分布式追踪排除可能性。
3. 应用层日志无错误，但通过内核级 `strace` 系统调用跟踪发现：hyper 在缓冲响应数据完全发送前过早关闭了连接，确认是依赖时序的竞态条件。
4. 最终定位到 hyper 的 HTTP/1 分发循环，它错误地忽略了未完成的缓冲刷新并过早关闭连接。

## 修复

- 添加可确定性复现该竞态的测试。
- 修改 hyper，确保在关闭连接前完成缓冲数据的刷新。
- 修复代码仅四行，已合并进 hyper 项目，将在未来发布中提供。

## 社区讨论

- **Rust 异步设计缺陷**：Rust 编译器贡献者 Martin Nordholts 指出，这是异步 Rust 已知的设计缺陷：同步 Rust 中能编译通常就能工作，异步 Rust 则不然，静默取消（silent cancellation）是此类问题的根源。
- **维护者赞助问题**：有人质疑 Cloudflare 年收入 20 亿美元却未直接支持 hyper 维护者 Sean McArthur。
- **Clippy lint 建议**：启用 `let_underscore_untyped` 或 `let_underscore_must_use` lint 可能提前发现问题，但这些 lint 未默认开启。
- **监控能力质疑**：部分从业者认为 Cloudflare 应通过采样和 lint 检查更早发现大规模错误响应，而非等客户投诉。

## 参考

- 英文原文：[Cloudflare Identifies Race Condition in hyper’s HTTP/1 Implementation](https://www.infoq.com/news/2026/08/cloudflare-hyper-race-condition/)（示例链接，实际以 InfoQ 发布为准）
