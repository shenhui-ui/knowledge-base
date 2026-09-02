import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import pytest
from ingest import collect_candidates, insert_sorted, publish, screen


def test_insert_sorted_unicode_order():
    text = "- [[B 文章]]\n- [[D 文章]]\n"
    out = insert_sorted(text, "- [[A 文章]]")
    assert out.splitlines() == ["- [[A 文章]]", "- [[B 文章]]", "- [[D 文章]]"]


def test_insert_sorted_mid():
    text = "- [[A 文章]]\n- [[C 文章]]\n"
    out = insert_sorted(text, "- [[B 文章]]")
    assert out.splitlines() == ["- [[A 文章]]", "- [[B 文章]]", "- [[C 文章]]"]


def test_insert_sorted_duplicate_noop():
    text = "- [[A 文章]]\n"
    assert insert_sorted(text, "- [[A 文章]]") == text


def test_collect_candidates_filters_manual_and_mtime(tmp_path):
    import os

    inbox = tmp_path / "inbox"
    inbox.mkdir()
    d = tmp_path / "daily"
    d.mkdir()
    old = inbox / "old.md"
    old.write_text("# x")
    old_ts = time.time() - 7200
    os.utime(old, (old_ts, old_ts))
    manual = inbox / "手动 @manual.md"
    manual.write_text("# y")
    rules = {"wiki": {"manual_marker": "@manual"}}
    cands, moved = collect_candidates(inbox, d, "2026-08-07", time.time(), rules)
    names = [c["source_path"].name for c in cands]
    assert "手动 @manual.md" not in names
    assert "old.md" in names


def test_screen_ai_failure_degrades(monkeypatch):
    import ingest

    def fake_ai(prompt, content, rules):
        raise RuntimeError("API down")

    monkeypatch.setattr(ingest, "ai_json", fake_ai)
    cands = [{"kind": "daily", "title": "t", "url": "https://x", "summary": "s", "text": "", "source_path": None}]
    passed, note = screen(cands, {})
    assert passed == []
    assert "降级" in note or "失败" in note


def test_build_digest_prompt_includes_writable_dirs():
    from ingest import build_digest_prompt

    rules = {
        "wiki": {
            "digest_rules": ["主题重复 → 合并到已有文章补充"],
            "writable": [
                "03-软件开发",
                "04-AI与机器学习",
                "05-数据分析",
                "06-项目",
                "07-模板与系统/MOC/索引.md",
                "07-模板与系统/MOC/操作日志.md",
            ],
        }
    }
    prompt = build_digest_prompt(rules)
    for d in ("03-软件开发", "04-AI与机器学习", "05-数据分析", "06-项目"):
        assert d in prompt
    assert "索引.md" not in prompt
    assert "操作日志.md" not in prompt


def test_run_skips_screen_for_inbox(tmp_path, monkeypatch):
    import os

    import ingest

    inbox = tmp_path / "00-收件箱"
    inbox.mkdir()
    daily = tmp_path / "02-资讯日报" / "日报"
    daily.mkdir(parents=True)
    src = inbox / "素材.md"
    src.write_text("正文内容")
    old_ts = time.time() - 7200
    os.utime(src, (old_ts, old_ts))
    daily_file = daily / "2026-08" / "科技资讯 2026-08-08.md"
    daily_file.parent.mkdir(parents=True)
    daily_file.write_text("- [日报链接](https://example.com/x)\n")

    rules = {
        "wiki": {
            "index": "07-模板与系统/MOC/索引.md",
            "log": "07-模板与系统/MOC/操作日志.md",
            "manual_marker": "@manual",
        }
    }

    screen_calls = []

    def fake_screen(cands, rules):
        screen_calls.append([c["kind"] for c in cands])
        return [], "筛选: 保留 0/1"

    digested = []

    def fake_digest(item, rules, vault_root):
        digested.append(item)
        article = vault_root / "03-软件开发" / "新文章.md"
        article.parent.mkdir(parents=True)
        article.write_text("# 新文章", encoding="utf-8")
        return article

    monkeypatch.setattr(ingest, "screen", fake_screen)
    monkeypatch.setattr(ingest, "digest", fake_digest)
    out = ingest._run(tmp_path, rules, inbox, daily, "2026-08-08", time.time())
    assert screen_calls == [["daily"]]
    assert [i["kind"] for i in digested] == ["inbox"]
    assert "筛选" in out
    assert "收件箱归档: 1 个文件移入 99-归档/" in out
    assert not src.exists()
    assert (tmp_path / "99-归档" / "素材.md").exists()


