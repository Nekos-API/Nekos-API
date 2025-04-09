use crate::db::models::{Image as DbImage, ImageTag as DbImageTag, Tag as DbTag};
use crate::db::schema::image_tags::dsl::{image_id, image_tags};
use crate::db::schema::images::dsl::{artist_name, id, images, rating};
use crate::db::schema::tags::dsl::{name, tags};
use crate::state::State;
use axum::{Extension, Json, http::StatusCode};
use axum_extra::extract::Query;
use diesel::prelude::*;
use schemas::{Error, Image, PaginatedResponse, Rating};
use serde::{Deserialize, Deserializer};
use serde_json::Value;
use std::sync::Arc;
use tokio::sync::Mutex;
mod schemas;

fn deserialize_list<'de, D>(deserializer: D) -> Result<Vec<String>, D::Error>
where
    D: Deserializer<'de>,
{
    let s = String::deserialize(deserializer)?;
    Ok(s.split(',')
        .map(str::trim)
        .filter(|s| !s.is_empty())
        .map(String::from)
        .collect())
}

#[derive(Deserialize)]
pub struct Pagination {
    pub limit: Option<usize>,
    pub offset: Option<usize>,

    #[serde(default, deserialize_with = "deserialize_list")]
    pub rating: Vec<String>,

    #[serde(default, deserialize_with = "deserialize_list")]
    pub artist: Vec<String>,

    #[serde(default, deserialize_with = "deserialize_list")]
    pub tags: Vec<String>,
}

pub async fn search_images(
    Extension(state): Extension<Arc<Mutex<State>>>,
    Query(page): Query<Pagination>,
) -> Result<Json<PaginatedResponse<Image>>, (StatusCode, Json<Value>)> {
    let conn = &mut state.lock().await.conn;

    let limit = page.limit.unwrap_or(100);
    let offset = page.offset.unwrap_or(0);

    if limit > 100 || limit == 0 {
        return Err((
            StatusCode::BAD_REQUEST,
            Json(serde_json::json!(Error {
                message: String::from(
                    "The `limit` query parameter cannot be zero nor bigger than 100."
                ),
            })),
        ));
    }

    let mut query = images.into_boxed();

    if !page.rating.is_empty() {
        query = query.filter(rating.eq_any(page.rating));
    }

    if !page.artist.is_empty() {
        query = query.filter(artist_name.eq_any(page.artist));
    }

    if !page.tags.is_empty() {
        query = query.filter(
            id.eq_any(
                image_tags
                    .inner_join(tags)
                    .select(image_id)
                    .filter(name.eq_any(page.tags)),
            ),
        );
    }

    let result = match query
        .select(DbImage::as_select())
        .limit(limit as i64)
        .offset(offset as i64)
        .load(conn)
    {
        Ok(i) => i,
        Err(e) => {
            dbg!(e);
            return Err((
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!(Error {
                    message: String::from("Could not retrieve images from the database."),
                })),
            ));
        }
    };
    let count: i64 = match images.count().get_result(conn) {
        Ok(c) => c,
        Err(_) => {
            return Err((
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!(Error {
                    message: String::from("Could not count images from the database."),
                })),
            ));
        }
    };

    let result_tag_relationships = match DbImageTag::belonging_to(&result)
        .inner_join(tags)
        .select((DbImageTag::as_select(), DbTag::as_select()))
        .load::<(DbImageTag, DbTag)>(conn)
    {
        Ok(r) => r,
        Err(_) => {
            return Err((
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!(Error {
                    message: String::from(
                        "Could not get image-tag relationships from the database for the resulting images."
                    ),
                })),
            ));
        }
    };

    let result_with_tags: Vec<(DbImage, Vec<DbTag>)> = result_tag_relationships
        .grouped_by(&result)
        .into_iter()
        .zip(result)
        .map(|(rss, image)| (image, rss.into_iter().map(|(_, tag)| tag).collect()))
        .collect();

    Ok(Json(PaginatedResponse {
        items: result_with_tags
            .into_iter()
            .map(|(img, img_tags)| Image {
                id: img.id as i64,
                url: format!(
                    "https://s3.nyeki.dev/nekos-api/images/original/{}",
                    img.file_name
                ),
                rating: Rating::from_string(&img.rating)
                    .expect("The rating retrieved from the database is not a valid rating"),
                tags: img_tags.into_iter().map(|tag| tag.name).collect(),
            })
            .collect(),
        count,
    }))
}
