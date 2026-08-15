---
type: ingest-note
source: Oxide Blog
date: 2026-08-13
---

# Kubernetes on Oxide：客户需求塑造的集成

2026年8月13日，Oxide 公司的解决方案软件工程师 Matthew Sanabria 撰文介绍了 Oxide 上 Kubernetes 集成的发展历程。文章回顾了团队如何从客户需求出发，逐步构建起对 Rancher、Omni 和 Cluster API 等不同工作流的支持。

## 背景

2024年底，客户和潜在客户迫切希望在 Oxide 上运行 Kubernetes，但当时 Oxide 没有受支持的集成方案。Kubernetes 通过标准扩展点定义其期望的基础设施行为，而 Oxide 则通过 API 提供实现这些行为所需的原语。需要的是软件集成以及对客户实际需求的理解。

## 起步：Rancher 节点驱动

团队从一份客户提交的 Rancher 节点驱动 pull request 开始。Rancher 节点驱动是一种可执行插件，教 Rancher 如何在特定基础设施平台上创建和管理虚拟机。Oxide 的节点驱动将这些操作转换为 Oxide API 请求。测试确认客户实现可用后，团队合并了 PR，添加了 CI/CD 和文档改进，发布了初始版本，从而成为 Oxide 的第一个 Kubernetes 集成。

## 与 Sidero Labs 合作：Omni 基础设施提供商

客户还希望使用 Sidero Labs 的 Omni 来供应运行 Talos Linux 的 Kubernetes 集群。Omni 通过基础设施提供商连接到基础设施平台，这些程序创建 Talos Linux 实例并注册到 Omni。在 KubeCon North America 2025 前七周，团队与 Sidero Labs 合作构建并展示了 Oxide 的 Omni 基础设施提供商。

集成过程中发现了 Omni 和 Talos Linux 的多个问题，例如 Talos 的文件系统探测只尝试从 NoCloud 配置磁盘读取 ISO 9660 超级块，而 Oxide 使用 FAT12 文件系统，导致 Talos 无法读取用户数据。修复无法及时发布，团队采用了一个有趣的变通方法：用注释填充用户数据，使其大小增加以使用 ISO 9660 超级块。

## 后续与展望

文章强调，集成设计不是抽象进行的，而是遵循客户在从供应集群到运行工作负载过程中遇到的问题。不同的供应工作流导致了 Rancher、Omni 和 Cluster API 等集成；运行集群需要基础设施协调，暴露应用则揭示了网络缺口，有状态工作负载暴露了存储限制。每个阶段的客户工作流都揭示了下一个缺口，塑造了团队构建的集成和未来的平台工作。