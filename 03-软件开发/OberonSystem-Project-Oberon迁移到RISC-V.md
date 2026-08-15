---
type: ingest-note
source: https://github.com/rochus-keller/OberonSystem
date: 2025-02-16
title: "OberonSystem：Project Oberon 迁移到 RISC-V"
---

# OberonSystem：Project Oberon 迁移到 RISC-V

> 来源：<https://github.com/rochus-keller/OberonSystem>

## 概述
OberonSystem 是一个将 Project Oberon System 从 Oberon-07 迁移到 Oberon-90 的项目，使用 OP2 编译器，带 RISC-V (RV32) 后端。仓库还包含一个虚拟机（VM），模拟 Wirth 在《Project Oberon》书中描述的机器；该 VM 基于知名的 RV32 模拟器，内存映射与 Wirth 机器 1:1 对应，因此 Kernel.Mod、Display.Mod、Input.Mod 等底层模块无需修改。

## Project Oberon 背景
- 1986–1989 年，Niklaus Wirth 与 Jürg Gutknecht 在 ETH Zürich 设计并实现了完整计算机系统，包括操作系统、编译器、编程语言、文本/图形编辑器，并著书 *Project Oberon: The Design of an Operating System and Compiler*（1992）。
- 2013 年修订版源码使用 Oberon-07（Wirth 最后、最激进的简化语言），书可免费获取。
- 2013 版系统实现于自研 RISC-5 处理器（FPGA，Xilinx Spartan-3 开发板，1 MB SARM），从设备驱动到光栅操作全部用 Oberon 实现，硬件用 Verilog 描述。
- RISC-5 与 RISC-V 都是 32 位 load/store 架构、固定 32 位基础指令编码、编译器友好设计，理念同源。

## 迁移要点
- 将 Oberon System 从 RISC-5 移植到 RISC-V (RV32)，可运行于现成低成本的 ESP32 微控制器（如 Olimex ESP32-P4-PC 开发板）。
- 虚拟机精确复现 Wirth 机器的内存映射，硬件/软件契约不变（内存映射 + 指令集）。
- 系统不需要 MMU，非常适合嵌入式教学平台。
- 仓库包含图形界面截图，系统可原生运行在 RISC-V VM 上。

## 价值
延续 Project Oberon "存在、实际使用、且细节齐全" 的教育理念，为编译原理、操作系统、计算机体系结构提供了可运行的完整参考实现，同时降低了硬件门槛。
