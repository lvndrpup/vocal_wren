package dog.lavenderpuppy.vocalwren.core

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test

class FrameTest {
    @Test
    fun helloFrameIsIndexOne() {
        assertEquals(1L, Frame.hello().index)
    }

    @Test
    fun helloFrameClaimsNoPitch() {
        val frame = Frame.hello()
        assertNull(frame.f0Hz)
        assertEquals(Confidence.NONE, frame.f0Confidence)
    }
}
