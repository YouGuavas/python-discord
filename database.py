import sqlite3

DB_NAME = "game_data.db"

def connect_db():
    """Establishes a database connection and returns the cursor & connection."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    return conn, cursor

def create_tables():
    """Creates the necessary tables for the bot."""
    conn, cursor = connect_db()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        level INTEGER DEFAULT 1,
        gold INTEGER DEFAULT 0,
        last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        action TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(username) REFERENCES players(username)
    )
    ''')

    conn.commit()
    conn.close()

def add_player(username):
    """Adds a new player if they don’t already exist."""
    conn, cursor = connect_db()

    try:
        cursor.execute("INSERT INTO players (username) VALUES (?)", (username,))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Player {username} already exists.")
    
    conn.close()

def log_action(username, action):
    """Logs player actions (like movement, combat, etc.)."""
    conn, cursor = connect_db()
    cursor.execute("INSERT INTO logs (username, action) VALUES (?, ?)", (username, action))
    conn.commit()
    conn.close()
