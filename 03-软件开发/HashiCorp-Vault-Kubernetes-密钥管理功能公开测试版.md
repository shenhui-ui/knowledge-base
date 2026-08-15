---
type: ingest-note
date: 2026-08-11
source: https://www.infoq.com/news/2026/08/vault-kubernetes-key-management/
---

# HashiCorp 发布 Vault Kubernetes 密钥管理功能的公开测试版

HashiCorp 已发布 Vault Kubernetes 密钥管理功能的公开测试版。该版本允许 Kubernetes 集群将 Vault Enterprise 作为其静态数据加密的 KMS 提供程序。

- 于 7 月 10 日发布，随附一个兼容 KMS v2 的插件 `vault-kube-kms`。
- 允许 Kubernetes API 服务器将信封加密任务卸载至 Vault，保护存储在 etcd 中的 Kubernetes 密钥和其他 API 资源，并将守护这些数据的密钥移出集群。

## 核心价值

- 保持标准信封加密的分离机制：Kubernetes 仍生成并使用数据加密密钥（DEK）加密敏感资源数据并写入 etcd，保持 API 服务器期望的吞吐量。
- DEK 种子由存储在 Vault 中的密钥加密密钥（KEK）保护，传输密钥引擎负责执行加密操作。
- 加密数据和加密后的 DEK 共同存储在 etcd 中，没有正确配置的 Vault 将无法解密数据。
- 职责分工：Kubernetes 处理大量加密/解密调用，Vault 负责密钥生命周期管理、轮换、策略执行和审计。

## 部署场景

- Red Hat OpenShift 等企业级 Kubernetes 平台
- 多集群生产环境
- 需要职责分离的受监管环境
- 零信任项目

## 现有集成与差异

- 托管平台已有类似方案，如面向 AKS 的 Azure Key Vault KMS。
- 社区项目 `vault-kubernetes-kms` 填补了自托管集群的空白。
- 本次发布为已采用 Vault Enterprise 的团队提供了一条供应商支持、且已在近期 Kubernetes 小版本中测试过的途径。

## 限制与注意事项

- 仅适用于 Vault Enterprise。
- 部署时需要修改 Kubernetes `EncryptionConfig` 和 `kube-apiserver` 配置文件，排除大多数全托管控制平面。
- 需要考虑 Vault 的可用性，因为 KMS 提供程序位于集群数据解密路径上。

HashiCorp 将此测试版描述为实现大规模 Kubernetes 加密集中化密钥管理的第一步，并邀请平台工程和安全团队进行评估与反馈。