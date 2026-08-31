---
type: ingest-note
source: https://www.infoq.com/news/2026/08/uno-platform-6-6/
date: 2026-08-14
---

# Uno Platform 6.6 发布：Android 启动性能最高提升 61%

Uno Platform 6.6 在五个目标平台上引入了原生 AOT 发布、可选的 Vulkan 渲染后端，以及框架模型上下文协议（MCP）服务器的自动注册功能。该版本还减少了 XAML 样板代码，扩大了 WinUI API 的跨平台覆盖范围，并改进了无障碍支持和多语言文本处理。

## 主要更新

- **原生 AOT 支持**：为 Android、iOS、Linux、macOS 和 Windows 提供原生 AOT 支持，提前编译应用程序代码，减少启动时 JIT 编译开销。使用 .NET 10 上的 Chefs 示例应用测试，启动性能提升幅度从 iOS 的 21% 到 Android 的 61% 不等，具体取决于应用结构、硬件和部署配置。基于 JIT 的发布方式仍然受支持。

- **可选 Vulkan 渲染后端**：在 Windows、Linux 和 Android 上引入可选择启用的 Vulkan 后端。OpenGL 仍是这些平台上默认的 Skia 后端，Apple 目标平台继续使用 Metal，WebAssembly 使用 WebGL。某些测试中 Vulkan 将每帧渲染成本降低多达 50%，适合动画丰富或图形密集型应用。

- **XAML 编写简化**：隐式提供标准 WinUI 表示命名空间和 `x:` 命名空间；开发者可在 `GlobalNamespaces.xaml` 文件中集中定义共享命名空间。声明 `x:Class` 的页面可自动获得生成的代码隐藏类，允许仅包含 XAML 的页面存在，而无需再提供空的 `.xaml.cs` 文件。

- **AI 辅助工作流增强**：Uno 的 App MCP 和 Docs MCP 服务器现在可向受支持的开发智能体自动注册。App MCP 向智能体开放正在运行的应用程序，以便检查和交互；Docs MCP 提供对最新 Uno 文档的访问。支持自动注册的工具包括 Visual Studio 和 VS Code Copilot、Claude Code、Cursor、Codex CLI 以及 Gemini CLI，但并非所有智能体都支持。

- **无障碍与文本处理改进**：通过 Skia 渲染的应用获得更广泛的无障碍支持，屏幕阅读器现在可访问 Windows、macOS 和 WebAssembly 上的 Uno 界面；Android 和 iOS 支持仍在开发中，Linux 支持已列入计划。所有主要目标平台上提供完整的输入法编辑器组合输入功能，支持需要多次击键的亚洲语言，并为多书写系统界面引入自动字体回退。

- **API 兼容范围扩大**：通过投影、几何变换、文本突出显示、拼写检查、浮出控件、剪贴板操作、拖放以及 WebView2 等 API 扩大 WinUI 兼容范围。新增动态 WebP 播放，以及 macOS 上的 Mica 和 Acrylic 窗口背景。支持程度因目标平台而异。

## 升级注意事项

- SkiaSharp 4.x 可作选择启用的依赖项，但 Uno 6.6 默认仍使用 SkiaSharp 3.x。
- 升级现有应用需更新 `global.json` 中的 Uno SDK 条目，并查阅迁移指南了解项目特定变更。

更多详细信息、基准测试、设置说明和 API 覆盖说明，请参阅 [Uno Platform 公告](https://platform.uno/blog/) 、 [GitHub 发布说明](https://github.com/unoplatform/uno/releases) 和 [文档](https://platform.uno/docs/) 。

原文链接：https://www.infoq.com/news/2026/08/uno-platform-6-6/
