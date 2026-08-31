---
type: ingest-note
source: MSX Info
date: 2026-08-05
---

# MSX上的Pascal编译器与Turbo Pascal生态

## 背景

- Pascal 语言以法国数学家布莱士·帕斯卡命名，1970 年由 Niklaus Wirth 在 Algol 块结构语言基础上完成开发。
- 其最初目标包括：
  - 提供适合系统化编程教学的语言；
  - 在当时的计算机上实现可靠且高效的编译器。
- Pascal 在七八十年代是编程教育中结构化编程教学的主要语言，并成为 ANSI 标准。
- Wirth 后来在 Pascal 基础上发展了 Modula、Oberon 等模块化语言。

## Turbo Pascal 与 MSX

- Borland 的 Turbo Pascal 在 CP/M 与 MS-DOS 平台大获成功，其中 Version 3 尤其流行，八九十年代小型计算机上的大量软件由 Turbo Pascal 写成。
- 在 MSX 平台上，Turbo Pascal 是支持最好的 Pascal 编译器。
- 相关版本与资源：
  - **Turbo Pascal 3.01 for CP/M**：未安装原版，随 Philips 发行的 MSX 版本分发。
  - **Turbo Pascal 8 bits MSX**：Philips 发行的版本，软盘标签显示为 Borland 产品。
  - **Turbo Pascal 3.3f**：由 Frits Hilderink（MCE）制作的 MSX-2 版本，包含 GIOS，并附带 PC 版本。
  - **Turbo Pascal DataBASE Toolkit 1.2**：Borland 官方附加组件，适用于 MS-DOS，带调试器，可用于交叉编译。
  - **Turbo Pascal 3.0 手册**：扫描版，包含 CP/M、CP/M-86、MS-DOS、MSX-DOS 版本说明。

## 其他 Pascal 编译器

- **Hisoft Pascal 80**：MSX 上的另一款 Pascal 编译器。
- 普通 Turbo Pascal 默认无法直接使用 MSX 硬件功能，但可以通过 include 文件中的 INLINE 机器码片段访问 MSX 设施。

## Pascal 开发环境与库

- **Graphpak**：Uwe Schroder 的 Pascal BIOS include 文件。
- **Beunsoft Pascal BIOS include files**：提供 MSX BIOS 调用支持。
- **Turbo-Lib V3.0**：由 Jacoon Bastiaansen 提供。
- **MDL-LIB 2.2**：作者 Martijn Dekker 已将其声明为公共领域；整合了 .typ、.var、.con 文件到 .lib 文件中，避免大量 include，支持 Turbo Pascal 3.3。
- **Kari Lammassaari 的 Pascal MSX 支持文件**：大型支持文件集合。
- **Fossil 驱动接口**：Erik Maas 为 RS232C 设备（如 Sunrise、Philips 调制解调器）制作了 Turbo Pascal 接口。
- **Slotman 的 Turbo Pascal 3.3 IDE**：运行于 PC（Windows），包含游戏开发所需的 include 文件。

## 意义

MSX 上的 Pascal 生态延续了 CP/M 时代的 Turbo Pascal 传统。通过 include 文件与 INLINE 机器码机制，Pascal 程序员能够绕过标准文本输出限制，直接调用 MSX 的图形、BIOS 与通信能力。这一生态是八位机时代高级语言与底层硬件结合的重要案例。
