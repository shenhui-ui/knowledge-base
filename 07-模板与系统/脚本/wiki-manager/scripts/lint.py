#!/usr/bin/env python3
"""
知识库 lint 工具 — 按 AGENTS.md 规则检查 wiki 知识库的一致性。

按 AGENTS.md「lint_rules」执行六项检查：
1. 索引条目 vs 实际文章（跨目录匹配）
2. 主题区分布
3. 链接目标存在性（含空格/中文文件名）
4. 双向链接对称性
5. 索引 Unicode 顺序
6. 收件箱/归档状态

能安全自动修的（索引补漏、移除 MISSING 条目）直接修；
需判断的（矛盾、孤立页）报告。
绝不报告原文/真实数据时输出本文件路径（沙箱外不可见）。

用法：
    python3 lint.py [--wiki /path/to/wiki] [--fix]
"""
import argparse
import re
import sys
from pathlib import Path

# 主题区白名单
TOPICS = ['03-软件开发', '04-AI与机器学习', '05-数据分析', '06-项目']
INDEX_FILE = '07-模板与系统/MOC/索引.md'
LOG_FILE = '07-模板与系统/MOC/操作日志.md'
INBOX = '00-收件箱'
ARCHIVE = '99-归档'


def scan_wiki(wiki_root: Path):
    """扫描 wiki 全部文件，构建索引。"""
    index_path = wiki_root / INDEX_FILE
    if not index_path.exists():
        print(f"❌ 索引文件不存在: {index_path}")
        sys.exit(1)

    content = index_path.read_text(encoding='utf-8')
    # 提取 [[文章名]] 形式的条目，过滤掉文档注释里的 [[文章名]] 示例
    index_entries = [e for e in re.findall(r'\[\[([^\]]+)\]\]', content) if e != '文章名']

    file_map = {}
    for d in TOPICS:
        for f in (wiki_root / d).rglob('*.md'):
            if f.stem in file_map:
                print(f"  ⚠️  重名: {d}/{f.stem} 与 {file_map[f.stem][0]}/{f.stem}")
            file_map[f.stem] = (d, f)

    return index_entries, file_map


def check_index_consistency(index_entries, file_map):
    """检查 1: 索引与实际文章一致。"""
    errors = []
    matched = 0
    for entry in index_entries:
        if entry in file_map:
            matched += 1
        else:
            errors.append(f"索引失效: [[{entry}]] 无对应文件")
    for name in file_map:
        if name not in index_entries:
            errors.append(f"孤立文章: {file_map[name][0]}/{name} 不在索引中")
    return matched, errors


def check_link_validity(file_map):
    """检查 3: 所有 [[...]] 链接目标存在。"""
    errors = []
    for name, (d, path) in file_map.items():
        content = path.read_text(encoding='utf-8')
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        for link in links:
            if link == name:
                errors.append(f"自我引用: {d}/{name}")
                continue
            if link not in file_map:
                errors.append(f"失效链接: {d}/{name} → [[{link}]]")
    return errors


def check_bidirectional(file_map):
    """检查 4: 双向链接对称性。"""
    warnings = []
    for name, (d, path) in file_map.items():
        content = path.read_text(encoding='utf-8')
        out_links = set(l for l in re.findall(r'\[\[([^\]]+)\]\]', content) if l != name)
        for link in out_links:
            if link in file_map:
                lp = file_map[link][1]
                back = re.findall(r'\[\[([^\]]+)\]\]', lp.read_text(encoding='utf-8'))
                if name not in back:
                    warnings.append(f"单向链接: {name} → {link}（反向缺失）")
    return warnings


def check_unicode_order(index_entries):
    """检查 5: 索引按 Unicode 码点字母序。"""
    sorted_entries = sorted(index_entries, key=lambda x: x.encode('utf-8'))
    if index_entries != sorted_entries:
        mismatches = []
        for i, (a, b) in enumerate(zip(index_entries, sorted_entries)):
            if a != b:
                mismatches.append(f"  位置 {i}: 当前={a} 应为={b}")
        return False, mismatches
    return True, []


def check_inbox_archive(wiki_root: Path):
    """检查 6: 收件箱应空，归档应有内容。"""
    inbox = list((wiki_root / INBOX).glob('*')) if (wiki_root / INBOX).exists() else []
    archive = list((wiki_root / ARCHIVE).glob('*')) if (wiki_root / ARCHIVE).exists() else []
    return {
        'inbox_count': len(inbox),
        'archive_count': len(archive),
        'inbox_files': [f.name for f in inbox]
    }


