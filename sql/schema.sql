-- Система учёта работ художника: структура SQLite.
CREATE TABLE IF NOT EXISTS collections (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS paints (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    size TEXT NOT NULL DEFAULT '',
    year INTEGER NOT NULL CHECK (year > 0),
    image TEXT NOT NULL DEFAULT '',
    technic TEXT NOT NULL DEFAULT '',
    material TEXT NOT NULL DEFAULT '',
    collection_id INTEGER NOT NULL,
    FOREIGN KEY (collection_id) REFERENCES collections(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_paints_year ON paints(year);
CREATE INDEX IF NOT EXISTS idx_paints_artist ON paints(artist);
CREATE INDEX IF NOT EXISTS idx_paints_collection_id ON paints(collection_id);
