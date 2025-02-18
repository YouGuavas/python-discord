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
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER,
        room INTEGER PRIMARY KEY,
        north INTEGER,
        south INTEGER,
        east INTEGER,
        west INTEGER
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        room INTEGER,
        FOREIGN KEY(room) REFERENCES rooms(room)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quest_mobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        room INTEGER,
        FOREIGN KEY(room) REFERENCES rooms(room)
    )
    ''')


    conn.commit()
    conn.close()

def list_tables():
    """Lists tables for the bot."""
    conn, cursor = connect_db()

    res = cursor.execute("SELECT name FROM sqlite_master")
    tables = res.fetchall()
    conn.close()
    return tables
def list_rooms():
    """Lists rooms for the bot."""
    conn, cursor = connect_db()

    res = cursor.execute("SELECT room FROM rooms")
    rooms = res.fetchall()
    conn.close()
    return rooms

def list_mobs(quest_mobs, room=None):
    """Lists rooms for the bot."""
    conn, cursor = connect_db()
    if room: 
        if quest_mobs:
            res = cursor.execute(f"SELECT name, room FROM quest_mobs WHERE room = {room}")
        else:
            res = cursor.execute(f"SELECT name, room FROM mobs WHERE room = {room}")
    else:
        if quest_mobs:
            res = cursor.execute(f"SELECT name, room FROM quest_mobs")
        else:
            res = cursor.execute(f"SELECT name, room FROM mobs")
    mobs = res.fetchall()
    conn.close()
    return mobs

def room_data(room):
    """Lists tables for the bot."""
    conn, cursor = connect_db()

    res = cursor.execute(f"SELECT room, north, south, east, west FROM rooms WHERE room = {room}")
    room = res.fetchone()
    conn.close()
    return room

def add_player(username):
    """Adds a new player if they don’t already exist."""
    conn, cursor = connect_db()

    try:
        cursor.execute("INSERT INTO players (username) VALUES (?)", (username,))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Player {username} already exists.")
    
    conn.close()

def add_room(room, north, south, east, west):
    conn, cursor = connect_db()
    
    try:
        cursor.execute("INSERT INTO rooms (room, north, south, east, west) VALUES (?, ?, ?, ?, ?)", (room, north, south, east, west))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Room {room} already exists.")
    
    conn.close()
def add_mob(name, room, quest_mob):
    conn, cursor = connect_db()
    
    try:
        if not quest_mob:
            cursor.execute("INSERT INTO mobs (name, room) VALUES (?, ?)", (name, room))
            print(f"Mob {name} added.")
        else:
            cursor.execute("INSERT INTO quest_mobs (name, room) VALUES (?, ?)", (name, room))
            print(f"Quest mob {name} added.")

        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Mob {name} already exists.")
    
    conn.close()
def log_action(username, action):
    """Logs player actions (like movement, combat, etc.)."""
    conn, cursor = connect_db()
    cursor.execute("INSERT INTO logs (username, action) VALUES (?, ?)", (username, action))
    conn.commit()
    conn.close()
