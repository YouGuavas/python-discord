import requests
from urllib.parse import urlencode
from utils.data_functions import get_talk_data

async def talk_by_name(url, channel, character, mob_name, quest_name):
    try:
        #This is the room API response
        world_data = requests.get(f'{url}ajax_changeroomb.php?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}').json()
        mobs_in_room = world_data["roomDetailsNew"]
        for mob in mobs_in_room:
            if mob["name"]:
                if mob["name"].lower() == mob_name.lower():
                    await talk(url, channel, character, mob, quest_name)
            else:
                pass
    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error with the grouping process. Check your logs.")
    return

async def talk(url, channel, character, mob, quest_name):
    try:
        data = await get_talk_data(url, channel, character, mob)
        quest = {}
        names = []
        for item in data:
            names.append(item["name"])
            if item["name"].lower() == quest_name.lower():
                quest = item
        if quest == {}:
            await channel["message"].reply(f"Please choose a valid quest for this quest giver! Quests available from {mob["name"]}: {', '.join(names)}")
            return
        if not "finish" in quest["href"]:
            #Checks for second phase of talking
            try:
                quest_progress = requests.get(f"{url}mob_talk.php?{quest["href"]}&serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}").text
                href = quest_progress.split('mob_talk.php?')[1].split('"')[0]
                quest["href"] = href
                await channel["message"].reply(f"Progressing quest: {quest["name"]}.")
            except Exception as e:
                print(e)
                if "message" in channel:
                    await channel["message"].reply("There was an error progressing that step. Check your logs.")

        try:
            quest_finish = requests.get(f"{url}mob_talk.php?{quest["href"]}&serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}").text
            await channel["message"].reply(f"Finishing step on quest: {quest["name"]}.")
            return
        except Exception as e:
            print(e)
            if "message" in channel:
                await channel["message"].reply("There was an error finishing that step. Check your logs.")
    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error with the questing process. Check your logs.")
