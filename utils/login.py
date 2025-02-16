import requests
from urllib.parse import urlencode

async def login(user, password, url, character, channel=None, cb=None):
    try:
        # Prepare login data
        data = {            
            "serverid": character["server_id"],
            "login_username": user,
            "login_password": password,
            "submitit": ""
        }
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        }

        # Send login request
        if (character["session"] == {}):
            response = requests.post(f"{url}index.php", data=data, headers=headers, allow_redirects=False)
        else:
            if cb:
                response = await cb(user, password, url, channel, character)  # Ensure it's awaited
        # Extract session ID from cookies
        character["session"] = await get_sess(response, channel, character)
        # Check login success
        if "message" in channel:
            if response.headers.get("Location", "") != "https://sigil.outwar.com/LE=1":
                print(f"Successfully logged into rga: {user}, new session id: {character["session"]}.")
                await channel["message"].reply(f"Successfully logged into rga: {user}, new session id: {character["session"]}.")
            else:
                print(f"Could not log into rga: {user}, check login info.")
                await channel["message"].reply(f"Could not log into rga: {user}, check login info.")

    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error with the login process. Check your logs.")



async def get_sess(response, channel, character):
        try:
            await channel["message"].reply('Attempting to get session.')
            # Extract session ID from cookies
            for cookie in response.cookies:
                if cookie.name == "rg_sess_id":
                    character["session"]["session"] = cookie.value
                    await channel["message"].reply('session: '+character["session"]["session"])
                    return character["session"]
        except Exception as e:
            print(e)
            if "message" in channel:
                await channel["message"].reply("There was an error getting the session. Check your logs.")



async def logout(url, channel):
    try:
        response = requests.get(f"{url}?cmd=logout")
        if "message" in channel:
            await channel["message"].reply("Successfully logged out.")
    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("Error. Check logs.")
