"""The built docs site loads nothing from the network (spec 001 D-006).

A browser fetches a remote resource on page load from these references, so the check
fails on any that is http(s):// or protocol-relative (//host/...):
  - in HTML: the src and poster of any element, any srcset candidate, the data of
    <object>, the href of <link>, and the href or xlink:href of SVG <image>, <use> and
    <feImage>;
  - in CSS, and anywhere in HTML (so <style> and style="" too): url() and @import.
Links (<a href>) load nothing until followed, and data: URIs load nothing, so both pass.

Usage: python scripts/docs/check_remote.py <dir>   (a built site, e.g. build/site)
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

REMOTE = re.compile(r"\s*(https?:)?//", re.IGNORECASE)
URL = re.compile(r"url\(\s*[\"']?\s*((?:https?:)?//[^)\"'\s]*)", re.IGNORECASE)
IMPORT = re.compile(r"@import\s*(?:url\(\s*)?[\"']?\s*((?:https?:)?//[^\"')\s]*)", re.IGNORECASE)
SVG_REFS = {"image", "use", "feimage"}


class _Refs(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.found: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if value is None:
                continue
            loads = (
                name in ("src", "poster")
                or (tag == "object" and name == "data")
                or (tag == "link" and name == "href")
                or (tag in SVG_REFS and name in ("href", "xlink:href"))
            )
            if loads and REMOTE.match(value):
                self.found.append(f"<{tag}> {name} {value.strip()}")
            elif name == "srcset" and any(REMOTE.match(c) for c in value.split(",")):
                self.found.append(f"<{tag}> srcset {value.strip()}")

    handle_startendtag = handle_starttag


def remote_refs(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    found = []
    if path.suffix == ".html":
        parser = _Refs()
        parser.feed(text)
        found += parser.found
    found += [f"url() {m}" for m in URL.findall(text)]
    found += [f"@import {m}" for m in IMPORT.findall(text)]
    return found


def problems(site: Path) -> tuple[list[str], int]:
    files = sorted(p for p in site.rglob("*") if p.suffix in (".html", ".css"))
    if not any(p.suffix == ".html" for p in files):
        return [f"no HTML under {site}; build the site first"], 0
    return [f"{p.relative_to(site).as_posix()} loads {ref}" for p in files for ref in remote_refs(p)], len(files)


def main() -> int:
    if len(sys.argv) != 2 or not Path(sys.argv[1]).is_dir():
        print("usage: python scripts/docs/check_remote.py <built site dir>", file=sys.stderr)
        return 2
    found, count = problems(Path(sys.argv[1]))
    for problem in found:
        print(f"docs-remote: {problem}", file=sys.stderr)
    if found:
        print(f"docs-remote: {len(found)} problem(s); the site must load nothing from the network", file=sys.stderr)
        return 1
    print(f"docs-remote: ok ({count} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
