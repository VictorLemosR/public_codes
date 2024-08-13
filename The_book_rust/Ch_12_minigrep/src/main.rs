use std::env;
use std::process;

use Ch_12_minigrep::Config;

fn main() {
    let config = Config::build(env::args()).unwrap_or_else(|err| {
        eprintln!("Problem parsing arguments: {}", err);
        process::exit(1);
    });

    println!("Searching for {}", config.query);
    println!("In file {}\n", config.file_path);

    //doesn't need to be unwrapped because we are not using the result of fn run
    if let Err(e) = Ch_12_minigrep::run(config) {
        eprintln!("Application error: {}", e);
        process::exit(1);
    };
}

//cargo run -- How poem.txt
//
//set IGNORE_CASE=1
//cargo run -- how poem.txt > output.txt
