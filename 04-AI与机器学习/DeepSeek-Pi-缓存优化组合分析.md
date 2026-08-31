---
type: ingest-note
source: https://x.com/badlogicgames/status/2086877202239353285
date: 2026-08-14
tags: [AI, Harness, DeepSeek, Pi, 缓存优化]
---

# DeepSeek + Pi 组合跑赢 Claude Code？缓存命中率99.9%

## 事件概述

2026年8月11日，Pi Harness 创始人 Mario Zechner 转发了一组数据：开发者 0xEvan 用 Pi 调用 DeepSeek V4 Flash，处理了近 10 亿输入 Token，缓存命中率达到 99.93%，最终只花了 2.65 美元。如果没有缓存，同等用量预计需要 132 美元。另一名开发者 Shantanu Goel 表示，DeepSeek V4 Flash 在其他 Harness 中的缓存命中率通常为 94% 至 97%，到了 Pi 中却能持续达到 99% 以上。

## Composio 对比测试

Composio 选用同一个模型 DeepSeek V4 Flash，分别运行在 8 种不同的智能体 Harness 中，完成 30 项高难度的智能体任务。

- **Pi Agent**：通过 20 项，成功率 66.7%，排名第一
- **Oh My Pi**：通过 17 项，排名第二
- **Claude Code、Codex、Deep Agents**：均通过 16 项
- **Prime Agent**：通过 15 项，但 6 次运行未计分（2 次因评分器超时，4 次无记录）
- **Hermes Agent**：通过 15 项
- **OpenCode**：通过 14 项，排名最后

成本方面，Pi 平均完成一项成功任务只花费 0.028 美元，Claude Code 需要 0.195 美元，接近前者的 7 倍。Pi 完成任务的中位时间 132.2 秒，略慢于 Claude Code 的 122.7 秒，但综合成功率、速度与成本来看表现最突出。

## Harness 乘数效应

同一模型在不同 Harness 中的成功率从 46.7% 升至 66.7%，相差 20 个百分点。Composio 强调：不应孤立评测模型，Agent 排行榜必须注明使用的 Harness。

## Pi 的极简设计优势

Pi 在测试中采用全新、未经修改的默认安装，仅接入所需的 MCP 服务器插件，没有额外调优，却通过了最多任务。相比之下，Prime Agent 产生最庞大的会话（单会话消耗多达 350 万 Token，进行 33 次工具调用），最终被运行负担拖慢。增加更多层并没有换来更好的结果。

## DeepSeek 前缀缓存优化

DeepSeek API 缓存请求中提示词的前缀。缓存命中的价格远低于未命中。关键在于前缀匹配需要从第一个 Token 开始，上下文前部变化会导致大量 Token 无法命中。

### Reasonix 的核心设计原则

- 保持上下文前端稳定，采用追加而非修改的方式
- 启动时注入精简、稳定的环境摘要，避免每轮重新生成
- 过时的工具输出在触发摘要压缩前截断和清理
- 工具 Schema 契约文档化，变更时进行回归审查
- 双模型模式下，执行模型和规划模型分别运行在独立且缓存稳定的会话中

### pi-deepseek-cache 扩展

- **P0 层**：启动时冻结日期和当前工作目录，避免动态内容导致缓存失效
- **P2 层**：通过 SHA-256 哈希对前缀进行诊断，追踪缓存失效根因
- **P3 层**：使用 deepseek-v4-flash 在 temperature=0 下进行确定性摘要，并对摘要结果做哈希缓存

降本效果：deepseek-v4-flash 输入 Token 成本从每百万 0.14 美元降至 0.003 美元（降幅 98%）；deepseek-v4-pro 从 3.00 美元降至 0.025 美元（降幅 99%）。

## DeepSeek 官方 Harness 动向

截至 2026 年 8 月 11 日，DeepSeek 官方尚未推出自己的 Harness。“DeepSeek Harness 团队”微信公众号已完成注册，被解读为 Harness 产品即将正式发布的重要信号，产品内测已启动。官方 Harness 的优势在于原生适配，可与模型训练团队协同优化调用模式。

## 参考链接

- https://x.com/badlogicgames/status/2086877202239353285
- https://www.reddit.com/r/DeepSeek/comments/1vhhxvy/deeppi_reasonixlevel_cache_performance_in_pi/
