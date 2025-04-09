CREATE TABLE IF NOT EXISTS images (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    rating TEXT NOT NULL,
    artist_name TEXT,
    source_url TEXT,
    color_dominant TEXT NOT NULL,
    color_palette TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS image_tags (
    image_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    FOREIGN KEY (image_id) REFERENCES images (id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE,
    PRIMARY KEY (image_id, tag_id)
);