"""四阶段 ingest 管线：收集→筛选→消化→发布。"""
import contextlib
import fcntl
import logging
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

from ai import ai_json
from fetch import fetch_article
from rules import is_writable, load_rules

logger = logging.getLogger("tech_wiki.ingest")

BASE_DIR = Path(__file__).parent
VAULT_ROOT = BASE_DIR.parents[2]  # tech_wiki -> 脚本 -> 07-模板与系统 -> Obsidian


def insert_sorted(index_text: str, entry: str) -> str:
    lines = index_text.splitlines(keepends=True)
    entry_line = entry if entry.endswith("\n") else entry + "\n"
    if any(l.strip() == entry.strip() for l in lines):
        return index_text
    target = entry.strip()
    for i, line in enumerate(lines):
        if line.strip() and line.strip() > target:
            lines.insert(i, entry_line)
            return "".join(lines)
    return "".join(lines) + entry_line


def _parse_daily(daily_path: Path) -> list[dict]:
    text = daily_path.read_text(encoding="utf-8")
    items = []
    seen = set()
    for pat in (
        r"- \[([^\]]+)\]\((https?://[^)]+)\)",
        r"- (.+?) \[↗\]\((https?://[^)]+)\)",
        r"## \[([^\]]+)\]\((https?://[^)]+)\)",
    ):
        for m in re.finditer(pat, text):
            url = m.group(2).strip()
            if not url or url in seen:
                continue
            seen.add(url)
            items.append({
                "kind": "daily",
                "title": m.group(1).strip(),
                "url": url,
                "summary": "",
                "text": "",
                "source_path": None,
            })
    return items


def collect_candidates(inbox: Path, daily_dir: Path, yesterday: str, now: float, rules: dict) -> tuple[list[dict], list[Path]]:
    marker = rules["wiki"]["manual_marker"]
    candidates: list[dict] = []
    moved: list[Path] = []
    if inbox.exists():
        for f in sorted(inbox.glob("*.md")):
            if marker in f.name:
                continue
            if now - f.stat().st_mtime < 3600:
                continue
            candidates.append({
                "kind": "inbox",
                "title": f.stem,
                "url": "",
                "summary": "",
                "text": f.read_text(encoding="utf-8")[:10000],
                "source_path": f,
            })
            moved.append(f)
    for pattern in (f"科技资讯 {yesterday}.md", f"AI 早报 {yesterday}.md"):
        p = daily_dir / yesterday[:7] / pattern
        if p.exists():
            candidates.extend(_parse_daily(p))
    return candidates, moved


def screen(candidates: list[dict], rules: dict) -> tuple[list[dict], str]:
    if not candidates:
        return [], "无候选"
    screen_rules = "\n".join(f"- {r}" for r in rules.get("wiki", {}).get("screen_rules", []))
    prompt = (
        "你是知识库筛选器。按以下筛选规则评估候选条目，只保留值得沉淀进 wiki 的：\n"
        f"{screen_rules}\n"
        '输出严格 JSON：{"keep": [{"index": 0, "reason": "…"}]}，index 对应输入数组下标。'
    )
    payload = []
    for i, c in enumerate(candidates):
        payload.append({"index": i, "title": c["title"], "summary": c.get("summary", "")[:200]})
    try:
        result = ai_json(prompt, str(payload), rules)
        kept_idx = set()
        for item in result.get("keep", []):
            if isinstance(item, dict) and "index" in item:
                kept_idx.add(item["index"])
            elif isinstance(item, int):
                kept_idx.add(item)
            elif isinstance(item, str) and item.isdigit():
                kept_idx.add(int(item))
        kept = [c for i, c in enumerate(candidates) if i in kept_idx]
        note = f"筛选: 保留 {len(kept)}/{len(candidates)}"
        return kept, note
    except Exception as err:
        logger.error("筛选失败降级: %s", err)
        return [], f"筛选失败降级: {err}"


def build_digest_prompt(rules: dict) -> str:
    digest_rules = "\n".join(f"- {r}" for r in rules["wiki"].get("digest_rules", []))
    writable_dirs = "\n".join(f"- {d}" for d in rules["wiki"].get("writable", []) if not d.endswith(".md"))
    return (
        "你是知识库编辑。根据索引与素材，决定合并到已有文章或新建文章。\n"
        f"消化规则：\n{digest_rules}\n"
        f"可写目标目录（target 必须位于以下其一之下，相对 vault 根）：\n{writable_dirs}\n"
        '输出严格 JSON：{"action": "merge|create", "target": "相对vault路径.md", "title": "文章标题", "content": "markdown正文"}。'
    )


class EmptyMaterialError(Exception):
    """素材为空（含抓取失败），跳过该条目。"""


def _resolve_target(raw: str, rules: dict, vault_root: Path) -> Path:
    target = (vault_root / raw.lstrip("/")).resolve()
    vault = vault_root.resolve()
    if vault not in target.parents and target != vault:
        raise ValueError(f"AI 目标越出 vault 边界: {target}")
    for key in ("index", "log"):
        sys_raw = rules["wiki"].get(key)
        if sys_raw and target == (vault / sys_raw).resolve():
            raise ValueError("禁止覆盖系统文件")
    if not is_writable(target, rules):
        raise ValueError(f"AI 目标不在可写区: {target}")
    return target


