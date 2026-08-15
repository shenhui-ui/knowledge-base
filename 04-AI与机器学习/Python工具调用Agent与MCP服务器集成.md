---
type: ingest-note
source:
  - https://simonwillison.net/2025/Jan/24/llm-python/
  - https://simonwillison.net/2025/Jan/24/llm-anthropic/
  - https://simonwillison.net/2025/Jan/24/llm-deepseek/
date: 2025-01-24
---

# Python构建工具调用Agent并作为MCP服务器接入Claude Desktop

## 概述

本笔记整理自 Simon Willison 2025 年 1 月 24 日发布的系列文章，核心围绕：

1. `llm` Python 库更新（支持可组合工具与函数调用）
2. `llm-anthropic` 插件支持将 MCP 服务器接入 Claude
3. `llm-deepseek` 插件发布，支持 DeepSeek 推理模型
4. 一个完整的带记忆 Agent 实现示例：函数调用 + LangGraph 记忆 + 向量存储 + 正则工具 + Web 搜索 API
5. 将该 Agent 作为 MCP 服务器暴露，并配置到 Claude Desktop

## 关键组件

### llm Python 库

- `llm` 是 Python 生态中的命令行/Python API 工具，用于调用多种大模型。
- 新版本支持可组合工具与函数调用，Agent 可循环调用工具直到得到最终答案。

### llm-anthropic 插件

- 为 Claude 增加 MCP（Model Context Protocol）服务器支持。
- 通过 MCP 可挂载外部工具与知识源。
- 相关文章介绍了 MCP 服务器的基础概念与接入方式。

### llm-deepseek 插件

- 新增 DeepSeek 推理模型接入。
- 需要配置 `DEEPSEEK_API_KEY` 环境变量。
- 示例：`llm -m deepseek-chat "提问"`。

## Agent 实现流程

1. 设置环境变量 `DEEPSEEK_API_KEY`
2. 引入函数调用能力，注册工具函数（如 `regex_search`）
3. 使用 `langgraph-checkpoint` 实现持久化记忆，结合向量语义搜索
4. 接入外部 Web 搜索 API 获取实时信息
5. 由 Agent 自主决定调用哪些工具并汇总结果

## 将 Agent 暴露为 MCP 服务器

- 将上述 Agent 封装为 MCP 服务器，向 Claude Desktop 暴露工具。
- 在 Claude Desktop 配置文件中注册 `mcpServers`，指向本地/远程 MCP 服务器。
- 之后 Claude 可在对话中动态调用 Agent 提供的能力（如正则搜索、Web 搜索、记忆查询）。

## 收获与可复用点

- Python 生态中构建最小可用 Agent 的路径：`llm` + 函数调用 + LangGraph 记忆。
- MCP 可作为统一工具接入层，连接 Claude、本地模型（Ollama）与外部 API。
- 该方案适合作为个人知识库/运维助手等轻量 Agent 的骨架。

## 参考

- [llm-python](https://simonwillison.net/2025/Jan/24/llm-python/)
- [llm-anthropic](https://simonwillison.net/2025/Jan/24/llm-anthropic/)
- [llm-deepseek](https://simonwillison.net/2025/Jan/24/llm-deepseek/)
