#[cfg(feature = "ssr")]
mod vector_store;
#[cfg(feature = "ssr")]
mod assistant;
#[cfg(feature = "ssr")]
mod msg;
#[cfg(feature = "ssr")]
mod client;
#[cfg(feature = "ssr")]
mod thread;
#[cfg(feature = "ssr")]
mod start_bot;

#[cfg(feature = "ssr")]
pub use client::AI;
#[cfg(feature = "ssr")]
pub use thread::run_thread_msg;
#[cfg(feature = "ssr")]
pub use start_bot::start;


pub const DEFAULT_QUERY: &[(&str, &str)] = &[("limit", "100")];
