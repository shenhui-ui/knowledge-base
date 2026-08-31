---
type: ingest-note
source: Dmitry.GR / Thoughts
date: 2026-08-01
title: RISC-V: They Should Have Known Better
---

# RISC-V: They Should Have Known Better

Dmitry.GR 对 RISC-V 架构的批评文章（素材截断，仅收录部分内容）。核心论点：RISC-V 拥护者宣称它能同时统治超级计算机和微控制器，这不可能成立；RISC-V 最终会占据廉价微控制器市场，但并非因为 ISA 设计好，而是"矬子里拔将军"——它只比 8051 强一点。

## 不可能适用于所有场景

高端 CPU 与低成本微控制器需要截然相反的设计选择，一个 ISA 不可能同时是两者的理想选择。

## 微控制器领域的真实需求

- 中断延迟低
- 芯片面积小
- 代码密度高（ROM/SRAM 面积昂贵）
- 通常不需要硬件乘除法器
- 单用途场景不需要特权隔离

微控制器典型用途是与硬件模块交互、配置寄存器。RISC-V 的 RV32IC/RV32EC 在代码密度和中断处理上不如现有竞争对手（如 Cortex-M0）。

## 中断处理成本对比

- RISC-V 需要 Zicsr 扩展才有规范的中断处理方式（需要 mscratch/sscratch 暂存寄存器）；MIPS 为此保留了 $k0/$k1
- RISC-V（RV32I）：进入中断至少 21 周期（CSRRW + 保存寄存器），退出至少 20 周期，加上 JAL/RET 合计每个中断至少 44 周期才能进入 C 处理函数
- Arm Cortex-M0：进入 15 周期、退出 12 周期，硬件自动压栈 ABI 所需寄存器

## 未收录的其余章节（目录参考）

Optionality / Missing Obvious Pieces / Ridiculous encoding / Alleged Fixes / How Did We Get Here and Where to Now? / Does This Mean RISC-V is Doomed?
