---
type: ingest-note
source: https://github.com/lajosdeme/mole
date: 2025-02-24
---

# mole - 深度研究代理（强制预算与本地隐私边界）

mole 是一个深度研究代理，运行在本地，使用自己的 API 密钥，通过 MCP 与编码代理集成。它把问题分解，搜索、读取来源、提取声明、对照原文逐条核查，并写出带引用的答案。

## 核心特性

- **预算强制**：每次模型调用前预留预算，调用后结算，数据库 schema 中有非负约束。`--usd 0.50` 意味着运行在五十美分内停止。测试语料库中实测超支为 0%。
- **引用验证**：每条声明都带有引用，且在提取时验证引用是否逐字出现在来源页面中，不匹配的声明会被丢弃。后续可重新对照来源，不被支持的声明会在报告中标记。
- **本地隐私边界**：本地 CSV 或文件夹的数据不会离开机器。模型选择假设模板和列名，mole 渲染并运行 SQL，只允许聚合结果（计数、均值、测试结果、至少覆盖五条记录的桶）离开。`mole crossings` 显示流出内容。

## 安装

- **脚本**：`curl -fsSL https://raw.githubusercontent.com/lajosdeme/mole/main/install.sh | sh`（Linux/macOS，amd64/arm64），安装到 `~/.local/bin` 或 `/usr/local/bin`，验证 SHA-256。
- **Homebrew**：`brew install lajosdeme/mole/mole`（注意 homebrew/core 中的无关 mole）。
- **Arch Linux**：AUR 包 `mole-research-bin` 或 `mole-research`。
- **Debian/Ubuntu**：从 releases 页下载 .deb，或 .rpm。
- **源码**：Go 1.25+，`go install github.com/lajosdeme/mole/cmd/mole@latest` 等。

## 配置

密钥存放在 `~/.config/mole/config.json`（模式 0600），命令如 `mole config set search.provider tavily` 等。

以上内容基于素材整理，更多信息见 [GitHub 仓库](https://github.com/lajosdeme/mole)。