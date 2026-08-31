---
type: ingest-note
date: 2026-08-13
source: https://arxiv.org/abs/2608.12700
---

# Contract-Grade Verifier for LLM-Generated GPU Kernels

## 概述

该论文（arXiv:2608.12700）针对当前 LLM 生成 GPU kernel 系统的高正确率声称提出质疑。现有系统通常只用单一宽松测试（固定 shape、少数随机输入、输出与参考接近即通过）来验收 kernel，但这种测试无法捕捉静默错误，例如：在结果本应为 NaN/Inf 时返回普通数值、运行时产生不确定结果、shape 变化后失效、或 fp16 累加而参考实现保持 fp32 等。

## 核心贡献

- **Contract-grade verifier**：构建一个包含 12 个对抗性检查门（adversarial gates）的验证器，每个门对应正确 kernel 必须满足的性质，其中多个门是免容差（tolerance-free）的，无法通过调整阈值来掩盖失败。

- **外部审计结果**：对一个公开系统自家 harness 已接受为正确的 2,638 个机器生成 kernel 进行审计，发现：
  - 39.5% 的 kernel 在任何容差论证下都是坏的；
  - 62.1% 的 kernel 至少违反一个性质；
  - 该领域标准测试会接受 1,487 个被验证器拒绝的 kernel，而反向误判仅 14 个。

- **验证方法的多重辩护**：
  - 7/7 阳性对照（positive control）
  - 阈值校准扫描（threshold-calibration sweep）
  - 与参考 benchmark 自身正确性代码的 98.5% 一致
  - 分层人工审计（stratified hand-audit）

- **内部应用**：验证器用于评估作者自己的 kernel——第一个原生 Blackwell tcgen05 训练反向传播实现，覆盖 gated-linear-recurrence（GDN）家族，包括此前仍需回退（fallback）的反向状态阶段。通过双精度 oracle 验证正确性，并对五个家族成员完成了训练。

## 结论

论文指出：kernel 生成领域所报告的正确率信号远弱于表面数字所示；一组免容差的合同（contracts）将能弥合大部分差距。

## 链接

- arXiv: https://arxiv.org/abs/2608.12700
- DOI（pending registration）: https://doi.org/10.48550/arXiv.2608.12700
