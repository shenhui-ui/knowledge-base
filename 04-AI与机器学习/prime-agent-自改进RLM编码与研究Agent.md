---
type: ingest-note
date: 2025-07-31
source: https://github.com/PrimeIntellect-ai/prime-agent
---

# Prime Agent：开源自改进 RLM 编码与研究 Agent

Prime Agent 是 PrimeIntellect 开源的编码与研究 Agent，专为通用、长期运行的任务设计。它围绕两个核心抽象构建：**递归语言模型（RLM）** 和 **持续增强系统（Continual Harness）**。

## 核心概念

- **RLM（递归语言模型）**：将上下文视为变量（prompt-as-a-variable），将递归子代理等工具视为函数调用，运行在持久 REPL 中。
- **Continual Harness**：将补充提示、记忆、技能描述和可复用的子代理规格作为持久状态存储，Agent 可通过小的、有证据支持的更新来改进这些状态，默认仅保留在会话本地。

## 主要特性

- 结合持久 Python 控制环境 + 持久 harness 状态，使工作上下文和可复用模式超越单次聊天窗口。
- 一切皆可编程：内置的 IPython 是模型工具；文件操作、shell 命令、工具调用、子代理及上下文管理都通过代码完成。
- 内置子代理：`rlm(...)` 可生成真实的子代理进行并行或后台工作，并以编程方式返回结果。
- 可自我改进：`/refine` 审查当前轨迹，并能对补充 harness 状态应用小的、有证据支持的更新，永不重写不可变的基础系统提示，支持快照回滚。
- 技能可执行：技能是可导入的 Python 包，内置技能创建器可将循环工作流转化为项目或个人技能。
- 后台运行：守护进程支持的 Agent 在终端断开后继续运行，并可在之后重新附着。
- 直接通信：运行中的 Agent 可以彼此交换消息和协调任务，无需经由用户中转。
- 长任务持续：自动压缩、持久目标、心跳、调度、自主模式及保留子代理，跨轮次和终端会话保持进度。这些特性在 TUI 和自主模式下均可用。

## 快速开始

macOS 或 Linux 下安装最新稳定版：

```bash
curl -fsSL https://app.primeintellect.ai/prime-agent/install.sh | sh
```

安装器会下载版本化发布、验证 SHA-256 校验和、安装 `prime-agent` 命令，并可选准备 IPython 运行时。

在目标项目目录启动：

```bash
cd /path/to/project
prime-agent
```

首次启动运行 `/login` 选择订阅或 API Key 提供商。

### 安全注意事项

Agent 会以当前用户权限执行模型生成的 Python 和项目命令。其 worker 与 kernel 进程改善了生命周期隔离和恢复能力，但并非安全沙箱。应使用可回滚的克隆、干净的工作树或其他可检查与恢复的检查点；只使用受信任的仓库、指令、技能和扩展，并在外部沙箱或受限环境中运行不可信代码或指令。

## 常用命令

```bash
prime-agent agents                    # 浏览运行中、空闲、已保存的会话
prime-agent attach <agent>            # 重新附着运行中的会话
prime-agent --resume <path|id>        # 恢复已保存会话
prime-agent status                    # 检查后台服务状态
prime-agent doctor [--fix]            # 检查或修复后台服务
prime-agent update [--force]          # 更新 Prime Agent
prime-agent shutdown [--force]        # 停止所有 Agent、worker 和后台服务
```

## 为长任务而生

Prime Agent 专为长周期工作构建，尤其适合研究中的评估任务。`/refine` 可以将聚焦的、可审查的经验持久化为补充提示、记忆、可复用的技能描述或子代理规格，并记录细化历史，便于追溯与回滚。

## 相关资源

- 官方文档、Verifiers、PRIME-RL、pi-mono 等仓库资源可通过 GitHub 仓库页访问。
- 仓库当前已有较高关注度（Star 13.1k，Fork 1.3k），是一个活跃的开源项目。

## 适用场景

Prime Agent 特别适合研究类长任务，例如评估、代码库探索、复杂多步骤实验。它提供了一种将上下文持久化、技能沉淀和自我改进纳入工作流的方案，是当前开源 Agent 领域中颇具特色的实现。
