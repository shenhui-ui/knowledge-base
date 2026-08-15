---
type: ingest-note
source: Why Tiny JPEGs Look Different in Chrome（原文标题，链接未提供）
date: 2026-08-03
---

# Why Tiny JPEGs Look Different in Chrome

## 现象
在 Chrome 与 Firefox 中渲染同一张小型 JPEG 图片时，Chrome 渲染结果看起来更“粗”。原作者最初以为是渲染 bug，但实际是 Chrome 对 JPEG 解码的优化。

## 原因
Chrome 的图像解码由 Skia 完成，Skia 对 JPEG 使用 libjpeg-turbo，其中实现了 **partial IDCT scaling**（部分 IDCT 缩放）。当目标显示尺寸较小时，Chrome 不会先把完整 JPEG 解压成位图再缩小，而是只解码低频率分量，直接得到缩略效果。

## 原理
- JPEG 压缩时将图像切成 8×8 块，通过 DCT（离散余弦变换）转换到频域。
- 8×8 块中最低频是纯色（常数分量），最高频是类似棋盘格的模式。
- 大幅缩小时，高频细节（如树叶、纹理）会自然丢失，因此只需低频系数即可近似表示目标尺寸的图像。
- 该优化适用于分母为 8 的缩放比例（如 1/8、2/8 等）。

例如，2000×2000 的 JPEG 显示为 20×20 时，完整解压需要约 12 MB 位图，而最终 20×20 图像仅需约 1.2 KB，大部分信息在缩放过程中被舍弃。

## 补充
这种解码优化不仅用于缩小，也可以扩展到放大场景。Chrome 与 Firefox 的视觉差异并不是渲染错误，而是不同解码路径对高频信息取舍的结果。

更多信息可以参考 [jpegclub.org](http://jpegclub.org) 上关于 partial IDCT scaling 的介绍。