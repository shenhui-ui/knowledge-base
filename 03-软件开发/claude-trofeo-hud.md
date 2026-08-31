---
type: ingest-note
date: 2026-08-15
source: https://github.com/christensen143/claude-trofeo-hud
---

# claude-trofeo-hud：macOS 驱动的 Claude 使用量桌面 HUD

一个开源项目，将 Claude 的实时使用统计显示在 Thermalright Trofeo Vision 6.86" LCD（1280×480，USB-C，约 $38）上，灵感来自 r/ClaudeAI 的热帖。HUD 运行在 macOS 上，通过 USB 驱动这块非显示器的 HID 设备。

## 功能

- 显示 Pro/Max 会话和每周限制条，及重置倒计时（来自 Anthropic usage 接口）
- 显示今日 token 消耗与假设的 API 成本（基于 `ccusage`）
- 实时会话信息（项目、模型、烧钱速率）
- 时钟与每小时 token 迷你走势图

## 技术方案

- **语言/环境**：Python 3.12+、uv、Node（用于 `npx ccusage`），还需通过 `brew install hidapi` 安装 C 库（hidapi Python 包的后端）
- **HID 通信**：设备 VID:PID `0416:5302`，接受 JPEG 帧；使用 `thermalright-trcc-linux` 的 `HidApiTransport`（IOHIDManager），而非 libusb（macOS 会阻止 HID 设备的 libusb 访问）
- **数据来源**：读取 Claude Code 本地日志和 Keychain 中的 OAuth token（只读，仅向 api.anthropic.com 发送用量查询），并调用 usage 端点
- **显示策略**：面板空闲时会休眠，因此 HUD 以 2 fps 持续传输帧
- **开机自启**：支持通过 launchd 安装 agent，并自动处理拔插重连

## 安装与配置

```bash
uv sync
uv run python -m claude_trofeo_hud preview   # 渲染 mock 布局到 out/preview.png
uv run python -m claude_trofeo_hud run      # 在 LCD 上运行
uv run python -m claude_trofeo_hud install-agent  # 设置登录自启
uv run python -m claude_trofeo_hud uninstall-agent # 停止并移除 launchd agent
```

首次运行时需在 macOS 中授权 Keychain 访问 "Claude Code-credentials"。配置文件为 `config.toml`（帧率、JPEG 质量、夜间调暗/关闭），日志位于 `~/Library/Logs/claude-trofeo-hud/`。

## 注意事项

- 权限错误通常意味着有其他程序通过 libusb 打开了设备，需确保使用本项目 CLI 而非 trcc 原始命令
- 面板不亮或无帧时检查 `hud.log`
- 成本/token 为空时，需先确保 `npx ccusage` 在终端可用，Node 升级后需重新运行 `install-agent` 以更新 plist 中的路径
- 限制数据陈旧可能是 Keychain 授权未授予或 Claude Code 未登录

此项目展示了如何逆向非标准 USB 显示器协议并集成 Claude 生态，为本地 AI 使用监控提供了可扩展的 HUD 参考实现。