def test_publish_updates_index_and_log(tmp_path):
    rules = {
        "wiki": {
            "index": "07-模板与系统/MOC/索引.md",
            "log": "07-模板与系统/MOC/操作日志.md",
            "manual_marker": "@manual",
        }
    }
    vault = tmp_path
    sysdir = vault / "07-模板与系统/MOC"
    sysdir.mkdir(parents=True)
    (sysdir / "索引.md").write_text("- [[已有]]\n", encoding="utf-8")
    (sysdir / "操作日志.md").write_text("# 操作日志\n", encoding="utf-8")
    inbox = vault / "00-收件箱"
    inbox.mkdir()
    src = inbox / "素材.md"
    src.write_text("x")
    article = vault / "03-软件开发" / "新文章.md"
    article.parent.mkdir(parents=True)
    article.write_text("# 新文章")
    publish(article, rules, vault)
    assert "[[新文章]]" in (sysdir / "索引.md").read_text(encoding="utf-8")
    assert "ingest" in (sysdir / "操作日志.md").read_text(encoding="utf-8")
    assert src.exists()


def test_parse_daily_ai_report_list_and_heading(tmp_path):
    from ingest import _parse_daily

    text = """# AI 早报

### 开发生态
- Prime Agent 开源：自改进 RLM 智能体 [↗](https://github.com/PrimeIntellect-ai/prime-agent) [#1](#event-1)
- addyosmani 发布技能包 [↗](https://github.com/addyosmani/agent-skills) [#2](#event-2)

## [Prime Agent 开源：自改进 RLM 智能体](https://github.com/PrimeIntellect-ai/prime-agent) #1
## [addyosmani 发布技能包](https://github.com/addyosmani/agent-skills) #2
"""
    p = tmp_path / "AI 早报 2026-08-08.md"
    p.write_text(text, encoding="utf-8")
    items = _parse_daily(p)
    assert len(items) == 2
    titles = {i["title"] for i in items}
    assert "Prime Agent 开源：自改进 RLM 智能体" in titles
    assert "addyosmani 发布技能包" in titles
    urls = {i["url"] for i in items}
    assert urls == {"https://github.com/PrimeIntellect-ai/prime-agent", "https://github.com/addyosmani/agent-skills"}


def test_parse_daily_plain_link_still_works(tmp_path):
    from ingest import _parse_daily

    p = tmp_path / "科技资讯 2026-08-08.md"
    p.write_text("- [DeepSeek 模型](https://arcprize.org/results/deepseek)\n", encoding="utf-8")
    items = _parse_daily(p)
    assert items == [{"kind": "daily", "title": "DeepSeek 模型", "url": "https://arcprize.org/results/deepseek", "summary": "", "text": "", "source_path": None}]


