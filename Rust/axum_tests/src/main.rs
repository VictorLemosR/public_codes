mod errors;
mod web;

pub use self::errors::{Error, Result};
use axum::extract::{Path, Query};
use axum::middleware;
use axum::response::{Html, IntoResponse, Response};
use axum::{
    routing::{get, post},
    Router,
};
use serde::Deserialize;
use tower_cookies::CookieManagerLayer;

#[tokio::main]
async fn main() {
    let routes_all = Router::new()
        .merge(routes_hello())
        .merge(web::routes_login::routes())
        .merge(routes_static())
        .layer(middleware::map_response(main_response_mapper))
        .layer(CookieManagerLayer::new());
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000")
        .await
        .expect("Tokio could not bind the address");
    axum::serve(listener, routes_all)
        .await
        .expect("Axum could not create the route");
}

async fn main_response_mapper(res: Response) -> Response {
    println!("->> main_response_mapper function; main.rs");
    println!();
    res
}

#[derive(Debug, Deserialize)]
struct HelloParams {
    name: Option<String>,
}
async fn handler_hello(Query(params): Query<HelloParams>) -> impl IntoResponse {
    println!("->> handler_hello function; main.rs");
    //Exemplo de query /hello?name=Victor
    let name = params.name.as_deref().unwrap_or("World!");
    Html(format!("Hello <strong>{name}!</strong>"))
}

async fn handler_hello2(Path(name): Path<String>) -> impl IntoResponse {
    println!("->> handler_hello2 function; main.rs");
    Html(format!("Hello <strong>{name}!</strong>"))
}

fn routes_hello() -> Router {
    Router::new()
        .route("/hello", get(handler_hello))
        .route("/hello2/{name}", get(handler_hello2))
}

fn routes_static() -> Router {
    let user_routes = Router::new().route("/{id}", get(|| async {}));

    let team_routes = Router::new().route("/", post(|| async {}));

    let api_routes = Router::new()
        .nest("/users", user_routes)
        .nest("/teams", team_routes);

    Router::new().nest("/api", api_routes)

    // Our app now accepts
    // - GET /api/users/{id}
    // - POST /api/teams
}
