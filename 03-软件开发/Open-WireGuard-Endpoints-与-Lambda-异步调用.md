---
type: ingest-note
source: "Proxylity Blog: Now Available: Open WireGuard Endpoints and Lambda Async Invocation"
date: 2026-06-03
---

# Open WireGuard Endpoints 与 Lambda 异步调用

作者：Lee Harding | 日期：2026-06-03 | 阅读时间：7 分钟

UDP Gateway 今日新增两项能力：

1. **WireGuard 开放端点（Open WireGuard Endpoints）**：允许 Listener 接受任何客户端的连接，无需预先注册客户端公钥。
2. **Lambda 异步调用（Lambda Async Invocation）**：允许 Lambda destinations 以 Event 方式异步触发，无需等待函数响应。

这两项能力共同开启了面向公众的、事件驱动的 WireGuard 服务的新场景，而这些场景此前往往需要构建庞大的自定义基础设施。

## WireGuard 开放端点

过去，WireGuard Listener 要求每个连接客户端都必须预先注册公钥（在 CloudFormation 模板中列出），否则握手会被拒绝。这种模型适用于设备集合可管理的私有服务，但无法扩展到需要大量或未知客户端访问的场景，例如：

- 首次启动时生成 WireGuard 密钥对的移动应用；
- 按需配置的设备集群，集中密钥管理在操作上不可行；
- 任何需要让从未见过的客户端连接的公共服务。

在旧模型下，每个新客户端都需要通过带外注册步骤、更新 CloudFormation 模板，才能完成握手，这无法支撑公共服务的规模。

新引入的 **`AllowUnknownPeers`** 属性移除了这一限制。当 WireGuard Listener 设置该属性为 `true` 时，Gateway 会对任何合法的 WireGuard 客户端完成握手，无论其公钥是否已知。连接仍然完全加密——WireGuard 的密码学属性不变，区别只是 Listener 不再要求预先知道密钥。

这与 HTTPS 的模型类似：访问网站时，服务器不需要预先知道你是谁，TLS 握手完成后通道加密，认证（如果有）是应用层的独立关注点。开放 WireGuard 端点同样如此：传输层加密，而身份识别由你的 Lambda 或 Step Functions destination 按应用需求处理。

## 共享凭据门控

完全开放注册（接受任意 WireGuard 客户端）适合部分服务。对于另一些服务，你可能希望同时保留加密、开放握手，但又需要阻止未获得凭证的客户端连接。

**`UnknownPeerPreSharedKey`** 属性为此提供了一个轻量级门控。设置该属性后，未知对等点必须在 WireGuard 配置中包含该 PSK，否则握手失败。这不是每设备认证——所有客户端共享同一秘密——但它能有效限制只有获得 PSK 的客户端才能接入。可将其视为传输层的共享 API Key：不是强身份，但确实能阻止未获凭证的任意连接。

PSK 的分发由应用负责：基础设施侧可存储于 AWS Secrets Manager 并通过 CloudFormation 引用，客户端侧可在制造或注册过程中预置。

```yaml
WireGuardListener:
  Type: Custom::ProxylityUdpGatewayListener
  Properties:
    ServiceToken: !FindInMap [ProxylityConfig, !Ref "AWS::Region", ServiceToken]
    ApiKey: !FindInMap [ProxylityConfig, Account, ApiKey]
    Protocols:
      - wg
    AllowUnknownPeers: true
    UnknownPeerPreSharedKey: !Sub "{{resolve:secretsmanager:${WireGuardPSK}:SecretString}}"
    Destinations:
      - Name: packet-handler
        DestinationArn: !GetAtt HandlerLambda.Arn
        Role: Arn: !GetAtt ProxylityRole.Arn
```

命名对等点（列于 `Peers` 数组）不受 `AllowUnknownPeers` 和 `UnknownPeerPreSharedKey` 影响，它们继续使用各自的 per-peer SharedSecret。两种模型可在同一 Listener 上共存：一组固定的已知设备使用每设备 PSK，同时为动态客户端提供共享凭据的开放槽位。

## Lambda 异步调用

此前，UDP Gateway 的 Lambda destinations 一直使用同步 `RequestResponse` 调用：Gateway 递交一批数据包，等待函数返回，然后利用返回值为客户端发送回复包。该模型与 UDP 请求/响应模式对齐，因此是默认方式。

但对于需要把处理流程延续到单次调用之外的场景，同步调用会成为瓶颈。Lambda 持久化函数（durable functions）正好解决这一问题：利用 checkpoint-and-replay 机制，持久化函数可最多执行一年，失败后自动恢复而不丢失进度。

`Event` 调用类型正是这类工作负载的正确交付方式——异步触发，Gateway 无需等待响应，即可将数据包注入长期运行的工作流。

## 总结

两项新能力让 UDP Gateway 支持更开放、更事件驱动的 WireGuard 服务场景，同时降低了自定义基础设施的复杂度。
