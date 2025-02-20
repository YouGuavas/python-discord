import requests
from urllib.parse import urlencode


async def get_sess(response, channel, character):
        try:
            await channel["message"].reply('Hang on, chief. Let me get a session.')
            # Extract session ID from cookies
            for cookie in response.cookies:
                if cookie.name == "rg_sess_id":
                    character["session"]["session"] = cookie.value
                    return character["session"]["session"]
        except Exception as e:
            print(e)
            if "message" in channel:
                await channel["message"].reply("Houston, we had an error getting the session.")



async def logout(url, channel, character):
    try:
        response = requests.get(f"{url}?cmd=logout")
        if "message" in channel:
            await channel["message"].reply("Successfully logged out.")
        return character["session"]
    
    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("Error. Check logs.")

async def login(url, user, password, channel, character, cb=None):
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
                response = await cb(url, user, password, channel, character)  # Ensure it's awaited
        print(character)
        session = await get_sess(response, channel, character)
        # Check login success
        if response.headers.get("Location", "") != "https://sigil.outwar.com/LE=1":
            print(f"Successfully logged into rga: {user}, new session id: {session}.")
            if "message" in channel:
                await channel["message"].reply(f"Play link: {url}home.php?serverid={character["server_id"]}&suid={character["character_id"]}&rg_sess_id={session}")
                
                # Extract session ID from cookies
            return session
        else:
            print(f"Could not log into rga: {user}, check login info.")
            if "message" in channel:
                await channel["message"].reply(f"Could not log into rga: {user}, check login info.")
            return

    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("There was an error with the login process. Check your logs.")

