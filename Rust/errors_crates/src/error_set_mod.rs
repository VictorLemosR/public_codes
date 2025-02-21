pub type Result<T> = core::result::Result<T, ErrorSet>;

error_set::error_set! {
    ErrorSet = {
        #[display("Could not read file: {}")]
        IoErr(std::io::Error),
    };
}

pub fn read_file(path: &str) -> Result<String> {
    Ok(std::fs::read_to_string(path)?)
}
