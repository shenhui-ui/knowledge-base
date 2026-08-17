#!/usr/bin/env python3
"""
知识库 query 工具 — 按 AGENTS.md「query」命令实现三阶段匹配。

匹配策略（三层优先级）：
1. 子串优先：文章名 ⊂ query
2. 关键词匹配标题：query 中任意词 ⊂ 文章名
3. 非泛词搜索内容：query 中去掉泛词（模型/架构/预训练等）的关键词命中正文

用法：
    python3 query.py <问题> [--wiki /path/to/wiki] [--limit 5]
"""
import argparse
import re
import sys
from pathlib import Path

TOPICS = ['03-软件开发', '04-AI与机器学习', '05-数据分析', '06-项目']
INDEX_FILE = '07-模板与系统/MOC/索引.md'

# 泛词黑名单：高频但无区分度的词，禁止用于内容匹配
GENERIC = {
    '模型', '架构', '预训练', '编程', '生成', '图像', '模板',
    '部署', '处理', '是什么', '怎么用', '如何', '进展',
    '区别', '应用', '方法', '特点', '作用', '影响',
}


def load_index(wiki_root: Path):
    """读取索引，加载所有文章。"""
    index_path = wiki_root / INDEX_FILE
    content = index_path.read_text(encoding='utf-8')
    entries = [e for e in re.findall(r'\[\[([^\]]+)\]\]', content) if e != '文章名']

    file_map = {}
    for d in TOPICS:
        for f in (wiki_root / d).rglob('*.md'):
            file_map[f.stem] = (d, f)
    return entries, file_map


def query(q: str, entries, file_map):
    """三阶段匹配：子串 → 标题关键词 → 正文非泛词。"""
    keywords = [w for w in re.split(r'[\s？?]+', q) if w]
    hits = []

    # 优先级 1: 子串优先
    for entry in entries:
        if entry in q:
            hits.append(entry)

    # 优先级 2: 关键词匹配标题
    if not hits:
        for entry in entries:
            for kw in keywords:
                if kw.lower() in entry.lower():
                    hits.append(entry)
                    break

    # 优先级 3: 非泛词搜索正文
    if not hits:
        specific = [kw for kw in keywords if kw not in GENERIC]
        for entry in entries:
            if entry in file_map:
                content = file_map[entry][1].read_text(encoding='utf-8')
                for kw in specific:
                    if kw.lower() in content.lower():
                        hits.append(entry)
                        break

    return list(set(hits))


def synthesize(hits, file_map, limit: int = 5):
    """读取命中文章，生成摘要。"""
    results = []
    for hit in hits[:limit]:
        if hit not in file_map:
            results.append({'name': hit, 'topic': '?', 'error': '文件不存在'})
            continue
        d, path = file_map[hit]
        content = path.read_text(encoding='utf-8')
        # 提取 frontmatter
        fm = {}
        if content.startswith('---'):
            fm_match = re.match(r'---\n(.*?)\n---', content, re.DOTALL)
            if fm_match:
                for line in fm_match.group(1).split('\n'):
                    if ':' in line:
                        k, v = line.split(':', 1)
                        fm[k.strip()] = v.strip()
        # 提取正文摘要（去掉 frontmatter 和 See Also）
        body = re.sub(r'---\n.*?---\n', '', content, count=1, flags=re.DOTALL)
        body = re.sub(r'## See Also\n.*$', '', body, flags=re.DOTALL)
        body = body.strip()
        # 摘要：前 300 字
        summary = body[:300] + ('...' if len(body) > 300 else '')
        results.append({
            'name': hit,
            'topic': d,
            'source': fm.get('source', '?'),
            'date': fm.get('date', '?'),
            'summary': summary,
        })
    return results


def llm_synthesize(question: str, results, model: str = 'deepseek-r1:7b'):
    """本地模型（Ollama）综合答案合成。"""
    import json
    import requests

    context = []
    for r in results:
        context.append(f"## {r['name']}（{r['topic']}）\n源: {r['source']} | date: {r['date']}\n{r['summary']}")
    prompt = (
        "你是知识库问答助手。根据以下从个人知识库检索到的文章内容，回答用户问题。"
        "只依据给定内容回答，内容不足时明确说明；引用时标注文章名。"
        '输出纯文本（非 JSON）。\n\n检索到的内容：\n' + "\n\n".join(context)
    )
    resp = requests.post(
        "http://localhost:11434/v1/chat/completions",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": question},
            ],
            "stream": False,
            "options": {"temperature": 0.3},
        },
        timeout=600,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def main():
    parser = argparse.ArgumentParser(description='知识库 query 工具')
    parser.add_argument('question', help='查询问题')
    parser.add_argument('--wiki', required=True, help='wiki 根目录路径')
    parser.add_argument('--limit', type=int, default=5, help='返回前 N 个结果')
    parser.add_argument('--llm', action='store_true', help='用本地模型（Ollama）综合答案')
    parser.add_argument('--model', default='deepseek-r1:7b', help='本地模型名（--llm 时生效）')
    args = parser.parse_args()

    wiki_root = Path(args.wiki)
    if not wiki_root.exists():
        print(f"❌ wiki 根目录不存在: {wiki_root}")
        sys.exit(1)

    entries, file_map = load_index(wiki_root)
    hits = query(args.question, entries, file_map)

    if not hits:
        print(f"Query: {args.question}")
        print("命中: 0 条")
        print("❌ 未找到相关文章")
        print("（知识库未覆盖此问题，可考虑 ingest 新素材）")
        sys.exit(0)

    results = synthesize(hits, file_map, args.limit)

    if args.llm:
        print(f"Query: {args.question}")
        print(f"命中: {len(hits)} 条（本地模型合成中…）")
        print("=" * 60)
        try:
            answer = llm_synthesize(args.question, results, args.model)
            print(f"\n{answer}\n")
        except Exception as err:
            print(f"⚠️ 本地模型合成失败: {err}")
            print("（以下为检索结果）")
            for r in results:
                print(f"\n## {r['name']}（{r['topic']}）")
                print(f"源: {r['source']} | date: {r['date']}")
                print(f"\n{r['summary']}")
        sys.exit(0)

    print(f"Query: {args.question}")
    print(f"命中: {len(hits)} 条")
    print("=" * 60)
    for r in results:
        print(f"\n## {r['name']}（{r['topic']}）")
        print(f"源: {r['source']} | date: {r['date']}")
        print(f"\n{r['summary']}")


if __name__ == '__main__':
    main()
