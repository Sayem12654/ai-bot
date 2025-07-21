import sqlite3
import os

DB_FILE = "blogger_bot.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feeds
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 url TEXT UNIQUE,
                 region TEXT)''')
    conn.commit()
    conn.close()

def add_feed(url, region):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO feeds (url, region) VALUES (?, ?)", (url, region))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_feeds():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT url, region FROM feeds")
    feeds = c.fetchall()
    conn.close()
    return feeds

# প্রথম রানে ডাটাবেস ইনিশিয়ালাইজ
if not os.path.exists(DB_FILE):
    init_db()
