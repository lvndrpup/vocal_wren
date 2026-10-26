plugins {
    alias(libs.plugins.android.library)
    alias(libs.plugins.kotlin.android)
}

android {
    namespace = "dog.lavenderpuppy.vocalwren.corebridge"
    compileSdk = 36

    defaultConfig {
        minSdk = 30
    }
}

kotlin {
    jvmToolchain(17)
}

dependencies {
    // UniFFI's generated Kotlin (src/main/java/uniffi/, from scripts/build-android.sh) loads the core via JNA.
    implementation(libs.jna) {
        artifact { type = "aar" }
    }

    testImplementation(libs.junit)
}
