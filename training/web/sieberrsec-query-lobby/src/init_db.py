import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""CREATE TABLE users (
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL
);""")

users = [
    ('admin', '0XThlEITLBPzkIeHCxqY6afyY'),
    ('guest','password123'),
    ('o levels','is a huge pain'),
    ('human1','fafdafafdfdfdasf'),
    ('spheal','r0ll1ng_4r0und'),
    ('garbled useradsf','4ctu4lly_my_4cc0unt'),
    ('i ran out of usernames','this is not falg')
]

conn.executemany("INSERT INTO users VALUES (?, ?)", users)

conn.commit()
conn.close()
