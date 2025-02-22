from inventory.backpack import get_contents
from utils.login import login, logout 
from utils.moving import move_by_direction, a_star_search, move_to_room
from utils.attacking import attack_by_names, attack_in_a_line, spam_attack
from utils.runs import alsayic, astral, holy, orbs
from utils.questing import talk_by_name
from utils.data_functions import get_room_data
from utils.setting import create_tables
from utils.getting import list_tables, list_rooms, room_data, list_mobs, get_mob_data
from utils.raid import raid_by_name
from utils.skills import underling_buff, get_skill_info, cast_skill
import asyncio
from discord.ext import commands

from config import OW_USERNAME, OW_PASSWORD
SERVER = "sigil"
BASE=f"https://{SERVER}.outwar.com/"

if SERVER == "torax":
    SERVERID = 2
else:
    SERVERID = 1

chars = ["000000"]

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rg_sess = {}

    #Login Commands
    @commands.command()
    async def sess(self, ctx):
        await ctx.send(self.rg_sess)
    @commands.command()
    async def login(self, ctx, character_id=chars[0]):
        await login(BASE, OW_USERNAME, OW_PASSWORD, {"message": ctx}, {"session": self.rg_sess, "server_id": SERVERID, "character_id": character_id}, login)
        current_room = await(get_room_data(BASE, {"message": ctx}, {"session": self.rg_sess, "server_id": SERVERID, "character_id": character_id}))
        current_room = current_room["data"]["current_room"]
        await self.bot.add_cog(Attacking(self.bot, self.rg_sess, character_id))
        await self.bot.add_cog(Inventory(self.bot, self.rg_sess, character_id))
        await self.bot.add_cog(Moving(self.bot, current_room, self.rg_sess, character_id))
        await self.bot.add_cog(Skilling(self.bot, self.rg_sess, character_id))


        await ctx.send(f"Current room: {current_room}")

    @commands.command()
    async def logout(self, ctx):
        await logout(BASE, {"message": ctx}, {"session": rg_sess, "server_id": SERVERID, "character_id": chars[0]})
        rg_sess = {}


    @commands.command()
    #Ping
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    #Create Tables
    async def create(self, ctx):
        await create_tables({"message": ctx})

    @commands.command()
    #List Tables
    async def list(self, ctx):
        await list_tables({"message": ctx})

    @commands.command()
    #List Rooms
    async def rooms(self, ctx):
        await list_rooms({"message": ctx})
    
    @commands.command()
    #Gets Room Data
    async def room_data(self, ctx, room):
        await room_data({"message": ctx}, room)

    @commands.command()
    #Gets Quest Mobs
    async def quest_mobs(self, ctx):
        await list_mobs({"message": ctx}, True)
    
    @commands.command()
    #Gets Normal Mobs
    async def mobs(self, ctx, room=None):
        await list_mobs({"message": ctx}, False, room)
    
    @commands.command()
    #Gets Mob Data -- broken
    async def mob(self, ctx, name):
        await get_mob_data({"message": ctx}, name, False)
    
    @commands.command()
    #Gets Quest Mob Data -- broken
    async def quest_mob(self, ctx, name):
        await get_mob_data({"message": ctx}, name, True)
    
    
class Attacking(commands.Cog):
    def __init__(self, bot, rg_sess, character_id):
        self.bot = bot
        self.rg_sess = rg_sess
        self.character_id = character_id

    #Attacking Commands
    @commands.command()
    async def attack(self, ctx, *mob_names):
        await attack_by_names(BASE, {"message": ctx}, {"character_id": self.character_id, "server_id": SERVERID, "session": self.rg_sess}, mob_names)
    
    @commands.command()
    async def zerx(self, ctx, loops):
        await spam_attack(BASE, {"message": ctx}, {"character_id": self.character_id, "server_id": SERVERID, "session": self.rg_sess}, ["Zerx, Gladiator Titan"], int(loops))
    
    @commands.command()
    async def potshot(self, ctx, loops, direction, *mob_names):
        if int(loops):
            counter = 0
            while counter < int(loops):
                await move_by_direction(BASE, {"message": ctx}, {"character_id": self.character_id, "server_id": SERVERID, "session": self.rg_sess}, direction=direction)
                await attack_by_names(BASE, {"message": ctx}, {"character_id": self.character_id, "server_id": SERVERID, "session": self.rg_sess}, mob_names)
                counter += 1
            await ctx["message"].reply("Finished.")
        else:
            ctx.send("Please choose a number of loops.")

class Inventory(commands.Cog):
    def __init__(self, bot, rg_sess, character_id):
        self.bot = bot
        self.rg_sess = rg_sess
        self.character_id = character_id
    @commands.command()
    async def get_bp(self, ctx):
        contents = await get_contents(BASE, {"message": ctx}, {"character_id": self.character_id, "server_id": SERVERID, "session": self.rg_sess}, "regular")
        if len(contents) == 0:
            await ctx.send("Backpack is empty!")
            return
        for item in contents:
            print(item)
    @commands.command()
    async def get_orbs(self, ctx):
        contents = await get_contents(BASE, {"message": ctx}, {"character_id": self.character_id, "server_id": SERVERID, "session": self.rg_sess}, "orb")
        if len(contents) == 0:
            await ctx.send("Orbs backpack is empty!")
            return
        for item in contents:
            print(item)
        

        
