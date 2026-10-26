// Pure Kotlin/JVM: no Android dependencies, so the core runs and is tested on any JVM
// (constitution IX and X).
plugins {
    alias(libs.plugins.kotlin.jvm)
}

kotlin {
    jvmToolchain(17)
}

dependencies {
    testImplementation(libs.junit)
}
