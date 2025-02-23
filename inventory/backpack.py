import requests


async def get_contents(url, channel, character, type):
    contents = requests.get(f"{url}ajax/backpackcontents.php?suid={character["character_id"]}&serverid={character["server_id"]}&rg_sess_id={character["session"]["session"]}&tab={type}").text
    slots = contents.split('<div class="backpackSlot')
    full_slots = []
    for slot in slots:
        if "alt=" in slot:
            name = slot.split('alt="')[1].split('"')[0]
            full_slots.append(name)
    return full_slots

async def has_enough_items(url : str, channel, character, type : str="quest", names : list=[""], cap : int=1):
    contents = await get_contents(url, channel, character, type)
    for name in names:
        i = 0
        for item in contents:
            if item in names:
                if i <= cap:
                    i += 1
            