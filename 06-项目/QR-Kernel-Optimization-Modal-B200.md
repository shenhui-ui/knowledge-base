---
type: ingest-note
source: "qr/"
date: 2026-08-01
---

# QR Kernel Optimization on Modal B200

该项目位于 `qr/` 目录，是一个在 Modal B200 上进行的 QR 内核优化项目。

目录结构包含：
- `submission.py`：实时提交入口
- `submission_*.py`：560个命名提交变体
- `modal_b200_*.py`：119个Modal B200探针/对比脚本
- `AGENTS.md`：顶层笔记/日志
- `attempts_log.md`, `claude_ideas.md`, `leaps.md`, `problem_statement.md`
- `docs/`：68个实验文档
- `code/`：QR内核源码树
- `scripts/`：摘要、计时、提交辅助脚本
- `archive/`：旧提交与探针归档
- `submit_logs/`：评估器提供的提交日志
- `profile.*/`：NCU性能分析运行

该项目通过大量命名变体和系统化实验，对QR内核进行性能优化。