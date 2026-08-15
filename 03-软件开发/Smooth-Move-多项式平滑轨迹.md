---
type: ingest-note
title: Smooth Move: Taming Trajectories with Polynomials
date: 2026-08-03
source: Smooth Move: Taming Trajectories with Polynomials
---

# Smooth Move: Taming Trajectories with Polynomials

机器人、3D 打印机等运动系统的路径规划中，平滑过渡至关重要。本文用多项式（SmoothStep 族）解决轨迹段之间的速度、加速度乃至更高阶导数不连续问题。

## 核心概念

- **位置、速度、加速度**：速度是位置的导数，加速度是速度的导数，均为矢量；许多机器各轴独立，可简化为标量处理。
- **Jerk（加加速度）**：加速度的导数。突然改变加速度会引起机械振动，例如大脑在颅骨内因加速度突变而滑动，Jerk 是真实存在的影响。
- **更高阶导数**：Snap（Jounce）、Crackle、Pop 等，对机构振动也有影响，通常应尽可能最小化。

## 问题：轨迹段之间的不连续

运动路径由多个线段组成。工作段（如挤出、切削）具有固定的位置和速度；自由段则需要快速到达下一工作段起点。拼接时：

- 速度不连续 → 需要巨大加速度
- 加速度不连续 → 需要巨大 Jerk

因此自由段必须设计为与相邻工作段平滑衔接，避免高阶不连续。

## SmoothStep 多项式

平滑过渡的理想函数是 Sigmoid 形，但逻辑斯蒂函数渐近 0 和 1，不能在有限时间内完成过渡。SmoothStep 族多项式可在 [0,1] 区间内实现平滑过渡。

### SmoothStep（三次多项式）

\(S_1(t)\)

$$S_1(t) = \begin{cases}0 & t \leq 0 \\ 3t^2 - 2t^3 & 0 \leq t \leq 1 \\ 1 & t \geq 1\end{cases}$$

一阶导数 \(S'_1(t) = -6t^2 + 6t\) 在两端为零，保证速度连续；但二阶导数（加速度）两端不为零，仍存在 Jerk 突变。

### SmootherStep（五次多项式）

\(S_2(t)\) 使加速度也在两端为零：

$$S_2(t) = \begin{cases}0 & t \leq 0 \\ 6t^5 - 15t^4 + 10t^3 & 0 \leq t \leq 1 \\ 1 & t \geq 1\end{cases}$$

其一二阶导数均在两端为零，实际运动规划中更常用。

### 更高阶 SmoothStep

可推广到任意 n 阶，例如 \(S_6\) 为 13 次多项式：

$$S_6(t) = \begin{cases}0 & t \leq 0 \\ 924t^{13} - 6006t^{12} + 16380t^{11} - 24024t^{10} + 20020t^9 - 9009t^8 + 1716t^7 & 0 \leq t \leq 1 \\ 1 & t \geq 1\end{cases}$$

一般地，第 n 个 SmoothStep 函数的所有导数（1 到 n 阶）在两端都为零：

$$S_n^{(m)}(0) = S_n^{(m)}(1) = 0 \quad (1 \leq m \leq n)$$

## 应用意义

实际工程中通常用 SmootherStep 作为平衡点：既能消除加速度突变，又不至于因多项式阶次过高带来数值敏感性和计算开销。此类积分多项式轨迹规划被广泛应用于 3D 打印、CNC 加工与机器人运动控制。