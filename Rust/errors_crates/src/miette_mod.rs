use miette::{Diagnostic, IntoDiagnostic, NamedSource, SourceSpan};
use thiserror::Error;
pub type Result<T> = core::result::Result<T, MyError>;

#[derive(Error, Diagnostic, Debug)]
pub enum MyError {
    #[error("pau")]
    #[diagnostic(help("matheus gayzao"))]
    Io {
        #[source_code]
        src: NamedSource<String>,
        #[label("Error occurred here")]
        span: SourceSpan,
    },
}

impl From<(std::io::Error, String, SourceSpan)> for MyError {
    fn from((error, src, span): (std::io::Error, String, SourceSpan)) -> Self {
        MyError::Io {
            src: NamedSource::new(src, format!("IO error: {}", error)),
            span,
        }
    }
}

impl MyError {
    pub fn new() -> Self {
        MyError::Io {
            src: NamedSource::new(file!(), "oieee".to_string()),

            span: SourceSpan::new(0.into(), 3),
        }
    }
}

pub fn read_file(path: &str) -> Result<String> {
    Ok(std::fs::read_to_string(path).map_err(|e| {
        let src = NamedSource::new(file!().to_string(), e.to_string());
        let span = SourceSpan::new(9.into(), 3);
        MyError::Io {
            src: src,
            span: span,
        }
    })?)
}
