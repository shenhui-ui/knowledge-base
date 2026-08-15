---
type: ingest-note
date: 2026-08-09
sources:
  - https://gitcode.com/openharmony-sig/deveco-cli
  - https://www.infoq.cn/article/deveco-cli-quickstart
source: https://www.infoq.cn/article/eDt24UFt212XlaW83ryM?utm_source=rss&utm_medium=article
---
## DevEco CLI 1.2.0 更新与快速入门

> 来源：[GitCode 项目](https://gitcode.com/openharmony-sig/deveco-cli) 与 [InfoQ / 华为开发者联盟社区](https://www.infoq.cn/article/deveco-cli-quickstart) | 日期：2026-08-07

DevEco CLI 现已开源，项目地址：https://gitcode.com/openharmony-sig/deveco-cli

### 定位

DevEco CLI 定位于统一集成开发工具链和 HarmonyOS 知识库，是专为 AI Agent 打造的原子化能力调度枢纽。它本质上是将 DevEco Studio 工具链统一封装为一个 CLI，内置 ohpm、hvigor、hdc、emulator、hilog，同时集成 HarmonyOS 技能安装、项目脚手架、本地 HarmonyOS 文档检索和 MCP 服务。

### 环境依赖与安装

前置要求：
- 操作系统为 macOS 或 Windows
- Node.js >= 18（推荐 22 及以上）
- DevEco Studio >= 6.1.0
- macOS：必须安装在 ~/Applications 或 /Applications 目录下

安装命令：

```bash
# 稳定版
npm install -g @deveco/deveco-cli@stable

# 尝鲜版
npm install -g @deveco/deveco-cli
```

### 一键集成现有 AI Agent

以 OpenCode 为例，只需运行：

```bash
devecocli init
```

运行该指令后即可完成深度集成。DevEco CLI 能为 AI Agent 专门提供结构化（如 JSON）的数据流，完美兼容 Agent 驱动开发的范式。你的 AI Agent 甚至可以自主指挥 DevEco CLI 去安装更多用于 HarmonyOS 应用开发的精品 Skills。

### 端到端研发原子能力

接入完成后，AI Agent 可自动推进整个研发流程：

- **工程初始化**：调用 `create` 命令，基于官方模板快速生成项目工程结构。
- **编译与构建**：调用 `build` 命令驱动 hvigor 构建系统，自动处理 HAP 打包、多目标产物构建及代码签名。
- **模拟器与运行**：使用 `device` / `emulator` 和 `run` 命令统一管理设备生命周期，自动完成安装、权限配置并启动应用。
- **实时语法检查与编译前错误拦截**：Check MCP 为模型提供实时语法检查和编译修复工具能力，支持 ArkTS 和 C++ 语法检查，无需耗时编译即可实时发现错误，大幅缩短反馈链路，使 Agent 修复效率提升 5 倍以上。

同时 DevEco CLI 内置最新官方知识文档与极速检索。可以引导 AI Agent 在生成代码前先执行查询命令，例如：

```bash
harmonyos knowledge "ArkUI 组件生命周期"
```

确保生成的代码严格遵循官方规范，而非过时信息。

### 内置 70+ 精品 Skills

DevEco CLI 内置 70+ 精品 Skills，沉淀 HarmonyOS 应用开发中的实践经验，覆盖多设备场景适配开发、知识检索、ArkTS 语法、应用质量等关键场景。

以多设备适配 Skills 为例，AI Agent 可结合多设备 Skills 生成更符合设备特性的布局与交互方案，避免简单拉伸、布局错乱等问题，大幅降低多设备适配的人力开发成本。

### 学习资源

- 鸿蒙应用AI辅助研发新范式技术报告（HarmonyOS 白皮书）
- DevEco Code 和 CLI 实践专题
- DevEco CLI 文档
- 课程视频：HarmonyOS 应用 AI 开发工具 -- DevEco CLI

对于拥有既定研发流程的团队来说，DevEco CLI 是将 HarmonyOS 能力接入现有 AI 体系的强有力辅助。

