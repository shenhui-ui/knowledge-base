import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sources import Entry, SourceFailure, collect_raw, load_config


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
