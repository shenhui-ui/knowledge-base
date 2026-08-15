---
type: ingest-note
tags: [AI, 工具调用, 小模型, 开源]
source: https://github.com/cactus-compute/needle
date: 2026-08-07
---

# Needle 2：45M参数的开源工具调用模型

Needle 2 是 Cactus Compute 推出的开源 45M 参数模型，专为工具调用、设备使用和结构化提取设计。整个模型打包为单个 14MB 的二进制文件，完整会话仅需约 28MB RAM，可在边缘设备或气隙环境中离线运行。

## 核心特性

- **极简部署**：通过 `pip install cactus-needle` 安装，推理引擎首次从 Hugging Face 拉取并缓存，之后离线运行，无需额外构建。
- **结构化合约**：工具调用以 JSON 形式返回，内置字节级语法约束，严格匹配用户声明的 schema。
- **置信度门控**：每个响应附带校准的置信度分数，可设定阈值决定自动执行或升级人工处理。
- **工具检索**：支持大型工具目录，内置检索头每轮只渲染前 5 个工具，语法约束限制在该子集。
- **有界内存**：256 token 滑动窗口，工具作为 KV 固定驻留，长对话内存保持约 28MB。

## 架构：简单注意力网络

Needle 2 基于 Simple Attention Network 设计，核心组件包括：

- Hadamard MLP 替代传统 FFN
- GQA 注意力
- Engram 键值记忆
- 多通道超连接
- 双随机注意力归一化（Sinkhorn 迭代）

详细设计与消融实验见论文 arXiv:2607.18363。

## 快速开始

```python
import needle

@needle.tool
def get_weather(city: str):
    """获取指定城市当前天气"""
    return {"city": city, "temp_c": 27, "sky": "clear"}

agent = needle.Needle(tools=[get_weather])
print(agent.run("what's it like in Lagos right now?")["results"])
# [{'city': 'Lagos', 'temp_c': 27, 'sky': 'clear'}]
```

结构化提取也简单：定义 Pydantic 模型并调用 `extract()` 即可。

## 基准表现

在官方基准中，Needle 2 与 FunctionGemma 270M、LFM2.5 230M 及 Apple FM 等其他小型模型互有胜负，但体积小 5 至 70 倍，且以 2-bit 精度运行。

## 资源

- 权重：[huggingface.co/Cactus-Compute/needle2](https://huggingface.co/Cactus-Compute/needle2)
- 源码：[github.com/cactus-compute/needle](https://github.com/cactus-compute/needle)
- API 文档：`doc/apis.md` 覆盖 Python 调用、离线部署及高级用法。
