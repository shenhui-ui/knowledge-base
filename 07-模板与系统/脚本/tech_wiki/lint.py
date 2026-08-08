"""体检：只报告不修改。"""
import re
import time
from pathlib import Path

from rules import load_rules


def lint_index(vault_root: Path, rules: dict) -> list[str]:
    reports: list[str] = []
    index_path = vault_root / rules["wiki"]["index"]
    entries: list[str] = []
    if index_path.exists():
        for line in index_path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"- \[\[(.+?)\]\]", line)
            if m:
                entries.append(m.group(1))
    for name in entries:
        if not list(vault_root.rglob(f"{name}.md")):
            reports.append(f"[MISSING] {name}")
    for area in rules["wiki"]["writable"]:
        area_path = vault_root / area
        if not area_path.exists():
            continue
        for f in sorted(area_path.rglob("*.md")):
            rel = f.relative_to(vault_root)
            if "MOC" in str(rel) or ".模板" in str(rel):
                continue
            if f.stem not in entries:
                reports.append(f"[未收录] {rel}")
    inbox = vault_root / "00-收件箱"
    if inbox.exists():
        for f in sorted(inbox.glob("*.md")):
            age_days = (time.time() - f.stat().st_mtime) / 86400
            if age_days > 7:
                reports.append(f"[滞留] {f.name} ({int(age_days)}天)")
    return reports


if __name__ == "__main__":
    vault = Path(__file__).parent.parents[2]  # Obsidian
    for line in lint_index(vault, load_rules(vault)):
        print(line)
