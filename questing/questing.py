import requests
from urllib.parse import urlencode
from utils.getting import get_talk_data

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

async def get_requirements(url, character, name : str):
    quest_log = requests.get(f"{url}world_questHelper.php?serverid={character['server_id']}&suid={character['character_id']}&rg_sess_id={character['session']['session']}").json()["qtable"]
    quests = quest_log.split("show_quest.php?quest=")[1:]
    new_quests = []

    for quest in quests:
        quest_id = quest.split('"')[0]
        if 'getQuestHelpData2' in quest:
            requirements = []
            for requirement in quest.split('getQuestHelpData2'):


                requirement_count = 0
                requirement_max = 0
                if "killed" in requirement:

                    branch_point = requirement.split(": </b>")
                    print(branch_point)
                    requirement_name = branch_point[0].split("<b>")[-1].split("</a>")[0]
                    requirement_count = int(branch_point[1].split("/")[0].replace(',', ''))
                    requirement_max = int(branch_point[1].split(" ")[0].split("/")[-1].replace(',', ''))
                    requirement_type = "kill"
                elif ": </b>" in requirement:

                    branch_point = requirement.split(": </b>")
                    print(branch_point)

                    requirement_name = branch_point[0].split("<b>")[-1].split("</a>")[0]
                    requirement_count = int(branch_point[1].split("/")[0].replace(',', ''))
                    requirement_max = int(branch_point[1].split("</font>")[0].split("/")[-1].replace(',', ''))
                    requirement_type = "pvp"
                elif ":</b> " in requirement:
                    branch_point = requirement.split(":</b> ")
                    print(branch_point)

                    requirement_name = branch_point[0].split("<b>")[-1].split("</a>")[0]
                    requirement_count = int(branch_point[1].split("/")[0].replace(',', ''))
                    requirement_max = int(branch_point[1].split("</a>")[0].split("/")[-1].replace(',', ''))
                    requirement_type = "collect"
                elif "Stripped" in requirement:

                    branch_point = requirement.split(": </b>")
                    print(branch_point)

                    requirement_name = branch_point[0].split("<b>")[-1].split("</a>")[0]
                    requirement_count = int(branch_point[1].split("/")[0].replace(',', ''))
                    requirement_max = int(branch_point[1].split("</a>")[0].split("/")[-1].replace(',', ''))
                    requirement_type = "strip"
                elif "Return" in requirement:

                    branch_point = requirement.split("</b>")
                    print(branch_point)

                    requirement_name = branch_point[0].split("</a>")[0].split("Return to ")[1]
                    requirement_type = "speak"
                else:
                    branch_point = requirement.split(":</b> ")
                    print(branch_point)

                    requirement_name = branch_point[0].split("</a>")[0]
                    requirement_count = int(branch_point[1].split("/")[0].replace(',', ''))
                    requirement_max = int(branch_point[1].split("</a>")[0].split("/")[-1].replace(',', ''))

                    requirement_type = "unknown"
                requirement = {"name": requirement_name, "count": requirement_count, "max": requirement_max, "type": requirement_type}
                requirements.append(requirement)
                
            #if not "div align" in quest_id:
            quest_name = quest.split("</svg> ")[2].split("</span")[0]
            quest = {"name": quest_name, "id": quest_id, "requirements": requirements}
            print(quest)

