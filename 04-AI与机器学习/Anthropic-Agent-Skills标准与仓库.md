---
type: ingest-note
source: https://github.com/anthropics/skills
date: 2026-08-15
---

---
type: ingest-note
source: https://github.com/anthropics/skills
date: 2025-07-25
---

# Anthropic Agent Skills 标准与示例仓库

> Anthropic 官方开源仓库，包含用于 Claude 的 Agent Skills 技能实现、规范与模板。

## 概述

Agent Skills 是 Claude 按需加载以提升特定任务表现的技能包，由指令、脚本和资源组成。本仓库展示了多种技能模式，涵盖创意应用、技术任务与企业工作流。

## 仓库结构

- `skills/`：示例技能集合，分为创意与设计、开发与技术、企业沟通、文档技能等类别；
- `spec/`：Agent Skills 规范（标准定义）；
- `template/`：创建自定义技能的模板；
- 文档技能（docx、pdf、pptx、xlsx）采用 source-available 许可，作为复杂技能的参考。

## 安装与使用

### Claude Code

注册为插件市场：

```sh
/plugin marketplace add anthropics/skills
```

安装类插件：

```sh
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

安装后直接描述需求即可触发技能，例如：

> "Use the PDF skill to extract the form fields from path/to/some-file.pdf"

### Claude.ai

示例技能已内置在付费计划中，也可上传自定义技能。

### Claude API

支持使用预构建技能及上传技能，参见官方 Skills API Quickstart。

## 创建基本技能

只需一个文件夹和 `SKILL.md` 文件：

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
---

# My Skill Name

[Add your instructions here...]

## Examples
...
## Guidelines
...
```

frontmatter 仅需 `name` 和 `description` 两个字段；正文包含指令、示例与准则。

## 标准与生态

Agent Skills 标准由 Anthropic 在 [agentskills.io](https://agentskills.io) 发布。本仓库即该标准的参考实现与展示，可用于扩展 Claude 的领域能力。

## 许可声明

仓库内示例技能大多为 Apache 2.0；文档创建编辑技能为 source-available，仅作参考。技能行为以实际部署环境为准，使用前应自行测试。

---

来源：<https://github.com/anthropics/skills>