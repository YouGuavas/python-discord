import discord

from config import TOKEN, DISCORD_CHANNEL_ID

import asyncio
from discord.ext import commands
from cogs.load_cogs import load_cogs



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
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    #print(f'channel: {channel}')
    if channel:
        print("✅ Bot started & logged into the game!")
    else:
        print("❌ Failed to find the debug channel. Check the ID.")
    print(f"Logged in as {bot.user}")
    #await create_tables()  # Ensures database is set up
    #print("Database initialized!")
    print("Loaded commands:", [command.name for command in bot.commands])
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"⚠️ Error: {error}")
    print(f"Error: {error}")
async def main():
    async with bot:
        await load_cogs(bot)  #Await this properly
        await bot.start(TOKEN)

asyncio.run(main())  #Ensure proper async execution
