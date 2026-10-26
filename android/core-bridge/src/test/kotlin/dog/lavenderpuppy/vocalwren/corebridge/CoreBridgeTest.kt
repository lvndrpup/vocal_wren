package dog.lavenderpuppy.vocalwren.corebridge

import org.junit.Assert.assertEquals
import org.junit.Test
import uniffi.vt_ffi.Frame

// Pure mapping tests: constructing the generated record does not load libvt_ffi.so.
class CoreBridgeTest {
    @Test
    fun `unmeasured frame maps to null pitch and zero confidence`() {
        val frame = Frame(index = 1uL, f0Hz = null, f0Confidence = 0.0f).toHelloFrame()

        assertEquals(HelloFrame(index = 1L, f0Hz = null, f0Confidence = 0.0f), frame)
    }

    @Test
    fun `measured frame keeps pitch and confidence`() {
        val frame = Frame(index = 42uL, f0Hz = 220.5f, f0Confidence = 0.9f).toHelloFrame()

        assertEquals(HelloFrame(index = 42L, f0Hz = 220.5f, f0Confidence = 0.9f), frame)
    }
}
