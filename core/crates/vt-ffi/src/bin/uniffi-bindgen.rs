//! Generates the Kotlin bindings; see `scripts/build-android.sh`.

fn main() {
    uniffi::uniffi_bindgen_main();
}
