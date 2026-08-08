import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from classifier import Section
from render import render_daily


def test_render_daily_structure(tmp_path):
    cfg = {"output": {"filename_prefix": "科技资讯"}}
    sections = [
        Section(name="大模型与AI应用", items=[
            {"url": "https://a.b/1", "title": "标题一", "summary": "摘要一"},
        ]),
    ]
    coverage = {"hacker-news": "完整", "sspai": "失败"}
    p = render_daily("2026-08-08", sections, coverage, degraded=False, cfg=cfg, out_dir=tmp_path)
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert p.name == "科技资讯 2026-08-08.md"
    assert "## 大模型与AI应用" in text
    assert "[标题一](https://a.b/1)" in text
    assert "摘要一" in text
    assert "hacker-news：完整" in text
    assert "sspai：失败" in text
    assert "degraded" not in text.lower()


def test_render_daily_marks_degraded(tmp_path):
    cfg = {"output": {"filename_prefix": "科技资讯"}}
    sections = [Section(name="Hacker News 精选", items=[])]
    coverage = {"hacker-news": "完整"}
    p = render_daily("2026-08-08", sections, coverage, degraded=True, cfg=cfg, out_dir=tmp_path)
    text = p.read_text(encoding="utf-8")
    assert "degraded: true" in text
    assert "（降级模式）" in text
