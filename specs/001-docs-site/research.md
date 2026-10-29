# Research: A Documentation Site for Contributors, Learners and Users

**Feature**: `001-docs-site` | **Date**: 2026-10-29 | **Status**: Active

Confidence tags: `[solid]` verified, `[likely]` reasoned inference, `[speculative]` guess,
`[verify]` must be checked by the task that depends on it. Versions are as of 2026-10-29.

This feature adapts OpenPlush's
[`004-docs-site`](https://github.com/openplush/openplush/tree/main/specs/004-docs-site).
Facts OpenPlush measured on 2026-10-20 are cited as "OpenPlush R*n*" and were not
re-measured here unless the row says so.

## R1. Which site generator, checked again

OpenPlush chose mdBook in its
[ADR 0017](https://github.com/openplush/openplush/blob/main/docs/adr/0017-docs-site.md).
The question here is whether anything about Vocal Wren changes that answer. The two
differences are that Vocal Wren has no Rust toolchain, and its API docs come from Dokka,
not rustdoc.

| Fact | Tag |
|---|---|
| mdBook 0.5.4 (2026-07-06) is still the latest release. It is MPL-2.0 and a single binary | [solid] crates.io and GitHub releases API, 2026-10-29 |
| mdBook publishes prebuilt binaries for Linux (gnu and musl), macOS and Windows on each GitHub release, so CI needs no Rust toolchain to install it. The release has no published checksum files, so the workflow pins its own SHA-256 | [solid] GitHub releases API, 2026-10-29 |
| mdBook 0.5.0 removed Google Analytics, bundles its fonts locally and inlines its icons as SVG. Two builds of the same input were byte-identical | [solid] OpenPlush R1 |
| Zola is EUPL-1.2 since 0.22. Material for MkDocs is in maintenance mode, reaches end of life around 2026-11 and loads Google Fonts by default. Zensical is alpha. Starlight, Docusaurus and VitePress add a Node toolchain | [solid] OpenPlush R1 |
| Vocal Wren's licensing constraint bars only GPL, AGPL and LGPL code in the app binary. It has no allow-list, unlike OpenPlush's principle IX | [solid] `docs/constitution.md` |
| Dokka can't be the whole site. It renders KDoc and per-module Markdown, not a book with ordered chapters and parts | [likely] Dokka docs |
| JetBrains Writerside needs its own builder and is not open source | [likely]; rejected without measuring |

**Decision**: mdBook 0.5.x, installed in CI from its release binary (D-001). Nothing
about Vocal Wren tips the comparison toward a Gradle- or JVM-based generator. A Gradle
static-site plugin would keep one toolchain, but none found is maintained and
privacy-clean by default [speculative; no candidate was measured].

## R2. How mdBook treats this repo's docs

| Fact | Tag |
|---|---|
| mdBook won't build without `SUMMARY.md`. `create-missing` defaults to true and silently creates empty pages for missing entries | [solid] OpenPlush R2 |
| The default `index` preprocessor turns `README.md` into `index.html` but rewrites body links `.md` → `.html` without checking them, so `learn/README.md` becomes a dead `learn/README.html`. `[build] use-default-preprocessors = false` plus `[preprocessor.links]` fixes it | [solid] OpenPlush R2, tested on 0.5.4 |
| A ```` ```rust ```` block becomes a playground block that POSTs to `play.rust-lang.org` on load unless `[output.html.playground] runnable = false`. Kotlin blocks are not playground blocks, but the setting is cheap insurance | [solid] OpenPlush R2; [likely] for Kotlin |
| mdBook's default theme bundles Source Code Pro (OFL-1.1) and Open Sans (Apache-2.0), and inlines Font Awesome Free icons (CC BY 4.0) | [solid] OpenPlush ADR 0017 |
| lychee 0.24.2 (2026-05-01, Apache-2.0 OR MIT) checks built HTML with `--offline`. Its GitHub releases include prebuilt binaries with `.sha256` files, and `lycheeverse/lychee-action` v2.9.0 exists | [solid] crates.io and GitHub releases API, 2026-10-29 |
| Vocal Wren's `docs/` (with PR #28) has 19 Markdown files. Two links leave `docs/`: `../../CLAUDE.md` and `../../android/core/.../Frame.kt`. One link points at `learn/README.md`, which the default `index` preprocessor would break. Every other relative link stays inside `docs/` | [solid] audit of `docs/learn-primer`, 2026-10-29 |
| `docs/salvage/voice-trainer.md` has code blocks. None are `rust` playground blocks | [solid] audit |

The scratch build of the Learn pages with mdBook 0.5.4 wasn't run in this session (the
binary download was not permitted). The first site task repeats OpenPlush's measurements
on this repo: determinism, zero remote references, README links [verify].

**Decisions**: a hand-curated `SUMMARY.md` with a completeness check (D-004); links that
leave the tree become GitHub URLs, and lychee checks the built HTML (D-005); a
network-free config and a check for it (D-006).

## R3. Kotlin API docs with Dokka

Measured on 2026-10-29 with a scratch copy of `android/core` (Kotlin 2.2.0, JDK 17,
Gradle wrapper 8.14.3), applying `org.jetbrains.dokka` 2.2.0 and running
`:core:dokkaGenerate`.

| Fact | Tag |
|---|---|
| Dokka 2.2.0 (2026-03-26) is the latest release. It is Apache-2.0. The v2 Gradle plugin is the default since 2.1.0, and HTML is its default output | [solid] GitHub releases and licence API; Gradle Plugin Portal |
| `:core` documented as 74 files, 1.5 MB, with no change to `:core`'s sources or its JAR | [solid] measured |
| Two clean builds (`clean :core:dokkaGenerate --rerun-tasks`) gave byte-identical output | [solid] measured |
| The output has no remote `<script>`, `<link>`, `<img>`, CSS `url()` or `@import`. Its only remote URLs are ordinary `<a href>` links: to `github.com/Kotlin/dokka` in the footer and to `kotlinlang.org` stdlib pages for types like `Float` and `String` | [solid] measured |
| The scripts call `fetch` only for local files: `navigation.html` and `scripts/pages.json`, relative to the page | [solid] measured |
| Because the navigation is fetched, the sidebar won't load when a downloaded preview is opened straight from disk (`file://`); a local web server is needed | [likely] browsers block `fetch` on `file://`; not tested in a browser |
| Dokka bundles Inter and JetBrains Mono as local `woff`/`woff2` files under `ui-kit/fonts/`. Both fonts are OFL-1.1. No licence file for them is written into the output | [solid] measured for the files; [likely] for the licences, from the fonts' upstream projects |
| The rest of the bundled front end (JetBrains Ring UI, Prism, React, core-js) is Apache-2.0 or MIT | [likely] from licence comments and upstream projects; the build task lists each with its licence [verify] |
| The stdlib links mean Dokka resolves the Kotlin stdlib's package list from `kotlinlang.org` at build time. That makes the build need the network and depend on a remote file. Dokka has options to turn off the stdlib and JDK links [verify] | [likely] |
| Documenting `:app` would need the Android SDK and the Android Gradle Plugin in the docs job. `:app` is UI glue (principle IX), so its API is not worth publishing yet | [likely] |

**Decision**: Dokka HTML for `:core` only, under `/dev/api/` (D-007), with the stdlib and
JDK links off so the build reads nothing remote (D-008).

## R4. Publishing and previews

| Fact | Tag |
|---|---|
| The repository `lvndrpup/vocal_wren` is public, so GitHub Pages is free for it. The default address is `https://lvndrpup.github.io/vocal_wren/` | [solid] `gh repo view`, 2026-10-29; [likely] for the address |
| The Pages actions are `upload-pages-artifact` and `deploy-pages`. The deploy job needs `pages: write` and `id-token: write`, and the `github-pages` environment can be limited to `main` | [solid] OpenPlush R4 |
| GitHub's native PR previews for Pages are not public. Branch-based preview actions need write tokens and fail for forks | [solid] OpenPlush R4 |
| The existing `android.yml` already sets up JDK 17 and Gradle with `gradle/actions/setup-gradle@v4` | [solid] `.github/workflows/android.yml` |

**Decisions**: a separate `docs.yml` workflow: build on PRs, deploy from `main` (D-009);
previews are a downloadable artifact (D-010).

## R5. Play policy and the site

| Fact | Tag |
|---|---|
| Google Play's User Data policy asks apps that access sensitive data or permissions to post a privacy policy in the Play Console and inside the app | [likely] from general knowledge of the policy; [verify] against the current policy when the play-checklist is written |
| The repository has no play-checklist and no play-checklist IDs yet | [solid] `grep` of the repository, 2026-10-29 |

## Sources

- mdBook: <https://github.com/rust-lang/mdBook/releases/tag/v0.5.4>; crates.io
  <https://crates.io/crates/mdbook>.
- lychee: <https://github.com/lycheeverse/lychee/releases/tag/lychee-v0.24.2>;
  <https://github.com/lycheeverse/lychee-action>.
- Dokka: <https://github.com/Kotlin/dokka/releases/tag/v2.2.0>; Gradle Plugin Portal
  <https://plugins.gradle.org/plugin/org.jetbrains.dokka/2.2.0>; migration guide
  <https://kotlinlang.org/docs/dokka-migration.html>.
- OpenPlush 004 research and ADR 0017:
  <https://github.com/openplush/openplush/blob/main/specs/004-docs-site/research.md>,
  <https://github.com/openplush/openplush/blob/main/docs/adr/0017-docs-site.md>.
- Google Play User Data policy: <https://support.google.com/googleplay/android-developer/answer/10144311>
  [verify].
