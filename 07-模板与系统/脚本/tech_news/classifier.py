"""分类模块：分段、AI 分类、按来源降级。"""
import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import httpx

from sources import Entry

logger = logging.getLogger("tech_news.classifier")


@dataclass
class Section:
    name: str
    items: list[dict] = field(default_factory=list)


def _api_client(cfg: dict) -> httpx.Client:
    return httpx.Client(timeout=120)


def _api_key(cfg: dict) -> str:
    env = cfg["model"].get("api_key_env")
    if env and os.environ.get(env):
        return os.environ[env]
    auth = Path.home() / ".codex/auth.json"
    if auth.exists():
        return json.loads(auth.read_text())["OPENAI_API_KEY"]
    raise RuntimeError("无 API key")


def chunk_entries(entries: list[Entry], max_tokens: int) -> list[list[Entry]]:
    chunks: list[list[Entry]] = []
    cur: list[Entry] = []
    cur_tokens = 0
    for e in entries:
        tokens = int(len(f"{e.title}{e.summary}") * 0.5) + 20
        if cur and cur_tokens + tokens > max_tokens:
            chunks.append(cur)
            cur, cur_tokens = [], 0
        cur.append(e)
        cur_tokens += tokens
    if cur:
        chunks.append(cur)
    return chunks


def _extract_json(data: dict) -> str:
    """从 responses API 响应中提取完整分类 JSON 文本。

    优先取 output_text（正常路径）；若 API 只返回 reasoning_text（长输入时
    完整 JSON 可能放在 reasoning 中），取第一个 '{' 到最后一个 '}' 的子串。
    """
    parts: list[str] = []
    for out in data.get("output", []):
        for content in out.get("content", []):
            if content.get("type") == "output_text":
                parts.append(content.get("text", ""))
    text = "".join(parts).strip()
    if text:
        return text
    for out in data.get("output", []):
        for content in out.get("content", []):
            if content.get("type") == "reasoning_text":
                text = content.get("text", "")
                start, end = text.find("{"), text.rfind("}")
                if start >= 0 and end > start:
                    return text[start : end + 1]
    return ""


def classify_with_ai(chunk: list[Entry], prompt: str, cfg: dict) -> list[Section]:
    payload = {
        "model": cfg["model"]["primary"],
        "input": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(
                [{"url": e.url, "title": e.title, "summary": e.summary, "date": e.published} for e in chunk],
                ensure_ascii=False,
            )},
        ],
    }
    client = _api_client(cfg)
    try:
        resp = client.post(
            cfg["model"]["api_base"],
            json=payload,
            headers={"Authorization": f"Bearer {_api_key(cfg)}"},
        )
        resp.raise_for_status()
        data = resp.json()
        text = _extract_json(data)
        parsed = json.loads(text)
        usage = data.get("usage", {})
        cost_log = Path(__file__).parent / ".raw" / "cost.log"
        cost_log.parent.mkdir(parents=True, exist_ok=True)
        with cost_log.open("a", encoding="utf-8") as f:
            f.write(
                f"{datetime.now().isoformat()} model={cfg['model']['primary']} "
                f"input_tokens={usage.get('input_tokens', '?')} "
                f"output_tokens={usage.get('output_tokens', '?')}\n"
            )
        return [Section(name=s["name"], items=s["items"]) for s in parsed["sections"]]
    finally:
        client.close()


def fallback_by_source(entries: list[Entry], cfg: dict) -> list[Section]:
    labels = {s["name"]: s["label"] for s in cfg["sources"]}
    groups: dict[str, list[dict]] = {}
    for e in entries:
        label = labels.get(e.source, f"{e.source} 精选")
        groups.setdefault(label, []).append(
            {"url": e.url, "title": e.title, "summary": e.summary}
        )
    return [Section(name=name, items=items) for name, items in groups.items()]


def classify(entries: list[Entry], cfg: dict) -> tuple[list[Section], bool]:
    if not entries:
        return [], False
    prompt = (Path(__file__).parent / "system_prompt.md").read_text(encoding="utf-8")
    try:
        sections: list[Section] = []
        for chunk in chunk_entries(entries, cfg["chunk"]["max_tokens"]):
            sections.extend(classify_with_ai(chunk, prompt, cfg))
        return sections, False
    except Exception as err:
        logger.error("AI 分类失败，降级按来源分组: %s", err)
        return fallback_by_source(entries, cfg), True
