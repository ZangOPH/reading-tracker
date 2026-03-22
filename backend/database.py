import sqlite3
import os

# Path to database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "tracker.db")

def get_connection():
    """Get a database connection with row factory set."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Returns rows as dicts instead of tuples
    conn.execute("PRAGMA foreign_keys = ON")  # Enforce foreign key constraints
    return conn
