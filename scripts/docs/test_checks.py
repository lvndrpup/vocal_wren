"""Tests for the docs checks. Run: python -m unittest discover scripts/docs"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import build_site  # noqa: E402
import check_remote  # noqa: E402
import check_summary  # noqa: E402


def write(root: Path, files: dict[str, str]) -> None:
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


class SummaryTest(unittest.TestCase):
    def check(self, files: dict[str, str]) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            write(Path(tmp), files)
            return check_summary.problems(Path(tmp))

    def test_listed_pages_pass(self) -> None:
        self.assertEqual(self.check({
            "docs/SUMMARY.md": "[Start](README.md)\n- [A](learn/a.md#top)\n",
            "docs/README.md": "", "docs/learn/a.md": "",
            "docs/user/SUMMARY.md": "- [Hi](hi.md)\n", "docs/user/hi.md": "",
            "docs/_templates/page.md": "", "docs/site/notes.md": "",
        }), [])

    def test_unlisted_page_fails(self) -> None:
        found = self.check({"docs/SUMMARY.md": "", "docs/lost.md": ""})
        self.assertEqual(found, ["docs/lost.md is in no SUMMARY.md; add it to docs/SUMMARY.md"])

    def test_page_in_two_books_fails(self) -> None:
        found = self.check({
            "docs/SUMMARY.md": "- [Hi](user/hi.md)\n",
            "docs/user/SUMMARY.md": "- [Hi](hi.md)\n", "docs/user/hi.md": "",
        })
        self.assertEqual(found, ["docs/user/hi.md is in 2 books; list it only in docs/user/SUMMARY.md"])

    def test_page_in_wrong_book_fails(self) -> None:
        found = self.check({"docs/SUMMARY.md": "- [Hi](user/hi.md)\n", "docs/user/hi.md": ""})
        self.assertEqual(found, ["docs/user/hi.md is in docs/SUMMARY.md; move it to docs/user/SUMMARY.md"])

    def test_missing_contributor_summary_fails(self) -> None:
        self.assertEqual(self.check({"docs/a.md": ""}), ["docs/SUMMARY.md is missing"])


class RemoteTest(unittest.TestCase):
    def check(self, files: dict[str, str]) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            write(Path(tmp), files)
            return check_remote.problems(Path(tmp))[0]

    def test_local_references_and_links_pass(self) -> None:
        self.assertEqual(self.check({
            "index.html": '<a href="https://example.com">x</a><img src="a.png">'
                          '<img src="data:image/png;base64,AA"><link href="s.css">',
            "s.css": "body { background: url(a.png) } /* see https://example.com */",
        }), [])

    def test_remote_resources_fail(self) -> None:
        found = self.check({
            "index.html": '<script src="https://cdn.example/x.js"></script>'
                          "<link rel=stylesheet href='//fonts.example/f.css'>"
                          '<img srcset="a.png 1x, https://x.example/b.png 2x">'
                          '<svg><use xlink:href="https://x.example/i.svg#a"/></svg>'
                          '<object data="http://x.example/o"></object>'
                          '<div style="background: url(https://x.example/bg.png)"></div>',
            "s.css": '@import "https://x.example/more.css";',
        })
        self.assertEqual(len(found), 7, found)

    def test_empty_site_fails(self) -> None:
        self.assertEqual(len(self.check({"s.css": ""})), 1)


class AdrStatusTest(unittest.TestCase):
    def test_proposed_adr_is_named(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            write(Path(tmp), {
                "docs/adr/0001-a.md": "---\nstatus: proposed\n---\n",
                "docs/adr/0002-b.md": "---\nstatus: accepted\n---\n",
            })
            self.assertEqual(build_site.proposed_adrs(Path(tmp)), ["docs/adr/0001-a.md"])


if __name__ == "__main__":
    unittest.main()
