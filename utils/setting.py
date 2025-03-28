import database as db

async def create_tables(channel):
    try:
        db.create_tables()
        db.create_map_tables()
        await channel["message"].send("Tables created!")
    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error creating tables. Check your logs.")

async def log_room(room, north, south, east, west, mobs):
    try:
        room_exists = db.get_room_from_db(room)
        print(room_exists)
        if not room_exists:
            status = db.add_room(room, north, south, east, west)
            if status:
                for mob in mobs:
                    try:
                        if 'noAttack' in mob.keys():
                            db.add_mob(mob["name"], room["curRoom"], room["name"], True)
                        else:
                            db.add_mob(mob["name"], room["curRoom"], room["name"], False)
                        print(f'Logged mob {mob["name"]} in room {room}.')
                    except Exception as e:
                        print(f'Error logging mob {mob["name"]} in room {room["curRoom"]}. Error: {e}')
            else:
                pass
        else:
            pass
    except Exception as e:
        print(f'Error logging room {room["curRoom"]}. Error: {e}')