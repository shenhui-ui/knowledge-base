---
type: ingest-note
source: https://blog.getutm.app/2026/introducing-triton-directx-11-driver-for-qemu/
date: 2026-08-10
---
# QEMU Triton：Windows 客户机 DirectX 11 加速驱动

## 概述

本文介绍 QEMU 中新一代 Windows 图形加速方案 Triton。Triton 是一个全新的 Windows 驱动，与之前的 Neptune（Direct3D 协议转发层）配合，为 QEMU 虚拟机带来完整的 DirectX 11 支持。该方案在 Windows 11 ARM64 虚拟机上成功运行了《Crash Bandicoot Trilogy》（x64）。

## 背景：Neptune 与 Wine 路径

Neptune 是面向 VirtIO 的 Direct3D 协议转发层，能够将 Direct3D API 调用序列化并跨虚拟机边界传输，从而在 Linux 客户机中运行 Wine 游戏。相比客户机内直接使用 DXVK，该方案性能更好，但真正的目标是为 Windows 客户机提供现代图形加速。

## 为什么不能直接复用 d3d11.dll 替换方案

有人可能认为，既然 Neptune 的 Mesa 驱动实现了 `d3d11.dll` 和 `dxgi.dll`，那么将这些文件放在游戏可执行文件旁边就能让 Windows 游戏加载它们。然而这种方案存在诸多问题：

1. **性能差**：窗口合成器（DWM）会将帧视为图像，需要通过 CPU blitting 将 GPU 图像缓冲区拷贝到正确位置，无法获得流畅的桌面体验。
2. **系统核心组件不可替换**：`d3d11.dll` 和 `dxgi.dll` 是 Windows 核心组件，替换系统文件可能导致系统不稳定。
3. **反作弊检测**：许多游戏的防作弊系统会检测此类 DLL 修改，导致游戏无法运行。
4. **易用性差**：每个需要加速的应用都要手动拷贝 DLL，用户体验不佳。

## 正确思路：实现 DDI（设备驱动接口）

正确方案不是实现 DirectX API，而是实现 DirectX DDI（Device Driver Interface）。Windows 图形栈结构如下：

```
用户态应用
    ↓
Direct3D 11 (d3d11.dll)
    ↓
用户态驱动 (UMD) —— 实现 DDI
    ↓
DXGI (dxgi.dll)
    ↓
内核态驱动 (KMD)
    ↓
硬件 / 虚拟化
```

应用通过系统 Direct3D/DXGI 库与驱动通信，`d3d11.dll` 负责状态跟踪，并将简化后的命令流发送给实现 DDI 的用户态驱动（UMD）。UMD 再通过 DXGI 与内核态驱动（KMD）通信。KMD 由图形厂商实现，驱动真实硬件（这里为虚拟硬件）。

## Triton 的实现路径

在 Wine 中，Neptune 实现了自定义的 `d3d11.dll` 与 `dxgi.dll` 来拦截 API。对于 Windows，则需要实现 UMD 和 KMD。幸运的是，KMD 部分已有基础：

- **anonimix007** 与 **arehnman** 分别独立开发了用于 Venus（Vulkan）的 KMD。
- 由于 Vulkan 是独立图形 API，其 UMD 类似“替换 d3d11.dll”的方法，直接与 KMD 通信驱动 QEMU。
- 因为 Neptune 的模型与 Venus 相似，内核接口（DMA、命令缓冲等）非常接近，UMD 与 KMD 之间的接口也完全相同。

最终，团队选择以 anonymix007 的分支为基础，因为其 KMD 实现的功能更多。

## 难点：实现 DirectX 11 DDI

实现 DirectX 11 的 DDI 是本次工作的核心难点。开源 DDI 实现非常稀少，Windows 图形驱动是一个极小众领域，多数专家集中在少数几家图形硬件厂商。这也解释了为何 QEMU 在 Windows GPU 加速方面长期进展缓慢。

不过仍有可参考的开源实现：

- Mesa 提供了 DirectX 10 UMD。
- 其他相关实现可提供借鉴。

通过借鉴前辈经验，Triton 最终实现了 DirectX 11 的 DDI，配合 Neptune 在 QEMU 中实现了完整的 DirectX 11 加速。

## 影响与展望

Triton 的发布意味着 QEMU 中的 Windows 虚拟机可以获得原生级 DirectX 11 图形加速，极大改善 Windows 虚拟化的图形性能，尤其是游戏和图形密集型应用。该方案也展示了如何利用已有 Vulkan/Venus 基础设施来扩展 DirectX 支持，未来可能进一步支持更高版本的 DirectX。

---

**source**: 素材来源（原文链接待补充）  
**date**: 2025-08-01