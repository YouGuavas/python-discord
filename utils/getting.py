import database as db

async def list_tables(channel):

    try:
        tables = db.list_tables()
        await channel["message"].send(tables)

    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error listing tables. Check your logs.")


async def list_rooms(channel):
    #Lists all rooms
    try:
        rooms = db.list_rooms()
        print(rooms)

    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error listing rooms. Check your logs.")


async def room_data(channel, room):

    try:
        room = db.room_data(room)
        return room
    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply(f"There was an error finding date for {room}. Check your logs.")


async def list_mobs(channel, quest_mobs, room=None):

    try:
        #Lists all mobs
        #quest_mobs: boolean
        #room (optional): if room number is given, will constrain to that room
        mobs = db.list_mobs(quest_mobs, room)
        print(f"Mobs: {mobs}")
        if room:
            await channel["message"].reply(f"Mobs in room {room}: {mobs}")

    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error listing mobs. Check your logs.")


async def get_mob_data(channel, quest_mob, name):

    try:
        #List Data for mob 'name'
        #quest_mob: boolean
        #name: string
        mob = db.get_mob(quest_mob, name)
        await channel["message"].reply(f"Mob details for {name}: {mob}")

    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply(f"There was an error getting mob data for {name}. Check your logs.")