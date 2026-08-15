---
type: ingest-note
date: 2026-08-01
source: https://github.com/TheRealYT/git-knife
---

# git-knife：Git 提交历史元数据编辑工具

git-knife 是一款基于 Tauri 的跨平台桌面 GUI，用于直接编辑 Git 提交的元数据：提交消息、作者/提交者姓名、邮箱和日期。它通过调用系统 git CLI 并使用 `git commit-tree` 重建提交，复用原始 tree 对象，因此文件内容不会被改动。

## 为什么需要它

现有图形工具（GitKraken、Sublime Merge、Fork、SmartGit、lazygit 等）在 reword 和 reorder 上体验良好，但普遍将提交日期视为不可变，很少暴露 committer date 和作者身份字段；而能够重写这些元数据的命令行工具（`git-filter-repo`、rebase 环境变量技巧、`git commit-tree` 等）缺少图形界面。git-knife 正好填补了这一空白，同时支持批量查找替换。

## 功能特性（MVP）

- 通过 ref 直接打开并编辑本地分支，无需 checkout，不会影响工作树
- 编辑提交消息、作者/提交者姓名与邮箱、作者日期与提交者日期
- 批量查找替换（支持文本和正则），适合统一修正错误邮箱
- 应用前预览所有变更
- 自动创建备份 ref，支持一键恢复
- 检测并警告已推送历史的改写
- 对签名提交进行识别，警告重写会去除签名，并可选择用你的密钥重新签名
- 合并提交当前不可编辑（锁定）

## 技术实现

- 前端：TypeScript + Vite（从 `package.json`、`vite.config.ts` 可见）
- 桌面壳：Tauri v2 + Rust
- 版本控制操作：直接 shell 调用系统 git，使用 `git commit-tree` 重建提交

## 与其他工具对比

与 GitKraken、Sublime Merge 等相比，git-knife 独有：可编辑任意提交的 committer date 和 author date、可编辑 author/email、支持正则批量替换。GUI 工具大多不支持这些；CLI 工具又缺乏 GUI。

## 构建与运行

依赖：Git 2.x、Node.js + pnpm、Rust（stable）。开发运行：`pnpm install && pnpm tauri dev`。打包：`pnpm tauri build`。GitHub Actions 已配置自动构建 macOS/Linux/Windows 安装包，推 tag 即可触发发布。

## 当前状态与规划

MVP 已实现核心编辑、批量替换、预览、备份恢复和签名处理；计划支持 reorder / squash / drop、合并提交重写等功能。
