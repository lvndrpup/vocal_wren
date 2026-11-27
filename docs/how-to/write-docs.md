# How to write a documentation page

This page takes you from "I need to document this" to a page that passes review. Follow
the steps in order: each one narrows the next. It is also the one home for the writing
rules. The [templates](https://github.com/lvndrpup/vocal_wren/tree/main/docs/_templates)
carry structure, and the agents' docs skill carries these steps and links back here.

## 1. Pick the part

The site has three parts, each for one reader. A page belongs to exactly one.

| Part | For | Lives in | Book |
|---|---|---|---|
| Contributor guide | Someone changing Vocal Wren: code, docs or process | `docs/` outside `learn/`, `user/` and `privacy/` | contributor book, `docs/SUMMARY.md` |
| Learn | Someone comfortable with code who wants the voice science behind the app | `docs/learn/` | contributor book, `docs/SUMMARY.md` |
| User guide | Someone using the app to train their voice. They don't program | `docs/user/` | user book, `docs/user/SUMMARY.md` |

The privacy policy is its own one-page book under `docs/privacy/`, written for users
under the user-guide rules.

If a fact matters to both contributors and users, it gets two pages: the user page says
what it means for them, and the contributor page holds the code, the exact message or
the type, and links to the user page.

## 2. Pick the kind

A page does one job. If you find yourself writing two, split the page.

| Kind | For | Template | Lives in |
|---|---|---|---|
| Tutorial | A newcomer learning by doing, start to finish, with a result at the end | `tutorial.md` | `docs/tutorials/` |
| How-to | Someone who knows the basics and has one goal | `how-to.md` | `docs/how-to/` |
| Explanation | Someone who wants to know why things are the way they are | `explanation.md` | `docs/explanation/` |
| Reference | Someone looking up an exact fact: a term, a message, a type | `reference.md` | `docs/reference/` |
| Learn page | A contributor learning one idea of voice science | `learn.md` | `docs/learn/` |
| User task | A user reaching one goal in the app | `user-task.md` | `docs/user/` |
| FAQ entry | A question every new user asks, with a short answer | `faq-entry.md` | a section of `docs/user/faq.md` |

Pages on the contributor's "Start here" path (status, setup, how the app is built) live
in `docs/start/` whatever their kind, so the path reads as one folder.

A decision is not a page kind: it is an ADR in `docs/adr/`, in the MADR 4 format that
[ADR-0000](../adr/0000-record-architecture-decisions.md) describes.

## 3. Copy the template

Copy the template for your kind from `docs/_templates/` into the folder from step 2, and
rename it. A folder that doesn't exist yet is created with its first page. Keep the
template's headings and their order, and replace each instruction with your text. If you
have nothing for a heading, delete it rather than leave it empty.

## 4. Place it in the navigation

Add the page to its book's `SUMMARY.md`, next to the pages a reader meets just before and
after it. The build fails on a page in no `SUMMARY.md` and on a page in two books.
Templates and `docs/site/` are the exceptions and never appear in navigation.

## 5. Write

Follow [the rules](#the-rules), then read the page once as its reader would.

## 6. Check

Run `python scripts/docs/build_site.py` from the repository root. It builds every book
and the API docs, and fails on a page missing from navigation, a dead link or anchor, or
anything that would load from the network. The built site is in `build/site/`; open it
through a local server (`python -m http.server -d build/site`), because the API docs
fetch their navigation.

## The rules

Each rule has its reason. If the reason doesn't apply, raise it in review rather than
quietly breaking the rule.

### Every page

- **One home per fact.** State a fact on one page and link to it everywhere else. Two
  copies drift, and a reader can't tell which one is right.
- **No empty sections.** A heading with nothing under it, or "coming soon", promises a
  page that doesn't exist. Leave the heading out until there is something to say.
- **Status lives on the status page only.** What is built and what isn't changes every
  week. One page can be kept current; twenty can't. Link to it.
- **Absolute dates** (YYYY-MM-DD), never "recently" or "next release".
- **Links to files that aren't published** (specs, `CLAUDE.md`, source code, folders) use
  the file's GitHub URL, so they work on the site and on GitHub alike. mdBook rewrites a
  `.md` link to `.html` without checking it, so a relative link out of `docs/` is dead on
  the site.
- **Same pull request.** A change to behaviour updates its page in the same pull request.
  A page that lags the code is wrong from the day it merges.
- **Targets, not identities.** Describe voices with parameters and directions: higher or
  lower, brighter or darker, lighter or heavier. Never sort voices or people by gender
  (constitution principle III).
- **Not medical care.** No page diagnoses or treats anything. Where pain, hoarseness or
  voice loss comes up, point the reader to a doctor or a speech-language pathologist
  (principle IV).
- **Alt text for every image**, saying what the image shows that the text doesn't. An
  image that adds nothing gets empty alt text (`![](...)`) or is left out.

### Repo IDs in each part

Repo IDs are the project's labels: `ADR-0006`, `OQ-C`, `F1`, `M7`, `D-018`, `PLAY-05`,
qew ids like `043ea4a6u`. The [glossary](../reference/glossary.md) explains each prefix.

- **Contributor guide**: only as links, or in a closing "Decisions" line. `D-018` in
  running text means nothing to a newcomer; [why the Play checklist dates every
  row](https://github.com/lvndrpup/vocal_wren/blob/main/specs/001-docs-site/plan.md#decision-ledger)
  does, and still leads to the decision.
- **Learn**: only where a reader needs to follow up, as a link. Learn is about voice
  science, not about the project.
- **User guide and privacy policy**: never. No IDs, no code, no module names.

### Contributor pages

- **Open with the page's purpose**: one or two sentences on what the reader gets from it,
  before any detail.
- **Every domain term in the glossary.** Link the term the first time a page uses it, and
  add it to the [glossary](../reference/glossary.md) if it isn't there.
- **Explain, don't instruct agents.** Directives for agents belong in `CLAUDE.md` and
  skills; a contributor page explains the fact and the reasoning behind it.

### Learn pages

- **Idea before name.** Explain an idea in plain language, with an example the reader can
  hear or try, before giving its technical name.
- **Every factual claim has a source**, cited by number and listed in a closing Sources
  section. Prefer sources a reader can read for free.
- **Say where the science is uncertain** (principle II). A confident sentence about an
  open question misleads the people who build on it.
- **Learn is background, not product copy.** Text users see in the app comes from content
  packs, not from Learn.

### User guide and privacy policy

- **User words.** Pitch, resonance, weight, session, target; not F0, formant, frame or LPC.
  A technical word a user needs is explained where it first appears.
- **Only what the app does today** on `main`. The user guide must never promise a feature
  the app lacks, and the store listing relies on it (Play checklist
  [PLAY-06](../play-checklist.md)).
- **No coaching text.** The guide explains what coaching is for and what each screen
  shows. The words users see during practice live in content packs (principle VIII).
- **No guilt or pressure.** No streaks, "don't break your chain" or "you missed a day"
  (principle VI).
- **Each message page says what happened and what to do**, in that order.
- **Accessible before it publishes.** The user book and the privacy page meet WCAG 2.2 AA
  before they first publish. The pull request that publishes them records this audit:
  - every image has alt text (see above);
  - headings go in order, one H1, no skipped levels;
  - link text says where it goes, never "here" or "click";
  - any custom CSS keeps text contrast at 4.5:1 or more (3:1 for large text), in both
    light and dark themes;
  - the page works with the keyboard alone, and at 200% zoom.
