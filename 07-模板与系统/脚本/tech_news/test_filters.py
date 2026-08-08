import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sources import Entry
from filters import apply_blacklist, dedupe, summarize_entries


def _e(url, title="t", summary="s", source="x"):
    return Entry(url=url, title=title, summary=summary, published="2026-08-08", source=source)


def test_dedupe_keeps_new_and_writes_index(tmp_path):
    idx = tmp_path / "urls.txt"
    a, b = _e("https://a.b/1"), _e("https://a.b/2")
    assert dedupe([a, b], idx) == [a, b]
    assert dedupe([_e("https://a.b/1")], idx) == []
    assert "https://a.b/2" in idx.read_text()


def test_blacklist_keyword():
    cfg = {"blacklist": {"keywords": ["限时抢购"], "domains": ["ads.com"]}}
    keep = _e("https://ok.com/a", title="正常标题")
    drop1 = _e("https://x.com/b", title="限时抢购专区")
    drop2 = _e("https://ads.com/c")
    result = apply_blacklist([keep, drop1, drop2], cfg)
    assert result == [keep]


def test_summarize_truncates_200():
    cfg = {"summary": {"max_chars": 200}}
    long = _e("https://a.b/l", summary="字" * 500)
    out = summarize_entries([long], cfg)
    assert len(out[0].summary) == 200


def test_summarize_strips_html_tags():
    cfg = {"summary": {"max_chars": 200}}
    html = _e(
        "https://a.b/h",
        summary='<div align="right"><a href="https://a.b/h">点击查看原文</a></div> 正文内容',
    )
    out = summarize_entries([html], cfg)
    assert "<" not in out[0].summary
    assert ">" not in out[0].summary
    assert "点击查看原文" in out[0].summary
    assert "正文内容" in out[0].summary
