---
name: wiki-manager
label: 知识库管家
description: 当需要建立/维护基于 Karpathy LLM Wiki 方法论的本地 Markdown 知识库时使用。触发场景："建一个 wiki/知识库"、"把这段内容沉淀到 wiki"、"我的 wiki 里关于 X 的文章在哪"、"检查我的知识库有什么问题"、"按 AGENTS.md 规则操作"。解决：从零搭建目录骨架、把收件箱素材沉淀为 wiki 文章、按自然语言问题检索已有文章、检查索引/链接/Unicode 顺序一致性。所有文件操作必须用 Python（避免 shell for 循环切分含空格/中文文件名）。
---

# 知识库管家（wiki-manager）

按 AGENTS.md 规则管理个人 wiki 知识库的完整生命周期。提供 init / ingest / query / lint 四个核心操作，每个操作都有对应的 Python 脚本（`scripts/`）。

## 快速开始

```bash
# 1. 初始化知识库骨架（一次性）
python3 scripts/init.py --wiki /path/to/your/wiki

# 2. 把素材放到 00-收件箱/，文件名加 @manual 后缀
cp my_material.md /path/to/wiki/00-收件箱/RAG\ 检索增强生成\ @manual.md

# 3. 写 wiki 文章到可写区（03/04/05/06），按 assets/article_template.md 模板

# 4. 同步更新索引（Unicode 字母序插入 [[文章名]]）

# 5. 跑 lint 检查
python3 scripts/lint.py --wiki /path/to/your/wiki

# 6. 检索
python3 scripts/query.py "RAG 是什么" --wiki /path/to/your/wiki
```

## 核心工作流

### init（一次性）
建立 9 个分区目录 + `MOC/索引.md` + `MOC/操作日志.md`。已存在则跳过。

### ingest（素材沉淀）
1. 素材放 `00-收件箱/<name> @manual.md`（手动处理用 @manual 后缀）
2. 读 `MOC/索引.md` 查重
3. 筛选：重复/广告/无内容 → 丢弃；高价值/新主题 → 沉淀
4. 写 wiki 到可写区（03/04/05/06），frontmatter 含 `type: ingest-note` + `source` + `date` + `tags`
5. 索引按 Unicode 字母序插入 `[[文章名]]`
6. 归档素材到 `99-归档/`
7. 追加操作日志

### query（检索）
三层匹配：① 子串（文章名 ⊂ query）→ ② 关键词匹配标题 → ③ 非泛词搜索正文
泛词黑名单：`模型/架构/预训练/编程/生成/图像/模板/部署/处理/是什么/怎么用/如何/进展/区别/应用/方法/特点/作用/影响`

### lint（六项检查）
1. 索引 vs 实际文章
2. 主题区分布
3. 链接目标存在性
4. 双向链接对称性
5. 索引 Unicode 顺序
6. 收件箱/归档状态

`--fix` 自动修：索引补漏/移除失效条目。

## 关键约束

| 约束 | 说明 |
|------|------|
| **必须用 Python** | 任何 lint/query/ingest 操作**不得**用 shell `for x in $(...)`，会按 IFS 切分含空格/中文文件名。Python pathlib 才能正确处理。 |
| **可写区** | 03-软件开发 / 04-AI与机器学习 / 05-数据分析 / 06-项目 + MOC/索引.md + MOC/操作日志.md |
| **只读区** | 00-收件箱 / 02-资讯日报 / 07-模板与系统/附件/ |
| **禁入区** | 07-模板与系统/.模板/ / .obsidian/ / 脚本/ |
| **写入前确认** | 修改已有 wiki 文件前先向用户确认（init/ingest 全链路验证场景除外） |
| **意向性单向** | 「需判断的（孤立页、矛盾）」按 AGENTS.md 报告而非自动修（如「知识库搭建项目 → RAG」保留单向） |

## 资源

- `scripts/init.py` — 初始化知识库骨架
- `scripts/lint.py` — 六项一致性检查 + 自动修复
- `scripts/query.py` — 三层匹配检索
- `references/rules.md` — AGENTS.md 精简版（目录语义 / 命令 / 安全边界 / 命名格式 / lint_rules）
- `assets/article_template.md` — wiki 文章 frontmatter 与正文模板
- `assets/source_material_template.md` — 收件箱素材模板

## 已知坑

- **shell 切分**：含空格文件名（如 "Pandas 数据处理"）在 shell `for x in $(...)` 里会被切成多段。永远用 Python。
- **泛词误报**：query 中"模型/架构/预训练"等词太泛，会触发正文误命中。用泛词黑名单 + 标题优先避免。
- **中文名 Unicode 序**：中文（如"知识库" U+77E5）远大于 ASCII 字母，排在大写 ASCII 之后、其它中文之前需按 codepoint 而非拼音。
- **索引条目假阳性**：`MOC/索引.md` 注释里的 `[[文章名]]` 文档示例会被正则误抓为条目，解析时需排除。
