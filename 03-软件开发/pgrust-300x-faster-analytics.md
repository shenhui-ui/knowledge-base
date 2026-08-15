---
type: ingest-note
date: 2026-08-09
source: https://pgrust.com/blog/rebuilding-postgres-for-300x-faster-analytics/
---

# pgrust：批处理、算子融合与 SIMD 实现 300x 分析加速

> 原文：[Rebuilding Postgres for 300x faster analytics: batching, operator fusion, and SIMD](https://pgrust.com/blog/rebuilding-postgres-for-300x-faster-analytics/)
> 原文发布日期：2025-02-07

## 更新：pgrust 0.2 性能优化细节

pgrust 0.2 发布，重点聚焦性能。相比上一版快 10 倍；在 OLTP 基准中比 Postgres 快 30%；在 ClickHouse 的 ClickBench 分析基准上，比 Postgres 快 300 倍，甚至超过 ClickHouse。

仅查询引擎自身就贡献了约 10 倍的加速（300 倍中的 10 倍）。

## 核心优化思路

针对 Postgres 查询引擎的火山模型进行重构，主要手段：

- **批处理（batching）**：不再逐行拉取数据，而是批量处理，减少函数调用和虚拟分派开销。
- **算子融合（operator fusion）**：将多个算子放在本地循环中融合执行，减少中间物化。
- **SIMD**：利用 CPU SIMD 指令加速批量数值计算。

## 性能对比

- pgrust 0.2 比 pgrust 0.1 快 10 倍。
- OLTP 场景比 Postgres 快 30%。
- ClickBench（ClickHouse 的分析基准）上比 Postgres 快 300 倍，超过 ClickHouse。

## 背景：Postgres 性能瓶颈

Postgres 源自 80 年代，当时数据库的主要瓶颈是磁盘 I/O。三个趋势改变了局面：

1. 许多数据集已可装入 RAM，消除了大部分磁盘 I/O。
2. 不适用 RAM 的分析工作负载是批量扫描，瓶颈常是 CPU 吞吐量或内存吞吐量，而非磁盘。
3. NVMe 比传统硬盘快数百倍。

因此 CPU 和内存速度变得比以往更重要。数据库的查询引擎是 CPU 的主要消费者，pgrust 的优化正是让处理同样查询时使用更少的 CPU 和内存带宽。

## 示例：SUM 5 亿行

查询：

```sql
CREATE TABLE my_table AS
SELECT col::float8 FROM generate_series(1.0, 500000000.0) g(col);

SELECT SUM(col) FROM my_table;
```

在 c8g.4xl、关闭并行查询的 Postgres 中约 20 秒；等价的 Rust 裸循环：

```rust
let table: Vec<f64> = (1..=500_000_000usize).map(|i| i as f64).collect();
let mut sum = 0.0;
for &value in &table {
    sum += value;
}
```

约 358ms，差距约 55 倍。Postgres 的主要额外开销来自锁机制和存储格式解析。

## 火山模型简介

Postgres 使用 Volcano 执行模型：查询计划由节点组成，每个节点通过 `next()` 返回一行。例如 `SeqScan` 每次返回表的一行，`SumAggregate` 循环调用子节点 `next()` 累加。

```rust
trait Node {
    fn next(&mut self) -> Option<f64>;
}

struct SeqScan<'a> {
    table: &'a [f64],
    pos: usize,
}

impl Node for SeqScan<'_> {
    fn next(&mut self) -> Option<f64> {
        if self.pos >= self.table.len() {
            return None;
        }
        let value = self.table[self.pos];
        self.pos += 1;
        Some(value)
    }
}

struct SumAggregate<'a> {
    child: Box<dyn Node + 'a>,
    total: f64,
    done: bool,
}

impl Node for SumAggregate<'_> {
    fn next(&mut self) -> Option<f64> {
        if self.done {
            return None;
        }
        while let Some(value) = self.child.next() {
            self.total += value;
        }
        self.done = true;
        Some(self.total)
    }
}
```

逐行 `next()` 调用带来大量函数调用和虚分派开销。pgrust 改为批量拉取数据并让算子本地融合执行，减少中间物化和调用开销，同时启用 SIMD 加速。

## 相关链接

- 原文：[Rebuilding Postgres for 300x faster analytics: batching, operator fusion, and SIMD](https://pgrust.com/blog/rebuilding-postgres-for-300x-faster-analytics/)
- pgrust 首页：https://pgrust.com/
