package dog.lavenderpuppy.vocalwren

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import dog.lavenderpuppy.vocalwren.corebridge.CoreBridge

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    HelloFrameScreen()
                }
            }
        }
    }
}

@Composable
private fun HelloFrameScreen() {
    val version = remember { CoreBridge.version() }
    val frame = remember { CoreBridge.helloFrame() }
    Box(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        contentAlignment = Alignment.Center,
    ) {
        // Plain Text is read by TalkBack as-is; no extra semantics needed.
        Text(
            text = stringResource(R.string.hello_frame, version, frame.index),
            style = MaterialTheme.typography.headlineSmall,
        )
    }
}
