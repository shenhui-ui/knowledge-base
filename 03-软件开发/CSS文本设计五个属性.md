---
type: ingest-note
source: https://css-tricks.com/5-css-properties-you-should-know-for-better-text-designs/
date: 2026-08-05
---

# 5个CSS文本设计属性

> 原文作者 Preethi Sam，2026年8月5日。本篇为知识库摘录，素材中仅完整包含前四个属性，第五个属性未在素材中展示。

选择正确的字体只是起点，文本的粗细、风格、间距与装饰还能更进一步。下面这些CSS属性可以让文字在网页上更突出、更有趣。

## 1. background-clip

`background-clip: text` 可以用图片或渐变填充文字形状。配合透明文字颜色，即可产生醒目的镂空效果。

```html
<p>Belize Reef</p>
```

```css
p {
  /* `background-clip: text` included in the shorthand */
  background: text url("image.jpg") center/auto 1lh;
  /* transparent text so that the clipped background is visible underneath */
  color: transparent;
}
```

## 2. vertical-align / align-content

水平居中一直很简单（`text-align: center`），但垂直居中的处理则不同。`vertical-align` 用于将行内元素（如 `span`、`img`、`input`）相对文本对齐；而现代布局中的 `align-content` 可以直接在块级盒内垂直排列内容，不需要 flex 或 grid。

```html
31 B <span class="emoji">&#x1F4BA;</span>
```

```css
.emoji {
  vertical-align: top;
}
```

```html
<p>Bonjour</p>
```

```css
p {
  width: 360px;
  aspect-ratio: 1;
  text-align: center;
  /* No grid or flexbox needed anymore */
  align-content: center;
}
```

## 3. box-decoration-mode（实际属性为 box-decoration-break）

当文本折行时，`box-decoration-break: clone` 可以让每个片段（行盒）都完整应用边框、阴影、圆角等装饰，而不是只在整体边缘出现。素材中写作 `box-decoration-mode`，但标准属性名是 `box-decoration-break`。

```html
<span>water cooler chat<br>everyone agrees<br>it is hot</span>
```

```css
span {
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
  /* the edge styles */
  border: solid blue;
  border-width: 0 1px 1px 0;
  box-shadow: 2px 2px 3px rgb(171, 171, 245);
  padding-inline: 6px;
  border-radius: 3px;
}
```

## 4. letter-spacing

`letter-spacing` 控制所有字形的尾部间距，可以取正值或负值，并可用于动画，实现文字揭示效果。

```html
<section id="text">
  <span>Ingvar</span>
  <span>Kamprad</span>
  <span>Elmtaryd</span>
  <span>Agunnaryd</span>
</section>
```

```css
span {
  /* Shrink and hide the letters */
  letter-spacing: -1ch;
  color: transparent;
  /* Keep the first one visible */
  &::first-letter {
    color: #FBDA0C; /* yellow */
  }
}
```

## 5. 第五个属性

原素材在介绍第五个属性前被截断，因此未包含该属性的名称和示例。后续如获取完整原文，可补充此节。
