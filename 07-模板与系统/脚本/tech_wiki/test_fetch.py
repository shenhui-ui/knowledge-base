import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fetch import extract_main_text

HTML = """<html><head><title>T</title><script>var x=1;</script></head>
<body><nav>菜单</nav><article><h1>标题</h1><p>第一段内容。</p>
<p>第二段有 <a href='https://x'>链接</a> 与 <b>粗体</b>。</p></article>
<footer>版权</footer></body></html>"""


def test_extract_main_text_strips_tags():
    text = extract_main_text(HTML)
    assert "菜单" not in text
    assert "版权" not in text
    assert "var x=1" not in text
    assert "第一段内容" in text
    assert "粗体" in text


def test_extract_main_text_no_links_left():
    text = extract_main_text(HTML)
    assert "<a" not in text
    assert "<" not in text


def test_extract_main_text_truncates():
    long_html = "<html><body><p>" + "字" * 6000 + "</p></body></html>"
    text = extract_main_text(long_html)
    assert len(text) == 5000


def test_extract_main_text_empty():
    assert extract_main_text("<html><body></body></html>") == ""
