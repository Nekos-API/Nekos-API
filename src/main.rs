use dotenv;
use state::State;
mod db;
mod routes;
mod state;

#[tokio::main]
async fn main() {
    dotenv::dotenv().ok();

    let conn = db::init();

    let router = routes::init(State { conn });

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, router).await.unwrap();
}
