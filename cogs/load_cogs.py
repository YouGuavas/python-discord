import asyncio
from discord.ext import commands

async def load_cogs(bot: commands.Bot):
    cogs = ["cogs.core"]  # Add other cogs here if needed

    for cog in cogs:
        try:
            await bot.load_extension(cog)  #Properly await loading
            print(f"Loaded {cog}")
        except Exception as e:
            print(f"Failed to load {cog}: {e}")
