use color_eyre::eyre::{eyre, Context, Result};
use reqwest::{Client, Url};
use scraper::{Html, Selector};

#[derive(Debug)]
struct CrawlCommand {
    url: Url,
    extract_links: bool,
}

#[tokio::main]
async fn main() {
    let _ = color_eyre::install();

    let client = Client::new();
    let start_url = Url::parse("https://www.google.org").unwrap();
    let crawl_command = CrawlCommand {
        url: start_url,
        extract_links: true,
    };
    match visit_page(&client, &crawl_command).await {
        Ok(links) => println!("Links: {links:#?}"),
        Err(err) => println!("Could not extract links: {err:#}"),
    }
}

async fn visit_page(client: &Client, command: &CrawlCommand) -> Result<Vec<Url>> {
    println!("Checking {}", command.url);

    let response = client.get(command.url.clone()).send().await?;
    if !response.status().is_success() {
        return Err(eyre!("{}", response.status()));
    }

    let mut link_urls = Vec::new();
    if !command.extract_links {
        return Ok(link_urls);
    }

    let base_url = response.url().to_owned();
    let body_text = response.text().await?;
    let document = Html::parse_document(&body_text);
    println!("->> document; visit_page function; main.rs\n{:?}", document);

    let selector = Selector::parse("a").unwrap();
    let href_values = document
        .select(&selector)
        .filter_map(|e| e.value().attr("href"));
    for href in href_values {
    println!("->> href; visit_page function; main.rs\n{:?}", href);
        match base_url.join(href) {
            Ok(link_url) => link_urls.push(link_url),
            Err(err) => println!("On {base_url:#}: ignored unparsable {href:?}: {err}"),
        }
    }

    Ok(link_urls)
}
