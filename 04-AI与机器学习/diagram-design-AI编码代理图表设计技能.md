---
type: ingest-note
source: https://github.com/cathrynlavery/diagram-design
date: 2026-08-06
---

# diagram-design：面向AI编码代理的编辑级图表设计技能

[diagram-design](https://github.com/cathrynlavery/diagram-design) 是一个专为 Claude Code、Codex 和 Pi 等 AI 编码代理设计的图表生成技能，旨在产出“设计师不会讨厌的编辑级图表”。它由 [littlemight.com](https://littlemight.com) 的作者 Cathryn Lavery 构建，可快速匹配品牌风格，避免通用圆角矩形和繁琐的颜色调整。

## 核心特性

- **27 种视觉类型**：覆盖架构图、流程图、时序图、状态机、ER 图、时间线、泳道图、象限图、嵌套图、树图、组织架构图、维恩图、分层栈、金字塔/漏斗图、2×2 咨询矩阵、雷达图、循环飞轮、IT 现状图、端到端堆栈、柱状图、折线图、甘特图、散点图、过程图、Medallion 数据层、数据流、DP 集成、DP 安全矩阵等。
- **三种静态变体**：每种视觉类型均提供极简浅色、极简深色和全编辑风格三种静态 HTML 输出，可直接在浏览器中打开，无需构建步骤、JavaScript 或外部图片依赖。
- **语义化模式**（2.3 新增）：将行为与布局分离，允许队列、策略追踪或信任边界复用现有类型，不增加类型数量。
- **可选动效**（2.3 新增）：默认为静态输出，可为有序解释开启可选的无障碍动效。
- **重绘能力**：可对 draw.io 或 Mermaid 源图按指定格式、尺寸和细节级别进行重绘。
- **Loop**（2.0 新增）：支持共享内存中心的飞轮图，虚线表示写回。

## 设计哲学

- 最高质量的图表往往来自删除：每个节点都应赢得自己的位置。
- 强调色仅保留给读者应首先关注的 1–2 个元素。
- 目标信息密度为 4/10（适中有留白）。

## 安装与使用

### Claude Code

```
/plugin marketplace add cathrynlavery/diagram-design
/plugin install diagram-design@diagram-design
```

安装后，建议在插件市场设置中启用自动更新（Claude Code 默认禁用第三方市场的自动更新），并按提示 `/reload-plugins` 或等待下次会话加载更新。

### Codex

```
codex plugin marketplace add cathrynlavery/diagram-design
codex plugin add diagram-design@diagram-design
```

Codex 会在启动时刷新已配置的 Git 市场；如需立即获取更新，可运行 `codex plugin marketplace upgrade diagram-design` 并开启新会话。

### Claude Cowork（组织市场）

组织 GitHub 市场需要私有或内部仓库，因此需先将此公开仓库镜像到组织名下，然后在组织设置 → 插件中添加 GitHub 插件并配置自动同步。

## 在线画廊

可在 [cathrynlavery.github.io/diagram-design](https://cathrynlavery.github.io/diagram-design) 浏览全部 27 种图表，或本地打开 `skills/diagram-design/assets/index.html` 在浅色/深色/全编辑标签间切换查看。

---

**来源**：[GitHub - cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design)