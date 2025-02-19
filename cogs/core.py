from utils.login import login, logout 
from utils.moving import move, gorganus 
from utils.attacking import attack_by_names, attack_in_a_line
from utils.runs import alsayic, astral
from utils.questing import talk_by_name
from utils.data_functions import get_room_data
from utils.setting import create_tables
from utils.getting import list_tables, list_rooms, room_data, list_mobs, get_mob_data
from utils.raid import raid_by_name

from discord.ext import commands

from config import OW_USERNAME, OW_PASSWORD, BASE, CHECKER, SERVERID
rg_sess = {}
class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        await get_mob_data({"message": ctx}, False, name)
    
    @commands.command()
    #Gets Quest Mob Data -- broken
    async def quest_mob(self, ctx, name):
        await get_mob_data({"message": ctx}, True, name)

    

class Login(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sess(self, ctx):
        await ctx.send(self.rg_sess)
    @commands.command()
    async def login(self, ctx):
        await login(BASE, OW_USERNAME, OW_PASSWORD, {"message": ctx}, {"session": rg_sess, "server_id": SERVERID, "character_id": CHECKER}, login)
    @commands.command()
    async def logout(self, ctx):
        await logout(BASE, {"message": ctx}, {"session": rg_sess, "server_id": SERVERID, "character_id": CHECKER})
        rg_sess = {}

class Moving(commands.Cog):
    #Moving Commands
    @commands.command()
    async def north(self, ctx):
        await move(BASE, {"message": ctx}, {"character_id": CHECKER, "server_id": SERVERID, "session": rg_sess}, direction="north")
    @commands.command()
    async def south(self, ctx):
        await move(BASE, {"message": ctx}, {"character_id": CHECKER, "server_id": SERVERID, "session": rg_sess}, direction="south")
    @commands.command()
    async def east(self, ctx):
        await move(BASE, {"message": ctx}, {"character_id": CHECKER, "server_id": SERVERID, "session": rg_sess}, direction="east")
    @commands.command()
    async def west(self, ctx):
        await move(BASE, {"message": ctx}, {"character_id": CHECKER, "server_id": SERVERID, "session": rg_sess}, direction="west")
    '''@commands.command()
    async def raid(self, ctx, former, god_name):
        chars = ["113468", "113466", "185325", "110591", "115544", "106621", "106622", "106623", "113464"]
        await raid_by_name(BASE, {"message": ctx}, {"character_id": former, "server_id": SERVERID, "session": rg_sess}, god_name, chars)'''

    @commands.command()
    async def astral(self, ctx):
        chars = ["93021"]
        for char in chars:
            await astral(BASE, {"message": ctx}, {"character_id": char, "server_id": SERVERID, "session": rg_sess}, ["Astral Servant"])

    @commands.command()
    async def alsayic(self, ctx):
        chars = ["93021"]
        for char in chars:
            await alsayic(BASE, {"message": ctx}, {"character_id": char, "server_id": SERVERID, "session": rg_sess}, ["Keeper of the Alsayic Rune"])

    @commands.command()
    async def gorganus(self, ctx):
        chars = ["113474"]#"93021", "113469", "113375", "113468", "93023"]#"113468", "113466", "185325", "110591", "115544", "106621", "106622", "106623", "113464"]
        for char in chars:
            await gorganus(BASE, {"message": ctx}, {"character_id": char, "server_id": SERVERID, "session": rg_sess})
class Attacking(commands.Cog):
    #Attacking Commands
    @commands.command()
    async def attack(self, ctx, *mob_names):
        await attack_by_names(BASE, {"message": ctx}, {"character_id": CHECKER, "server_id": SERVERID, "session": rg_sess}, mob_names)
    @commands.command()
    async def potshot(self, ctx, loops, direction, *mob_names):
        if int(loops):
            counter = 0
            while counter < int(loops):
                await move(BASE, {"message": ctx}, {"character_id": CHECKER, "server_id": SERVERID, "session": rg_sess}, direction=direction)
                await attack_by_names(BASE, {"message": ctx}, {"character_id": CHECKER, "server_id": SERVERID, "session": rg_sess}, mob_names)
                counter += 1
            await ctx["message"].reply("Finished.")
        else:
            ctx.send("Please choose a number of loops.")
    @commands.command()
    async def orbs1(self, ctx, *mob_names):
        await attack_in_a_line(BASE, {"message": ctx}, {"character_id": CHECKER, "server_id": SERVERID, "session": rg_sess}, mob_names, 14, "north")
        self.east(self, ctx)
        await attack_in_a_line(BASE, {"message": ctx}, {"character_id": CHECKER, "server_id": SERVERID, "session": rg_sess}, mob_names, 14, "south")
class Questing(commands.Cog):
    #Questing Commands
    @commands.command()
    async def talk(self, ctx, mob_name, quest_name):
        await talk_by_name(BASE, {"message": ctx}, {"character_id": CHECKER, "server_id": SERVERID, "session": rg_sess}, mob_name, quest_name)
    @commands.command()
    async def room(self, ctx):
        await get_room_data(BASE, {"message": ctx}, {"character_id": CHECKER, "server_id": SERVERID, "session": rg_sess})

# Use an async function to properly load the cog
async def setup(bot):
    await bot.add_cog(Main(bot))
    await bot.add_cog(Login(bot))  #Await this
    await bot.add_cog(Moving(bot))
    await bot.add_cog(Attacking(bot))
    await bot.add_cog(Questing(bot))
