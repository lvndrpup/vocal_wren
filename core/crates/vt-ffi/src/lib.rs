//! The only crate Kotlin sees. Thin uniffi exports over `vt-analysis`;
//! no analysis logic lives here.

uniffi::setup_scaffolding!();

/// One analysis frame as seen by Kotlin.
///
/// Constitution principle II (measurement honesty): `f0_hz` is `None` when
/// nothing was measured, and the app must not show a pitch whose
/// `f0_confidence` (always in `[0, 1]`) is below threshold.
#[derive(Debug, Clone, Copy, PartialEq, uniffi::Record)]
pub struct Frame {
    pub index: u64,
    pub f0_hz: Option<f32>,
    pub f0_confidence: f32,
}

impl From<vt_analysis::Frame> for Frame {
    fn from(frame: vt_analysis::Frame) -> Self {
        Self {
            index: frame.index,
            f0_hz: frame.f0_hz,
            f0_confidence: frame.f0_confidence.get(),
        }
    }
}

/// The core's version, e.g. `"0.1.0"`.
#[uniffi::export]
pub fn core_version() -> String {
    env!("CARGO_PKG_VERSION").to_owned()
}

/// The M0 round-trip frame: index 1, nothing measured, zero confidence.
#[uniffi::export]
pub fn hello_frame() -> Frame {
    vt_analysis::Frame::hello().into()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn hello_frame_round_trips_honestly() {
        assert_eq!(
            hello_frame(),
            Frame {
                index: 1,
                f0_hz: None,
                f0_confidence: 0.0,
            }
        );
    }

    #[test]
    fn core_version_is_workspace_version() {
        assert_eq!(core_version(), "0.1.0");
    }
}
