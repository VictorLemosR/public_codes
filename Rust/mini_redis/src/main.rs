use mini_redis::{Connection, Frame};
use tokio::net::{TcpListener, TcpStream};

use std::io::Result;

#[tokio::main]
async fn main() -> Result<()> {
    let listener = TcpListener::bind("127.0.0.1:6379").await?;

    loop {
        let (socket, _) = listener.accept().await?;
        tokio::spawn(async move {
            process(socket).await.unwrap();
        });
    }

    Ok(())
}

async fn process(socket: TcpStream) -> Result<()> {
    let mut connection = Connection::new(socket);

    if let Some(frame) = connection
        .read_frame()
        .await
        .expect("to be able to read frame")
    {
        println!("Got frame: {frame:?}");
        let response = Frame::Error("unimplemented".to_string());
        connection.write_frame(&response).await?;
    };

    Ok(())
}
