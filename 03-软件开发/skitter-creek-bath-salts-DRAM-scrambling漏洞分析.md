---
type: ingest-note
source: https://github.com/xoreaxeaxeax/skitter-creek-bath-salts
date: 2026-08-01
---

# skitter-creek-bath-salts：利用DRAM scrambling解锁CPU

## 概述

skitter-creek-bath-salts 是一个针对 AMD Family 16h CPU 的安全研究项目，通过操纵 DRAM scrambling（内存扰码）机制，重写物理 DRAM 地址翻译，从而暴露内核不可见的受保护内存区域（carveouts）。该攻击可解锁 Platform Security Processor (PSP)、System Management Mode (SMM)、C6 DRAM 状态以及 CPU 微码，打破了建立在物理地址隔离之上的安全基元。

## 核心原理

现代 CPU 在访问 DRAM 时，虚拟地址需要经过 MMU 页表转换、IOMMU、MTRR/PAT、缓存一致性协议等多层抽象，最终到达内存控制器（MCT/IMC）。DRAM scrambling 是内存控制器对物理地址进行的一种额外重新映射，旨在将数据在 DRAM 芯片上打散。skitter-creek-bath-salts 通过修改 DRAM 控制器的翻译寄存器，使一个地址可以“落”到内存中的任意位置，从而绕过基于地址隔离的安全保护。

项目作者指出：

> Poke the DRAM controller and an address can be made to land wherever you want in memory.

## 影响范围

- **目标平台**：AMD Family 16h CPU（最后一代数据手册公开了 DRAM 控制器翻译寄存器且未锁定的一代）。后续 17h 及更高架构不再公开这些信息，但底层变换在 ARM、RISC-V 等架构中同样存在。
- **解锁目标**：
  - Platform Security Processor (PSP)
  - System Management Mode (SMM)
  - C6 DRAM 状态
  - CPU 微码

## 技术细节：一次完整的内存访问路径

项目中用生动的 ASCII 图展示了从 `*p` 到 DRAM 的完整路径，包括：

- CPU core / MMU：虚拟地址检查、TLB probe、页表分级查询、保护键、EPT/NPT 重走、TLB shootdown
- IOMMU：设备 DMA 页表翻译
- 缓存与一致性：L1/L2/LLC 探测、MESI/MOESI 协议、QPI/UPI/Infinity Fabric 广播
- 数据互连：MMIO 或 DRAM 路由
- 内存控制器：DRAM hole remap、地址交错、DRAM scrambling

攻击正是在最后的“MCT / IMC”层介入，通过修改翻译寄存器实现物理地址重写。

## 利用方式

项目仓库包含 kernel 与 userspace 代码、分析/数据目录、Makefile 与 USAGE。利用流程大致为：

1. 定位 DRAM 控制器的翻译寄存器（在 Family 16h 上可读写且未锁定）。
2. 修改地址翻译规则，使目标物理地址落入受保护区域。
3. 绕过隔离边界，读取或修改 PSP、SMM、微码等保留区域。

## 防御与影响

该研究揭示了依赖物理地址保密的安全模型缺陷。DRAM scrambling 本可作为一种混淆层，但其设计未考虑对抗拥有内核权限或直接物理访问的攻击者。AMD 后续架构虽然不再公开寄存器细节，但安全问题并未根除，只是提高了研究门槛。

对于系统安全设计者而言，此工作表明：物理地址隔离必须作为攻击面的一部分来评估，不能假设 DRAM scrambling 或内存控制器机制可提供强安全保证。

## 参考

- GitHub 仓库：https://github.com/xoreaxeaxeax/skitter-creek-bath-salts
