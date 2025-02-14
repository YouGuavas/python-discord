import requests
from urllib.parse import urlencode

async def login(user, password, url, channel, character, cb=None):
    try:
       print(character)
    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error with the login process. Check your logs.")