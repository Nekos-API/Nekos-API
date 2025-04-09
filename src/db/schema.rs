// @generated automatically by Diesel CLI.

diesel::table! {
    image_tags (image_id, tag_id) {
        image_id -> Integer,
        tag_id -> Integer,
    }
}

diesel::table! {
    images (id) {
        id -> Integer,
        file_name -> Text,
        rating -> Text,
        artist_name -> Nullable<Text>,
        source_url -> Nullable<Text>,
        color_dominant -> Text,
        color_palette -> Text,
    }
}

diesel::table! {
    tags (id) {
        id -> Integer,
        name -> Text,
    }
}

diesel::joinable!(image_tags -> images (image_id));
diesel::joinable!(image_tags -> tags (tag_id));

diesel::allow_tables_to_appear_in_same_query!(
    image_tags,
    images,
    tags,
);
