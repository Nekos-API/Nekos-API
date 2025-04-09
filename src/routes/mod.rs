use std::sync::Arc;

use axum::{Extension, Router, routing::get};
use tokio::sync::Mutex;

use crate::state::State;

mod images;

pub fn init(state: State) -> Router {
    Router::new()
        .route("/v5/images", get(images::search_images))
        .layer(Extension(Arc::new(Mutex::new(state))))
}
