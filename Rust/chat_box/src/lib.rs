use color_eyre::eyre::Result;
pub mod openai;
pub mod utils;
pub mod app;
#[cfg(feature = "hydrate")]
#[wasm_bindgen::prelude::wasm_bindgen]
pub fn hydrate() {
    use app::App;
    leptos::logging::log!("Hydrate running");
    console_error_panic_hook::set_once();
    leptos::mount::hydrate_body(App);
}
