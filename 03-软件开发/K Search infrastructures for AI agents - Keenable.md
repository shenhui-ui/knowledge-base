---
type: ingest-note
source: https://www.infoq.cn/article/KbbHdAQFxQM7AJIYMLqR
date: 2026-08-31
---

## 面向 AI Agent 的搜索基础设施：Keenable（InfoQ）

人与 Agent 使用互联网的方式根本不同：传统搜索围绕"人查网页"优化（十个蓝色链接、点击行为），而 Agent 在任务执行循环中可能连续搜索几十上百次再交叉验证。Agent 时代的搜索指标变成 Recall、Freshness、Latency、QPS、Token Efficiency、Provenance——用尽可能低的成本找到"足够完成任务"的信息。

## Keenable 的做法

- 创始人 Andrey Styskin（前 Yandex 搜索/AI/云负责人近二十年，后任 Amazon AGI 网页基础设施负责人）与 Matthias Petri（同样来自 Amazon AGI）创立；团队约 15 名工程师，Accel 领投 2600 万美元种子轮
- 不做面向人的 AI 搜索框，也不在 Google/Bing API 上套大模型，而是自建抓取（Crawl）、索引（Index）、检索（Retrieval）、排序（Ranking）全链路，通过 REST API、MCP Server、CLI 交付给 Agent
- 自建 Web Index 覆盖超 1000 亿文档，美国东部 p95 延迟低于 250ms
- 定价：每千次请求 4 美元，100 RPS 以上降至 1 美元

## 关键技术点

- Token Efficiency：先过滤广告与冗余内容，只把精炼片段送入上下文——搜索质量决定上下文质量，进而决定 Agent 成本
- WebQueryLanguage（开发中）：组合多个网页来源回答单页无法完整回答的问题，方向是"开放 Web 的 SQL"
- 已进入数家 AI Lab 与推理服务商的生产环境（训练与运行时检索）

## 竞争与挑战

- Exa 已有同量级独立索引（1000 亿文档、C 轮 2.5 亿美元、估值 22 亿美元）；国内有博查、心流等 API，腾讯云、阿里云也在改造联网搜索
- 数据悖论：Agent 越成功，网站越可能失去流量并限制爬虫（如 Cloudflare Pay Per Crawl），重建索引越贵
- 安全风险：搜索结果可能通过间接 Prompt Injection 影响拥有实际权限的 Agent
- 中国特殊性：大量有价值信息封闭在微信、小红书、抖音生态内——"1000 亿索引 ≠ 看见中国互联网"

## See Also

- [[The-Agentic-Web-Index]]
- [[Cloudflare-Kitesurf-面向AI代理的浏览器]]
