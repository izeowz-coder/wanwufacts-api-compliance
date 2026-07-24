from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = [
    ROOT / "index.html",
    ROOT / "privacy.html",
    ROOT / "terms.html",
    ROOT / "data-deletion.html",
]


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.titles: list[str] = []
        self.descriptions = 0
        self.scripts = 0
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.links.append(str(values["href"]))
        if tag == "link" and values.get("href"):
            self.links.append(str(values["href"]))
        if tag == "meta" and values.get("name") == "description" and values.get("content"):
            self.descriptions += 1
        if tag == "script":
            self.scripts += 1
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.titles.append(data.strip())


def local_target(page: Path, href: str) -> Path | None:
    if href.startswith(("#", "mailto:", "tel:")):
        return None
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc:
        return None
    path = parsed.path
    if not path:
        return None
    return (page.parent / path).resolve()


all_text = ""
for page in HTML_FILES:
    assert page.exists(), f"missing page: {page}"
    text = page.read_text(encoding="utf-8")
    all_text += text
    parser = Links()
    parser.feed(text)
    assert parser.titles and any(parser.titles), f"missing title: {page.name}"
    assert parser.descriptions == 1, f"missing description: {page.name}"
    assert parser.scripts == 0, f"unexpected script: {page.name}"
    for href in parser.links:
        target = local_target(page, href)
        if target is not None:
            assert target.exists(), f"broken local link in {page.name}: {href}"

privacy = (ROOT / "privacy.html").read_text(encoding="utf-8")
for required in (
    "https://www.youtube.com/t/terms",
    "https://policies.google.com/privacy",
    "https://security.google.com/settings/security/permissions",
    "YouTube API Services",
    "seven calendar days",
    "30 days",
):
    assert required in privacy, f"privacy policy missing: {required}"

for expected in (
    ROOT / "evidence" / "audit-evidence-complete.pdf",
    ROOT / "evidence" / "01-homepage-and-overview.pdf",
    ROOT / "evidence" / "02-privacy-policy.pdf",
    ROOT / "evidence" / "03-terms-of-use.pdf",
    ROOT / "evidence" / "04-oauth-and-upload-flow.pdf",
    ROOT / "evidence" / "05-architecture.pdf",
):
    assert expected.exists() and expected.stat().st_size > 1000, f"invalid PDF: {expected.name}"

secret_patterns = (
    r"\bAIza[0-9A-Za-z_-]{20,}\b",
    r"\bya29\.[0-9A-Za-z_-]{20,}\b",
    r"\b1//[0-9A-Za-z_-]{20,}\b",
    r"\bGOCSPX-[0-9A-Za-z_-]{10,}\b",
)
for pattern in secret_patterns:
    assert not re.search(pattern, all_text), f"possible secret matched: {pattern}"

print(f"Validated {len(HTML_FILES)} pages, internal links, policies, PDFs and secret scan")
