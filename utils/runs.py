from utils.moving import move_by_direction, a_star_move
from utils.attacking import attack_by_names
from utils.getting import get_mob_data

async def alsayic(url, channel, character, mobs):
    steps = [{"direction": "north", "steps": 16}, 
             {"direction": "east", "steps": 16},
             {"direction": "south", "steps": 16},
             {"direction": "west", "steps": 16},
             #Layer 1 End
             {"direction": "north", "steps": 8},
            {"direction": "east", "steps": 2},
            #Layer 2 Start
            {"direction": "north", "steps": 6},
            {"direction": "east", "steps": 12},
            {"direction": "south", "steps": 12},
            {"direction": "west", "steps": 12},
            {"direction": "north", "steps": 6},



             ]
    for step in steps:
        i = 0 
        while i < step["steps"]:
            await move_by_direction(url, channel, character, step["direction"])
            await attack_by_names(url, channel, character, mobs)

            i += 1
        await channel["message"].send("Turning.")
    await channel["message"].send("Finished.")

async def astral(self, url, channel, character, mobs):

    steps = await get_mob_data(channel, mobs, False)

    for step in enumerate(steps):
        next_room = steps[step[0]+1]
        await a_star_move(self, url, channel, character, next_room)
        await attack_by_names(url, channel, character, mobs)

    await channel["message"].send("Finished.")  
