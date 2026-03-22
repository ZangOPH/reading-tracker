-- Reading Tracker Database Schema

CREATE TABLE titles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    format TEXT CHECK(format IN ('manga', 'manhwa', 'manhua', 'web_novel', 'light_novel', 'book', 'comic', 'audiobook')),
    status TEXT CHECK(status IN ('reading', 'completed', 'dropped', 'plan_to_read')),
    cover_url TEXT,
    source_url TEXT,
    external_id TEXT,
    external_source TEXT CHECK(external_source IN ('mangadex', 'anilist', 'royal_road', 'novelupdates', 'manual')),
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    start_date DATE,
    finish_date DATE,
    narrator TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chapters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title_id INTEGER NOT NULL REFERENCES titles(id) ON DELETE CASCADE,
    chapter_number REAL,
    page_number INTEGER,
    duration_minutes INTEGER,
    read_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE genres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE title_genres (
    title_id INTEGER REFERENCES titles(id) ON DELETE CASCADE,
    genre_id INTEGER REFERENCES genres(id) ON DELETE CASCADE,
    PRIMARY KEY (title_id, genre_id)
);

CREATE TABLE title_tags (
    title_id INTEGER REFERENCES titles(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (title_id, tag_id)
);
