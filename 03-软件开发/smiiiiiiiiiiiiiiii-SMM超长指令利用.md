---
type: ingest-note
title: smiiiiiiiiiiiiiiii：用超长指令打破x86 SMM同步
source: https://github.com/xoreaxeaxeax/smiiiiiiiiiiiiiiii
date: 2026-04-27
---

# smiiiiiiiiiiiiiiii：用超长指令打破x86 SMM同步

xoreaxeaxeax 开源的 PoC，展示只需一条“长得离谱”的机器指令即可破坏 x86 CPU 的 SMM（系统管理模式）同步机制，使单个核心在 SMM 内执行时，另一个核心仍停留在 SMM 外，从而打破 SMM 的安全隔离模型。

## 原理

SMM 要求所有核心要么全部进入 SMM，要么全部退出 SMM。其安全模型依赖于这个“全进全出”的约束：当一个线程进入 SMM 时，硬件会强制其他核心也进入。

攻击的关键在于：让某个核心长时间忙于执行一条不可中断的指令，从而无法响应 SMI（系统管理中断）。SMI 只在指令边界触发，因此只要一条指令的执行时间超过 SMM 同步等待超时，该核心就会错过同步。

具体时序：

1. Core 0 开始执行一条超长指令（约 40 亿周期，超过 1 秒）。
2. Core 1 触发 SMI，等待 Core 0 进入 SMM。
3. 固件中的 SMM 同步代码最多等待 1 秒（`mTimeoutTicker`）。
4. Core 1 等待超时后放弃，独立进入 SMM 执行秘密代码。
5. Core 1 退出 SMM 后，Core 0 才姗姗来迟“加入” SMM。

此时 Core 1 在 SMM 外、Core 0 在 SMM 内，Core 1 就可以攻击 Core 0。

## 关键代码片段

### x86 固件的 SMM 同步等待逻辑

```c
for ( Timer = StartSyncTimer (); 
      ! IsSyncTimerTimeout ( Timer , mTimeoutTicker ) && SyncNeeded ; ) {
    mSmmMpSyncData -> AllApArrivedWithException = AllCpusInSmmExceptBlockedDisabled ();
    if ( mSmmMpSyncData -> AllApArrivedWithException ) {
        break;
    }
    CpuPause ();
}
```

### PoC 中的超长加载指令

针对 Zen 3 Ryzen 7 5800H，使用宽 XMM 加载从慢速 MMIO 地址读取：

```asm
mov $0xfcc68860, %rsi   ; 目标 MMIO 地址
vmovdqu (%rsi), %xmm0   ; 非常非常长的加载
```

受害核心循环执行该加载，忙于处理慢速 MMIO 响应而无法响应 SMI：

```c
for (;;)
    asm volatile ("vmovdqu (%0), %%xmm0" :: "r" (mmio) : "xmm0");
```

另一个核心则通过 MSR 配置核心性能计数器并触发 SMI，使同步机制超时。

## 技术要点

- 需要找到高延迟 MMIO 地址（如未公开的慢速响应区域）。
- 使用 ISA 中最宽的加载指令，单条指令搬运尽可能多的字节。
- 让其他核心竞争同一总线，进一步减缓读取速度。
- 具体可利用的 MMIO 地址因平台而异，PoC 目前针对 AMD Zen 3。

## 影响与意义

- 打破 SMM“所有核心同步进出”的根基，可能为更深层的固件级攻击铺路。
- 展示了现代 CPU 微架构与固件假设之间的鸿沟。
- 属于低层系统安全研究的重要样例，与 [[Rosenbridge-x86硬件后门研究]] 等主题同属 x86 攻防研究谱系。

## 参考链接

- 仓库：https://github.com/xoreaxeaxeax/smiiiiiiiiiiiiiiii
