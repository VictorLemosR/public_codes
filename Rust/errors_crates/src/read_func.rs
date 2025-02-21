use eyre::Result;
use std::fs::File;
use std::io::Read;
use tracing::instrument;

#[instrument]
pub fn read_file(path: &str) -> Result<String> {
    let mut file = File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}
