"""管线主入口：日更与历史回溯。"""
import argparse
import logging
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

from classifier import classify
from filters import apply_blacklist, dedupe, summarize_entries
from render import render_daily
from sources import Entry, fetch_entries, load_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[logging.FileHandler(Path(__file__).parent / ".raw" / "pipeline.log"), logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger("tech_news.pipeline")

BASE_DIR = Path(__file__).parent


def _index_path() -> Path:
    return BASE_DIR / ".raw" / "urls.txt"


def build_report_date_path(out_dir: Path, prefix: str, report_date: str) -> Path:
    month = report_date[:7]
    return out_dir / month / f"{prefix} {report_date}.md"


def _process(entries: list[Entry], cfg: dict):
    entries = dedupe(entries, _index_path())
    entries = apply_blacklist(entries, cfg)
    entries = summarize_entries(entries, cfg)
    sections, degraded = classify(entries, cfg)
    return sections, degraded


def _notify_failed_sources(coverage: dict) -> None:
    failed = [k for k, v in coverage.items() if v == "失败"]
    if not failed:
        return
    logger.warning("失败源: %s", failed)
    try:
        subprocess.run(
            ["notify-send", "科技资讯管线", f"采集失败源: {', '.join(failed)}"],
            timeout=5,
            capture_output=True,
        )
    except Exception:
        pass


def run_daily(cfg: dict) -> Path:
    today = date.today().isoformat()
    entries, coverage = fetch_entries(cfg)
    logger.info("采集 %d 条，覆盖: %s", len(entries), coverage)
    _notify_failed_sources(coverage)
    sections, degraded = _process(entries, cfg)
    out_dir = Path(cfg["output"]["dir"])
    p = render_daily(today, sections, coverage, degraded, cfg, out_dir)
    logger.info("日报已生成: %s (degraded=%s)", p, degraded)
    return p


def run_backfill(start: str, end: str, cfg: dict) -> list[Path]:
    d0 = date.fromisoformat(start)
    d1 = date.fromisoformat(end)
    paths: list[Path] = []
    d = d0
    while d <= d1:
        ds = d.isoformat()
        entries, coverage = fetch_entries(cfg, date_range=(ds, ds))
        logger.info("[%s] 采集 %d 条，覆盖: %s", ds, len(entries), coverage)
        sections, degraded = _process(entries, cfg)
        out_dir = Path(cfg["output"]["dir"])
        p = render_daily(ds, sections, coverage, degraded, cfg, out_dir)
        paths.append(p)
        d += timedelta(days=1)
    return paths


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="科技资讯日报管线")
    parser.add_argument("--backfill", nargs=2, metavar=("START", "END"), help="回溯日期范围 YYYY-MM-DD YYYY-MM-DD")
    parser.add_argument("--config", default=str(BASE_DIR / "config.yaml"))
    args = parser.parse_args(argv)
    cfg = load_config(args.config)
    try:
        if args.backfill:
            paths = run_backfill(*args.backfill, cfg)
            print(f"回溯完成: {len(paths)} 天 -> {[str(p) for p in paths]}")
        else:
            p = run_daily(cfg)
            print(f"日报已生成: {p}")
        return 0
    except Exception as err:
        logger.error("管线失败: %s", err)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
