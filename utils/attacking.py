import requests
from urllib.parse import urlencode

async def attack_by_names(url, channel, character, mob_names=[]):
    try:
        #This is the room API response
        world_data = requests.get(f'{url}ajax_changeroomb.php?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}').json()
        mobs_in_room = world_data["roomDetailsNew"]
        #print(f"Mobs in room: {mobs_in_room}")
        mob_name_string = ', '.join(mob_names).lower()
        for mob in mobs_in_room:
            #print(f"Mob in room: {mob}")
            if mob["name"]:
                if mob["name"].lower() in mob_name_string:
                    #print(f"Final Mob: {mob}")
                    await attack(url, channel, character, mob)
                else:
                    await channel["message"].reply("That mob is not in this room.")
            else:
                pass
    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error with the grouping process. Check your logs.")

async def attack(url, channel, character, mob):
    try:
        data = await get_mob_data(url, channel, character, mob)
        #This is the attack page
        attack_data = requests.get(f'{url}somethingelse.php?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}&{data}')
        await channel["message"].reply(f"Attacking {mob["name"]}")
    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error with the attacking process. Check your logs.")

async def get_mob_data(url, channel, character, mob):
    try:
        h = mob["h"]
        spawnId = mob["spawnId"]
        #print(f"h: {h}, spawnId: {spawnId}")
        #This is the mob page
        world_mob_data = requests.get(f'{url}mob.php?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}&h={h}&id={spawnId}')
        if world_mob_data.status_code == 200:
            data = world_mob_data.text.split('somethingelse.php?')[1].split('"')[0]
            await channel["message"].reply(f"Successfully grabbed mob data for {mob["name"]}.")
            return data
    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error grabbing mob data. Check your logs.")
