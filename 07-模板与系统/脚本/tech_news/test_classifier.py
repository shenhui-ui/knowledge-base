import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sources import Entry
from classifier import (
    Section,
    chunk_entries,
    classify_with_ai,
    fallback_by_source,
)


def _e(url, source="x", title="t", summary="s"):
    return Entry(url=url, title=title, summary=summary, published="2026-08-08", source=source)


def test_chunk_entries_respects_limit():
    entries = [_e(f"https://a.b/{i}", summary="字" * 400) for i in range(10)]
    chunks = chunk_entries(entries, max_tokens=1000)
    assert len(chunks) >= 2
    assert all(len(c) > 0 for c in chunks)


def test_fallback_by_source_groups_label():
    cfg = {
        "sources": [
            {"name": "hacker-news", "label": "Hacker News 精选"},
            {"name": "sspai", "label": "少数派精选"},
        ]
    }
    entries = [_e("https://1", source="hacker-news"), _e("https://2", source="sspai")]
    sections = fallback_by_source(entries, cfg)
    names = [s.name for s in sections]
    assert names == ["Hacker News 精选", "少数派精选"]
    assert sections[0].items[0]["url"] == "https://1"


def test_extract_json_from_reasoning_only():
    from classifier import _extract_json
    data = {
        "output": [
            {"type": "reasoning", "content": [
                {"type": "reasoning_text", "text": '先思考\n{"sections": [{"name": "AI", "items": []}]}\n结束'}
            ]}
        ]
    }
    assert _extract_json(data) == '{"sections": [{"name": "AI", "items": []}]}'


def test_extract_json_from_output_text_preferred():
    from classifier import _extract_json
    data = {
        "output": [
            {"type": "reasoning", "content": [
                {"type": "reasoning_text", "text": '先思考\n{"sections": []}\n'}
            ]},
            {"type": "message", "content": [
                {"type": "output_text", "text": '{"sections": [{"name": "AI", "items": []}]}'}
            ]},
        ]
    }
    assert _extract_json(data) == '{"sections": [{"name": "AI", "items": []}]}'


def test_extract_json_empty_when_nothing():
    from classifier import _extract_json
    assert _extract_json({"output": []}) == ""


def test_extract_json_multiline_reasoning_takes_last_brace_span():
    from classifier import _extract_json
    data = {
        "output": [
            {"type": "reasoning", "content": [
                {"type": "reasoning_text", "text": "先思考\n{\"a\": 1}\n中间\n{\"sections\": [{\"name\": \"AI\", \"items\": []}]}\n"}
            ]}
        ]
    }
    assert _extract_json(data) == '{"a": 1}\n中间\n{"sections": [{"name": "AI", "items": []}]}'


def test_extract_json_reasoning_no_output_text_returns_json():
    from classifier import _extract_json
    data = {
        "output": [
            {"type": "reasoning", "content": [
                {"type": "reasoning_text", "text": "{\"sections\": [{\"name\": \"AI\", \"items\": []}]}"}
            ]}
        ]
    }
    assert _extract_json(data) == '{"sections": [{"name": "AI", "items": []}]}'


def test_classify_with_ai_uses_fake_api(monkeypatch, tmp_path):
    import classifier

    class FakeClient:
        def close(self):
            pass

        def post(self, url, **kw):
            payload = json.dumps({
                "output": [
                    {"type": "message", "content": [
                        {"type": "output_text", "text": json.dumps(
                            {"sections": [{"name": "AI", "items": [{"url": "https://a.b", "title": "t", "summary": "s"}]}]}
                        )}
                    ]}
                ]
            }).encode()
            return SimpleNamespace(
                status_code=200,
                content=payload,
                raise_for_status=lambda: None,
                json=lambda: json.loads(payload),
            )

    from types import SimpleNamespace
    monkeypatch.setattr(classifier, "_api_client", lambda cfg: FakeClient())
    monkeypatch.setattr(classifier, "_cost_log_path", lambda: tmp_path / "cost.log")
    cfg = {"model": {"api_base": "http://x", "primary": "m", "api_key_env": "NOPE"}}
    sections = classify_with_ai([_e("https://a.b")], "prompt", cfg)
    assert sections[0].name == "AI"
    assert sections[0].items[0]["url"] == "https://a.b"
    assert (tmp_path / "cost.log").exists()
    assert "model=m" in (tmp_path / "cost.log").read_text()


def test_classify_merges_same_name_sections(monkeypatch):
    import classifier

    e1, e2 = _e("https://a"), _e("https://b")
    monkeypatch.setattr(classifier, "chunk_entries", lambda entries, max_tokens: [[e1], [e2]])
    monkeypatch.setattr(
        classifier,
        "classify_with_ai",
        lambda chunk, prompt, cfg: [Section("其他", [{"url": chunk[0].url, "title": chunk[0].title, "summary": chunk[0].summary}])],
    )
    cfg = {"chunk": {"max_tokens": 8000}}
    sections, degraded = classifier.classify([e1, e2], cfg)
    assert degraded is False
    assert len(sections) == 1
    assert sections[0].name == "其他"
    assert [i["url"] for i in sections[0].items] == ["https://a", "https://b"]


def test_classify_dedupes_items_by_url_across_sections(monkeypatch):
    import classifier

    e1, e2 = _e("https://a"), _e("https://b")
    monkeypatch.setattr(classifier, "chunk_entries", lambda entries, max_tokens: [[e1], [e2]])
    monkeypatch.setattr(
        classifier,
        "classify_with_ai",
        lambda chunk, prompt, cfg: [
            Section("AI", [{"url": "https://a", "title": "t", "summary": "s"}]),
            Section("硬件", [{"url": "https://a", "title": "t", "summary": "s"}]),
        ],
    )
    cfg = {"chunk": {"max_tokens": 8000}}
    sections, degraded = classifier.classify([e1, e2], cfg)
    assert degraded is False
    assert [i["url"] for i in sections[0].items] == ["https://a"]
    assert sections[1].items == []
