plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
}

android {
    namespace = "dog.lavenderpuppy.vocalwren"
    compileSdk = 36

    defaultConfig {
        applicationId = "dog.lavenderpuppy.vocalwren"
        minSdk = 30
        targetSdk = 36
        versionCode = 1
        versionName = "0.1.0"

        // The Rust core is only built for these ABIs (scripts/build-android.sh). Without this
        // filter JNA's 32-bit libs would ship and a 32-bit device would crash loading vt_ffi.
        ndk {
            abiFilters += listOf("arm64-v8a", "x86_64")
        }
    }

    buildFeatures {
        compose = true
    }
}

kotlin {
    jvmToolchain(17)
}

dependencies {
    implementation(project(":core-bridge"))

    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.material3)
    implementation(libs.androidx.activity.compose)
}
