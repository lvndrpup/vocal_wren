"""Build the docs site into build/site/ and run every docs check, locally and in CI.

Downloads the pinned mdBook and lychee release binaries into build/tools/ on first use,
checking each against its SHA-256, so no Rust toolchain is needed (spec 001 D-001).

Layout (spec 001 plan, Architecture):
  build/site/index.html   landing page, from docs/site/index.html
  build/site/dev/         contributor book (book.toml), with Dokka HTML for :core in api/
  build/site/guide/       user book, once docs/user/book.toml exists
  build/site/privacy/     privacy book, once docs/privacy/book.toml exists

Usage: python scripts/docs/build_site.py
"""

import hashlib
import io
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "build/site"
TOOLS = ROOT / "build/tools"

MDBOOK = "0.5.4"
LYCHEE = "0.24.2"
# (tool, OS) -> (release asset URL, SHA-256). Hashes from the GitHub releases API, 2026-10-29.
DOWNLOADS = {
    ("mdbook", "Linux"): (
        f"https://github.com/rust-lang/mdBook/releases/download/v{MDBOOK}/mdbook-v{MDBOOK}-x86_64-unknown-linux-gnu.tar.gz",
        "3f28de05dafca9d0f2eab99c662116b0e37b89b1d96a08f8f430b9eeae958cd7"),
    ("mdbook", "Windows"): (
        f"https://github.com/rust-lang/mdBook/releases/download/v{MDBOOK}/mdbook-v{MDBOOK}-x86_64-pc-windows-msvc.zip",
        "8a6b2421aa522de06d746871d2b8fff9c8d71773467e310a4516d2566e7f2de4"),
    ("lychee", "Linux"): (
        f"https://github.com/lycheeverse/lychee/releases/download/lychee-v{LYCHEE}/lychee-x86_64-unknown-linux-gnu.tar.gz",
        "1f4e0ef7f6554a6ed33dd7ac144fb2e1bbed98598e7af973042fc5cd43951c9a"),
    ("lychee", "Windows"): (
        f"https://github.com/lycheeverse/lychee/releases/download/lychee-v{LYCHEE}/lychee-x86_64-pc-windows-msvc.zip",
        "32975d1493ee1a975d6bb41e4fb56fe419cb442ded628bb772ba2e614acfacad"),
}
VERSIONS = {"mdbook": MDBOOK, "lychee": LYCHEE}


def tool(name: str) -> Path:
    """The pinned binary, downloaded and checked on first use."""
    exe = name + (".exe" if os.name == "nt" else "")
    path = TOOLS / f"{name}-{VERSIONS[name]}" / exe
    if path.is_file():
        return path
    key = (name, platform.system())
    if key not in DOWNLOADS:
        sys.exit(f"docs: no pinned {name} for {key[1]}; add one to DOWNLOADS in {Path(__file__).name}")
    url, sha256 = DOWNLOADS[key]
    print(f"docs: downloading {url}")
    with urllib.request.urlopen(url) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != sha256:
        sys.exit(f"docs: {url} does not match its pinned SHA-256; refusing to use it")
    if url.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            member = next(n for n in archive.namelist() if Path(n).name == exe)
            binary = archive.read(member)
    else:
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:
            member = next(m for m in archive.getmembers() if Path(m.name).name == exe)
            binary = archive.extractfile(member).read()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(binary)
    path.chmod(0o755)
    return path


def run(*command: str | Path, cwd: Path = ROOT) -> None:
    print("docs: $ " + " ".join(str(part) for part in command), flush=True)
    if subprocess.run([str(part) for part in command], cwd=cwd).returncode != 0:
        sys.exit(f"docs: failed: {Path(command[0]).name}")


def proposed_adrs(root: Path) -> list[str]:
    """ADRs whose status line still says proposed; on main, merging already accepted them."""
    return [p.relative_to(root).as_posix() for p in sorted((root / "docs/adr").glob("*.md"))
            if re.search(r"^status:\s*proposed\b", p.read_text(encoding="utf-8"), re.I | re.M)]


def main() -> int:
    python = sys.executable
    run(python, "-m", "unittest", "discover", "-s", ROOT / "scripts/docs")
    mdbook, lychee = tool("mdbook"), tool("lychee")
    shutil.rmtree(SITE, ignore_errors=True)

    run(mdbook, "build")
    # mdBook copies every non-Markdown file under docs/ into the book; the landing page
    # belongs at the root, where its dev/ link resolves.
    shutil.rmtree(SITE / "dev/site")
    shutil.copy(ROOT / "docs/site/index.html", SITE / "index.html")

    gradlew = ROOT / "android" / ("gradlew.bat" if os.name == "nt" else "gradlew")
    run(gradlew, "-q", ":core:dokkaGenerate", cwd=ROOT / "android")
    shutil.copytree(ROOT / "android/core/build/dokka/html", SITE / "dev/api")

    for book in ("user", "privacy"):
        if (ROOT / f"docs/{book}/book.toml").is_file():
            run(mdbook, "build", f"docs/{book}")
            # The book's source is its own directory, so mdBook copies its book.toml too.
            for copied in SITE.glob("*/book.toml"):
                copied.unlink()

    run(python, ROOT / "scripts/docs/check_summary.py")
    run(python, ROOT / "scripts/docs/check_remote.py", SITE)
    # Offline: links leaving the site are not followed, so every machine gets the same answer.
    run(lychee, "--offline", "--include-fragments", "--no-progress", "--root-dir", SITE.resolve(), SITE)

    for adr in proposed_adrs(ROOT):
        print(f"docs: warning: {adr} says proposed; merging accepted it, so the next change to docs/adr/ sets it to accepted")
    print(f"docs: ok, site in {SITE.relative_to(ROOT).as_posix()}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
