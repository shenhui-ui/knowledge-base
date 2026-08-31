---
type: ingest-note
source: Temani Afif（原文标题：Something Nobody Told You About The Image Element (It Can Overflow!)）
date: 2026-08-03
---

# CSS图像元素溢出与object-fit的隐藏行为

`<img>` 是最常用的 HTML 元素之一，但它的 CSS 行为却隐藏着一些不为人知的细节。本文来自 Temani Afif 的分享，揭示了图像元素如何同时作为“容器”和“内容”，以及它为何可以溢出自身。

## 图像元素的双重身份

`<img>` 元素本身是一个“容器”，而它加载的图像资源才是“内容”。这就像普通元素的容器-内容关系，因此也可以讨论溢出。图片元素实际上是一个“替换元素”（replaced element），这意味着它的内容和元素框可以分别控制。

但默认情况下，浏览器会为图像应用 `overflow: clip`，所以任何溢出都会被裁剪。不过我们可以将其改为 `overflow: visible`，从而让图像内容溢出到元素边界之外。

```css
img {
  overflow: visible;
}
```

## 哪些属性会让图像溢出？

### `object-fit: cover`

`object-fit: cover` 会保持图像固有比例并填充容器，通常意味着图像的部分内容会被裁剪。当图像内容比容器大时，它就产生了溢出。默认裁剪，但可以改成 `overflow: visible` 显示溢出。

### `border-radius`

圆角边框也会让图像内容溢出圆角区域，因为矩形图像被裁切成圆角形状，但内容默认仍然覆盖矩形区域。

### `object-position`

```css
img {
  object-position: 50px 0;
}
```

该声明会将图像内容向左平移 50px，但不影响元素框本身，因此会产生溢出。这个特性之后可以用在创意演示中。

## `object-fit: none` 的奇怪行为

`object-fit` 除了常见的 `cover` 和 `contain`，还有一个易被忽略的值 `none`。根据规范，`none` 表示替换内容不被调整大小以适应元素的内容框。也就是说，图像资源始终保持其固有尺寸，无论元素尺寸如何变化。

```css
img {
  width: 80vw;
  height: 80vh;
  object-fit: none;
}
```

这段代码会让元素大小随视口变化，但图像内容始终为原始尺寸（如 300×300），当元素小于内容时就会发生溢出。

## 默认值 `fill` 与 `none` 相反

`object-fit` 的默认值是 `fill`，效果与 `none` 完全相反：无论图像资源固有尺寸多大，它都会调整大小以填满元素的内容框。

## 结论

图像元素远不止是一个简单展示图片的标签，它同时是容器和内容，并且这两个尺寸可以分别控制。理解这种双重身份，有助于掌握 `object-fit`、`overflow` 等属性的行为，也能解释为何图像有时会意外溢出。
