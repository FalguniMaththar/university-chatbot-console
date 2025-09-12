import sqlite3
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_DIR = os.path.join(BASE_DIR, 'db')
DB_PATH = os.path.join(DB_DIR, 'university.db')

def _connect():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _connect()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT UNIQUE,
            answer TEXT,
            tags TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_faq(question: str, answer: str, tags: str = ""):
    conn = _connect()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO faqs(question, answer, tags) VALUES(?, ?, ?)', (question.strip(), answer.strip(), tags))
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        cur.execute('UPDATE faqs SET answer = ?, tags = ? WHERE question = ?', (answer.strip(), tags, question.strip()))
        conn.commit()
        return None
    finally:
        conn.close()

def list_faqs():
    conn = _connect()
    cur = conn.cursor()
    cur.execute('SELECT id, question, answer, tags FROM faqs ORDER BY id')
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def import_from_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    count = 0
    for item in data:
        q = item.get('question') or item.get('q')
        a = item.get('answer') or item.get('a')
        tags = item.get('tags', '')
        if q and a:
            add_faq(q, a, tags)
            count += 1
    return count