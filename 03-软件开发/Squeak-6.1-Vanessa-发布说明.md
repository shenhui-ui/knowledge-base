---
type: ingest-note
source: https://squeak.org/
date: 2025
title: Squeak 6.1 "Vanessa" 发布说明
tags: [Squeak, Smalltalk, 发布说明]
---

# Squeak 6.1 "Vanessa" 发布说明

Squeak 6.1 是接近 Squeak 30 周年之际发布的重要版本，自上一版本（4 年前）以来合并了 1700+ 补丁，9000+ 方法变更。此版本为纪念 Vanessa Freudenberg（1972-2025）命名。

## 主要亮点

- **新树浏览器**：通过翻新的层次化 Morph 在类与分类中导航。
- **Objectland 回归**：也被称为 "Worlds of Squeak"。
- **内核基础设施修复**：包括模拟、展开、调度进程和重塑类的修复与变更。
- **工具集与 UI 改进**：检查、调试、剖析和版本控制代码的改进。

## GUI 框架（Morphic）

- 树 morph 的重大改版：改进颜色、鼠标与键盘快捷键；类型过滤；搜索高亮；递归查找；拖放时自动扩展节点。
- 支持将类引用、系统和方法分类、检查器/资源管理器字段拖放到新窗口。
- 添加窗口折叠菜单项，改进 "find workspace"。
- 文本编辑器改进：链接悬停下划线，嵌套引号自动转义/取消转义。
- Morphic API：允许 morph 选择退出单个 halo 事件，balloon 文本可通过块指定。
- 大量 UI 稳定性、主题、高 DPI、多语言支持改进。

## 兼容性与已知问题

- 包含重大弃用说明，详见完整发布说明。

（注：此为基于发布说明的摘要，完整内容请参阅 [Squeak 官网](https://squeak.org/) 或系统内交互式发布说明。）
