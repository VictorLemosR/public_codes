use futures::executor::block_on;
use tokio::sync::mpsc;
use anyhow::Result;
use futures::future;
use std::collections::HashMap;

#[tokio::main]
async fn main() {
    println!("Async tokio");
    tokio::spawn(async_count_sp(20));
    println!("Async futures");
    block_on(async_main(5));
    println!("Async tokio");
    async_count_await(10).await;
    println!("No async");
    count(3);
    println!("Hello, world!");

    //Using channels
    let (sender, receiver) = mpsc::channel(3);
    let ping_handler_task = tokio::spawn(ping_handler(receiver));

    for i in 1..11 {
        sender.send(()).await.expect("Failed to send ping");
        println!("Sent {i} pings so far.");
    }


    //Using join
    let urls: [&str; 4] = [
        "https://google.com",
        "https://httpbin.org/ip",
        "https://play.rust-lang.org/",
        "BAD_URL",
    ];
    let futures_iter = urls.into_iter().map(size_of_page);
    let results = future::join_all(futures_iter).await;
    let page_sizes_dict: HashMap<&str, Result<usize>> =
        urls.into_iter().zip(results.into_iter()).collect();
    println!("{page_sizes_dict:?}");
}

async fn async_count_sp(count: i32) {
    for i in 0..count {
        println!("Spawn {i}");
        tokio::time::sleep(tokio::time::Duration::from_millis(30)).await;
    }
}

async fn async_count_await(count: i32) {
    for i in 0..count {
        println!("Await: {i}");
        tokio::time::sleep(tokio::time::Duration::from_millis(30)).await;
    }
}

async fn async_count(count: i32) {
    for i in 0..count {
        println!("Block: {i}");
        tokio::time::sleep(tokio::time::Duration::from_millis(30)).await;
    }
}

async fn async_main(count: i32) {
    async_count(count).await;
}

fn count(count: i32) {
    for i in 0..count {
        println!("No async: {i}");
    }
}

async fn ping_handler(mut input: mpsc::Receiver<()>){
    let mut count = 0;

    while let Some(_) = input.recv().await {
        count += 1;
        println!("Received {count} pings");
    }
    println!("pings done");
}


async fn size_of_page(url: &str) -> Result<usize> {
    let resp = reqwest::get(url).await?;
    Ok(resp.text().await?.len())
}
