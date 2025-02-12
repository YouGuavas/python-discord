from dotenv import load_dotenv
import os
from utils.login import login 
from utils.moving import move 

from discord.ext import commands


load_dotenv()
OW_USERNAME = os.getenv("OW_USERNAME")
OW_PASSWORD = os.getenv("OW_PASSWORD")
BASE = os.getenv("BASE")
CHECKER = os.getenv("CHECKER")
SERVERID = os.getenv("SERVERID")
class Login(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rg_sess = {}

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")
    @commands.command()
    async def login(self, ctx):
        await login(OW_USERNAME, OW_PASSWORD, BASE, {"session": self.rg_sess, "message": ctx}, None, login)
        await ctx.send("Login executed")
    @commands.command()
    async def move(self, ctx):
        await move(BASE, {"message": ctx}, {"character_id": CHECKER, "server_id": SERVERID, "session": self.rg_sess})
# Use an async function to properly load the cog
async def setup(bot):
    await bot.add_cog(Login(bot))  #Await this
