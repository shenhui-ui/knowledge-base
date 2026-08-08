import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sources import Entry, SourceFailure, _robots_allows, collect_raw, load_config


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
