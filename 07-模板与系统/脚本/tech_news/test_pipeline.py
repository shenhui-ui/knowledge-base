import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pipeline import build_report_date_path, main


def test_build_report_date_path(tmp_path):
    p = build_report_date_path(tmp_path, "科技资讯", "2026-08-08")
    assert p.parent.name == "2026-08"
    assert p.name == "科技资讯 2026-08-08.md"


def test_main_usage(capsys, tmp_path, monkeypatch):
    import pytest

    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "--backfill" in out
