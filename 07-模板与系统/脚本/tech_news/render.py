"""渲染模块：生成统一格式的科技资讯日报。"""
from pathlib import Path

from classifier import Section


def render_daily(
    report_date: str,
    sections: list[Section],
    coverage: dict,
    degraded: bool,
    cfg: dict,
    out_dir: Path,
) -> Path:
    prefix = cfg["output"]["filename_prefix"]
    name = f"{prefix} {report_date}.md"
    lines: list[str] = []
    lines.append("---")
    lines.append(f"date: {report_date}")
    lines.append("type: tech-daily")
    if degraded:
        lines.append("degraded: true")
    lines.append("---")
    lines.append(f"# 科技资讯 {report_date}")
    lines.append("")
    lines.append("## 数据覆盖")
    for src, status in coverage.items():
        lines.append(f"- {src}：{status}")
    lines.append("")
    if degraded:
        lines.append("> （降级模式）AI 分类不可用，已按来源分组")
        lines.append("")
    for section in sections:
        lines.append(f"## {section.name}")
        lines.append("")
        for item in section["items"] if isinstance(section, dict) else section.items:
            title = item["title"] or item["url"]
            summary = item.get("summary") or ""
            lines.append(f"- [{title}]({item['url']})")
            if summary:
                lines.append(f"  {summary}")
        lines.append("")
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / name
    p.write_text("\n".join(lines), encoding="utf-8")
    return p
