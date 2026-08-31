---
type: ingest-note
source: https://github.com/schapman1974/briskdb
date: 2026-08-03
---

# BriskDB：将SQLite文件转化为分片数据库

BriskDB 是一个开源项目，目标是将普通 SQLite 文件转化为一个支持并行写入、PostgreSQL 兼容、HTTP 访问、以及嵌入式 Rust/Python API 的分片数据库。它保留 SQLite 成熟的存储引擎和工具链，同时增加路由层、分片安全 ID、跨分片索引、协议支持和运维护栏。

## 核心特性

- **不 fork SQLite**：每个数据分片仍是普通 SQLite WAL 数据库，现有工具可检查。
- **无中央写锁**：写入不同分片使用不同 WAL，可并行进行。
- **无每次插入的中央 ID 写操作**：原生 range 和 hi/lo 分配提供跨分片与进程的无冲突生成 ID。
- **安全的跨分片剪枝**：全局唯一性具有权威性；异步索引使用验证、水印、Bloom 过滤器及 min/max 摘要，确保优化不会悄悄隐藏行。
- **一个引擎处处可用**：PostgreSQL、HTTP、Rust、Python 共享路由、限制、取消、错误及存储行为。
- **运维可见**：`/health`、`/metrics`、admin JSON 和 Rust 状态报告暴露延迟、修复、重建、争用及 outbox 压力。

## 架构

架构采用协议无关的 Rust 引擎作为核心，通过 4,096 个虚拟桶路由到多个 SQLite WAL 分片。协议适配器只负责协议转换，不拥有数据库语义；路由、限制、取消、值、会话和执行都在共享引擎中。当前支持 PostgreSQL 和 HTTP，MongoDB 与 MySQL 协议正在规划中。同一 Rust 引擎同时驱动二进制、Python wheel 和 Rust crate，既可嵌入也可作为服务运行。

## 分片安全的生成 ID

- **native_range_v1**：每个分片获得不重叠的正 64 位范围，使用 SQLite 自身的 `INTEGER PRIMARY KEY AUTOINCREMENT` 进行本地分配，无需为每行插入访问中心节点。
- **hilo_v1**：从 manifest 租赁 4,096 个 ID 的块，然后在内存中分配，并通过哈希路由每个 ID。崩溃可能产生空洞，但 ID 不会被重用。

两种策略均在 manifest 中版本化。生成键执行目前仍为实验性且需显式启用。

## 当前状态

BriskDB 是 alpha 版，不是生产级数据库服务。目前可用的能力包括：

- 持久化虚拟桶路由，基于独立 SQLite WAL 文件
- 精确键路由和有界 scatter/gather 读
- HTTP 查询/写 API 和 admin 数据浏览器（仅限 loopback）
- PostgreSQL wire 协议，支持 TLS/SCRAM、背压流式行、SQLite-interrupt 取消、文本/二进制 CRUD、真实单分片事务，以及实时 psql/tokio-postgres/psycopg 客户端

该项目的边界是明确的，并公开已测量的结果，即使结果并不理想。
