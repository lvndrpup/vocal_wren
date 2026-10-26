//! Pure-Rust analysis model for Vocal Wren.
//!
//! Holds the [`Frame`] model and the [`Confidence`] type every user-facing
//! metric carries. No FFI lives here; `vt-ffi` maps these types for Kotlin.
#![forbid(unsafe_code)]

mod confidence;
mod frame;

pub use confidence::{Confidence, ConfidenceError};
pub use frame::Frame;
