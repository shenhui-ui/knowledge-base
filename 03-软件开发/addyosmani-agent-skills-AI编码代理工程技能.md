---
type: ingest-note
source: https://github.com/addyosmani/agent-skills
date: 2026-08-12
---
# AI 编码代理工程技能：addyosmani/agent-skills 与 mattpocock/skills

## 概述

[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) 是一个开源仓库（86.6k stars，9.3k forks，421 commits），提供「生产级工程技能」（Production-grade engineering skills）。它把资深工程师在构建软件时使用的工作流、质量门禁和最佳实践封装成 AI 编码代理可一致遵循的技能包，覆盖从想法到上线的完整开发阶段。仓库根目录包含 `skills/`（技能包）、`commands/`（斜杠命令）、`hooks/`、`references/`、`agents/` 等组织结构，并支持多种智能体框架插件。

## 开发生命周期与命令

仓库将开发流程划分为 6 个阶段（DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP），并提供 8 个斜杠命令来映射整个生命周期：

| 阶段 | 命令 | 关键原则 |
|------|------|----------|
| Define | /spec | Spec before code（先写规格再写代码） |
| Plan | /plan | Small, atomic tasks（小而原子的任务） |
| Build | /build | One slice at a time（一次只做一个切片） |
| Test | /test | Tests are proof（测试就是证明） |
| Review | /review | Improve code health（合并前先审查） |
| Web 性能 | /webperf | Measure before you optimize（先测量再优化） |
| 简化 | /code-simplify | Clarity over cleverness（清晰胜过聪明） |
| Ship | /ship | Faster is safer（更快更安全地交付） |

其中 `/build` 可在规格已经存在时自动生成计划并实施所有任务，只需一次批准计划即可自主运行。它减少了人工步骤，但保留了验证：每个任务仍然以测试驱动的方式单独提交，遇到失败或风险步骤会暂停。

## 技能自动激活

除了斜杠命令，技能也会根据当前工作自动激活。例如设计 API 时触发 `api-and-interface-design`，构建 UI 时触发 `frontend-ui-engineering`。仓库共打包 24 个技能，可通过 CLI 安装到 70+ 种智能体（Claude Code、Cursor、Codex、Copilot、Cline 等）。

## 安装与集成

### 通用 CLI

- `npx skills add addyosmani/agent-skills` 安装全部 24 个技能
- `npx skills add addyosmani/agent-skills --list` 浏览后再安装
- `npx skills add addyosmani/agent-skills --skill <name>` 单独安装某个技能，例如：
  - `--skill code-review-and-quality`（合并前五维审查）
  - `--skill interview-me`（逐问题需求盘问）
  - `--skill test-driven-development`（强制红-绿-重构）

**单技能安装注意事项**：单技能安装时 `npx` 只复制 `skills/<name>/` 目录，不会复制仓库级的 `references/` 共享清单目录。技能仍可运行，但指向共享检查清单的路径不可用。解决办法是采用整仓集成、克隆仓库，或将所需清单复制到已安装技能内部的 `references/` 目录中（该问题跟踪于 [#361](https://github.com/addyosmani/agent-skills/issues/361)）。

### Claude Code（推荐）

Marketplace 安装：

```
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

SSH 错误处理：如果本机没有配置 GitHub SSH key，marketplace 克隆会失败，可在 `marketplace add` 时使用完整 HTTPS URL 强制走 HTTPS：

```
/plugin marketplace add https://github.com/addyosmani/agent-skills.git
/plugin install agent-skills@addy-agent-skills
```

若在 Windows/macOS 上 `/plugin install` 仍报 `git@github.com: Permission denied (publickey)`，可全局配置 Git 将 GitHub SSH URL 重写为 HTTPS 供子进程克隆使用：

```
git config --global url. "https://github.com/".insteadOf git@github.com:
```

本地/开发方式：

```
git clone https://github.com/addyosmani/agent-skills.git claude --plugin-dir /path/to/agent-skills
```

### Cursor

将工作流技能放到 `.cursor/skills/`（从 `agent-skills/skills/` 同步），将简短策略放到 `.cursor/rules/*.mdc`，不要把完整技能粘贴进 rules。详细步骤见 `docs/cursor-setup.md`。

### Antigravity CLI

可作为原生插件安装，支持技能、子代理和斜杠命令，参考 `docs/antigravity-setup.md`。

## 相关链接

- 仓库：https://github.com/addyosmani/agent-skills
- 文档：`docs/cursor-setup.md`、`docs/antigravity-setup.md`
