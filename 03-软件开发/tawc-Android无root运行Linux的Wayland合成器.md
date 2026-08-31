---
type: ingest-note
source: https://github.com/wmww/tawc
date: 2026-08-02
---

# tawc-Android无root运行Linux的Wayland合成器

`tawc`（Tess's Android Wayland Compositor）是一个在 Android 上无需 root 运行 CLI 和图形 Linux 程序的项目。图形应用通过手机原生图形栈获得硬件加速。项目由 AI 智能体构建，主要使用 Claude Code 和最新 Anthropic 模型。

## 特性

- 嵌入 Termux 的 widget，提供熟悉的终端 UI（不需要安装 Termux 应用本身）
- 安装图形应用后，可从 tawc 的启动器菜单运行
- Linux 应用可添加到手机主屏幕，并与 Android 应用一起出现在应用切换器中
- 包含 XWayland，已为硬件加速 X11 做好接线
- 内置任务管理器，可查看并终止 Linux 进程
- `ando` 命令和存储绑定允许 Linux 程序按需与 Android 数据交互

## 高层设计

- 下载并解压标准 Linux 发行版（如 Arch Linux ARM 或 Debian）作为 rootfs
- 使用 `tawcroot` 在发行版 rootfs 内运行 Linux 程序；它模拟 chroot 和其他系统调用，以克服无 root Android 的限制（与 PRoot 类似，但更快，因为它使用单进程）
- Smithay 为基础的 Wayland 合成器提供 Android 集成（如从 Android 普通键盘传递输入）
- libhybris 允许 glibc Linux 程序加载标准 Android 图形驱动。上游 libhybris 在 stock Android 上不起作用，但本项目 fork 已使其可用

## 限制

- 没有超越 Android 自身机制的真实沙箱；由于单进程设计，tawcroot 可被逃逸
- 不支持桌面 GL，仅支持手机提供的图形 API（通常为 GLES 和 Vulkan）
- 尚未针对游戏进行测试或优化
- 性能优于替代方案，但并非原生
- 官方仅提供 arm64 构建；可为 x86 构建，但 libhybris 技巧依赖 arm
- 需要 Android 10+

## 贡献

- 偏好 issue 而非 PR，欢迎 bug 报告和功能请求，但不保证时间线
- 若 issue 包含 LLM 编写的内容，请明确标记（最好说明由哪个 LLM 编写），并始终包含人工编写的描述
- 请包含应用版本、手机型号、Android 版本和发行版（如相关）

## 许可

- `deps/` 之外的所有代码为 MIT（LICENSE.MIT）
- 由于 vendored 依赖中有 GPLv3 代码（termux-shared 的 extra-keys widget），项目整体为 GPLv3（LICENSE）
- 应用内所有捆绑组件的逐组件归属见 Settings → About → Licenses

## 相关链接

- GitHub 仓库: <https://github.com/wmww/tawc>
