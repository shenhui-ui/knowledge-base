# 自生长知识库（Knowledge Base）

> 基于 **Karpathy LLM Wiki 方法论** 的个人知识库：**素材收件箱 → LLM 提炼 → 结构化 Wiki 文章 → 自然语言检索 → 一致性体检**，内置每日自动化的科技资讯管线与 LLM 成本记账。

**规模**：176 篇 Wiki 文章 · 25 个 Python 模块 · 11 个 pytest 测试文件 · 9 个分区 · 每日 01:00 自动运行

## 这套系统解决什么问题

个人知识管理的典型痛点：素材收集了但**进得去出不来**——没有主题化沉淀、无法检索、越堆越乱。Karpathy LLM Wiki 方法论的要点是：**把知识库当 Wiki 管理，用主题分区 + 索引驱动**，让 LLM 承担"提炼、归类、体检"的重复劳动，人只负责提供素材和做判断。本仓库是该方法论的**完整落地实现**：

- 素材先进入 `00-收件箱/`，管线按规则**筛选**（丢弃重复/广告/无实质内容）后**沉淀**为结构化 Wiki 文章（含 source 链接、date、frontmatter）
- 所有文章登记在索引中（按 Unicode 码点排序），`query` 通过索引命中文章并引用具体链接合成回答
- `lint` 对知识库做一致性体检：索引缺失、孤立页面、失效链接、矛盾内容等

## 目录结构

```
├── Obsidian/                          # Obsidian 库（Claudian / Dataview / Templater 插件）
│   ├── AGENTS.md                      # 知识库管理员规则书：对话命令 + 读写安全边界 + YAML 规则
│   ├── 00-收件箱/                     # 素材区（@manual 后缀 = 人工处理）
│   ├── 01-日记/                       # 每日笔记
│   ├── 02-资讯日报/                   # 自动化管线专用写区（日报 / 周报）
│   ├── 03-软件开发/                   # Wiki 主题区（92 篇）
│   ├── 04-AI与机器学习/               # Wiki 主题区（59 篇）
│   ├── 05-数据分析/                   # Wiki 主题区（6 篇）
│   ├── 06-项目/                       # 项目区
│   ├── 07-模板与系统/                 # 规则、隐藏模板(.模板)、索引与日志(MOC/)、管线脚本(脚本/)
│   └── 99-归档/                       # 归档区
└── docs/superpowers/                  # 3 份设计文档（plans + specs，Superpowers 方法论）
```

## 核心机制

### 1. AGENTS.md —— 知识库管理员规则书
- **对话命令**：`ingest`（素材 → 索引定位 → 合并/新建文章 → 记日志）、`query`（索引命中 → 合成回答带链接）、`lint`（检查 + 可自动修复的直接修）
- **安全边界**：可写 / 只读 / 禁入三级白名单（AI 永不触碰 `.obsidian/`、`.模板/`、`脚本/`）
- **YAML 规则块**：`screen_rules`（取舍：重复丢弃/广告丢弃/高价值沉淀）+ `digest_rules`（归类：合并或新建、source 必须为原文链接、target 必须位于白名单目录）

### 2. 科技资讯管线 `tech_news/`（每日 01:00 systemd timer 触发）
```
sources.yaml（可编辑源清单）→ fetch → dedupe（.raw/urls.txt）→ 黑名单过滤
→ LLM 自动主题分类（不设固定清单）→ render → 02-资讯日报/日报/YYYY-MM/科技资讯 YYYY-MM-DD.md
```
- 信息源：Hacker News、Ars Technica、The Verge、少数派、36氪、InfoQ 中文、机器之心（公开 RSS，源列表 YAML 配置可改）
- 支持 `--backfill` 历史回溯；日志写 `.raw/pipeline.log`

### 3. wiki 写入引擎 `tech_wiki/`
`ai.py`（LLM 调用）/ `fetch.py` / `ingest.py` / `lint.py`（索引一致性、链接有效性、Unicode 顺序等）/ `rules.py`（规则加载）

### 4. 可靠性设计
- `check_daily_report.py`：01:00 健康检查昨日日报是否生成，缺失即退出码 1 告警
- JSON 解析失败自动重试；LLM 成本记账（含缓存命中统计），运行成本透明可审计
- 11 个 pytest 测试文件（`tmp_path` / `capsys` / `monkeypatch` 夹具，无外部网络依赖）

## 运行

```bash
cd Obsidian/07-模板与系统/脚本/tech_news

python3 pipeline.py          # 当日日更
python3 pipeline.py --backfill   # 历史回溯（如 2026-08-01 ~ 08-08）

# 测试（脚本目录下，测试文件自带路径处理）
pytest
```

## 设计文档

`docs/superpowers/`：3 份按 **Superpowers 方法论**（先规划后实现）沉淀的设计稿——自生长 Wiki 设计、Obsidian 知识库设计、科技资讯管线设计（含信息源选型与系统 Prompt 稳定性策略）。

## 关联项目

- **obsidian-skill-wiki-manager**：本系统方法论的产品化 skill——`init / ingest / query / lint` 四能力 + 万字教程，可安装到任意本地 Markdown 知识库
