package dog.lavenderpuppy.vocalwren.core

/**
 * One analysis frame of the voice signal.
 *
 * Constitution principle II (measurement honesty): [f0Hz] is only non-null when a pitch was
 * measured, and [f0Confidence] says how far to trust it. Callers must not show a pitch whose
 * confidence is below threshold.
 */
data class Frame(
    /** Position of this frame in the stream, starting at 1. */
    val index: Long,
    /** Fundamental frequency in hertz, or null when nothing was measured. */
    val f0Hz: Float?,
    val f0Confidence: Confidence,
) {
    companion object {
        /** The M0 frame: index 1, nothing measured, zero confidence. */
        fun hello() = Frame(index = 1, f0Hz = null, f0Confidence = Confidence.NONE)
    }
}
