"""每日检查当天日报是否生成（cron 调用，非轮询归档）。缺失即退出码 1 并输出告警。"""
import sys
from datetime import datetime
from pathlib import Path

WATCH_DIR = Path.home() / "Obsidian/02-资讯日报/日报"


def main() -> int:
    today = datetime.now().strftime("%Y-%m-%d")
    month_dir = WATCH_DIR / today[:7]
    candidates = sorted(
        p for p in month_dir.glob("*.md") if today in p.name
    )
    if candidates:
        print(f"OK: 今日日报 {candidates[0].name}")
        return 0
    print(f"MISSING: 今日日报 {today} 未生成", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
