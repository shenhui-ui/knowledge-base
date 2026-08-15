---
type: ingest-note
source: 个人技术博客（Hacker News 趋势文章更新）
date: 2026-08-14
---

# 多GPU本地LLM构建FAQ（更新笔记）

这篇文章于 2026 年 8 月 14 日在 Hacker News 和 Bluesky 上短暂流行。作者针对读者提问给出了详细回答，记录了构建四 GPU 本地推理机的实践经验，并预告了第二章内容。

## 硬件配置

- 机箱：SilverStone RM4A（主要是因为它有 8 个 PCI 卡槽，比通常的 7 个多，可以并排放下 4 张 GPU）
- GPU：4 张，每张协商到 $350（一次买四张的批量价格）
- 主板：Supermicro C9X299-PGF
- CPU：Intel Core i9-10900X
- 电源：EVGA 1600W
- 内存：4×32GB DDR4（不同品牌混插，作者认为有些过度，后续章节会展开）
- 硬盘：Samsung 980 PRO NVMe
- 散热：Asetek AIO CPU 水冷 + Arctic S8038-10K 风扇

## 常见问题解答

### 为什么不用 Ryzen AI Max Halo 或 DGX Spark？
直接用这些设备当然更省事，也能获得 128GB 内存跑模型；但成本大约翻倍，而且无法学到多 GPU 并行知识。更省钱的方式是直接买 Deepseek V4 Flash 的 API 额度，但那又失去了自己构建的意义。

### 需要服务器级主板/CPU/内存才能驱动四卡吗？
系统内存是非 ECC，CPU 是 Core i9 而非 Xeon，主板甚至多处写着“Play Harder”。但另一方面它通过独立以太网口提供 IPMI，而且启动很慢。作者对此的归类比较模糊。

### 穿过车库和起居室之间的防火隔墙跑以太网，是否影响房屋保险？
没有直接剪断防火屏障，而是利用了原有的同轴电缆线盒走线。

## 经验与展望

- ROCm 的实际体验没有想象中那么糟
- 作者正在撰写第二章，但尚未提供 RSS 源
