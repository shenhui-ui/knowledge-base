---
type: ingest-note
date: 2026-08-01
source: https://github.com/carpdiem/ember
---

# Ember：夜览/红移安全颜色调色板

## 概述

Ember 是一个开源颜色调色板项目，旨在解决传统调色板在开启 Nightshift / Redshift 等暖色屏幕滤镜后颜色难以区分的问题。它提供了在多种色温过滤下仍保持可辨识度的终端、图表、热力图和 UI 配色方案，并导出了 Alacritty、iTerm2、Windows Terminal、Matplotlib、CSS 等多种格式。

## 核心设计原则

- **首要目标**：在暖色滤镜下保持颜色可区分。
- **次要优化**：在不启用滤镜的白天场景下，进一步调整人眼感知退化的色通道以增强对比。
- 暖色滤镜并非简单的色调叠加，而是对 R/G/B 通道乘以不同增益；在 1200K 极端模型下蓝色增益为零，因此仅靠蓝色区分的颜色会完全混淆。
- 更深的滤镜会显著缩小可感知颜色空间，因此深色配置文件刻意减少“颜色身份”数量，而不是让别名颜色假装是不同颜色。

## 四个调色板

| 调色板 | 适用场景 | 可区分类别数 |
| --- | --- | --- |
| 3400K Dark | 近黑底色的通用暖色主题 | 6 |
| 3400K Light | 浅色表面上的中等暖色偏移 | 6 |
| 2000K Dark | Redshift 接近 2000K 时 | 4 |
| 1200K Dark | 极端 1200K 压力测试 | 3 |

- 推荐默认使用 **3400K Dark**，除非你刻意使用更深的滤镜。
- 2000K 和 1200K 仅提供暗色版本，因为过滤后的浅色画布会变成大面积橙红色区域。

## 导出格式与可用性

每个调色板均以 commanded sRGB 编写，并在对应色温的每通道 RGB 增益模型下验证，导出为：

- 终端主题（Alacritty、iTerm2、Windows Terminal）
- UI 角色色板
- 分类图表颜色
- 256 级顺序色带（sequential map）
- Matplotlib、CSS、JSON、Python 工件

## 快速使用

### 获取文件

```bash
git clone https://github.com/carpdiem/ember.git
cd ember
```

Python 用户可直接从 GitHub 安装：

```bash
python -m pip install "ember-palettes @ git+https://github.com/carpdiem/ember.git"
```

### 导入终端主题（Alacritty 示例）

```bash
mkdir -p ~/.config/alacritty/themes
cp themes/terminal/alacritty/2000k-dark.toml ~/.config/alacritty/themes/
```

然后在 `alacritty.toml` 中导入：

```toml
[general]
import = [ "~/.config/alacritty/themes/2000k-dark.toml" ]
```

iTerm2：打开 Settings → Profiles → Colors → Color Presets… 导入对应主题文件。

## 注意事项

- Ember 本身不应用暖色滤镜，仍需使用你已有的夜览/红移工具。
- 过滤后的行是确定性信号模拟（commanded sRGB × 各配置文件的增益），不是真实照片或物理色温预测。
- 评判滤色效果前请先关闭屏幕上的暖色滤镜，避免双重变换。

## 参考

- 仓库：<https://github.com/carpdiem/ember>
