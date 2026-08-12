"""DeepSeek API 调用（模式与 tech_news 一致，独立实现）。"""
import json
import logging
import os
from datetime import datetime
from pathlib import Path

import requests

logger = logging.getLogger("tech_wiki.ai")


def _api_key(rules: dict) -> str:
    if os.environ.get("DEEPSEEK_API_KEY"):
        return os.environ["DEEPSEEK_API_KEY"]
    auth = Path.home() / ".codex/auth.json"
    if auth.exists():
        return json.loads(auth.read_text())["OPENAI_API_KEY"]
    raise RuntimeError("无 API key")


def _cost_log() -> Path:
    return Path(__file__).parent / ".raw" / "cost.log"


def _write_cost_log(model: str, usage: dict) -> None:
    log = _cost_log()
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as f:
        f.write(
            f"{datetime.now().isoformat()} model={model} "
            f"input_tokens={usage.get('input_tokens', '?')} "
            f"output_tokens={usage.get('output_tokens', '?')} "
            f"cached_tokens={usage.get('input_tokens_details', {}).get('cached_tokens', 0)}\n"
        )


def _extract_text(data: dict) -> str:
    texts = []
    for out in data.get("output", []):
        for content in out.get("content", []):
            if isinstance(content, dict) and content.get("type") == "output_text":
                texts.append(content.get("text", ""))
    joined = "".join(texts).strip()
    if joined:
        return joined
    for out in data.get("output", []):
        for content in out.get("content", []):
            if isinstance(content, dict) and content.get("type") == "reasoning_text":
                text = content.get("text", "")
                start, end = text.find("{"), text.rfind("}")
                if start != -1 and end > start:
                    return text[start:end + 1]
    return ""


def ai_call(messages: list[dict], rules: dict) -> str:
    model = rules.get("model", {}).get("primary", "deepseek-v4-flash")
    base = rules.get("model", {}).get("api_base", "https://api.deepseek.com/v1/responses")
    resp = requests.post(
        base,
        json={"model": model, "input": messages},
        headers={"Authorization": f"Bearer {_api_key(rules)}"},
        timeout=180,
    )
    resp.raise_for_status()
    data = resp.json()
    text = _extract_text(data)
    if not text:
        raise RuntimeError("AI 响应无文本")
    _write_cost_log(model, data.get("usage", {}))
    return text


def ai_json(prompt: str, user_content: str, rules: dict) -> dict:
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_content},
    ]
    text = ai_call(messages, rules)
    try:
        return json.loads(text)
    except json.JSONDecodeError as err:
        retry_content = (
            f"{user_content}\n\n【上次输出不是合法 JSON，错误：{err}。"
            f"请只输出合法 JSON。上次输出：{text[:200]}】"
        )
        text = ai_call(
            [
                {"role": "system", "content": prompt},
                {"role": "user", "content": retry_content},
            ],
            rules,
        )
        try:
            return json.loads(text)
        except json.JSONDecodeError as err2:
            raise RuntimeError(f"AI 返回非 JSON: {err2}") from err2
