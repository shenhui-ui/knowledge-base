---
type: ingest-note
source: "https://fellowship.blog/2024/07/eufy-video-doorbell-research"
date: "2024-07-01"
---

# Eufy安全视频门铃逆向工程分析

本文是对 Eufy Security Video Doorbell 生态系统的安全研究笔记，基于公开博客文章整理。

## 研究背景

作者在参加 EuskalHack 大会后，注意到城市中大量短租民宿安装了视频门铃，决定研究最常见的型号。最终目标是 Eufy Security Video Doorbell，由 Homebase Station 2 和门铃本体组成。

## 生态系统架构

- Homebase Station 2：作为中央网关，连接互联网（Wi-Fi/以太网）。
- Doorbell：通过隐藏Wi-Fi网络与Homebase通信，网络名为 `OCEAN_XXXXXX`，后缀为Homebase MAC地址的后24位。
- 手机App控制Homebase和门铃，实现查看视频、管理等。

Homebase同时充当路由器，若接入隐藏网络，可访问内网其他设备。

## 漏洞1：Jamming（无线干扰）

利用标准WPA2的deauth攻击，可远程持续发送取消认证帧，使门铃断开隐藏网络。结果：视频/音频仅在本地记录，无法实时传输到Homebase或App。这为物理接近门铃提供了时间窗口。

## 漏洞2：声波同步协议（待补充）

0x03小节涉及声波同步协议的反向工程，素材未提供细节。

## 漏洞3：从内存转储提取并解密OCEAN凭据（待补充）

0x04小节说明恢复并逆向工程了加密配置文件，该文件包含门铃连接隐藏网络所需的凭据。素材未提供细节。

## 相关研究

本文参考了USENIX关于Eufy生态系统的研究：《Reverse Engineering the Eufy Ecosystem: A Deep Dive into Security Vulnerabilities and Proprietary Protocols》（2023）。

---

*注意：原始素材为英文博客节选，部分章节内容缺失，后续可补充。*