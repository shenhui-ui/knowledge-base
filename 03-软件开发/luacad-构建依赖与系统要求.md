---
type: ingest-note
source: luacad 项目文档（未提供 URL）
date: 2026-08-01
---

# luacad 构建依赖与系统要求

`luacad` 及其配套 `luacad-studio` 在构建时需要本地 C/C++ 工具链，因为两者都将 C/C++ 依赖以 vendor 方式纳入项目内部，因此无需预先安装相关系统库。但构建过程仍然需要：

- C++ 编译器
- CMake

其中：
- `luacad` 会构建 **Manifold** 与 **Clipper2**
- `luacad-studio` 额外构建 **OpenCSG**，这需要 OpenGL 开发头文件

在 Debian/Ubuntu 上可安装：

```bash
sudo apt install libgl1-mesa-dev libx11-dev libxcb1-dev libxkbcommon-dev libxrandr-dev libwayland-dev
```
