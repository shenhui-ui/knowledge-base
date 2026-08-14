"""每日凌晨检查昨日日报是否生成（systemd timer 01:00 调用）。缺失即退出码 1 并输出告警。"""
import sys
from datetime import datetime, timedelta
from pathlib import Path

WATCH_DIR = Path.home() / "Obsidian/02-资讯日报/日报"


def main() -> int:
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    month_dir = WATCH_DIR / yesterday[:7]
    candidates = sorted(
        p for p in month_dir.glob("*.md") if yesterday in p.name
    )
    if candidates:
        print(f"OK: 昨日日报 {candidates[0].name}")
        return 0
    print(f"MISSING: 昨日日报 {yesterday} 未生成", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
