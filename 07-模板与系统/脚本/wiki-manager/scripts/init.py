#!/usr/bin/env python3
"""
知识库 init 工具 — 按 AGENTS.md「目录语义」一次性建好骨架。

用法：
    python3 init.py --wiki /path/to/wiki
"""
import argparse
from datetime import date
from pathlib import Path

# 目录语义
DIRECTORIES = [
    ('00-收件箱', '素材区（只读），用户扔素材，自动管线处理后归档'),
    ('01-日记', '每日笔记'),
    ('02-资讯日报', '工具只写区（只读），自动管线写入'),
    ('03-软件开发', 'wiki 主题区（可写）'),
    ('04-AI与机器学习', 'wiki 主题区（可写）'),
    ('05-数据分析', 'wiki 主题区（可写）'),
    ('06-项目', '项目区（可写），仅项目相关文档'),
    ('07-模板与系统', '系统区，索引与日志在 MOC/ 下'),
    ('07-模板与系统/MOC', '索引与操作日志'),
    ('99-归档', '归档区，已处理的素材'),
]

# 只读区
READONLY = {'00-收件箱', '02-资讯日报', '07-模板与系统/附件', '07-模板与系统/.模板', '07-模板与系统/脚本'}
# 可写区
WRITABLE = {'03-软件开发', '04-AI与机器学习', '05-数据分析', '06-项目'}

INDEX_TEMPLATE = """---
type: moc
title: 知识库索引
created: {date}
---

# 知识库索引

> 本索引由 AGENTS.md 规则维护。新增 / 合并 / 归档文章时同步更新本文件。
> 条目按文章名 Unicode 码点字母序排列，格式：`- [[文章名]]`

<!-- index:start -->

（暂无文章）

<!-- index:end -->
"""

LOG_TEMPLATE = """---
type: log
title: 知识库操作日志
created: {date}
---

# 知识库操作日志

> 记录所有 ingest / merge / archive / lint / query 等操作。格式：`- YYYY-MM-DD HH:MM 动作 详情`

<!-- log:start -->

- {date} 00:00 init 按 AGENTS.md 规则建立知识库目录骨架（00-收件箱 / 01-日记 / 02-资讯日报 / 03-软件开发 / 04-AI与机器学习 / 05-数据分析 / 06-项目 / 07-模板与系统/MOC / 99-归档），初始化 索引.md 与操作日志.md。

<!-- log:end -->
"""


def init_wiki(wiki_root: Path):
    today = date.today().isoformat()
    created = []

    for dirname, desc in DIRECTORIES:
        d = wiki_root / dirname
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            created.append(f"  ✅ {dirname}/ — {desc}")
        else:
            created.append(f"  ⏭️  {dirname}/ — 已存在")

    index_file = wiki_root / '07-模板与系统/MOC/索引.md'
    if not index_file.exists():
        index_file.write_text(INDEX_TEMPLATE.format(date=today), encoding='utf-8')
        print(f"  ✅ 07-模板与系统/MOC/索引.md — 初始化")
    else:
        print(f"  ⏭️  07-模板与系统/MOC/索引.md — 已存在")

    log_file = wiki_root / '07-模板与系统/MOC/操作日志.md'
    if not log_file.exists():
        log_file.write_text(LOG_TEMPLATE.format(date=today), encoding='utf-8')
        print(f"  ✅ 07-模板与系统/MOC/操作日志.md — 初始化")
    else:
        print(f"  ⏭️  07-模板与系统/MOC/操作日志.md — 已存在")

    return created


def main():
    parser = argparse.ArgumentParser(description='知识库 init 工具')
    parser.add_argument('--wiki', required=True, help='wiki 根目录路径')
    args = parser.parse_args()

    wiki_root = Path(args.wiki)
    if wiki_root.exists():
        print(f"⚠️  wiki 目录已存在: {wiki_root}")
        print("（已存在的目录/文件会跳过，缺失的会补齐）")
    else:
        wiki_root.mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建 wiki 根目录: {wiki_root}")

    print(f"\n建立知识库骨架（{wiki_root}）：")
    for line in init_wiki(wiki_root):
        print(line)

    print(f"\n{'='*60}")
    print(f"✅ 知识库已就绪")
    print(f"\n可写区（写入 wiki 前确认）: {', '.join(sorted(WRITABLE))}")
    print(f"只读区: {', '.join(sorted(READONLY))}")
    print(f"\n下一步：")
    print(f"  1. 在 00-收件箱/ 放素材（@manual 后缀表示手动处理）")
    print(f"  2. 写 wiki 文章到可写区（含 frontmatter + See Also）")
    print(f"  3. 同步更新 07-模板与系统/MOC/索引.md（Unicode 字母序）")
    print(f"  4. 归档素材到 99-归档/，追加操作日志")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
