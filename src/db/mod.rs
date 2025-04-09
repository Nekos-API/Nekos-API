pub mod models;
pub mod schema;
use diesel::{Connection, RunQueryDsl, SqliteConnection, sql_query};
use std::env;

pub fn init() -> SqliteConnection {
    let db_url = env::var("DATABASE_URL")
        .expect("No database URL was provided. Make sure to set DATABASE_URL in your .env file.");

    let mut conn = SqliteConnection::establish(&db_url)
        .expect(&format!("Could not connect to database {db_url}."));

    sql_query("PRAGMA journal_mode = WAL; PRAGMA foreign_keys = ON;")
        .execute(&mut conn)
        .expect("Could not set SQLite pragma.");

    conn
}
