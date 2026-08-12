import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import pytest
from ai import ai_call, ai_json


def _rules():
    return {"model": {"primary": "test-model", "api_base": "http://fake"}}


def test_ai_json_retries_after_bad_json(monkeypatch):
    import ai as ai_module

    calls = []

    def fake_call(messages, rules):
        calls.append(messages)
        if len(calls) == 1:
            return "这不是 JSON"
        return json.dumps({"action": "create", "target": "03-软件开发/x.md", "title": "x", "content": "# x"})

    monkeypatch.setattr(ai_module, "ai_call", fake_call)
    result = ai_json("系统提示", "用户内容", _rules())
    assert result["action"] == "create"
    assert len(calls) == 2
    assert calls[1][0] == {"role": "system", "content": "系统提示"}
    assert "不是合法 JSON" in calls[1][1]["content"]
    assert "上次输出" in calls[1][1]["content"]
    assert "这不是 JSON" in calls[1][1]["content"]


def test_ai_json_raises_after_retry_fails(monkeypatch):
    import ai as ai_module

    calls = []

    def fake_call(messages, rules):
        calls.append(messages)
        return "依然不是 JSON"

    monkeypatch.setattr(ai_module, "ai_call", fake_call)
    with pytest.raises(RuntimeError, match="非 JSON"):
        ai_json("系统提示", "用户内容", _rules())
    assert len(calls) == 2


def test_ai_call_writes_cost_log_with_cached_tokens(monkeypatch, tmp_path):
    import ai as ai_module

    class FakeResp:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "output": [
                    {"type": "message", "content": [{"type": "output_text", "text": '{"ok": true}'}]}
                ],
                "usage": {
                    "input_tokens": 100,
                    "output_tokens": 50,
                    "input_tokens_details": {"cached_tokens": 42},
                },
            }

    monkeypatch.setattr(ai_module.requests, "post", lambda *a, **kw: FakeResp())
    monkeypatch.setattr(ai_module, "_cost_log", lambda: tmp_path / "cost.log")
    text = ai_call([{"role": "user", "content": "hi"}], _rules())
    assert text == '{"ok": true}'
    content = (tmp_path / "cost.log").read_text(encoding="utf-8")
    assert "model=test-model" in content
    assert "input_tokens=100" in content
    assert "output_tokens=50" in content
    assert "cached_tokens=42" in content
