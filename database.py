import sqlite3

GAME_DB = "game_data.db"
MAP_DB = "map_data.db"
PLAYER_DB = "player_data.db"
#### MAIN ####
def connect_db(DB):
    """Establishes a database connection and returns the cursor & connection."""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    return conn, cursor

def update_table(table, column):
    #Updates table
    conn, cursor = connect_db()

    cursor.execute(f'''
            ALTER TABLE IF EXISTS {table} ADD COLUMN {column}
                   ''')
    conn.close()

def create_map_tables():
    conn, cursor = connect_db(MAP_DB)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER,
        room INTEGER PRIMARY KEY,
        north INTEGER,
        south INTEGER,
        east INTEGER,
        west INTEGER,
        map TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        room INTEGER,
        map TEXT,
        FOREIGN KEY(room) REFERENCES rooms(room),
        FOREIGN KEY(map) REFERENCES rooms(map)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quest_mobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        room INTEGER,
        map TEXT,
        FOREIGN KEY(room) REFERENCES rooms(room),
        FOREIGN KEY(map) REFERENCES rooms(map)
    )
    ''')
    conn.commit()
    conn.close()
    
def create_tables():
    """Creates the necessary tables for the bot."""
    conn, cursor = connect_db(PLAYER_DB)

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        level INTEGER DEFAULT 1,
        server TEXT DEFAULT 'sigil',
        user_id INTEGER UNIQUE,
        power INTEGER DEFAULT 10,
        ele_power INTEGER DEFAULT 0,
        chaos INTEGER DEFAULT 0,
        ele_res INTEGER DEFAULT 0,
        max_rage INTEGER DEFAULT 0,                    
        gold INTEGER DEFAULT 0,
        crew TEXT DEFAULT 'none'
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


def list_tables(db):
    """Lists tables for the bot."""
    conn, cursor = connect_db(db)

    res = cursor.execute("SELECT name FROM sqlite_master")
    tables = res.fetchall()
    conn.close()
    return tables






##### PLAYERS ###########

def add_player(username):
    """Adds a new player if they don’t already exist."""
    conn, cursor = connect_db(PLAYER_DB)

    try:
        cursor.execute("INSERT INTO players (username) VALUES (?)", (username,))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Player {username} already exists.")
    
    conn.close()


def get_player(username):
    #Checks for player
    conn, cursor = connect_db()
    try:
        cursor.execute("SELECT username FROM players")
        conn.commit()

    except sqlite3.IntegrityError:
        print(f"Player {username} does not exist.")
    conn.close()





##### ACTIONS ###########

def log_action(username, action):
    """Logs player actions (like movement, combat, etc.)."""
    conn, cursor = connect_db()
    cursor.execute("INSERT INTO logs (username, action) VALUES (?, ?)", (username, action))
    conn.commit()
    conn.close()






##### ROOMS ###########

def add_room(room, north, south, east, west):

    conn, cursor = connect_db(MAP_DB)
    added = False
    try:
        room_number = room["curRoom"]
        map_name = room["name"]
        status = cursor.execute("INSERT INTO rooms (room, north, south, east, west, map) VALUES (?, ?, ?, ?, ?, ?)", (room_number, north, south, east, west, map_name))
        conn.commit()
        added = True

    except sqlite3.IntegrityError:
        print(f"Room {room} already exists.")
        added = False
    conn.close()
    return added


def get_room_from_db(room):
    #Used as a status check
    conn, cursor = connect_db(MAP_DB)
    exists = False
    try:
        room_number = room["curRoom"]
        rooms = cursor.execute("SELECT map, room FROM rooms WHERE room = ?", (room_number,))
        conn.commit()
        if len(rooms.fetchall()) > 0:
            exists = True
            rooms = rooms.fetchall()

    except sqlite3.IntegrityError:
        print(f"Room {room} does not exist.")
    conn.close()
    return exists


def room_data(room):
    #Lists DATA about room.
    conn, cursor = connect_db(MAP_DB)

    res = cursor.execute(f"SELECT room, north, south, east, west FROM rooms WHERE room = ?", (room,))
    room = res.fetchone()
    conn.close()
    return room


def list_rooms():
    """Lists rooms for the bot."""
    conn, cursor = connect_db(MAP_DB)

    res = cursor.execute("SELECT map, room FROM rooms")
    rooms = res.fetchall()

    conn.close()
    return rooms





##### MOBS ###########

def get_mob(quest_mob, name):

    conn, cursor = connect_db(MAP_DB)
    try:
        if not quest_mob:
            print(f"Grabbing mob: {name}.")
            res = cursor.execute(f"SELECT name, room FROM mobs WHERE name = ?",  (name,))
            print(f"Mob {name} grabbed.")
            mob = res.fetchall()

        else:
            print(f"Grabbing quest mob: {name}.")
            res = cursor.execute(f"SELECT name, room FROM quest_mobs WHERE name = ?", (name,))
            print(f"Quest mob {name} grabbed.")
            mob = res.fetchone()
        conn.commit()

    except sqlite3.IntegrityError:
        print(f"Could not find mob {name}.")
    conn.close()
    print(f"mob: {mob}")
    return mob


def add_mob(name, room, map, quest_mob):

    conn, cursor = connect_db(MAP_DB)
    try:
        if not quest_mob:
            cursor.execute("INSERT INTO mobs (name, room, map) VALUES (?, ?, ?)", (name, room, map))
            print(f"Mob {name} added.")
        
        else:
            cursor.execute("INSERT INTO quest_mobs (name, room, map) VALUES (?, ?, ?)", (name, room, map))
            print(f"Quest mob {name} added.")
        conn.commit()

    except sqlite3.IntegrityError:
        print(f"Mob {name} already exists.")
    conn.close()


def list_mobs(quest_mobs, room=None):
    #Lists MOBS
    conn, cursor = connect_db(MAP_DB)
    if room: 
        if quest_mobs:
            res = cursor.execute(f"SELECT name,room FROM quest_mobs WHERE room = ?", (room,))
        
        else:
            res = cursor.execute(f"SELECT name,room FROM mobs WHERE room = ?", (room,))
    
    else:
        if quest_mobs:
            res = cursor.execute(f"SELECT name, room FROM quest_mobs")
        
        else:
            res = cursor.execute(f"SELECT name, room FROM mobs")
    mobs = res.fetchall()
    conn.close()
    return mobs