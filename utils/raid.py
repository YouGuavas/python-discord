import requests
from urllib.parse import urlencode
from urllib.request import urlopen
from utils.getting import get_room_data


async def raid_by_name(url, channel, character, raid_name, joiners):
    try:
        #This is the room API response
        room_data = await get_room_data(url, character)
        mobs = room_data["mobs"]
        for mob in mobs:
            if mob["name"]:
                if mob["name"].lower() == raid_name.lower():
                    if mob["canForm"]:
                        await raid(url, channel, character, mob, joiners)
            else:
                pass
    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error with spotting. Check your logs.")
async def raid(url, channel, character, mob, joiners):
    try:
        data = {
            "formtime": "3",
            "submit": "Join this Raid!",
            "bomb": "none"
        }
        encoded_data = urlencode(data).encode('UTF-8')
        raid = urlopen(f"{url}formraid.php?suid={character["character_id"]}&serverid={character["server_id"]}&rg_sess_id={character["session"]["session"]}&h={mob["h"]}", data=encoded_data).read()
        print(raid)
        #link = requests.post(f"{url}joinraid.php?suid={character["character_id"]}&serverid={character["server_id"]}&rg_sess_id={character["session"]["session"]}&h={mob["h"]}&target={f"M{mob["mobId"]}"}", data=data, headers=headers, allow_redirects=False).text
        return
    
    except Exception as e:
            print(e)
            if "message" in channel:
                await channel["message"].reply("There was an error with raiding. Check your logs.")