//mod eyre_mod;
//use eyre_mod::{read_file, Result};

mod color_eyre_mod;
use color_eyre_mod::read_file;
use color_eyre::eyre::{Context, Result};

//mod simple_miette;
//use miette::Result;
//use simple_miette::read_file;

//mod miette_mod;
//use miette_mod::{read_file, MyError};
//use miette::{Context, IntoDiagnostic, Result};

//mod error_set_mod;
//use error_set::ResultContext;
//use error_set_mod::{Result, read_file};

//mod read_func;
//use tracing::{error, Level};
//use tracing_error::ErrorLayer;
//use tracing_subscriber::{prelude::*, fmt};
//use tracing::instrument;
//use eyre::Result;

fn fail() -> Result<()>{
    read_file("asrt").wrap_err("oozz")?;
    Ok(())
}

fn main() -> Result<()>{
    color_eyre::install()?;
    fail()?;
    println!("Hello, world!");
    Ok(())
}
