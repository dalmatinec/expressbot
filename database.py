# database.py
import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_file="bot.db"):
        self.conn = sqlite3.connect(db_file)
        self.create_tables()

    def create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_seen TIMESTAMP,
                last_active TIMESTAMP
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS bans (
                user_id INTEGER PRIMARY KEY,
                ban_date TIMESTAMP
            )
        """)
        self.conn.commit()

    def add_user(self, user_id, username):
        self.conn.execute(
            "INSERT OR REPLACE INTO users (user_id, username, first_seen, last_active) "
            "VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
            (user_id, username)
        )
        self.conn.commit()

    def update_last_active(self, user_id):
        self.conn.execute(
            "UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE user_id = ?",
            (user_id,)
        )
        self.conn.commit()

    def ban_user(self, user_id):
        self.conn.execute(
            "INSERT INTO bans (user_id, ban_date) VALUES (?, CURRENT_TIMESTAMP)",
            (user_id,)
        )
        self.conn.commit()

    def is_banned(self, user_id):
        cursor = self.conn.execute("SELECT 1 FROM bans WHERE user_id = ?", (user_id,))
        return cursor.fetchone() is not None

    def get_all_users(self):
        cursor = self.conn.execute("SELECT user_id FROM users")
        return [row[0] for row in cursor.fetchall()]

    def get_stats(self):
        total_users = self.conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        active_users = self.conn.execute(
            "SELECT COUNT(*) FROM users WHERE last_active > datetime('now', '-24 hours')"
        ).fetchone()[0]
        banned_users = self.conn.execute("SELECT COUNT(*) FROM bans").fetchone()[0]
        return {
            "total_users": total_users,
            "active_users": active_users,
            "banned_users": banned_users
        }