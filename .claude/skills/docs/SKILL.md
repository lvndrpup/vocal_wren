---
name: "docs"
description: "Write or change a page under docs/: pick the part and kind, copy the template, place it in navigation, write, check. Use before adding or editing any documentation page."
---

# Writing a docs page

The steps for an agent writing documentation. Every rule lives in
[`docs/how-to/write-docs.md`](../../../docs/how-to/write-docs.md); this file only orders
the work and links there. Where the two seem to disagree, the guide wins and this file is
the bug.

1. **Part**: decide contributor guide, Learn or user guide
   ([guide, step 1](../../../docs/how-to/write-docs.md#1-pick-the-part)). A fact both
   contributors and users need gets two pages.
2. **Kind**: pick one page kind and its folder
   ([step 2](../../../docs/how-to/write-docs.md#2-pick-the-kind)). Editing an existing
   page: keep its kind; if the change needs another kind, write a second page instead.
3. **Template**: copy it from `docs/_templates/`
   ([step 3](../../../docs/how-to/write-docs.md#3-copy-the-template)).
4. **Navigation**: add the page to its book's `SUMMARY.md`
   ([step 4](../../../docs/how-to/write-docs.md#4-place-it-in-the-navigation)).
5. **Write**: apply [the rules](../../../docs/how-to/write-docs.md#the-rules) for every
   page, for repo IDs in the page's part, and for the part from step 1. Then reread the
   page as that reader.
6. **Check**: run `python scripts/docs/build_site.py`
   ([step 6](../../../docs/how-to/write-docs.md#6-check)) and fix what it names.
7. **Propose**: commit with a `Refs: <qew id>` trailer and open the pull request with
   `qew pr open` (`CLAUDE.md`). The owner reviews and merges.
