import requests
from urllib.parse import urlencode
from utils.moving import move 
from utils.data_functions import get_attack_data


async def attack_by_names(url, channel, character, mob_names=[]):
    try:
        #This is the room API response
        world_data = requests.get(f'{url}ajax_changeroomb.php?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}').json()
        mobs_in_room = world_data["roomDetailsNew"]
        mob_name_string = ', '.join(mob_names).lower()
        for mob in mobs_in_room:
            if mob["name"]:
                if mob["name"].lower() in mob_name_string:
                    await attack(url, channel, character, mob)
            else:
                pass
    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error with the grouping process. Check your logs.")

async def attack(url, channel, character, mob):
    try:
        data = await get_attack_data(url, channel, character, mob)
        print(data)
        new_results = []
        #This is the attack page
        attack_data = requests.get(f'{url}somethingelse.php?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}&{data}').text
        #print(attack_data)
        if "Found" in attack_data:
            found_item = attack_data.split('Found ')[1].split('</b>')[0]
            #new_results.append(f"{found_item}")
            await channel["message"].reply(f"Found {found_item}")
        won = attack_data.split('var successful = ')[1].split(';')[0]
        print('1')
        results = attack_data.split('battle_result = "')[1].split('"')[0].split("gained")
        print('2')
        for result in results:
            print('result1')
            result = result.split('<br>')[0]
            print('result2')

            if '!' in result:
                result = result.split('!')[0]
            if '</b>' in result:
                result = result.split('</b>')[1]
            new_results.append(result)
        await channel["message"].reply(f"Attacking {mob["name"]}.")
        
        if won == '1':
            pass
            #await channel["message"].reply(f"Won against {mob["name"]}. \nResults: {', '.join(new_results[1:])}")
        else:
            await channel["message"].reply(f"Failed to defeat {mob["name"]}.")
    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error with the attacking process. Check your logs.")

async def attack_in_a_line(url, channel, character, mob_names, loops, direction): 
            counter = 0
            while counter < int(loops):
                await move(url, {"message": channel["message"]}, {"character_id": character["character_id"], "server_id": character["server_id"], "session": character["session"]["session"]}, direction=direction)
                await attack_by_names(url, {"message": channel["message"]}, {"character_id": character["character_id"], "server_id": character["server_id"], "session": character["session"]}, mob_names)
                counter += 1
