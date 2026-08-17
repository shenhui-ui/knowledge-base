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


def _cost_log_path() -> Path:
    return Path(__file__).parent / ".raw" / "cost.log"


def classify_with_ai(chunk: list[Entry], prompt: str, cfg: dict) -> list[Section]:
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": json.dumps(
            [{"url": e.url, "title": e.title, "summary": e.summary, "date": e.published} for e in chunk],
            ensure_ascii=False,
        )},
    ]
    if cfg["model"].get("provider") == "ollama":
        text = _classify_ollama(messages, cfg)
    else:
        payload = {"model": cfg["model"]["primary"], "input": messages}
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
            usage = data.get("usage", {})
        finally:
            client.close()
        _write_cost_log(cfg["model"]["primary"], usage)
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as err:
        retry_messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": (
                messages[-1]["content"]
                + f"\n\n【上次输出不是合法 JSON，错误：{err}。"
                f"请只输出合法 JSON。上次输出：{text[:200]}】"
            )},
        ]
        if cfg["model"].get("provider") == "ollama":
            text = _classify_ollama(retry_messages, cfg)
        else:
            client = _api_client(cfg)
            try:
                resp = client.post(
                    cfg["model"]["api_base"],
                    json={"model": cfg["model"]["primary"], "input": retry_messages},
                    headers={"Authorization": f"Bearer {_api_key(cfg)}"},
                )
                resp.raise_for_status()
                data = resp.json()
                text = _extract_json(data)
                usage = data.get("usage", {})
            finally:
                client.close()
            _write_cost_log(cfg["model"]["primary"], usage)
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as err2:
            raise RuntimeError(f"分类返回非 JSON: {err2}") from err2
    return [Section(name=s["name"], items=s["items"]) for s in parsed["sections"]]


def _classify_ollama(messages: list[dict], cfg: dict) -> str:
    """本地模型（Ollama）分类调用，返回 JSON 文本。"""
    import requests

    resp = requests.post(
        "http://localhost:11434/v1/chat/completions",
        json={
            "model": cfg["model"]["primary"],
            "messages": messages,
            "stream": False,
            "response_format": {"type": "json_object"},
            "options": {"temperature": 0.2, "num_predict": 4000},
        },
        timeout=900,
    )
    resp.raise_for_status()
    data = resp.json()
    text = data["choices"][0]["message"]["content"]
    if not text:
        raise RuntimeError("AI 响应无文本")
    usage = data.get("usage", {})
    _write_cost_log(
        cfg["model"]["primary"],
        {
            "input_tokens": usage.get("prompt_tokens", "?"),
            "output_tokens": usage.get("completion_tokens", "?"),
            "input_tokens_details": {},
        },
    )
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise RuntimeError("本地模型输出中无 JSON 对象")
    return text[start : end + 1]


def _write_cost_log(model: str, usage: dict) -> None:
    cost_log = _cost_log_path()
    cost_log.parent.mkdir(parents=True, exist_ok=True)
    with cost_log.open("a", encoding="utf-8") as f:
        f.write(
            f"{datetime.now().isoformat()} model={model} "
            f"input_tokens={usage.get('input_tokens', '?')} "
            f"output_tokens={usage.get('output_tokens', '?')} "
            f"cached_tokens={usage.get('input_tokens_details', {}).get('cached_tokens', 0)}\n"
        )


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
        merged: list[Section] = []
        seen_urls: set[str] = set()
        for chunk in chunk_entries(entries, cfg["chunk"]["max_tokens"]):
            for section in classify_with_ai(chunk, prompt, cfg):
                items = [i for i in section.items if i.get("url") not in seen_urls]
                seen_urls.update(i["url"] for i in items)
                existing = next((m for m in merged if m.name == section.name), None)
                if existing:
                    existing.items.extend(items)
                else:
                    merged.append(Section(name=section.name, items=items))
        return merged, False
    except Exception as err:
        logger.error("AI 分类失败，降级按来源分组: %s", err)
        return fallback_by_source(entries, cfg), True
