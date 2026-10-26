package dog.lavenderpuppy.vocalwren.core

import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Test

class ConfidenceTest {
    @Test
    fun acceptsValuesInRange() {
        for (value in listOf(0f, 0.25f, 1f)) {
            assertEquals(value, Confidence.of(value).value)
        }
    }

    @Test
    fun rejectsNaN() {
        assertThrows(IllegalArgumentException::class.java) { Confidence.of(Float.NaN) }
    }

    @Test
    fun rejectsOutOfRange() {
        for (value in listOf(-0.01f, 1.01f, Float.POSITIVE_INFINITY, Float.NEGATIVE_INFINITY)) {
            assertThrows(IllegalArgumentException::class.java) { Confidence.of(value) }
        }
    }

    @Test
    fun clampsOutOfRange() {
        assertEquals(Confidence.NONE, Confidence.clamped(-3f))
        assertEquals(Confidence.FULL, Confidence.clamped(1.5f))
        assertEquals(Confidence.FULL, Confidence.clamped(Float.POSITIVE_INFINITY))
        assertEquals(Confidence.of(0.5f), Confidence.clamped(0.5f))
    }

    @Test
    fun clampsNaNToNone() {
        assertEquals(Confidence.NONE, Confidence.clamped(Float.NaN))
    }
}
