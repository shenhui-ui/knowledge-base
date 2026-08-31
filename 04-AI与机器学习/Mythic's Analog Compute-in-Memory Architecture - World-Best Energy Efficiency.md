---
type: ingest-note
source: https://www.mythic.ai
date: 2026-08-24
---

## Mythic 的模拟计算内存（Analog Compute-in-Memory）架构

传统芯片每秒在处理器与内存之间搬运数据数十亿次，大部分能耗花在数据移动而非计算本身——Mythic 称这是行业 80 年未受质疑的冯·诺依曼架构缺陷。Mythic 的方案是把 AI 模型权重直接保存在闪存阵列中，在模拟域"就地"完成矩阵计算，从源头消除数据搬运开销。

## 能效与定位

- 宣称系统级 performance-per-watt-per-dollar 最高提升 100 倍（100x energy efficient compute for AI）
- 核心产品为 APU（Analog Processing Unit，模拟处理单元），产品线包括 M1、Vanguard、Starlight、Mead
- 面向边缘到企业部署：汽车/ADAS、机器人与物理 AI、企业级 LLM、国防与传感

## 近期动态

- 2026 年 1 月收购德国 AI 处理器公司 Videantis，其芯片已装车约 3000 万辆量产车，ADAS 平台经过量产验证
- 投资方包括 NEA、DCVC、洛克希德·马丁、本田等

## See Also

- [[AI-SSD-LLM推理存储层级]]
- [[多GPU本地LLM构建FAQ]]