def test_digest_rejects_system_files(monkeypatch, tmp_path):
    import ingest

    sysdir = tmp_path / "07-模板与系统/MOC"
    sysdir.mkdir(parents=True)
    (sysdir / "索引.md").write_text("# 索引\n", encoding="utf-8")
    (sysdir / "操作日志.md").write_text("# 日志\n", encoding="utf-8")
    rules = {
        "wiki": {
            "index": "07-模板与系统/MOC/索引.md",
            "log": "07-模板与系统/MOC/操作日志.md",
            "writable": ["03-软件开发", "07-模板与系统/MOC/索引.md", "07-模板与系统/MOC/操作日志.md"],
        }
    }

    def fake_ai(prompt, content, rules):
        return {"action": "create", "target": "07-模板与系统/MOC/索引.md", "title": "x", "content": "# x"}

    monkeypatch.setattr(ingest, "ai_json", fake_ai)
    item = {"kind": "inbox", "title": "t", "url": "", "text": "正文"}
    with pytest.raises(ValueError, match="禁止覆盖系统文件"):
        ingest.digest(item, rules, tmp_path)
    assert (sysdir / "索引.md").read_text(encoding="utf-8") == "# 索引\n"


def test_digest_skips_empty_body(monkeypatch, tmp_path):
    import ingest

    calls = []

    def fake_ai(prompt, content, rules):
        calls.append(1)
        return {}

    monkeypatch.setattr(ingest, "ai_json", fake_ai)
    monkeypatch.setattr(ingest, "fetch_article", lambda url, rules: "")
    item = {"kind": "daily", "title": "空标题", "url": "https://x", "text": ""}
    with pytest.raises(ingest.EmptyMaterialError, match="跳过空素材: 空标题"):
        ingest.digest(item, {"wiki": {}}, tmp_path)
    assert calls == []


def test_digest_merge_injects_existing_content(monkeypatch, tmp_path):
    import ingest

    old = tmp_path / "03-软件开发" / "旧文章.md"
    old.parent.mkdir(parents=True)
    old.write_text("---\ntype: ingest-note\n---\n# 旧文章\n旧内容片段\n", encoding="utf-8")
    rules = {"wiki": {"index": "07-模板与系统/MOC/索引.md", "log": "07-模板与系统/MOC/操作日志.md", "writable": ["03-软件开发"]}}
    calls = []

    def fake_ai(prompt, content, rules):
        calls.append(content)
        if len(calls) == 1:
            return {"action": "merge", "target": "03-软件开发/旧文章.md", "title": "旧文章", "content": "# 旧文章\n新内容"}
        return {"action": "merge", "target": "03-软件开发/旧文章.md", "title": "旧文章", "content": "# 旧文章\n旧内容片段\n新内容"}

    monkeypatch.setattr(ingest, "ai_json", fake_ai)
    item = {"kind": "inbox", "title": "t", "url": "", "text": "素材正文"}
    out = ingest.digest(item, rules, tmp_path)
    assert out == old
    assert len(calls) == 2
    assert "已有文章内容" in calls[1]
    assert "旧内容片段" in calls[1]
    final = old.read_text(encoding="utf-8")
    assert "旧内容片段" in final
    assert "新内容" in final


def test_normalize_frontmatter_closes_unclosed():
    from ingest import _normalize_frontmatter

    content = "---\ntype: ingest-note\n# 标题\n正文内容"
    out = _normalize_frontmatter(content, "https://x")
    assert out.endswith("---\n")
    assert "# 标题" in out
    assert "source: https://x" in out
    assert "date: " in out
    assert out.count("---") == 2


def test_normalize_frontmatter_injects_full_block():
    from ingest import _normalize_frontmatter

    content = "# 标题\n正文"
    out = _normalize_frontmatter(content, "https://y")
    assert out.startswith("---\ntype: ingest-note\nsource: https://y\ndate: ")
    assert "---\n" in out
    assert out.endswith("# 标题\n正文")


def test_digest_preserves_closed_frontmatter_without_source(monkeypatch, tmp_path):
    import ingest

    rules = {"wiki": {"index": "07-模板与系统/MOC/索引.md", "log": "07-模板与系统/MOC/操作日志.md", "writable": ["03-软件开发"]}}

    def fake_ai(prompt, content, rules):
        return {"action": "create", "target": "03-软件开发/新文章.md", "title": "新文章", "content": "---\ntype: ingest-note\n---\n# 标题\n正文"}

    monkeypatch.setattr(ingest, "ai_json", fake_ai)
    item = {"kind": "daily", "title": "t", "url": "https://x", "text": "素材"}
    out = ingest.digest(item, rules, tmp_path)
    text = out.read_text(encoding="utf-8")
    assert text.startswith("---\ntype: ingest-note\nsource: https://x\ndate: ")
    assert text.endswith("---\n# 标题\n正文\n")


