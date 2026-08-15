---
type: ingest-note
title: 手机变身服务器：Android + Termux 取代 VPS
source: https://blog.example.com/cmf-phone-server
 date: 2025-07-30
---

# 手机变身服务器：Android + Termux 取代 VPS

本文记录了作者将一台 CMF Phone 1 改造成家庭服务器的完整过程，旨在替代原先的 Hetzner VPS。

## 背景

个人基础设施曾运行在 Hetzner VPS 上，包括 Web 应用、远程浏览器 Surf、Caddy 等。VPS 成本高，入门机型性能不足。DRAM 价格暴涨，自行组装新机不划算，于是想到利用手头的 CMF Phone 1 作为服务器。

该手机拥有 8 核 ARM、8GB RAM、128GB 存储、Wi-Fi 6、5G，内置电池，适合充当不关机的小型服务器。

## 失败尝试：刷入 postmarketOS

作者首先尝试用 postmarketOS 替代 Android，但 Wi-Fi、蓝牙、硬件加速等驱动不完善，导致启动后黑屏，并且恢复原厂系统的过程也十分曲折（需 Windows + QEMU 直通 + MediaTek 驱动）。最终成功恢复，但得出教训：Android 驱动全部齐全，不应抛弃。

## 成功方案：Android + Termux

保留 Android，将 Termux 作为宿主环境：

- 提供 OpenSSH、runit、Caddy、Cloudflared、软件包管理
- Termux:Boot 负责开机自启
- Tailscale 提供稳定内网地址，可 `ssh cmf`

各应用以 Linux 用户空间运行在 Termux 之上，由 runit 监督。

## 系统架构

```
Android boot
→ Tailscale 常开 VPN
→ Termux:Boot 启动 runit
→ runit 启动常驻服务
→ 本地/公网健康检查
```

## Android 主机配置

作者用 Ansible 配置了以下关键项：

- 持久唤醒锁，禁用空闲休眠
- 豁免 Termux、Termux:Boot、Tailscale 后台限制
- 禁用子进程限制
- 防止 Wi-Fi 挂起
- Tailscale 设为始终开启的 VPN

## 结论

这不是传统 Linux 服务器，没有 systemd 和 Docker daemon，但底层是 Linux 内核 + 足够强大的用户态，足以替代 VPS。手机移动时也能通过网络可达，重启后自动恢复。
