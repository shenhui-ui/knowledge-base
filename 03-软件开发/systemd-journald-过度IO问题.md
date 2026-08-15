---
type: ingest-note
date: 2026-01-03
source: https://github.com/systemd/systemd/issues/40262
---

# systemd-journald 过度IO问题（issue #40262）

## 概述
systemd-journald 在写入日志时产生异常高的磁盘 IO，远超预期。用户报告在每秒钟仅写入 2 行日志的情况下，虚拟机持续产生约 50 IOPS。

## 详细信息
- **systemd 版本**：257.9
- **发行版**：Debian 13
- **内核版本**：6.12.57+deb13-amd64
- **组件**：systemd-journald
- **文件系统**：XFS

## 预期行为
日志写入的 IO 开销应与 syslog 保持在同一数量级。

## 实际行为
持续写入日志时，虚拟机产生约 50 IOPS 的额外 IO 流量，即使日志量极小（每秒两行）。

## 复现步骤
1. 将 journald 配置为写盘模式，文件系统使用 XFS。
2. 保持持续日志流（例如 haproxy 访问日志）。
3. 观察虚拟机 IO 流量。

日志示例：
```
Jan 03 13:37:01 cthylla haproxy[727]: 192.168.1.1:48550 ... "GET / HTTP/1.0"
Jan 03 13:37:03 cthylla haproxy[727]: 192.168.1.1:36892 ... "GET / HTTP/1.0"
...
```

## 用户观点
- 该问题与早前被无理由关闭的 issue #15292 完全相同。
- 用户认为 journald 的文件格式效率极低，文件体积远超实际写入内容，且曾在非正常重启后损坏，稳定性存疑。

## 相关性
- 这是 systemd 项目上的一个公开 bug 报告，需关注后续修复进展。
