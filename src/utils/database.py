import sqlite3
from datetime import datetime
import os

def init_db():
    conn = sqlite3.connect('mental_health.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  email TEXT UNIQUE, username TEXT UNIQUE, password_hash TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS conversations 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_email TEXT, created_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  conversation_id INTEGER, sender TEXT, content TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def get_db():
    return sqlite3.connect('mental_health.db', check_same_thread=False)

def create_user(email, username, password_hash):
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)",
                 (email, username, password_hash))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def get_user(email, password_hash):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE email=? AND password_hash=?", (email, password_hash))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_conversations(user_email):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, created_at FROM conversations WHERE user_email=? ORDER BY created_at DESC LIMIT 10", (user_email,))
    convs = c.fetchall()
    conn.close()
    return [{"id": c[0], "created_at": c[1]} for c in convs]

def create_conversation(user_email):
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO conversations (user_email, created_at) VALUES (?, ?)",
             (user_email, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conv_id = c.lastrowid
    conn.commit()
    conn.close()
    return conv_id

def get_messages(conv_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT sender, content FROM messages WHERE conversation_id=? ORDER BY timestamp", (conv_id,))
    messages = c.fetchall()
    conn.close()
    return [{"sender": m[0], "content": m[1]} for m in messages]

def save_message(conv_id, sender, content):
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO messages (conversation_id, sender, content, timestamp) VALUES (?, ?, ?, ?)",
             (conv_id, sender, content, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()
