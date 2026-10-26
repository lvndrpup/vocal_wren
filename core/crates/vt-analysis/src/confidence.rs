use std::fmt;

/// How sure the core is about a measurement, always in `[0, 1]`.
///
/// Constitution principle II (measurement honesty): every user-facing metric
/// carries a confidence computed in Rust, and below threshold the app shows no
/// number, trend or claim. This type guarantees the value is never NaN and
/// never outside `[0, 1]`, so a threshold check on it is always meaningful.
#[derive(Debug, Clone, Copy, PartialEq, PartialOrd, Default)]
pub struct Confidence(f32);

/// Why a raw value could not become a [`Confidence`].
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ConfidenceError {
    /// The value was NaN.
    NotANumber,
    /// The value was outside `[0, 1]`.
    OutOfRange(f32),
}

impl fmt::Display for ConfidenceError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::NotANumber => write!(f, "confidence is NaN"),
            Self::OutOfRange(value) => write!(f, "confidence {value} is outside [0, 1]"),
        }
    }
}

impl std::error::Error for ConfidenceError {}

impl Confidence {
    /// Nothing is known: the honest value when nothing was measured.
    pub const NONE: Self = Self(0.0);
    /// Complete certainty.
    pub const FULL: Self = Self(1.0);

    /// Validates `value`, rejecting NaN and anything outside `[0, 1]`.
    ///
    /// # Errors
    ///
    /// [`ConfidenceError::NotANumber`] for NaN,
    /// [`ConfidenceError::OutOfRange`] for values outside `[0, 1]`.
    pub fn new(value: f32) -> Result<Self, ConfidenceError> {
        if value.is_nan() {
            Err(ConfidenceError::NotANumber)
        } else if (0.0..=1.0).contains(&value) {
            Ok(Self(value))
        } else {
            Err(ConfidenceError::OutOfRange(value))
        }
    }

    /// Clamps `value` into `[0, 1]`. NaN becomes [`Confidence::NONE`]:
    /// an unknown confidence must never read as a confident one.
    #[must_use]
    pub fn clamped(value: f32) -> Self {
        if value.is_nan() {
            Self::NONE
        } else {
            Self(value.clamp(0.0, 1.0))
        }
    }

    /// The value, guaranteed to be in `[0, 1]`.
    #[must_use]
    pub const fn get(self) -> f32 {
        self.0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn accepts_values_in_range() {
        for value in [0.0, 0.25, 1.0] {
            let confidence = Confidence::new(value).expect("in range");
            assert_eq!(confidence.get().to_bits(), value.to_bits());
        }
    }

    #[test]
    fn rejects_nan() {
        assert_eq!(Confidence::new(f32::NAN), Err(ConfidenceError::NotANumber));
    }

    #[test]
    fn rejects_out_of_range() {
        for value in [-0.01, 1.01, f32::INFINITY, f32::NEG_INFINITY] {
            assert_eq!(
                Confidence::new(value),
                Err(ConfidenceError::OutOfRange(value))
            );
        }
    }

    #[test]
    fn clamps_out_of_range() {
        assert_eq!(Confidence::clamped(-3.0), Confidence::NONE);
        assert_eq!(Confidence::clamped(1.5), Confidence::FULL);
        assert_eq!(Confidence::clamped(f32::INFINITY), Confidence::FULL);
        assert_eq!(Confidence::clamped(0.5), Confidence::new(0.5).unwrap());
    }

    #[test]
    fn clamps_nan_to_none() {
        assert_eq!(Confidence::clamped(f32::NAN), Confidence::NONE);
    }

    #[test]
    fn default_is_none() {
        assert_eq!(Confidence::default(), Confidence::NONE);
    }
}