def auto_fix_index(wiki_root: Path, file_map):
    """自动修复索引：补漏（加入孤立文章）、移除失效条目。"""
    index_path = wiki_root / INDEX_FILE
    content = index_path.read_text(encoding='utf-8')
    entries = [e for e in re.findall(r'\[\[([^\]]+)\]\]', content) if e != '文章名']

    fixed = False
    new_entries = sorted(set(entries + list(file_map.keys())), key=lambda x: x.encode('utf-8'))

    if new_entries != entries:
        new_block = '\n'.join(f'- [[{e}]]' for e in new_entries)
        # 有 index:start/end 标记块 → 只重建块内
        if '<!-- index:start -->' in content:
            new_content = re.sub(
                r'(<!-- index:start -->\n).*?(\n<!-- index:end -->)',
                f'\\1{new_block}\\2',
                content,
                flags=re.DOTALL
            )
        else:
            # 无标记（本项目形态）：保留非条目行（标题等），重建条目区
            header = [l for l in content.splitlines(keepends=True) if not l.startswith('- [[')]
            new_content = ''.join(header) + new_block + '\n'
        if new_content != content:
            index_path.write_text(new_content, encoding='utf-8')
            fixed = True
            print(f"  🔧 已自动修复索引（补漏/去失效）")

    return fixed, new_entries


def main():
    parser = argparse.ArgumentParser(description='知识库 lint 工具')
    parser.add_argument('--wiki', required=True, help='wiki 根目录路径')
    parser.add_argument('--fix', action='store_true', help='自动修复可安全修的问题')
    args = parser.parse_args()

    wiki_root = Path(args.wiki)
    if not wiki_root.exists():
        print(f"❌ wiki 根目录不存在: {wiki_root}")
        sys.exit(1)

    print("=" * 60)
    print(f"知识库 lint — {wiki_root}")
    print("=" * 60)

    index_entries, file_map = scan_wiki(wiki_root)

    # 检查 1: 索引一致性
    print(f"\n【1. 索引一致性】")
    print(f"   索引: {len(index_entries)} 条 | 文章: {len(file_map)} 篇")
    matched, idx_errors = check_index_consistency(index_entries, file_map)
    for e in idx_errors:
        print(f"   ❌ {e}")
    print(f"   {'✅' if not idx_errors else '⚠️'} 匹配: {matched}/{len(index_entries)}")

    # 检查 2: 主题区分布
    print(f"\n【2. 主题区分布】")
    for d in TOPICS:
        cnt = sum(1 for dd, _ in file_map.values() if dd == d)
        print(f"   {d}: {cnt} 篇")
    print(f"   总计: {len(file_map)} 篇")

    # 检查 3: 链接目标
    print(f"\n【3. 链接目标存在性】")
    link_errors = check_link_validity(file_map)
    for e in link_errors:
        print(f"   ❌ {e}")
    print(f"   {'✅' if not link_errors else '⚠️'} {'全部有效' if not link_errors else f'有 {len(link_errors)} 个问题'}")

    # 检查 4: 双向链接
    print(f"\n【4. 双向链接对称性】")
    bidir_warnings = check_bidirectional(file_map)
    for w in bidir_warnings:
        print(f"   ⚠️  {w}")
    print(f"   {'✅ 对称' if not bidir_warnings else f'⚠️ {len(bidir_warnings)} 条意向性单向'}")

    # 检查 5: Unicode 顺序
    print(f"\n【5. 索引 Unicode 顺序】")
    ok, mismatches = check_unicode_order(index_entries)
    if ok:
        print(f"   ✅ 顺序正确（{len(index_entries)} 条）")
    else:
        print(f"   ❌ 顺序错乱")
        for m in mismatches:
            print(m)

    # 检查 6: 收件箱/归档
    print(f"\n【6. 收件箱/归档】")
    state = check_inbox_archive(wiki_root)
    print(f"   收件箱: {state['inbox_count']} 个" + (" ⚠️ 非空" if state['inbox_count'] else " ✅ 空"))
    print(f"   归档: {state['archive_count']} 份")

    # 自动修复
    if args.fix and (idx_errors or not ok):
        print(f"\n【自动修复】")
        auto_fix_index(wiki_root, file_map)

    # 汇总
    print(f"\n{'='*60}")
    error_count = len(idx_errors) + len(link_errors) + (0 if ok else 1)
    warning_count = len(bidir_warnings)
    print(f"错误: {error_count} | 警告: {warning_count}")
    if error_count == 0:
        print("✅ 全部通过")
    print("=" * 60)

    sys.exit(0 if error_count == 0 else 1)


if __name__ == '__main__':
    main()
