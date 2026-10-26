use crate::Confidence;

/// One analysis frame of the voice signal.
///
/// Constitution principle II (measurement honesty): `f0_hz` is only `Some`
/// when a pitch was measured, and `f0_confidence` says how far to trust it.
/// Callers must not show a pitch whose confidence is below threshold.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Frame {
    /// Position of this frame in the stream, starting at 1.
    pub index: u64,
    /// Fundamental frequency in hertz, or `None` when nothing was measured.
    pub f0_hz: Option<f32>,
    /// Confidence in `f0_hz`.
    pub f0_confidence: Confidence,
}

impl Frame {
    /// The M0 round-trip frame: index 1, nothing measured, zero confidence.
    #[must_use]
    pub const fn hello() -> Self {
        Self {
            index: 1,
            f0_hz: None,
            f0_confidence: Confidence::NONE,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn hello_frame_is_index_one() {
        assert_eq!(Frame::hello().index, 1);
    }

    #[test]
    fn hello_frame_claims_no_pitch() {
        let frame = Frame::hello();
        assert_eq!(frame.f0_hz, None);
        assert_eq!(frame.f0_confidence, Confidence::NONE);
    }
}
