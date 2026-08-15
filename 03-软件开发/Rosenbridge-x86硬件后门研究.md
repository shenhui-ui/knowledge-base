---
type: ingest-note
date: 2026-04-27
source: https://github.com/xoreaxeaxeax/rosenbridge
---

# Rosenbridge：x86 CPU硬件后门研究

## 概述

Rosenbridge 项目揭示了部分桌面、笔记本和嵌入式 x86 处理器中存在硬件后门。该后门允许 ring 3（用户态）代码绕过处理器保护机制，自由读写 ring 0（内核态）数据。

虽然该后门通常被禁用（需要 ring 0 权限才能开启），但在某些系统上默认即为启用状态。本仓库包含了检测处理器是否受影响、关闭后门的工具，以及用于发现和分析后门的研究与工具。

## 后门原理

- Rosenbridge 后门是一个与主 x86 核心并列的小型非 x86 核心。
- 通过模型特定寄存器（MSR）控制位启用，并使用启动指令（launch instruction）触发。
- 恶意指令被包装在特殊格式的 x86 指令中，隐藏核心执行这些命令（称为“深度嵌入指令集”，DEIS），从而绕过所有内存保护和权限检查。
- 该后门深度远超已知的协处理器（如 Management Engine 或 Platform Security Processor），不仅能访问全部内存，还能访问寄存器文件和执行流水线。

## 受影响系统

- 目前认为仅 VIA C3 CPU 受影响。
- C 系列处理器面向工业自动化、POS 机、ATM、医疗硬件以及部分消费级台式机和笔记本。
- 后续 CPU 代际已不再包含该特性，因此影响范围有限。

## 检查与关闭

### 检查自己的 CPU 是否受影响

```bash
git clone https://github.com/xoreaxeaxeax/rosenbridge
cd rosenbridge/util
make
sudo modprobe msr
sudo ./bin/check
```

注意：该工具必须在裸机（非虚拟机）上运行，且处于 alpha 状态，可能会使不含后门的系统崩溃、死机或挂起。此外，这些工具针对特定处理器家族和核心设计；如果后门与所研究的形态相比有细微改动，工具将无法检测到。

### 关闭后门

如果检查显示系统易受影响，可在启动早期安装脚本关闭后门：

```bash
cd fix
make
sudo make install
reboot
```

注意：即使关闭，具有内核级访问权限的攻击者仍可重新启用后门。该脚本只是启动过程中的纠正措施，需适配不同系统。

## 研究工具

- **sandsifter**：用于发现未知指令的模糊测试工具。
- **asm**：深度嵌入指令集（DEIS）的汇编器，可将自定义 rosenbridge 汇编程序转换为 x86 指令。
- **esc**：利用 rosenbridge 后门进行权限提升的概念验证。
- **fix**：通过模型特定寄存器更新关闭漏洞的修复方案。
- **fuzz**：用于模糊测试 x86 和 rosenbridge 核心，隔离未知的启动指令和桥接指令，并解析 rosenbridge 核心指令格式。
- **deis**：用于探索深层次嵌入指令集的模糊测试器。

## 研究意义

该工作作为案例研究和思想实验，展示在日益复杂的处理器中可能出现怎样的后门，以及研究人员和最终用户如何识别此类特性。这里提供的工具和研究为更深入的处理器漏洞研究提供了起点。
