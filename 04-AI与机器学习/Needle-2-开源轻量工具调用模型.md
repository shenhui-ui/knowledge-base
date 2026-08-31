---
type: ingest-note
tags: [AI, 工具调用, 小模型, 开源]
source: https://github.com/cactus-compute/needle
date: 2026-08-07
---

# Needle 2：45M参数的开源工具调用模型

Needle 2 是 Cactus Compute 推出的开源 45M 参数模型，专为工具调用、设备使用和结构化提取设计。整个模型打包为单个 14MB 的二进制文件，完整会话仅需约 28MB RAM，可在边缘设备或气隙环境中离线运行。项目在 GitHub 上已获得 6.9k stars。本仓库提供 Python 包：推理、LoRA 微调与导出。

> Needle 读取你的工具描述来决定调用什么以及如何填充参数，所以好的描述就是全部关键。

## 核心特性

- **极简部署**：通过 `pip install cactus-needle` 安装，推理引擎首次从 Hugging Face 拉取并缓存，之后离线运行，无需额外构建。支持气隙环境离线部署。
- **自包含**：权重烘焙进单个 14MB 引擎，无独立模型文件管理，推理不进行网络请求。
- **结构化合约**：工具调用以 JSON 形式返回，内置字节级语法约束（由声明的 schema 编译），严格匹配用户声明的 schema。
- **置信度门控**：每个响应附带校准的置信度分数，可设定阈值决定自动执行或升级人工处理。
- **工具检索**：支持大型工具目录，内置检索头每轮只渲染前 5 个工具，语法约束限制在该子集。
- **有界内存**：256 token 滑动窗口，工具作为 KV 固定驻留，长对话内存保持约 28MB。
- **微调与导出**：支持 LoRA 微调和模型导出。

## 架构：简单注意力网络

Needle 2 基于 Simple Attention Network 设计，核心组件包括：

- Hadamard MLP 替代传统 FFN
- GQA 注意力
- Engram 键值记忆
- 多通道超连接
- 双随机注意力归一化（Sinkhorn 迭代）

每个块携带自己的更新规则：x̂ 是四个残差流的 RMS 归一化扁平化；H 是正交 Walsh-Hadamard 变换（固定矩阵，以 n log n 时间应用，无需读取权重）；(kₜ, vₜ) 行从哈希 n-gram 表中收集；P 是路由 logits A 的双随机归一化，通过 Sinkhorn 迭代计算；a、b、g 及所有 σ 门均为可学习且依赖输入。注意力和 MLP 残差均采用 sandwich-norm 和门控，engram 位点作用于两层，解码由声明 schema 编译的字节级语法约束。详细设计与消融实验见论文 arXiv:2607.18363。

## 快速开始

`pip install cactus-needle`，然后装饰函数即可：

```python
import needle

@needle.tool
def get_weather(city: str):
    '''Get the current weather for a city.'''
    return {'city': city, 'temp_c': 27, 'sky': 'clear'}

agent = needle.Needle(tools=[get_weather])
print(agent.run("what's it like in Lagos right now?")['results'])
# [{'city': 'Lagos', 'temp_c': 27, 'sky': 'clear'}]
```

结构化提取也简单：定义 Pydantic 模型并调用 `extract()` 即可。

```python
from pydantic import BaseModel

class Invoice(BaseModel):
    vendor: str
    total: float
    due_date: str

invoice = needle.extract("Invoice from Acme Corp, $1,200.00, due 2026-09-01", Invoice)
print(invoice.vendor, invoice.total)  # -> Acme Corp 1200.0
```

## 基准表现

在官方基准中，Needle 2 与 FunctionGemma 270M、LFM2.5 230M 及 Apple FM 等其他小型模型互有胜负，但体积小 5 至 70 倍，且以 2-bit 精度对比对方的 f16。

## Playground

在浏览器中试用模型：选择预设，编辑工具或提示词，即可直接体验。
