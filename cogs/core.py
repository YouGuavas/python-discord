from utils.login import login, logout 
from utils.moving import move 
from utils.attacking import attack_by_names, attack_in_a_line
from utils.questing import talk_by_name
from utils.data_functions import get_room_data

from discord.ext import commands

from config import OW_USERNAME, OW_PASSWORD, BASE, CHECKER, SERVERID
rg_sess = {}
class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")
    

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
