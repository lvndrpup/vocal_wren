// Pure Kotlin/JVM: no Android dependencies, so the core runs and is tested on any JVM
// (constitution IX and X).
plugins {
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.dokka)
}

kotlin {
    jvmToolchain(17)
}

// API docs for the docs site (/dev/api/). The stdlib and JDK links are off so the build
// reads nothing from the network (spec 001 D-008).
dokka {
    dokkaSourceSets.configureEach {
        enableKotlinStdLibDocumentationLink.set(false)
        enableJdkDocumentationLink.set(false)
    }
}

dependencies {
    testImplementation(libs.junit)
}
