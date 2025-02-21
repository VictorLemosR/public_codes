use color_eyre::eyre::Result;
pub fn read_file(path: &str) -> Result<String> {
    Ok(std::fs::read_to_string(path)?)
}
