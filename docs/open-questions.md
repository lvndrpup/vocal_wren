# Open questions

Questions the owner needs to answer, each with when it must be answered. When one is
resolved, record the answer (usually in an ADR or spec) and link it here.

| ID | Question | Needed by | Notes |
|---|---|---|---|
| OQ-J | Is JNA's `libjnidispatch.so` aligned for 16 KB pages? | First CI run | The CI 16 KB check answers it. If not aligned, find another JNA build or approach. See [ADR-0005](adr/0005-16kb-page-alignment.md). |
| OQ-F | Should confidence be computed per formant, so F2 can be shown for high voices even when F1 is unreliable? | Before the F4 spec | Recommended: yes. Fits principle II (measurement honesty). |
| OQ-T | How does a user move their history to a new phone without breaking principle I (on-device)? | Before M5 | Relates to F14 Privacy & data. |
| OQ-I | Run emulator (instrumented) tests in CI, or test manually? | M1 | See [ADR-0004](adr/0004-github-actions-ci-on-ubuntu.md). |
| OQ-R | Why minSdk 30? | With its ADR | Rationale is a TODO in [ADR-0002](adr/0002-android-kotlin-compose-minsdk-30.md). |
| OQ-D | What donation mechanism is Play-compliant for a free app? | Before M5 | Must not need `INTERNET` in the app (principle I). |
| OQ-B | Are "Wren" / "Wren Buddy" clear for trademark, Play listing and a domain? | Before the first Play upload | |
| OQ-C | Which Play Store category? | Before M7 | Must stay consistent with principle IV (not medical care). |
| OQ-H | Do M1 spike results hold on real, consented voices? | M1 / M2 | Re-check spike conclusions against the M2 corpus. |
| OQ-O | Synthetic oracle tests need their own tolerance file, because the core correctly declines to measure at high pitch where the oracle still reports values. | When the oracle lands (M2) | Tolerance changes need an ADR (principle X). |

## Related

`docs/salvage/voice-trainer.md` (added separately) inventories reusable material from the
older [voice-trainer](https://github.com/lvndrpup/voice-trainer) project.
