use std::env;
use std::error::Error;
use std::fs;

pub struct Config {
    pub query: String,
    pub file_path: String,
    pub ignore_case: bool,
}

impl Config {
    pub fn build(mut args: impl Iterator<Item = String>) -> Result<Config, &'static str> {
        //First argument is the name of the program
        args.next();

        let query = match args.next() {
            Some(arg) => arg,
            None => return Err("Didn't get a query string"),
        };

        let file_path = match args.next() {
            Some(arg) => arg,
            None => return Err("Didn't get a file path"),
        };

        let ignore_case = env::var("IGNORE_CASE").is_ok();

        Ok(Config {
            query,
            file_path,
            ignore_case,
        })
    }
}

pub fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let contents = fs::read_to_string(config.file_path)?;

    if config.ignore_case {
        for line in search_case_insensitive(&config.query, &contents) {
            println!("{line}");
        }
    } else {
        for line in search(&config.query, &contents) {
            println!("{line}");
        }
    }
    Ok(())
}

pub fn search_case_insensitive<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    //Old way without iterator as explained in chapter 12
    let query = query.to_lowercase();
    let mut line_with_query = vec![];

    for line in contents.lines() {
        if line.to_lowercase().contains(&query) {
            line_with_query.push(line);
        }
    }
    println!("{:?}", line_with_query);
    line_with_query
}

fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    //New way with iterator as explained in chapter 13
    contents.lines().filter(|line| line.contains(query)).collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn case_sensitive() {
        let query = "duct";
        let contents = "\
Rust:
safe, fast, productive.
Pick three.
Duct tape";

        assert_eq!(vec!["safe, fast, productive."], search(query, contents));
    }
    #[test]
    fn case_insensitive() {
        let query = "duCt";
        let contents = "\
Rust, Duct:
safe, fast, productive.
Pick three.";

        assert_eq!(
            vec!["Rust, Duct:", "safe, fast, productive."],
            search_case_insensitive(query, contents)
        );
    }
}
