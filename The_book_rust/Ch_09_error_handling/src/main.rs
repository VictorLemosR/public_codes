use std::fs::File;
use std::io::ErrorKind;
use std::io::{self, Read};
fn main() {
    println!("Hello, world!");
    //panic!("Fodeu")
    let v = vec![1, 2, 3];
    //v[99];
    println!("{}", v[2]);

    const PATH: &str = "C:\\Users\\victor.reial\\Desktop\\hello.txt";
    let f = File::open(PATH);
    handle_error(f);

    //const PATH2: &str = "C:\\Users\\victor.reial\\Desktop\\hello2.txt";
    //let f = File::open(PATH2);
    //handle_error(f);

    const PATH3: &str = "C:\\Users\\victor.reial\\Desktop";
    let f = File::open(PATH3);
    //handle_error(f);
    //File::open(PATH3).unwrap();
    //File::open(PATH3).expect("Failed to open");

    let f = error_to_caller(PATH3);
    println!("{:?}", f);
}

fn handle_error(f: Result<File, std::io::Error>) {
    match f {
        Ok(file) => file,
        Err(e) => match e.kind() {
            ErrorKind::NotFound => panic!("File not found: {:?}", e),
            other_error => panic!("Problem opening the file: {:?}", other_error),
        },
    };
}
//unwrap_or_else para substituir nested matchs
fn handle_error_no_match(path: &str) {
    File::open(path).unwrap_or_else(|error| {
        if error.kind() == ErrorKind::NotFound {
            File::create("hello.txt").unwrap_or_else(|error| {
                panic!("Problem creating the file: {:?}", error);
            })
        } else {
            panic!("Problem opening the file: {:?}", error)
        }
    });
}

fn error_to_caller(path: &str) -> Result<String, std::io::Error> {
    let mut username_file = File::open(path)?;
    let mut username = String::new();
    username_file.read_to_string(&mut username)?;
    Ok(username)

    //Or even shorter
    //let mut username = String::new();
    //
    //File::open("hello.txt")?.read_to_string(&mut username)?;
    //
    //Ok(username)
}

