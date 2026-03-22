import sqlite3
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(BASE_DIR, "data", "schema.sql")
DB_PATH = os.path.join(BASE_DIR, "data", "tracker.db")

def init_db():
    """Initialise the SQLite database from schema.sql"""
    
    # Check schema file exists
    if not os.path.exists(SCHEMA_PATH):
        print(f"Error: schema.sql not found at {SCHEMA_PATH}")
        return

    # Read schema
    with open(SCHEMA_PATH, "r") as f:
        schema = f.read()

    # Connect and execute schema
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.executescript(schema)
        conn.commit()
        print(f"Database initialised successfully at {DB_PATH}")
        
        # Confirm tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables created: {[t[0] for t in tables]}")

    except sqlite3.Error as e:
        print(f"Error initialising database: {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
