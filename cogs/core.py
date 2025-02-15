from utils.login import login 
from utils.moving import move 
from utils.attacking import attack_by_names

from discord.ext import commands

from config import OW_USERNAME, OW_PASSWORD, BASE, CHECKER, SERVERID

class Login(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rg_sess = {}

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")
    @commands.command()
    async def sess(self, ctx):
        await ctx.send(self.rg_sess)
    @commands.command()
    async def login(self, ctx):
        await login(OW_USERNAME, OW_PASSWORD, BASE, {"message": ctx}, {"session": self.rg_sess, "server_id": SERVERID, "character_id": CHECKER}, login)
        await ctx.send("Login executed")
    
    #Moving Commands
    @commands.command()
    async def north(self, ctx):
        await move(BASE, {"message": ctx}, {"character_id": CHECKER, "server_id": SERVERID, "session": self.rg_sess}, direction="north")
    @commands.command()
    async def south(self, ctx):
        await move(BASE, {"message": ctx}, {"character_id": CHECKER, "server_id": SERVERID, "session": self.rg_sess}, direction="south")
    @commands.command()
    async def east(self, ctx):
        await move(BASE, {"message": ctx}, {"character_id": CHECKER, "server_id": SERVERID, "session": self.rg_sess}, direction="east")
    @commands.command()
    async def west(self, ctx):
        await move(BASE, {"message": ctx}, {"character_id": CHECKER, "server_id": SERVERID, "session": self.rg_sess}, direction="west")

    #Attacking Commands
    @commands.command()
    async def attack(self, ctx, *mob_names):
        await attack_by_names(BASE, {"message": ctx}, {"character_id": CHECKER, "server_id": SERVERID, "session": self.rg_sess}, mob_names)

# Use an async function to properly load the cog
async def setup(bot):
    await bot.add_cog(Login(bot))  #Await this
