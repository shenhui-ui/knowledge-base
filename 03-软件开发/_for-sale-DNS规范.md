---
type: ingest-note
tags: [DNS, RFC, 域名交易]
source: https://www.rfc-editor.org/rfc/rfc10023
date: 2026-07-01
---

# _for-sale DNS 保留叶子节点：域名出售信号的 RFC 规范

RFC 10023（Informational, July 2026）定义了一个保留 DNS 叶子节点名称 `_for-sale`，允许域名所有者在 DNS 中发布“该域名可出售”的信号，同时保持站点正常运行。该约定注册于 IANA，旨在弥补 WHOIS/RDAP 与网站展示之间的信息缺口。

## 核心机制

在待售域名的区域中发布一条 TXT 记录：

```
_for-sale IN TXT "v=FORSALE1;furi=https://example.com/for-sale"
```

记录必须包含强制版本标记 `v=FORSALE1;`（区分大小写），后面至多一个 `tag=value` 对。当前定义的标签：

| Tag | 含义 | 示例 |
|-----|------|------|
| `ftxt` | 自由文本 | `ftxt=Eligibility criteria apply.` |
| `furi` | 联系/信息 URI | `furi=mailto:hq@example.com` |
| `fval` | 要价（货币代码+金额） | `fval=EUR2500.00` |
| `fcod` | 专有代码（需事先约定） | `fcod=XX-aHR0cHM...` |

## 与域名停放、注册数据的区别

- **不是停放**：停放用销售页替换网站，会损失现有访问者；`_for-sale` 记录静默存在于 DNS，浏览器不感知，站点和邮件不受影响。
- **不是注册数据**：WHOIS/RDAP 只说明“是否注册”，无法表达“虽注册但可出售”。`_for-sale` 专门传递这一信号，目标受众是经纪人和自动化可用性服务，而非普通浏览者。

## 实现要点

- **发布位置**：在待售域的 `_for-sale` 叶子节点发布 TXT 记录，仅在确实出售时发布。
- **每条记录一个键值对**：要同时发布价格和联系 URI，在同一个 RRset 中发布多条记录，由处理方自行选取可理解的字段。不拼接，不类 SPF。
- **每条字符数**：单条记录最多 255 字节，避免解析时重组。
- **TTL ≤ 3600**：过期价格或已售域的记录比没有记录更糟。
- **叶子节点有效**：`_for-sale.example.com` 任意层级有效，但 `xyz._for-sale.example.com` 无效；忽略 `_for-sale.arpa` 下的记录。
- **停用即删除**：域名不再出售就移除记录，“不出售”没有显式值，缺席即“否”。
- ** DNSSEC 签名**：尽可能用 DNSSEC 签名，防止伪造。

## 常见错误

- 把多个键值对塞进一条记录（如 `v=FORSALE1;fval=EUR2500;furi=https://…`）——不符合格式定义。
- 出于期望而非事实发布记录，“售卖意向”滥用被 RFC 点名禁止。
- 以为发布记录就构成出售承诺——`fval` 仅作参考，处理器应显示免责声明。
- 期望通配符覆盖整个二级域或 TLD——`_for-sale.*.example.com` 不是有效通配符，无法用一条记录声明整个区域待售。
- 信任文本内容——`ftxt` 可能是攻击者控制的文本，`furi` 可能是恶意 URI，解析方需自行验证。

## 参考

- RFC 10023: The `_for-sale` Reserved DNS Leaf Node Name（2026 年 7 月）
- IANA 注册信息

本规范站点明确未发布 `_for-sale` 记录：specification.website 不对外出售。