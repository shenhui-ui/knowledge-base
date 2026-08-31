---
type: ingest-note
source: 未标注来源（项目文件树）
date: 2026-07-31
---

# QR Submission 项目工作目录结构

该素材来自一个 QR 码提交项目的工作目录，包含大量提交变体、Modal B200 探测脚本、源码树、文档与提交日志，推测为 AI 辅助迭代优化的竞赛或研究项目。

```text
qr/
├── submission.py                 # the live entry
├── submission_*.py (560)         # named submission variants (crystal_rain, blue_reply, …)
├── modal_b200_*.py (119)         # Modal B200 probe / compare scripts
│   ├── AGENTS.md                 # top-level notes / logs
│   ├── attempts_log.md
│   ├── claude_ideas.md
│   ├── leaps.md
│   └── problem_statement.md
├── docs/ (68)                    # per-experiment writeups & status docs
├── code/                         # the actual QR kernel source tree
├── scripts/                      # summarizers, timing, submit helpers
├── archive/                      # cleaned-out old submissions & probes
│   ├── submissions_20260616_17/
│   ├── submissions_20260618_20/
│   ├── probe_scripts_cleanup_20260627/
│   └── …
├── submit_logs/                  # logs provided by the evaluator for each submission
└── profile.*/                    # captured NCU profile runs
```
