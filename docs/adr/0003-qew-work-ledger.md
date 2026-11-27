---
status: accepted
date: 2026-10-26
decision-makers: owner (lvndrpup)
---

# Track work with the qew ledger

## Context and Problem Statement

Work is done by the owner and by AI agents, often in parallel. We need one place that says
what work exists, what is ready, who has claimed it and what evidence shows it is done.
Where does that live?

## Decision Drivers

* One source of truth for work that agents can query and update safely
* The owner keeps control of approval and merging
* Work visible on GitHub for anyone following the project

## Considered Options

* qew ledger in a sibling repository, mirrored to GitHub issues
* A `docs/ledger.md` file in this repository
* GitHub issues and projects only

## Decision Outcome

Chosen option: "qew ledger in a sibling repository, mirrored to GitHub issues", because
it gives agents a structured workflow (`qew ready`, `start`, `evidence`, `complete`,
`create`, `pr open`) while keeping ledger history separate from code history.

* The ledger lives in [`vocal_wren-ledger`](https://github.com/lvndrpup/vocal_wren-ledger),
  checked out at `../vocal_wren-ledger` (configured in `.qew/config.toml`).
* It is mirrored to GitHub issues on `lvndrpup/vocal_wren`. The mirror is output: nobody
  edits mirrored issues directly.
* Pull requests are opened with `qew pr open`. Commits carry `Refs: <qew id>`.
* This replaces the planned `docs/ledger.md` file; no such file is kept.

### Consequences

* Good, because ready, claimed and done states are explicit, and agents can't silently
  skip steps.
* Good, because code history stays free of bookkeeping commits.
* Bad, because contributors need qew installed and the sibling repo checked out.

## More Information

* qew: <https://github.com/foundlings/qew>
* [CLAUDE.md](https://github.com/lvndrpup/vocal_wren/blob/main/CLAUDE.md) for the agent workflow
