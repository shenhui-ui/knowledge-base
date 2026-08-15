---
title: "pg_clickhouse v0.10.0 更新：子查询下推、TPC-H提速、C驱动与聚合函数"
type: ingest-note
source: "https://github.com/auxten/pg_clickhouse/releases/tag/v0.10.0"
date: "2026-08-11"
---

# pg_clickhouse v0.10.0 更新：子查询下推、TPC-H提速、C驱动与聚合函数

> 本文译自 pg_clickhouse 官方博客，介绍 v0.10.0 的核心改进：TPC-H 下推覆盖率提升、子查询下推、NOT IN 实现修正以及新的 C 驱动客户端。

## TPC-H 成绩更新

从 v0.3 到 v0.10.0，完全下推的 TPC-H 查询从 12/22 增加到 **16/22**，剩余 6 条（Q13、Q15、Q16、Q18、Q20、Q21）。

最亮眼的改进：

- **Q2**：3,446 ms → 24 ms（整条查询变成单一外部扫描）
- **Q17**：32,709 ms → 37 ms（整条查询为单一外部扫描）
- **Q22**：1,415 ms → 45 ms（下推但拆成多个远程查询，典型为外层扫描 + InitPlan 扫描）

Q17 是最大亮点——相关子查询（`l_quantity` 按 part 取平均）原本每次外层行都要对 600 万行 lineitem 做一次本地求值，现在完全下推到 ClickHouse，比原生 PostgreSQL 的 2.1 秒还快三个数量级。

## 子查询下推

此前版本中，相关 `EXISTS` 子查询已被下推为 `LEFT SEMI JOIN`，但更复杂的子查询（如标量 SubPlan）仍留在 PostgreSQL 本地执行。v0.10.0 实现了 **SubPlan 整体下推**（#289），PostgreSQL 中的子查询会变成 ClickHouse 中的子查询，整条 Remote SQL 包含完整的子查询逻辑：

```sql
SELECT sale_id, amount
FROM subplan_test.sales r1
WHERE ((r1.amount > (SELECT (1.5 * avg(q1_1.amount))
                     FROM subplan_test.sales q1_1
                     WHERE ((q1_1.item_id = (r1.item_id))))))
ORDER BY r1.sale_id ASC NULLS LAST
```

这使 Q2 这类查询只需一个 Foreign Scan 和一次远程查询即可完成。

## NOT IN 的正确实现

`NOT IN` 通过 `LEFT ANTI JOIN` 下推（semi-join 的否定形态），前提是规划器能证明转换是安全的。

需要注意：此功能依赖 ClickHouse **25.8+** 对关联子查询 SQL 形状的支持。pg_clickhouse 在规划时检查服务器版本，旧版本自动回退到本地求值。

## 其他改进

- **二进制驱动重构**：基于全新的纯 C 客户端库重建，并修复了几个并发 bug。
- **函数与聚合下推覆盖**：下推的函数和聚合表面面积增加了一倍以上。

## 剩余工作

Q16 和 Q18 的阻塞点在于 PostgreSQL 会将子查询展平成 anti/semi-join，但输入本身是 join 树，去解析器目前无法在 join 两侧同时遍历 join 树。Q15 和 Q20 也遇到类似问题，这是下一阶段的子查询下推重点。

---

*参考链接：原文来自 pg_clickhouse 官方工程博客（2026-08-11），GitHub release 页面见 source。*