def _normalize_frontmatter(content: str, url: str) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    if not content.startswith("---"):
        return f"---\ntype: ingest-note\nsource: {url}\ndate: {today}\n---\n" + content
    lines = content.split("\n")
    close_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            close_idx = i
            break
    if close_idx is None:
        content = content.rstrip("\n") + "\n---\n"
        lines = content.split("\n")
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                close_idx = i
                break
    existing = set()
    for line in lines[1:close_idx]:
        m = re.match(r"^([A-Za-z_]\w*)\s*:", line.strip())
        if m:
            existing.add(m.group(1))
    inserts = []
    if "type" not in existing:
        inserts.append("type: ingest-note")
    if "source" not in existing:
        inserts.append(f"source: {url}")
    if "date" not in existing:
        inserts.append(f"date: {today}")
    if not inserts:
        return content
    fm = "\n".join(lines[1:close_idx] + inserts)
    body = "\n".join(lines[close_idx + 1:])
    return f"---\n{fm}\n---\n" + (body + "\n" if body else "")


def digest(item: dict, rules: dict, vault_root: Path) -> Path:
    body = item.get("text") or ""
    if not body and item.get("url"):
        body = fetch_article(item["url"], rules)
    if not body.strip():
        raise EmptyMaterialError(f"跳过空素材: {item.get('title', '')}")
    index_path = vault_root / rules["wiki"]["index"]
    index_text = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    prompt = build_digest_prompt(rules)
    user = f"索引:\n{index_text[:3000]}\n\n素材:\n{body[:6000]}"
    result = ai_json(prompt, user, rules)
    target = _resolve_target(result["target"], rules, vault_root)
    if target.exists():
        existing = target.read_text(encoding="utf-8")[:2000]
        merge_user = f"索引:\n{index_text[:3000]}\n\n已有文章内容:\n{existing}\n\n素材:\n{body[:6000]}"
        result = ai_json(prompt, merge_user, rules)
        target = _resolve_target(result["target"], rules, vault_root)
    target.parent.mkdir(parents=True, exist_ok=True)
    content = _normalize_frontmatter(result["content"], item.get("url") or "")
    target.write_text(content, encoding="utf-8")
    return target


def publish(article: Path, rules: dict, vault_root: Path) -> None:
    index_path = vault_root / rules["wiki"]["index"]
    log_path = vault_root / rules["wiki"]["log"]
    index_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not index_path.exists():
        index_path.write_text("# 知识库索引\n\n", encoding="utf-8")
    entry = f"- [[{article.stem}]]"
    index_path.write_text(insert_sorted(index_path.read_text(encoding="utf-8"), entry), encoding="utf-8")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"- {now} ingest 消化 {article.relative_to(vault_root)} → 索引更新\n")


@contextlib.contextmanager
def acquire_lock(lock_path: Path):
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def run_pipeline(vault_root: Path) -> str:
    rules = load_rules(vault_root)
    inbox = vault_root / "00-收件箱"
    daily_dir = vault_root / "02-资讯日报" / "日报"
    yesterday = (datetime.now().date() - timedelta(days=1)).strftime("%Y-%m-%d")
    return _run(vault_root, rules, inbox, daily_dir, yesterday, time.time())


def _run(vault_root: Path, rules: dict, inbox: Path, daily_dir: Path, yesterday: str, now: float) -> str:
    candidates, _ = collect_candidates(inbox, daily_dir, yesterday, now, rules)
    if not candidates:
        return "无候选素材"
    inbox_cands = [c for c in candidates if c["kind"] == "inbox"]
    daily_cands = [c for c in candidates if c["kind"] == "daily"]
    lines = []
    if daily_cands:
        kept, note = screen(daily_cands, rules)
        lines.append(note)
    else:
        kept, note = [], ""
    kept = inbox_cands + kept
    archived = 0
    for item in kept:
        try:
            article = digest(item, rules, vault_root)
            publish(article, rules, vault_root)
            lines.append(f"消化: {item['title']} → {article.relative_to(vault_root)}")
            if item["kind"] == "inbox":
                src = item.get("source_path")
                if src is not None and src.exists():
                    archive = vault_root / "99-归档"
                    archive.mkdir(parents=True, exist_ok=True)
                    src.rename(archive / src.name)
                    archived += 1
        except EmptyMaterialError as err:
            lines.append(str(err))
        except Exception as err:
            logger.error("消化失败 %s: %s", item.get("title"), err)
            lines.append(f"消化失败: {item.get('title')} ({err})")
    if archived:
        lines.append(f"收件箱归档: {archived} 个文件移入 99-归档/")
    return "\n".join(lines)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    with acquire_lock(BASE_DIR / ".raw" / "ingest.lock"):
        print(run_pipeline(VAULT_ROOT))
