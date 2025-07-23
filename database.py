import sqlite3
from pathlib import Path

DB_FILE = Path('planner.db')


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        start DATETIME,
        end DATETIME,
        color TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS water (
        day DATE PRIMARY KEY,
        glasses INTEGER DEFAULT 0
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS mood (
        day DATE PRIMARY KEY,
        mood TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS checklist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        checked INTEGER DEFAULT 0,
        parent_id INTEGER,
        FOREIGN KEY(parent_id) REFERENCES checklist(id)
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        item TEXT,
        liked INTEGER DEFAULT 0
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )''')
    conn.commit()
    conn.close()