def test_force_md_suffix_variants():
    from ingest import _force_md_suffix

    base = Path("/vault/03-软件开发")
    assert _force_md_suffix(base / "a.pdf") == base / "a.md"
    assert _force_md_suffix(base / "a.json") == base / "a.md"
    assert _force_md_suffix(base / "a") == base / "a.md"
    assert _force_md_suffix(base / "vllm_project_0.28.0") == base / "vllm_project_0.28.0.md"
    assert _force_md_suffix(base / "a.md") == base / "a.md"


def test_resolve_target_forces_md(tmp_path):
    import ingest

    rules = {"wiki": {"writable": ["03-软件开发"]}}
    out = ingest._resolve_target("03-软件开发/Netbsd-for-enterprise-network.pdf", rules, tmp_path)
    assert out == tmp_path / "03-软件开发" / "Netbsd-for-enterprise-network.md"


def test_digest_redirects_near_duplicate_to_existing(monkeypatch, tmp_path):
    import ingest

    old = tmp_path / "03-软件开发" / ".NET-MAUI-11-Preview-6-架构更新.md"
    old.parent.mkdir(parents=True)
    old.write_text("# 旧文", encoding="utf-8")
    rules = {
        "wiki": {
            "index": "07-模板与系统/MOC/索引.md",
            "log": "07-模板与系统/MOC/操作日志.md",
            "writable": ["03-软件开发"],
        }
    }
    sysdir = tmp_path / "07-模板与系统/MOC"
    sysdir.mkdir(parents=True)
    (sysdir / "索引.md").write_text("- [[.NET-MAUI-11-Preview-6-架构更新]]\n", encoding="utf-8")
    calls = []

    def fake_ai(prompt, content, rules):
        calls.append(content)
        if len(calls) == 1:
            return {"action": "create", "target": "03-软件开发/NET-MAUI-11-Preview-6-架构更新.md", "title": "x", "content": "# 新"}
        return {"action": "merge", "target": "03-软件开发/NET-MAUI-11-Preview-6-架构更新.md", "title": "x", "content": "# 旧文\n# 新"}

    monkeypatch.setattr(ingest, "ai_json", fake_ai)
    item = {"kind": "inbox", "title": "t", "url": "", "text": "素材"}
    out = ingest.digest(item, rules, tmp_path)
    assert out == old
    assert len(calls) == 2
    assert "旧文" in old.read_text(encoding="utf-8")
    assert "新" in old.read_text(encoding="utf-8")


def test_digest_prompt_includes_item_title(monkeypatch, tmp_path):
    import ingest

    seen = {}

    def fake_ai(prompt, content, rules):
        seen["content"] = content
        return {"action": "create", "target": "03-软件开发/新.md", "title": "新", "content": "# 新"}

    monkeypatch.setattr(ingest, "ai_json", fake_ai)
    rules = {
        "wiki": {
            "index": "07-模板与系统/MOC/索引.md",
            "log": "07-模板与系统/MOC/操作日志.md",
            "writable": ["03-软件开发"],
        }
    }
    sysdir = tmp_path / "07-模板与系统/MOC"
    sysdir.mkdir(parents=True)
    (sysdir / "索引.md").write_text("", encoding="utf-8")
    ingest.digest({"kind": "daily", "title": "Slic3r 争议", "url": "https://x", "text": "正文"}, rules, tmp_path)
    assert "素材标题: Slic3r 争议" in seen["content"]
    assert "素材来源: https://x" in seen["content"]
