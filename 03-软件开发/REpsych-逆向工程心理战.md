---
type: ingest-note
date: 2025-08-03
source: https://github.com/xoreaxeaxeax/REpsych
---

# REpsych：逆向工程心理战

## 概述
REpsych 是 Christopher Domas（@xoreaxeaxeax）发布的概念验证工具集，用于演示如何通过程序的控制流图（CFG）生成图像。每个源图像像素会转换为一个基本块（CFG 节点），最终生成两个可运行程序：`repsych_v1` 和 `repsych_v2`，分别采用不同策略确保 CFG 渲染器正确定位节点。

该工具可让 IDA Pro 等逆向工程工具将目标图片显示在 CFG 视图中，从而对逆向分析人员造成心理干扰。项目本身是一个“为了证明可以做到”的 PoC，实际应用场景在 DEF CON 演讲中有所描述。

## 使用方法
1. 将图片保存到 `gfx/` 目录，格式为 24 BPP 位图（建议尺寸不超过 100×100）。
2. 在项目根目录执行 `make image`（`image` 为不含扩展名的文件名）。
3. 生成两个程序 `repsych_v1` 和 `repsych_v2`，用 IDA Pro 或其他 CFG 查看器打开即可看到目标图像。

## 注意事项
- 每个像素生成一个 CFG 节点，图片过大会导致节点数超限，需在 CFG 查看器中调大允许节点数量。
- 若输入为文字图像，先转换为 2 BPP 黑白位图，再转成 24 BPP 位图，可获得最佳效果。

## 兼容性
程序在 IDA Pro 各版本上测试可靠，对 Hopper、BinNavi、radare2 等 CFG 查看器半可靠。

## 参考
- 项目地址：https://github.com/xoreaxeaxeax/REpsych
- DEF CON 演讲幻灯片位于仓库 `slides/` 目录