class Moving(commands.Cog):
    def __init__(self, bot, current_room, rg_sess, character_id):
        self.bot = bot
        self.current_room = current_room
        self.rg_sess = rg_sess
        self.character_id = character_id

    #Moving Commands
    @commands.command()
    async def north(self, ctx, steps=1):
        i = 0
        while i < steps:
            await move_by_direction(BASE, {"message": ctx}, {"character_id": self.character_id, "server_id": SERVERID, "session": self.rg_sess}, direction="north")
            i += 1
    
    @commands.command()
    async def south(self, ctx, steps=1):
        i = 0 
        while i < steps:
            await move_by_direction(BASE, {"message": ctx}, {"character_id": self.character_id, "server_id": SERVERID, "session": self.rg_sess}, direction="south")
            i += 1
    
    @commands.command()
    async def east(self, ctx, steps=1):
        i = 0
        while i < steps:
            await move_by_direction(BASE, {"message": ctx}, {"character_id": self.character_id, "server_id": SERVERID, "session": self.rg_sess}, direction="east")
            i += 1
    
    @commands.command()
    async def west(self, ctx, steps=1):
        i = 0
        while i < steps:
            await move_by_direction(BASE, {"message": ctx}, {"character_id": self.character_id, "server_id": SERVERID, "session": self.rg_sess}, direction="west")
            i += 1
    
    @commands.command()
    #####A-Star#####
    async def path(self, ctx, target_room: int):
        """Finds a path from the current room to the target room and moves step-by-step."""
        path = await a_star_search(self, {"message": ctx}, self.current_room, target_room)
        print(f"Path: {path}")
        if not path:
            await ctx.send("No valid path found.")
            return
        # For demonstration, send the entire path as text.
        msg_lines = []
        for room in enumerate(path):
            path_id = room[0]
            if path_id < len(path)-1:
                current_room_number = room[1]
                next_room_number = path[path_id+1]
                await move_to_room(BASE, {"message": ctx}, {"character_id": self.character_id, "server_id": SERVERID, "session": self.rg_sess}, str(current_room_number), str(next_room_number))
                msg_lines.append(f"Move to {next_room_number}.")    
            # Optionally, you might simulate a delay per move.
            #await asyncio.sleep(1)  # Delay per move
            self.current_room = room  # Update current room
        await ctx.send("Path found:\n" + "\n".join(msg_lines))

    @commands.command()
    async def astral(self, ctx):
        for char in chars:
            await astral(BASE, {"message": ctx}, {"character_id": char, "server_id": SERVERID, "session": self.rg_sess}, ["Astral Servant"])
    @commands.command()
    async def holy(self, ctx):
        await holy(BASE, {"message": ctx}, {"character_id": chars[0], "server_id": SERVERID, "session": self.rg_sess}, ["Holy Headhunter" "Holy Elder" "Holy Skelemech" "Holy Exterminator" "Holy Potionmaster"])

    @commands.command()
    async def alsayic(self, ctx):
        for char in chars:
            await alsayic(BASE, {"message": ctx}, {"character_id": char, "server_id": SERVERID, "session": self.rg_sess}, ["Keeper of the Alsayic Rune"])
    @commands.command()
    async def truth(self, ctx):
        for char in chars:
            await orbs(BASE, {"message": ctx}, {"character_id": char, "server_id": SERVERID, "session": self.rg_sess}, ["Initiate of Truth"])

    @commands.command()
    async def orbs(self, ctx):
        for char in chars:
            await orbs(BASE, {"message": ctx}, {"character_id": char, "server_id": SERVERID, "session": self.rg_sess})



class Skilling(commands.Cog):
    def __init__(self, bot, rg_sess, character_id):
        self.bot = bot
        self.rg_sess = rg_sess
        self.character_id = character_id
    @commands.command()
    async def lings(self, ctx):
        for char in chars:
            await underling_buff(BASE, {"message": ctx}, {"character_id": char, "server_id": SERVERID, "session": self.rg_sess})
        await ctx.send("Finished casting lings.")
    @commands.command()
    async def skill(self, ctx, skill_name):
        for char in chars:
            await get_skill_info(BASE, {"message": ctx}, {"character_id": char, "server_id": SERVERID, "session": self.rg_sess}, skill_name)
    @commands.command()
    async def cast(self, ctx, skill_name):
        for char in chars:
            await cast_skill(BASE, {"message": ctx}, {"character_id": char, "server_id": SERVERID, "session": self.rg_sess}, skill_name)

# Use an async function to properly load the cog
async def setup(bot):
    await bot.add_cog(Main(bot))