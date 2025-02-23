from inventory.backpack import get_contents
from utils.moving import move_by_direction, a_star_move, room_teleport
from utils.attacking import attack_by_names
from utils.getting import get_mob_data

async def orbs(url, channel, character):
    steps = [
        {"direction": "west", "steps": 2},
        {"direction": "north", "steps": 15},
        {"direction": "east", "steps": 7},
        {"direction": "west", "steps": 14},
        {"direction": "south", "steps": 14},
        {"direction": "east", "steps": 1},
                {"direction": "north", "steps": 14},
        {"direction": "east", "steps": 1},
                {"direction": "south", "steps": 14},
        {"direction": "east", "steps": 1},
                {"direction": "north", "steps": 14},
        {"direction": "east", "steps": 1},
                {"direction": "south", "steps": 14},

        {"direction": "east", "steps": 1},
                {"direction": "north", "steps": 14},
        {"direction": "east", "steps": 1},
                {"direction": "south", "steps": 14},
        #midpoint
        {"direction": "east", "steps": 2},
                {"direction": "north", "steps": 14},
        {"direction": "east", "steps": 1},
                {"direction": "south", "steps": 14},
        {"direction": "east", "steps": 1},
                {"direction": "north", "steps": 14},

        {"direction": "east", "steps": 1},
                {"direction": "south", "steps": 14},
        {"direction": "east", "steps": 1},
                {"direction": "north", "steps": 14},
    ]

    mobs = {
        "Initiate of Slight": "Orb of Slight",
        "Initiate of Strength": "Orb of Inner Strength",
        "Descendant of Destiny": "Orb of Destiny",
        "Descendant of Will": "Orb of Will",
    }
    excluded_mobs = []
    


    
        

    
    await room_teleport(url, channel, character, "10")
    for step in steps:
        i = 0 
        while i < step["steps"]:
            orbs = {
                "Orb of Slight": 0,
                "Orb of Inner Strength": 0,
                "Orb of Destiny": 0,
                "Orb of Will": 0
            }
            orb_contents = await get_contents(url, channel, character, "orb")
            for orb in orb_contents:
                if orb in orbs.keys():
                    orbs[orb] += 1
            for mob in mobs.keys():
                if orbs[mobs[mob]] >= 3:
                    if mob not in excluded_mobs:
                        excluded_mobs.append(mob)
            print(excluded_mobs)
            await move_by_direction(url, channel, character, step["direction"])
            await attack_by_names(url, channel, character, mobs.keys(), excluded_mobs)

            i += 1
        await channel["message"].send("Turning.")
    await channel["message"].send("Finished.")
    return



async def orbs2(url, channel, character):
    steps = [
        {"direction": "north", "steps": 14},
        {"direction": "east", "steps": 1},
        {"direction": "south", "steps": 14},
        {"direction": "east", "steps": 1},
                {"direction": "north", "steps": 14},
        {"direction": "east", "steps": 1},
                {"direction": "south", "steps": 14},
        {"direction": "east", "steps": 1},
                {"direction": "north", "steps": 14},
        {"direction": "east", "steps": 1},
                {"direction": "south", "steps": 14},

        {"direction": "east", "steps": 1},
                {"direction": "north", "steps": 14},
        {"direction": "east", "steps": 1},
                {"direction": "south", "steps": 14},
        #midpoint
        {"direction": "east", "steps": 2},
                {"direction": "north", "steps": 14},
        {"direction": "east", "steps": 1},
                {"direction": "south", "steps": 14},
        {"direction": "east", "steps": 1},
                {"direction": "north", "steps": 14},

        {"direction": "east", "steps": 1},
                {"direction": "south", "steps": 14},
        {"direction": "east", "steps": 1},
                {"direction": "north", "steps": 14},
    ]

    mobs = {
        "Conscript of Focus": "Orb of Focus",
        "Conscript of the Gathering": "Orb of the Gathering",
        "Conscript of the Elements": "Orb of the Elements",

        "Patron of Malice": "Orb of Malice",
        "Patron of Melee": "Orb of Melee",
                "Patron of the Order": "Orb of the Order",

    }
    excluded_mobs = []
    


    
        

    
    for step in steps:
        i = 0 
        while i < step["steps"]:
            orbs = {
                "Orb of Focus": 0,
                "Orb of the Gathering": 0,
                "Orb of the Elements": 0,
                "Orb of Malice": 0,
                                "Orb of Melee": 0,
                                                "Orb of the Order": 0


            }
            orb_contents = await get_contents(url, channel, character, "orb")
            for orb in orb_contents:
                if orb in orbs.keys():
                    orbs[orb] += 1
            print(orbs)
            for mob in mobs.keys():
                if orbs[mobs[mob]] >= 3:
                    if mob not in excluded_mobs:
                        excluded_mobs.append(mob)
            print(excluded_mobs)
            await move_by_direction(url, channel, character, step["direction"])
            await attack_by_names(url, channel, character, mobs.keys(), excluded_mobs)

            i += 1
        await channel["message"].send("Turning.")
    await channel["message"].send("Finished.")
    return

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



async def astral(url, channel, character, mobs):
    steps = [
            {"direction": "east", "steps": 3},
            
            {"direction": "north", "steps": 2}, 
            {"direction": "east", "steps": 4},
            {"direction": "south", "steps": 4},
            {"direction": "west", "steps": 4},
            #Layer 1 End
            {"direction": "north", "steps": 2},
            {"direction": "east", "steps": 4},
            {"direction": "west", "steps": 7},            


            ]
    for step in steps:
        i = 0 
        while i < step["steps"]:
            await move_by_direction(url, channel, character, step["direction"])
            await attack_by_names(url, channel, character, mobs)

            i += 1
        await channel["message"].send("Turning.")
    await channel["message"].send("Finished.")
async def holy(url, channel, character, mobs):
    steps = [{"direction": "north", "steps": 18}, 
             {"direction": "west", "steps": 1},
             {"direction": "south", "steps": 18},
             {"direction": "west", "steps": 1},
             {"direction": "north", "steps": 18}, 
             {"direction": "west", "steps": 1},
             {"direction": "south", "steps": 16},
             #Layer 1 End
            {"direction": "west", "steps": 13},
            {"direction": "south", "steps": 1},
            {"direction": "east", "steps": 13},
            {"direction": "south", "steps": 1},
            {"direction": "west", "steps": 13},
            {"direction": "south", "steps": 1},
            {"direction": "east", "steps": 13},
            {"direction": "south", "steps": 1},

             ]
    for step in steps:
        i = 0 
        while i < step["steps"]:
            await move_by_direction(url, channel, character, step["direction"])
            await attack_by_names(url, channel, character, mobs)

            i += 1
        await channel["message"].send("Turning.")
    await channel["message"].send("Finished.")


async def astral2(self, url, channel, character, mobs):

    steps = await get_mob_data(channel, mobs, False)

    for step in enumerate(steps):
        next_room = steps[step[0]+1]
        await a_star_move(self, url, channel, character, next_room)
        await attack_by_names(url, channel, character, mobs)

    await channel["message"].send("Finished.")  
