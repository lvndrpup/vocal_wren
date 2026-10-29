# Feature Specification: A Documentation Site for Contributors, Learners and Users

**Feature branch**: `spec/001-docs-site`

**Created**: 2026-10-29

**Status**: Accepted (merged in #29); amended 2026-10-29 with the owner's answers to plan Q-1 to Q-7

**Ledger item**: `043ea3ndd` (parent epic C)

**Input**: Adapt OpenPlush's
[`specs/004-docs-site`](https://github.com/openplush/openplush/tree/main/specs/004-docs-site)
for Vocal Wren. Three parts (contributor guide, Learn, user guide), Kotlin API docs via
Dokka in place of rustdoc, the generator choice checked again (mdBook as CI-only tooling),
no network on page load, Principles Touched and Play Impact sections, and a Proposed ADR
for the tools and licences.

> Rule: this file states **what** and **why** only. Tool choices live in
> [`research.md`](research.md) and [`plan.md`](plan.md).

Vocal Wren's documentation today is a constitution, a roadmap, ADRs and agent rules, all
written for the owner and agents. The Learn primer and glossary
([PR #28](https://github.com/lvndrpup/vocal_wren/pull/28), ledger `043ea313v`) add the
first pages written for people learning the subject. This feature gives `docs/` readers,
a shape and a published home, and makes room for the user guide the app will need at
release.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A contributor finds their way in (Priority: P1)

A developer opens the site from the README. A "Start here" page tells them what Vocal
Wren is, what is built today, and the path to follow. They set up, run the build CI runs,
see which Gradle module owns what and why, and find a first piece of work in the qew
ledger. They don't have to open `CLAUDE.md`, the constitution or an ADR unless they want
to go deeper.

**Why this priority**: The project is solo and part-time. The person most likely to need
"start here" is the owner coming back after weeks away, and the second is a first outside
contributor. Both need the path written down, not rebuilt from agent rules.

**Independent test**: Someone new to the repository follows only the site from its
landing page, reaches a passing `./gradlew :core:test :app:assembleDebug`, and answers
five orientation questions: what `:core` and `:app` each hold, why no `INTERNET`
permission is allowed, who merges a PR, what `qew ready` shows, and where the project
status lives.

**Acceptance scenarios**:

1. **Given** the published site, **When** a reader opens it, **Then** the first page names
   each part's audience (contributors, learners, users) and the path through the
   contributor part, in order.
2. **Given** a reader on the setup page, **When** they follow it, **Then** it gets them to
   a passing local build in three documented commands or fewer.
3. **Given** a page that uses a domain term (formant, F0, LPC, AGC) or a repo ID (OQ-,
   ADR-, F*n*, M*n*, a qew id), **When** a reader meets it, **Then** the term or the ID's
   prefix is defined in the one glossary the page links to.
4. **Given** a question "is X built yet?", **When** a reader looks it up, **Then** exactly
   one page answers it, and every other place that mentions status links there.

---

### User Story 2 - A learner reads the voice science in order (Priority: P1)

A contributor who has never studied acoustics opens the Learn part and reads it front to
back: sound, pitch, source and filter, formants, vocal weight, how it's measured. Each
page links its sources and the glossary.

**Why this priority**: The Learn primer exists already (PR #28). Publishing it is nearly
free, and it is the part people outside the repository are most likely to read.

**Independent test**: The Learn part builds, appears in the navigation in the primer's
reading order, and passes the link and network checks. Every Learn page has a Sources
section.

**Acceptance scenarios**:

1. **Given** the contributor navigation, **When** a reader opens Learn, **Then** its pages
   appear in the order the Learn index gives.
2. **Given** a Learn page, **When** it cites a source, **Then** the link opens the source
   or a stable archive of it. No Learn page is published without a Sources section.

---

### User Story 3 - Every reader can trust what the site shows (Priority: P1)

Whatever page a reader lands on is current, reachable from the navigation, free of dead
links, and loads nothing from the network. The site is rebuilt and republished from
`main` with no manual step.

**Why this priority**: A wrong page that looks authoritative is the docs version of a
confident wrong number, which principle II forbids in the app. A site that sends
requests would break the privacy promise on the project's most public surface, even
though principle I only binds the app.

**Independent test**: Build the site from a clean checkout. The checks fail on a page left
out of the navigation, a dead internal link, or any reference to a remote font, script or
stylesheet, and pass otherwise. Building the same commit twice gives identical output.

**Acceptance scenarios**:

1. **Given** a change that adds a page without listing it in a navigation, **When** the
   checks run, **Then** they fail and name the page.
2. **Given** a link from the site to a repository file that isn't published (a spec,
   `CLAUDE.md`, a source file), **When** the site is built, **Then** the link opens that
   file on GitHub, never a dead page.
3. **Given** any published page, **When** it loads, **Then** the browser requests nothing
   from outside the site.
4. **Given** a change merged to `main`, **When** the publish run finishes, **Then** the
   site shows it.
5. **Given** a proposed change to the docs, **When** its checks run, **Then** a reviewer can
   download and open the built site for that change.

---

### User Story 4 - A user gets help with the app (Priority: P2)

Once Vocal Wren is released, a user (someone training their voice, not a programmer) finds
a user guide and an FAQ. They cover what the app does, how to record a first baseline,
what each screen shows, why a number is sometimes missing, and what to do about each
message the app shows. The FAQ answers what every new user asks: is it free, does my
voice leave my phone, is this medical advice, why doesn't it ask who I am. It is written
in the user's words, with no code and no repo IDs.

**Why this priority**: Users are who the app is for. Writing their guide alongside the
features means it is never a catch-up project before release, and it makes each
user-facing feature prove it can be explained plainly. It is P2 because nothing
user-facing exists yet.

**Independent test**: The user guide builds and passes the same checks as the rest of the
site. Every page describes behaviour that exists in the code. A plain-language check
finds no repo ID and no code identifier in it.

**Acceptance scenarios**:

1. **Given** the user part, **When** a reader opens it, **Then** it has its own navigation
   and landing page, separate from the contributor and Learn parts, and never sends a
   user into contributor pages for something they need.
2. **Given** a change that adds or changes behaviour a user sees, **When** it is merged,
   **Then** the user-guide page for that behaviour changes in the same change.
3. **Given** the app has not reached its closed test, **When** the site is published,
   **Then** the user part is built and checked but not published, so the site never
   promises users something that doesn't exist. From the closed test until the first
   public release, every user page says it describes a test version.
4. **Given** a metric the app hides because its confidence is too low (principle II),
   **When** a user asks why, **Then** the guide explains it plainly, without blaming
   their voice.

---

### User Story 5 - Any author, human or agent, writes a page the same way (Priority: P2)

An author, a person or an agent, starts from one writing guide. It tells them which part
and which kind of page this is (tutorial, how-to, explanation, reference, Learn page, user
task guide, FAQ entry), which template to copy, where the page goes in the navigation,
and the writing rules. Agents follow the same guide through a docs skill that adds only
the procedure.

**Why this priority**: Without a shared shape the site grows into each author's habit,
which today means agent-style rule lists. The first contributor pages need it, so in
practice it lands early.

**Independent test**: A new page written from a template passes the checks with no change
to the template's structure. The docs skill names the writing guide and adds no rule of
its own.

**Acceptance scenarios**:

1. **Given** an author starting a page, **When** they open the writing guide, **Then** it
   gives them the part, the page kind, the template and the navigation position, in that
   order.
2. **Given** the docs skill, **When** an agent loads it, **Then** every rule it applies
   links into the writing guide.
3. **Given** a fact both agents and people need (the build command, the branch rule, the
   merge rule), **When** it is written down, **Then** it has one home in `docs/` and
   `CLAUDE.md` links to it, unless the plan records a reason otherwise.

---

### User Story 6 - A developer looks up the core's API beside the guide (Priority: P3)

From a guide page that names a type in `:core`, a developer opens the generated API
documentation for it on the same site.

**Why this priority**: `:core` holds all the analysis, confidence and safety logic
(principle IX), so it is the API worth reading. It is P3 because `:core` is still almost
empty.

**Independent test**: The published site has the API documentation for `:core`, reachable
from the contributor navigation, and it passes the link and network checks.

**Acceptance scenarios**:

1. **Given** the contributor navigation, **When** a reader opens the API entry, **Then**
   they reach the `:core` API pages.

---

### Edge cases

- **A page in no navigation**: the checks fail and name it. Templates are left out by a
  stated rule, not by accident.
- **A link to a folder's index page**: it opens that folder's landing page, not a dead
  file.
- **A link to something outside the published tree**: it opens on GitHub. A relative link
  that leaves the published tree fails the checks.
- **An empty section**: it stays out of the navigation until it has a real page. No
  "coming soon" pages.
- **Status drift**: a page other than the status page that states what is built fails
  review and gets a link instead.
- **A user-facing change before release**: the change adds or updates its user-guide
  page, which is built and checked but not published.
- **Coaching wording in the user guide**: the guide describes what coaching does and
  never copies its wording. Coaching text lives in content packs (principle VIII).
- **The API build or the user part fails to build**: the whole publish fails. A partial
  site is never published.
- **A forked contributor's change**: it can be built and previewed, never published.

## Requirements *(mandatory)*

### Functional requirements

**Site and publishing**

- **FR-001**: The project MUST publish one documentation site built from `docs/`, with a
  landing page that sends each audience to its part.
- **FR-002**: The site MUST have three parts: a contributor guide, Learn, and a user guide
  (with an FAQ). The user guide MUST have navigation separate from the other two.
- **FR-003**: The site MUST be rebuilt and republished automatically from `main`.
  Publishing MUST NOT run for proposed changes or forks.
- **FR-004**: Every proposed change that touches `docs/` or the site's build MUST build
  the whole site and make it available to reviewers to download.
- **FR-005**: The user guide MUST be built and checked on every such change, but MUST NOT
  be published before the app's closed test (M7). From then until the first public
  release, every user-guide page MUST say it describes a test version.
- **FR-006**: The privacy policy MUST be published on the site at a stable address, apart
  from the user guide, as soon as it is written. It MUST state only what the app does at
  that time.

**Trust**

- **FR-010**: Every page under `docs/` MUST appear in exactly one navigation, or be left
  out by a stated rule (templates). The checks MUST fail otherwise.
- **FR-011**: The checks MUST fail on any dead link inside the built site, anchors
  included.
- **FR-012**: Links to repository files that aren't published MUST point to the file on
  GitHub.
- **FR-013**: No published page MAY load a font, script, stylesheet or any other resource
  from outside the site, or send any request on load. The checks MUST fail on a remote
  resource reference in the built output.
- **FR-014**: Building the same commit twice MUST give identical output.
- **FR-015**: Project status (what is built and what isn't) MUST be stated on exactly one
  page. Other documents link to it.

**Contributor guide and Learn**

- **FR-020**: The contributor guide MUST be ordered as a path: start here, set up, how the
  app is built, how the project is run (qew, branches, ADRs), reference, decisions.
- **FR-021**: It MUST include the one glossary, which defines domain terms and every repo
  ID prefix (from PR #28, `docs/reference/glossary.md`).
- **FR-022**: Learn MUST be published as its own part of the contributor navigation, in
  the reading order its index gives. Every Learn page MUST keep a Sources section.
- **FR-023**: Every fact a human contributor needs MUST have its home in `docs/`.
  `CLAUDE.md` keeps agent directives and links to `docs/` for the facts, except where the
  plan records a reason.
- **FR-024**: It SHOULD include the generated API documentation of `:core` (US6).

**User guide**

- **FR-030**: The user guide MUST be written for users, not programmers: no code, no repo
  IDs, no module names.
- **FR-031**: It MUST contain an FAQ, a getting-started path to a first session, task
  guides, and an explanation of every message the app shows a user.
- **FR-032**: It MUST describe only behaviour that exists in the code. A change that
  alters user-facing behaviour MUST update the guide in the same change.
- **FR-033**: It MUST NOT contain coaching text. Coaching wording lives in content packs
  (principle VIII); the guide explains what coaching is for.
- **FR-034**: It MUST NOT make medical claims, and it MUST point users to a doctor or a
  speech-language pathologist for pain, voice loss or lasting hoarseness (principle IV).
- **FR-035**: It MUST NOT ask about, assume or sort users by gender. Targets are described
  as parameters; presets are optional labels the user chooses (principle III).
- **FR-036**: The user guide and the privacy policy MUST meet WCAG 2.2 AA before they are
  first published, shown by an audit recorded in the change that publishes them.

**Authoring**

- **FR-040**: There MUST be one writing guide that defines the parts, the page kinds, the
  writing rules, and how IDs may appear in each part.
- **FR-041**: There MUST be one template per page kind.
- **FR-042**: There MUST be a docs skill that walks an agent through the writing guide's
  steps and states no rule of its own.

### Key entities

- **Part**: an audience's section of the site (contributor guide, Learn, user guide).
- **Book**: one built unit with one navigation. A book holds one or more parts.
- **Page kind**: tutorial, how-to, explanation, reference (Diátaxis), plus Learn page,
  user task guide and FAQ entry.
- **Template**: the starting structure for one page kind.
- **Writing guide**: the one home for documentation rules.
- **Status page**: the one home for what is built.

## Success Criteria *(mandatory)*

- **SC-001**: Following only the site, a new contributor reaches a passing local build in
  three documented commands or fewer.
- **SC-002**: A person new to the repository answers the five orientation questions in US1
  within 30 minutes using only the site. A person measures this once, before the
  onboarding pages are called done.
- **SC-003**: The built site has zero dead internal links and zero remote resource
  references, checked on every change that touches it.
- **SC-004**: Every page under `docs/` is in exactly one navigation, checked on every
  change that touches it.
- **SC-005**: Project status appears on exactly one page.
- **SC-006**: Zero repo IDs and zero code identifiers in the user guide, checked on every
  change that touches it.
- **SC-007**: Two builds of the same commit are byte-identical.

## Principles Touched

| Principle | How this feature complies |
|---|---|
| I On-device | The site is not the app and adds nothing to the APK: no permission, no dependency in `:app`. It keeps the same promise for its own readers anyway: nothing leaves the site on page load (FR-013), and nothing on it collects data. |
| II Measurement honesty | Pages that describe measurement cite sources and say where the science is uncertain. The user guide explains why a metric is sometimes hidden (US4) and never quotes accuracy the core hasn't shown. |
| III Targets, not identities | No page sorts voices or users into gender categories. The user guide describes targets as parameter sets and presets as optional labels (FR-035). |
| IV Not medical care | No page diagnoses or treats anything. The user guide and FAQ point to professionals (FR-034). User-facing explanations of voice science are written after, or checked in, the SLP review (M6). |
| VI Encouragement, not coercion | The writing guide bans guilt and pressure wording in the user guide, as for content packs. |
| VII Visual-first accessibility | The principle binds the app. The site uses a generator whose default theme supports keyboard navigation and a high-contrast theme, and the writing guide requires alt text for every image. The user guide and privacy policy meet WCAG 2.2 AA before they publish (FR-036). |
| VIII Content as data | The user guide never holds coaching text (FR-033). |
| IX Shared core | No production code changes. The API docs plugin is applied to `:core`'s build for documentation only: it adds no runtime dependency, and `:core` stays free of Android dependencies. |
| X Test-first | Each site check lands with a test that fails before it, in the same change. |
| XI Decisions recorded | Tools and licences are recorded in [ADR-0007](../../docs/adr/0007-docs-site.md) (Accepted). |
| Licensing constraint | Nothing from the docs toolchain enters the app binary. ADR-0007 lists the licence of every tool and every third-party asset in the published site. |

## Play Impact

IDs are from [`docs/play-checklist.md`](../../docs/play-checklist.md).

| Point | Effect | Checklist ID |
|---|---|---|
| App binary, permissions, Data safety form | None. The feature changes nothing in `:app`, the manifest or any shipped dependency. | PLAY-02, PLAY-03, PLAY-04 |
| Privacy policy | Google Play asks apps that use sensitive permissions such as `RECORD_AUDIO` for a privacy policy at a public URL and inside the app, even when no personal data is collected. The site hosts it at a stable address, published as soon as it is written and apart from the user guide (FR-006). | PLAY-01 |
| Store listing consistency | The FAQ and user guide must not contradict the store listing or the Data safety answers ("no data collected or shared"). Publishing the user guide for the closed test lets review check all three together before release. | PLAY-02, PLAY-06, PLAY-07 |
| Health and medical claims | The user guide makes no medical claims (FR-034), consistent with principle IV and the category question OQ-C. | PLAY-05 |
| Deceptive behaviour | The guide describes only behaviour that exists (FR-032), so it can't promise features the app lacks. | PLAY-06 |

## Assumptions

- The site lives on GitHub Pages at the repository's default address. A custom domain
  waits on OQ-B (name and domain).
- The site is English only.
- Diagrams are out of scope until a page needs one.
- The user guide may later be bundled inside the app as offline help. That is out of
  scope here, and nothing in this feature should prevent it. Bundled help needs no
  network, which fits principle I.
- Everything already under `docs/` (the constitution, roadmap, open questions, ADRs,
  salvage notes) is published in the contributor guide, since FR-010 puts every page in
  a navigation. Files outside `docs/` (specs, `CLAUDE.md`, the ledger, source code) are
  linked on GitHub, never rendered. Specs record intent; the site describes what exists.
- PR #28 (Learn and the glossary) merges before the site's first build. If it doesn't,
  Learn enters the navigation when it lands.

## Out of scope

- A wiki outside the repository (pages not reviewed through pull requests).
- Analytics, comments, a hosted search service, or any third-party service on the site.
- Versioned docs per release.
- Translating the user guide.
- In-app help.
