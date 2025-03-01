import database as db
import requests
from urllib.parse import urlencode

from utils.setting import log_room

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


def get_mob_data(channel, name, quest_mob=False,):

    try:
        #List Data for mob 'name'
        #quest_mob: boolean
        #name: string
        mobs = db.get_mob(quest_mob, name)
        new_mobs = []
        for mob in mobs:
            new_mobs.append(mob[0])
        
        return new_mobs

    except Exception as e:
        print(e)
        if "message" in channel:
            channel["message"].reply(f"There was an error getting mob data for {name}. Check your logs.")

async def get_room_data(url, channel, character):
    room = requests.get(f'{url}ajax_changeroomb.php?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}').json()
    data = {}
    available_moves = []
    mobs = room["roomDetailsNew"]
    data['current_room'] = room['curRoom']
    data['north'] = room['north']
    data['south'] = room['south']
    data['east'] = room['east']
    data['west'] = room['west']
    data['map'] = room['name']
    
    await log_room({"curRoom": room['curRoom'], "name": room['name']}, room['north'], room['south'], room['east'], room['west'], mobs)

    for key in data:
        if key !='current_room':
            if data[key] != '0':
                available_moves.append(key)
    return {"data": data, "available_moves":available_moves, "mobs": mobs}




async def get_attack_data(url, channel, character, mob):
    try:
        h = mob["h"]
        spawnId = mob["spawnId"]
        #This is the mob page
        world_mob_data = await requests.get(f'{url}mob.php?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}&h={h}&id={spawnId}')
        if world_mob_data.status_code == 200:
            data = world_mob_data.text.split('somethingelse.php?')[1].split('"')[0]
            #await channel["message"].reply(f"Successfully grabbed mob data for {mob["name"]}.")
            return data
    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error grabbing mob data. Check your logs.")


async def get_talk_data(url, channel, character, mob):
    try:
        h = mob["h"]
        spawnId = mob["spawnId"]
        data = []
        #This is the mob page
        world_mob_data = requests.get(f'{url}mob.php?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}&h={h}&id={spawnId}')

        if world_mob_data.status_code == 200:
            raw_quests = world_mob_data.text.split('Available Quests')[1].split("</table>")[0].split('</b>')
            for quest in raw_quests:
                if 'mob_talk.php' in quest:
                    name = quest.split('<b>')[-1]
                    href = quest.split('href="mob_talk.php?')[1].split('"')[0]
                    step_id = href.split('stepid=')[1].split('&')[0]
                    quest_id = href.split('questid=')[1].split("'")[0]


                    data.append({"name": name, "href": href, "step_id": step_id, "quest_id": quest_id})
                #await channel["message"].reply(f"{name}")

            await channel["message"].reply(f"Successfully grabbed talk data for {mob["name"]}.")
            return data
    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error grabbing talk data. Check your logs.")