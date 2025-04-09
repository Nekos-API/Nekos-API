use colored::*;
use diesel::dsl::insert_into;
use diesel::prelude::*;
use futures::{StreamExt, stream};
use nekosapi::db;
use nekosapi::db::models::*;
use nekosapi::db::schema::image_tags::dsl::*;
use nekosapi::db::schema::images::dsl::*;
use nekosapi::db::schema::tags::dsl::*;
use reqwest::Client;
use std::io::{self, Write};
use std::{
    collections::{HashMap, HashSet},
    sync::{Arc, Mutex},
};
use url::Url;

mod load {
    use serde::Deserialize;

    #[derive(Deserialize)]
    pub struct ImagesResponse {
        pub items: Vec<Image>,
        pub count: usize,
    }

    #[derive(Deserialize)]
    pub struct Image {
        pub id: u16,
        pub url: String,
        pub rating: String,
        pub color_dominant: [u8; 3],
        pub color_palette: [[u8; 3]; 9],
        pub tags: Vec<String>,
        pub artist_name: Option<String>,
        pub source_url: Option<String>,
    }
}

fn rgb_to_hex([r, g, b]: &[u8; 3]) -> String {
    format!("{r:X}{g:X}{b:X}")
}

fn get_filename_from_url(url: &String) -> Option<String> {
    Url::parse(&url)
        .ok()
        .and_then(|url| {
            url.path_segments()
                .map(|paths| paths.map(String::from).collect::<Vec<_>>())
        })
        .and_then(|paths| paths.last().cloned())
}

const IMAGES_TO_IMPORT: u16 = 50_000;

#[tokio::main]
async fn main() {
    dotenv::dotenv().ok();

    let mut conn = db::init();

    let images_list = Arc::new(Mutex::new(Vec::<load::Image>::new()));

    println!("🔃 Fetching images from Nekos API v3...");

    {
        let client = Client::new();

        let urls = (0..=(IMAGES_TO_IMPORT / 100))
            .map(|i| {
                format!(
                    "https://api.nekosapi.com/v4/images?limit=100&offset={}",
                    i * 100
                )
            })
            .collect::<Vec<_>>();

        let bodies = stream::iter(urls)
            .map(|url| {
                let client = client.clone();
                tokio::spawn(async move {
                    let resp = client.get(url).send().await?;
                    resp.text().await
                })
            })
            .buffer_unordered(10);

        bodies
            .for_each(|b| async {
                match b {
                    Ok(Ok(text)) => {
                        let mut res: load::ImagesResponse = serde_json::from_str(&text)
                            .expect("Could not parse images from API response.");

                        {
                            let mut images_lock = images_list.lock().unwrap();
                            images_lock.append(&mut res.items);
                        }

                        print!(
                            "{}",
                            format!(
                                "\r   Fetched {} (out of {}) images.",
                                images_list.lock().unwrap().len(),
                                res.count
                            )
                            .dimmed()
                        );
                        io::stdout().flush().unwrap();
                    }
                    Ok(Err(e)) => eprintln!("Got a reqwest::Error: {}", e),
                    Err(e) => eprintln!("Got a tokio::JoinError: {}", e),
                }
            })
            .await;
    }

    println!("\r✅ API images fetched!                      ");

    let images_list = images_list.lock().unwrap();

    let tags_list: HashSet<String> = images_list
        .iter()
        .flat_map(|image| image.tags.clone())
        .collect();

    println!("✅ Tags collected!");

    for (i, tag_name) in tags_list.iter().enumerate() {
        diesel::insert_into(tags)
            .values(Tag {
                id: i
                    .try_into()
                    .expect("Could not convert enumeration counter into i32 for the tag's ID."),
                name: tag_name.to_owned(),
            })
            .execute(&mut conn)
            .expect("Could not insert tag into the database.");
    }

    println!("✅ Tags inserted!");

    let tag_rows = tags
        .select(Tag::as_select())
        .load(&mut conn)
        .expect("Could not fetch tags from database.");

    let tag_map: HashMap<_, _> = tag_rows
        .iter()
        .map(|row| (row.name.clone(), row.id))
        .collect();

    println!("✅ Inserting images into the database...");

    for (i, image) in images_list.iter().enumerate() {
        if i != 0 && i % 500 == 0 {
            print!(
                "\r{}",
                format!("   Inserted {:} (out of {:}) images.", i, images_list.len()).dimmed()
            );
            io::stdout().flush().unwrap();
        }

        let Some(image_file_name) = get_filename_from_url(&image.url) else {
            println!(
                "WARNING: URL '{}' for Image with ID {} could not be parsed. Skipping...",
                image.url, image.id
            );
            continue;
        };

        insert_into(images)
            .values(Image {
                id: image.id.try_into().expect(
                    "Could not convert API's image ID into database's image table ID type.",
                ),
                file_name: image_file_name,
                rating: image.rating.clone(),
                artist_name: image.artist_name.clone(),
                source_url: image.source_url.clone(),
                color_dominant: rgb_to_hex(&image.color_dominant),
                color_palette: image
                    .color_palette
                    .map(|color| rgb_to_hex(&color))
                    .join(","),
            })
            .execute(&mut conn)
            .expect("Could not insert image into database.");

        insert_into(image_tags)
            .values(
                image
                    .tags
                    .iter()
                    .map(|tag_name| ImageTag {
                        image_id: image.id.try_into().expect("Could not convert API's image ID into images_tag table's image_id type."),
                        tag_id: *tag_map
                            .get(tag_name)
                            .expect(
                                "Could not get ID for tag name. Are you updating your database while loading images?"
                            )
                    })
                    .collect::<Vec<ImageTag>>()
            )
            .execute(&mut conn)
            .expect("Could not insert image:tag relationships for image.");
    }

    println!("\r✅ Successfully imported images from v3!");
}
