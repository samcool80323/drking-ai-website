CREATE TABLE IF NOT EXISTS submissions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  practice TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT NOT NULL,
  consent INTEGER DEFAULT 1,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS submissions_created_at_idx ON submissions (created_at DESC);