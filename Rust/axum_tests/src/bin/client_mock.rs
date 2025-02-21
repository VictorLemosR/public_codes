use serde_json::json;

#[tokio::main]
async fn main() {
    let hc = httpc_test::new_client("http://localhost:3000").expect("Erro ao abrir a pagina");
    hc.do_get("/hello2/asrrrss").await.expect("Error ao abrir / ").print().await.unwrap();
    hc.do_get("/hello3/asrrrss").await.expect("Error ao abrir / ").print().await.unwrap();

    hc.do_post("/api/login", json!({
        "username": "demo1",
        "password": "welcomed"
    })).await.expect("Error ao abrir /api/login ").print().await.unwrap();

}
