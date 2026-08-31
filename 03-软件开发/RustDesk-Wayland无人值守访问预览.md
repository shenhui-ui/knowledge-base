---
type: ingest-note
source: RustDesk
date: 2026-08-01
---

# RustDesk Wayland 无人值守访问预览

RustDesk 宣布推出基于 Wayland 的无人值守访问预览版。Wayland 支持一直是 Linux 远程桌面中最困难的部分之一。该预览版允许在 Wayland 上实现真正的无人值守访问，无需远程机器上有人批准每个会话。同时支持多显示器设置。初始设置后，即使重启后无人值守，也可以从登录屏幕连接。

目前该预览版仅适用于 x86_64 Debian/Ubuntu 系统，作为独立版本发布。RustDesk 希望获得更多真实世界测试，因为 Wayland 在主流远程桌面产品中支持仍然有限。例如 AnyDesk 目前要求 Xorg 进行 Linux 传入会话，TeamViewer 仍将 Wayland 支持描述为实验性。

一旦实现稳定，RustDesk 计划将无人值守 Wayland 访问带到更多 Linux 发行版，包括 Fedora 和 Arch Linux，并最终包含在标准 RustDesk 发布版中。

（来源：RustDesk）