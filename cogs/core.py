import asyncio
import sys

from inventory.backpack import get_contents
from characters.getting import get_chars
from questing.questing import get_requirements
from utils.login import login, logout 
from utils.moving import move_by_direction, a_star_search, move_to_room
from utils.attacking import attack_by_names, spam_attack
from utils.runs import alsayic, astral, holy, orbs, orbs2, demons, truth
from utils.setting import create_tables
from utils.getting import list_tables, list_rooms, room_data, list_mobs, get_mob_data, get_room_data
from utils.skills import underling_buff, get_skill_info, cast_skill
from discord.ext import commands

if len(sys.argv) > 1:
    if sys.argv[1] == '2':
        from config import OW_USERNAME_2 as OW_USERNAME, OW_PASSWORD_2 as OW_PASSWORD
    else:
        from config import OW_USERNAME, OW_PASSWORD
else:
    from config import OW_USERNAME, OW_PASSWORD
SERVER = "sigil"

if SERVER == "torax":
    SERVERID = 2
else:
    SERVERID = 1
BASE=f"https://{SERVER}.outwar.com/"
teleports = ["10", "91", "130", "6640"]

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rg_sess = {}
        self.mains = []
        self.trustees = []
        self.chars = []
    #Login Commands
    @commands.command()
    async def sess(self, ctx):
        await ctx.send(self.rg_sess)
    @commands.command()
    async def login(self, ctx):
        await login(BASE, OW_USERNAME, OW_PASSWORD, {"message": ctx}, {"session": self.rg_sess, "server_id": SERVERID}, login)


        await self.bot.add_cog(Inventory(self))
        await self.bot.add_cog(Moving(self))
        await self.bot.add_cog(Skilling(self))
        await self.bot.add_cog(Questing(self))
        names = []
        chars = await get_chars(BASE, {"message": ctx}, {"server_id": SERVERID, "session": self.rg_sess})
        self.mains = chars[0]
        self.trustees = chars[1]
        self.chars = self.mains + self.trustees
        character_id = self.mains[0]["suid"]

        for character in self.mains:
            names.append(character["name"])

        #current_room = await(get_room_data(BASE, {"message": ctx}, {"session": self.rg_sess, "server_id": SERVERID, "character_id": character_id}))
        #current_room = current_room["data"]["current_room"]
        await ctx.send(f"Loaded up rga {OW_USERNAME}.")
        await ctx.send(f"Playable characters: {' '.join(names)}.")
        #await ctx.send(f"{self.mains[0]["name"]} current room: {current_room}")
        await ctx.send(f"Play link: {BASE}home.php?serverid={SERVERID}&rg_sess_id={self.rg_sess["session"]}&suid={character_id}")


    @commands.command()
    async def logout(self, ctx):
        await logout(BASE, {"message": ctx}, {"session": self.rg_sess, "server_id": SERVERID, "character_id": self.mains[0]})
        self.rg_sess = {}


    @commands.command()
    #Ping
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    async def select(self, ctx, *names):
        new_chars = []
        for name in names:
            for char in self.chars:
                if char["name"].lower() == name.lower():

                    new_chars.append(char)
        self.chars = new_chars
        await ctx.send(f"Successfully selected {', '.join(names)}. Ready to move.")

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
    

class Inventory(commands.Cog):
    def __init__(self, bot): #fix this - character_id
        self.bot = bot
        
    @commands.command()
    async def get_bp(self, ctx):
        contents = await get_contents(BASE, {"message": ctx}, {"character_id": self.bot.chars[0], "server_id": SERVERID, "session": self.bot.rg_sess}, "regular")
        if len(contents) == 0:
            await ctx.send("Backpack is empty!")
            return
        for item in contents:
            print(item)
    @commands.command()
    async def get_orbs(self, ctx):
        contents = await get_contents(BASE, {"message": ctx}, {"character_id": self.bot.chars[0], "server_id": SERVERID, "session": self.bot.rg_sess}, "orb")
        if len(contents) == 0:
            await ctx.send("Orbs backpack is empty!")
            return
        for item in contents:
            print(item)

    
        

        
