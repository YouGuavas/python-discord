from utils.moving import move
from utils.attacking import attack_by_names

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
            await move(url, channel, character, step["direction"])
            await attack_by_names(url, channel, character, mobs)

            i += 1
        await channel["message"].send("Turning.")
    await channel["message"].send("Finished.")

async def astral(url, channel, character, mobs):
        steps = [{"direction": "north", "steps": 4}, 
                {"direction": "east", "steps": 4},
                {"direction": "south", "steps": 4},
                {"direction": "west", "steps": 4},
                #Layer 1 End
                {"direction": "north", "steps": 2},
                {"direction": "east", "steps": 4},
                #Layer 2 Start
                {"direction": "west", "steps": 4},
                {"direction": "south", "steps": 2},


                ]
        for step in steps:
            i = 0 
            while i < step["steps"]:
                await move(url, channel, character, step["direction"])
                await attack_by_names(url, channel, character, mobs)

                i += 1
            await channel["message"].send("Turning.")
        await channel["message"].send("Finished.")