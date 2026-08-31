---
type: ingest-note
source: https://mail-index.netbsd.org/netbsd-advocacy/2005/09/10/0000.html
date: 2026-08-24
---

## NetBSD 在企业网络中的实践（2005 年案例）

netbsd-advocacy 邮件列表的经典帖子：作者因 Windows 服务器频繁崩溃导致错过与女儿的出游，推动公司全面迁移到 NetBSD，并用实际运行数据说明其企业级可靠性。

## 核心数据

- 29 台 NetBSD 2.0.2 高端服务器支撑 4800+ 重度用户，每天传输超过 870 GB 数据
- 迁移测试期间，Windows 上的 MySQL 反复自行重启，NetBSD 机器持续稳定运行——老板两小时内批准全面推广
- 有趣的对比：公司的 Linux 文件服务器宕机次数反而比 NetBSD 服务器更多

## 承载的企业负载

- MySQL 数据库（流量与资源消耗最大头）
- Apache 内外部网站（峰值约每分钟 35 个请求）
- Postfix 内外部邮件（日均约 1200 封）
- Samba/NFS 文件服务（4800 名用户）

## 方法论

渐进式迁移：先两台试点、验证稳定后逐步推广；pkgsrc 快速部署。结果是从救火式运维转向周末 SSH 远程轮值——稳定性同时改善了基础设施与运维人员的生活质量。

## See Also

- [[OpenBSD-发布说明更新]]
- [[DigitalOcean-Run-OpenBSD-on-DigitalOcean-for-$4-month]]