class Moving(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Moving Commands
    
    @commands.command()
    async def north(self, ctx, steps=1, chars = []):
        if len(chars) < 1:
            chars = self.bot.chars
        for char in chars:
            i = 0
            while i < steps:
                await move_by_direction(BASE, {"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess}, direction="north")
                i += 1
    
    @commands.command()
    async def south(self, ctx,  steps=1, chars=[]):
        if len(chars) < 1:
            chars = self.bot.chars
        for char in chars:
            i = 0
            while i < steps:
                await move_by_direction(BASE, {"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess}, direction="south")
                i += 1
    
    @commands.command()
    async def east(self, ctx,  steps=1, chars=[]):
        if len(chars) < 1:
            chars = self.bot.chars
        for char in chars:
            i = 0
            while i < steps:
                await move_by_direction(BASE, {"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess}, direction="east")
                i += 1
    
    @commands.command()
    async def west(self, ctx, steps=1, chars=[]):
        if len(chars) < 1:
            chars = self.bot.chars
        for char in chars:
            i = 0
            while i < steps:
                await move_by_direction(BASE, {"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess}, direction="west")
                i += 1
    
    @commands.command()
    #####A-Star##### --- needs updating after the self refactoring
    async def path(self, ctx, target_room: int, chars=[]):
        """Finds a path from the current room to the target room and moves step-by-step."""
        for char in chars:
            current_room = await get_room_data(BASE, {"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess})
            path = await a_star_search({"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess}, current_room, target_room)
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
    async def hit_mob(self, ctx, *mobs):
        mob_rooms = []
        for mob in mobs:
            mob_rooms.append(get_mob_data({"message": ctx}, mob, False))
        
        for char in self.bot.chars:
            start_room = await get_room_data(BASE, {"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess})
            path_to = await a_star_search({"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess}, start_room, mob_rooms[0])
            for room in path_to:
                await move_to_room(BASE, {"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess}, str(start_room["data"]["current_room"]), str(room))
            await ctx.send(f"Moved {char["name"]} to area.")
            for room in mob_rooms:
                await move_to_room(BASE, {"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess}, str(start_room["data"]["current_room"]), str(room))
        await ctx.send("Finished.")

    @commands.command()
    async def astral(self, ctx):
        for char in self.bot.chars:
            await astral(BASE, {"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess}, ["Astral Servant"])
    @commands.command()
    async def holy(self, ctx):
        await holy(BASE, {"message": ctx}, {"character_id": self.bot.chars[0]["suid"], "server_id": SERVERID, "session": self.bot.rg_sess}, ["Holy Headhunter" "Holy Elder" "Holy Skelemech" "Holy Exterminator" "Holy Potionmaster"])

    @commands.command()
    async def alsayic(self, ctx):
        for char in self.bot.chars:
            await alsayic(BASE, {"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess}, ["Keeper of the Alsayic Rune"])
    @commands.command()
    async def truth(self, ctx):
        for char in self.bot.chars:
            await truth(BASE, {"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess})

    @commands.command()
    async def orbs(self, ctx):
        tasks = []
        for char in self.bot.chars:
            task = asyncio.create_task(orbs(BASE, {"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess}))
            tasks.append(task)
        for task in tasks:
            await task
    @commands.command()
    async def demons(self, ctx):
        for char in self.bot.chars:
            await demons(BASE, {"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess})
    @commands.command()
    async def orbs2(self, ctx):
        for char in self.bot.chars:
            await orbs2(BASE, {"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess})

class Questing(commands.Cog):
    def __init__(self, bot): #fix this - character_id
        self.bot = bot
    @commands.command()
    async def quest(self, ctx, quest_name="The Astral Guardian"):
        for char in self.bot.chars:
            await get_requirements(BASE, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess}, quest_name)

class Skilling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lings(self, ctx):
        for char in self.bot.chars:
            await underling_buff(BASE, {"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess})
        await ctx.send("Finished casting lings.")
    @commands.command()
    async def skill(self, ctx, skill_name):
        for char in self.bot.chars:
            await get_skill_info(BASE, {"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess}, skill_name)
    @commands.command()
    async def cast(self, ctx, skill_name):
        print("casting...")
        for char in self.bot.chars:
            await cast_skill(BASE, {"message": ctx}, {"character_id": char["suid"], "server_id": SERVERID, "session": self.bot.rg_sess}, skill_name)

# Use an async function to properly load the cog
async def setup(bot):
    await bot.add_cog(Main(bot))