---
status: proposed
date: 2026-10-29
decision-makers: owner (lvndrpup)
---

# Build the docs site with mdBook and the core's API docs with Dokka

## Context and Problem Statement

[Spec 001](../../specs/001-docs-site/spec.md) publishes `docs/` as a static site in three
parts: a contributor guide, Learn, and a user guide, with the `:core` API docs beside them.
Three questions need an answer before its build lands. Which tool builds the guide pages?
Which builds the API docs? And what licences may the tools and the files they put in the
published site carry, given that the licensing constraint in the
[constitution](../constitution.md#licensing-constraint) speaks only of the app binary?

This ADR records the plan's decisions D-001, D-007, D-008 and D-011
([plan](../../specs/001-docs-site/plan.md#decision-ledger)).

## Decision Drivers

* No network on page load: no remote fonts, scripts or stylesheets (spec FR-013). Principle
  I binds the app, but the site keeps the same promise for its readers.
* The same commit builds a byte-identical site (spec FR-014).
* Licensing constraint: no GPL, AGPL or LGPL code in the app binary. Nothing in the docs
  toolchain may reach the binary.
* Maintainability for one part-time developer: no new language toolchain; tools pinned
  exactly.
* Principle IX: `:core` keeps no Android dependency and gains no runtime dependency.

## Considered Options

Guide pages (D-001):

* A: mdBook 0.5.x, installed from its release binary
* B: Zola
* C: Material for MkDocs, or its successor Zensical
* D: Starlight, Docusaurus or VitePress
* E: Dokka alone, with Markdown modules

API docs (D-007, D-008):

* F: Dokka 2.x HTML for `:core` only, stdlib and JDK links off
* G: Dokka for `:core` and `:app`
* H: no published API docs

Site licences (D-011):

* I: the licensing constraint governs the app binary; the published site may carry OFL-1.1
  fonts and CC BY 4.0 icons, and every third-party asset is listed with its licence
* J: hold the site to the same licences as permissive code, and strip or replace the
  bundled fonts and icons

## Decision Outcome

**Guide pages: A, mdBook 0.5.x**, for both books. It is a single MPL-2.0 binary, privacy-clean
by default since 0.5.0, and two builds of the same input were byte-identical [solid:
OpenPlush ADR 0017]. It ships prebuilt binaries for Linux, macOS and Windows, so CI
installs it with a download and a pinned SHA-256, and no Rust toolchain enters the project
[solid: GitHub releases, 0.5.4, 2026-10-29]. Required settings: `create-missing = false`,
the default `index` preprocessor off, `[output.html.playground] runnable = false`, no
MathJax.

**API docs: F, Dokka 2.2.x HTML for `:core` only**, published under `/dev/api/`. Measured
on a scratch copy of `:core` on 2026-10-29: two clean builds were byte-identical, the
output loads nothing remote, and its scripts fetch only local files. With stdlib and JDK
links off, the build reads nothing from the network either. The plugin is applied to
`:core`'s build for documentation only and adds no runtime or Android dependency.

**Site licences: I.** The licensing constraint bars GPL, AGPL and LGPL code from the app
binary. The published site is not the binary, so this reads the constraint rather than
amends it, and no constitution version bump follows. The site may carry:

| Asset | Licence | From |
|---|---|---|
| Source Code Pro font | OFL-1.1 | mdBook theme |
| Open Sans font | Apache-2.0 | mdBook theme |
| Font Awesome Free icons, inlined as SVG | CC BY 4.0 (attribution kept in each SVG) | mdBook theme |
| clipboard.js, elasticlunr, mark.js; highlight.js | MIT; BSD-3-Clause | mdBook theme |
| Inter and JetBrains Mono fonts | OFL-1.1 | Dokka HTML |
| Ring UI, Prism, React, core-js | Apache-2.0 or MIT [verify] | Dokka HTML |

Tools that run only in CI or on a contributor's machine, and write nothing into the app:

| Tool | Licence |
|---|---|
| mdBook 0.5.4 | MPL-2.0 |
| lychee 0.24.2 | Apache-2.0 OR MIT |
| Dokka 2.2.0 (Gradle plugin) | Apache-2.0 |

### Consequences

* Good, because the site builds from two pinned binaries and one Gradle task, with no
  Python, Node or Rust toolchain for the site itself (the checks use Python's standard
  library, which the oracle needs anyway).
* Good, because Learn and the contributor guide publish as they are written, and the API
  docs follow `:core` without hand-kept pages.
* Good, because the site's licences are written down once, and it is clear that none of
  them reach the APK.
* Bad, because the site carries font files under OFL-1.1 and icons under CC BY 4.0. Any
  asset under another licence needs its own ADR.
* Bad, because mdBook's theming is plainer than the alternatives', and Dokka's and mdBook's
  styles won't match.
* Bad, because without stdlib links, types like `Float` in `:core`'s API pages are not
  links.

### Confirmation

* The docs workflow's build (ledger `043ea4y10`) lists every third-party asset in the
  built site with its licence. An asset that is not in the tables above stops that task
  for a new ADR. A version bump of mdBook or Dokka repeats the list.
* Review: a PR that adds any docs-site asset or tool to `:app`, or to `:core`'s runtime
  classpath, is rejected.
* The remote-reference check fails the build on any remote resource in the output.

## Pros and Cons of the Options

### A: mdBook

* Good, because it is one binary, privacy-clean by default, and its unknown config keys are
  errors.
* Bad, because it is a second documentation tool next to Dokka.

### B: Zola

* Bad, because it is EUPL-1.2 since 0.22.0. That is outside the licensing constraint's
  scope (the site is not the binary), but a weak-copyleft licence on a tool adds review
  cost for no gain over A.

### C: Material for MkDocs or Zensical

* Bad, because Material reaches end of life around 2026-11 and loads Google Fonts by
  default, Zensical is alpha, and both add a Python toolchain for the site.

### D: Starlight, Docusaurus or VitePress

* Bad, because each adds a Node toolchain. Astro's CLI sends telemetry unless turned off,
  Docusaurus has no offline search built in, and VitePress stable has been idle since
  2025-08.

### E: Dokka alone

* Good, because it is one tool.
* Bad, because it renders API docs and per-module Markdown, not ordered chapters in parts.
  Learn and the user guide don't fit it.

### F: Dokka for `:core` only

* Good, because `:core` is where the logic worth reading lives (principle IX), and its build
  is plain Kotlin/JVM.
* Bad, because `:app`'s API isn't published.

### G: Dokka for `:core` and `:app`

* Bad, because the docs job would need the Android SDK and the Android Gradle Plugin, for
  pages about UI glue.

### H: no API docs

* Good, because it is the least work.
* Bad, because contributors lose the reference for the module that matters most.

### I: the constraint governs the binary

* Good, because it matches the constitution's own text and what it protects: what users
  install.
* Bad, because it depends on review to keep site assets out of the app.

### J: same licences for the site

* Good, because one rule covers everything.
* Bad, because neither mdBook nor Dokka has a stable way to drop its fonts; a post-build
  step that deletes fonts and patches CSS breaks on each release.

## More Information

* Spec 001: [spec](../../specs/001-docs-site/spec.md),
  [research](../../specs/001-docs-site/research.md),
  [plan](../../specs/001-docs-site/plan.md).
* Adapted from OpenPlush
  [ADR 0017](https://github.com/openplush/openplush/blob/main/docs/adr/0017-docs-site.md).
* Revisit if mdBook or Dokka starts loading anything remote, if a docs asset is needed in
  the app (for example bundled offline help), or if `:app` gains API worth publishing.
