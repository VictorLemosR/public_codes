use eyre::Result;
use tracing::{span, Level};
use tracing_subscriber::FmtSubscriber;

pub fn install() -> Result<()> {
    let subscriber = FmtSubscriber::builder()
        .with_max_level(Level::TRACE)
        .finish();
    tracing::subscriber::set_global_default(subscriber)?;
    Ok(())
}

pub fn create_span(name: &str) -> tracing::Span {
    span!(Level::TRACE, "dynamic_span", name)
}
