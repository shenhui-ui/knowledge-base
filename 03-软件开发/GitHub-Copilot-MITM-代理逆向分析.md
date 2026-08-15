---
type: ingest-note
title: GitHub Copilot 置于 MITM 代理后的逆向分析
date: 2026-08-04
source: "https://lighthouse.ai"
---

# GitHub Copilot 置于 MITM 代理后的逆向分析

作者 Rafael Pierre 在 Lighthouse Newsletter 中分享了他如何通过 MITM 代理检查 GitHub Copilot 的网络流量，以探索其内部工作原理。本文记录该文章的核心背景与方法论。

## 背景

近两年 AI 应用和功能激增，传统厂商如 Slack 快速添加 AI 功能，而 Cursor、Notion、ChatGPT Desktop、Claude Desktop 等则以 AI 为核心。作者对这些应用的内在工作机制产生好奇，希望通过逆向工程窥探其底层实现。

巧合的是，作者发现自己的 Copilot 配额每月消耗得越来越早，因此选择 VS Code 与 Copilot 作为主攻方向。

## Electron 共性

上述应用绝大多数基于 Electron 构建。Electron 将 Node.js 运行时与 HTML/CSS/JavaScript 打包，再通过 Chromium 渲染，从而用一套代码库跨平台运行，免去为不同平台分别维护原生代码的负担。这带来了架构上的相似性：探测一个应用所学到的经验大多可迁移到其他应用。

## 方法：从源代码转向运行时观测

作者最初打算直接阅读 VS Code 源代码，但面临两个问题：
- 尚未形成明确的问题集，在数百万行代码中搜索会耗费大量时间或 token；
- 源代码描述的是应用“能做什么”，而运行时观测才能发现“实际做了什么”。

此外，VS Code 的开源程度在同类应用中属于例外，Claude、ChatGPT、Notion、Slack 等均非开源（注：Codex 源码在 GitHub 可用）。因此作者转向逆向工程路线：先被动观察网络流量，让请求与响应指引出值得深挖的问题，再回到源码验证。

## 拦截 Electron 网络流量

Electron 应用内置 Chromium，渲染进程可使用浏览器的网络栈发起 HTTP/WebSocket 请求；也可通过 Node 的 http/https/fetch 发起。请求路径的不同影响拦截方式。VS Code 采用解耦架构，存在独立的扩展宿主进程，有助于区分 UI、IDE 功能和插件职责。

经典的网络流量拦截方式是搭建代理服务器，让应用走代理——即 MITM（中间人）代理。代理拦截客户端发出的 HTTP 请求，转发到服务器，并转发响应。企业环境中常以类似手段做流量审查。开源工具 mitmproxy 是此场景的常用选择。

## 待续

原文后续将深入展示实际捕获到的 Copilot 网络流量、harness、内存及“上下文即产品”的洞察，留待后续补充。
