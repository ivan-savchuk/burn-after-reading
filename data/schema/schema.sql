
CREATE TABLE secrets_to_share (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NULL,
    secret TEXT NOT NULL,
    -- this hash_link will be formed from user_email + salt + secret itself
    hash_link TEXT UNIQUE,
    passphrase_applied INTEGER DEFAULT 0,
    expiration_time TEXT DEFAULT "7d",
    burned INTEGER DEFAULT 0,
    viewed INTEGER DEFAULT 0,
    creation_datetime TEXT NOT NULL
);

CREATE TABLE app_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_key TEXT UNIQUE
);