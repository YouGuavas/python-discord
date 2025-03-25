import requests
from urllib.parse import urlencode
from utils.moving import move_by_direction 
from utils.getting import get_attack_data


async def attack_by_names(url, channel, character, mob_names=[], excluded=[]):
    try:
        #This is the room API response
        world_data = requests.get(f'{url}ajax_changeroomb.php?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}').json()
        mobs_in_room = world_data["roomDetailsNew"]
        final_names = []
        for name in mob_names:
            if name not in excluded:
                final_names.append(name)
            
        mob_name_string = ', '.join(final_names).lower()
        found_items = []
        for mob in mobs_in_room:
            if mob["name"]:
                if mob["name"].lower() in mob_name_string:
                    found = await attack(url, channel, character, mob)
                    if found:
                        await channel["message"].reply(f"{character["character_name"]} found {found}.")
                        found_items.append(found)
            else:
                pass
        return found_items
    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error with the grouping process. Check your logs.")

async def attack(url, channel, character, mob):
    try:

        data = await get_attack_data(url, channel, character, mob)

        new_results = []
        #This is the attack page
        attack_data = requests.get(f'{url}somethingelse.php?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}&{data}').text

        if "Found" in attack_data:
            found_item = attack_data.split('Found ')[1].split('</b>')[0]
            #new_results.append(f"{found_item}")
            return found_item
        won = attack_data.split('var successful = ')[1].split(';')[0]
        results = attack_data.split('battle_result = "')[1].split('"')[0].split("gained")
        for result in results:
            result = result.split('<br>')[0]

            if '!' in result:
                result = result.split('!')[0]
            if '</b>' in result:
                result = result.split('</b>')[1]
            new_results.append(result)
        #await channel["message"].reply(f"Attacking {mob["name"]}.")
        
        if won == '1':
            print(f"{character["character_name"]} won against {mob["name"]}")
            #await channel["message"].reply(f"Won against {mob["name"]}. \nResults: {', '.join(new_results[1:])}")
        else:
            await channel["message"].reply(f"{character["character_name"]} failed to defeat {mob["name"]}.")
    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error with the attacking process. Check your logs.")


async def spam_attack(url, channel, character, mob_names, loops):
    counter = 0
    while counter < int(loops):
        await attack_by_names(url, {"message": channel["message"]}, {"character_id": character["character_id"], "server_id": character["server_id"], "session": character["session"]}, mob_names)
        counter += 1

async def attack_in_a_line(url, channel, character, mob_names, loops, direction): 
            counter = 0
            while counter < int(loops):
                await move_by_direction(url, {"message": channel["message"]}, {"character_id": character["character_id"], "server_id": character["server_id"], "session": character["session"]["session"]}, direction=direction)
                await attack_by_names(url, {"message": channel["message"]}, {"character_id": character["character_id"], "server_id": character["server_id"], "session": character["session"]}, mob_names)
                counter += 1
