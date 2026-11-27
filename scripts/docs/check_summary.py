"""Every documentation page is in exactly one book's navigation.

mdBook publishes only the pages a SUMMARY.md lists, so an unlisted page would exist in
the repository and silently never reach the site (spec 001 D-004).

Books: docs/user/** is the user book, docs/privacy/** the privacy book, and the rest of
docs/ the contributor book. docs/_templates/ and docs/site/ are in no book by rule. A
SUMMARY.md entry for a missing file is left to mdBook (create-missing = false).

Usage: python scripts/docs/check_summary.py [root]   (default: the repository)
"""

import posixpath
import re
import sys
from pathlib import Path

# Longest prefix first: a page belongs to the first book whose directory holds it.
BOOKS = ("docs/user/", "docs/privacy/", "docs/")
UNPUBLISHED = ("docs/_templates/", "docs/site/")
LINK = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")


def book_of(page: str) -> str:
    return next(book for book in BOOKS if page.startswith(book))


def listed(root: Path, book: str) -> set[str]:
    """The repository path of every page the book's SUMMARY.md links."""
    summary = root / book / "SUMMARY.md"
    if not summary.is_file():
        return set()
    text = summary.read_text(encoding="utf-8")
    return {posixpath.normpath(book + target) for target in LINK.findall(text)}


def problems(root: Path) -> list[str]:
    if not (root / "docs/SUMMARY.md").is_file():
        return ["docs/SUMMARY.md is missing"]
    navigation = {book: listed(root, book) for book in BOOKS}
    found = []
    for path in sorted((root / "docs").rglob("*.md")):
        page = path.relative_to(root).as_posix()
        if page.startswith(UNPUBLISHED) or page.endswith("/SUMMARY.md"):
            continue
        own = book_of(page)
        books = [book for book in BOOKS if page in navigation[book]]
        if not books:
            found.append(f"{page} is in no SUMMARY.md; add it to {own}SUMMARY.md")
        elif len(books) > 1:
            found.append(f"{page} is in {len(books)} books; list it only in {own}SUMMARY.md")
        elif books != [own]:
            found.append(f"{page} is in {books[0]}SUMMARY.md; move it to {own}SUMMARY.md")
    return found


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
    found = problems(root)
    for problem in found:
        print(f"docs-summary: {problem}", file=sys.stderr)
    if found:
        print(f"docs-summary: {len(found)} page(s) misplaced in navigation", file=sys.stderr)
        return 1
    print("docs-summary: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
