---
type: ingest-note
source: https://github.com/jolt-lang/jolt
date: 2026-08-01
---
# Jolt：自托管Clojure编译器

Jolt 是一个自托管的 Clojure 编译器：它读取 Clojure 代码，将其分析为宿主无关的中间表示（IR），并生成 Scheme 代码来执行。编译器本身使用 Clojure 编写，并且能够编译自身。

## 关键特性

- **独立二进制**：`jolt build` 可以提前编译项目，将运行时、标准库、应用及依赖合并为单一自包含的可执行文件。运行时不依赖 Chez、JVM 或源码。
- **真实并发**：`future`/`promise`/`agent`/`pmap` 在共享堆上的 OS 线程上运行，符合 JVM 语义；`core.async` 提供 channel 和 go block。
- **完整数值塔**：支持精确整数、大整数（bignum）、精确比率（如 `(/ 1 2) => 1/2`）和浮点双精度。`=` 区分类别，`==` 进行值相等比较。
- **持久化数据**：不可变向量（32 路前缀树）、cons 列表、HAMT 映射/集合，遵循 Clojure 值语义。Transient 是可变的临时集合。
- **Clojure 兼容**：支持惰性/无限序列、transducers、解构、multimethods、协议/记录、元数据、命名空间、运行时 `eval` 以及完整 reader。

## 运行方式

Jolt 以原生方式运行于 Chez Scheme，或通过 Gambit 编译为 JavaScript 运行。