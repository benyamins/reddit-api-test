-- SCHEMA
-- data: {url, title, subreddit, permalink}


CREATE TABLE IF NOT EXISTS Saved (
    Id INTEGER PRIMARY KEY,
    UploadedUrl TEXT,
    Title TEXT,
    Subreddit TEXT,
    RedditLink TEXT,
    CreateDate REAL,
    Updvoted INTEGER
)
