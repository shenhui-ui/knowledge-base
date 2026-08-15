---
type: ingest-note
date: 2014-08-19
source: https://github.com/alfikpl/ao486
---

# ao486：x86兼容Verilog核心

## 项目概述

ao486 是一个 x86 兼容的 Verilog 内核，实现了 486 SX 的全部特性。该内核基于 Bochs 软件 x86 实现进行建模和测试。除了 486 内核，ao486 项目还包含一个能够启动 Linux 3.13 和 Microsoft Windows 95 的 SoC。

## 特性

- 4 级流水线架构：decode、read、execute、write
- 完整实现所有 486 指令，支持 CPUID
- 16 kB 指令缓存
- 16 kB 写回数据缓存
- 32 项 TLB
- Altera Avalon 接口（内存和 IO 访问）

## SoC 组成

- ao486 处理器
- IDE 硬盘驱动（重定向到 HDL SD 卡驱动）
- 软驱控制器（也重定向到 SD 卡驱动）
- 8259 PIC、8237 DMA
- Sound Blaster 2.0（DSP 和 OPL2，FM 合成未完全支持），声音输出重定向到 WM8731 音频编解码器
- 8254 PIT、8042 键盘鼠标控制器、RTC、标准 VGA
- 所有组件均建模为 Altera Qsys 组件，Altera Qsys 连接所有部件并提供 SDRAM 控制器

## 平台支持

目前仅运行在 Terasic DE2-115 开发板上（Altera Cyclone IV E EP4CE115F29C7）。时钟 30 MHz（最高 39 MHz）。

## 资源占用

| 单元 | 逻辑单元 | M9K内存块 |
|------|---------|-----------|
| ao486处理器 | 36517 | 47 |
| 软驱 | 1514 | 2 |
| 硬盘 | 2071 | 17 |
| NIOS2 | 1056 | 3 |
| 片上NIOS2 | 0 | 32 |
| PC DMA | 848 | 0 |
| PIC | 388 | 0 |
| PIT | 667 | 0 |
| PS2 | 742 | 2 |
| RTC | 783 | 1 |
| 声卡 | 37131 | 29 |
| VGA | 2534 | 260 |

编译后整体资源使用（Quartus II 13.1，Cyclone IV E）：

- 总逻辑单元：91,256 / 114,480（80%）
- 组合功能：86,811 / 114,480（76%）
- 专用逻辑寄存器：26,746 / 114,480（23%）
- 总寄存器：26,865
- 总引脚：108 / 529（20%）
- 总内存位：2,993,408 / 3,981,312（75%）
- 嵌入式9位乘法器：44 / 532（8%）
- 总PLL：1 / 4（25%）

## 性能基准

使用来自 http://www.roylongbottom.org.uk/dhrystone%20results.htm 的 DosTests.zip 进行基准测试：

| 测试 | 结果 |
|------|------|
| Dhrystone 1 非优化 | 1.00 VAX MIPS |
| Dhrystone 1 优化 | 4.58 VAX MIPS |
| Dhrystone 2 非优化 | 1.01 VAX MIPS |
| Dhrystone 2 优化 | 3.84 VAX MIPS |

## 软件兼容性

成功运行以下软件：

- Microsoft MS-DOS 6.22
- Microsoft Windows for Workgroups 3.11
- Microsoft Windows 95
- Linux 3.13.1

## BIOS

- 使用 Bochs 项目（2.6.2）的 BIOS，为支持硬盘做了少量修改
- VGA BIOS 来自 VGABIOS 0.7a（无需修改），VGA 模型不支持 VBE 扩展，因此禁用了扩展

## NIOS2 控制器

SoC 使用 Altera NIOS2 处理器管理所有组件并显示 OSD（屏幕显示）。OSD 允许用户插入和移除软盘。

## 许可证

- rtl、ao486_tool、sim 目录：BSD 许可证
- bochs486、bochsDevs 目录：来自 Bochs 项目，LGPL 许可证
- sd/fd_1_44m/fdboot.img：来自 FreeDOS 项目
- sd/bios/bochs_legacy：Bochs 项目编译的 BIOS
- sd/vgabios/vgabios-lgpl：vgabios 项目编译的 VGA BIOS

## 状态历史

- 2014年3月31日：初始版本 1.0
- 2014年8月19日：driver_sd 更新，ps2 修复

## 编译

要编译包含 NIOS II 微控制器的 SoC，需要 Altera Quartus II 软件。SoC 的 Verilog 组件（特别是 ao486 处理器）应该可以在任何 Verilog 编译器中编译。目前 synthesis 项目文件已准备。

Source: https://github.com/alfikpl/ao486
Date: 2014-08-19
