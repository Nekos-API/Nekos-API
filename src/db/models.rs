use crate::db::schema;
use diesel::prelude::*;

#[derive(Queryable, Selectable, Insertable, Identifiable, Associations)]
#[diesel(table_name = schema::image_tags)]
#[diesel(check_for_backend(diesel::sqlite::Sqlite))]
#[diesel(belongs_to(Image))]
#[diesel(belongs_to(Tag))]
#[diesel(primary_key(image_id, tag_id))]
pub struct ImageTag {
    pub image_id: i32,
    pub tag_id: i32,
}

#[derive(Queryable, Selectable, Insertable, Identifiable)]
#[diesel(table_name = schema::images)]
#[diesel(check_for_backend(diesel::sqlite::Sqlite))]
pub struct Image {
    pub id: i32,
    pub file_name: String,
    pub rating: String,
    pub artist_name: Option<String>,
    pub source_url: Option<String>,
    pub color_dominant: String,
    pub color_palette: String,
}

#[derive(Queryable, Selectable, Insertable, Identifiable)]
#[diesel(table_name = schema::tags)]
#[diesel(check_for_backend(diesel::sqlite::Sqlite))]
pub struct Tag {
    pub id: i32,
    pub name: String,
}
