import sqlite3
from typing import Dict, Any, List

class DatabaseConnection:
    def __init__(self, db_path=':memory:'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.init_schema()

    def init_schema(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE,
                password_hash TEXT,
                role TEXT,
                created_at REAL
            );
            """)
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS task_jobs (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                payload TEXT,
                status TEXT,
                retry_count INTEGER,
                created_at REAL
            );
            """)
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                amount_cents INTEGER,
                currency TEXT,
                paid INTEGER,
                created_at REAL
            );
            """)

    def execute_query(self, query: str, params: tuple = ()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor.fetchall()
