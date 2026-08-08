import tempfile
import time
from pathlib import Path

from archive_watcher import (
    extract_date,
    is_final_write,
    is_temp_name,
    monthly_dir,
    versioned_dest,
)


def test_monthly_dir():
    assert monthly_dir("2026-08-08") == "2026-08"


def test_extract_date_from_prefixed_stem():
    assert extract_date("AI 早报 2026-08-08") == "2026-08-08"
    assert extract_date("无日期文件名") is None


def test_is_final_write(tmp_path):
    f = tmp_path / "2026-08-08.md"
    f.write_text("x")
    assert is_final_write(f, 0.0)
    assert not is_temp_name("2026-08-08.md")


def test_is_temp_name():
    assert is_temp_name("a.tmp")
    assert is_temp_name("a.part")
    assert is_temp_name("~a.md")
    assert not is_temp_name("2026-08-08.md")


def test_versioned_dest_increments(tmp_path):
    dest = tmp_path / "2026-08"
    dest.mkdir()
    first = versioned_dest(dest, "2026-08-08", ".md")
    assert first.name == "2026-08-08.md"
    first.write_text("a")
    second = versioned_dest(dest, "2026-08-08", ".md")
    assert second.name == "2026-08-08-1.md"
    second.write_text("b")
    third = versioned_dest(dest, "2026-08-08", ".md")
    assert third.name == "2026-08-08-2.md"
