"""观察 02-资讯日报/日报/ 下新文件，按 YYYY-MM 归档到月目录。事件驱动，无轮询。"""
import argparse
import logging
import re
import sys
import time
from datetime import datetime
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

QUIET_SECONDS = 10.0
HEARTBEAT = Path.home() / ".local/state/obsidian-archive-watcher/heartbeat"
TEMP_SUFFIXES = (".tmp", ".part")
IGNORED_PREFIX = "~"
DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")


def monthly_dir(date_str: str) -> str:
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m")


def extract_date(stem: str):
    """从文件名中提取 YYYY-MM-DD 日期；非日期名（如「AI 早报 2026-08-08」）也能解析，失败返回 None。"""
    match = DATE_PATTERN.search(stem)
    return match.group(0) if match else None


def is_temp_name(name: str) -> bool:
    return (
        name.endswith(TEMP_SUFFIXES)
        or name.startswith(IGNORED_PREFIX)
        or name.endswith(IGNORED_PREFIX)
    )


def is_final_write(path: Path, quiet_seconds: float) -> bool:
    if is_temp_name(path.name):
        return False
    return (time.time() - path.stat().st_mtime) >= quiet_seconds


def versioned_dest(dest_dir: Path, stem: str, suffix: str) -> Path:
    candidate = dest_dir / f"{stem}{suffix}"
    n = 1
    while candidate.exists():
        candidate = dest_dir / f"{stem}-{n}{suffix}"
        n += 1
    return candidate


class ArchiveHandler(FileSystemEventHandler):
    def __init__(self, watch_dir: Path, quiet_seconds: float = QUIET_SECONDS):
        self.watch_dir = watch_dir
        self.quiet_seconds = quiet_seconds
        self.logger = logging.getLogger("archive_watcher")

    def on_closed(self, event):
        if event.is_directory:
            return
        src = Path(event.src_path)
        if is_temp_name(src.name):
            return
        stem, suffix = src.stem, src.suffix
        date_str = extract_date(stem)
        if date_str is None:
            self.logger.warning("文件名不含日期，跳过: %s", src.name)
            return
        month = monthly_dir(date_str)
        dest_dir = src.parent / month
        dest_dir.mkdir(exist_ok=True)
        if not is_final_write(src, self.quiet_seconds):
            self.logger.info("等待静默窗口: %s", src.name)
            time.sleep(self.quiet_seconds + 0.5)
        if not is_final_write(src, self.quiet_seconds):
            self.logger.warning("文件仍在写入，跳过: %s", src.name)
            return
        dest = versioned_dest(dest_dir, stem, suffix)
        src.rename(dest)
        self.logger.info("归档: %s -> %s", src.name, dest.relative_to(self.watch_dir))
        HEARTBEAT.parent.mkdir(parents=True, exist_ok=True)
        HEARTBEAT.write_text(datetime.now().isoformat())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch", default=str(Path.home() / "Obsidian/02-资讯日报/日报"))
    parser.add_argument("--quiet-seconds", type=float, default=QUIET_SECONDS)
    args = parser.parse_args()
    watch_dir = Path(args.watch).resolve()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    handler = ArchiveHandler(watch_dir, args.quiet_seconds)
    observer = Observer()
    observer.schedule(handler, str(watch_dir), recursive=False)
    observer.start()
    logging.getLogger("archive_watcher").info("监听 %s (quiet=%ss)", watch_dir, args.quiet_seconds)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
