"""AGENTS.md rules:wiki 块解析——规则单一事实来源。"""
import re
from pathlib import Path

import yaml

START = "<!-- rules:wiki:start -->"
END = "<!-- rules:wiki:end -->"


def extract_rules_block(text: str) -> str:
    start = text.find(START)
    end = text.find(END)
    if start == -1 or end == -1 or end <= start:
        raise ValueError("AGENTS.md 缺少 rules:wiki 块标记")
    return text[start + len(START):end]


def load_rules(vault_root: Path) -> dict:
    agents = Path(vault_root) / "AGENTS.md"
    if not agents.exists():
        raise ValueError(f"AGENTS.md 不存在: {agents}")
    block = extract_rules_block(agents.read_text(encoding="utf-8"))
    yaml_match = re.search(r"```yaml\s*\n(.*?)```", block, re.DOTALL)
    if not yaml_match:
        raise ValueError("rules:wiki 块内缺少 ```yaml 代码块")
    try:
        rules = yaml.safe_load(yaml_match.group(1))
    except yaml.YAMLError as err:
        raise ValueError(f"rules:wiki YAML 解析失败: {err}") from err
    if not isinstance(rules, dict) or "wiki" not in rules:
        raise ValueError("rules:wiki YAML 顶层必须是 wiki 键")
    return rules


def is_writable(path: Path, rules: dict) -> bool:
    parts = list(Path(path).resolve().parts)
    for entry in rules["wiki"]["writable"]:
        entry_parts = [part for part in Path(entry).parts if part not in ("/", ".")]
        if len(entry_parts) > len(parts):
            continue
        for i in range(len(parts) - len(entry_parts) + 1):
            if parts[i:i + len(entry_parts)] == entry_parts:
                return True
    return False
