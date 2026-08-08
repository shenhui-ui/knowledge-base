import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sources import Entry, SourceFailure, _fetch_hn_backfill, _robots_allows, collect_raw, load_config


class _FakeResp:
    status_code = 200

    def __init__(self, text: str):
        self._text = text

    @property
    def text(self) -> str:
        return self._text


class _FakeClient:
    def __init__(self, resp: _FakeResp):
        self._resp = resp

    def get(self, url: str, follow_redirects: bool = True) -> _FakeResp:
        return self._resp


def test_load_config():
    cfg = load_config(str(Path(__file__).parent / "config.yaml"))
    assert len(cfg["sources"]) >= 7
    assert cfg["request"]["retries"] == 3


def test_collect_raw(tmp_path):
    p = collect_raw(b"<xml/>", "test", "2026-08-08", tmp_path)
    assert p.exists() and p.read_bytes() == b"<xml/>"
    assert p.name == "test-2026-08-08.xml"


def test_entry_fields():
    e = Entry(url="https://a.b", title="t", summary="s", published="2026-08-08", source="x", raw_path=None)
    assert e.url == "https://a.b"


def test_robots_allows_fail_open_when_no_entries():
    robots = "User-Agent: *\nDisallow: /rss\n"
    client = _FakeClient(_FakeResp(robots))
    assert _robots_allows(client, "https://example.com/rss", "TechNewsCollector/1.0") is True


def test_robots_allows_still_blocks_named_agent():
    robots = "User-Agent: badbot\nDisallow: /rss\n"
    client = _FakeClient(_FakeResp(robots))
    assert _robots_allows(client, "https://example.com/rss", "badbot") is False


def test_robots_allows_allows_when_agent_not_listed():
    robots = "User-Agent: badbot\nDisallow: /rss\n"
    client = _FakeClient(_FakeResp(robots))
    assert _robots_allows(client, "https://example.com/rss", "goodbot") is True


class _HnFakeClient:
    """按 page 参数返回固定 JSON 的 HN Algolia 客户端。"""

    def __init__(self, nb_pages: int, hits_per_page: int = 100):
        self._nb_pages = nb_pages
        self._hits_per_page = hits_per_page
        self.pages_fetched: list[int] = []

    def get(self, url: str, params: dict | None = None, follow_redirects: bool = True):
        page = (params or {}).get("page", 0)
        self.pages_fetched.append(page)
        hits = []
        for i in range(self._hits_per_page):
            hits.append({
                "objectID": f"{page}-{i}",
                "title": f"t{page}-{i}",
                "created_at": "2026-08-08T10:00:00Z",
                "url": f"https://example.com/{page}-{i}",
            })
        body = json.dumps({"nbPages": self._nb_pages, "hits": hits}).encode()
        return _FakeRespWithJson(body)

    @property
    def total_pages(self) -> int:
        return len(self.pages_fetched)


class _FakeRespWithJson:
    def __init__(self, content: bytes):
        self.content = content
        self.status_code = 200

    def raise_for_status(self):
        pass

    def json(self):
        return json.loads(self.content)


def test_hn_backfill_complete_false_when_truncated_by_max_pages(monkeypatch, tmp_path):
    import sources

    monkeypatch.setattr(sources.time, "sleep", lambda s: None)
    client = _HnFakeClient(nb_pages=20)
    src = {
        "name": "hacker-news",
        "backfill_api": "https://hn.algolia.com/api/v1/search_by_date",
        "archive_max_pages": 2,
    }
    entries, complete = _fetch_hn_backfill(client, src, "2026-08-08", "2026-08-08", tmp_path)
    assert complete is False
    assert client.total_pages == 2
    assert len(entries) == 2 * 100


def test_hn_backfill_complete_true_when_all_pages_exhausted(monkeypatch, tmp_path):
    import sources

    monkeypatch.setattr(sources.time, "sleep", lambda s: None)
    client = _HnFakeClient(nb_pages=2)
    src = {
        "name": "hacker-news",
        "backfill_api": "https://hn.algolia.com/api/v1/search_by_date",
        "archive_max_pages": 12,
    }
    entries, complete = _fetch_hn_backfill(client, src, "2026-08-08", "2026-08-08", tmp_path)
    assert complete is True
    assert client.total_pages == 2


def test_fetch_entries_hn_coverage_partial(monkeypatch, tmp_path):
    import sources

    def fake_backfill(client, src, start, end, raw_dir):
        e = Entry(url="https://x", title="t", summary="", published=start, source="hacker-news")
        return [e], False

    monkeypatch.setattr(sources, "_robots_allows", lambda *a, **k: True)
    monkeypatch.setattr(sources, "_fetch_hn_backfill", fake_backfill)
    monkeypatch.setattr(sources.time, "sleep", lambda s: None)
    cfg = {
        "request": {"timeout_seconds": 30, "user_agent": "test", "interval_seconds": 0},
        "sources": [{"name": "hacker-news", "url": "https://news.ycombinator.com/rss", "backfill_api": "x"}],
    }
    entries, coverage = sources.fetch_entries(cfg, date_range=("2026-08-08", "2026-08-08"), raw_dir=tmp_path)
    assert coverage["hacker-news"] == "部分"
    assert len(entries) == 1


def test_fetch_entries_hn_coverage_complete(monkeypatch, tmp_path):
    import sources

    def fake_backfill(client, src, start, end, raw_dir):
        e = Entry(url="https://x", title="t", summary="", published=start, source="hacker-news")
        return [e], True

    monkeypatch.setattr(sources, "_robots_allows", lambda *a, **k: True)
    monkeypatch.setattr(sources, "_fetch_hn_backfill", fake_backfill)
    monkeypatch.setattr(sources.time, "sleep", lambda s: None)
    cfg = {
        "request": {"timeout_seconds": 30, "user_agent": "test", "interval_seconds": 0},
        "sources": [{"name": "hacker-news", "url": "https://news.ycombinator.com/rss", "backfill_api": "x"}],
    }
    entries, coverage = sources.fetch_entries(cfg, date_range=("2026-08-08", "2026-08-08"), raw_dir=tmp_path)
    assert coverage["hacker-news"] == "完整"
    assert len(entries) == 1


def test_fetch_entries_hn_coverage_no_history(monkeypatch, tmp_path):
    import sources

    monkeypatch.setattr(sources, "_robots_allows", lambda *a, **k: True)
    monkeypatch.setattr(sources, "_fetch_hn_backfill", lambda *a, **k: ([], True))
    monkeypatch.setattr(sources.time, "sleep", lambda s: None)
    cfg = {
        "request": {"timeout_seconds": 30, "user_agent": "test", "interval_seconds": 0},
        "sources": [{"name": "hacker-news", "url": "https://news.ycombinator.com/rss", "backfill_api": "x"}],
    }
    entries, coverage = sources.fetch_entries(cfg, date_range=("2026-08-08", "2026-08-08"), raw_dir=tmp_path)
    assert coverage["hacker-news"] == "无历史"
    assert entries == []
