---
type: ingest-note
date: 2026-08-10
source: "原文未提供URL，来源名：Moving integer division to floating-point is trivial（原文博客文章）"
---

# Moving integer division to floating-point is trivial

## 概述

整数除法（`x / y`）和取余（`x % y`）在硬件上通常是代价高昂的操作：延迟长、吞吐低。相反，浮点除法往往更快：延迟更短、吞吐更高，且通常有更多执行单元。因此，在某些场景下将整数除法/取余转换为浮点运算是有意义的。本文提出：对于能精确表示在浮点精度范围内的整数（double 53 位、single 24 位），在标准舍入模式下，可以通过浮点除法 + FMA（融合乘加）得到与整数除法完全相同的商和余数。

## 核心公式

对于两个整数 `x` 和 `y`（符号或无符号均可），将它们提升为浮点数后，在标准舍入模式（round-to-nearest, ties to even）下：

```cpp
d = trunc(x / y);   // 商，与整数除法 x / y 一致
m = -fma(d, y, -x); // 余数，与整数取余 x % y 一致
```

- `trunc` 截断操作在浮点转整数时是免费的。
- 无符号整数情形更难，因为最大数值更大；带符号整数只需考虑符号量值，范围更小。

## 数学依据

### 为什么不会遇到 tie（平局）？

标准舍入模式是“舍入到最近，平局到偶数”（round-to-nearest, ties to even）。Tie 发生在运算精确结果恰好位于两个浮点数中点时。作者指出：在基为 2 且使用相同精度的浮点除法中，**不存在中点**（参考：*Midpoints and exact points of some algebraic functions in floating-point arithmetic*, section 6.1, corollary 1）。因此永远不会有 tie，只需考虑“最近舍入”部分。

### 为什么不会向上舍入到下一个整数？

设精确结果 `x/y` 分为整数部分 `n` 和分数部分 `a/b`：

```
x/y = n + a/b,  其中 0 ≤ a/b < 1
```

给定 `p` 位二进制浮点格式，除以产生 `d` 位整数后，剩余 `r = p - d` 位小数。若要舍入到下一个整数，分数部分必须有至少 `r+1` 个前导 1（即非常接近 1）。

对于 `r` 位小数部分，可能的分数值上限为：

```
(2^r - 1) / 2^r = Σ(1/2^i)  (i=1..r)
```

这是产生 `r` 个前导 1 的最小值。但作者证明：在合法输入下，这种情况不可能出现，因此不会发生向上舍入。

## 实践要点

- **舍入模式切换**：可通过设置舍入模式为 `TOWARD_ZERO` 来替代 `trunc`，但修改控制字（control word）通常非常昂贵。
- **硬件支持**：有些硬件除法指令允许直接指定舍入模式，例如 AVX-512 的 `_mm_div_round_sd`（示例延迟 14 周期）。
- **整数转换开销**：int 转 float 和转回也有成本，需要注意（尤其 x64 上无符号整数转浮点没有专用指令）。
- **精度上限**：浮点精度 `p` 决定了可处理的整数宽度。例如 32 位整数用 double（p=53），16 位整数用 single（p=24）。更小的宽度自然成立。
- **SIMD 场景**：最适合在 SIMD 中使用，以摊销标量转换和舍入模式开销。
- **常量除数**：对于编译期常量除数，编译器通常已经优化。
- **运行时除数 + 少量复用**：可以使用 `libdivide` 等软件库。

## 参考与验证

- 存在形式化验证的方法：*Formally verified 32- and 64-bit integer division using double-precision floating-point arithmetic*。
- 文章中给出的示例基于 4 位精度浮点格式，展示了 GRS（guard/round/sticky）位情况，并指出“tie 情况不可能发生，只需要 guard bit”。

## 总结

通过浮点除法 + FMA 实现整数除法/取余在数学上是可行的，前提是输入整数不超过浮点格式的精确表示范围。实际收益取决于硬件指令延迟、吞吐、舍入模式切换成本以及是否能用 SIMD 摊销开销。该技巧适合对性能敏感且规模化的整数处理场景。
