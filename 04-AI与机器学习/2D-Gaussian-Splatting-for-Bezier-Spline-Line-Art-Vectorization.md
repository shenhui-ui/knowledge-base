---
type: ingest-note
source: SIGGRAPH 2026, DisneyResearch|Studios
date: 2026-07-16
---

# 2D Gaussian Splatting for Bézier Spline Line Art Vectorization

## 概述

这是 DisneyResearch|Studios 与 ETH Zurich 合作发表于 SIGGRAPH 2026 的论文，提出了一种基于 **2D Gaussian Splatting** 的线条艺术（line art）矢量化新方法，在图像重建质量、速度和笔画质量上均达到当前最优水平。

## 核心方法

- **笔画提取**：不依赖传统启发式规则，而是利用**深度预测**和**语义特征提取**模型，将素描的骨架图分割为有意义的子图，从而初始化笔画集合，使结果更符合艺术意图。
- **笔画建模**：将笔画表示为**贝塞尔曲线**，同时包含几何（控制点）和外观（笔刷纹理）参数。
- **可微渲染**：采用**2D Gaussian Splatting** 进行快速可微渲染，实现对控制点和笔刷纹理的联合优化，高效拟合输入图像。
- **视频扩展**：引入时序跟踪和自适应关键帧机制，可推广到动画视频场景。

## 结果与意义

- 图像重建质量达到 SOTA，同时保持高速度。
- 生成的笔画质量高，且支持用户通过修正样条和调整优化参数进行交互式控制。
- 为计算机图形学中的线条矢量化提供了新思路，结合了神经渲染与传统几何建模。

## 参考

- 论文发表于 SIGGRAPH 2026，作者来自 DisneyResearch|Studios、Walt Disney Animation Studios 与 ETH Zurich。
- 图片来源与版权归作者所有。
