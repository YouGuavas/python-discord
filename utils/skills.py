import requests

skills = {
            "circumspect": {
                 "name": "Circumspect",
                 "id": "3008",
                 "page": "4"
                 }
        }
async def underling_buff(url, channel, character):
    try:
        print(f"Casting ling buff on {character["character_id"]}")
        requests.get(f"{url}underlings.php?suid={character["character_id"]}&serverid={character["server_id"]}&rg_sess_id={character["session"]["session"]}&claim=1")
    except Exception as e:
            print(f'error: {e}')
            if "message" in channel:
                await channel["message"].send("There was an error casting ling buff. Check your logs.")

async def get_skill_info(url, channel, character, skill_name):
    try:
        
        skill = requests.get(f"{url}skills_info.php?id={skills[skill_name.lower()]["id"]}&suid={character["character_id"]}&serverid={character["server_id"]}&rg_sess_id={character["session"]["session"]}").text
        level = skill.split(f"{skill_name.capitalize()} Level ")[1].split("</")[0]
        await channel["message"].send(f"Skill {skill_name} is level {level}.")
    except Exception as e:
            print(f'error: {e}')
            if "message" in channel:
                await channel["message"].send("There was an error with getting skill info. Check your logs.")

async def cast_skill(url, channel, character, skill_name):
    try:
        skill_name=skill_name.lower()
        print(f"Casting skill {skills[skill_name]["name"]} on {character["character_id"]}")
        data = {            
                "castskillid": skills[skill_name]["id"],
                "cast": "Cast Skill"
            }
        requests.post(f"{url}cast_skills.php?C={skills[skill_name]["page"]}&suid={character["character_id"]}&serverid={character["server_id"]}&rg_sess_id={character["session"]["session"]}&claim=1", data)
    except Exception as e:
            print(f'error: {e}')
            if "message" in channel:
                await channel["message"].send(f"There was an error casting skill {skill["name"]}. Check your logs.")
