import discord
from dotenv import load_dotenv
import os
from utils.login import login  # Assuming Login is a module with a login function


from discord.ext import commands


load_dotenv()
OW_USERNAME = os.getenv("OW_USERNAME")
OW_PASSWORD = os.getenv("OW_PASSWORD")
BASE = os.getenv("BASE")
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")
    @commands.command()
    async def login(self, ctx):
        rg_sess = {}
        await login(OW_USERNAME, OW_PASSWORD, BASE, {"session": rg_sess, "message": ctx}, None, login)
        await ctx.send("Login executed")
# Use an async function to properly load the cog
async def setup(bot):
    await bot.add_cog(Fun(bot))  #Await this
