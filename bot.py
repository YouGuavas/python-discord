import discord
from dotenv import load_dotenv
import os

import asyncio
from discord.ext import commands
from cogs.load_cogs import load_cogs
import ssl
import certifi

ssl_context = ssl.create_default_context(cafile=certifi.where())


# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set bot command prefix and intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Loaded commands:", [command.name for command in bot.commands])

async def main():
    async with bot:
        await load_cogs(bot)  #Await this properly
        await bot.start(TOKEN)

asyncio.run(main())  #Ensure proper async execution
