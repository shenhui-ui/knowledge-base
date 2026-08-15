---
type: ingest-note
source: https://sspai.com
date: 2026-08-01
---

# 借助ACC实现旧手机直供电改造

## 背景

去年4月，我受视频影响，萌生了将旧安卓手机利用起来的想法。后续虽然跑起来了，但设备长期充电，电池安全成为难题。此前通过拆机飞线直供电解决鼓包问题，但破坏物理结构，存在安全隐患。本文介绍利用 Advanced Charging Controller (ACC) 实现不拆机的直供电。

## ACC 工作原理

ACC 通过读写系统底层的充电参数，接管手机硬件原本的充电行为，进而实现对充电的精准控制。原生系统插上充电器就充电，充满就停；ACC 相当于一个“充电开关”，可以自由设置充电过程（例如电量降到 40% 启动充电，升到 60% 停止），甚至让电流绕过电池直接为主板供电，即直供电/旁路供电（battIdleMode）。

## 安装准备

1. 获取 Root 权限（参考极客湾视频教程）
2. 安装 Magisk
3. 安装 ACC 模块：
   - 从 GitHub Releases 下载最新 .zip
   - 传输到手机，打开 Magisk → 模块 → 从本地安装
   - 重启手机
4. 安装 Termux（用于命令行控制）

## 配置 ACC

在 Termux 中执行：

```bash
su                          # 获取root权限
acc -v                      # 查看版本
acc -u dev                  # 更新到最新开发版
```

然后插上充电线，执行测试：

```bash
acc -t
```

该命令会测试所有可用的充电开关，测试结果会显示在屏幕并生成 .log 文件。选择最后两行显示 `Switch works ✅ battIdleMode=true` 的开关。

示例输出：

```
6/33: battery/constant_charge_current_max 3300000 0
off (0) -6mA Idle
on (3300000) -6mA Idle
on (3300000) -866mA Charging
Switch works ✅ battIdleMode=true
```

其中 `battIdleMode=true` 表示支持直供电模式。

### 指定充电开关

例如使用 `battery/constant_charge_current_max 3300000 0` 开关：

```bash
acc -s s="battery/constant_charge_current_max 3300000 0 --"
```

确认设置：

```bash
acc -s
```

### 设置充电策略

通过电量百分比控制：

```bash
acc 50 40
```

表示电量达到 50% 停止充电，降到 40% 恢复充电。此时充电停止后即进入直供电模式。

## 注意事项

- 测试时请使用原装充电头和数据线，保证结果可靠。
- ACC 为纯后台服务，无图形界面，建议使用 Termux 命令行操作。
- 第三方客户端 ACCA / ACC Settings 已停止维护，不推荐使用。

来源：少数派（原文链接未提供）
