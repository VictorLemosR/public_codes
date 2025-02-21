use std::{
    fs,
    io::{prelude::*, BufReader},
    net::{TcpListener, TcpStream},
    thread,
    time::Duration,
};
fn main() {
    //Non-admin can only listen to port 1024 and above
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        handle_connection(stream);
    }
}

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&mut stream);
    let request_line = buf_reader.lines().next().unwrap().unwrap();

    let (status_line, contents) = match &request_line[..] {
        "GET /m HTTP/1.1" => (
            "HTTP/1.1 200 Ok",
            fs::read_to_string("html_file.html").unwrap(),
        ),
        "GET /s HTTP/1.1" => {
            thread::sleep(Duration::from_secs(5));
            (
                "HTTP/1.1 200 Ok",
                fs::read_to_string("html_file.html").unwrap(),
            )
        }
        _ => (
            "HTTP/1.1 404 NOT FOUND",
            fs::read_to_string("html_file.html").unwrap(),
        ),
    };
    let length = contents.len();
    let response = format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");
    stream.write_all(response.as_bytes()).unwrap();

    println!("{:#?}", request_line);
}
