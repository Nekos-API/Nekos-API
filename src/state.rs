use diesel::SqliteConnection;

pub struct State {
    pub conn: SqliteConnection,
}
