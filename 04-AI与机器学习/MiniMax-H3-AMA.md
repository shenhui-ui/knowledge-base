---
type: ingest-note
date: 2026-08-09
source: https://www.infoq.cn/article/9C3eK9tJqDXbabbBy3aj
---
type: ingest-note
## Reddit AMA 补充要点（2026-08-08）

> 来源：李冬梅. MiniMax H3 团队 Reddit 被问爆：2K 要开源，图像模型在路上，Apache-2.0 也在考虑了. InfoQ, 2026-08-08. https://www.infoq.cn

MiniMax H3 团队于 8 月 7 日在 Reddit r/StableDiffusion 举行 AMA，首次集中回应了开放权重后的工程落地问题。关键信息如下：

### 2K 输出模型

- 最终 2K 生成所需的 `H3-Regenerate-2K` 会发布，不会太久。
- 它不是传统 upscaler，而是使用专门的 latent-space DiT regeneration checkpoint，将基础模型输出作为额外上下文，并以更高分辨率提供部分参考输入。

### Sparse Attention

- H3 没有沿用 M3 的 MSA，而是采用类似 MoBA-style block selection：对相邻视觉 Token 做 mean pooling 得到 block representation，据此判断重要 block，无需额外训练 learned indexer。
- 目前只对视频 Token 做了三维稀疏化，图片和文本 Token 尚未覆盖，团队正在研究扩展。
- 近期将提供一个保守的 Sparse Attention 参考实现，首要目标是无可感知质量损失，而非极致加速。

### 低步数版本

- 现有 checkpoint 已包含 CFG distillation，具备一定低步数推理能力。
- 团队正在积极考虑 4-NFE / 8-NFE 版本，但暂无承诺日期。
- 社区第三方 Turbo LoRA 已出现，但激进降步会导致运动、结构或音频质量退化。

### 像素化 / 小主体变形问题

- 团队已复现该问题，尤其是远距离小主体。
- 不是单纯 VAE 压缩或单一训练阶段造成，而是系统级问题，涉及模型与训练流程多环节，正在改善。

### 图像模型计划

- 团队正在从 H3 谱系的共同祖先模型派生专门的图像生成模型，并优化后训练阶段。
- 将通过 Weight Slicing 从 H3 的 Causal Temporal Encoder 获得 2D VAE Encoder，并计划设计专门的 VAE Decoder。
- H3 不是 streaming 模型，推荐先由图像模型生成首帧，再交给 H3 的 I2VA 模式生成视频。

### Ref2Vid 清晰度问题

- Ref2Vid 比 I2V 更容易糊，源于两个 checkpoint 的后训练策略不同，团队正在主动改善 Ref2VA 的视觉质量。
- 官方建议：提供尽可能高质量的 reference input。
