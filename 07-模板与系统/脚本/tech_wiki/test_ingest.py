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


def test_publish_updates_index_and_log_and_moves(tmp_path):
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
    archive = vault / "99-归档"
    archive.mkdir()
    (sysdir / "索引.md").write_text("- [[已有]]\n", encoding="utf-8")
    (sysdir / "操作日志.md").write_text("# 操作日志\n", encoding="utf-8")
    inbox = vault / "00-收件箱"
    inbox.mkdir()
    src = inbox / "素材.md"
    src.write_text("x")
    article = vault / "03-软件开发" / "新文章.md"
    article.parent.mkdir(parents=True)
    article.write_text("# 新文章")
    publish(article, rules, vault, [src])
    assert "[[新文章]]" in (sysdir / "索引.md").read_text(encoding="utf-8")
    assert "ingest" in (sysdir / "操作日志.md").read_text(encoding="utf-8")
    assert not src.exists()
    assert (archive / "素材.md").exists()
