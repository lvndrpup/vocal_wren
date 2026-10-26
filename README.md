# Vocal Wren

Vocal Wren ("Wren Buddy") is a free Android vocal trainer for pitch, resonance and vocal
weight, with plain-language coaching. It is a general-purpose trainer: you choose a
target, and a target is just a set of parameters. Gendered presets exist as optional
shortcuts; the app never asks for or infers your gender.

## Privacy promise

Everything happens on your phone. Audio never leaves the device: the app has no internet
permission, no analytics, no ads and no crash reporting. It never records in the
background.

Wren is a training aid, not medical care. See the [constitution](docs/constitution.md)
for the full set of principles.

## Status

**M0 Foundations.** The app shell and the pure-Kotlin core module build and test in CI;
the app shows `Core 0.1.0 · frame 1`. See the [roadmap](docs/roadmap.md).

## Layout

```
android/    Gradle project "wren": :app (Kotlin, Jetpack Compose) and :core (pure Kotlin:
            analysis, confidence, safety, coaching)
.github/    CI workflow
docs/       Constitution, roadmap, open questions, ADRs
```

## Building

Needs JDK 17 and the Android SDK. Open `android/` in IntelliJ IDEA or Android Studio, or
from a terminal:

```powershell
cd android
.\gradlew.bat :core:test :app:assembleDebug
```

## Contributing and work tracking

Work is tracked with [qew](https://github.com/foundlings/qew); the ledger lives in the
sibling [`vocal_wren-ledger`](https://github.com/lvndrpup/vocal_wren-ledger) repository
(`../vocal_wren-ledger`). Run `qew ready` to see available work. Agents: read
[CLAUDE.md](CLAUDE.md). Decisions are recorded in [docs/adr](docs/adr/).

## Licence

Intended licence: Apache-2.0. The `LICENSE` file is still to be added.
