import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import pytest
from rules import extract_rules_block, is_writable, load_rules

BLOCK = """<!-- rules:wiki:start -->
```yaml
wiki:
  index: "07-模板与系统/MOC/索引.md"
  log: "07-模板与系统/MOC/操作日志.md"
  writable:
    - "03-软件开发"
    - "07-模板与系统/MOC/索引.md"
  readonly:
    - "00-收件箱"
  manual_marker: "@manual"
  screen_rules: ["a", "b"]
  digest_rules: ["c"]
```
<!-- rules:wiki:end -->"""

AGENTS_SAMPLE = f"""# 自生长知识库
说明文本…
{BLOCK}
"""


def test_extract_rules_block():
    assert "yaml" in extract_rules_block(AGENTS_SAMPLE)


def test_load_rules(tmp_path):
    (tmp_path / "AGENTS.md").write_text(AGENTS_SAMPLE, encoding="utf-8")
    rules = load_rules(tmp_path)
    assert rules["wiki"]["index"] == "07-模板与系统/MOC/索引.md"
    assert "@manual" in rules["wiki"]["manual_marker"]


def test_load_rules_missing_block_raises(tmp_path):
    (tmp_path / "AGENTS.md").write_text("# 无规则块", encoding="utf-8")
    with pytest.raises(ValueError):
        load_rules(tmp_path)


def test_load_rules_bad_yaml_raises(tmp_path):
    bad = "# x\n<!-- rules:wiki:start -->\n```yaml\nwiki: [unclosed\n```\n<!-- rules:wiki:end -->"
    (tmp_path / "AGENTS.md").write_text(bad, encoding="utf-8")
    with pytest.raises(ValueError):
        load_rules(tmp_path)


def test_is_writable(tmp_path):
    rules = {"wiki": {"writable": ["03-软件开发", "07-模板与系统/MOC/索引.md"], "readonly": ["00-收件箱"]}}
    assert is_writable(tmp_path / "03-软件开发/a.md", rules)
    assert is_writable(tmp_path / "07-模板与系统/MOC/索引.md", rules)
    assert not is_writable(tmp_path / "00-收件箱/x.md", rules)
    assert not is_writable(tmp_path / "08-其他/y.md", rules)
