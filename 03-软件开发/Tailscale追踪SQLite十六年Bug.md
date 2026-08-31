---
type: ingest-note
title: Tailscale追踪SQLite十六年Bug
source: https://tailscale.com/blog/sqlite-bug
date: 2026-08-12
---

# Tailscale追踪SQLite十六年Bug

2026年8月12日，Tailscale博客发布文章，讲述了他们如何追踪到一个存在16年的SQLite bug。

## 背景

去年年底，Tailscale的稳定性出现波动，许多故障由SQLite深处的单一bug引起。团队花了数月时间进行取证，最终在夏天确认并修复了该问题。

## 数据库架构

Tailscale的控制平面内部由一系列协调服务器（shard）组成。每个shard有一个SQLite数据库，保存该shard上所有tailnet的信息。单个Go进程独占访问该数据库，这是SQLite的预期使用方式。

自2022年起，Tailscale将SQLite作为主数据库，备份流程是每隔几分钟对数据库做完整快照，并上传到S3。

## 问题浮现

2025年8月，读取S3备份的数据管道报告数据库错误，`PRAGMA integrity_check`确认备份损坏。此后六个月中，共发生19次数据库损坏事件。

由于控制平面只处理配置数据，损坏不涉及私钥或网络流量。但恢复期间，受影响shard的整个控制平面不可用，导致tailnet无法获取设备列表，新增设备或配置变更无法持久化。

## 排查难点

团队最初检查近期代码变更，未发现相关改动，也没有人修改过低层SQLite交互代码。这个bug抵抗了所有初步排查尝试。

## 后续

文章详细描述了取证过程，并最终揭示了SQLite中一个存在16年的bug。Tailscale对多次中断表示歉意，并公开了问题的来龙去脉。

（原文未完，此处为素材摘要）

## See Also

- [[antithesis-sqlite-wal-reset-bug]]（Antithesis + Claude 一小时复现同一 bug 的完整过程）
