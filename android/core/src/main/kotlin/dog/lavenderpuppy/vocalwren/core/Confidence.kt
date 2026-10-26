package dog.lavenderpuppy.vocalwren.core

/**
 * How sure the core is about a measurement, always in `[0, 1]`.
 *
 * Constitution principle II (measurement honesty): every user-facing metric carries a
 * confidence computed in the core, and below threshold the app shows no number, trend or
 * claim. This type guarantees the value is never NaN and never outside `[0, 1]`, so a
 * threshold check on it is always meaningful.
 */
@JvmInline
value class Confidence private constructor(val value: Float) {
    companion object {
        /** Nothing is known: the honest value when nothing was measured. */
        val NONE = Confidence(0f)

        /** Complete certainty. */
        val FULL = Confidence(1f)

        /** Validates [value], rejecting NaN and anything outside `[0, 1]`. */
        fun of(value: Float): Confidence {
            require(!value.isNaN()) { "confidence is NaN" }
            require(value in 0f..1f) { "confidence $value is outside [0, 1]" }
            return Confidence(value)
        }

        /** Clamps [value] into `[0, 1]`. NaN becomes [NONE]: an unknown confidence must never read as a confident one. */
        fun clamped(value: Float): Confidence =
            if (value.isNaN()) NONE else Confidence(value.coerceIn(0f, 1f))
    }
}
