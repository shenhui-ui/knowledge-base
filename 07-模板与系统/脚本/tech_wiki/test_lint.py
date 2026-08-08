import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lint import lint_index


def test_lint_reports_missing_and_unindexed(tmp_path):
    rules = {
        "wiki": {
            "index": "07-模板与系统/MOC/索引.md",
            "writable": ["03-软件开发", "04-AI与机器学习", "05-数据分析", "06-项目"],
        }
    }
    sysdir = tmp_path / "07-模板与系统/MOC"
    sysdir.mkdir(parents=True)
    (sysdir / "索引.md").write_text("# 索引\n- [[存在文章]]\n- [[幽灵文章]]\n", encoding="utf-8")
    area = tmp_path / "03-软件开发"
    area.mkdir(parents=True)
    (area / "存在文章.md").write_text("# a", encoding="utf-8")
    (area / "未收录文章.md").write_text("# b", encoding="utf-8")
    (tmp_path / "04-AI与机器学习").mkdir()
    (tmp_path / "05-数据分析").mkdir()
    (tmp_path / "06-项目").mkdir()
    reports = lint_index(tmp_path, rules)
    text = "\n".join(reports)
    assert "[MISSING] 幽灵文章" in text
    assert "[未收录] 03-软件开发/未收录文章.md" in text
    assert "存在文章" not in text


def test_lint_reports_stale_inbox(tmp_path):
    rules = {"wiki": {"index": "07-模板与系统/MOC/索引.md", "writable": ["03-软件开发"]}}
    (tmp_path / "07-模板与系统/MOC").mkdir(parents=True)
    (tmp_path / "07-模板与系统/MOC" / "索引.md").write_text("# 索引\n", encoding="utf-8")
    inbox = tmp_path / "00-收件箱"
    inbox.mkdir()
    stale = inbox / "滞留素材.md"
    stale.write_text("x")
    old = time.time() - 8 * 86400
    import os
    os.utime(stale, (old, old))
    reports = lint_index(tmp_path, rules)
    assert "[滞留]" in "\n".join(reports) and "滞留素材" in "\n".join(reports)
