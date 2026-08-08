"""过滤模块：URL 去重、黑名单、摘要截断。"""
from pathlib import Path
from urllib.parse import urlparse

from sources import Entry


def dedupe(entries: list[Entry], index_path: Path) -> list[Entry]:
    seen = set()
    if index_path.exists():
        seen = {line.strip() for line in index_path.read_text(encoding="utf-8").splitlines() if line.strip()}
    fresh: list[Entry] = []
    with index_path.open("a", encoding="utf-8") as f:
        for e in entries:
            if e.url in seen:
                continue
            seen.add(e.url)
            fresh.append(e)
            f.write(e.url + "\n")
    return fresh


def apply_blacklist(entries: list[Entry], cfg: dict) -> list[Entry]:
    keywords = cfg["blacklist"]["keywords"]
    domains = set(cfg["blacklist"]["domains"])
    out = []
    for e in entries:
        hay = f"{e.title} {e.summary}"
        if any(k in hay for k in keywords):
            continue
        if urlparse(e.url).netloc in domains:
            continue
        out.append(e)
    return out


def summarize_entries(entries: list[Entry], cfg: dict) -> list[Entry]:
    limit = cfg["summary"]["max_chars"]
    for e in entries:
        if len(e.summary) > limit:
            e.summary = e.summary[:limit]
    return entries
