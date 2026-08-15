---
type: ingest-note
date: 2026-08-07
source: https://www.infoq.com/news/2026/07/cloudflare-internal-dns/
---

# Cloudflare Internal DNS 全面可用：挑战 AWS Route 53

Cloudflare 官方博客宣布，其 Internal DNS 服务正式进入全面可用（General Availability）阶段。此前，该服务已经经历了从 2025 年 6 月开始的私有测试和公开 Beta 测试阶段。

## 核心能力

这项新能力将简化 IT 团队和企业管理私有 DNS 工作负载的方式。它通过统一控制平面，将私有 DNS 和公共 DNS 整合到同一套系统中，并提供统一 API、审计记录以及策略注册表。

据 Cloudflare 产品经理 Enrique Somoza 和高级产品经理 Hannes Gerhart 介绍，该服务由两个组件组成：

- **Gateway Resolver**：执行 DNS 安全和路由策略
- **Internal Authoritative DNS**：权威管理 DNS 区域

这两个组件构建在 Cloudflare 过去十年一直运营的平台之上，利用了公司大规模管理该平台过程中积累的经验。

## 三类实体

用户可操作三类不同实体：

- **内部区域（internal zones）**：包含私有资源的权威记录，例如应用程序、服务端点或数据库。
- **DNS 视图（DNS views）**：允许针对特定使用场景组合不同的内部区域，减少配置重复和配置漂移，让分流 DNS（split-horizon DNS）架构无需维护并行系统即可运行。
- **解析器策略（resolver policies）**：存储在 Gateway Resolver 组件中，匹配传入请求，并将请求转发到指定的 DNS 视图。

## 请求处理流程

新的 DNS 请求首先由 Gateway Resolver 组件根据已注册策略进行评估，策略可以选择阻止请求或转发请求。若策略匹配成功并指向一个 DNS 视图，请求会被转发到 Internal Authoritative DNS 进行解析；否则请求进入公共 DNS 路径。DNS 视图还可配置为：如果请求的名称无法在内部找到，则回退到公共解析路径，简化客户端名称查询流程。

无论操作来自管理控制台、Terraform 模块，还是直接 API 调用，所有操作都会经过同一统一入口，从而实现更简单的审计管理。

## 社区反馈与竞争

Reddit 上有评论认为，这项公告违背了 Cloudflare 关于“不再推出仅面向企业版功能”的承诺。也有评论指出，该功能具有明显企业属性：

> “这是一个非常小众的产品，除非你正在管理大型内部网络，否则它的使用场景并不明显。”

对于将工作负载运行在其他云服务商上的团队，也有相应替代方案：

- **AWS**：Amazon Route 53 Resolver 和 Private Hosted Zones
- **Azure**：Azure Private DNS 和 Azure DNS Private Resolver
- **Google Cloud**：Google Cloud DNS 的私有区域、转发区域和对等连接区域

## 可用性

Cloudflare Internal DNS 目前面向所有企业级客户开放，无需额外付费，可通过管理控制台、Terraform 或 Cloudflare API 进行管理。
