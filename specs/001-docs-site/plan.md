# Implementation Plan: A Documentation Site for Contributors, Learners and Users

**Branch**: `spec/001-docs-site` | **Date**: 2026-10-29 | **Status**: Accepted (merged in #29)
**Spec**: [spec.md](spec.md) · **Research**: [research.md](research.md) · **ADR**:
[ADR-0007](../../docs/adr/0007-docs-site.md) (Accepted)

## Summary

Publish `docs/` as a static site in two books. The contributor book holds the
contributor guide and Learn, so the people who read both get one sidebar. The user book
holds the user guide and FAQ. It is built and checked from its first page and published
from the M7 closed test, with a test-version banner until the M8 release. The `:core` API docs from Dokka sit beside the
contributor book. One writing guide, one template per page kind and a `docs` skill make
every author produce the same shape.

**Technically this is two mdBook books, one Dokka task, three small checks and one
workflow.** Nothing changes in `:app` or in `:core`'s code.

## Technical context

| Field | Value |
|---|---|
| Tools | mdBook 0.5.4 (MPL-2.0) and lychee 0.24.2 (Apache-2.0 OR MIT), both from release binaries pinned by version and SHA-256. Dokka 2.2.0 (Apache-2.0) as a Gradle plugin on `:core`, pinned in `libs.versions.toml` |
| Checks | Python 3, standard library only, under `scripts/docs/`, with `unittest` tests beside them. Python is already planned for the oracle (M2), so this adds no new toolchain, and it runs the same on the owner's Windows machine and on Ubuntu CI |
| Hosting | GitHub Pages, deployed by Actions from `main`, at `https://lvndrpup.github.io/vocal_wren/` |
| Constraints | No remote resources on page load (FR-013); byte-identical builds (FR-014); no docs tooling in the app binary (licensing constraint) |
| Scope | 19 existing pages (with PR #28); about 6 new contributor pages; a user-guide skeleton and FAQ |

No `data-model.md` or `contracts/`: the feature adds no types and no API.

## Constitution check

| Principle | Status |
|---|---|
| I On-device | ✅ Nothing in `:app` changes. The site sends no request on load (D-006) |
| II Measurement honesty | ✅ Learn keeps its sources; the user guide explains hidden metrics (spec US4) |
| III Targets, not identities | ✅ Writing guide and review (spec FR-035) |
| IV Not medical care | ✅ Writing guide and review (spec FR-034) |
| V Safety over progress | ✅ Not applicable |
| VI Encouragement, not coercion | ✅ Writing guide bans pressure wording in the user guide |
| VII Visual-first accessibility | ✅ Binds the app, not the site. The site follows the writing guide's accessibility rules, and the user book and privacy page meet WCAG 2.2 AA before they publish (D-016) |
| VIII Content as data | ✅ The user guide holds no coaching text (spec FR-033) |
| IX Shared core | ✅ Dokka is a build-time plugin on `:core`. It adds no runtime dependency and no Android dependency |
| X Test-first | ✅ Each check lands with its failing test first, in the same change |
| XI Decisions recorded | ✅ ADR-0007 (Accepted) records D-001, D-007, D-008 and D-011 |
| Licensing constraint | ✅ It bars GPL, AGPL and LGPL code from the app binary only. No docs tool or site asset reaches the binary. ADR-0007 lists every licence anyway (D-011) |

## Project structure

### This feature's documents

```text
specs/001-docs-site/
├── spec.md
├── plan.md        # this file
└── research.md
```

There is no `tasks.md`. The ledger items listed under [Phasing](#phasing) are the
tasks.

### Repository changes

```text
book.toml                       # contributor book: src = "docs", build-dir = "build/site/dev"
docs/SUMMARY.md                 # contributor navigation, hand-curated, path-ordered (D-004)
docs/README.md                  # NEW: the contributor book's landing page ("Start here")
docs/start/                     # NEW: status, setup, how the app is built
docs/how-to/write-docs.md       # NEW: the writing guide, the one home for doc rules (D-012)
docs/_templates/                # NEW: one template per page kind; left out of navigation by rule
docs/learn/, docs/reference/    # from PR #28, unchanged
docs/user/                      # NEW: the user book
docs/user/book.toml             #   src = ".", build-dir = "../../build/site/guide"
docs/user/SUMMARY.md
docs/privacy/                   # NEW: one-page book for the privacy policy (D-015)
docs/site/index.html            # NEW: landing page linking /dev/ and, after release, /guide/
android/gradle/libs.versions.toml   # + dokka version and plugin alias
android/core/build.gradle.kts       # + dokka plugin, stdlib and JDK links off (D-008)
scripts/docs/check_summary.py   # NEW: every page in exactly one navigation
scripts/docs/check_remote.py    # NEW: no remote resource references in the built site
scripts/docs/check_plain.py     # NEW: no repo IDs or code identifiers in the user book
scripts/docs/build_site.py      # NEW: builds both books and the API docs, runs every check
scripts/docs/test_*.py          # their tests
.github/workflows/docs.yml      # NEW: build on PR (artifact preview), deploy on main
.claude/skills/docs/SKILL.md    # NEW: procedure only; links to the writing guide
CLAUDE.md                       # + docs skill pointer; facts move to docs/ (D-013)
README.md                       # + link to the site; status moves to docs/start/status.md
.gitignore                      # + build/
```

**Structure decision**: two books, three parts (D-002). Learn and the contributor guide
share a book because they share readers: Learn's own index says it is written for the
owner and contributors. The user book lives under `docs/user/` so the contributor book's
`src = "docs"` keeps today's paths. The summary check assigns `docs/user/**` to the user
book, `docs/_templates/**` and `docs/site/**` to no book by rule, and everything else to
the contributor book.

## Architecture

### Published layout

```text
https://lvndrpup.github.io/vocal_wren/
├── index.html        landing page: "Using Wren" (after release) · "Contributing and Learn"
├── dev/              contributor book: Start here, Learn, How the project is run, Reference, Decisions
│   └── api/          Dokka HTML for :core
├── guide/            user book (published from the M7 closed test; D-003)
└── privacy/          privacy policy, its own one-page book (published once written; D-015)
```

The URLs are fixed from the first deploy, so the release adds `/guide/` without moving
anything.

### Contributor navigation (first cut)

```text
Start here                  docs/README.md
  Status                    docs/start/status.md       (the one status page, FR-015)
  Set up and build          docs/start/setup.md
  How the app is built      docs/start/architecture.md (:core vs :app, the audio path, why no INTERNET)
Learn                       docs/learn/README.md and its six pages, in its order
How the project is run
  Constitution              docs/constitution.md
  Roadmap                   docs/roadmap.md
  Open questions            docs/open-questions.md
  Work tracking with qew    docs/how-to/qew.md          (facts from CLAUDE.md and ADR-0003)
  Writing docs              docs/how-to/write-docs.md
Reference
  Glossary                  docs/reference/glossary.md
  API (:core)               → api/
  Salvage notes             docs/salvage/voice-trainer.md
Decisions
  ADRs                      docs/adr/*.md
```

### Build

```text
mdbook build                         ─▶ build/site/dev/
mdbook build docs/user               ─▶ build/site/guide/
gradlew :core:dokkaGenerate          ─▶ copy android/core/build/dokka/html/ to build/site/dev/api/
cp docs/site/index.html              ─▶ build/site/
checks: summary (sources) · remote references (output) · plain language (user sources) · lychee --offline --include-fragments (output)
```

`scripts/docs/build_site.py` runs all of it, locally and in CI. The deploy job removes
`build/site/guide/` before upload until the M7 closed test (D-003), so the checks always see the
whole site but only the published parts ship.

### Writing standards (summary; the writing guide is their home)

- **Part first, then kind.** Every page belongs to one part and one page kind; the
  template carries both.
- **Contributor pages** open with what the page is for. A repo ID never stands in for an
  explanation: it appears as a link, and the glossary explains its prefix.
- **Learn pages** explain an idea in plain language before naming it, and end with a
  Sources section. They follow the rules already in `docs/learn/README.md`.
- **User pages** use the user's words (pitch, resonance, session, target), with no code,
  no repo IDs and no module names. They make no medical claims, never assume gender, and
  use no guilt or pressure wording. Each message page says what happened and what to do.
- **No empty sections**: a section enters the navigation with its first real page.

## Phasing

Each phase maps to a ledger item, so the ledger stays the one list of work.

| Phase | What | Ledger item | Gate |
|---|---|---|---|
| 0 | This spec, research, plan and ADR-0007 | `043ea3ndd` | Owner merges; owner accepts ADR-0007 |
| 1 | Writing guide, templates, docs skill | `043ea4a6u` | Owner merges (skill, `CLAUDE.md`) |
| 2 | Books, Dokka, checks, workflow, Pages | `043ea4y10` | Owner merges; owner turns on Pages |
| 3 | Start here, status, setup, architecture, qew pages; facts out of `CLAUDE.md` | `043k77v78`, after `043ea4y10` (D-019) | Owner merges (`CLAUDE.md`) |
| 4 | User-guide skeleton and FAQ, unpublished until M7 | `043ea5k2j` | Owner merges; the M7 publish needs the D-016 audit |
| 5 | Privacy page at `/privacy/` | `043kotf51` (draft) | Owner merges |
| — | Play policy checklist, before the F1 spec | `043k784ev` (D-018) | Owner merges |

Phases 1 and 2 can run in parallel. Phases 3 and 4 need Phase 1's templates. Phase 5 needs
Phase 2 and the Play checklist.

## Decision ledger

| Date | ID | Decision | Status |
|---|---|---|---|
| 2026-10-29 | D-001 | **mdBook 0.5.x** for both books, installed in CI from its release binary with a pinned SHA-256, so no Rust toolchain enters the project. OpenPlush's comparison still holds, and nothing Kotlin-specific beats it (research R1) | Accepted in ADR-0007 |
| 2026-10-29 | D-002 | **Two books, three parts**: the contributor book (contributor guide and Learn) at `/dev/`, the user book at `/guide/`, a static landing page at `/`. The privacy page is a third, one-page book at `/privacy/` (D-015). Separate sidebars keep the user guide free of contributor vocabulary | Accepted (merged in #29, 2026-10-29) |
| 2026-10-29 | D-003 | **The user book is built and checked from its first page and published from the M7 closed test**, so testers can read it and the guide itself gets tested. Until the M8 release every page carries a banner saying it describes a test version. Amended by the owner's answer to Q-7 | Accepted (owner, 2026-10-29) |
| 2026-10-29 | D-004 | **A hand-curated `SUMMARY.md` per book, ordered as a reader's path**, with `create-missing = false` and a check that fails on any page in no navigation | Accepted (merged in #29, 2026-10-29) |
| 2026-10-29 | D-005 | **Links that leave the published tree become GitHub URLs**. Today that is two links (research R2). lychee checks the built HTML, not the Markdown, because mdBook rewrites `.md` to `.html` without checking | Accepted (merged in #29, 2026-10-29) |
| 2026-10-29 | D-006 | **No network on page load**: the default `index` preprocessor off, `runnable = false` for the playground, no MathJax, no remote `additional-*` files. A check fails on any `http(s)://` resource reference (`src`, `href` on `link`, CSS `url()`, `@import`) in the built output. Plain `<a href>` links to other sites are allowed | Accepted (merged in #29, 2026-10-29) |
| 2026-10-29 | D-007 | **API docs are Dokka HTML for `:core` only**, under `/dev/api/`. `:app` is UI glue and would pull the Android SDK into the docs job. Measured: deterministic, 1.5 MB, nothing remote on load (research R3) | Accepted in ADR-0007 |
| 2026-10-29 | D-008 | **Dokka's Kotlin stdlib and JDK links are turned off**, so the build reads nothing from the network and can't change when a remote package list does. The cost is that stdlib types in signatures are not links | Accepted in ADR-0007 |
| 2026-10-29 | D-009 | **A separate `docs.yml` workflow** builds the site on PRs that touch `docs/`, `book.toml`, `scripts/docs/`, `android/core/` or the workflow, and deploys from `main`. It stays out of `android.yml`, so a docs failure never hides a build failure. The workflow triggers on every PR and skips its job inside when nothing relevant changed, because a required check behind a `paths:` filter waits forever on PRs that skip it. It starts advisory and becomes required after ten green runs in a row on `main` (Q-6) | Accepted (owner, 2026-10-29) |
| 2026-10-29 | D-010 | **PR previews are a downloadable workflow artifact**, not a live host. The preview README says to open it through a local server (`python -m http.server`), because Dokka fetches its navigation (research R3) | Accepted (merged in #29, 2026-10-29) |
| 2026-10-29 | D-011 | **Site assets outside the usual permissive licences are allowed in the published site only**: OFL-1.1 fonts (Source Code Pro from mdBook; Inter and JetBrains Mono from Dokka) and CC BY 4.0 icons (Font Awesome in mdBook). The licensing constraint already limits itself to the app binary, so this records a reading, not an exception. Each build task lists every third-party asset with its licence | Accepted in ADR-0007 |
| 2026-10-29 | D-012 | **The writing guide (`docs/how-to/write-docs.md`) is the one home for documentation rules.** Templates carry structure; the docs skill carries steps and links to the guide | Accepted (merged in #29, 2026-10-29) |
| 2026-10-29 | D-013 | **`docs/` is the home of every fact a person needs; `CLAUDE.md` keeps agent directives and links.** Exception: the hard rules list and the build command stay in `CLAUDE.md`, because agents read it every turn and those rules guard the constitution | Accepted (merged in #29, 2026-10-29) |
| 2026-10-29 | D-014 | **The user guide never holds coaching text** (principle VIII). It explains what coaching is for and what each screen shows; wording users see during practice comes from content packs | Accepted (merged in #29, 2026-10-29) |

| 2026-10-29 | D-015 | **The privacy policy is a one-page book at `/privacy/`**, published as soon as it is written, separate from the user book so D-003 never holds it back. One Markdown source, so F14 can bundle the same text in the app for the in-app copy Play asks for. It describes only what the app does today (Q-3) | Accepted (owner, 2026-10-29) |
| 2026-10-29 | D-016 | **Site accessibility: best effort for the contributor book; WCAG 2.2 AA for the user book and privacy page before they first publish**, checked by a manual audit recorded in the PR that publishes them. The writing guide carries the audit checklist (alt text, heading order, link text, contrast of any custom CSS). No Node-based checker in CI for now (Q-4) | Accepted (owner, 2026-10-29) |
| 2026-10-29 | D-017 | **Spec folders are `specs/NNN-fNN-slug/`**: a sequence number, then the roadmap feature tag; specs that are not roadmap features leave the tag out. Recorded in `CLAUDE.md` and the roadmap (Q-5) | Accepted (owner, 2026-10-29) |
| 2026-10-29 | D-018 | **The Play policy checklist is written before the F1 spec** (`043k784ev`), each row with a source URL and the date it was last checked, so drift shows up as an old date (Q-1) | Accepted (owner, 2026-10-29) |
| 2026-10-29 | D-019 | **The onboarding pages are their own item** (`043k77v78`), done after the site builds (`043ea4y10`) so they land in a working site (Q-2) | Accepted (owner, 2026-10-29) |

### Accepted cons and their guards

Every con the owner accepted has a guard: something that makes the cost show up early, and
the ledger item that builds it. A con with no guard is a con nobody watches.

| Con | Guard | Built by |
|---|---|---|
| A hand-curated sidebar can lag a new page | The summary check fails the build and names the page | `043ea4y10` |
| The user guide is written before anyone reads it | It publishes at M7, so closed testers read it before release (D-003) | `043ea5k2j` |
| Three books duplicate `book.toml` settings | Kept small; a fourth book is the point to generate them | — |
| No stdlib links in the API docs (D-008) | Accepted as is; revisit if readers ask for them | — |
| Play policy text drifts after the checklist is written | Each row carries a source URL and a last-checked date; M7's exit criteria include re-checking every row within 30 days of the first upload (roadmap) | `043k784ev` |
| The privacy page publishes before the app exists | It is its own book, so the exception to D-003 is structural, not a rule to remember; it states only what the app does today, and F14 changes it in the same PR as the behaviour | `043kotf51` |
| WCAG AA is checked by hand, not by a tool | The audit checklist lives in the writing guide; the PR that first publishes the user book or the privacy page records the audit, and review rejects it without one | `043ea4a6u`, `043ea5k2j` |
| Long spec folder names | None needed | — |
| An advisory docs check lets breakage merge | `scripts/docs/build_site.py` runs the same checks locally; the workflow uses the always-run pattern from day one, so making it required is one settings change once it has ten green runs in a row on `main` | `043ea4y10` |
| Public pages describe a test version at M7 | A banner on every user-book page from one theme override, removed in the M8 release PR; pages still change with behaviour (FR-032) | `043ea5k2j` |
| ADR status lines lag the merge (merging accepts, `CLAUDE.md`) | The docs build prints a warning naming any ADR on `main` still marked proposed, and the next change to `docs/adr/` fixes it | `043ea4y10` |

### Resolved questions

The owner accepted every recommendation on 2026-10-29.

| Question | Answer |
|---|---|
| Q-1 Play checklist | Write it now, before the F1 spec: D-018, `043k784ev` (approved) |
| Q-2 Onboarding pages | Own item after the site builds: D-019, `043k77v78` (approved) |
| Q-3 Privacy policy | One-page book at `/privacy/`, published once written: D-015, `043kotf51` (draft) |
| Q-4 Site accessibility | Best effort, then AA before the user book publishes: D-016 |
| Q-5 Spec numbering | `NNN-fNN-slug`: D-017 |
| Q-6 Required check | Advisory, then required after ten green runs, always-run pattern: D-009 |
| Q-7 Closed test | Publish at M7 with a test-version banner: D-003 |
