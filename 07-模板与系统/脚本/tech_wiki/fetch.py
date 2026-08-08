"""网页正文抓取：requests + BeautifulSoup，UA/重试/robots 模式与 tech_news 一致。"""
import logging
import re
import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("tech_wiki.fetch")

MAX_TEXT = 5000


def extract_main_text(html: str) -> str:
    if not html or not html.strip():
        return ""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    best = ""
    for block in soup.find_all(["p", "article", "section", "div"]):
        text = block.get_text(" ", strip=True)
        if len(text) > len(best):
            best = text
    if not best:
        best = soup.get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", best).strip()
    return text[:MAX_TEXT]


def _robots_allows(session: requests.Session, url: str, ua: str) -> bool:
    parts = urlparse(url)
    try:
        resp = session.get(f"{parts.scheme}://{parts.netloc}/robots.txt", timeout=15)
        if resp.status_code != 200:
            return True
        rp = RobotFileParser()
        rp.parse(resp.text.splitlines())
        if not rp.entries:
            return True
        return rp.can_fetch(ua, url)
    except Exception:
        return True


def fetch_article(url: str, rules: dict) -> str:
    ua = "TechWikiCollector/1.0 (personal knowledge base; contact: local-user)"
    session = requests.Session()
    session.headers.update({"User-Agent": ua})
    if not _robots_allows(session, url, ua):
        logger.info("robots 禁止: %s", url)
        return ""
    last_err = None
    for attempt in range(3):
        try:
            resp = session.get(url, timeout=30, headers={"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"})
            resp.raise_for_status()
            if "html" not in resp.headers.get("Content-Type", "").lower():
                return ""
            text = extract_main_text(resp.text)
            logger.info("抓取 %s: %d 字符", url, len(text))
            return text
        except Exception as err:
            last_err = err
            time.sleep(2 ** attempt)
    logger.warning("抓取失败 %s: %s", url, last_err)
    return ""
