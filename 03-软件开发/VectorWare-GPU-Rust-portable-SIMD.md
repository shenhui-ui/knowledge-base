---
type: ingest-note
source: https://vectorware.io/blog/rust-portable-simd-on-gpu/
date: 2025-07-31
title: VectorWare 在 GPU 上实现 Rust 便携 SIMD
---

# VectorWare 在 GPU 上实现 Rust 便携 SIMD

## 概述

Rust 的 portable SIMD（`core::simd`）成功在 GPU 上运行。这是 VectorWare 朝着 GPU-native 软件公司愿景迈进的重要里程碑：开发者可以使用熟悉的 Rust 抽象，编写充分利用 GPU 硬件的高性能应用。

## 背景：线程之下的并行

- VectorWare 此前已将 Rust 线程映射到 GPU warp，每个线程对应一个 GPU warp。
- 但还未利用线程/warp 内部的并行 lane。
- CPU 上线程内并行的抽象是 SIMD，而 GPU 的 SIMT 本质上就是 SIMD：一个计算单元对多个数据执行同一条指令。

## 核心映射：SIMT 即 SIMD

- GPU 的 warp 可视为一个宽向量单元，portable SIMD 向量直接映射到 warp。
- 例如 `Simd<i16, 32>` 将 32 个 i16 元素对应到 warp 的 32 个 lane。
- 两个向量的加法在 CPU 上编译为 `vpaddw`（x86-64），在 GPU 上编译为 `add.s16`，源代码完全相同。

## 统一并行层次

- CPU 线程内含 SIMD lane，GPU 上 `std::thread` 是 warp，其硬件 lane 扮演同一角色。
- 两者的 lane 都由 `core::simd` 驱动。
- 由于 portable SIMD 位于 `core` 而非 `std`，甚至不需要为标准库做 GPU 移植扩展。

## 示例代码效果

一个简单的 `relu_dot` 函数，同时计算：
- 逐元素乘法（32 个乘积一次完成）
- 逐 lane 比较生成掩码
- 基于掩码的 `select`
- 跨 lane 水平归约（`reduce_sum`）

这段函数同一份源码既能运行在 CPU 上（x86-64 / Arm），也能运行在 GPU 上，验证了可移植性。

## 意义

- 实现了从多线程到 SIMD 的完整并行层次，全部沿用 Rust 标准抽象。
- 为 GPU 编程提供了一种比 vendor intrinsics 更简洁、跨架构的路径。
- 未来复杂应用或将能够完全使用 Rust 生态编写，同时获得 GPU 的算力。
