use miette::{Context, IntoDiagnostic, Result};
pub fn read_file(path: &str) -> Result<String> {
    Ok(std::fs::read_to_string(path).into_diagnostic().wrap_err("oiee")?)
}
