---
status: accepted
date: 2026-10-26
decision-makers: owner (lvndrpup)
---

# Record architecture decisions as MADR ADRs

## Context and Problem Statement

Vocal Wren is built by one part-time developer working with AI agents. Context is lost
between sessions, and the constitution (principle XI) requires decisions to be written
down. How should we record them?

## Decision Drivers

* Constitution principle XI (decisions recorded)
* Readable by the owner and by agents without extra tooling
* Lives next to the code and is reviewed in pull requests

## Considered Options

* MADR 4 Markdown files in `docs/adr/`
* Free-form notes in the README or a wiki
* No formal record

## Decision Outcome

Chosen option: "MADR 4 Markdown files in `docs/adr/`", because it is a lightweight,
widely used template that fits plain Markdown review in pull requests.

Rules:

* Files are named `NNNN-title-with-dashes.md`, numbered sequentially from `0000`.
* Agents may write ADRs but always with status **Proposed**. Only the owner changes the
  status to Accepted, Rejected, Deprecated or Superseded.
* Merging the pull request that adds an ADR accepts it (owner, 2026-10-29). A merged ADR
  is Accepted whatever its status line says; the next change that touches `docs/adr/`
  sets the line to `accepted`.
* Loosening any oracle tolerance (principle X) requires an ADR.
* A superseded ADR is kept and links to the ADR that replaces it.

### Consequences

* Good, because decisions and their reasons survive between sessions and agents.
* Good, because ADRs are reviewed in the same PR flow as code.
* Bad, because writing an ADR adds a small cost to each significant decision.

## More Information

* MADR: <https://adr.github.io/madr/>
* [Constitution](../constitution.md), principle XI
