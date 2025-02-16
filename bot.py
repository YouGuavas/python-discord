import discord

from config import OW_USERNAME, OW_PASSWORD, BASE, CHECKER, SERVERID, TOKEN, DISCORD_CHANNEL_ID

import asyncio
from discord.ext import commands
from cogs.load_cogs import load_cogs
from utils.login import login
from database import create_tables  # Import database functions



import ssl
import certifi

ssl_context = ssl.create_default_context(cafile=certifi.where())


# Set bot command prefix and intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # Send a message to the debug channel
    #bot.rg_sess = await login(OW_USERNAME, OW_PASSWORD, BASE, {"session": {}}, None, login)

    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send("✅ Bot started & logged into the game!")
    else:
        print("❌ Failed to find the debug channel. Check the ID.")
    print(f"Logged in as {bot.user}")
    create_tables()  # Ensures database is set up
    print("Database initialized!")
    print("Loaded commands:", [command.name for command in bot.commands])

async def main():
    async with bot:
        await load_cogs(bot)  #Await this properly
        await bot.start(TOKEN)

asyncio.run(main())  #Ensure proper async execution
