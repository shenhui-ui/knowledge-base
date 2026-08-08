"""采集模块：RSS 解析、历史回溯、robots.txt 尊重、重试退避、原始数据留存。"""
import json
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import feedparser
import httpx

logger = logging.getLogger("tech_news.sources")


@dataclass
class Entry:
    url: str
    title: str
    summary: str
    published: str
    source: str
    raw_path: str | None = None


class SourceFailure(Exception):
    pass


def load_config(path: str) -> dict:
    import yaml
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def collect_raw(text: bytes, name: str, date: str, raw_dir: Path) -> Path:
    raw_dir.mkdir(parents=True, exist_ok=True)
    suffix = "json" if text[:1] == b"{" else "xml"
    p = raw_dir / f"{name}-{date}.{suffix}"
    p.write_bytes(text)
    return p


def _client(cfg: dict) -> httpx.Client:
    return httpx.Client(
        timeout=cfg["request"]["timeout_seconds"],
        headers={"User-Agent": cfg["request"]["user_agent"]},
    )


def _robots_allows(client: httpx.Client, url: str, ua: str) -> bool:
    parts = urlparse(url)
    robots_url = f"{parts.scheme}://{parts.netloc}/robots.txt"
    rp = RobotFileParser()
    try:
        resp = client.get(robots_url, follow_redirects=True)
        if resp.status_code != 200:
            return True
        rp.parse(resp.text.splitlines())
        return rp.can_fetch(ua, url)
    except Exception:
        return True


def _parse_rss(text: bytes, source_name: str) -> list[Entry]:
    feed = feedparser.parse(text)
    out = []
    for item in feed.entries[:50]:
        link = item.get("link")
        if not link:
            continue
        published = ""
        if item.get("published_parsed"):
            published = datetime(*item.published_parsed[:6]).date().isoformat()
        out.append(Entry(
            url=link,
            title=item.get("title", ""),
            summary=item.get("summary", "")[:500],
            published=published,
            source=source_name,
        ))
    return out


def _fetch_rss(client: httpx.Client, src: dict, cfg: dict, raw_dir: Path, date: str) -> list[Entry]:
    retries = cfg["request"]["retries"]
    base = cfg["request"]["backoff_base"]
    last_err = None
    for attempt in range(retries):
        try:
            resp = client.get(src["url"], follow_redirects=True)
            resp.raise_for_status()
            raw = collect_raw(resp.content, src["name"], date, raw_dir)
            entries = _parse_rss(raw, src["name"])
            for e in entries:
                e.raw_path = str(raw)
            return entries
        except Exception as err:
            last_err = err
            delay = base ** (attempt + 1)
            logger.warning("源 %s 第 %d 次失败: %s，%ds 后重试", src["name"], attempt + 1, err, delay)
            time.sleep(delay)
    raise SourceFailure(f"{src['name']}: {last_err}")


def _fetch_hn_backfill(client: httpx.Client, src: dict, start: str, end: str, raw_dir: Path) -> list[Entry]:
    t0 = int(datetime.fromisoformat(start + "T00:00:00").timestamp())
    t1 = int(datetime.fromisoformat(end + "T23:59:59").timestamp())
    entries: list[Entry] = []
    page = 0
    while True:
        resp = client.get(
            src["backfill_api"],
            params={
                "tags": "story",
                "numericFilters": f"created_at_i>{t0},created_at_i<{t1}",
                "hitsPerPage": 100,
                "page": page,
            },
        )
        resp.raise_for_status()
        raw = collect_raw(resp.content, src["name"], f"{start}_{end}_p{page}", raw_dir)
        data = resp.json()
        for hit in data.get("hits", []):
            url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
            published = hit.get("created_at", "")[:10]
            if not (start <= published <= end):
                continue
            entries.append(Entry(
                url=url,
                title=hit.get("title", ""),
                summary="",
                published=published,
                source=src["name"],
                raw_path=str(raw),
            ))
        if page + 1 >= data.get("nbPages", 1) or page + 1 >= src.get("archive_max_pages", 5):
            break
        page += 1
        time.sleep(1)
    return entries


def _fetch_archive_pages(client: httpx.Client, src: dict, start: str, end: str, raw_dir: Path, cfg: dict) -> list[Entry]:
    entries: list[Entry] = []
    for page in range(1, src.get("archive_max_pages", 5) + 1):
        url = f"{src['url']}?p={page}"
        try:
            resp = client.get(url, follow_redirects=True)
            resp.raise_for_status()
            raw = collect_raw(resp.content, src["name"], f"archive-{start}_{end}-p{page}", raw_dir)
            for e in _parse_rss(raw, src["name"]):
                if start <= e.published <= end:
                    e.raw_path = str(raw)
                    entries.append(e)
        except Exception as err:
            logger.warning("归档分页 %s p%d 失败: %s", src["name"], page, err)
            break
        time.sleep(cfg["request"]["interval_seconds"])
    return entries


def fetch_entries(cfg: dict, date_range: tuple[str, str] | None = None, raw_dir: Path | None = None) -> tuple[list[Entry], dict]:
    raw_dir = raw_dir or Path(__file__).parent / ".raw" / "daily"
    client = _client(cfg)
    coverage: dict = {}
    all_entries: list[Entry] = []
    for src in cfg["sources"]:
        try:
            if not _robots_allows(client, src["url"], cfg["request"]["user_agent"]):
                coverage[src["name"]] = "禁止抓取"
                logger.warning("robots.txt 禁止: %s", src["url"])
                continue
            if date_range and src.get("backfill_api"):
                entries = _fetch_hn_backfill(client, src, *date_range, raw_dir)
                coverage[src["name"]] = "完整" if entries else "无历史"
            elif date_range:
                entries = _fetch_archive_pages(client, src, *date_range, raw_dir, cfg)
                coverage[src["name"]] = "部分" if entries else "无历史"
            else:
                entries = _fetch_rss(client, src, cfg, raw_dir, datetime.now(timezone.utc).date().isoformat())
                coverage[src["name"]] = "完整" if entries else "无条目"
            all_entries.extend(entries)
        except SourceFailure as err:
            coverage[src["name"]] = "失败"
            logger.error("源失败: %s", err)
        time.sleep(cfg["request"]["interval_seconds"])
    return all_entries, coverage
