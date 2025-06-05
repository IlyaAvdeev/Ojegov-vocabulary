\connect words;

CREATE TABLE ojegov (
    word VARCHAR(80) NOT NULL,
    explanation TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS word_idx ON ojegov(word) WITH (deduplicate_items = off);