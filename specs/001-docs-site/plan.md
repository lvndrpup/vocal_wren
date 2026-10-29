# Implementation Plan: A Documentation Site for Contributors, Learners and Users

**Branch**: `spec/001-docs-site` | **Date**: 2026-10-29 | **Status**: Draft
**Spec**: [spec.md](spec.md) · **Research**: [research.md](research.md) · **ADR**:
[ADR-0007](../../docs/adr/0007-docs-site.md) (Proposed)

## Summary

Publish `docs/` as a static site in two books. The contributor book holds the
contributor guide and Learn, so the people who read both get one sidebar. The user book
holds the user guide and FAQ. It is built and checked from its first page but published
only at the first public release. The `:core` API docs from Dokka sit beside the
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
| VII Visual-first accessibility | ⚠️ Binds the app, not the site. The site's own target is Q-4 |
| VIII Content as data | ✅ The user guide holds no coaching text (spec FR-033) |
| IX Shared core | ✅ Dokka is a build-time plugin on `:core`. It adds no runtime dependency and no Android dependency |
| X Test-first | ✅ Each check lands with its failing test first, in the same change |
| XI Decisions recorded | ✅ ADR-0007 (Proposed) records D-001, D-007, D-008 and D-011 |
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
└── guide/            user book (published from the first public release; D-003)
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
`build/site/guide/` before upload until D-003 is lifted, so the checks always see the
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
| 3 | Start here, status, setup, architecture, qew pages; facts out of `CLAUDE.md` | `043k77v78` (draft, Q-2) | Owner merges (`CLAUDE.md`) |
| 4 | User-guide skeleton and FAQ, unpublished | `043ea5k2j` | Owner merges; publishing is the owner's decision |

Phases 1 and 2 can run in parallel. Phases 3 and 4 need Phase 1's templates.

## Decision ledger

| Date | ID | Decision | Status |
|---|---|---|---|
| 2026-10-29 | D-001 | **mdBook 0.5.x** for both books, installed in CI from its release binary with a pinned SHA-256, so no Rust toolchain enters the project. OpenPlush's comparison still holds, and nothing Kotlin-specific beats it (research R1) | Proposed in ADR-0007 |
| 2026-10-29 | D-002 | **Two books, three parts**: the contributor book (contributor guide and Learn) at `/dev/`, the user book at `/guide/`, a static landing page at `/`. Separate sidebars keep the user guide free of contributor vocabulary | Proposed |
| 2026-10-29 | D-003 | **The user book is built and checked from its first page but published only at the first public release** (M8 on the roadmap). Lifting this is the owner's decision; see Q-7 for the closed test | Proposed |
| 2026-10-29 | D-004 | **A hand-curated `SUMMARY.md` per book, ordered as a reader's path**, with `create-missing = false` and a check that fails on any page in no navigation | Proposed |
| 2026-10-29 | D-005 | **Links that leave the published tree become GitHub URLs**. Today that is two links (research R2). lychee checks the built HTML, not the Markdown, because mdBook rewrites `.md` to `.html` without checking | Proposed |
| 2026-10-29 | D-006 | **No network on page load**: the default `index` preprocessor off, `runnable = false` for the playground, no MathJax, no remote `additional-*` files. A check fails on any `http(s)://` resource reference (`src`, `href` on `link`, CSS `url()`, `@import`) in the built output. Plain `<a href>` links to other sites are allowed | Proposed |
| 2026-10-29 | D-007 | **API docs are Dokka HTML for `:core` only**, under `/dev/api/`. `:app` is UI glue and would pull the Android SDK into the docs job. Measured: deterministic, 1.5 MB, nothing remote on load (research R3) | Proposed in ADR-0007 |
| 2026-10-29 | D-008 | **Dokka's Kotlin stdlib and JDK links are turned off**, so the build reads nothing from the network and can't change when a remote package list does. The cost is that stdlib types in signatures are not links | Proposed in ADR-0007 |
| 2026-10-29 | D-009 | **A separate `docs.yml` workflow** builds the site on PRs that touch `docs/`, `book.toml`, `scripts/docs/`, `android/core/` or the workflow, and deploys from `main`. It stays out of `android.yml`, so a docs failure never hides a build failure | Proposed |
| 2026-10-29 | D-010 | **PR previews are a downloadable workflow artifact**, not a live host. The preview README says to open it through a local server (`python -m http.server`), because Dokka fetches its navigation (research R3) | Proposed |
| 2026-10-29 | D-011 | **Site assets outside the usual permissive licences are allowed in the published site only**: OFL-1.1 fonts (Source Code Pro from mdBook; Inter and JetBrains Mono from Dokka) and CC BY 4.0 icons (Font Awesome in mdBook). The licensing constraint already limits itself to the app binary, so this records a reading, not an exception. Each build task lists every third-party asset with its licence | Proposed in ADR-0007 |
| 2026-10-29 | D-012 | **The writing guide (`docs/how-to/write-docs.md`) is the one home for documentation rules.** Templates carry structure; the docs skill carries steps and links to the guide | Proposed |
| 2026-10-29 | D-013 | **`docs/` is the home of every fact a person needs; `CLAUDE.md` keeps agent directives and links.** Exception: the hard rules list and the build command stay in `CLAUDE.md`, because agents read it every turn and those rules guard the constitution | Proposed |
| 2026-10-29 | D-014 | **The user guide never holds coaching text** (principle VIII). It explains what coaching is for and what each screen shows; wording users see during practice comes from content packs | Proposed |

### Trade-offs accepted

- **A hand-curated sidebar can lag a new page.** The summary check turns that into a
  failed build, not a hidden page.
- **The user guide is written before anyone reads it.** It keeps each user-facing feature
  explainable and avoids a catch-up project before release.
- **Two books mean two `book.toml` files.** Shared settings are duplicated. A third book
  would be the point to generate them.
- **No stdlib links in the API docs** (D-008), in exchange for an offline, stable build.

### Open questions for the owner

- **Q-1 Play checklist.** CLAUDE.md asks specs to cite play-checklist IDs, and none
  exists. The spec's Play Impact marks each point "pending". Draft ledger item `043k784ev`
  writes the checklist; approve it, change it, or say where the IDs should come from.
- **Q-2 Onboarding pages.** Phase 3 (start here, status, setup, architecture, qew, and
  moving facts out of `CLAUDE.md`) has no approved ledger item. Draft `043k77v78` covers it.
- **Q-3 Privacy policy.** Play will need a public privacy-policy URL before the first
  upload. Should it live on this site, and if so as its own page published before the
  user guide (it describes the app's promise, not its features), or somewhere else?
- **Q-4 Site accessibility.** Should the site itself target WCAG 2.2 AA, as the app does
  under principle VII? mdBook's default theme has keyboard navigation and a
  high-contrast theme, but nobody has audited it.
- **Q-5 Spec numbering.** The roadmap says feature IDs F1–F16 refer to specs under
  `specs/`. This spec is `001` but is not a roadmap feature. Keep a plain sequence
  (`001`, `002`, ...) and name the F-number inside each spec, or name folders by F-number
  (`f01-audio-engine`) and put non-roadmap specs elsewhere?
- **Q-6 Required check.** Should the docs workflow be a required check on PRs, or
  advisory until the site has settled?
- **Q-7 Closed test.** Should the user guide publish for the M7 closed test, so testers
  can read it, or only at the M8 public release as D-003 says?
