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

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

kotlin {
    jvmToolchain(17)
}

dependencies {
    // UniFFI's generated Kotlin (src/main/java/uniffi/, from scripts/build-android.sh) loads the core via JNA.
    // "@aar" picks JNA's Android AAR (with libjnidispatch.so) instead of the desktop JAR.
    implementation("net.java.dev.jna:jna:${libs.versions.jna.get()}@aar")

    testImplementation(libs.junit)
}
