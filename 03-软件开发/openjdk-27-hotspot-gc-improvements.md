---
type: ingest-note
source: OpenJDK Blog
date: 2026-08-02
---

# OpenJDK 27 HotSpot STW收集器改进综述

JDK 27 即将发布，HotSpot VM 的 STW（Stop-The-World）垃圾收集器迎来约 350 项变更。其中约一半为重构与清理（如使用 `Atomic<T>` 替换 `volatile` + `AtomicAccess` 的跨线程共享变量惯例，以及 G1 状态机清理）；约 35% 为 bug 修复与稳健性改进；其余则为新行为或实质性功能调整。

## 基础设施

- **JEP 401: Value Objects (Preview)**：为值对象适配对象迭代器与 eager reclaim 等基础设施。

## G1 GC 关键变化

- **JEP 523: Make G1 the Default Garbage Collector in All Environments**：G1 成为所有环境下的默认 GC，不再因环境条件退回 Serial GC。若需旧行为，仍可用 `-XX:+UseSerialGC`。
- **堆大小调整变更**：G1 不再于 Full GC 后依据 `-XX:MinHeapFreeRatio` / `-XX:MaxHeapFreeRatio` 调整堆大小；默认值从 40/70 改为 0/100（JDK-8238686），避免与基于 CPU 使用率的调整启发式相互冲突。
- **并发标记自适应启动改进**：增强对不利条件的抵抗，避免不必要的连续并发工作（JDK-8379846、JDK-8381006）。
- **Humongous 对象弱引用修复**：修复本可回收的 humongous 对象被弱引用意外保持存活的问题（JDK-8378331、JDK-8378336）。
- **Cleanup 暂停不再更新 MemoryPoolMXBean**：G1 Cleanup 暂停不再调用 `MemoryPoolMXBean.getCollectionUsage()`，因其不改变 Java 堆（JDK-8386332）。
- **GC CPU 时间计算修正**：此前未找到足够复制空间而失败的 GC 未被计入 GC CPU 使用率，现予修正，改善堆大小决策（JDK-8373894）。

## Parallel GC 关键变化

- **自适应晋升阈值可下降**：此前阈值只增不减，导致高阈值下长命对象占据 survivor 空间，迫使年轻对象过早晋升。JDK-8380590 允许阈值下降，更合理地促进长命对象晋升、保留短期对象。
- **堆扩展修复**：当连续大分配导致数千次 Full GC 而堆仍有足够余量却不扩展时，Parallel GC 现在能正确扩展 Java 堆（JDK-8377561）。

## Serial GC

- 无特殊变更，仅在默认场景下不再是默认收集器。

## 所有收集器

- 包含 TLAB sizing 等相关改动（素材截断，细节待补充）。

> 本笔记基于 OpenJDK 官方博客文章整理，原始链接未提供。