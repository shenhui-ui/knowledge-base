---
type: ingest-note
source: https://github.com/altic-dev/FluidVoice
date: 2026-08-04
---

# FluidVoice：开源 macOS 语音转文字听写应用

FluidVoice 是一款开源的 macOS 语音转文字听写应用，具备设备端 AI 增强能力。项目采用 GPLv3 许可证，支持通过 Homebrew 安装，目前适用于 macOS，iOS 和 Windows 版本已在开发中。

## 核心特性

- **Fluid Intelligence**：完全本地的 AI 增强层，提供智能格式化、上下文感知大写和后期处理，所有数据在 Mac 上本地运行，无需云服务或 API 密钥。
- **命令模式**：通过语音控制 Mac，包括启动应用、运行快捷指令、触发系统操作以及自动化工作流程。
- **写入模式**：在任何应用中的任意文本框中直接写入或重写文本，支持选中文本重写或内联听写。
- **实时预览**：支持刘海屏的实时转录叠加，边说话边看到文字出现。
- **多种语音模型**：支持 Nemotron Speech 3.5、Parakeet Flash、Parakeet TDT v3/v2、Cohere Transcribe、Apple Speech 和 Whisper，可根据语言和延迟需求选择。
- **AI 增强**：可选通过 OpenAI、Groq、自定义提供商或本地 Fluid Intelligence 进行后期处理，获得更干净准确的转录。
- **音频历史**：可选本地录音历史，带预算控制和 ZIP 导出功能。
- **今日用量统计**：每日使用量一目了然，支持状态栏卡片和工具栏指示器。
- **自适应主题**：跟随系统的浅色/深色主题，并提供紧凑的工具栏切换器。
- **全局热键**：可从任意位置即时开始语音捕获。
- **智能输入**：通过无障碍 API 直接插入任何应用，实现可靠的、与应用无关的文本输入。
- **菜单栏集成**：从菜单栏快速访问、查看状态和设置。
- **自动更新**：无缝更新，可选 beta 通道。

## 安装方式

```bash
brew install --cask fluidvoice
```

也可以从 GitHub 官方发布页手动下载最新版本。

## 版本 1.6.0 亮点

- **Parakeet 重构**：几乎零延迟，说话与文字出现在屏幕上之间基本无等待。
- **Fluid Intelligence**：完全本地的 AI 模型用于设备端听写增强，无云、无 API 密钥、无数据离开 Mac。
- **更好的主题**：自适应浅色/深色主题，带紧凑工具栏切换器。
- **全新入门流程**：语言优先的语音引擎设置、真实听写试用和 AI 增强设置一次完成。

## 开源与商业化说明

FluidVoice 在 GPLv3 下完全开源。Fluid Intelligence 是一个独立的、私人维护的本地 AI 运行时，为高级设备端听写增强提供支持。应用本身可在任何受支持的语音模型和可选的云 AI 提供商下正常工作；Fluid Intelligence 则为需要完全本地、私有 AI 层的用户提供增强。目前 Fluid Intelligence 保持私有，以便可持续地免费提供核心听写体验，未来可能改变。

## 支持与反馈

项目鼓励用户 star 仓库以提升可见度，并支持持续开发和未来 iOS、Windows 平台工作，可通过 GitHub Sponsors 赞助。
