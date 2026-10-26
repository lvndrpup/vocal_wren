package dog.lavenderpuppy.vocalwren.corebridge

import uniffi.vt_ffi.Frame
import uniffi.vt_ffi.coreVersion
import uniffi.vt_ffi.helloFrame as ffiHelloFrame

/** One analysis frame as the app sees it. [f0Hz] is null when nothing was measured. */
data class HelloFrame(val index: Long, val f0Hz: Float?, val f0Confidence: Float)

/** The app's only door into the Rust core (generated `uniffi.vt_ffi` bindings stay internal to this module). */
object CoreBridge {
    fun version(): String = coreVersion()

    fun helloFrame(): HelloFrame = ffiHelloFrame().toHelloFrame()
}

internal fun Frame.toHelloFrame(): HelloFrame =
    HelloFrame(index = index.toLong(), f0Hz = f0Hz, f0Confidence = f0Confidence)
