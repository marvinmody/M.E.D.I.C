
import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parent / "medic.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS inspections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                inspected_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                status TEXT NOT NULL DEFAULT 'pending'
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS hazards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inspection_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT DEFAULT '',
                latitude REAL,
                longitude REAL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (inspection_id) REFERENCES inspections(id)
            )
        """)
