# Google Play policy checklist

The Google Play policies Vocal Wren must meet, one row per point. Specs cite these IDs in
their **Play Impact** section (`CLAUDE.md`).

Rules for this file:

- **IDs are stable.** `PLAY-NN` is never renumbered or reused. A point that no longer
  applies is marked *Retired* and stays in the table.
- **Every row has a source and a last-checked date.** Google moves and rewrites policy
  pages, so an old date is the signal to re-read the source (spec 001 D-018). M7's exit
  criteria re-check every row within 30 days of the first upload ([roadmap](roadmap.md)).
- **This file summarises; the linked page is the policy.** When they disagree, the linked
  page wins: fix the row and its date.
- Constitution principles are cited as `I` to `XI` ([constitution](constitution.md)).

Index of all policies: the [Policy Center](https://play.google.com/about/developer-content-policy/),
[policy announcements](https://support.google.com/googleplay/android-developer/announcements/13412212)
and [policy deadlines](https://support.google.com/googleplay/android-developer/table/12921780).

## Checklist

| ID | Point | What Vocal Wren must do | How it complies | Source | Last checked |
|---|---|---|---|---|---|
| PLAY-01 | Privacy policy | Link a privacy policy in the Play Console **and** inside the app. It must be on a public, non-geofenced URL, not a PDF, and name the developer contact, the data collected and shared, security practices, and retention and deletion. Required even when no personal data is collected. | One Markdown source published at `/privacy/` on the docs site and bundled in the app by F14 (spec 001 D-015, ledger `043kotf51`). It states that audio never leaves the device (I). | [User Data](https://support.google.com/googleplay/android-developer/answer/10144311) | 2026-10-29 |
| PLAY-02 | Data safety form | Complete the Data safety section in the Play Console, from the first closed test onward. It must match the privacy policy and the app's real behaviour, including any SDK. Data processed only on the device is generally not "collected". | No `INTERNET` permission and no analytics, ads or crash SDKs (I), so the expected answer is "no data collected or shared". Any change to that answer is a spec-level change. | [Data safety](https://support.google.com/googleplay/android-developer/answer/10787469) | 2026-10-29 |
| PLAY-03 | Microphone (`RECORD_AUDIO`) | Request a sensitive permission only for core functionality promoted in the store listing, use the data only for purposes the user agreed to, and honour a refusal without nagging or manipulation. Show a prominent in-app disclosure first if the use would surprise the user. | Asked in context when a practice session starts (ledger `043eaij52`), audio analysed on the device only, no background recording (I). Denial leaves the rest of the app usable. | [Permissions and APIs that access sensitive information](https://support.google.com/googleplay/android-developer/answer/16558241); [prominent disclosure](https://support.google.com/googleplay/android-developer/answer/11150561) | 2026-10-29 |
| PLAY-04 | Notifications (`POST_NOTIFICATIONS`) | Same general permission rules as PLAY-03. | Requested only after the user opts into reminders (VI). M0 declares no permissions. | [Permissions and APIs that access sensitive information](https://support.google.com/googleplay/android-developer/answer/16558241) | 2026-10-29 |
| PLAY-05 | Health claims | Apps that are not regulated medical devices must not offer misleading or harmful health functionality, and need a disclaimer in the store description that they are not a medical device and do not diagnose, treat, cure or prevent any condition. Apps using device sensors for health functions must say which devices work. Every developer completes the Health apps declaration, even with no health features. | Not medical care (IV): no diagnosis or treatment claims in the app, listing or guide. The listing carries the disclaimer. Device support is stated once M1 spikes measure it. Category waits on OQ-C. | [Health Content and Services](https://support.google.com/googleplay/android-developer/answer/16679511); [Health apps declaration](https://support.google.com/googleplay/android-developer/answer/14738291) | 2026-10-29 |
| PLAY-06 | Deceptive behaviour | The listing, screenshots and description must accurately reflect what the app does. No claims of functions it cannot perform, no hidden features. | The user guide and listing describe only behaviour that exists (spec 001 FR-032). Metrics below confidence threshold are hidden, not guessed (III). | [Deceptive Behavior](https://support.google.com/googleplay/android-developer/answer/17006354) | 2026-10-29 |
| PLAY-07 | Store listing metadata | Title of 30 characters or fewer. No ranking, price or promotional claims in the title, icon or images. Metadata appropriate for all users. | "Vocal Wren" fits. The name waits on OQ-B (trademark). | [Metadata](https://support.google.com/googleplay/android-developer/answer/9898842) | 2026-10-29 |
| PLAY-08 | Target API level | From 2026-08-31, new apps and updates must target Android 16 (API 36) or higher. The bar moves up about once a year, usually each August. | `:app` targets API 36 today. Re-check before the M7 upload (2027-08), when API 37 is likely to be required. | [Target API level requirements](https://support.google.com/googleplay/android-developer/answer/11926878); [developer guide](https://developer.android.com/google/play/requirements/target-sdk) | 2026-10-29 |
| PLAY-09 | Target audience and content rating | Declare the target age groups and whether the app has ads, give app-access instructions, and complete the content rating questionnaire. Misstatements can get the app removed. | No ads (I), no account or login, so no access instructions beyond "none". If children are in the audience the Families policies apply too; deciding the audience is open. | [Target audience and app content](https://support.google.com/googleplay/android-developer/answer/9867159); [content ratings](https://support.google.com/googleplay/android-developer/answer/9859655); [Families](https://support.google.com/googleplay/android-developer/answer/9893335) | 2026-10-29 |
| PLAY-10 | Closed test before production | Personal developer accounts created after 2023-11-13 must run a closed test with at least 12 testers opted in for 14 consecutive days before applying for production access. | M7 runs a closed test with at least 25 testers for four weeks ([roadmap](roadmap.md)). Testers must stay opted in the whole time to count. | [Testing requirements for new personal accounts](https://support.google.com/googleplay/android-developer/answer/14151465) | 2026-10-29 |
| PLAY-11 | Payments and donations | Donations fall under the Payments policy. Rules for linking out to an external page vary by region and programme. | Not applicable while the app takes no money. Any donation mechanism is decided in OQ-D and must not need `INTERNET` (I). Re-read this row then. | [Developer Program Policy](https://play.google.com/about/developer-content-policy/) (Payments) | 2026-10-29 |
| PLAY-12 | Account deletion | Apps that let users create an account must offer in-app and web deletion. | Not applicable: Vocal Wren has no accounts (I). | [Account deletion requirements](https://support.google.com/googleplay/android-developer/answer/13327111) | 2026-10-29 |

## Not applicable today

These policies exist but nothing in Vocal Wren touches them, so they have no row. Add a row
if a spec changes that: ads, in-app purchases and subscriptions, location, contacts,
SMS and call log, all-files access, `QUERY_ALL_PACKAGES`, accessibility services,
foreground services, local network, and AI-generated content.
