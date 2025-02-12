import requests
from urllib.parse import urlencode

async def login(user, password, url, channel, rg_sess=None, cb=None):
    print(user, url)
    try:
        # Prepare login data
        data = {            
            "serverid": "1",
            "login_username": user,
            "login_password": password,
            "submitit": ""
        }
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        }

        # Send login request
        if (rg_sess == None):
            response = requests.post(f"{url}index.php", data=data, headers=headers, allow_redirects=False)
        else:
            if cb:
                response = await cb(user, password, url, channel, rg_sess)  # Ensure it's awaited
        # Extract session ID from cookies
        rg_sess = await get_sess(response, channel)
        # Check login success
        if "message" in channel:
            if response.headers.get("Location", "") != "https://sigil.outwar.com/LE=1":
                await channel["message"].reply(f"Successfully logged into rga: {user}, new session id: {rg_sess}")
            else:
                await channel["message"].reply(f"Could not log into rga: {user}, check login info")

        

    except Exception as e:
        print(e)
        if "message" in channel:
            await channel["message"].reply("Error. Check logs.")

async def get_sess(response, channel):
        await channel["message"].reply('Attempting to get session.')
 # Extract session ID from cookies
        for cookie in response.cookies:
            if cookie.name == "rg_sess_id":
                rg_sess = cookie.value
                await channel["message"].reply('session: '+rg_sess)
                await set_sess(rg_sess, response)
                return rg_sess
async def set_sess(rg_sess, channel):
     # Store session if applicable
        if "session" in channel:
            channel["session"]["session"] = rg_sess


async def logout(url, stuff):
    try:
        response = requests.get(f"{url}?cmd=logout")
        if "message" in stuff:
            await stuff["message"].reply("Successfully logged out.")
    except Exception as e:
        print(e)
        if "message" in stuff:
            await stuff["message"].reply("Error. Check logs.")
